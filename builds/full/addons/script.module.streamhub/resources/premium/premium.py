 #############Imports#############
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,base64,os,re,unicodedata,requests,time,string,sys,urllib,urllib2,json,urlparse,datetime,zipfile,shutil
from resources.premium.modules import client,control,tools,user
from datetime import date
import xml.etree.ElementTree as ElementTree


#################################

#############Defined Strings#############
icon         = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/premium', 'icon.png'))
fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/premium', 'fanart.jpg'))

username     = xbmcaddon.Addon('plugin.video.streamhub').getSetting('Username')
password     = xbmcaddon.Addon('plugin.video.streamhub').getSetting('Password')

live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(user.host,user.port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(user.host,user.port,username,password)
panel_api    = '%s:%s/panel_api.php?username=%s&password=%s'%(user.host,user.port,username,password)
play_url     = '%s:%s/live/%s/%s/'%(user.host,user.port,username,password)

premium_jpg = xbmc.translatePath(os.path.join('special://home/addons/addons/'+user.id + '/resources/premium', 'premium.jpg'))

advanced_settings           =  xbmc.translatePath('special://home/addons/'+user.id + '/resources/premium/advanced_settings')
advanced_settings_target    =  xbmc.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))

KODIV        = float(xbmc.getInfoLabel("System.BuildVersion")[:4])

logfile    = xbmc.translatePath(os.path.join('special://home/addons/' + user.id, 'log.txt'))


#########################################

def log(text):
	file = open(logfile,"w+")
	file.write(str(text))


def buildcleanurl(url):
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	return url
	
def start(type):
		username     = xbmcaddon.Addon('plugin.video.streamhub').getSetting('Username')
		password     = xbmcaddon.Addon('plugin.video.streamhub').getSetting('Password')
		auth = '%s:%s/panel_api.php?username=%s&password=%s'%(user.host,user.port,username,password)
		auth = tools.OPEN_URL(auth)
		if "username" in auth:
			exp = tools.regex_from_to(auth,'"status":"','"')
			if exp == 'Expired':
				xbmcgui.Dialog().ok(user.name,'Your Account Has Expired! %s'%username,'You Can Renew At: http://facebook.com/groups/streamh')
				sys.exit()
			if type=="NEW":
				xbmcgui.Dialog().ok(user.name, 'Welcome To %s, %s'%(user.name,username), 'Thankyou For Donating And I Hope You Enjoy Your Subscription', 'Please Continue With The Setup Guide')
				tvguidesetup()
				addonsettings('ADS2','')
				xbmc.executebuiltin('Container.Refresh')
			tools.addDir('[COLOR ffff0000][B]M[/COLOR][COLOR white]y Premium Information[/COLOR][/B]','url',999996,'https://s18.postimg.org/rhnmrvxp5/myinfo.png',fanart,"Access Your Account Information, Inlcuding Username, Password and More")
			tools.addDir('[COLOR ffff0000][B]L[/COLOR][COLOR white]ive Tv[/COLOR][/B]','url',999991,'https://s18.postimg.org/ggshmv5g9/livetv.png',fanart,"Get Access to All of Your Favourite Channels, In Stunning HD")
			tools.addDir('[COLOR ffff0000][B]L[/COLOR][COLOR white]ive Events[/COLOR][/B]','LIVE',999991,'https://s18.postimg.org/ggshmv5g9/livetv.png',fanart,"Containing Live Events, Including: NBA, NFL, NHL, MLB, English Premier League and PPV!")
			tools.addDir('[COLOR ffff0000][B]C[/COLOR][COLOR white]atchup Tv[/COLOR][/B]','url',9999912,'https://s18.postimg.org/wp8pwceah/CATCHUP.png',fanart,"Get Access To Full 7 Days Catchup Tv On A Whole Bunch Of Channels!")
			if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
				tools.addDir('[COLOR ffff0000][B]T[/COLOR][COLOR white]V Guide[/COLOR][/B]','pvr',999997,'https://s18.postimg.org/479gw7l95/TVGUIDE.png',fanart,"Open Kodi's Inbuilt Tv Guide")
			tools.addDir('[COLOR ffff0000][B]O[/COLOR][COLOR white]n Demand[/COLOR][/B]','vod',999993,'https://s18.postimg.org/82cuys4ex/VOD.png',fanart,'')
			tools.addDir('[COLOR ffff0000][B]S[/COLOR][COLOR white]earch[/COLOR][/B]','url',999995,'https://s2.postimg.org/oeceg5ort/search.png',fanart,"Search Through StreamHub's Premium Content")
			tools.addDir('[COLOR ffff0000][B]E[/COLOR][COLOR white]xtras[/COLOR][/B]','url',9999916,'https://s18.postimg.org/i7biocmzd/extras.png',fanart,"Some Extra Features, Inlcuding Football Guides. Setting Tweaks and More")
		else:
			d = xbmcgui.Dialog().yesno(user.name, 'Your Login Details Are Incorrect, Would You Like To Re-Enter?')
			if not d:
				sys.exit()
			else:
				xbmcaddon.Addon('plugin.video.streamhub').openSettings()
				if type == "NEW":
					type = 'NEW'
				else:
					type = 'NONE'
				start(type)
