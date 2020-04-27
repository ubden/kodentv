# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse,random
from resources.lib.modules import client


def request(url, check):
    try:
        r = client.request(url)
        if r == None: return r
        if check in str(r): return r.decode('iso-8859-1').encode('utf-8')

        r = client.request(get() + urllib.quote_plus(url))
        if check in str(r): return r.decode('iso-8859-1').encode('utf-8')

        r = client.request(get() + urllib.quote_plus(url))
        if check in str(r): return r.decode('iso-8859-1').encode('utf-8')
    except:
        pass


def geturl(url):
    try:
        r = client.request(url, output='geturl')
        if r == None: return r

        host1 = re.findall('([\w]+)[.][\w]+$', urlparse.urlparse(url.strip().lower()).netloc)[0]
        host2 = re.findall('([\w]+)[.][\w]+$', urlparse.urlparse(r.strip().lower()).netloc)[0]
        if host1 == host2: return r

        r = client.request(get() + urllib.quote_plus(url), output='geturl')
        if not r == None: return parse(r)

        r = client.request(get() + urllib.quote_plus(url), output='geturl')
        if not r == None: return parse(r)
    except:
        pass


def parse(url):
    try: url = client.replaceHTMLCodes(url)
    except: pass
    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
    except: pass
    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
    except: pass
    return url


def get():
    return random.choice([
    'https://www.3proxy.us/index.php?hl=2e5&q=',
    'https://www.4proxy.us/index.php?hl=2e5&q=',
    'http://free-proxyserver.com/browse.php?b=20&u=',
    'http://www.mybriefonline.xyz/browse.php?b=20&u=',
    'http://www.navigate-online.xyz/browse.php?b=20&u=',
    'http://protectproxy.com/browse.php?b=20&u=',
    'http://proxite.net/browse.php?b=20&u=',
    'http://proxydash.com/browse.php?b=20&u=',
    'http://www.proxywebsite.us/browse.php?b=20&u=',
    'http://proxyguru.info/b.php?b=20&u=',
    'http://www.ruby-group.xyz/browse.php?b=20&u=',
    'http://securefor.com/browse.php?b=20&u=',
    'http://www.singleclick.info/browse.php?b=20&u=',
    'http://www.socialcommunication.xyz/browse.php?b=20&u=',
    'http://webproxy.stealthy.co/browse.php?b=20&u=',
    'http://www.whyproxy.com/browse.php?b=20&u=',
    'http://www.xxlproxy.com/index.php?hl=3e4&q=',
    'http://www.theprotected.xyz/browse.php?b=20&u=',
    'http://proxybrowser.org/browse.php?b=20&u=',
    'http://sslpro.eu/browse.php?b=20&u=',
    'http://webtunnel.org/browse.php?b=20&u=',
    'http://proxycloud.net/browse.php?b=20&u=',
    'http://www.onlineproxy.co.uk/browse.php?b=20&u=',
    'http://twisell.com/browse.php?b=20&u=',
    'https://www.sudoip.com/browse.php?b=20&u=',
    'http://sno9.com/browse.php?b=20&u=',
    'http://www.highlytrustedgroup.xyz/browse.php?b=20&u=',
    'http://www.medicalawaregroup.xyz/browse.php?b=20&u=',
    'http://www.onlineipchanger.com/browse.php?b=20&u=',
    'http://www.pingproxy.com/browse.php?b=20&u='
    ])


