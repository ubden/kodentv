import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,re,os,sys

def TVShows(name,url,iconimage):
    stringlist=''
    link=open_url(url)
    try:
        np=re.compile('<a class="nextpostslink" rel="next" href="(.+?)">.+?</a>').findall(link)[0]
        stringlist=stringlist+'<np>'+np+'<np>'
    except: pass
    shows=re.compile('<div class="kutu-resim"> <a href="(.+?)" title="(.+?)"><img style="border-width: 0px; height: .+?; width: .+?;" src="(.+?)" alt=".+?" width=".+?" height=".+?"/>',re.DOTALL).findall(link)
    for url,name,iconimage in shows:
        name=name.split('.')[0]
        string='<start>'+name+'<sep>'+url+'<sep>'+iconimage+'<end>'
        stringlist=stringlist+string
    return stringlist

def Parts(url):
    parts=[]
    link=open_url(url)
    parts.append(url)
    print parts
    fparts=re.compile('<div id="part">(.+?)<div class="video">',re.DOTALL).findall(link)[0]
    part_pages=re.compile('<a href="(.+?)"><span>').findall(fparts)
    for page in part_pages:
        parts.append(page)
    return parts
    
def Stream(url):
    link=open_url(url)
    link=open_url(url)
    host_link=re.compile('src="(.+?)"').findall(link)
    print host_link
    for host in host_link:
        if 'dailymotion' in host or 'hqq' in host:
            return host
        elif 'canlidizihd6' in host:
            link=open_url(host)
            host_link=re.compile('src="(.+?)"').findall(link)
            for host in host_link:
                if 'dailymotion' in host:
                    return host
           


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req, timeout=30)
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