def home():
			tools.addDir('[COLOR ffff0000][B]M[/COLOR][COLOR white]y Premium Information[/COLOR][/B]','url',999996,'https://s18.postimg.org/rhnmrvxp5/myinfo.png',fanart,'')
			tools.addDir('[COLOR ffff0000][B]L[/COLOR][COLOR white]ive Tv[/COLOR][/B]','live',999991,'https://s18.postimg.org/ggshmv5g9/livetv.png',fanart,'')
			tools.addDir('[COLOR ffff0000][B]L[/COLOR][COLOR white]ive Events[/COLOR][/B]','live',999991,'https://s18.postimg.org/ggshmv5g9/livetv.png',fanart,'')
			tools.addDir('[COLOR ffff0000][B]C[/COLOR][COLOR white]atchup Tv[/COLOR][/B]','url',9999912,'https://s18.postimg.org/wp8pwceah/CATCHUP.png',fanart,'')
			if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
				tools.addDir('[COLOR ffff0000][B]T[/COLOR][COLOR white]V Guide[/COLOR][/B]','pvr',999997,'https://s18.postimg.org/479gw7l95/TVGUIDE.png',fanart,'')
			tools.addDir('[COLOR ffff0000][B]O[/COLOR][COLOR white]n Demand[/COLOR][/B]','vod',999993,'https://s18.postimg.org/82cuys4ex/VOD.png',fanart,'')
			tools.addDir('[COLOR ffff0000][B]S[/COLOR][COLOR white]earch[/COLOR][/B]','url',999995,'https://s2.postimg.org/oeceg5ort/search.png',fanart,'')
			tools.addDir('[COLOR ffff0000][B]E[/COLOR][COLOR white]xtras[/COLOR][/B]','url',9999916,'https://s18.postimg.org/i7biocmzd/extras.png',fanart,'')			
