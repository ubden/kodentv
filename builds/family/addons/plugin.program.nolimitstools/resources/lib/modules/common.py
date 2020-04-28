"""
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
"""
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
from urllib2 import urlopen
from resources.lib.modules import extract
from resources.lib.modules import downloader
from resources.lib.modules import uploadlog
import re
import time

ADDONTITLE      = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
ADDON_ID        = xbmcaddon.Addon().getAddonInfo('id') #'plugin.program.nolimitstools'
ADDON           = xbmcaddon.Addon(id=ADDON_ID)
HOME            = xbmc.translatePath('special://home/')
dialog          = xbmcgui.Dialog()
dp              = xbmcgui.DialogProgress()
#BASEURL         = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v') #http://echocoder.com
SUPPORT_ICON    = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/support.png'))
FANART          = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'fanart.jpg'))
ICON            = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'icon.png'))

COLOR1              = 'magenta'
COLOR2              = 'cyan'
THEME1              = '[COLOR '+COLOR1+'][I][B]([COLOR '+COLOR2+']No Limits[/COLOR])[/B][/I][/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
THEME2              = '[COLOR '+COLOR2+']%s[/COLOR]'
THEME3              = '[COLOR '+COLOR1+']%s[/COLOR]'

#######################################################################
#						Add to menus
#######################################################################

def GET_KODI_VERSION():

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	if version >= 11.0 and version <= 11.9:
		codename = 'Eden'
	elif version >= 12.0 and version <= 12.9:
		codename = 'Frodo'
	elif version >= 13.0 and version <= 13.9:
		codename = 'Gotham'
	elif version >= 14.0 and version <= 14.9:
		codename = 'Helix'
	elif version >= 15.0 and version <= 15.9:
		codename = 'Isengard'
	elif version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
	elif version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
	elif version >= 18.0 and version <= 18.9:
		codename = 'Leia'
	else: codename = "Decline"
	
	return codename
	
