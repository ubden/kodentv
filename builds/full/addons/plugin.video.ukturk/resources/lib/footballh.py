import urllib,urllib2,re,os,sys

def FHighlights(name,url,iconimage):
    stringlist=''
    link=open_url(url)
    try:
        np=re.compile('<span class="current">.+?</span><a href="(.+?)" class="page" title=".+?">.+?</a>',re.DOTALL).findall(link)
        for purl in np:
            stringlist=stringlist+'<np>'+purl+'<np>'
    except: pass
    match=re.compile('<div class="td_module_1 td_module_wrap td-animation-stack">.+?<div class="td-module-thumb"><a href="(.+?)" rel="bookmark" title="(.+?)"><img width=".+?" height=".+?" class="entry-thumb" src="(.+?)?resize=.+?" alt="" title=".+?" /></a></div>',re.DOTALL).findall(link)
    for url,name,iconimage in match:
        name=name.replace('&#8211;',' - ').replace('&#038;','').replace(' Full Match','')
        string='<start>'+name+'<sep>'+url+'<sep>'+iconimage+'<end>'
        stringlist=stringlist+string
    return stringlist

def FHStream(url):
    link=open_url(url)
    host_links=re.compile('<iframe.+?src=".+?" data-lazy-src="(.+?)" frameborder=',re.DOTALL).findall(link)
    return host_links

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