def livecategory(url):
	
	open = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		if not 'Install Videos' in name:
			if not 'TEST CHANNELS' in name:
				if not 'TEST' in name:
					if url == 'LIVE':
						if 'Live:' in name:	
							tools.addDir(name.replace('UK:','[COLOR ffff0000][B]UK:[/COLOR][/B]').replace('USA/CA:','[COLOR ffff0000][B]USA/CA:[/COLOR][/B]').replace('All','[COLOR ffff0000][B]All[/COLOR][/B]').replace('International Sport','[COLOR ffff0000][B]INT: [/COLOR][/B]International Sport').replace('Live:','[COLOR ffff0000][B]Live:[/COLOR][/B]').replace('TEST','[COLOR ffff0000][B]TEST[/COLOR][/B]').replace('Install','[COLOR ffff0000][B]Install[/COLOR][/B]').replace('24/7','[COLOR ffff0000][B]24/7: [/COLOR][/B]Channels').replace('DE:','[COLOR ffff0000][B]DE:[/COLOR][/B]').replace('FR:','[COLOR ffff0000][B]FR:[/COLOR][/B]').replace('PL:','[COLOR ffff0000][B]PL:[/COLOR][/B]').replace('AR:','[COLOR ffff0000][B]AR:[/COLOR][/B]').replace('LIVE:','[COLOR ffff0000][B]LIVE:[/COLOR][/B]').replace('ES:','[COLOR ffff0000][B]ES:[/COLOR][/B]').replace('IN:','[COLOR ffff0000][B]IN:[/COLOR][/B]').replace('PK:','[COLOR ffff0000][B]PK:[/COLOR][/B]').replace('NBC Extra Time','[COLOR ffff0000][B]NBC:[/COLOR][/B] NBC Extra Time'),url1,999992,icon,fanart,'')
					else:
						if not 'Live:' in name:	
							tools.addDir(name.replace('UK:','[COLOR ffff0000][B]UK:[/COLOR][/B]').replace('USA/CA:','[COLOR ffff0000][B]USA/CA:[/COLOR][/B]').replace('All','[COLOR ffff0000][B]All[/COLOR][/B]').replace('International Sport','[COLOR ffff0000][B]INT: [/COLOR][/B]International Sport').replace('Live:','[COLOR ffff0000][B]Live:[/COLOR][/B]').replace('TEST','[COLOR ffff0000][B]TEST[/COLOR][/B]').replace('Install','[COLOR ffff0000][B]Install[/COLOR][/B]').replace('24/7','[COLOR ffff0000][B]24/7: [/COLOR][/B]Channels').replace('DE:','[COLOR ffff0000][B]DE:[/COLOR][/B]').replace('FR:','[COLOR ffff0000][B]FR:[/COLOR][/B]').replace('PL:','[COLOR ffff0000][B]PL:[/COLOR][/B]').replace('AR:','[COLOR ffff0000][B]AR:[/COLOR][/B]').replace('LIVE:','[COLOR ffff0000][B]LIVE:[/COLOR][/B]').replace('ES:','[COLOR ffff0000][B]ES:[/COLOR][/B]').replace('IN:','[COLOR ffff0000][B]IN:[/COLOR][/B]').replace('PK:','[COLOR ffff0000][B]PK:[/COLOR][/B]').replace('NBC Extra Time','[COLOR ffff0000][B]NBC:[/COLOR][/B] NBC Extra Time'),url1,999992,icon,fanart,'')
def Livelist(url):
	url  = buildcleanurl(url)
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		name = re.sub('\[.*?min ','-',name)
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		tools.addDir(name.replace('UK:','[COLOR ffff0000][B]UK:[/COLOR][/B]').replace('USA/CA:','[COLOR ffff0000][B]USA/CA:[/COLOR][/B]').replace('All','[COLOR ffff0000][B]A[/COLOR][/B]ll').replace('International','[COLOR ffff0000][B]Int[/COLOR][/B]ertaional').replace('Live:','[COLOR ffff0000][B]Live:[/COLOR][/B]').replace('TEST','[COLOR ffff0000][B]TEST[/COLOR][/B]').replace('Install','[COLOR ffff0000][B]Install[/COLOR][/B]').replace('24/7','[COLOR ffff0000][B]24/7[/COLOR][/B]').replace('INT:','[COLOR ffff0000][B]INT:[/COLOR][/B]').replace('DE:','[COLOR ffff0000][B]DE:[/COLOR][/B]').replace('FR:','[COLOR ffff0000][B]FR:[/COLOR][/B]').replace('PL:','[COLOR ffff0000][B]PL:[/COLOR][/B]').replace('AR:','[COLOR ffff0000][B]AR:[/COLOR][/B]').replace('LIVE:','[COLOR ffff0000][B]LIVE:[/COLOR][/B]').replace('ES:','[COLOR ffff0000][B]ES:[/COLOR][/B]').replace('IN:','[COLOR ffff0000][B]IN:[/COLOR][/B]').replace('PK:','[COLOR ffff0000][B]PK:[/COLOR][/B]'),url1,999994,thumb,fanart,base64.b64decode(desc))
		
	
def vod(url):
	if url =="vod":
		open = tools.OPEN_URL(vod_url)
	else:
		url  = buildcleanurl(url)
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = tools.regex_from_to(a,'<title>','</title>')
			url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
			tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,999993,icon,fanart,'')
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.regex_from_to(a,'<title>','</title>')
					name = base64.b64decode(name)
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					desc = tools.regex_from_to(a,'<description>','</description>')
					desc = base64.b64decode(desc)
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[/COLOR][/B].','.[/COLOR][/B]'),url,999994,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			else:
				name = tools.regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
				desc = tools.regex_from_to(a,'<description>','</description>')
				tools.addDir(name,url,999994,thumb,fanart,base64.b64decode(desc))
				
				
		
