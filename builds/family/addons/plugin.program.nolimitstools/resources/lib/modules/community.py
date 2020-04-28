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
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys
import urllib2,urllib
from resources.lib.modules import extract
from resources.lib.modules import downloader
import requests
from resources.lib.modules import protected_wizards
import re
from resources.lib.modules import plugintools
from resources.lib.modules import common as Common
from resources.lib.modules import installer

AddonData = xbmc.translatePath('special://userdata/addon_data')
addon_id = 'plugin.program.nolimitstools'
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ADDON = xbmcaddon.Addon(id=addon_id)
dp               =  xbmcgui.DialogProgress()
AddonTitle="[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
MaintTitle="[COLOR aqua]No Limits[/COLOR] [COLOR white]Maintenance Tools[/COLOR]"
BASEURL = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
key = base64.b64encode(plugintools.get_setting("beta"))
COMMUNITY_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/community.png'))
TEMP_FILE      =  xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + addon_id,'temp/temp.xml'))
Community_List = BASEURL + base64.b64decode(b"Y29tbXVuaXR5L3dpemFyZHMudHh0")
Protected_List = BASEURL + base64.b64decode(b"Y29tbXVuaXR5L3Byb3RlY3RlZC9wYWdl")
COM_NOTICE = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/files/community_notice.txt'))
SEARCH_ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'resources/art/search.png'))
page_number = 1
dialog = xbmcgui.Dialog()

#######################################################################
#######################################################################
#						Community Builds
#######################################################################

