import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib,urllib2,json,urlresolver
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
from addon.common.addon import Addon
from addon.common.net import Net
from resources import control
from resources import cloudflare

addon_id   = 'script.module.whitedevil'
selfAddon  = xbmcaddon.Addon(id=addon_id)
addon      = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
art        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
afdah      = 'http://afdah.org'
ccurl      = 'http://cartooncrazy.me'
s          = requests.session()
net        = Net()
ccurl      = 'http://cartooncrazy.me'
xxxurl     ='http://www.xvideos.com'
kidsurl    = base64.b64decode ('aHR0cDovL21rb2RpLmNvLnVrL21lZGlhaHViL2xpc3RzL0tpZHMva2lkc2Nvcm5lci54bWw=')
docurl     = 'http://documentaryheaven.com'


def CAT():
	addDir('XXX SECTION','URL',31,icon,fanart,'')
	
	
def MovieCAT():
	addDir('RECENT MOVIES',afdah+'/recent_movies',19,icon,fanart,'')
	addDir('COMEDY MOVIES',afdah+'/comedy_movies',19,icon,fanart,'')
	addDir('CRIME MOVIES',afdah+'/crime_movies',19,icon,fanart,'')
	addDir('WAR MOVIES',afdah+'/war_movies',19,icon,fanart,'')
	addDir('ROMANCE MOVIES',afdah+'/romance_movies',19,icon,fanart,'')
	addDir('MUSICAL MOVIES',afdah+'/musical_movies',19,icon,fanart,'')
	addDir('SPORT MOVIES',afdah+'/sport_movies',19,icon,fanart,'')

	
def xxxCAT():
	addDir("XXXX",xxxurl+'/a',99,icon,fanart,'')

def regex_from_to(text, from_string, to_string, excluding=True):
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param


def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==3 or mode==7 or mode==17 or mode==15 or mode==23 or mode==30 or mode==27 or mode ==36:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory

def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = s.get(url, headers=headers).text
	link = link.encode('ascii', 'ignore')
	return link
	xbmcplugin.endOfDirectory

