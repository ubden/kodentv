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
import time
from resources.lib.modules import downloader
import requests
from resources.lib.modules import common as Common
from resources.lib.modules import wipe
import re
import zipfile
import hashlib
from resources.lib.modules import skinSwitch
from resources.lib.modules import backuprestore

ADDONTITLE          = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
USERDATA            =  xbmc.translatePath(os.path.join('special://home/userdata',''))
NOLIMITS_VERSION    =  os.path.join(USERDATA,'nolimits_build.txt')
skin                =  xbmc.getSkinDir()
KODIV               =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
FAVS_NEW            =  xbmc.translatePath(os.path.join(USERDATA,'favourites_RESTORE.xml'))
FAVS                =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
HOME                =  xbmc.translatePath('special://home/')
TMP_TRAKT           =  xbmc.translatePath(os.path.join(HOME,'tmp_trakt'))
TRAKT_MARKER        =  xbmc.translatePath(os.path.join(TMP_TRAKT,'marker.xml'))
BASEURL             = base64.b64decode(b"aHR0cDovL2VjaG9jb2Rlci5jb20v")
ADDON_DATA          =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
EXCLUDES_FOLDER     =  xbmc.translatePath(os.path.join(USERDATA,'BACKUP'))
COMMUNITY_BUILD	    =  xbmc.translatePath(os.path.join('special://home/userdata/','community_build.txt'))
COM_DOWNLOAD_ERROR  = BASEURL + base64.b64decode(b"b3RoZXIvY29tbXVuaXR5X2Rvd25sb2FkX2Vycm9yLnR4dA==")

############################
###INSTALL BUILD############
############################
	