##############################################
#### RULE NO.1 - DONT WRITE CODE THAT IS  ####
#### ALREADY WRITTEN AND PROVEN TO WORK :)####
##############################################


def catchup():
    listcatchup()
		
def listcatchup():
	open = tools.OPEN_URL(panel_api)
	all  = tools.regex_get_all(open,'{"num','direct')
	for a in all:
		if '"tv_archive":1' in a:
			name = tools.regex_from_to(a,'"epg_channel_id":"','"').replace('\/','/')
			thumb= tools.regex_from_to(a,'"stream_icon":"','"').replace('\/','/')
			id   = tools.regex_from_to(a,'stream_id":"','"')
			if not name=="":
				name = name.replace('ENT:','[B]ENT:[/B]').replace('KID:','[B]KID:[/B]').replace('MOV:','[B]MOV:[/B]').replace('DOC:','[B]DOC:[/B]').replace('SSS:','[B]SSS:[/B]').replace('BTS:','[B]BTS:[/B]').replace('UKS:','[B]UKS:[/B]')
				tools.addDir(name,'url',9999913,thumb,fanart,id)
			

def tvarchive(name,description):
    days = 7
	
    now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
    date3 = datetime.datetime.now() - datetime.timedelta(days)
    date = str(date3)
    date = str(date).replace('-','').replace(':','').replace(' ','')
    APIv2 = base64.b64decode("JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF9zaW1wbGVfZGF0YV90YWJsZSZzdHJlYW1faWQ9JXM=")%(user.host,user.port,username,password,description)
    link=tools.OPEN_URL(APIv2)
    match = re.compile('"title":"(.+?)".+?"start":"(.+?)","end":"(.+?)","description":"(.+?)"').findall(link)
    for ShowTitle,start,end,DesC in match:
        ShowTitle = base64.b64decode(ShowTitle)
        DesC = base64.b64decode(DesC)
        format = '%Y-%m-%d %H:%M:%S'
        try:
            modend = dtdeep.strptime(end, format)
            modstart = dtdeep.strptime(start, format)
        except:
            modend = datetime.datetime(*(time.strptime(end, format)[0:6]))
            modstart = datetime.datetime(*(time.strptime(start, format)[0:6]))
        StreamDuration = modend - modstart
        modend_ts = time.mktime(modend.timetuple())
        modstart_ts = time.mktime(modstart.timetuple())
        FinalDuration = int(modend_ts-modstart_ts) / 60
        strstart = start
        Realstart = str(strstart).replace('-','').replace(':','').replace(' ','')
        start2 = start[:-3]
        editstart = start2
        start2 = str(start2).replace(' ',' - ')
        start = str(editstart).replace(' ',':')
        Editstart = start[:13] + '-' + start[13:]
        Finalstart = Editstart.replace('-:','-')
        if Realstart > date:
            if Realstart < now:
                catchupURL = base64.b64decode("JXM6JXMvc3RyZWFtaW5nL3RpbWVzaGlmdC5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmc3RyZWFtPSVzJnN0YXJ0PQ==")%(user.host,user.port,username,password,description)
                ResultURL = catchupURL + str(Finalstart) + "&duration=%s"%(FinalDuration)
                kanalinimi = "[COLOR white]%s[/COLOR] - %s"%(start2,ShowTitle)
                tools.addDir(kanalinimi,ResultURL,999994,icon,fanart,DesC)

	
					