def toonlist(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>.+?art>(.+?)</art>',re.DOTALL).findall(OPEN)
    for name,url,icon,fanart in Regex:
		addDir(name,url,18,icon,fanart,'') 
	
def toon_get(url):
    OPEN = Open_Url(url)
    Regex = re.compile('&nbsp;&nbsp;<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(OPEN)
    for url,name in Regex:
            name = name.replace('&#8217;','')
            addDir(name,url,17,iconimage,fanart,'')
    np = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(OPEN)
    for url,name in np:
            if 'Next' in name:
                    addDir('[B][COLOR yellow]More >[/COLOR][/B]',url,2,iconimage,fanart,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    xbmcplugin.endOfDirectory
	
def resolvetoons(name,url,iconimage,description):
    OPEN = Open_Url(url)
    dialog = xbmcgui.Dialog()
    servers = dialog.yesno('[B][COLOR red]Stream Hub[/COLOR]', 'Please Select A Link', yeslabel='Link 1', nolabel='Link 2')
    if servers:
            url = re.compile('Playlist 1</span>.+?<iframe src="(.+?)"',re.DOTALL).findall(OPEN)[0]
            play=urlresolver.HostedMediaFile(url).resolve()

    else:
            url = re.compile('Playlist 2</span>.+?<iframe src="(.+?)"',re.DOTALL).findall(OPEN)[0]
            play=urlresolver.HostedMediaFile(url).resolve()

    try: 
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
            liz.setProperty('IsPlayable','true')
            liz.setPath(str(play))
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except: pass
	
def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def OPEN_URLafdah(url):
        headers = {}
        headers['User-Agent'] = User_Agent
        link = requests.get(url, headers=headers, allow_redirects=False).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        return link
		
def addDirafdah(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3 or mode ==15:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
	
def afdahread(url):
        url = url.replace('https','http')
        link = OPEN_URLafdah(url)
        all_videos = regex_get_all(link, 'cell_container', '<div><b>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'a title="', '\(')
                name = addon.unescape(name)
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"')
                addDirafdah(name,afdah+url,15,'http://'+thumb,fanart,'')
        try:
                match = re.compile('<a href="(.*?)\?page\=(.*?)">').findall(link)
                for url, pn in match:
                        url = afdah+url+'?page='+pn
                        addDirafdah('[I][B][COLOR red]Page %s [/COLOR][/B][/I]' %pn,url,19,icon,fanart,'')
        except: pass
        setView('movies', 'movie-view')
		
def afdahplay(url):
        url = re.split(r'#', url, re.I)[0]
        request_url = afdah+'/video_info/iframe'
        link = OPEN_URLafdah(url)
        form_data={'v': re.search(r'v\=(.*?)$',url,re.I).group(1)}
        headers = {'origin':'https://afdah.org', 'referer': url,
                   'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
        r = requests.post(request_url, data=form_data, headers=headers, allow_redirects=False)
        try:
                url = re.findall(r'url\=(.*?)"', str(r.text), re.I|re.DOTALL)[-1]
        except:
                url = re.findall(r'url\=(.*?)"', str(r.text), re.I|re.DOTALL)[0]
        url = url.replace("&amp;","&").replace('%3A',':').replace('%3D','=').replace('%2F','/')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		
def xxx(url):
        link = OPEN_URL(url)
        xxxadd_next_button(link)
        all_videos = regex_get_all(link, 'class="thumb-block ">', '</a></p>')
        for a in all_videos:
			name = regex_from_to(a, 'title="', '"')
			name = str(name).replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#039;',"'")
			url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
			thumb = regex_from_to(a, '<img src="', '"')
			setView('movies', 'movie-view')
			addDir(name,'http://www.xvideos.com'+url,27,thumb,'','')
			

def xxxadd_next_button(link):
			try:
				if '/tags/' in link:
					link = str(link).replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace('  ','')
					nextp=regex_from_to(link,'<aclass="active"href="">.+?</a></li><li><ahref="','"')
					addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',xxxurl+nextp,24,'','','')
			except: pass
			
			try:
				if '/tags/' not in link:
					link = str(link).replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace('  ','')
					nextp = regex_from_to(link,'<aclass="active"href="">.+?</a></li><li><ahref="','"')
					xbmc.log(str(nextp))
					addDir('[B][COLOR red]Next Page[/COLOR][/B]',xxxurl+nextp,24,'','','')
			except: pass
			return
			
def xxxgenre(url):
        link = passpopup(url)
        link = OPEN_URL(link)
        main = regex_from_to(link,'<strong>All tags</strong>','mobile-hide')
        all_videos = regex_get_all(main, '<li>', '</li>')
        for a in all_videos:
			name = regex_from_to(a, '"><b>', '</b><span').replace("&amp;","&")
			url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
			url = url+'/'
			thumb = regex_from_to(a, 'navbadge default">', '<')
			setView('movies', 'movie-view')
			addDir('%s     [B][COLOR red](%s Videos)[/COLOR][/B]' %(name,thumb),xxxurl+url,24,'','','')
		
def resolvexxx(url):
	base = 'http://www.xvideos.com'
	page  = OPEN_URL(url)
	page=urllib.unquote(page.encode("utf8"))
	page=str(page).replace('\t','').replace('\n','').replace('\r','').replace('                                            	','')
	play = regex_from_to(page,"setVideoUrlHigh.+?'","'")
	url = str(play).replace('[','').replace("'","").replace(']','')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
		
def passpopup(url):
 kb =xbmc.Keyboard ('', 'heading', True)
 kb.setHeading('Enter 18+ Password') # optional
 kb.setHiddenInput(True) # optional
 kb.doModal()
 if (kb.isConfirmed()):
    text = kb.getText()
    if 'pula' in text:
       text = str(text).replace('pula','/tags')
       return (str(xxxurl+text)).replace('%3a','').replace('%2f','')
    else:
        Msg="                                   Incorrect Password\n\n      Donate To john4551@hotmail.co.uk Using Paypal\n[COLOR dodgerblue]Email Or Message White Devil Group On Facebook After Donation For Password[/COLOR]"
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('Attention Donation Required', Msg)
        return False

'''def resolvecartooncrazy(url,icon):
	bypass  = cloudflare.create_scraper()
	u       = bypass.get(url).content
	embed = re.compile('<iframe src="(.+?)"').findall(u)
	embed = str(embed).replace("', '/300.html', '/300.html']","").replace('[','').replace("'","")
	get = OPEN_URL(embed)
	regex = re.compile('<iframe src=(.+?)"').findall(get)
	regex = str(regex).replace('[','').replace('"','').replace(']','').replace("'","")
	geturl = OPEN_URL(regex)
	stream = re.compile('file: "(.+?)"').findall(geturl)
	stream = str(stream).replace('[','').replace('"','').replace(']','').replace("'","")
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={"Title": name})
	liz.setProperty("IsPlayable","true")
	liz.setPath(url)
	xbmc.Player().play(stream,liz)
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def opencartooncrazy(url):
	bypass  = cloudflare.create_scraper()
	u       = bypass.get(url).content
	regex   = regex_from_to(u,'data-id="','"')
	url     = ccurl+'/ep.php?id='+regex
	#link    = regex_from_to(u,'<img src="','"')
	openurl = bypass.get(url).content
	all_videos = regex_get_all(openurl, '<tr>', '</tr>')
	for a in all_videos:
		name = regex_from_to(a, '<h2>', '</h2>')
		name = str(name).replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
		url  = regex_from_to(a, 'href="', '"')
		addDir(name,ccurl+url,30,'','','')
		
def CartooncrazyList():
    OPEN = Open_Url('http://mkodi.co.uk/streamhub/lists/cartooncrazy.xml')
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>',re.DOTALL).findall(OPEN)
    for name,url,icon in Regex:
		fanart='http://'
		addDir(name,url,34,icon,fanart,'') 
    xbmc.executebuiltin('Container.SetViewMode(50)')

def CartooncrazysubList(url):
    OPEN = Open_Url(url)
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>',re.DOTALL).findall(OPEN)
    for name,url,icon in Regex:
		fanart='http://'
		addDir(name,url,26,icon,fanart,'') 
    xbmc.executebuiltin('Container.SetViewMode(50)')'''
def documentary(url):
	OPEN = OPEN_URL(url)
	regex = regex_get_all(OPEN,'<h2><a href','alt="')
	for a in regex:
		url = regex_from_to(a,'="','"')
		title = regex_from_to(a,'">','<').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
		thumb = regex_from_to(a,'img src="','"')
		vids = regex_from_to(a,'</a> (',')</h2>').replace('(','').replace(')','')
		if vids == "":
			addDir(title,url,36,thumb,fanart,'')
		else:
			addDir(title,docurl+url,35,thumb,fanart,'')
	try:
		link = re.compile('<li class="next-btn"><a href="(.+?)"').findall(OPEN)
		link = str(link).replace('[','').replace(']','').replace("'","")
		xbmc.log(str(link))
		if link == "":
			return False
		else:
			addDir('[B][COLOR red]NEXT PAGE[/COLOR][/B]',link,35,thumb,fanart,'')
	except:pass
def resolvedoc(url):
	open = OPEN_URL(url)
	xbmc.log(str(open))
	url = regex_from_to(open,'height=".*?" src="','"')
	link = urlresolver.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(link))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

	

def setView(content, viewType):
    ''' Why recode whats allready written and works well,
    Thanks go to Eldrado for it '''
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.get_setting('auto-view') == 'true':

        print addon.get_setting(viewType)
        if addon.get_setting(viewType) == 'Info':
            VT = '504'
        elif addon.get_setting(viewType) == 'Info2':
            VT = '503'
        elif addon.get_setting(viewType) == 'Info3':
            VT = '515'
        elif addon.get_setting(viewType) == 'Fanart':
            VT = '508'
        elif addon.get_setting(viewType) == 'Poster Wrap':
            VT = '501'
        elif addon.get_setting(viewType) == 'Big List':
            VT = '51'
        elif addon.get_setting(viewType) == 'Low List':
            VT = '724'
        elif addon.get_setting(viewType) == 'Default View':
            VT = addon.get_setting('default-view')

        print viewType
        print VT
        
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ( int(VT) ) )

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )

#get = OPEN_URL(cartoons)
#xbmc.log(str(get))


params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None
# OpenELEQ: query & type-parameter (added 2 lines above)

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
# OpenELEQ: query & type-parameter (added 8 lines above)

if mode==None or url==None or len(url)<1:
	CAT()

elif mode==1:
	INDEX(url)

elif mode==2:
	INDEX2(url)

elif mode==3:
	LINKS(url)

elif mode==4:
	TV()

elif mode==6:
	EPIS(url)

elif mode==7:
	LINKS2(url,description)

elif mode==8:
	SEARCH(query,type)
# OpenELEQ: query & type-parameter (added to line above)

elif mode==9:
	GENRE(url)

elif mode==10:
	COUNTRY(url)

elif mode==11:
	YEAR(url)
	
elif mode==12:
	INDEX3(url)
	
elif mode==13:
	resolve(name,url,iconimage,description)
	
elif mode==19:
	afdahread(url)
	
elif mode==15:
	afdahplay(url)
	
elif mode==16:
	toonlist(url)
	
elif mode==17:
	resolvetoons(name,url,iconimage,description)
	
elif mode==18:
	toon_get(url)
	
elif mode==24:
	xxx(url)
	
elif mode==25:
	LiveTV()
	
elif mode==26:
	opencartooncrazy(url)
	
elif mode==27:
	resolvexxx(url)
	
elif mode==99:
	xxxgenre(url)
	
elif mode==30:
	resolvecartooncrazy(url,icon)
	
elif mode==31:
	xxxCAT()
	
elif mode==32:
	CartooncrazyList()
	
elif mode==33:
	listgenre(url)
	
elif mode==34:
	CartooncrazysubList(url)
	
elif mode==35:
	documentary(url)
	
elif mode==36:
	resolvedoc(url)
	
elif mode==98:
	xxxstars(url)
	
elif mode==100:
	MovieCAT()





xbmcplugin.endOfDirectory(int(sys.argv[1]))