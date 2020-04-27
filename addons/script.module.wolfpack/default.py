import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib,urllib2,json,urlresolver
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
from addon.common.addon import Addon
from addon.common.net import Net
from resources import control
from resources import cloudflare

addon_id   = 'script.module.wolfpack'
selfAddon  = xbmcaddon.Addon(id=addon_id)
addon      = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
art        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
s          = requests.session()
net        = Net()
xxxurl     ='http://www.xvideos.com'



def CAT():
	addDir('XXX SECTION','URL',31,icon,fanart,'')

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
	
def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

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
			addDir('%s     [B][COLOR ghostwhite](%s Videos)[/COLOR][/B]' %(name,thumb),xxxurl+url,24,'','','')
		
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
    if 'thepack' in text:
       text = str(text).replace('thepack','/tags')
       return (str(xxxurl+text)).replace('%3a','').replace('%2f','')
    else:
        Msg="                                   Incorrect Password\n\n                            Password is available from\n                                [COLOR ghostwhite]Our facebook page. search Wolfpack Lives[/COLOR]"
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('Attention', Msg)
        return False

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


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

elif mode==7:
	LINKS2(url,description)

elif mode==8:
	SEARCH(query,type)
# OpenELEQ: query & type-parameter (added to line above)
	
elif mode==12:
	INDEX3(url)
	
elif mode==13:
	resolve(name,url,iconimage,description)
	
elif mode==24:
	xxx(url)
	
elif mode==27:
	resolvexxx(url)
	
elif mode==99:
	xxxgenre(url)
	
elif mode==31:
	xxxCAT()
	
elif mode==33:
	listgenre(url)
	
elif mode==98:
	xxxstars(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))