def GET_KODI_VERSION_DETAILS():

	try:
		xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
		version=float(xbmc_version[:4])
		if version >= 11.0 and version <= 11.9:
			codename = 'Eden'
		elif version >= 12.0 and version <= 12.9:
			codename = 'Frodo'
		elif version >= 13.0 and version <= 13.9:
			codename = 'Gotham'
		elif version >= 14.0 and version <= 14.9:
			codename = 'Helix'
		elif version >= 15.0 and version <= 15.9:
			codename = 'Isengard'
		elif version >= 16.0 and version <= 16.9:
			codename = 'Jarvis'
		elif version >= 17.0 and version <= 17.9:
			codename = 'Krypton'
		elif version >= 18.0 and version <= 18.9:
			codename = 'Leia'
		else: codename = "Decline"
		
		string = codename + " - " + str(version)
	except: string = "Unknown"

	return string


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirL(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def createMenu(type, add, name):
	if   type == 'saveaddon':
		menu_items=[]
		add2  = urllib.quote_plus(add.lower().replace(' ', ''))
		add3  = add.replace('Debrid', 'Real Debrid')
		name2 = urllib.quote_plus(name.lower().replace(' ', ''))
		name = name.replace('url', 'URL Resolver')
		menu_items.append((THEME2 % name.title(),             ' '))
		menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Clear %s Data' % add3,              'RunPlugin(plugin://%s/?mode=clear%s&name=%s)' %   (ADDON_ID, add2, name2)))
	elif type == 'save'    :
		menu_items=[]
		add2  = urllib.quote_plus(add.lower().replace(' ', ''))
		add3  = add.replace('Debrid', 'Real Debrid')
		name2 = urllib.quote_plus(name.lower().replace(' ', ''))
		name = name.replace('url', 'URL Resolver')
		menu_items.append((THEME2 % name.title(),             ' '))
		menu_items.append((THEME3 % 'Register %s' % add3,                'RunPlugin(plugin://%s/?mode=auth%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Save %s Data' % add3,               'RunPlugin(plugin://%s/?mode=save%s&name=%s)' %    (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Restore %s Data' % add3,            'RunPlugin(plugin://%s/?mode=restore%s&name=%s)' % (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Import %s Data' % add3,             'RunPlugin(plugin://%s/?mode=import%s&name=%s)' %  (ADDON_ID, add2, name2)))
		menu_items.append((THEME3 % 'Clear Addon %s Data' % add3,        'RunPlugin(plugin://%s/?mode=addon%s&name=%s)' %   (ADDON_ID, add2, name2)))
	elif type == 'install'  :
		menu_items=[]
		name2 = urllib.quote_plus(name)
		menu_items.append((THEME2 % name,                                'RunAddon(%s, ?mode=viewbuild&name=%s)'  % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Fresh Install',                     'RunPlugin(plugin://%s/?mode=install&name=%s&url=fresh)'  % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Standard Install',                    'RunPlugin(plugin://%s/?mode=install&name=%s&url=normal)' % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Apply GuiFix',                      'RunPlugin(plugin://%s/?mode=install&name=%s&url=gui)'    % (ADDON_ID, name2)))
		menu_items.append((THEME3 % 'Build Information',                 'RunPlugin(plugin://%s/?mode=buildinfo&name=%s)'  % (ADDON_ID, name2)))
	menu_items.append((THEME2 % '%s Settings' % ADDONTITLE,              'RunPlugin(plugin://%s/?mode=settings)' % ADDON_ID))
	return menu_items

def addItem(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDirWTW(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
        + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=False)
    return ok

#######################################################################
#				INDIVIDUAL BUILDS MENU
#######################################################################

def BUILDER(name,url,iconimage,fanart,description):

	urla = url
	name,url,original = url.split(",")
	url = name + "," + url
	send_youtube_multi = name + "," + original
	desca = description
	youtube_id = "null"
	notice = "null"
	build_image = "null"
	notice,hash,fresh,youtube_id,skin,build_image = desca.split(',')

	TEMP_FILE =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID,'temp/temp.xml'))
	week  = (str(count(name,TEMP_FILE)))
	total =(str(count(name+"TOTAL_COUNT",TEMP_FILE)))  
	countfail = week
	try:
		count2 = int(week)
		count3 = "{:,}".format(count2)
		week = str(count3)
	except: week = countfail		

	if not youtube_id.lower() == "null":
		if "http" in youtube_id.lower():
			youtube_id = youtube_id.replace("https://www.youtube.com/watch?v=","")
		if not "multi" in youtube_id.lower():
			youtube_id = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9")+youtube_id
	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(name)
	body = urllib2.urlopen(service_url).read()
	addDir("[COLOR yellowgreen][B]Download " + name.title() + " Now[/B][/COLOR]",url,90,iconimage,fanart,description)
	if not notice.lower() == "null":
		addItem("[COLOR white][B]View " + name.title() + " Information[/B][/COLOR]",notice,182,iconimage,fanart,description)
	url = name

	if "multi" in youtube_id.lower():
		addItem('[COLOR white][B]Watch YouTube Review of ' + name.title() + '[/B][/COLOR]',send_youtube_multi,183,iconimage,fanart,'')
	elif "null" not in youtube_id.lower():
		addItem('[COLOR white][B]Watch YouTube Review of ' + name.title() + '[/B][/COLOR]',youtube_id,95,iconimage,fanart,'')
		
	addItem('[COLOR white][B]Downloads This Week -  [/COLOR][COLOR yellowgreen]' + str(week) + '[/B][/COLOR]',url,999,iconimage,fanart,'')
	addItem('[COLOR white][B]All Time Downloads -  [/COLOR][COLOR yellowgreen]' + str(total) + '[/B][/COLOR]',url,999,iconimage,fanart,'')

	if "null" not in build_image.lower():
		addItem("[COLOR white][B]View Image of " + name.title() + "[/COLOR][/B]",build_image,116,iconimage,fanart,description)
	addItem("[COLOR white][B]Leave A Review for " + name.title() + "[/COLOR][/B]",url,58,iconimage,fanart,description)
	addDir("[COLOR white][B]Read All Reviews for " + name.title() + " - [COLOR yellowgreen]" + body + " [/COLOR] [/COLOR][/B]",url,59,iconimage,fanart,description)

def BUILDER_COMMUNITY(name,url,iconimage,fanart,description):

	send_youtube_multi = "null"
	try:
		name,url,original = url.split(",")
		send_youtube_multi = name + "," + original
	except: name,url = url.split(',')
	urla = url
	youtube_id = "null"
	notice = "null"
	build_image = "null"
	try:
		skin_used, developer, contact = description.split(',')
	except:	skin_used, developer, youtube_id, notice, build_image, contact = description.split(',')

	TEMP_FILE =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID,'temp/temp.xml'))
	week  = (str(count(name,TEMP_FILE)))
	countfail = week
	try:
		count2 = int(week)
		count3 = "{:,}".format(count2)
		week = str(count3)
	except: week = countfail	
	total =(str(count(name+"TOTAL_COUNT",TEMP_FILE)))   

	if not contact == "Unknown":
		addItem("[COLOR white][B]Contact Details: [/COLOR][COLOR yellowgreen]" + str(contact) + "[/B][/COLOR]","url",999,iconimage,fanart,description)

	if not youtube_id.lower() == "null":
		if "http" in youtube_id.lower():
			youtube_id = youtube_id.replace("https://www.youtube.com/watch?v=","")
		if not "multi" in youtube_id.lower():
			youtube_id = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9")+youtube_id
	url = str(name + "," + urla + "," + skin_used + "," + developer)
	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(name)
	body = urllib2.urlopen(service_url).read()
	addDir("[COLOR yellowgreen][B]Download The " + name.title() + " Now[/B][/COLOR]",url,96,iconimage,fanart,description)
	if not notice.lower() == "null":
		addItem("[COLOR white][B]View " + name.title() + " Information[/B][/COLOR]",notice,182,iconimage,fanart,description)
	url = name

	if "multi" in youtube_id.lower():
		addItem('[COLOR white][B]Watch YouTube Review of ' + name.title() + '[/B][/COLOR]',send_youtube_multi,183,iconimage,fanart,'')
	elif "null" not in youtube_id.lower():
		addItem('[COLOR white][B]Watch YouTube Review of ' + name.title() + '[/B][/COLOR]',youtube_id,95,iconimage,fanart,'')

	addItem('[COLOR white][B]Downloads This Week -  [/COLOR][COLOR yellowgreen]' + str(week) + '[/B][/COLOR]',url,999,iconimage,fanart,'')
	addItem('[COLOR white][B]All Time Downloads -  [/COLOR][COLOR yellowgreen]' + str(total) + '[/B][/COLOR]',url,999,iconimage,fanart,'')

	if "null" not in build_image.lower():
		addItem("[COLOR white][B]View Image of " + name.title() + "[/COLOR][/B]",build_image,116,iconimage,fanart,description)
	addItem("[COLOR white][B]Leave A Review for " + name.title() + "[/COLOR][/B]",url,58,iconimage,fanart,description)
	addDir("[COLOR white][B]Read All Reviews for " + name.title() + " - [COLOR yellowgreen]" + body + " [/COLOR] [/COLOR][/B]",url,59,iconimage,fanart,description)

def multi_youtube_videos(url):

	name,url = url.split(",")
	streamurl=[]
	streamname=[]
	link=OPEN_URL(url)
	urls=re.compile('<title>'+re.escape(name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
	links=re.compile('<youtube>(.+?)</youtube>').findall(urls)
	for sturl in links:
		if "(" in sturl:
			sturl2=sturl
			sturl=sturl.split('(')[0]
			caption=str(sturl2.split('(')[1].replace(')',''))
			caption2 = "[COLOR white]" + caption + "[/COLOR]"
			streamurl.append(sturl)
			streamname.append(caption2)
		else:
			streamurl.append(sturl)
			streamname.append("[COLOR white]No Description Given[/COLOR]")

	name='[COLOR yellowgreen][B]'+name+' YouTube Videos[/B][/COLOR]'
	dialog = xbmcgui.Dialog()
	select = dialog.select(name,streamname)
	if select < 0:
		quit()
	else:
		url = streamurl[select]
		print url

	url = streamurl[select]
	name = streamname[select]
	if "http" in url.lower():
		url = url.replace("https://www.youtube.com/watch?v=","")
	url = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9")+url

	PLAYLINK(name,url,ICON)

def PLAYLINK(name,url,icon):

	xbmc.Player().play(url)

#######################################################################
#				INDIVIDUAL BUILDS MENU
#######################################################################

def SHOW_PICTURE(url):

    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)
    sys.exit(1)

def WriteReview(build_name):

	review_text =''
	name_text = ''
	review_ip = urlopen('http://ip.42.pl/raw').read()

	try:
		Review_keyboard = xbmc.Keyboard(review_text, 'Enter Your Review')
		Review_keyboard.doModal()

		if Review_keyboard.isConfirmed():
			review_text = Review_keyboard.getText()
			Review_Name = xbmc.Keyboard(name_text, 'Enter Your Name')
			Review_Name.doModal()
	
		if Review_Name.isConfirmed():
			name_text = Review_Name.getText()
			
		if 	review_text == "":
			dialog.ok(ADDONTITLE, "[B][COLOR white]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR white]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		if 	name_text == "":
			dialog.ok(ADDONTITLE, "[B][COLOR white]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR white]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1hZGQmdGV4dD0=') + base64.b64encode(review_text) + base64.b64decode(b'Jm5hbWU9') + base64.b64encode(name_text) + base64.b64decode(b'JmlwPQ==') + base64.b64encode(review_ip) + base64.b64decode(b'JmJ1aWxkPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except: sys.exit(1)

	dialog.ok(ADDONTITLE, "[COLOR white]" + name_text + ", thank you for leaving a review for " + build_name + ".[/COLOR]")

	xbmc.executebuiltin("Container.Refresh")

def ListReview(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9idWlsZF9yZXZpZXcucGhwP2FjdGlvbj1yZWFkJmJ1aWxkPQ==') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	reviews = review_parse(data)
	xbmc.log("got review parse : "+data)
	for review in reviews:
		review_title = "[COLOR yellowgreen][B]"+review['date']+"[/COLOR][/B] - [COLOR white][B]" +review['name']+ "[/COLOR][/B]"
		url = review['review']
		date = "Review Date : " + review['date']
		xbmc.log(review['name']+" : "+review['date'])
		
		addItem(review_title,url,49,ICON,FANART,'')

def Write_Addon_Review(build_name):

	review_text =''
	name_text = ''
	review_ip = urlopen('http://ip.42.pl/raw').read()

	try:
		Review_keyboard = xbmc.Keyboard(review_text, 'Enter Your Review')
		Review_keyboard.doModal()

		if Review_keyboard.isConfirmed():
			review_text = Review_keyboard.getText()
			Review_Name = xbmc.Keyboard(name_text, 'Enter Your Name')
			Review_Name.doModal()
	
		if Review_Name.isConfirmed():
			name_text = Review_Name.getText()
			
		if 	review_text == "":
			dialog.ok(ADDONTITLE, "[B][COLOR white]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR white]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		if 	name_text == "":
			dialog.ok(ADDONTITLE, "[B][COLOR white]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR white]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1hZGQmdGV4dD0=') + base64.b64encode(review_text) + base64.b64decode(b'Jm5hbWU9') + base64.b64encode(name_text) + base64.b64decode(b'JmlwPQ==') + base64.b64encode(review_ip) + base64.b64decode(b'JmJ1aWxkPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except: sys.exit(1)

	dialog.ok(ADDONTITLE, "[B][COLOR white]Thank you for leaving a review.[/COLOR][/B]")

def List_Addon_Review(build_name):

	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1yZWFkJmJ1aWxkPQ==') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	reviews = review_parse(data)
	xbmc.log("got review parse : "+data)
	for review in reviews:
		review_title = "[COLOR blue][B]"+review['date']+"[/COLOR][/B] - [COLOR white][B] Read Review By : " +review['name']+ "[/COLOR][/B]"
		url = review['review']
		date = "Review Date : " + review['date']
		xbmc.log(review['name']+" : "+review['date'])
		
		addItem(review_title,url,49,ICON,FANART,'')

def WriteTicket():

	build_name = "[COLOR orangered][B]Ticket[/B][/COLOR]"
	review_text =''
	name_text = ''
	review_ip = urlopen('http://ip.42.pl/raw').read()

	try:
		Review_keyboard = xbmc.Keyboard(review_text, 'What Is The Issue You Have Found?')
		Review_keyboard.doModal()

		if Review_keyboard.isConfirmed():
			review_text = Review_keyboard.getText()
			Review_Name = xbmc.Keyboard(name_text, 'Enter Your E-Mail')
			Review_Name.doModal()
	
		if Review_Name.isConfirmed():
			name_text = Review_Name.getText()
			
		if 	review_text == "":
			dialog.ok(ADDONTITLE, "[B][COLOR smokewhite]Sorry not a valid entry![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		if 	"@" not in name_text:
			dialog.ok(ADDONTITLE, "[B][COLOR smokewhite]Sorry not a valid e-mail![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)
		if 	"." not in name_text:
			dialog.ok(ADDONTITLE, "[B][COLOR smokewhite]Sorry not a valid e-mail![/COLOR][/B]", "[B][COLOR smokewhite]Please try again.[/COLOR][/B]", '')
			sys.exit(1)

		service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9zdXBwb3J0LnBocD9hY3Rpb249YWRkJnRleHQ9') + base64.b64encode(review_text) + base64.b64decode(b'Jm5hbWU9') + base64.b64encode(name_text) + base64.b64decode(b'JmlwPQ==') + base64.b64encode(review_ip) + base64.b64decode(b'JmJ1aWxkPQ==') + base64.b64encode(build_name)
		body =urllib2.urlopen(service_url).read()
	except: sys.exit(1)

	splitter = name_text
	ref,rest = splitter.split('@')
	ref2 = base64.b64encode(ref)
	ref3 = ref2.replace("=","")
	dialog.ok(ADDONTITLE, "[B][COLOR lightskyblue]Thank you for contacting us![/COLOR][/B]", "We will be in touch in 24-48 Hours", "[COLOR smokewhite][B]Reference: [/B][COLOR white][I]" + ref3.upper() + "[/COLOR][/I]")

	xbmc.executebuiltin("Container.Refresh")

def ListTickets():

	build_name = "[COLOR orangered][B]Ticket[/B][/COLOR]"
	service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9zdXBwb3J0LnBocD9hY3Rpb249cmVhZCZidWlsZD0=') + base64.b64encode(build_name)
	f = urllib2.urlopen(service_url)
	data = f.read()
	f.close()

	reviews = review_parse(data)
	xbmc.log("got review parse : "+data)
	for review in reviews:
		review_title = "[COLOR blue][B]Ticket Raised: [/COLOR][/B][COLOR white][I]"+review['date']+"[/COLOR][/I] - [COLOR white][B]" +review['review']+ "[/COLOR][/B]"
		url = review['review']
		date = "Review Date : " + review['date']
		xbmc.log(review['name']+" : "+review['date'])
		
		addItem(review_title,url,120,SUPPORT_ICON,FANART,'')

def review_parse(data):

    patron = "<item>(.*?)</item>"
    reviews = re.findall(patron,data,re.DOTALL)

    items = []
    for review in reviews:
        item = {}
        item["name"] = find_single_match(review,"<name>([^<]+)</name>")
        item["date"] = find_single_match(review,"<date>([^<]+)</date>")
        item["review"] = find_single_match(review,"<review>([^<]+)</review>")

        if item["name"]!="":
            items.append(item)

    return items

def add_one(build_name):

	if not "ADDON_INSTALLER" in build_name:
		build_name,dev_name = build_name.split('|SPLIT|')
		build_name = INVALID_CHARACTERS(build_name)
		try:
			service_url = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1idWlsZHMmYWN0aW9uPWFkZCZidWlsZD0=') + base64.b64encode(build_name) + "&dev=" + base64.b64encode(dev_name)
			body =urllib2.urlopen(service_url).read()
		except:
			sys.exit(0)
	else:
		build_name = build_name.replace("ADDON_INSTALLER","")
		build_name = INVALID_CHARACTERS(build_name)
		try:
			service_url = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1hZGRvbnMmYWN0aW9uPWFkZCZidWlsZD0=') + base64.b64encode(build_name)
			body =urllib2.urlopen(service_url).read()
		except:
			sys.exit(0)

def count(build_name,FILE):

	if "ADDON_INSTALLER" in build_name:
		build_name = build_name.replace("ADDON_INSTALLER","")
		build_name = INVALID_CHARACTERS(build_name)
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>'+re.escape(build_name)+'</name><count>(.+?)</count>',re.DOTALL).findall(msg)[0]
		except: count = 0
		return count
	elif "NUMBER_OF_ADDONS" in build_name:
		build_name = build_name.replace("NUMBER_OF_ADDONS","")
		build_name = INVALID_CHARACTERS(build_name)
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>addon Count</name><count>(.+?)</count>',re.DOTALL).findall(msg)[0]
		except: count = 0
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		return count
	elif "ADDON_TOTAL" in build_name:
		build_name = build_name.replace("ADDON_TOTAL","")
		build_name = INVALID_CHARACTERS(build_name)
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>'+re.escape(build_name)+'</name>.+?<atotal>(.+?)</atotal>',re.DOTALL).findall(msg)[0]
		except: count = 0
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		return count
	elif "DEVEL_COUNT" in build_name:
		build_name = build_name.replace("DEVEL_COUNT","")
		build_name = INVALID_CHARACTERS(build_name)
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<dev>'+re.escape(build_name)+'</dev><dcount>(.+?)</dcount>',re.DOTALL).findall(msg)[0]
		except: count = 0
		return count
	elif "TOTAL_DEV" in build_name:
		build_name = build_name.replace("TOTAL_DEV","")
		build_name = INVALID_CHARACTERS(build_name)
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<dev>'+re.escape(build_name)+'</dev><dcount>.+?</dcount><dtotal>(.+?)</dtotal>',re.DOTALL).findall(msg)[0]
		except: count = 0
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		return count
	elif "TOTAL_COUNT" in build_name:
		build_name = build_name.replace("TOTAL_COUNT","")
		build_name = INVALID_CHARACTERS(build_name)
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>'+re.escape(build_name)+'</name>.+?<total>(.+?)</total>',re.DOTALL).findall(msg)[0]
		except: count = 0
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		return count
	elif "TOTAL_BUILDS_WEEK" in build_name:
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>Download Count</name><count>(.+?)</count>',re.DOTALL).findall(msg)[0]
		except: count = 0
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		return count
	elif "TOTAL_ADDONS_WEEK" in build_name:
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>Download Count</name><count>(.+?)</count>',re.DOTALL).findall(msg)[0]
		except: count = 0
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		return count
	elif "TOTAL_BUILDS_ALLTIME" in build_name:
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>Download Total Count</name><count>(.+?)</count>',re.DOTALL).findall(msg)[0]
		except: count = 0
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		return count
	elif "TOTAL_ADDONS_ALLTIME" in build_name:
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>Download Total Count</name><count>(.+?)</count>',re.DOTALL).findall(msg)[0]
		except: count = 0
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		return count
	else:
		f = open(FILE,mode='r'); msg = f.read(); f.close()
		msg = msg.replace('\n','')
		try:
			count = re.compile('<item><name>'+re.escape(build_name)+'</name><count>(.+?)</count>',re.DOTALL).findall(msg)[0]
		except: count = 0
		return count

def INVALID_CHARACTERS(string):

	string = str(string)
	string = string.replace("&","and")
	string = string.replace(",","")
	
	return string

def SHOW_PICTURE(url):

    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)
    sys.exit(1)

def find_single_match(text,pattern):

    result = ""
    try:    
        single = re.findall(pattern,text, flags=re.DOTALL)
        result = single[0]
    except:
        result = ""

    return result

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

def TextBoxError(title, msg):
	class TextBoxes(xbmcgui.WindowXMLDialog):
		def onInit(self):
			self.title         = 100
			self.msg           = 101
			self.okbutton      = 102
			self.uploadbutton  = 103
			self.scrollbar     = 104

			self.showdialog()

		def showdialog(self):
		
			self.getControl(self.title).setLabel(title)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)

			
		def onClick(self, controlId):
			if (controlId == self.okbutton):
				self.close()
			elif (controlId == self.uploadbutton):
				uploadlog.main(argv=None)	
	
	if "log" in title.lower():

		match=re.compile('WARNING: (.+?)\n',re.DOTALL).findall(msg)
		for items in match:
			if not "repeats" in items.lower():
				msg=msg.replace(items, '[COLOR yellow]'+items+'[/COLOR]')

		match2=re.compile('ERROR: (.+?)\n',re.DOTALL).findall(msg)
		for items2 in match2:
			if not "repeats" in items2.lower():
				if not "exception" in items2.lower():
					msg=msg.replace(items2, '[COLOR orange]'+items2+'[/COLOR]')
				
		match3=re.compile('ERROR: EXCEPTION(.+?)report<--',re.DOTALL).findall(msg)
		for items3 in match3:
			msg=msg.replace(items3, '[COLOR orangered]'+items3+'[/COLOR]')

		msg = msg.replace(' ERROR: EXCEPTION', ' [COLOR orangered] ERROR:EXCEPTION[/COLOR] ') \
			.replace(' ERROR: ', ' [COLOR orange] ERROR: [/COLOR] ') \
			.replace(' WARNING: ', ' [COLOR yellow] WARNING: [/COLOR] ') \
			.replace(' NOTICE: ', ' [COLOR lime] NOTICE: [/COLOR] ') \
			.replace('report<--', ' [COLOR orangered]report<--[/COLOR] ')

	if "error" in title.lower():

		msg = msg.replace('[COLOR yellowgreen]','') \
		.replace('[/COLOR]','') \
		.replace('[B]','') \
		.replace('[/B]','') \

		match=re.compile('COLOR red](.+?)\n',re.DOTALL).findall(msg)
		for items in match:
			msg=msg.replace(items, '[B]'+items+'[/B][/COLOR]')
			
	if "ERRORS" in title:

		try:
			import traceback as tb
			# start by logging the usual info to stderr
			(etype, value, traceback) = sys.exc_info()
			tb.print_exception(etype, value, traceback)
			#this now contains the traceback information
			error_traceback = tb.format_tb(traceback)
			#this now contains the error type
			error_type = str(etype)
			#this now contains the error value
			error_value =  str(value)
			
			xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
			xbmc_builddate=xbmc.getInfoLabel('System.BuildDate')
			xbmc_language=xbmc.getInfoLabel('System.Language')
			python_version = sys.version
			local_time = time.asctime( time.localtime(time.time()) )
			version=float(xbmc_version[:4])
			if version >= 11.0 and version <= 11.9:
				codename = 'Eden'
			elif version >= 12.0 and version <= 12.9:
				codename = 'Frodo'
			elif version >= 13.0 and version <= 13.9:
				codename = 'Gotham'
			elif version >= 14.0 and version <= 14.9:
				codename = 'Helix'
			elif version >= 15.0 and version <= 15.9:
				codename = 'Isengard'
			elif version >= 16.0 and version <= 16.9:
				codename = 'Jarvis'
			elif version >= 17.0 and version <= 17.9:
				codename = 'Krypton'
			elif version >= 18.0 and version <= 18.9:
				codename = 'Leia'
			else: codename = "Decline"

			GET_VERSION         =  xbmc.translatePath('special://home/addons/plugin.program.nolimitstools/addon.xml')

			a=open(GET_VERSION).read()
			b=a.replace('\n',' ').replace('\r',' ')
			match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
			for item in match:
				addon_version = float(item)

			msg = "\n[I]Kodi Information[/I]" + \
			"\nLocal Time : " + local_time + \
			"\nKodi " + codename + \
			"\nVersion - " + str(version) + \
			"\nBuild Date -  " + str(xbmc_builddate) + \
			"\nLanguage - " + str(xbmc_language) + \
			"\nPython - " + str(python_version) + \
			"\nNo Limits Version - " + str(addon_version) + \
			"\n\n" + \
			"--------------------------------------------------------------------------------------------------------------------------------------------" \
			"\n\n" + msg
		except:
			msg = "[I]Kodi Information[/I]" + \
			"\nUnable to get information." \
			"\n\n" + msg
	tb = TextBoxes( "textboxerror.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', title=title, msg=msg)
	tb.doModal()
	del tb

def TextBox(title, msg):
	class TextBoxes(xbmcgui.WindowXMLDialog):
		def onInit(self):
			self.title      = 100
			self.msg        = 101
			self.okbutton   = 102
			self.scrollbar  = 104

			self.showdialog()

		def showdialog(self):
		
			self.getControl(self.title).setLabel(title)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)

			
		def onClick(self, controlId):
			if (controlId == self.okbutton):
				self.close()
			elif (controlId == self.uploadbutton):
				uploadlog.main(argv=None)	

	tb = TextBoxes( "textboxnormal.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', title=title, msg=msg)
	tb.doModal()
	del tb

def OPEN_URL(url):

		if "https://" in url:
			url = url.replace("https://","http://")
		req = urllib2.Request(url)
		req.add_header('User-Agent', base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl'))
		try:
			response = urllib2.urlopen(req, timeout = 10)
		except urllib2.URLError, e:
			dialog.ok(ADDONTITLE, "There was an error reaching the url. Please try again later.")
			quit()
		link=response.read()
		response.close()
		return link
	
def OPEN_URL_CUSTOM(url,ua):

		if "https://" in url:
			url = url.replace("https://","http://")
		req = urllib2.Request(url)
		req.add_header('User-Agent', ua)
		try:
			response = urllib2.urlopen(req, timeout = 10)
		except urllib2.URLError, e:
			dialog.ok(ADDONTITLE, "There was an error reaching the url. Please try again later.")
			quit()
		link=response.read()
		response.close()
		return link

def OPEN_URL_NORMAL(url):

		if "https://" in url:
			url = url.replace("https://","http://")
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
		response = urllib2.urlopen(req, timeout = 30)
		link=response.read()
		response.close()
		return link

def OPEN_URL_DIALOG(url):

	dp.create(ADDONTITLE,'[COLOR red][B]CONNECTING.....[/B][/COLOR]','[COLOR yellowgreen]Please wait...[/COLOR]')
	if "https://" in url:
		url = url.replace("https://","http://")
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
	try:
		response = urllib2.urlopen(req, timeout = 10)
	except urllib2.URLError, e:
		dialog.ok(ADDONTITLE, "There was an error reaching the url. Please try again later.")
		quit()
	link=response.read()
	response.close()
	dp.update(100,'[COLOR lime][B]CONNECTED.....[/B][/COLOR]',' ')
	dp.close()
	return link

def OPEN_URL_BEAST(url):

		if "https://" in url:
			url = url.replace("https://","http://")
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36 ReplicantWizard/1.0.0')
		try:
			response = urllib2.urlopen(req, timeout = 10)
		except urllib2.URLError, e:
			dialog.ok(ADDONTITLE, "There was an error reaching the url. Please try again later.")
			quit()
		link=response.read()
		response.close()
		return link

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def convertSize(size):
   import math
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   
   return s,size_name[i]

##########################
###DETERMINE PLATFORM#####
##########################
        
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
		
############################
###REMOVE EMPTY FOLDERS#####
############################

def REMOVE_EMPTY_FOLDERS():
#initialize the counters
	print"########### Start Removing Empty Folders #########"
	empty_count = 0
	used_count = 0
	try:
		for curdir, subdirs, files in os.walk(HOME):
			if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
				empty_count += 1 #increment empty_count
				os.rmdir(curdir) #delete the directory
				print "successfully removed: "+curdir
			elif len(subdirs) > 0 and len(files) > 0: #check for used directories
				used_count += 1 #increment 
	except: pass

def REMOVE_EMPTY_FOLDERS_BUILDS():
#initialize the counters
	print"########### Start Removing Empty Folders #########"
	empty_count = 0
	used_count = 0
	
	EXCLUDES = ['Thumbnails']

	try:
		for dirs, subdirs, files in os.walk(HOME,topdown=True):
			subdirs[:] = [d for d in subdirs if d not in EXCLUDES]
			if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
				empty_count += 1 #increment empty_count
				os.rmdir(dirs) #delete the directory
				print "successfully removed: "+dirs
			elif len(subdirs) > 0 and len(files) > 0: #check for used directories
				used_count += 1 #increment 
	except: pass

###############################################################
###FORCE CLOSE KODI - ANDROID ONLY WORKS IF ROOTED#############
#######LEE @ COMMUNITY BUILDS##################################

def killxbmc():
    dialog       =  xbmcgui.Dialog()
    choice = xbmcgui.Dialog().yesno('[COLOR=lightsteelblue]Force Close Kodi[/COLOR]', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='[COLOR=green]Yes, Close[/COLOR]')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass     
        try: os.system('adb shell am force-stop com.semperpax.spmc16')
        except: pass
        try: os.system('adb shell am force-stop com.spmc16')
        except: pass      		
        try: os.system('adb shell am force-stop com.semperpax.spmc')
        except: pass
        try: os.system('adb shell am force-stop com.spmc')
        except: pass    
        try: os.system('adb shell am force-stop uk.droidbox.dbmc')
        except: pass
        try: os.system('adb shell am force-stop uk.dbmc')
        except: pass   
        try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
        except: pass
        try: os.system('adb shell am force-stop com.jesusboxmedia')
        except: pass 
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try: os._exit(1)
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    


def KillKodi():
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass     
        try: os.system('adb shell am force-stop com.semperpax.spmc16')
        except: pass
        try: os.system('adb shell am force-stop com.spmc16')
        except: pass      		
        try: os.system('adb shell am force-stop com.semperpax.spmc')
        except: pass
        try: os.system('adb shell am force-stop com.spmc')
        except: pass    
        try: os.system('adb shell am force-stop uk.droidbox.dbmc')
        except: pass
        try: os.system('adb shell am force-stop uk.dbmc')
        except: pass   
        try: os.system('adb shell am force-stop com.perfectzoneproductions.jesusboxmedia')
        except: pass
        try: os.system('adb shell am force-stop com.jesusboxmedia')
        except: pass 
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try: os._exit(1)
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os._exit(1)
        except: pass
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=yellowgreen]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    