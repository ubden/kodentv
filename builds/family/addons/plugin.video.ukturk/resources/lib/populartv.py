import urllib,urllib2,re,os,sys,base64,xbmcgui
import cfscrape
dialog = xbmcgui.Dialog()

def TVShows(url):
	print url
	stringlist=''
	scraper = cfscrape.CloudflareScraper()
	link = scraper.get(url).content
	cats = re.findall('<h2 class="listbig">(.*?)<br class="clear"',link,flags=re.DOTALL)[0]
	pattern = r'''<a\s?href=['"](.*?)['"]\s*title=['"](.*?)['"].+?>(.*?)<'''
	getcats = re.findall(pattern,cats,flags=re.DOTALL)
	for link,title,date in getcats:
			string='<start>'+title+'<sep>'+link+'<sep>'
			stringlist=stringlist+string
	return stringlist

def TVSeasons(name,url,iconimage):
	stringlist=''
	link=open_url(url)
	c = re.findall('<div class="Season">(.*?)</div>',link,flags=re.DOTALL)[0]
	pattern = '''<a\s+href='(.*?)'.+?<strong>(.*?)</a>'''
	data = re.findall(pattern,c)
	for link,name in data:
		findseason = re.compile('-s(.*?)e').findall(link)[0]
		name = name.replace('</strong>','')
		name = 'Season ' + findseason + ' | ' + name
		string='<start>'+name+'<sep>'+link+'<end>'
		stringlist=stringlist+string
	return stringlist

def TVEpisodes(name,url,iconimage):
        stringlist=''
        link=open_url(url)
        match=re.compile('<div class="tv_episode_item"> <a href="(.+?)">E(.+?)<span class="tv_episode_name"> (.+?)</span>.+?<span class="tv_episode_airdate">.+?</span>',re.DOTALL).findall(link)
        for url,ep,epname in match:
            url='http://www.gowatchfreemovies.to'+url
            string='<start>'+ep+'<sep>'+epname+'<sep>'+url+'<end>'
            stringlist=stringlist+string
        return stringlist

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    req.add_header('Referer', 'http://daddylive.info/tv/sonyten2clap.php')
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

