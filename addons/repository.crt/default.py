'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import sys,os
import urllib,urllib2,re,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,urlparse
import urlresolver
import random


Dialog = xbmcgui.Dialog()
Decode = base64.decodestring
addon_id='repository.crt'
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
PATH = "crt"
VERSION = "1.0"
IE_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
IOS_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
ANDROID_USER_AGENT = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
parental = 'true'

ADDONS      =  xbmc.translatePath(os.path.join('special://home','addons',''))
ART         =  os.path.join(ADDONS,addon_id,'resources','art')+os.sep
FANART      =  xbmc.translatePath(os.path.join(ADDONS,addon_id,'fanart.jpg'))
IMAGES 		= ART + 'icon.png'
BASE 		= Decode('aHR0cDovL3d3dy5hbmltZXRvb24ub3JnL2NhcnRvb24=')

import os, shutil, xbmcgui
Dialog = xbmcgui.Dialog()
addons = xbmc.translatePath('special://home/addons/')
ADDON = xbmcaddon.Addon(id=addon_id)

def Home_Menu():
    addDirFolder('[B][COLOR white]2[/COLOR][COLOR red]4/[/COLOR][COLOR white]7[/COLOR][/B]','',12,IMAGES,FANART,'')

def Random_Lists():
    Random_play('24/7 Random Cartoon',13,url=BASE,image=IMAGES,isFolder=False)
    addDirFolder('24/7 Select Cartoon','',17,IMAGES,FANART,'')
    Random_play('20 Random Movies',14,url='http://www.animetoon.org/movies',image=IMAGES,isFolder=False)

def Random_Cartoon(url):
    Playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    Playlist.clear()
    Counter = []
    full_count = []
    Prog_Name = [] 
    html=OPEN_URL(url) 
    match = re.compile('<td><a href="(.+?)">(.+?)</a></td>').findall(html) 
    for url,name in match: 
        full_count.append([url,name]) 
        if len(full_count) == len(match): 
            for item in full_count: 
                get_random=random.randint(1,len(full_count)) 
                try: 
                    url_to_add = full_count[int(get_random)] 
                except: 
                    pass 
                if url_to_add[1] not in Prog_Name:
                    Prog_Name.append(url_to_add[1]) 
                    if int(len(Counter)) < 1:
                        Counter.append(url_to_add[1][0])
                        Random_Play_Cartoon(url_to_add[0],url_to_add[1])
                    else:
                        pass
                else:
                    pass
        else:
            pass
			
def twenty47_select():
    html=OPEN_URL(BASE)
    match = re.compile('<td><a href="(.+?)">(.+?)</a></td>').findall(html)
    for url,name in match:
        Random_play(name,16,url=url,image=IMAGES,isFolder=False)
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	
		
def Random_Movie(url):
	Playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	Playlist.clear()
	Full_List = []
	Count = []
	Name = []
	HTML = OPEN_URL(url)
	match = re.compile('<td><a href="(.+?)">(.+?)</a></td>').findall(HTML)
	for url2,name in match:
		Full_List.append([url2,name])
		if len(Full_List)==len(match):
			for item in Full_List:
				random_movie=random.randint(1,len(Full_List))
				try:
					next_url = Full_List[int(random_movie)]
				except:
					pass
				if len(Count)<=20:
					if next_url[1] not in Name:
						HTML2 = OPEN_URL(next_url[0])
						match3 = re.compile('&nbsp;<a href="(.+?)">(.+?)</a>').findall(HTML2) 
						for Playlink_url,Ep_name in match3: 
							HTML4 = OPEN_URL(Playlink_url)
							match4 = re.compile('"playlist">(.+?)</span></div><div><iframe src="(.+?)"').findall(HTML4)
							for ignore,link in match4:
								if 'panda' in link:
									HTML5 = OPEN_URL(link)
									match5 = re.compile("url: '(.+?)'").findall(HTML5)
									for finally_got_there_phew in match5:
										if 'http' in finally_got_there_phew:
											liz = xbmcgui.ListItem(next_url[1], iconImage=IMAGES, thumbnailImage=IMAGES)
											liz.setInfo( type="Video", infoLabels={"Title": next_url[1]})
											liz.setProperty("IsPlayable","true")
											Playlist.add(finally_got_there_phew, liz)
											xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
									
			
		
	