def INSTALL(name,url,description):
	urla = url
	desca = description

	notice2,description,fresh,youtube,skin_used,build_notice = desca.split(',')
	name,url = urla.split(',')
	wipeme = 0
	xxl = 0
	skipskin = 0
	skin_swapped = 0
	skin         =  xbmc.getSkinDir()
	KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
	skinswapped = 0
	SKIP_FAVS = 0

	if "lose your favourites" in notice2.lower():
		SKIP_FAVS = 1

	if not "skin." in skin_used:
		skin_used = "NULL"

	if fresh == "1":
		wipeme = 1
	else:
		wipeme = 0
		skipskin = 1	

	#SWITCH THE SKIN IF THE CURRENT SKIN IS NOT CONFLUENCE
	if skin not in ['skin.confluence','skin.estuary'] and skipskin == 0:
		skin = 'skin.estuary' if KODIV >= 17 else 'skin.confluence'
		skinSwitch.swapSkins(skin)
		skinswapped = 1
		time.sleep(2)
	
	#IF A SKIN SWAP HAS HAPPENED CHECK IF AN OK DIALOG (CONFLUENCE INFO SCREEN) IS PRESENT, PRESS OK IF IT IS PRESENT
	if skinswapped == 1:
		if not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Select)" )
	
	#IF THERE IS NOT A YES NO DIALOG (THE SCREEN ASKING YOU TO SWITCH TO CONFLUENCE) THEN SLEEP UNTIL IT APPEARS
	if skinswapped == 1:
		while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			time.sleep(1)
	
	#WHILE THE YES NO DIALOG IS PRESENT PRESS LEFT AND THEN SELECT TO CONFIRM THE SWITCH TO CONFLUENCE.
	if skinswapped == 1:
		while xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Left)" )
			xbmc.executebuiltin( "Action(Select)" )
			time.sleep(1)
	
	skin         =  xbmc.getSkinDir()

	#CHECK IF THE SKIN IS NOT CONFLUENCE
	if skin not in ['skin.confluence','skin.estuary']:
		if skin_swapped == 1:
			choice = xbmcgui.Dialog().yesno(ADDONTITLE, '[COLOR lightskyblue][B]ERROR: AUTOSWITCH WAS NOT SUCCESSFUL[/B][/COLOR]','[COLOR lightskyblue][B]CLICK YES TO MANUALLY SWITCH TO CONFLUENCE NOW[/B][/COLOR]','[COLOR lightskyblue][B]YOU CAN PRESS NO AND ATTEMPT THE AUTO SWITCH AGAIN IF YOU WISH[/B][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
			if choice == 1:
				xbmc.executebuiltin("ActivateWindow(appearancesettings)")
				return
			else:
				sys.exit(1)

	if wipeme == 1:
		found_trakt = 0
		link=Common.OPEN_URL(BASEURL + base64.b64decode(b'b3RoZXIvcmRfdHJha3QueG1s'))
		plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
		for match in plugins:
			ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
			ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
			EXCLUDEMOVE = xbmc.translatePath(os.path.join(EXCLUDES_FOLDER,match+'_settings.xml'))
		
			if os.path.isfile(ADDONSETTINGS):
				found_trakt = 1

		if SKIP_FAVS == 1:
			keep_kodi_favs = 0
			keep_trakt_rd = 0

			if found_trakt == 1:
				found_a = 0
				dialog = xbmcgui.Dialog()
				choice = dialog.select('[COLOR lightskyblue][B]TRAKT AND RD SETTINGS DETECTED[/B][/COLOR]', ['[COLOR yellowgreen][B]Yes, Keep Trakt & Real Debrid Settings[/B][/COLOR]','[COLOR lightskyblue][B]No, Remove My Settings[/B][/COLOR]'])
				if choice == 0:
					keep_trakt_rd = 1
					found_a = 1
				if choice == 1:
					keep_trakt_rd = 0
					found_a = 1
				if found_a == 0:
					sys.exit(1)
		else:
			found_favourites = 0
			if os.path.isfile(FAVS):
				found_favourites = 1

			keep_kodi_favs = 0
			keep_trakt_rd = 0

			if found_favourites == 1 and found_trakt == 1:
				found_c = 0
				dialog = xbmcgui.Dialog()
				choice = dialog.select('[COLOR lightskyblue][B]TRAKT, RD & FAVOURITES DETECTED[/B][/COLOR]', ['[COLOR lightskyblue][B]KEEP BOTH RD, TRAKT & FAVOURITES[/B][/COLOR]','[COLOR yellowgreen][B]Only Keep Trakt & Real Debrid Settings[/B][/COLOR]','[COLOR yellowgreen][B]Only Keep Kodi Favourites[/B][/COLOR]','[COLOR lightskyblue][B]Remove All Settings & Favourites[/B][/COLOR]'])
				if choice == 0:
					keep_trakt_rd = 1
					keep_kodi_favs = 1
					found_c = 1
				if choice == 1:
					keep_trakt_rd = 1
					keep_kodi_favs = 0
					found_c = 1
				if choice == 2:
					keep_trakt_rd = 0
					keep_kodi_favs = 1
					found_c = 1
				if choice == 3:
					keep_trakt_rd = 0
					keep_kodi_favs = 0
					found_c = 1
				if found_c == 0:
					sys.exit(1)

			if found_favourites == 1 and found_trakt == 0:
				found_b = 0
				dialog = xbmcgui.Dialog()
				choice = dialog.select('[COLOR lightskyblue][B]KODI FAVOURITES DETECTED[/B][/COLOR]', ['[COLOR yellowgreen][B]Yes, Keep Favourites[/B][/COLOR]','[COLOR lightskyblue][B]No Use The Builds Favourites[/B][/COLOR]'])
				if choice == 0:
					found_b = 1
					keep_kodi_favs = 1
				if choice == 1:
					found_b = 1
					keep_kodi_favs = 0
				if found_b == 0:
					sys.exit(1)

			if found_favourites == 0 and found_trakt == 1:
				found_a = 0
				dialog = xbmcgui.Dialog()
				choice = dialog.select('[COLOR lightskyblue][B]TRAKT AND RD SETTINGS DETECTED[/B][/COLOR]', ['[COLOR yellowgreen][B]Yes, Keep Trakt & Real Debrid Settings[/B][/COLOR]','[COLOR lightskyblue][B]No, Remove My Settings[/B][/COLOR]'])
				if choice == 0:
					keep_trakt_rd = 1
					found_a = 1
				if choice == 1:
					keep_trakt_rd = 0
					found_a = 1
				if found_a == 0:
					sys.exit(1)

		if keep_trakt_rd == 1:
			backuprestore.AUTO_BACKUP_RD_TRAKT()

		wipe.WIPERESTORE(keep_kodi_favs)

	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = name
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"Please wait while we get everything ready to","download the " + buildname + " build.","[B]Build: [/B]" + buildname)
	buildname = "build"
	lib=os.path.join(path, buildname+'.zip')
		
	try:
		os.remove(lib)
	except:
		pass
	
	if description.lower() != "null":
		hash = "null"
		while hash.lower() != description.lower():
			dialog = xbmcgui.Dialog()
			downloader.download(url, lib, dp)
			addonfolder = xbmc.translatePath(os.path.join('special://','home'))
			dp.update(0,"","Checking Zip File Integrity","Please Wait..")
			hash = hashlib.md5(open(lib, 'rb').read()).hexdigest()		
			if hash.lower() != description.lower():
				choice = xbmcgui.Dialog().yesno(ADDONTITLE, 'Error: Unfortunatly the ZIP file hash does not match.','The file has therefore been flagged as corrupt.','Would you like to download the file again?',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]',yeslabel='[B][COLOR yellowgreen]YES[/COLOR][/B]')
				if choice == 0:
					try:
						os.remove(lib)
					except: pass
					sys.exit(1)
				else:
					try:
						os.remove(lib)
					except: pass
	else:
		dialog = xbmcgui.Dialog()
		downloader.download(url, lib, dp)
		addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	dp.update(0,"Extracting Zip Please Wait"," "," ")
	unzip(lib,addonfolder,dp)
	try:
		os.remove(lib)
	except:
		pass

	send_to_count = name + "|SPLIT|No Limits"
	add_download = Common.add_one(send_to_count)

	if os.path.isfile(FAVS_NEW):
		if os.path.isfile(FAVS):
			try:
				os.remove(FAVS)
				os.rename(FAVS_NEW, FAVS)
			except: pass
		else:
			try:
				os.rename(FAVS_NEW, FAVS)
			except: pass

	MARKER_TRAKT = xbmc.translatePath(os.path.join(TMP_TRAKT,'marker.xml'))
	if os.path.isfile(MARKER_TRAKT):
		backup_zip = xbmc.translatePath(os.path.join(TMP_TRAKT,'Restore_RD_Trakt_Settings.zip'))
		backuprestore.AUTO_READ_ZIP_TRAKT(backup_zip)
		_out = xbmc.translatePath(os.path.join('special://','home/tmp_trakt'))
		try:
			os.remove(MARKER_TRAKT)
			shutil.rmtree(_out)
			shutil.rmdir(_out)
		except: pass

	skin_swapped = 0
	skin         =  xbmc.getSkinDir()
	if "skin." in skin_used:
		#SWITCH THE SKIN IF THE CURRENT SKIN IS NOT CONFLUENCE
		if skin not in [skin_used]:
			skin_swapped = 1
			xbmc.executebuiltin("UpdateAddonRepos")
			xbmc.executebuiltin("UpdateLocalAddons")
			xbmc.executebuiltin("RefreshRSS")
			skin = skin_used if KODIV >= 17 else skin_used
			skinSwitch.swapSkins(skin)
			time.sleep(1)
	
		#IF A SKIN SWAP HAS HAPPENED CHECK IF AN OK DIALOG (CONFLUENCE INFO SCREEN) IS PRESENT, PRESS OK IF IT IS PRESENT
		if not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Select)" )
	
		#IF THERE IS NOT A YES NO DIALOG (THE SCREEN ASKING YOU TO SWITCH TO CONFLUENCE) THEN SLEEP UNTIL IT APPEARS
		while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			time.sleep(1)
	
	#WHILE THE YES NO DIALOG IS PRESENT PRESS LEFT AND THEN SELECT TO CONFIRM THE SWITCH TO CONFLUENCE.
		while xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Left)" )
			xbmc.executebuiltin( "Action(Select)" )
			time.sleep(1)
	
	skin         =  xbmc.getSkinDir()

	if skin != skin_used:
		if skin_swapped == 1:
			choice = xbmcgui.Dialog().yesno(ADDONTITLE, '[COLOR lightskyblue][B]ERROR: AUTOSWITCH WAS NOT SUCCESSFUL[/B][/COLOR]','[COLOR lightskyblue][B]CLICK YES TO MANUALLY SWITCH NOW[/B][/COLOR]','', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
			if choice == 1:
				xbmc.executebuiltin("ActivateWindow(appearancesettings)")
				return
			else:
				sys.exit(1)

	if skin_swapped == 1:
		dialog.ok(ADDONTITLE, '[B][COLOR smokewhite]Your build has been installed.[/COLOR][/B]','[B][COLOR orangered]YOU DO NOT NEED TO CLOSE KODI[/COLOR][/B].', '[COLOR white]Please press OK to enjoy your build![/COLOR]')
		xbmc.executebuiltin( "ActivateWindow(Home)" )
		sys.exit(1)
	else:
		dialog.ok(ADDONTITLE, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
		Common.killxbmc()

def INSTALL_COMMUNITY(name,url,description):
	urla = url
	name,url,skin_used,developer = urla.split(',')
	skin         =  xbmc.getSkinDir()
	KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
	skinswapped = 0

	raw_name = name.split('-')[0]

	if not "skin." in skin_used:
		skin_used = "NULL"

	#SWITCH THE SKIN IF THE CURRENT SKIN IS NOT CONFLUENCE
	if skin not in ['skin.confluence','skin.estuary']:
		choice = xbmcgui.Dialog().yesno(ADDONTITLE, '[COLOR lightskyblue][B]We can see that you are not using the default confluence skin.[/B][/COLOR]','[COLOR lightskyblue][B]CLICK YES TO ATTEMPT TO AUTO SWITCH TO CONFLUENCE[/B][/COLOR]','[COLOR lightskyblue][B]PLEASE DO NOT DO PRESS ANY BUTTONS OR MOVE THE MOUSE WHILE THIS PROCESS IS TAKING PLACE, IT IS AUTOMATIC[/B][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
		if choice == 0:
			sys.exit(1)
		skin = 'skin.estuary' if KODIV >= 17 else 'skin.confluence'
		skinSwitch.swapSkins(skin)
		skinswapped = 1
		time.sleep(1)
	
	#IF A SKIN SWAP HAS HAPPENED CHECK IF AN OK DIALOG (CONFLUENCE INFO SCREEN) IS PRESENT, PRESS OK IF IT IS PRESENT
	if skinswapped == 1:
		if not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Select)" )
	
	#IF THERE IS NOT A YES NO DIALOG (THE SCREEN ASKING YOU TO SWITCH TO CONFLUENCE) THEN SLEEP UNTIL IT APPEARS
	if skinswapped == 1:
		while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			time.sleep(1)
	
	#WHILE THE YES NO DIALOG IS PRESENT PRESS LEFT AND THEN SELECT TO CONFIRM THE SWITCH TO CONFLUENCE.
	if skinswapped == 1:
		while xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Left)" )
			xbmc.executebuiltin( "Action(Select)" )
			time.sleep(1)
	
	skin         =  xbmc.getSkinDir()

	#CHECK IF THE SKIN IS NOT CONFLUENCE
	if skin not in ['skin.confluence','skin.estuary']:
		if skinswapped == 1:
			choice = xbmcgui.Dialog().yesno(ADDONTITLE, '[COLOR lightskyblue][B]ERROR: AUTOSWITCH WAS NOT SUCCESFULL[/B][/COLOR]','[COLOR lightskyblue][B]CLICK YES TO MANUALLY SWITCH TO CONFLUENCE NOW[/B][/COLOR]','[COLOR lightskyblue][B]YOU CAN PRESS NO AND ATTEMPT THE AUTO SWITCH AGAIN IF YOU WISH[/B][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
			if choice == 1:
				xbmc.executebuiltin("ActivateWindow(appearancesettings)")
				return
			else:
				sys.exit(1)

	found_trakt = 0
	link=Common.OPEN_URL(BASEURL + base64.b64decode(b'b3RoZXIvcmRfdHJha3QueG1s'))
	plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
	for match in plugins:
		ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
		ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
		EXCLUDEMOVE = xbmc.translatePath(os.path.join(EXCLUDES_FOLDER,match+'_settings.xml'))
	
		if os.path.isfile(ADDONSETTINGS):
			found_trakt = 1
	
	found_favourites = 0
	if os.path.isfile(FAVS):
		found_favourites = 1
		
	keep_kodi_favs = 0
	keep_trakt_rd = 0

	if found_favourites == 1 and found_trakt == 1:
		found_c = 0
		dialog = xbmcgui.Dialog()
		choice = dialog.select('[COLOR lightskyblue][B]TRAKT, RD & FAVOURITES DETECTED[/B][/COLOR]', ['[COLOR lightskyblue][B]KEEP BOTH RD, TRAKT & FAVOURITES[/B][/COLOR]','[COLOR yellowgreen][B]Only Keep Trakt & Real Debrid Settings[/B][/COLOR]','[COLOR yellowgreen][B]Only Keep Kodi Favourites[/B][/COLOR]','[COLOR lightskyblue][B]Remove All Settings & Favourites[/B][/COLOR]'])
		if choice == 0:
			keep_trakt_rd = 1
			keep_kodi_favs = 1
			found_c = 1
		if choice == 1:
			keep_trakt_rd = 1
			keep_kodi_favs = 0
			found_c = 1
		if choice == 2:
			keep_trakt_rd = 0
			keep_kodi_favs = 1
			found_c = 1
		if choice == 3:
			keep_trakt_rd = 0
			keep_kodi_favs = 0
			found_c = 1
		if found_c == 0:
			sys.exit(1)

	if found_favourites == 1 and found_trakt == 0:
		found_b = 0
		dialog = xbmcgui.Dialog()
		choice = dialog.select('[COLOR lightskyblue][B]KODI FAVOURITES DETECTED[/B][/COLOR]', ['[COLOR yellowgreen][B]Yes, Keep Favourites[/B][/COLOR]','[COLOR lightskyblue][B]No Use The Builds Favourites[/B][/COLOR]'])
		if choice == 0:
			found_b = 1
			keep_kodi_favs = 1
		if choice == 1:
			found_b = 1
			keep_kodi_favs = 0
		if found_b == 0:
			sys.exit(1)

	if found_favourites == 0 and found_trakt == 1:
		found_a = 0
		dialog = xbmcgui.Dialog()
		choice = dialog.select('[COLOR lightskyblue][B]TRAKT AND RD SETTINGS DETECTED[/B][/COLOR]', ['[COLOR yellowgreen][B]Yes, Keep Trakt & Real Debrid Settings[/B][/COLOR]','[COLOR lightskyblue][B]No, Remove My Settings[/B][/COLOR]'])
		if choice == 0:
			keep_trakt_rd = 1
			found_a = 1
		if choice == 1:
			keep_trakt_rd = 0
			found_a = 1
		if found_a == 0:
			sys.exit(1)
	
	if keep_trakt_rd == 1:
		backuprestore.AUTO_BACKUP_RD_TRAKT()
		
	wipe.WIPERESTORE(keep_kodi_favs)

	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = name
	raw_name_string = str(raw_name)
	raw_name = 	raw_name_string.replace('[B]','').replace('[/B]','')
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"Please wait while we get everything ready to","download the " + raw_name + " build."," ")
	buildname = "build"
	lib=os.path.join(path, buildname+'.zip')
	try:
		os.remove(lib)
	except: pass
	dialog = xbmcgui.Dialog()
	dp.update(0,"","","[B]Build: [/B]" + raw_name)
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	dp.update(0,"","Extracting Zip File","")
	unzip(lib,addonfolder,dp)
	time.sleep(1)
	send_to_count = name + "|SPLIT|" + developer
	add_download = Common.add_one(send_to_count)
	try:
		os.remove(lib)
	except:
		pass

	if os.path.isfile(FAVS_NEW):
		if os.path.isfile(FAVS):
			try:
				os.remove(FAVS)
				os.rename(FAVS_NEW, FAVS)
			except: pass
		else:
			try:
				os.rename(FAVS_NEW, FAVS)
			except: pass

	MARKER_TRAKT = xbmc.translatePath(os.path.join(TMP_TRAKT,'marker.xml'))
	if os.path.isfile(MARKER_TRAKT):
		backup_zip = xbmc.translatePath(os.path.join(TMP_TRAKT,'Restore_RD_Trakt_Settings.zip'))
		backuprestore.AUTO_READ_ZIP_TRAKT(backup_zip)
		_out = xbmc.translatePath(os.path.join('special://','home/tmp_trakt'))
		try:
			os.remove(MARKER_TRAKT)
			shutil.rmtree(_out)
			shutil.rmdir(_out)
		except: pass

	skin_swapped = 0
	skin         =  xbmc.getSkinDir()
	if "skin." in skin_used:
		#SWITCH THE SKIN IF THE CURRENT SKIN IS NOT CONFLUENCE
		if skin not in [skin_used]:
			skin_swapped = 1
			xbmc.executebuiltin("UpdateAddonRepos")
			xbmc.executebuiltin("UpdateLocalAddons")
			xbmc.executebuiltin("RefreshRSS")
			skin = skin_used if KODIV >= 17 else skin_used
			skinSwitch.swapSkins(skin)
			time.sleep(1)
	
		#IF A SKIN SWAP HAS HAPPENED CHECK IF AN OK DIALOG (CONFLUENCE INFO SCREEN) IS PRESENT, PRESS OK IF IT IS PRESENT
		if not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Select)" )
	
		#IF THERE IS NOT A YES NO DIALOG (THE SCREEN ASKING YOU TO SWITCH TO CONFLUENCE) THEN SLEEP UNTIL IT APPEARS
		while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			time.sleep(1)
	
	#WHILE THE YES NO DIALOG IS PRESENT PRESS LEFT AND THEN SELECT TO CONFIRM THE SWITCH TO CONFLUENCE.
		while xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
			xbmc.executebuiltin( "Action(Left)" )
			xbmc.executebuiltin( "Action(Select)" )
			time.sleep(1)
	
	skin         =  xbmc.getSkinDir()

	if skin != skin_used:
		if skin_swapped == 1:
			choice = xbmcgui.Dialog().yesno(ADDONTITLE, '[COLOR lightskyblue][B]ERROR: AUTOSWITCH WAS NOT SUCCESFULL[/B][/COLOR]','[COLOR lightskyblue][B]CLICK YES TO MANUALLY SWITCH NOW[/B][/COLOR]','', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
			if choice == 1:
				xbmc.executebuiltin("ActivateWindow(appearancesettings)")
				return
			else:
				sys.exit(1)

	if skin_swapped == 1:
		open(COMMUNITY_BUILD, 'w')
		dialog.ok(ADDONTITLE, '[B][COLOR smokewhite]Your build has been installed.[/COLOR][/B]','[B][COLOR orangered]YOU DO NOT NEED TO CLOSE KODI[/COLOR][/B].', '[COLOR white]Please press OK to enjoy your build![/COLOR]')
		xbmc.executebuiltin( "ActivateWindow(Home)" )
		sys.exit(1)
	else:
		open(COMMUNITY_BUILD, 'w')
		dialog.ok(ADDONTITLE, "To save changes you now need to force close Kodi, Press OK to force close Kodi")
		Common.killxbmc()
	
def INSTALL_FANRIFFIC(name,url,description):	
	buildname,url = url.split("|SPLIT|")

	choice = xbmcgui.Dialog().yesno(ADDONTITLE, '[COLOR white]Do you wish to download the ' + buildname + ' theme?[/COLOR]','',yeslabel='[B][COLOR yellowgreen]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
	if choice == 0:
		sys.exit(1)

	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"Please wait while we get everything ready to","download the " + buildname + " build.","[B]Build: [/B]" + buildname)
	lib=os.path.join(path, 'theme.zip')
		
	try:
		os.remove(lib)
	except:
		pass

	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	dp.update(0,"Extracting Zip Please Wait",""," ")
	unzip(lib,addonfolder,dp)
	send_to_count = buildname + "|SPLIT|Fanriffic"
	add_download = Common.add_one(send_to_count)
	dialog = xbmcgui.Dialog()
	dialog.ok(ADDONTITLE, "The theme has now been installed. To save the changes you must now force close Kodi.")
	Common.killxbmc()

def INSTALL_ADVANCED(name,url,description):
	name,url = url.split("|SPLIT|")

	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons/','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	buildname = name
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"","","[B]Build: [/B]" + buildname)
	buildname = "build"
	lib=os.path.join(path, buildname+'.zip')
	
	try:
		os.remove(lib)
	except:
		pass

	dialog = xbmcgui.Dialog()
	downloader.download(url, lib, dp)

	addonfolder = xbmc.translatePath(os.path.join('special://home/','userdata'))
	time.sleep(2)
	dp.update(0,"Extracting Zip Please Wait",""," ")
	unzip(lib,addonfolder,dp)
	time.sleep(1)
	try:
		os.remove(lib)
	except:
		pass
	send_to_count = name + "|SPLIT|Advanced Settings"
	add_download = Common.add_one(send_to_count)
	xbmc.executebuiltin("Container.Refresh")

	dialog.ok(ADDONTITLE, "[COLOR white]Advanced Settings installed![/COLOR]","[COLOR white]You should now see an imporvment in buffering[/COLOR]","[COLOR white]Thank you for using No Limits Tools![/COLOR]")