def COMMUNITY():

	i=0
	dp.create(AddonTitle,"[COLOR blue]We are getting the list of developers from our server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
	dp.update(0)
	namelist=[]
	urllist=[]
	hiddenlist=[]
	useragentlist=[]
	countlist=[]
	totallist=[]
	deslist=[]
	iconlist=[]
	fanartlist=[]
	link = Common.OPEN_URL(Community_List).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?rotected="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?seragent="(.+?)".+?ontact="(.+?)"').findall(link)
	dis_links = len(match)
	for name,url,hidden,iconimage,fanart,useragent,contact in match:
		if useragent.lower() == "null":
			useragent == "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
		i = i + 1
		dis_count = str(i)
		progress = 100 * int(i)/int(dis_links)
		dp.update(progress,"Getting details of developer " + str(dis_count) + " of " + str(dis_links),'',"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
		developer = str(name.replace('[COLOR white][B]','').replace('[/B][/COLOR]','').replace('[/B][/COLOR]','').replace(' BUILDS',''))
		developer = developer.upper()
		description = str(developer + "," + hidden + "," + contact)
		namelist.append(name)
		urllist.append(url)
		hiddenlist.append(hidden)
		useragentlist.append(useragent)
		countlist.append(str(Common.count(developer+"DEVEL_COUNT",TEMP_FILE)))
		totallist.append(str(Common.count(developer+"TOTAL_DEV",TEMP_FILE)))   
		deslist.append(description)
		iconlist.append(iconimage)
		fanartlist.append(fanart)
		combinedlists = list(zip(countlist,totallist,namelist,urllist,hiddenlist,deslist,iconlist,fanartlist,useragentlist))
	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	dp.close()
	rank = 1
	for count,total,name,url,hidden,description,iconimage,fanart,ua in tup:
		developer = str(name.replace('[COLOR white][B]','').replace('[/B][/COLOR]','').replace('[/B][/COLOR]','').replace(' BUILDS',''))
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		if hidden != "false":
			url = hidden + "|SPLIT|" + url + "|SPLIT|" + ua
			if rank == 1:
				bname = "[B] | [COLOR gold] This Week:[/COLOR][COLOR gold] " + count + " - [COLOR gold]Total:[/COLOR][COLOR gold] " + total + "[/COLOR] - [COLOR red][PASSWORD PROTECTED][/COLOR][/B][/COLOR]"
				Common.addDir("[B][COLOR gold]1st - " + developer + "[/B][/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
			elif rank == 2:
				bname = "[B] | [COLOR silver] This Week:[/COLOR][COLOR silver] " + count + " - [COLOR silver]Total:[/COLOR][COLOR silver] " + total + "[/COLOR] - [COLOR red][PASSWORD PROTECTED][/COLOR][/B][/COLOR]"
				Common.addDir("[B][COLOR silver]2nd - " + developer + "[/B][/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
			elif rank == 3:
				bname = "[B] | [COLOR orange] This Week:[/COLOR][COLOR orange] " + count + " - [COLOR orange]Total:[/COLOR][COLOR orange] " + total + "[/COLOR] - [COLOR red][PASSWORD PROTECTED][/COLOR][/B][/COLOR]"
				Common.addDir("[B][COLOR orange]3rd - " + developer + "[/B][/COLOR]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
				Common.addItem("[COLOR white]-----------------------------------------------[/COLOR]",url,17,ICON,FANART,description)
			else:
				bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + " - [COLOR white]Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/COLOR] - [COLOR red][PASSWORD PROTECTED][/COLOR][/B][/COLOR]"
				Common.addDir("[COLOR white]" + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
		else:
			url = url + "|SPLIT|" + ua
			if rank == 1:
				bname = "[B] | [COLOR gold] This Week:[/COLOR][COLOR gold] " + count + "[/COLOR] - [COLOR gold]Total:[/COLOR][COLOR gold] " + total + "[/B][/COLOR]"
				Common.addDir("[B][COLOR gold]1st - " + developer + "[/COLOR][/B]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
			elif rank == 2:
				bname = "[B] | [COLOR silver] This Week:[/COLOR][COLOR silver] " + count + "[/COLOR] - [COLOR silver]Total:[/COLOR][COLOR silver] " + total + "[/B][/COLOR]"
				Common.addDir("[B][COLOR silver]2nd - " + developer + "[/COLOR][/B]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
			elif rank == 3:
				bname = "[B] | [COLOR orange] This Week:[/COLOR][COLOR orange] " + count + "[/COLOR] - [COLOR orange]Total:[/COLOR][COLOR orange] " + total + "[/B][/COLOR]"
				Common.addDir("[B][COLOR orange]3rd - " + developer + "[/COLOR][/B]"  + bname,url,93,iconimage,fanart,description)
				rank = rank + 1
				Common.addItem("[COLOR white]-----------------------------------------------[/COLOR]",url,17,ICON,FANART,description)
			else:
				bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR] - [COLOR white]Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
				Common.addDir("[COLOR white]" + developer + "[/COLOR]"  + bname,url,93,iconimage,fanart,description)
	
	Common.addItem('[B][COLOR yellowgreen]HOW TO ADD YOUR BUILDS TO THE LIST[/COLOR][/B]',BASEURL,17,COMMUNITY_ICON,FANART,'')

def SHOWCOMMUNITYBUILDS(name, url, description):

	try:
		contact = description.split(',')[2]
	except: contact = "Unknown"

	if not contact == "Unknown":
		Common.addItem("[COLOR white][B]Contact Details: [/COLOR][COLOR yellowgreen]" + str(contact) + "[/B][/COLOR]","url",999,ICON,FANART,description)

	try:
		url,ua = url.split("|SPLIT|")
	except:
		passed = 0

		try:
			hidden,url,ua = url.split("|SPLIT|")
		except:
			dialog.ok(AddonTitle, 'Sorry, an error occured! You are using a shortcut, please go through the wizards main menu to get to your desired location. If you do not know how to update from the wizard main menu please ask your build maker for assistence as I cannot help with this issue.')
			quit()
		
		vq = Common._get_keyboard( heading="Please Enter Your Password" )
		title = vq

		if len(title) == 0:
			quit()

		if title==hidden:
			passed = 1

		if passed == 0:
			dialog.ok(AddonTitle, "Sorry the password entered was not found.",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
			sys.exit(0)

	original = url

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	codename = "Decline"

	i=0
	dp.create(AddonTitle,"[COLOR blue]We are getting the list of builds from our server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
	dp.update(0)

	if version >= 16.0 and version < 17.0:
		codename = 'Jarvis'
	if version >= 17.0 and version < 18.0:
		codename = 'Krypton'

	v = str(version)
	vv = v.split(".")[0]
	vvv = vv + ".9"
	www = vv + ".0"
	version_start = float(www)
	version_end   = float(vvv)

	if 'endlessflix' in url:
		protected_wizards.Endless_Install()


	if 'CALL_THE_BEAST' in url:
		protected_wizards.Beast_Install()
		url = url.replace('CALL_THE_BEAST','')

	i=0
	dp.create(AddonTitle,"[COLOR blue]We are getting the list of developers from our server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
	dp.update(0)
	namelist=[]
	urllist=[]
	countlist=[]
	deslist=[]
	iconlist=[]
	fanartlist=[]
	totallist=[]
	combinedlists=[]
	desca = description
	developer = desca.split(',')[0]
	hidden = desca.split(',')[1]
	a = 0
	b = 0

	link = Common.OPEN_URL_CUSTOM(url,ua).replace('\n','').replace('\r','').replace(',','')
	
	link = link.replace("<notice></notice>","<notice>null</notice>").replace("<platform></platform>","<platform>16.1</platform>").replace("<youtube></youtube>","<youtube>null</youtube>").replace("<thumbnail></thumbnail>","<thumbnail>null</thumbnail>").replace("<fanart></fanart>","<fanart>null</fanart>").replace("<version></version>","<version>null</version>").replace("<build_image></build_image>","<build_image>null</build_image>")
	match= re.compile('<item>(.+?)</item>').findall(link)
	match2 = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
	dis_links1 = len(match)
	dis_links2 = len(match2)
	dis_links = dis_links1 + dis_links2
	for item in match:
		name=re.compile('<title>(.+?)</title>').findall(item)[0]
		url=re.compile('<link>(.+?)</link>').findall(item)[0]
		try:
			build_version=re.compile('<version>(.+?)</version>').findall(item)[0]
		except: build_version = "null"
		try:
			notice=re.compile('<notice>(.+?)</notice>').findall(item)[0]
		except: notice = "null"
		try:
			platform=re.compile('<platform>(.+?)</platform>').findall(item)[0]
		except: platform = "16.1"
		
		tubes=re.compile('<youtube>(.+?)</youtube>').findall(item)
		if len(tubes) > 1:
			youtube_id = "multi"
		else:
			try:
				youtube_id=re.compile('<youtube>(.+?)</youtube>').findall(item)[0]
			except: youtube_id = "null"
		try:
			iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
		except: iconimage = ICON
		try:
			fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
		except: fanart = FANART
		try:
			build_image=re.compile('<build_image>(.+?)</build_image>').findall(item)[0]
		except: build_image = "null"
		if iconimage.lower() == "null":
			iconimage = ICON
		if fanart.lower() == "null":
			fanart = FANART
		if platform == "16":
			platform = "16.1"
		if "16.0" in platform:
			platform = "16.1"
		if not "." in platform:
			platform = platform + ".0"
			platform = float(platform)
		else: platform = float(platform)
		i = i + 1
		dis_count = str(i)
		progress = 100 * int(i)/int(dis_links)
		dp.update(progress,"Getting details for developer " + str(dis_count) + " of " + str(dis_links),'',"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
		found = 1
		description = "null" + "," + developer + "," + youtube_id + "," + notice + "," + build_image + "," + contact
		name2 = name
		url = name2 + "," + url + "," + original
		name = name.lower()
		name=name.replace('(krypton)','').replace('(jarvis)','').replace('jarvis ','').replace('krypton ','')
		if build_version.lower() == "null":
			name = "[COLOR silver][B]" + name.title() + "[/B][/COLOR]"
		else: name = "[COLOR silver][B]" + name.title() + "[/COLOR] - [COLOR yellowgreen]Ver: " + build_version + "[/B][/COLOR] "
		if platform >= version_start and platform < version_end:
			namelist.append(name)
			urllist.append(url)
			countlist.append(str(Common.count(name2,TEMP_FILE)))
			totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))   
			deslist.append(description)
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			combinedlists = list(zip(countlist,totallist,namelist,urllist,deslist,iconlist,fanartlist))
	for name,url,iconimage,fanart in match2:
		i = i + 1
		dis_count = str(i)
		progress = 100 * int(i)/int(dis_links)
		dp.update(progress,"Getting details for developer " + str(dis_count) + " of " + str(dis_links),'',"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
		found = 1
		description = "null" + "," + developer  + "," + contact 
		name2 = name
		url = name2 + "," + url
		name = name.lower()
		name=name.replace('(krypton)','').replace('(jarvis)','').replace('jarvis ','').replace('krypton ','')
		name = "[COLOR silver][B]" + name.title() + "[/B][/COLOR]"

		if codename.lower() == "jarvis":
			if not "krypton" in name2.lower():
				namelist.append(name)
				urllist.append(url)
				countlist.append(str(Common.count(name2,TEMP_FILE)))
				totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))   
				deslist.append(description)
				iconlist.append(iconimage)
				fanartlist.append(fanart)
				combinedlists = list(zip(countlist,totallist,namelist,urllist,deslist,iconlist,fanartlist))
		else:
			if codename.lower() in name2.lower():
				namelist.append(name)
				urllist.append(url)
				countlist.append(str(Common.count(name2,TEMP_FILE)))
				totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))   
				deslist.append(description)
				iconlist.append(iconimage)
				fanartlist.append(fanart)
				combinedlists = list(zip(countlist,totallist,namelist,urllist,deslist,iconlist,fanartlist))

	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	for count,total,name,url,description,iconimage,fanart in tup:
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail	
		a = a + 1
		if "skip" in name.lower():
			name=name.replace('skip','')
			Common.addItem(name,url,999,iconimage,fanart,description)
		else:
			bname = "- [COLOR white]Week:[/COLOR] [COLOR yellowgreen][B]" + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR] [COLOR yellowgreen][B]" + total + "[/B][/COLOR]"
			Common.addDir(name + bname,url,97,iconimage,fanart,description)
	
	if a == 0:
		dialog.ok(AddonTitle, "[COLOR white]Sorry, no builds were found for " + codename + "![/COLOR]")
		sys,exit(1)

	try:
		f = open(COM_NOTICE,mode='r'); msg = f.read(); f.close()
		Common.TextBox('[COLOR yellowgreen][B]No Limits Tools Community Builds[/B][/COLOR]',"%s" % msg)
	except: pass

def SHOWPROTECTEDBUILDS(name, url, description):

	desca = description
	developer = desca.split(',')[0]
	hidden = desca.split(',')[1]
	
	try:
		youtube_id = desca.split(',')[2] 
	except: youtube_id = "null"

	try:
		link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
		match = re.compile('notice="(.+?)"').findall(link)
		for notice in match:
			dialog.ok(AddonTitle, '[COLOR red][B]' + notice + '[/B][/COLOR]')
	except: pass

	vq = Common._get_keyboard( heading="Please Enter Your Password" )
	if ( not vq ): return False, 0
	title = vq

	if "http" not in hidden:
		AUTH = BASEURL + "community/protected/" + hidden + '.txt'
	else:
		AUTH = hidden
	passed = 0
	link = Common.OPEN_URL(AUTH).replace('\n','').replace('\r','')
	match = re.compile('passkey="(.+?)"').findall(link)
	for passkey in match:
		if title==passkey:
			passed = 1

	if passed == 0:
		dialog.ok(AddonTitle, "Sorry the password entered was not found.",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
		sys.exit(0)

	link = Common.OPEN_URL(url).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
	for name,url,iconimage,fanart in match:
		description = "null" + "," + developer + "," + youtube_id 
		name2 = name
		url = name2 + "," + url
		name = "[COLOR silver][B]" + name + "[/B][/COLOR]"
		bname = "- [COLOR white]Week:[/COLOR] [COLOR yellowgreen][B]" + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR] [COLOR yellowgreen][B]" + total + "[/B][/COLOR]"
		Common.addDir(name + bname,url,97,iconimage,fanart,description)

	try:
		f = open(COM_NOTICE,mode='r'); msg = f.read(); f.close()
		Common.TextBox('[COLOR aqua][B]No Limits Tools Community Builds[/B][/COLOR]',"%s" % msg)
	except: pass

#######################################################################
#                       Community
#######################################################################
def CommunityBuilds():
    
    dialog = xbmcgui.Dialog()
    dialog.ok(AddonTitle, "[COLOR white]If you would like your build to be hosted by[/COLOR]", "[COLOR silver]No Limits[/COLOR] [COLOR lightsteelblue]Tools[/COLOR]  [COLOR white]please visit:[/COLOR]", "[COLOR smokewhite]http://www.kodinolimits.com/forum [/COLOR]")
