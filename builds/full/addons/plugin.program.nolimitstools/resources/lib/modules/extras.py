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
#######################################################################
#						GET ALL DEPENDANCIES NEEDED
#######################################################################
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
from resources.lib.modules import common as Common
import time
from resources.lib.modules import extract
import shutil
from resources.lib.modules import downloader
from resources.lib.modules import installer

#######################################################################
#					VERIABLES NEEDED
#######################################################################

ADDONTITLE        = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
ADDON_ID          = 'plugin.program.nolimitstools'
ADDON             = xbmcaddon.Addon(id=ADDON_ID)
skin              = xbmc.getSkinDir()
FANART            = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID , 'fanart.jpg'))
ICON              = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'icon.png'))
SKIN_DIR          = xbmc.translatePath(os.path.join('special://home/addons',skin))
BASEURL           = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
dialog            = xbmcgui.Dialog()
AdvancedSettings  = xbmc.translatePath('special://userdata/advancedsettings.xml')
EXTRAS_ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/extras.png'))
PLAYER_CORE       = xbmc.translatePath('special://userdata/playercorefactory.xml')
YOUTUBE_INSTALL   = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.youtube'))
YOUTUBE_DATA      = xbmc.translatePath('special://userdata/addon_data/plugin.video.youtube')
GUIDE             = xbmc.translatePath('special://userdata/addon_data/plugin.program.echotvguide')

#######################################################################
#						EXTRAS MENU
#######################################################################

def EXTRAS_MENU():

	match = 0
 	INTRO_ENABLE  = xbmc.translatePath(os.path.join(SKIN_DIR,'extras/TDBINTRO.MP4'))
	INTRO_DISABLE = xbmc.translatePath(os.path.join(SKIN_DIR,'extras/TDBINTO_DISABLED.MP4'))
 	ECHO_INTRO_ENABLE  = xbmc.translatePath(os.path.join(SKIN_DIR,'extras/ECHOINTRO.MP4'))
	ECHO_INTRO_DISABLE = xbmc.translatePath(os.path.join(SKIN_DIR,'extras/ECHOINTRO_DISABLED.MP4'))
	PLAYER_CORE   = xbmc.translatePath('special://userdata/playercorefactory.xml')

	#Common.addItem('[B][COLOR ghostwhite]SPORTS DEVIL FIX[/COLOR][/B]',BASEURL,146,EXTRAS_ICON,FANART,'')

	if os.path.exists(GUIDE):
		Common.addItem('[B][COLOR ghostwhite]REMOVE ALL TV GUIDE SETTINGS[/COLOR][/B]',BASEURL,158,EXTRAS_ICON,FANART,'')

	if os.path.isfile(INTRO_ENABLE) or os.path.isfile(INTRO_DISABLE):
 		if os.path.isfile(INTRO_ENABLE):
 			INTRO_VID = "[COLOR yellowgreen][B]ENABLED[/COLOR][/B]"
			match = 1
 		else:
 			INTRO_VID = "[COLOR lightskyblue][B]DISABLED[/COLOR][/B]"
			match = 1

	if match == 0:
		if os.path.isfile(ECHO_INTRO_ENABLE) or os.path.isfile(ECHO_INTRO_DISABLE):
			if os.path.isfile(INTRO_ENABLE):
				INTRO_VID = "[COLOR yellowgreen][B]ENABLED[/COLOR][/B]"
			else:
				INTRO_VID = "[COLOR lightskyblue][B]DISABLED[/COLOR][/B]"
		else:
			INTRO_VID = "[COLOR ghostwhite][B]NOT APPLICABLE[/COLOR][/B]"

 	if os.path.isfile(PLAYER_CORE):
 		PLAYER_CORE_EN_DIS = "[COLOR yellowgreen][B]ENABLED[/COLOR][/B]"
 	else:
 		PLAYER_CORE_EN_DIS = "[COLOR lightskyblue][B]DISABLED[/COLOR][/B]"

 	if not "NOT APPLICABLE" in INTRO_VID:
		Common.addItem('[B][COLOR ghostwhite]HORUS / HORUS XXL INTRO VIDEO - [/COLOR][/B]' + INTRO_VID,BASEURL,75,EXTRAS_ICON,FANART,'')
	if xbmc.getCondVisibility('system.platform.android'):
		Common.addItem('[B][COLOR ghostwhite]PLAYERCOREFACTORY.XML - [/COLOR][/B]' + PLAYER_CORE_EN_DIS,'url',110,EXTRAS_ICON,FANART,'')
	if xbmc.getCondVisibility('system.platform.windows'):
		Common.addItem('[B][COLOR ghostwhite]PLAYERCOREFACTORY.XML - [/COLOR][/B]' + PLAYER_CORE_EN_DIS,'url',115,EXTRAS_ICON,FANART,'')

	Common.addItem('[B][COLOR ghostwhite]RUYA EMPTY LIST FIX[/COLOR][/B]','url',109,EXTRAS_ICON,FANART,'')

	if os.path.exists(YOUTUBE_INSTALL):
		Common.addItem('[B][COLOR ghostwhite]YOUTUBE FIX (EXCEEDED DAILY LIMIT)[/COLOR][/B]','url',132,EXTRAS_ICON,FANART,'')

