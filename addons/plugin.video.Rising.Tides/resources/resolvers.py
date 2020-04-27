import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,cookielib
from datetime import datetime,tzinfo,timedelta
import json
import base64

def resolve(url):
		import requests
		if 'tvcatchup' in url:
			open = OPEN_URL(url)
			url  = re.compile("file: '(.+?)'").findall(open)[0]
			url  = url  + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
		elif 'tvplayer' in url:
			url  = playtvplayer(url)
		elif 'sdwnet' in url:
			
			open  = OPEN_URL(url)
		
			iframe= regex_from_to(open,"iframe src='","'")
			h     = {}
			h['referer'] = url
			link = requests.session().get(iframe, headers=h, verify=False).text
			link = link.encode('ascii', 'ignore')
			url  = regex_from_to(link,'source: "','"')
			if not url.endswith=='.ts':
				url = url+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
			else:
				url    = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=%s'%url

		elif 'swiftstreams:' in url:
			url = (url).replace('swiftstreams:','')
			headers = {'Authorization': 'Basic QFN3aWZ0MTQjOkBTd2lmdDE0Iw==',
				'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)'}
			
			try:
				open = requests.session().get('http://173.212.202.101/token4004.php',headers=headers).text
			except:	
				open = requests.session().get('http://173.212.202.101/token10304.php',headers=headers).text
			if '404 Not Found' in open:
				open = requests.session().get('http://173.212.202.101/token7004.php',headers=headers).text
				
			link = url+open
			url  = link+'|User-Agent=Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q'
			

			url = url
		return (url).replace('<p>','')
	
logfile    = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.Rising.Tides', 'log.txt'))

def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	
def swiftstreamsresolve(url):
	headers = {'Authorization': 'Basic U25hcHB5OkBTbmFwcHlA',
		'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; SM-G900F Build/KTU84Q)'}
		
	open = requests.session().get('http://173.212.202.101/token10304.php',headers=headers).text
	log(open)
	link = url+open
	return link
	
def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    #print 'cookieString',cookieString
    return cookieString
	
def OPEN_URL(url):
	import requests
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
	link = requests.session().get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
    
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None,jsonpost=False):

    #ctx = ssl.create_default_context()
    #ctx.check_hostname = False
    #ctx.verify_mode = ssl.CERT_NONE

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    #opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx),cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    header_in_page=None
    if '|' in url:
        url,header_in_page=url.split('|')
    req = urllib2.Request(url)

    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Accept-Encoding','gzip')

    if headers:
        for h,hv in headers:
            req.add_header(h,hv)
    if header_in_page:
        header_in_page=header_in_page.split('&')
        
        for h in header_in_page:
            if len(h.split('='))==2:
                n,v=h.split('=')
            else:
                vals=h.split('=')
                n=vals[0]
                v='='.join(vals[1:])
                #n,v=h.split('=')
            #print n,v
            req.add_header(n,v)
            
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req,post,timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
            from StringIO import StringIO
            import gzip
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            link = f.read()
    else:
        link=response.read()
    response.close()
    return link;
    
def regex_from_to(text, from_string, to_string, excluding=True):
	import re,string
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	import re
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r