def Random_Play_Cartoon(url,name):
    url = url;name = name
    Playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    Playlist.clear()
    episode_full_count = []
    Ep_Name_List = []
    html2 = OPEN_URL(url) 
    match2 = re.compile('<img src="(.+?)" id="series_image" width="250" height="370" alt=".+?" />').findall(html2) 
    for img in match2: 
        IMAGE = img 
    match3 = re.compile('&nbsp;<a href="(.+?)">(.+?)</a>').findall(html2) 
    for Playlink_url,Ep_name in match3: 
        episode_full_count.append([Playlink_url,Ep_name]) 
        if len(episode_full_count)==len(match3):
            for item in episode_full_count:
                get_random_ep=random.randint(1,len(episode_full_count))
                try:									
                    next_url_to_use=episode_full_count[int(get_random_ep)]
                    if next_url_to_use[1] not in Ep_Name_List:
                        Ep_Name_List.append(next_url_to_use[1])
                        html3 = OPEN_URL(next_url_to_use[0])
                        match4 = re.compile('"playlist">(.+?)</span></div><div><iframe src="(.+?)"').findall(html3)
                        for ignore,final_playlink_get in match4:
                            if 'panda' in final_playlink_get:
                                html4 = OPEN_URL(final_playlink_get)
                                match5 = re.compile("url: '(.+?)'").findall(html4)
                                for finally_got_there_phew in match5:
                                    if 'http' in finally_got_there_phew:
                                        liz = xbmcgui.ListItem(next_url_to_use[1], iconImage=IMAGE, thumbnailImage=IMAGE)
                                        liz.setInfo( type="Video", infoLabels={"Title": next_url_to_use[1]})
                                        liz.setProperty("IsPlayable","true")
                                        Playlist.add(finally_got_there_phew, liz)
                                        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
                                    else:
                                        pass
                            else:
                                pass
                    else:
                        pass
                except:
                    pass
        else:
            pass
                    
	
def watch_cartoon_menu():
    addDirFolder('Cartoons','https://www.watchcartoononline.io/cartoon-list',7,IMAGES,FANART,'')
    addDirFolder('Movies','https://www.watchcartoononline.io/movie-list',9,IMAGES,FANART,'')

def watch_cartoon_grab_episode(url):
	html = OPEN_URL(url)
	match = re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a>').findall(html)
	for url, name in match:
		name = name.replace('&#8217;','\'').replace('&#8216;','\'').replace('&#038;','&').replace('&#8211;','-')
		if '<' in name:
			pass
		else:
			addDirFolder(name,url,10,IMAGES,FANART,'')
			
def watch_cartoon_grab_episode_second(url):
	html = OPEN_URL(url)
	match = re.compile('<li><a href="(.+?)" rel="bookmark" title=".+?" class="sonra">(.+?)</a>').findall(html)
	for url, name in match:
		name = name.replace('&#8217;','\'').replace('&#8216;','\'').replace('&#038;','&').replace('&#8211;','-')
		if '<' in name:
			pass
		else:
			addDir(name,url,8,IMAGES,FANART,'')
			
def watch_cartoon_grab_movies(url):
	html = OPEN_URL(url)
	match = re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a>').findall(html)
	for url, name in match:
		name = name.replace('&#8217;','\'').replace('&#8216;','\'').replace('&#038;','&').replace('&#8211;','-')
		if '<' in name:
			pass
		else:
			addDir(name,url,8,IMAGES,FANART,'')
			
def watch_cartoon_final(url):
	url = url.replace('www','m')
	html = OPEN_URL(url)
	playlink = re.compile('<source src="(.+?)"').findall(html)
	for play in playlink:
		Resolve(play)

	
def Search_cartoons():
    Search_Name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    HTML = OPEN_URL(BASE)
    match = re.compile('<td><a href="(.+?)">(.+)</a></td>').findall(HTML)
    for url,name in match:
        if Search_Name.replace(' ','').replace('\'','').replace('-','').lower() in name.replace(' ','').replace('\'','').replace('-','').lower():
            addDirFolder('Source 1 - '+name,url,3,IMAGES,FANART,'')
    HTML2 = OPEN_URL('https://www.watchcartoononline.io/cartoon-list')
    match = re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a>').findall(HTML2)
    for url, name in match:
        if Search_Name.replace(' ','').replace('\'','').replace('-','').lower() in name.replace(' ','').replace('\'','').replace('-','').lower():
            addDirFolder(name,url,10,IMAGES,FANART,'')
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	

def Search_movies():
    Search_Name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    HTML = OPEN_URL('https://www.watchcartoononline.io/movie-list')
    match = re.compile('<li><a href="(.+?)" title=".+?">(.+?)</a>').findall(HTML)
    for url, name in match:
        name = name.replace('&#8217;','\'').replace('&#8216;','\'').replace('&#038;','&').replace('&#8211;','-')
        if '<' in name:
            pass
        else:
            if Search_Name.replace(' ','').replace('\'','').replace('-','').lower() in name.replace(' ','').replace('\'','').replace('-','').lower():
                addDir(name,url,8,IMAGES,FANART,'')
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	
	
	
def TESTCATS():
    html=OPEN_URL(BASE)
    match = re.compile('<td><a href="(.+?)">(.+?)</a></td>').findall(html)
    for url,name in match:
        addDirFolder(name,url,3,IMAGES,FANART,'')
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	
    