#######################################################################
#				ENABLE/DISABLE THE INTRO VIDEO FOR HORUS
#######################################################################

def HORUS_INTRO():


	INTRO_ENABLE = xbmc.translatePath(os.path.join(SKIN_DIR,'extras/TDBINTRO.MP4'))
	INTRO_DISABLE = xbmc.translatePath(os.path.join(SKIN_DIR,'extras/TDBINTRO.MP4'))
 	ECHO_INTRO_ENABLE  = xbmc.translatePath(os.path.join(SKIN_DIR,'extras/ECHOINTRO.MP4'))
	ECHO_INTRO_DISABLE = xbmc.translatePath(os.path.join(SKIN_DIR,'extras/ECHOINTRO_DISABLED.MP4'))

	if os.path.exists(INTRO_ENABLE) or os.path.exists(INTRO_DISABLE):
		if os.path.exists(INTRO_ENABLE):
			try:
				os.rename(INTRO_ENABLE, INTRO_DISABLE)
			except: pass
		else:
			try:
				os.rename(INTRO_DISABLE, INTRO_ENABLE)
			except: pass

	if os.path.exists(ECHO_INTRO_ENABLE) or os.path.exists(ECHO_INTRO_DISABLE):
		if os.path.exists(ECHO_INTRO_ENABLE):
			try:
				os.rename(ECHO_INTRO_ENABLE, ECHO_INTRO_DISABLE)
			except: pass
		else:
			try:
				os.rename(ECHO_INTRO_DISABLE, ECHO_INTRO_ENABLE)
			except: pass

	xbmc.executebuiltin("Container.Refresh")

#######################################################################
#				PLAYER CORE FUNCTIONS
#######################################################################

def PLAYERCORE_ANDROID():

	pass_me = 0
	if os.path.isfile(PLAYER_CORE):
		pass_me = 1
		try:
			os.remove(PLAYER_CORE)
		except: pass

	if pass_me == 0:
		name = "[COLOR white][B]playercorefactory.xml[/B][/COLOR]"
		url = BASEURL + base64.b64decode(b'a29kaS9wbGF5ZXJjb3JlZmFjdG9yeS9hbmRyb2lkLnppcA==')
		description = "NULL"
		#Check is the packages folder exists, if not create it.
		path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
		if not os.path.exists(path):
			os.makedirs(path)
		buildname = name
		dp = xbmcgui.DialogProgress()
		dp.create(ADDONTITLE,"Downaloading the playercorefactory.xml file for","the Android OS, Please Wait......")
		buildname = "build"
		lib=os.path.join(path, buildname+'.zip')
	
		try:
			os.remove(lib)
		except:
			pass

		dialog = xbmcgui.Dialog()
		downloader.download(url, lib, dp)
		addonfolder = xbmc.translatePath(os.path.join('special://home','userdata'))
		time.sleep(2)
		dp.update(0,"","Extracting Zip Please Wait","")
		installer.unzip(lib,addonfolder,dp)
		time.sleep(1)
		try:
			os.remove(lib)
		except:
			pass

		dialog.ok(ADDONTITLE, "[COLOR white]playercorefactory.xml installed![/COLOR]",'',"[COLOR white]Thank you for using No Limits Tools![/COLOR]")

	xbmc.executebuiltin("Container.Refresh")

def PLAYERCORE_WINDOWS():

	pass_me = 0
	if os.path.isfile(PLAYER_CORE):
		pass_me = 1
		try:
			os.remove(PLAYER_CORE)
		except: pass

	if pass_me == 0:
		name = "[COLOR white][B]playercorefactory.xml[/B][/COLOR]"
		url = BASEURL + base64.b64decode(b'a29kaS9wbGF5ZXJjb3JlZmFjdG9yeS93aW5kb3dzLnppcA==')
		description = "NULL"
		#Check is the packages folder exists, if not create it.
		path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
		if not os.path.exists(path):
			os.makedirs(path)
		buildname = name
		dp = xbmcgui.DialogProgress()
		dp.create(ADDONTITLE,"Downaloading the playercorefactory.xml file for","the Windows OS. Please Wait......")
		buildname = "build"
		lib=os.path.join(path, buildname+'.zip')
	
		try:
			os.remove(lib)
		except:
			pass

		dialog = xbmcgui.Dialog()
		downloader.download(url, lib, dp)
		addonfolder = xbmc.translatePath(os.path.join('special://home','userdata'))
		time.sleep(2)
		dp.update(0,"","Extracting Zip Please Wait","")
		installer.unzip(lib,addonfolder,dp)
		time.sleep(1)
		try:
			os.remove(lib)
		except:
			pass

		dialog.ok(ADDONTITLE, "[COLOR white]playercorefactory.xml installed![/COLOR]",'',"[COLOR white]Thank you for using No Limits Tools![/COLOR]")

	xbmc.executebuiltin("Container.Refresh")

