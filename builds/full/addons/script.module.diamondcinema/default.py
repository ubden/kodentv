import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib,resolveurl,urllib2,json,ssl,zipfile,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs

addon_id   = 'script.module.diamondcinema'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
s          = requests.session()

logfile    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'log.txt'))

def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	
def footballhighlight():
	open = OPEN_URL('http://livefootballvideo.com/highlights')
	all  = regex_get_all(open,'class="date_time','class="play_btn')
	for a in all:
		home = regex_from_to(a,' class="team home.+?>','&nbsp')
		away = regex_from_to(a,'class="team column".+?alt="','"')
		date = regex_from_to(a,'shortdate".+?>','<')
		score= regex_from_to(a,'class="score">','<')
		url  = regex_from_to(a,'href="','"')
		if 'span class' in score:
			score = 'Postponed'
		
		name = '[COLOR white][B]%s[/COLOR][/B]: %s v %s | %s'%(date,home,away,score)
		addDir(name,'HIGHLIGHT:'+url,113,icon,fanart,'')
		#log(t)
		
def footballreplaysget(url):
	if url.startswith('HIGHLIGHT:'):
		url = url.replace('HIGHLIGHT:','')
		open = OPEN_URL(url)
		url  = re.compile('><iframe src="(.+?)"').findall(open)[0]
	else:
		open = OPEN_URL(url)
		all  = re.findall('><iframe src="(.+?)"',open)
		d    = xbmcgui.Dialog().select('Select a Half', ['First Half: 0 - 45min', 'Second Half: 45 - 90min'])
		if d==0:
			url = all[0]
		elif d==1:
			url = all[1]
		else:
			return
	
	play=resolveurl.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		
def toongetlist(url):
	open = OPEN_URL(url)
	all  = regex_get_all(open,'<td>','</td>')
	for a in all:
		url = regex_from_to(a,'href="','"')
		name= regex_from_to(a,'">','<')
		addDir('[COLOR white]%s[/COLOR]'%name,url,52,icon,fanart,'')
		
def toongeteps(url):
		open = OPEN_URL(url)
		all  = regex_get_all(open,'&nbsp;&nbsp;','<span')
		for a in all:
			url = regex_from_to(a,'href="','"')
			name = regex_from_to(a,'">','<')
			addDir('[COLOR white]%s[/COLOR]'%name,url,53,icon,fanart,'')
			
def toongetresolve(name,url):
    OPEN = OPEN_URL(url)
    url1=regex_from_to(OPEN,'Playlist 1</span></div><div><iframe src="','"')
    url2=regex_from_to(OPEN,'Playlist 2</span></div><div><iframe src="','"')
    url3=regex_from_to(OPEN,'Playlist 3</span></div><div><iframe src="','"')
    url4=regex_from_to(OPEN,'Playlist 4</span></div><div><iframe src="','"')
    xbmc.log(str(url1))
    xbmc.log(str(url2))
    xbmc.log(str(url3))
    xbmc.log(str(url4))
    try:
			u   = OPEN_URL(url1)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url2)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url3)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url4)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:
		xbmcgui.Dialog().notification('[COLOR white]Diamond Cinema[/COLOR]','Oops... It Seems This Link Is Down!')
		
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

def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==3 or mode==7 or mode==117 or mode==17 or mode==15 or mode==113 or mode==23 or mode==30 or mode==27 or mode ==36 or mode==39 or mode==97 or mode==46 or mode==50 or mode==53 or mode==55 or mode==57 or mode==60 or mode==104 or mode==62 or mode ==75 or mode==80 or mode==90 or mode==94 or mode==105 or mode==999:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==73 or mode==1000:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory

def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = s.get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
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

elif mode==51:
	toongetlist(url)
	
elif mode==52:
	toongeteps(url)
	
elif mode==53:
	toongetresolve(name,url)
	
elif mode==113:
	footballreplaysget(url)
	
elif mode==114:
	footballhighlight()
	
elif mode==115:
	footballhighlight()
	
elif mode==999:
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Music', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

elif mode==1000:
	url = str(url).replace('\t','').replace('\r','').replace('\n','').replace(' ','%20')
	try:
		playf4m(url,name)
	except:
		pass
xbmcplugin.endOfDirectory(int(sys.argv[1]))