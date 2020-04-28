import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,re,os,sys

def STShows(url):
    stringlist=''
    link=open_url(url)
    match=re.compile('<div class="dizi" id=".+?">.+?<a href="(.+?)"><img class="diziImage" src="(.+?)?v=.+?" width=".+?" height=".+?">.+?<ul class="diziBilgi">.+?<li class="dizi_adi">(.+?)</li>',re.DOTALL).findall(link)
    for url,iconimage,name in match:
        name=name.replace("&#39;","'").replace("&#231;","c").replace("&#199;","C").replace("&#252;","u").replace("&#220;","U").replace("&#214;","O").replace("&#246;","o")
        string='<start>'+name+'<sep>'+url+'<sep>'+iconimage+'<end>'
        stringlist=stringlist+string
    return stringlist

def STEpisodes(name,url):
    stringlist=''
    link=open_url(url)
    match=re.compile('<div class="dropdown-content dropdown-scroll">(.+?)</div>',re.DOTALL).findall(link)[0]
    bolum=re.compile('<a href="javascript:;" id="" data-href="(.+?)">(.+?)</a>').findall(match)
    for url,name in bolum:
        url='http://www.showtv.com.tr'+url
        string='<start>'+name+'<sep>'+url+'<end>'
        stringlist=stringlist+string
    return stringlist

def STStream(url):
    link=open_url(url)
    host_link=re.compile('<meta name="popcorn:stream" content="(.+?)" />',re.DOTALL).findall(link)
    print host_link
    for host in host_link:
        return host


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
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