def YOUTUBE_REMOVE():

	dialog = xbmcgui.Dialog()
	
	if os.path.exists(YOUTUBE_DATA):
		try:
			shutil.rmtree(YOUTUBE_DATA)
		except:
			dialog.ok(ADDONTITLE,"[COLOR white]There was an error removing the YouTube addon data folder. Thank you for using No Limits Tools[/COLOR]")
			quit()
	try:
		YOUTUBE_FOLDER              =  xbmc.translatePath('special://home/userdata/addon_data/plugin.video.youtube')
		os.makedirs(YOUTUBE_FOLDER)
		DEFAULT_YOUTUBE_SETTINGS    =  xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID,'resources/files/youtube_settings.xml'))
		YOUTUBE_SETTINGS            =  xbmc.translatePath('special://home/userdata/addon_data/plugin.video.youtube/settings.xml')
		shutil.copyfile(DEFAULT_YOUTUBE_SETTINGS, YOUTUBE_SETTINGS)
	except:
		dialog.ok(ADDONTITLE,"[COLOR white]There was an error creating the YouTube addon data settings. Thank you for using No Limits Tools[/COLOR]")
		quit()
	dialog.ok(ADDONTITLE,"[COLOR white]The YouTube plugin should now be fixed and working correctly. Thank you for using No Limits Tools[/COLOR]")
		
def SPORTS_DEVIL_FIX():

	SPORTS_DEVIL_FOLDER = xbmc.translatePath(os.path.join('special://home/addons','plugin.video.SportsDevil'))
	PYDEV_FOLDER = xbmc.translatePath(os.path.join('special://home/addons','script.module.pydevd'))
	REPO_FOLDER = xbmc.translatePath(os.path.join('special://home/addons','repository.echo'))
	path = xbmc.translatePath(os.path.join('special://home/addons','packages'))

	choice = xbmcgui.Dialog().yesno(ADDONTITLE,'This option will remove all traces of Sports Devil (If Installed) and install a clean version along with the ECHO Repo.','Would you like to continue?',yeslabel='[B][COLOR yellowgreen]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
	if choice == 0:
		sys.exit(1)
	dialog = xbmcgui.Dialog()
	if os.path.exists(SPORTS_DEVIL_FOLDER):
		try:
			shutil.rmtree(SPORTS_DEVIL_FOLDER)
		except: pass
	if os.path.exists(PYDEV_FOLDER):
		try:
			shutil.rmtree(PYDEV_FOLDER)
		except: pass
	purgePath = xbmc.translatePath('special://home/addons/packages')
	for root, dirs, files in os.walk(purgePath):
		file_count = 0
		file_count += len(files)
	for root, dirs, files in os.walk(purgePath):
		file_count = 0
		file_count += len(files)
		if file_count > 0:            
			for f in files:
				os.unlink(os.path.join(root, f))
			for d in dirs:
				shutil.rmtree(os.path.join(root, d))
	
	if not os.path.exists(path):
		os.makedirs(path)

	url = ('http://www.echocoder.com/addons/Plugins/dependencies/script.module.pydevd-4.4.0.zip')
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"","","Installing Dependencies")
	lib=os.path.join(path, 'addon.zip')
		
	try:
		os.remove(lib)
	except:
		pass

	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait","")
	extract.all(lib,addonfolder,dp)
	url = ('http://www.echocoder.com/addons/Plugins/plugin.video.SportsDevil.zip')
	dp = xbmcgui.DialogProgress()
	dp.create(ADDONTITLE,"","","Installing Sports Devil")
	lib=os.path.join(path, 'addon.zip')
		
	try:
		os.remove(lib)
	except:
		pass

	downloader.download(url, lib, dp)
	addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
	time.sleep(2)
	dp.update(0,"","Extracting Zip Please Wait","")
	extract.all(lib,addonfolder,dp)
	try:
		os.remove(lib)
	except:
		pass
	xbmc.executebuiltin("UpdateAddonRepos")
	xbmc.executebuiltin("UpdateLocalAddons")	

	dialog.ok(ADDONTITLE,"[COLOR white]The Sports Devil plugin should now be fixed and working correctly. If you have any issues please turn AUTO UPDATE OFF on Sports Devil and run this fix again.[/COLOR]")
	quit()

def REMOVE_GUIDE():

	if os.path.exists(GUIDE):
		try:
			shutil.rmtree(GUIDE)
			os.rmdir(GUIDE)
		except: pass
	choice = xbmcgui.Dialog().yesno(ADDONTITLE,'[COLOR white]All traces of the ECHO TV Guide settings have been removed. Would you like to launch the guide now?[/COLOR]',yeslabel='[B][COLOR yellowgreen]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
	if choice == 1:
		RUN = "RunAddon(plugin.program.echotvguide)"
		xbmc.executebuiltin(RUN)
	else:
		xbmc.executebuiltin("Container.Refresh")