def INSTALL_KEYMAP(name,url,description):
	name,url = url.split("|SPLIT|")

	KEYBOARD_FILE   =  xbmc.translatePath(os.path.join('special://home/userdata/keymaps/','keyboard.xml'))
	if os.path.isfile(KEYBOARD_FILE):
		try:
			os.remove(KEYBOARD_FILE)
		except: pass
	#Check is the packages folder exists, if not create it.
	path = xbmc.translatePath(os.path.join('special://home/addons/','packages'))
	if not os.path.exists(path):
		os.makedirs(path)
	path_key = xbmc.translatePath(os.path.join('special://home/userdata/','keymaps'))
	if not os.path.exists(path_key):
		os.makedirs(path_key)
	buildname = name
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"","","[B]Build: [/B]" + buildname)
	buildname = "build"
	lib=os.path.join(path, buildname+'.zip')
	
	try:
		os.remove(lib)
	except:
		pass

	dialog = xbmcgui.Dialog()
	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	time.sleep(2)
	dp.update(0,"Extracting Zip Please Wait",""," ")
	unzip(lib,addonfolder,dp)
	time.sleep(1)
	send_to_count = name + "|SPLIT|Keymaps"
	add_download = Common.add_one(send_to_count)
	try:
		os.remove(lib)
	except:
		pass

	xbmc.executebuiltin("Container.Refresh")
	dialog.ok(ADDONTITLE, "[COLOR white]Custom Keymap settings installed![/COLOR]","[COLOR white]Thank you for using No Limits Tools![/COLOR]")

