# -*- coding: utf-8 -*-

import re, urllib, urlparse, random
from resources.lib.modules import client
from resources.lib.modules import utils


def get():
    return [
        #'http://dontfilter.us/browse.php?b=20&u=',
        #'http://free-proxyserver.com/browse.php?b=20&u=',
        #'http://proxite.net/browse.php?b=20&u=',
        #'http://proxycloud.net/browse.php?b=20&u=',
        #'http://securefor.com/browse.php?b=20&u=',
        #'http://webtunnel.org/browse.php?b=20&u=',
        #'http://www.onlineipchanger.com/browse.php?b=20&u=',
        #'http://www.pingproxy.com/browse.php?b=20&u=',

        'http://www.xxlproxy.com/index.php?hl=3e4&q=',
        'https://proxy-us1.toolur.com/browse.php?u=',
        'https://proxy-us2.toolur.com/browse.php?u=',
        'https://proxy-us7.toolur.com/browse.php?u=',
        'https://us1.free-proxy.com/browse.php?u=',
        'https://us2.free-proxy.com/browse.php?u=',
        'https://us6.free-proxy.com/browse.php?u='
    ]


def parse(url):
    try:
        url = client.replaceHTMLCodes(url)
    except:
        pass
    try:
        url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
    except:
        pass
    try:
        url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
    except:
        pass
    return url


def geturl(url):
    try:
        r = client.request(url, output='geturl')
        if r is None:
            return r
        host1 = re.findall('([\w]+)[.][\w]+$', urlparse.urlparse(url.strip().lower()).netloc)[0]
        host2 = re.findall('([\w]+)[.][\w]+$', urlparse.urlparse(r.strip().lower()).netloc)[0]
        if host1 == host2:
            return r
        proxies = sorted(get(), key=lambda x: random.random())
        proxies = sorted(proxies, key=lambda x: random.random())
        proxies = proxies[:3]
        for p in proxies:
            p += urllib.quote_plus(url)
            r = client.request(p, output='geturl')
            if r is not None:
                return parse(r)
    except:
        pass


def request(url, check, close=True, redirect=True, error=False, proxy=None, post=None, headers=None, mobile=False, XHR=False, limit=None, referer=None, cookie=None, compression=True, output='', timeout='30'):
    try:
        r = client.request(url, close=close, redirect=redirect, proxy=proxy, post=post, headers=headers, mobile=mobile, XHR=XHR, limit=limit, referer=referer, cookie=cookie, compression=compression, output=output, timeout=timeout)
        if r is not None and error is not False:
            return r
        if check in str(r) or str(r) == '':
            return r
        proxies = sorted(get(), key=lambda x: random.random())
        proxies = sorted(proxies, key=lambda x: random.random())
        proxies = proxies[:3]
        for p in proxies:
            p += urllib.quote_plus(url)
            if post is not None:
                if isinstance(post, dict):
                    post = utils.byteify(post)
                    post = urllib.urlencode(post)
                p += urllib.quote_plus('?%s' % post)
            r = client.request(p, close=close, redirect=redirect, proxy=proxy, headers=headers, mobile=mobile, XHR=XHR, limit=limit, referer=referer, cookie=cookie, compression=compression, output=output, timeout='20')
            if check in str(r) or str(r) == '':
                return r
    except:
        pass