def LISTS(url):
    html=OPEN_URL(url)
    match2 = re.compile('<img src="(.+?)" id="series_image" width="250" height="370" alt=".+?" />').findall(html)
    for img in match2:
        IMAGE = img
    match = re.compile('&nbsp;<a href="(.+?)">(.+?)</a>').findall(html)
    for url,name in match:
        addDirFolder(name,url,4,IMAGE,FANART,'')
    match3 = re.compile('<li><a href="(.+?)">Next</a></li>').findall(html)
    for url in match3:
	    addDirFolder('NEXT PAGE',url,3,IMAGE,FANART,'')
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	
	

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	

def LISTS2(url,IMAGE):
    sources = []
    html=OPEN_URL(url)
    match = re.compile('"playlist">(.+?)</span></div><div><iframe src="(.+?)"').findall(html)
    for name,url2 in match:
        if 'panda' in url2:
            HTML = OPEN_URL(url2)
            match2 = re.compile("url: '(.+?)'").findall(HTML)
            for url3 in match2:
                if 'http' in url3:
					sources.append({'source': 'playpanda', 'quality': 'SD', 'url': url3})
        elif 'easy' in url2:
            HTML2 = OPEN_URL(url2)
            match3 = re.compile("url: '(.+?)'").findall(HTML2)
            for url3 in match3:
                if 'http' in url3:
					sources.append({'source': 'easyvideo', 'quality': 'SD', 'url': url3})
        elif 'zoo' in url2:
            HTML3 = OPEN_URL(url2)
            match4 = re.compile("url: '(.+?)'").findall(HTML3)
            for url3 in match4:
                if 'http' in url3:
					sources.append({'source': 'videozoo', 'quality': 'SD', 'url': url3})
    if len(sources)>=3:
    	choice = Dialog.select('Select Playlink',
	                                [link["source"] + " - " + " (" + link["quality"] + ")"
	                                for link in sources])
        if choice != -1:
            url = sources[choice]['url']
            isFolder=False
            xbmc.Player().play(url)
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);			

def LISTS3(url):
    html=OPEN_URL(url)
    match = re.compile("url: '(.+?)',").findall(html)
    for url in match:
        Resolve(url)

def Random_play(name, mode, url='', image=None, isFolder=True, page=1, keyword=None, infoLabels=None, contextMenu=None):
    if not image:
        image = ICON
    u  = sys.argv[0] 
    u += '?mode='  + str(mode)
    u += '&title=' + urllib.quote_plus(name)
    u += '&image=' + urllib.quote_plus(image)
    u += '&page='  + str(page)
    if url != '':     
        u += '&url='   + urllib.quote_plus(url) 
    if keyword:
        u += '&keyword=' + urllib.quote_plus(keyword) 
    liz = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
    if contextMenu:
        liz.addContextMenuItems(contextMenu)
    if infoLabels:
        liz.setInfo(type="Video", infoLabels=infoLabels)
    if not isFolder:
        liz.setProperty("IsPlayable","true")
    liz.setProperty('Fanart_Image', FANART)     
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)
		

def addDir(name,url,mode,iconimage,fanart,description):

        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDirFolder(name,url,mode,iconimage,fanart,description):

        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

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
iconimage=None
mode=None
description=None


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
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

def Resolve(url): 
	import urlresolver
	try:
		resolved_url = urlresolver.resolve(url)
		xbmc.Player().play(resolved_url, xbmcgui.ListItem(name))
	except:
		xbmc.Player().play(url, xbmcgui.ListItem(name))
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def OPEN_URL(url):
        req = urllib2.Request(url)
        IE_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
        FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
        IOS_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
        ANDROID_USER_AGENT = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def setView(content, viewType):
	if content:
	    xbmcplugin.setContent(int(sys.argv[1]), content)


if mode == None     : Home_Menu()
elif mode == 1 		: TESTCATS()
elif mode == 2    	: Search_cartoons()
elif mode == 3    	: LISTS(url)
elif mode == 4    	: LISTS2(url,iconimage)
elif mode == 5    	: Resolve(url)
elif mode == 6 		: watch_cartoon_menu()
elif mode == 7 		: watch_cartoon_grab_episode(url)
elif mode == 8 		: watch_cartoon_final(url)
elif mode == 9 		: watch_cartoon_grab_movies(url)
elif mode == 10 	: watch_cartoon_grab_episode_second(url)
elif mode == 11 	: Search_movies()
elif mode == 12 	: Random_Lists()
elif mode == 13 	: Random_Cartoon(url)
elif mode == 14 	: Random_Movie(url)
elif mode == 16 	: Random_Play_Cartoon(url,name)
elif mode == 17 	: twenty47_select()

xbmcplugin.endOfDirectory(int(sys.argv[1]))