def INSTALLAPK(name,url,description):
	if "NULL" in url:
		dialog = xbmcgui.Dialog()
		dialog.ok(ADDONTITLE, "[B][COLOR smokewhite]Not a valid selection, please try again.[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
		sys.exit(1)

	path = xbmc.translatePath(os.path.join('/storage/emulated/0/Download',''))
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"","",'APK: ' + name)
	lib=os.path.join(path, name+'.apk')
	downloader.download(url, lib, dp)
	dialog = xbmcgui.Dialog()
	dialog.ok(ADDONTITLE, "Launching the APK to be installed" , "Follow the install process to complete.")
	xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:' + lib + '")' )

def INSTALLAPK_INSTALLER(name,url,description):
	dialog = xbmcgui.Dialog()
	name,url = url.split('#!')
	dialog.ok(ADDONTITLE, str(name))

	#add_download = Common.add_one_addons_week(name)

	path = xbmc.translatePath(os.path.join('/storage/emulated/0/Download',''))
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"","",'APK: ' + name)
	new_name = name.replace(' ','')
	lib=os.path.join(path, name+'.apk')
	downloader.download(url, lib, dp)
	dialog = xbmcgui.Dialog()

	dialog.ok(ADDONTITLE, "Launching the APK to be installed" , "Follow the install process to complete.")
	xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:' + lib + '")' )

