import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,re,os,sys

def TVShows(url):

    base_url = 'http://www.ddizi1.com'

    if url == '0':
        page_num = 1
    else:
        page_num = int(url) + 1

    stringlist=''
    page = base_url + '/l.php?sayfa=' + str(page_num)
    link=open_url(page)
    try:
        next_page = int(page_num)+1
        stringlist=stringlist+'<np>'+str(next_page)+'<np>'
    except: pass
    shows=re.compile('<div class="dizi-box"><a href="(.+?)" title=".+?"><img src="(.+?)" width=".+?" height=".+?" alt=".+?" /><span class=".+?">(.+?)</span></a></div>',re.DOTALL).findall(link)
    for url,iconimage,name in shows:
        name=name.split('.')[0]
        url=url.replace('htm','htm/0')
        iconimage='http://www.ddizi1.com/'+iconimage
        string='<start>'+name+'<sep>'+url+'<sep>'+iconimage+'<end>'
        stringlist=stringlist+string
    return stringlist

def Parts(url):
    parts=[]
    link=open_url(url)
    parts.append(url)
    fparts=re.compile('<div class="dizi-parts">(.+?)<div class="dizi-video">',re.DOTALL).findall(link)[0]
    part_pages=re.compile('<a href="(.+?)">.+?</a></li>').findall(fparts)
    for page in part_pages:
        page='http://www.ddizi1.com'+page
        parts.append(page)
    return parts
    
def Stream(url):
    link=open_url(url)
    host_link=re.compile('src="(.+?)"').findall(link)
    print host_link
    for host in host_link:
        if 'dailymotion' in host or 'youtube' in host:
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