def DownloaderClass(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create('Fetching latest Catch Up',"Fetching latest Catch Up...",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR white]%.02f MB of less than 5MB[/COLOR][/B]' % (currently_downloaded)
            e = '[COLOR white]Speed:  %.02f Mb/s ' % mbps_speed  + '[/COLOR][/B]'
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled():
            dialog = xbmcgui.Dialog()
            dialog.ok(user.name, 'The download was cancelled.')
				
            sys.exit()
            dp.close()
#####################################################################

def tvguide():
		xbmc.executebuiltin('ActivateWindow(TVGuide)')
def stream_video(url):
	url = buildcleanurl(url)
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def searchdialog():
	search = control.inputDialog(heading='Search '+user.name+':')
	if search=="":
		return
	else:
		return search

	
def search():
	text = searchdialog()
	if not text:
		xbmc.executebuiltin("XBMC.Notification([COLOR white][B]Search is Empty[/B][/COLOR][/B],Aborting search,4000,"+icon+")")
		return
	xbmc.log(str(text))
	open = tools.OPEN_URL(panel_api)
	all_chans = tools.regex_get_all(open,'{"num":','epg')
	for a in all_chans:
		name = tools.regex_from_to(a,'name":"','"').replace('\/','/')
		url  = tools.regex_from_to(a,'"stream_id":"','"')
		thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
		if text in name.lower():
			tools.addDir(name,play_url+url+'.ts',999994,thumb,fanart,'')
		elif text not in name.lower() and text in name:
			tools.addDir(name,play_url+url+'.ts',999994,thumb,fanart,'')

	
def settingsmenu():
	if xbmcaddon.Addon().getSetting('meta')=='true':
		META = '[COLOR lime]ON[/COLOR][/B]'
	else:
		META = '[COLOR red]OFF[/COLOR][/B]'
	if xbmcaddon.Addon().getSetting('update')=='true':
		UPDATE = '[COLOR lime]ON[/COLOR][/B]'
	else:
		UPDATE = '[COLOR red]OFF[/COLOR][/B]'
	tools.addDir('Edit Advanced Settings','ADS',10,icon,fanart,'')
	tools.addDir('META for VOD is %s'%META,'META',10,icon,fanart,META)
	tools.addDir('Log Out','LO',10,icon,fanart,'')
	
def editas():

		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==5:
			advancedsettings('remove')
			xbmcgui.Dialog().ok(user.name, 'Advanced Settings Removed')

def addonsettings(url,description):
	url  = buildcleanurl(url)
	if   url =="CC":
		tools.clear_cache()
	elif url =="m3unepg":
		m3uselector()
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'%user.id)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==5:
			advancedsettings('remove')
			xbmcgui.Dialog().ok(user.name, 'Advanced Settings Removed')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
	elif url =="tv":
		dialog = xbmcgui.Dialog().yesno(user.name,'Would You like us to Setup the TV Guide for You?')
		if dialog:
			pvrsetup()
			xbmcgui.Dialog().ok(user.name, 'PVR Integration Complete')
	elif url =="ST":
		xbmc.executebuiltin('Runscript("special://home/addons/'+user.id+'/resources/modules/speedtest.py")')
	elif url =="VODSOURCE":
		if 'ON' in description:
			xbmcaddon.Addon('plugin.video.streamhub').setSetting('vodsource','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon('plugin.video.streamhub').setSetting('vodsource','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="LO":
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')
			
	elif url.endswith('.apk'):
		from resources.premium.modules import apkinstaller
		apkinstaller.install(description,url)
	
		
def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(advanced_settings_target)
	
	try:
		read = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(read)
		f.close()
	except:
		pass
		
		
def userpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Username')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

		
def passpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Password')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False
		
		
def accountinfo():
	try:
		open = tools.OPEN_URL(panel_api)
		username   = tools.regex_from_to(open,'"username":"','"')
		password   = tools.regex_from_to(open,'"password":"','"')
		status     = tools.regex_from_to(open,'"status":"','"')
		connects   = tools.regex_from_to(open,'"max_connections":"','"')
		active     = tools.regex_from_to(open,'"active_cons":"','"')
		expiry     = tools.regex_from_to(open,'"exp_date":"','"')
		expiry     = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
		expreg     = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
		for day,month,year in expreg:
			month     = tools.MonthNumToName(month)
			year      = re.sub(' -.*?$','',year)
			expiry    = month+' '+day+' - '+year
			ip        = tools.getlocalip()
			extip     = tools.getexternalip()
			tools.addDir('[B]U[COLOR white]sername: %s[/COLOR][/B]'%username,'','',icon,fanart,'')
			tools.addDir('[B]P[COLOR white]assword: %s[/COLOR][/B]'%password,'','',icon,fanart,'')
			tools.addDir('[B]E[COLOR white]xpiry Date: %s[/COLOR][/B]'%expiry,'','',icon,fanart,'')
			tools.addDir('[B]A[COLOR white]ccount Status: %s[/COLOR][/B]'%status,'','',icon,fanart,'')
			tools.addDir('[B]C[COLOR white]urrent Connections: %s[/COLOR][/B]'%active,'','',icon,fanart,'')
			tools.addDir('[B]A[COLOR white]llowed Connections: %s[/COLOR][/B]'%connects,'','',icon,fanart,'')
			tools.addDir('[B]L[COLOR white]ocal IP Address: %s[/COLOR] [/B]'%ip,'','',icon,fanart,'')
			tools.addDir('[B]E[COLOR white]xternal IP Address: %s[/COLOR][/B] '%extip,'','',icon,fanart,'')
			tools.addDir('[B]K[COLOR white]odi Version: %s[/COLOR][/B] '%str(KODIV),'','',icon,fanart,'')
	except:
		pass
		
	
def correctPVR():
	addon = xbmcaddon.Addon(user.id)
	username     = xbmcaddon.Addon('plugin.video.streamhub').getSetting('Username')
	password     = xbmcaddon.Addon('plugin.video.streamhub').getSetting('Password')
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
	IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
	nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
	loginurl   = user.host+':'+user.port+"/get.php?username=" + username + "&password=" + password + "&type=m3u_plus&output=ts"
	EPGurl     = user.host+':'+user.port+"/xmltv.php?username=" + username + "&password=" + password

	xbmc.executeJSONRPC(jsonSetPVR)
	xbmc.executeJSONRPC(IPTVon)
	xbmc.executeJSONRPC(nulldemo)
	
	moist = xbmcaddon.Addon('pvr.iptvsimple')
	moist.setSetting(id='m3uUrl', value=loginurl)
	moist.setSetting(id='epgUrl', value=EPGurl)
	moist.setSetting(id='m3uCache', value="false")
	moist.setSetting(id='epgCache', value="false")
	xbmc.executebuiltin("Container.Refresh")

	
def tvguidesetup():
		dialog = xbmcgui.Dialog().yesno(user.name,'Would You like us to Setup the PVR TV Guide for You?')
		if dialog:
				correctPVR()
				xbmcgui.Dialog().ok(user.name, 'PVR TV Guide Integration Complete - Restart Kodi For The Changes to Take Effect')
def num2day(num):
	if num =="0":
		day = 'monday'
	elif num=="1":
		day = 'tuesday'
	elif num=="2":
		day = 'wednesday'
	elif num=="3":
		day = 'thursday'
	elif num=="4":
		day = 'friday'
	elif num=="5":
		day = 'saturday'
	elif num=="6":
		day = 'sunday'
	return day
	
def extras():
	tools.addDir('APK Installer','tv',9999919,icon,fanart,"Install Various Android Applications.[CR][CR]For Android Devices Only.")
	tools.addDir('Football Guide','tv',9999914,icon,fanart,"Find out who's playing football, then be taken straight to the stream!")
	tools.addDir('Edit Advanced Settings','url',9999918,icon,fanart,"This setting enables you to edit the Advanced Settings in Kodi[CR][CR]In most cases allowing a smoother stream.")
	tools.addDir('M3U & EPG Url Generator','m3unepg',9999910,icon,fanart,"Create a M3U and EPG URL and then run it through TinyUrl.com[CR][CR]Making the URL's up to 100+ characters smaller")
	tools.addDir('Integrate With PVR TV Guide','tv',9999917,icon,fanart,"Integrate StreamHub Premium Live Streams and EPG with Kodi's inbuilt TV Guide.[CR][CR]Allowing A Full, Sleek Looking TV Guide!")
	if xbmcaddon.Addon('plugin.video.streamhub').getSetting('vodsource')=='true':
		VOD = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		VOD = '[B][COLOR red]OFF[/COLOR][/B]'
		
#	tools.addDir('Show Premium Links in StreamHub Movie/Show Sources: %s'%VOD,'VODSOURCE',9999910,icon,fanart,VOD)
	
def m3uselector():
	dialog = xbmcgui.Dialog().select('Select a M3U Format', ['M3U Standard','M3U Plus (Has Channel Categorys)'])
	if dialog==0:
		type = 'm3u'
	elif dialog==1:
		type = 'm3u_plus'
	
	dialog = xbmcgui.Dialog().select('Select a Stream Format', ['MPEGTS (Recommended)','HLS','RTMP'])
	if dialog==0:
		output = 'ts'
	elif dialog==1:
		output = 'm3u8'
	elif dialog==2:
		output = 'rtmp'
		
	m3u = user.host + ':' + user.port + '/get.php?username=' + username + '&password=' + password + '&type=' + type + '&output=' + output
	epg = user.host + ':' + user.port + '/xmltv.php?username=' + username + '&password=' + password
	
	m3u = urllib.quote_plus(m3u)
	epg = urllib.quote_plus(epg)
	m3u,epg = tinyurlGet(m3u,epg)
	
	text = 'Here Is Your Shortened M3U & EPG URL[CR][CR]M3U URL: %s[CR][CR]EPG URL: %s'%(m3u,epg)
	popupd(text)

def tinyurlGet(m3u,epg):
		request  = 'https://tinyurl.com/create.php?source=indexpage&url='+m3u+'&submit=Make+TinyURL%21&alias='
		request2 = 'https://tinyurl.com/create.php?source=indexpage&url='+epg+'&submit=Make+TinyURL%21&alias='
		m3u = tools.OPEN_URL(request)
		epg = tools.OPEN_URL(request2)
		shortm3u = tools.regex_from_to(m3u,'<div class="indent"><b>','</b>')
		shortepg = tools.regex_from_to(epg,'<div class="indent"><b>','</b>')
		return shortm3u,shortepg
	
def startupd():
	try:
		if xbmcaddon.Addon('plugin.video.streamhub').getSetting('startupd') == '0':raise Exception()
		
		from datetime import date

		open       = tools.OPEN_URL(panel_api)
		
		username   = tools.regex_from_to(open,'"username":"','"')
		status     = tools.regex_from_to(open,'"status":"','"')
		expiry     = tools.regex_from_to(open,'"exp_date":"','"')
		if status == 'Expired':xbmcgui.Dialog().ok('[COLOR ffff0000][B]StreamHub[/B][/COLOR]','Hello There, %s. Your Account Has Expired!','Head To facebook.com/groups/streamh To Renew!'%username)
		expiry     = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y')
		expreg     = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
		
		for day,month,year in expreg:
			d0 = date(int(year),int(month),int(day))
			
		times       = time.time()
		times      = datetime.datetime.fromtimestamp(int(times)).strftime('%d/%m/%Y')
		times       = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(times)
		
		for day,month,year in times:
			d1 = date(int(year),int(month),int(day))
			
		delta = d0 - d1
		days  = delta.days
		
		if xbmcaddon.Addon('plugin.video.streamhub').getSetting('startupd') == '2':
			xbmcgui.Dialog().notification('[COLOR ffff0000][B]StreamHub[/B][/COLOR]','Welcome Back, You Have %s Days Left Of Premium Content'%days)
		elif xbmcaddon.Addon('plugin.video.streamhub').getSetting('startupd') == '1':
			xbmcgui.Dialog().ok('[COLOR ffff0000][B]StreamHub[/B][/COLOR]','Welcome Back, %s '%username,'You Have %s Days Left Of Premium Content'%days)
	except:
		pass
		
		
def footballguide():
	url  = 'http://www.wheresthematch.com/live-football-on-tv/'
	open = tools.OPEN_URL(url)
	all_lists = tools.regex_get_all(open,'<td class="home-team">','</tr>')
	tools.addDir('[COLOR blue]Only Shows Main Matches - Find More at http://liveonsat.com[/COLOR]','url',500,icon,fanart,'')
	for a in all_lists:
		name = re.compile('<em class="">(.*?)<em class="">(.*?)</em>.*?<em class="">(.*?)</em>',re.DOTALL).findall(a)
		for home,v,away in name:
			koff  = tools.regex_from_to(a,'<strong>','</strong>')
			chan = tools.regex_from_to(a,'class="channel-name">','</span>')
			if chan == "Live Stream":
				chan = 'Check liveonsat.com'
			if chan == 'LFC TV':
				chan = 'LFCTV'
			thumb = tools.regex_from_to(a,'    <img src="','"')
			if 'Bet 365 Live' not in chan:
					tools.addDir(koff+' - '+str(home).replace('</em>','')+' '+v+'  '+away+'   -   [COLOR blue]%s[/COLOR]'%chan,'url',9999915,'http://www.wheresthematch.com'+str(thumb).replace('..',''),fanart,chan)

def footballguidesearch(description):
	if description=='BBC1 Scotland':
		tools.addDir('BBC1 Scotland','http://a.files.bbci.co.uk/media/live/manifesto/audio_video/simulcast/hls/uk/abr_hdtv/ak/bbc_one_scotland_hd.m3u8',4,icon,fanart,'')
	else:
		open = tools.OPEN_URL(panel_api)
		all_chans = tools.regex_get_all(open,'{"num":','epg')
		for a in all_chans:
			name = tools.regex_from_to(a,'name":"','"').replace('\/','/')
			url  = tools.regex_from_to(a,'"stream_id":"','"')
			thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
			chan = description.lower()
			if chan in name.lower():
				tools.addDir(name.replace('UK:','[COLOR ffff0000][B]UK:[/COLOR][/B]').replace('USA/CA:','[COLOR ffff0000][B]USA/CA:[/COLOR][/B]').replace('All','[COLOR ffff0000][B]All[/COLOR][/B]').replace('International Sport','[COLOR ffff0000][B]INT: [/COLOR][/B]International Sport').replace('Live:','[COLOR ffff0000][B]Live:[/COLOR][/B]').replace('TEST','[COLOR ffff0000][B]TEST[/COLOR][/B]').replace('Install','[COLOR ffff0000][B]Install[/COLOR][/B]').replace('24/7','[COLOR ffff0000][B]24/7: [/COLOR][/B]Channels').replace('DE:','[COLOR ffff0000][B]DE:[/COLOR][/B]').replace('FR:','[COLOR ffff0000][B]FR:[/COLOR][/B]').replace('PL:','[COLOR ffff0000][B]PL:[/COLOR][/B]').replace('AR:','[COLOR ffff0000][B]AR:[/COLOR][/B]').replace('LIVE:','[COLOR ffff0000][B]LIVE:[/COLOR][/B]').replace('ES:','[COLOR ffff0000][B]ES:[/COLOR][/B]').replace('IN:','[COLOR ffff0000][B]IN:[/COLOR][/B]').replace('PK:','[COLOR ffff0000][B]PK:[/COLOR][/B]').replace('NBC Extra Time','[COLOR ffff0000][B]NBC:[/COLOR][/B] NBC Extra Time'),play_url+url+'.ts',999994,thumb,fanart,'')
			
		
def popupd(announce):
	import time,xbmcgui
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR ghostwhite][B]Live[/COLOR][COLOR red] Hub[/COLOR][/B]') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)
		
		
def apkdownloads():
	open = requests.get('https://raw.githubusercontent.com/sClarkeIsBack/StreamHub/master/Links/apks.txt').text
	all  = re.compile('<item>.+?title>(.+?)<.+?link>(.+?)<.+?thumbnail>(.+?)<',re.DOTALL|re.MULTILINE).findall(open)
	for name,url,icon in all:
		tools.addDir(name,url,9999910,icon,fanart,name)