def INSTALLEXE(name,url,description):
	if "NULL" in url:
		dialog = xbmcgui.Dialog()
		dialog.ok(ADDONTITLE, "[B][COLOR smokewhite]Not a valid selection, please try again.[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
		sys.exit(1)
			
	path = xbmc.translatePath(os.path.join('special://home/','Downloads'))
	if not os.path.exists(path):
		os.makedirs(path)
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"","",'File: ' + name)
	lib=os.path.join(path, name)
	downloader.download(url, lib, dp)
	dialog = xbmcgui.Dialog()
	dialog.ok(ADDONTITLE, "[COLOR smokewhite]Download complete, File Location: [/COLOR][COLOR white]" + lib + "[/COLOR]")
		
def INSTALLLIB(name,url,description):
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"","","")

	if "Android" in name:
		if not xbmc.getCondVisibility('system.platform.android'):
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE + " - Android", "[B][COLOR smokewhite]Sorry, this file is only for Android devices[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
			sys.exit(1)
		else:	
			name = "librtmp.so"
			path = xbmc.translatePath(os.path.join('special://home',''))
	
	if "Windows" in name:
		if not xbmc.getCondVisibility('system.platform.windows'):
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE + " - Windows", "[B][COLOR smokewhite]Sorry, this file is only for Windows devices[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
			sys.exit(1)
		else:	
			name = "librtmp.dll"
			path = 'C:\Program Files (x86)\Kodi\system\players\dvdplayer'
			if not os.path.exists(path):
				path = 'C:\Program Files\Kodi\system\players\dvdplayer'
			lib=os.path.join(path, name)
			try:
				os.remove(lib)
			except:
				dialog = xbmcgui.Dialog()
				dialog.ok(ADDONTITLE + " - Windows", "[B][COLOR smokewhite]Sorry, we could not remove the old lib file[/COLOR][/B]",'[COLOR smokewhite]Please run Kodi as ADMINISTRATOR and try again.[/COLOR]')
				sys.exit(1)

	if "Linux" in name:
		if not xbmc.getCondVisibility('system.platform.linux'):
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE + " - Linux", "[B][COLOR smokewhite]Sorry, this file is only for Linux devices[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
			sys.exit(1)
		else:	
			name = "librtmp.so.1"
			path = xbmc.translatePath(os.path.join('special://home',''))
			
	if "osx" in name:
		if not xbmc.getCondVisibility('system.platform.osx'):
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE + " - MacOSX", "[B][COLOR smokewhite]Sorry, this file is only for MacOSX devices[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
			sys.exit(1)
		else:	
			name = "librtmp.1.dylib"
			path = xbmc.translatePath(os.path.join('special://home',''))

	if "ATV" in name:
		if not xbmc.getCondVisibility('system.platform.atv2'):
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE + " - ATV", "[B][COLOR smokewhite]Sorry, this file is only for ATV devices[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
			sys.exit(1)
		else:	
			name = "librtmp.1.dylib"
			path = xbmc.translatePath(os.path.join('special://home',''))
		
	if "iOS" in name:
		if not xbmc.getCondVisibility('system.platform.ios'):
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE + " - iOS", "[B][COLOR smokewhite]Sorry, this file is only for iOS devices[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
			sys.exit(1)
		else:	
			name = "librtmp.1.dylib"
			path = xbmc.translatePath(os.path.join('special://home',''))
			
	if "RPi" in name:
		if not xbmc.getCondVisibility('system.platform.rpi'):
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE + " - RPi", "[B][COLOR smokewhite]Sorry, this file is only for RPi devices[/COLOR][/B]",'[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
			sys.exit(1)
		else:	
			name = "librtmp.1.so"
			path = xbmc.translatePath(os.path.join('special://home',''))

	lib=os.path.join(path, name)
	try:
		os.remove(lib)
	except:
		pass
	downloader.download(url, lib, dp)
	dialog = xbmcgui.Dialog()
	dialog.ok(ADDONTITLE, "[COLOR smokewhite]Download complete, Lib Location: [/COLOR][COLOR white]" + lib + "[/COLOR]")

