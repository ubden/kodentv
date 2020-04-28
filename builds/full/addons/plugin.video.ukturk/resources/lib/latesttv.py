import urllib,urllib2,re,os,sys,requests
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
dialog = xbmcgui.Dialog()
def TVShows(url):
#FIXED THIS AS REGEX WAS BROKEN
	print url
	stringlist=''
	fixdate=''
	link=requests.get(url).content
	#getdata = re.findall('''<div class="poster">(.*?)</article>''',link)[0]
	pattern = '''<div\s+class="poster">.+?href="(.*?)".+?class="serie">(.*?)<.+?<span>(.*?)<'''
	sort = re.findall(pattern,link,flags=re.DOTALL)
	for link,name,date in sort:
		string='<start>'+ date + ' | '+name+'<sep>'+link+'<end>'
		stringlist=stringlist+string
	return stringlist

def Stream(url):
    link=requests.get(url).content
    host_links=re.compile('<a target="_blank" rel="nofollow" href="(.+?)">Play</a>').findall(link)
    return host_links

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    response = urllib2.urlopen(req, timeout=10)
    link=response.read()
    link = link.replace('\n','').replace('\r','').replace('\t','')
    response.close()
    return link

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