def unzip(_in, _out, dp):
	try:
		__in = zipfile.ZipFile(_in,  'r')
	except:
		dialog = xbmcgui.Dialog()
		import traceback as tb
		(etype, value, traceback) = sys.exc_info() 
		tb.print_exception(etype, value, traceback)
		error_traceback = tb.format_tb(traceback)
		if "bytes" in str(error_traceback).lower():
			dialog.ok(ADDONTITLE, 'Sorry, your connection to the download was lost before the file could be downloaded. Please try again.','If problems persist please contact @kodinolimits or if you are downloading a Community Build please contact them with this.')
			dp.close()
			quit()
		elif "file is not a zip file" in str(error_traceback).lower():
			dialog.ok(ADDONTITLE, 'Sorry, the file is not a zip file.','If problems persist please contact @kodinolimits or if you are downloading a Community Build please contact them with this.')
			dp.close()
			quit()
		else:
			dialog.ok(ADDONTITLE, 'Sorry, there was a problem extracting the file.','If problems persist please contact @kodinolimits or if you are downloading a Community Build please contact them with this.')
			dp.close()
			quit()
	nofiles = float(len(__in.infolist()))
	count   = 0

	try:
		for item in __in.infolist():
			count += 1
			update = (count / nofiles) * 100
			
			if dp.iscanceled():
				dialog = xbmcgui.Dialog()
				dialog.ok(ADDONTITLE, 'Extraction was cancelled.')
				
				sys.exit()
				dp.close()
			
			try:
				dp.update(int(update),'','[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
				__in.extract(item, _out)
			
			except Exception, e:
				print str(e)

	except Exception, e:
		print str(e)
		return False