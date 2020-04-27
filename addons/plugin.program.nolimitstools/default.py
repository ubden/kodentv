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
#			GET ALL DEPENDANCIES NEEDED
#######################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
from urllib import FancyURLopener
from HTMLParser import HTMLParser
import platform
import shutil
import urllib2,urllib
import re
import glob
import time
import errno
import socket
import json
import fnmatch

#######################################################################
#		        REQUIRES script.module.requests AS A DEPENDANCY.
#######################################################################

import requests

#######################################################################
#			LOCAL .PY DEPENDANCIES
#######################################################################
from resources.lib.modules import get_addons
from resources.lib.modules import uploadlog
#from resources.lib.modules import runner
from resources.lib.modules import community
from resources.lib.modules import installer
from resources.lib.modules import update
from resources.lib.modules import parameters
from resources.lib.modules import maintenance
from resources.lib.modules import plugintools
from resources.lib.modules import backuprestore
from resources.lib.modules import speedtest
from resources.lib.modules import common as Common
from resources.lib.modules import wipe
from resources.lib.modules import versioncheck
from resources.lib.modules import extras
from resources.lib.modules import security
from resources.lib.modules import cache_dir
from resources.lib.modules import web
from resources.lib.modules import debridit
from resources.lib.modules import traktit
from resources.lib.modules import notify
from resources.lib.modules import wizard as wiz

#######################################################################
#			VERIABLES NEEDED
#######################################################################

ADDONTITLE          =  "[COLOR aqua]KodenTV[/COLOR] [COLOR white]Tools[/COLOR]"
ADDON_ID            =  xbmcaddon.Addon().getAddonInfo('id') #'plugin.program.nolimitstools'
ADDON               =  xbmcaddon.Addon(id=ADDON_ID)
ADDONDATA           =  xbmc.translatePath('special://userdata/addon_data')
#ADDOND              =  xbmc.translatePath('special://userdata/addon_data')
HOME                =  xbmc.translatePath('special://home/')
ADDONS              =  xbmc.translatePath('special://home/addons')
PACKAGES            =  xbmc.translatePath('special://home/addons/packages')
USERDATA            =  xbmc.translatePath('special://home/userdata')
THUMBS              =  xbmc.translatePath('special://home/userdata/Thumbnails')
CHANGELOG           =  xbmc.translatePath('special://home/addons/' + ADDON_ID + '/changelog.txt')
WIZARD_VERSION      =  xbmc.translatePath('special://home/addons/' + ADDON_ID + '/version.txt')
RESOURCES           =  xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources')
NOTICE              =  xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/NOTICE.txt')
GET_VERSION         =  xbmc.translatePath('special://home/addons/' + ADDON_ID + '/addon.xml')
DEFAULT_SETTINGS    =  xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/files/settings_default.xml')
ADDON_DATA          =  xbmc.translatePath('special://userdata/addon_data/' + ADDON_ID)
NOLIMITS_SETTINGS   =  xbmc.translatePath('special://userdata/addon_data/' + ADDON_ID + '/settings.xml')
TEMP_FOLDER         =  xbmc.translatePath('special://userdata/addon_data/' + ADDON_ID + '/temp')
TEMP_FILE           =  xbmc.translatePath('special://userdata/addon_data/' + ADDON_ID + '/temp/temp.xml')
TEMP_ADDONS         =  xbmc.translatePath('special://userdata/addon_data/' + ADDON_ID + '/temp/temp_installer.xml')
KODIAPPS_FILE       =  xbmc.translatePath('special://userdata/addon_data/' + ADDON_ID + '/temp/kodiapps.xml')
COMMUNITY_BUILD	    =  xbmc.translatePath('special://userdata/community_build.txt')
COMMUNITY_OTA	    =  xbmc.translatePath('special://userdata/nolimits_community_ota.txt')
KEYBOARD_FILE       =  xbmc.translatePath('special://userdata/keymaps/keyboard.xml')
ADVANCED_SET_FILE   =  xbmc.translatePath('special://userdata/advancedsettings.xml')
WIZLOG              =  xbmc.translatePath('special://userdata/addon_data/' + ADDON_ID + '/wizard.log')
YTDATA	 	    =  xbmc.translatePath('special://userdata/addon_data/plugin.video.youtube/')
CONTACT             =  'Follow Us At... \n \n \nYouTube.com/kodentv \n \nSnapchat.com/add/kodentv \n \nPaypal.me/kodentv '

DIALOG              =  xbmcgui.Dialog()
dialog              =  xbmcgui.Dialog()
dp                  =  xbmcgui.DialogProgress()
skin                =  xbmc.getSkinDir()
string              =  ""
THE_TIME 	    =  time.strftime("%H:%M %p")
THE_DATE 	    =  time.strftime("%A %B %d %Y")
DEFAULT_HEADERS     =  [["User-Agent","nolimits-tools"]]
COLOR1              = 'magenta'
COLOR2              = 'cyan'
THEME1              = '[COLOR '+COLOR1+'][I][B]([COLOR '+COLOR2+']KodenTV[/COLOR])[/B][/I][/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
THEME2              = '[COLOR '+COLOR2+']%s[/COLOR]'
THEME3              = '[COLOR '+COLOR1+']%s[/COLOR]'
EXCLUDES            = [ADDON_ID]
DEFAULTPLUGINS      = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv', 'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org', 'metadata.tvdb.com', 'service.xbmc.versioncheck']
HIDESPACERS         = 'No'

TRAKTSAVE        = wiz.getS('traktlastsave')
REALSAVE         = wiz.getS('debridlastsave')
KEEPTRAKT        = wiz.getS('keeptrakt')
KEEPREAL         = wiz.getS('keepdebrid')
TRAKTID          = traktit.TRAKTID
DEBRIDID         = debridit.DEBRIDID

#######################################################################
#			ADDON SETTINGS
#######################################################################

check               = plugintools.get_setting("checkupdates")
check_addon         = plugintools.get_setting("checkaddonupdates")
auto                = plugintools.get_setting("autoupdates")

#######################################################################
#			URLS NEEDED
#######################################################################

BASEURL             = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')# http://echocoder.com/
#AdvancedSettings    = BASEURL + base64.b64decode(b'YWR2YW5jZWRzZXR0aW5ncy93aXphcmRfcmVsLnR4dA==')# advancedsettings/wizard_rel.txt
BASEURL2            = base64.b64decode(b'aHR0cDovL25vbGltaXRzYnVpbGRzLmNvbS8=')
AdvancedSettings    = BASEURL2 + 'advancedsettings/advancedsettingslist.txt'
SpeedTest           = BASEURL + base64.b64decode(b'c3BlZWR0ZXN0L3NwZWVkdGVzdC50eHQ=')
KeymapsURL          = BASEURL + base64.b64decode(b'a2V5bWFwcy93aXphcmRfcmVsLnR4dA==')
APKS                = BASEURL + base64.b64decode(b'a29kaS9hcGtzL2Fwa2xpc3QudHh0')
APKS_INSTALLER      = BASEURL + base64.b64decode(b'YWRkb25zL2Fwa3MudHh0')
AND_APKS            = BASEURL + base64.b64decode(b'YW5kcm9pZC9hcGtzL2xpc3QudHh0')
WINDOWS             = BASEURL + base64.b64decode(b'a29kaS93aW5kb3dzL2xpc3QudHh0')
OSX                 = BASEURL + base64.b64decode(b'a29kaS9vc3gvbGlzdC50eHQ=')
IOS                 = BASEURL + base64.b64decode(b'a29kaS9pb3MvbGlzdC50eHQ=')
APKSLIB             = BASEURL + base64.b64decode(b'YXBrcy9hcGtsaWJsaXN0LnR4dA==')
LIB                 = BASEURL + base64.b64decode(b'bGliL2xpYmxpc3QudHh0')
TOOLS               = BASEURL + base64.b64decode(b'a29kaS90b29scy9saXN0LnR4dA==')
CONTACTS            = BASEURL + base64.b64decode(b'b3RoZXIvY29udGFjdGxpc3QudHh0')
SUPPORT             = BASEURL + base64.b64decode(b'b3RoZXIvc3VwcG9ydC50eHQ=')
CREDITS             = BASEURL + base64.b64decode(b'Y3JlZGl0cy93aXphcmQudHh0')
NEWS                = BASEURL + base64.b64decode(b'b3RoZXIvbmV3cy50eHQ=')
SERVER_CHECKER      = BASEURL + base64.b64decode(b'ZG93bi50eHQ=')
SERVER_CHECK        = BASEURL + base64.b64decode(b'Y2hlY2tlci50eHQ=')
ADD_COMMUNITY       = BASEURL + base64.b64decode(b'b3RoZXIvYWRkX2NvbW11bml0eS50eHQ=')
ADDONS_API          = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1hZGRvbnMmYWN0aW9uPWNvdW50')
ECHO_API            = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1idWlsZHMmYWN0aW9uPWNvdW50')
ECHO_CHANNEL        = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20veW91dHViZS95b3V0dWJlLnBocD9pZD1VQ29ZVkVRd3psU3VFLU4yQ3VLdlFKNHc=')
NOLIMITS_BUILDS     = BASEURL + base64.b64decode(b'YnVpbGRzL3dpemFyZC54bWw=') + '|SPLIT|aqua'
NOLIMITS_BLUE_BUILDS= BASEURL + base64.b64decode(b'YnVpbGRzL2VjaG9fYmx1ZS93aXphcmQueG1s') + '|SPLIT|dodgerblue'
youtubelink         = base64.b64decode(b'cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9')
FANRIFFIC_URL_NEW   = base64.b64decode(b'aHR0cDovL2ZhbnJpZmZpYy5jb20vd2l6d2l6L3Bob29leXRoZW1lcy50eHQ=')
FANRIFFIC_URL_OLD   = base64.b64decode(b'aHR0cDovL2ZhbnJpZmZpYy5jb20vd2l6d2l6L3Bob29leXRoZW1lc29sZC50eHQ=')
FANRIFFIC_KRYPTON   = base64.b64decode(b'aHR0cDovL2ZhbnJpZmZpYy5jb20vd2l6d2l6L2tyeXB0b250aGVtZXMudHh0')
KODIAPPS_FANART     = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20vaW1hZ2VzL2FkZG9ucy9wbHVnaW4udmlkZW8uZXRoZXJlYWx0di9mYW5hcnQuanBn')
KODIAPPS_API        = base64.b64decode(b'aHR0cDovL2tvZGlhcHBzLmNvbS9lY2hvcy54bWw=')

#######################################################################
#			KodenTV Tools ICONS
#######################################################################

FANART              = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/fanart.jpg')
ICON                = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
DIVIDER_ICON        = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/icondivider.png')
ART                 = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/')
NOLIMITSICON        = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
WIZARDICON          = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
ADVANCED_SET_ICON   = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
APK_ICON            = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
BACKUP_ICON         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/backup-icon.jpg')
COMMUNITY_ICON      = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
SETTINGS_ICON       = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/settings-icon.png')
SPEEDTEST_ICON      = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
SPMC_ICON           = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
SUPPORT_ICON        = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
SYSTEM_INFO_ICON    = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
TMP_ICON            = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
TOOLS_ICON          = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/tools-icon.png')
VIP_ICON            = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
LIB_ICON            = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
YOUTUBE_ICON        = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
VIEWER_ICON         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/viewer-icon.png')
GUEST_ICON          = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
SERVER_ICON         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
BUILD_ICON          = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
KODI_ICON           = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
KODI_FANART         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
SPMC_ICON           = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
SPMC_FANART         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
UPDATE_ICON         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/update-icon.jpg')
EXTRAS_ICON         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
SPORTS_ICON         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
ERROR_ICON          = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/error-icon.png')
STATS_ICON          = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
TWITTER_ICON        = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
KEYMAPS_ICON        = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')
PASSWORD_ICON       = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/password-icon.png')
DELETE_ICON         = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/delete-icon.png')
RESET_ICON          = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/reset-icon.png')
DIAGNOSE_ICON       = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/diagnose-icon.jpg')
KODIAPPS_ICON       = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/art/kodiapps-icon.jpg')


#######################################################################
#			KodenTV VERSION CHECKERS
#######################################################################

NOLIMITS_VERSION        =  os.path.join(USERDATA,'nolimits_build.txt')

#######################################################################
#			CUSTOM HEADER FOR SECURITY
#######################################################################

class MyOpener(FancyURLopener):
	version = base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl')

#######################################################################
#			REDIRECT URLLIB COMMANDS TO MYOPENER
#######################################################################

myopener = MyOpener()
urlopen = MyOpener().open

#######################################################################
#			CREATE SETTINGS XML IF IT DOES NOT EXIST
#######################################################################

if not os.path.isfile(NOLIMITS_SETTINGS):
	if not os.path.exists(ADDON_DATA):
		os.makedirs(ADDON_DATA)
	shutil.copyfile(DEFAULT_SETTINGS, NOLIMITS_SETTINGS)

#######################################################################
#			CREATE PATH FOR BACKUPS
#######################################################################

backuprestore.check_path()

#######################################################################
#			CHECK FOR NOTICE
#######################################################################

if os.path.isfile(NOTICE):
	f = open(NOTICE,mode='r'); msg = f.read(); f.close()
	Common.TextBoxesPlain("%s" % msg)
	os.remove(NOTICE)

#######################################################################
#			KodenTV Tools ROOT MENU
#######################################################################

def INDEX():


	#######################################################################
	#		GET API INFORMATION
	#######################################################################

	api_interval = plugintools.get_setting("api_interval")

	if api_interval == "0":
		mark = "60"
	elif api_interval == "1":
		mark = "50"
	elif api_interval == "2":
		mark = "40"
	elif api_interval == "3":
		mark = "30"
	elif api_interval == "4":
		mark = "20"
	elif api_interval == "5":
		mark = "10"
	elif api_interval == "6":
		mark = "5"
	else: mark = "60"

	#######################################################################
	#	        VARIABLES NEEDED IN THE LIST MENU
	#######################################################################

	pleasecheck 	= 0
	BUILD_CHECK_ERROR   = 0
	CURRENT_BUILD = "[COLOR aqua]ERROR[/COLOR]"
	CURRENT_VERSION_CODE = "[COLOR aqua]ERROR[/COLOR]"
	LATEST_VERSION = "[COLOR aqua]ERROR[/COLOR]"

	#######################################################################
	#		FIND KodenTV TOOLS VERSION
	#######################################################################
	
	a=open(GET_VERSION).read()
	b=a.replace('\n',' ').replace('\r',' ')
	match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
	for item in match:
		addon_version = item
	
	#######################################################################
	#		FIND BUILD INFORMATION
	#######################################################################

	try:
		U_A = 'TheWizardIsHere'
		if os.path.exists(NOLIMITS_VERSION):
			VERSIONCHECK = NOLIMITS_VERSION
			FIND_URL = BASEURL + base64.b64decode(b'YnVpbGRzL3VwZGF0ZV93aXoudHh0')
			checkurl = BASEURL + base64.b64decode(b'YnVpbGRzL3ZlcnNpb25fY2hlY2sudHh0')
			pleasecheck = 1
		if os.path.exists(COMMUNITY_OTA):
			VERSIONCHECK = COMMUNITY_OTA
			a=open(VERSIONCHECK).read()
			FIND_URL = re.compile('<update_url>(.+?)</update_url>').findall(a)[0]
			checkurl = re.compile('<version_check>(.+?)</version_check>').findall(a)[0]
			try:
				U_A = re.compile('<user_agent>(.+?)</user_agent>').findall(a)[0]
			except: pass
			pleasecheck = 1
	except:
		pass

	#######################################################################
	#		CHECK FOR BUILD UPDATES
	#######################################################################

	try:
		if pleasecheck == 1:
			a=open(VERSIONCHECK).read()
			CURRENT_BUILD = re.compile('<build>(.+?)</build>').findall(a)[0]
			CURRENT_VERSION = re.compile('<version>(.+?)</version>').findall(a)[0]
			req = urllib2.Request(checkurl)
			req.add_header('User-Agent',U_A)
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			match = re.compile('<build>'+CURRENT_BUILD+'</build><version>(.+?)</version><fresh>(.+?)</fresh>').findall(link)
			for newversion,fresh in match:
				LATEST_VERSION = newversion
				if CURRENT_VERSION < LATEST_VERSION:
					CURRENT_VERSION_CODE = '[COLOR aqua]' + CURRENT_VERSION + '[/COLOR]'
				else:
					CURRENT_VERSION_CODE = '[COLOR aqua]' + CURRENT_VERSION + '[/COLOR]'
	except:
		CURRENT_BUILD = "[COLOR aqua]ERROR[/COLOR]"
		CURRENT_VERSION_CODE = "[COLOR aqua]ERROR[/COLOR]"
		LATEST_VERSION = "[COLOR aqua]ERROR[/COLOR]"

	#######################################################################
	#		MAIN MENU
	#######################################################################

	kodi_name = Common.GET_KODI_VERSION()
	kodi_details = Common.GET_KODI_VERSION_DETAILS()

	startup_clean = plugintools.get_setting("acstartup")
	weekly_clean = plugintools.get_setting("clearday")
	sizecheck_clean = plugintools.get_setting("startupsize")

	if startup_clean == "false":
		startup_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		startup_onoff = "[COLOR aqua][B]ON[/COLOR][/B]"
	if weekly_clean == "0":
		weekly_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		weekly_onoff = "[COLOR aqua][B]ON[/COLOR][/B]"
	if sizecheck_clean == "false":
		sizecheck_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		sizecheck_onoff = "[COLOR aqua][B]ON[/COLOR][/B]"
	
	#if pleasecheck == 1:
	#	Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	#	Common.addItem("[COLOR white]KodenTV Tools Version:[/COLOR] [COLOR aqua]" + str(nolimits_ver) + "[/COLOR]",'url',999,ICON,FANART,'')
	#	Common.addItem('[COLOR ghostwhite]CURRENT BUILD: [/COLOR][COLOR aqua]' + CURRENT_BUILD + '[/COLOR]',BASEURL,4,BUILD_ICON,FANART,'')
	#	Common.addItem('[COLOR ghostwhite]YOUR VERSION: [/COLOR]' + CURRENT_VERSION_CODE + '',BASEURL,4,BUILD_ICON,FANART,'')
	#	Common.addItem('[COLOR ghostwhite]LATEST VERSION: [/COLOR][COLOR aqua]' + LATEST_VERSION + '[/COLOR]',BASEURL,4,BUILD_ICON,FANART,'')
	#	try:
	#		if LATEST_VERSION > CURRENT_VERSION:
	#			if "ERROR" not in CURRENT_VERSION_CODE:
	#				Common.addItem('[COLOR ghostwhite]CLICK TO UPDATE ' + CURRENT_BUILD.upper() + ' NOW![/COLOR]',BASEURL,33,UPDATE_ICON,FANART,'')
	#		else:
	#			Common.addItem('[COLOR aqua]' + CURRENT_BUILD.upper() + ' IS UP TO DATE![/COLOR]',BASEURL,4,UPDATE_ICON,FANART,'')
	#	except:
	#		Common.addItem('[COLOR ghostwhite]ERROR RETRIEVING INFORMATION[/COLOR]',BASEURL,4,UPDATE_ICON,FANART,'')
	Common.addItem("[COLOR white]KODI VERSION[/COLOR] [COLOR aqua]" + str(kodi_details) + "[/COLOR]",'url',79,ICON,FANART,'')
	Common.addItem("[COLOR white]KodenTV TOOLS VERSION[/COLOR] [COLOR aqua]" + str(addon_version) + "[/COLOR]",'url',79,ICON,FANART,'')
	Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]RUN THE KodenTV SECURITY CHECK[/COLOR]',BASEURL,181,TOOLS_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]SOURCE AND REPOSITORY STATUS CHECKER[/COLOR]',BASEURL,184,KODIAPPS_ICON,KODIAPPS_FANART,'Information brought to you by kodiapps.com')
	Common.addDir('[COLOR ghostwhite]MAINTENANCE TOOLS[/COLOR]',BASEURL,5,TOOLS_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite]BACKUP [COLOR white]/[/COLOR] RESTORE[/COLOR]',BASEURL,8,BACKUP_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]DEBRID MENU [/COLOR]',BASEURL,202,BACKUP_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]TRAKT MENU [/COLOR]',BASEURL,201,BACKUP_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite]BUFFERING FIX (AdvancedSettings.XML)[/COLOR]',BASEURL,30,SETTINGS_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]SPEED TEST[/COLOR]',BASEURL,16,SPEEDTEST_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]EXTRAS - FIXES, TWEAKS ETC[/COLOR]',BASEURL,74,EXTRAS_ICON,FANART,'')	
	Common.addItem('[COLOR ghostwhite]VIEW LAST ERROR IN LOG FILE[/COLOR]',BASEURL,154,ERROR_ICON,FANART,'')
	Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addDir('[COLOR ghostwhite]KODIAPPS ADDON CHART[/COLOR]',BASEURL,185,KODIAPPS_ICON,KODIAPPS_FANART,'')
	#Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]CUSTOM KEYMAPS[/COLOR]',BASEURL,129,KEYMAPS_ICON,FANART,'')	
	#Common.addDir('[COLOR ghostwhite]ANDROID APKS[/COLOR]',BASEURL,149,TOOLS_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]MUST HAVE KODI PROGRAMS & TOOLS[/COLOR]',BASEURL,46,TOOLS_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]KODI/SPMC INSTALLATION FILES[/COLOR]',BASEURL,28,APK_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]KODI/SPMC LIBRTMP FILES[/COLOR]',BASEURL,29,LIB_ICON,FANART,'')
	#Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]THE DAYS SPORT LISTINGS[/COLOR]',BASEURL,47,SPORTS_ICON,FANART,'')
	#Common.addDir('[COLOR ghostwhite]SYSTEM INFORMATION[/COLOR]',BASEURL,163,VIEWER_ICON,FANART,'')
	Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]CLEAR DOWNLOAD COUNTERS[/COLOR]',BASEURL,180,SETTINGS_ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]LATEST NEWS[/COLOR]',BASEURL,106,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]CONTACT: [COLOR aqua]Kodi KodenTV[/COLOR][/COLOR]',BASEURL,190,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]DONATIONS: [COLOR aqua]donorbox.org/kodentv[/COLOR][/COLOR]',BASEURL,208,ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]DONATIONS: [COLOR aqua]paypal.me/kodentv[/COLOR][/COLOR]',BASEURL,206,ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]DONATIONS: [COLOR aqua]patreon.com/kodentv[/COLOR][/COLOR]',BASEURL,207,ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]TWITTER: [/COLOR][COLOR aqua]@kodentv[/COLOR]',BASEURL,4,BUILD_ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]HOW TO GET SUPPORT[/COLOR]',BASEURL,79,SUPPORT_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]VIEW CHANGELOG[/COLOR]',BASEURL,80,VIEWER_ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]VIEW KodenTV Tools CREDITS[/COLOR]',BASEURL,81,SETTINGS_ICON,FANART,'')
	Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]KodenTV TOOLS SETTINGS[/COLOR]',BASEURL,9,SETTINGS_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]AUTO CLEAN ON KODI LAUNCH - [/COLOR]' + startup_onoff,BASEURL,112,SETTINGS_ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]WEEKLY AUTO CLEAN - [/COLOR]' + weekly_onoff,BASEURL,113,SETTINGS_ICON,FANART,'')
	#Common.addItem('[COLOR ghostwhite]SETUP AUTO CLEAN AT SPECIFIC MB - [/COLOR]' + sizecheck_onoff,BASEURL,9,SETTINGS_ICON,FANART,'')

	kodi_name = Common.GET_KODI_VERSION()

	if kodi_name == "Jarvis":
		xbmc.executebuiltin("Container.SetViewMode(50)")
	elif kodi_name == "Krypton":
		xbmc.executebuiltin("Container.SetViewMode(55)")
	else: xbmc.executebuiltin("Container.SetViewMode(50)")

#######################################################################
#			MAINTENANCE MENU
#######################################################################

def MAINTENANCE_MENU():
	check_folders = plugintools.get_setting("maint_check_folders")
	check_log     = plugintools.get_setting("maint_check_log")

	HOME          =  xbmc.translatePath('special://home/')
	PACKAGES      =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
	#THUMBS       =  xbmc.translatePath(os.path.join('special://profile/userdata','Thumbnails'))
	THUMBS        =  xbmc.translatePath(os.path.join('special://userdata','Thumbnails'))
	CACHE_FOLDER  =  xbmc.translatePath(os.path.join('special://home','cache'))
	TEMP_FOLDER   =  xbmc.translatePath(os.path.join('special://','temp'))
	CACHE         =  "NULL"

	if check_folders == "true":
		if os.path.exists(CACHE_FOLDER):
			CACHE = CACHE_FOLDER

		if os.path.exists(TEMP_FOLDER):
			CACHE = TEMP_FOLDER

		if not os.path.exists(PACKAGES):
			os.makedirs(PACKAGES)

		if CACHE == "NULL":
			try:
				PACKAGES_SIZE_BYTE = maintenance.get_size(PACKAGES)
				THUMB_SIZE_BYTE    = maintenance.get_size(THUMBS)
			except: pass
		else:
			try:
				CACHE_SIZE_BYTE    = maintenance.get_size(CACHE)
				PACKAGES_SIZE_BYTE = maintenance.get_size(PACKAGES)
				THUMB_SIZE_BYTE    = maintenance.get_size(THUMBS)
			except: pass
		
		if CACHE == "NULL":
			try:
				PACKAGES_SIZE = maintenance.convertSize(PACKAGES_SIZE_BYTE)
				THUMB_SIZE    = maintenance.convertSize(THUMB_SIZE_BYTE)
			except: pass
		else:
			try:
				CACHE_SIZE    = maintenance.convertSize(CACHE_SIZE_BYTE)
				PACKAGES_SIZE = maintenance.convertSize(PACKAGES_SIZE_BYTE)
				THUMB_SIZE    = maintenance.convertSize(THUMB_SIZE_BYTE)
			except: pass
		
		if CACHE == "NULL":
			CACHE_SIZE    =  "[COLOR red][B]ERROR READING CACHE[/B][/COLOR]"

	startup_clean = plugintools.get_setting("acstartup")
	weekly_clean = plugintools.get_setting("clearday")
	sizecheck_clean = plugintools.get_setting("startupsize")

	if startup_clean == "false":
		startup_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		startup_onoff = "[COLOR aqua][B]ON[/COLOR][/B]"
	if weekly_clean == "0":
		weekly_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		weekly_onoff = "[COLOR aqua][B]ON[/COLOR][/B]"
	if sizecheck_clean == "false":
		sizecheck_onoff = "[COLOR red][B]OFF[/COLOR][/B]"
	else:
		sizecheck_onoff = "[COLOR aqua][B]ON[/COLOR][/B]"

	if check_log == "true":

		curr = maintenance.grab_Log(True, False)
		old = maintenance.grab_Log(True, True)
		errors1 = []; errors2 = []
		if not curr == False: errors1 = maintenance.errorList(curr)
		if not old == False: errors2 = maintenance.errorList(old)
		i = len(errors1) + len(errors2)

		if i == 0:
			ERRORS_IN_LOG = "[COLOR aqua]0 Errors Found in Log[/COLOR]"
		elif i == 1:
			ERRORS_IN_LOG = "[COLOR red]" + str(i) + " Error Found in Log[/COLOR]"
		else:
			ERRORS_IN_LOG = "[COLOR red]" + str(i) + " Errors Found in Log[/COLOR]"

	Common.addDir('[COLOR aqua]Press for System Overview[/COLOR]',BASEURL,163,SYSTEM_INFO_ICON,FANART,'')
	if check_folders == "true":
		try:
			Common.addItem("[COLOR white]Cache Size is [/COLOR]" + str(CACHE_SIZE),BASEURL,79,ICON,FANART,'')
		except: 		
			Common.addItem("[COLOR white]Error Getting Cache Size[/COLOR]",BASEURL,79,ICON,FANART,'')
		try:
			Common.addItem("[COLOR white]Packages Size is [/COLOR]" + str(PACKAGES_SIZE),BASEURL,79,ICON,FANART,'')
		except:
			Common.addItem("[COLOR white]Error Getting Packages Size[/COLOR]",BASEURL,79,ICON,FANART,'')
		try:
			Common.addItem("[COLOR white]Thumbnail Size is [/COLOR]" + str(THUMB_SIZE),BASEURL,79,ICON,FANART,'')
		except:
			Common.addItem("[COLOR white]Error Getting Thumbnail Size[/COLOR]",BASEURL,79,ICON,FANART,'')
	Common.addItem("[COLOR aqua]----CLEANUP---------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem('[COLOR white]Auto Clean (Cache, Packages, Thumbnails)[/COLOR]','url',31,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Clear Cache[/COLOR]','url',1,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Purge Packages[/COLOR]','url',3,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Delete Week Old Thumbnails[/COLOR]','url',194,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Delete All Thumbnails (Restart Required)[/COLOR]','url',2,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Purge Databases[/COLOR]','url',188,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Clear Wizard Log[/COLOR]','url',189,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Clear Crash Logs[/COLOR]','url',25,DELETE_ICON,FANART,'')
	Common.addItem("[COLOR aqua]----AUTOCLEAN------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem('[COLOR white]KODEN TV Tools Settings[/COLOR]',BASEURL,9,SETTINGS_ICON,FANART,'')
	Common.addItem('[COLOR white]Auto Clean on Kodi Launch - [/COLOR]' + startup_onoff,BASEURL,112,SETTINGS_ICON,FANART,'')
	#Common.addItem('[COLOR white]Weekly Auto Clean - [/COLOR]' + weekly_onoff,BASEURL,113,SETTINGS_ICON,FANART,'')
	#Common.addItem('[COLOR white]Setup Auto Clean at Specific MB - [/COLOR]' + sizecheck_onoff,BASEURL,9,SETTINGS_ICON,FANART,'')
	Common.addItem("[COLOR aqua]----LOGS------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	if check_log == "true":
		Common.addItem(ERRORS_IN_LOG,BASEURL,155,DIVIDER_ICON,FANART,'')
	Common.addItem('[COLOR white]View last Error in Log File[/COLOR]',BASEURL,154,ERROR_ICON,FANART,'')
	if check_log == "true":
		Common.addItem('[COLOR white]View All ' + str(i) + ' Errors in Log File[/COLOR]',BASEURL,155,ERROR_ICON,FANART,'')
	Common.addItem('[COLOR white]View Full Log File[/COLOR]',BASEURL,82,ERROR_ICON,FANART,'')
	Common.addItem('[COLOR white]Upload Log File[/COLOR]','url',36,ERROR_ICON,FANART,'')
	Common.addItem("[COLOR aqua]----ADDONS----------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem('[COLOR white]Open Addons Settings[/COLOR]','url',126,SETTINGS_ICON,FANART,'')
	Common.addItem('[COLOR white]Open Resolver Settings[/COLOR]','url',204,SETTINGS_ICON,FANART,'')
	Common.addItem('[COLOR white]Open Scraper Settings[/COLOR]','url',205,SETTINGS_ICON,FANART,'')
	#Common.addItem('[COLOR white]Enable Addons[/COLOR]','url',196,UPDATE_ICON,FANART,'')
	Common.addItem('[COLOR white]Remove Addons[/COLOR]','url',191,DELETE_ICON,FANART,'')
	#Common.addDirL('[COLOR white]Remove Addon Data[/COLOR]','url',192,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Force Update Addons & Repositories[/COLOR]','url',125,UPDATE_ICON,FANART,'')
	Common.addItem('[COLOR white]Check for Broken Repositories[/COLOR]','url',147,DIAGNOSE_ICON,FANART,'')
	Common.addItem('[COLOR white]Check for Broken Sources in sources.xml[/COLOR]','url',148,DIAGNOSE_ICON,FANART,'')
	Common.addItem("[COLOR aqua]----FIXES-----------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem('[COLOR white]Ruya Empty List Fix[/COLOR]','url',109,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Fix Addon Update Errors (Remove Addon Database)[/COLOR]','url',10,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Youtube Fix (Clear Data)[/COLOR]','url',193,TOOLS_ICON,FANART,'')
	#Common.addItem('[COLOR white]Remove non ASCII Filenames[/COLOR]','url',200,TOOLS_ICON,FANART,'')
	Common.addItem('[COLOR white]Convert Physical Paths To Special[/COLOR]','url',13,TOOLS_ICON,FANART,'')
	#Common.addItem('[COLOR white]Reload Skin[/COLOR]','url',124,TOOLS_ICON,FANART,'')
	Common.addItem("[COLOR aqua]----MISCELLANEOUS---------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem('[COLOR white]Force Close Kodi[/COLOR]','url',86,DELETE_ICON,FANART,'')
	Common.addItem('[COLOR white]Hide All Passwords[/COLOR]','url',26,PASSWORD_ICON,FANART,'')
	Common.addItem('[COLOR white]Unhide All Passwords[/COLOR]','url',37,PASSWORD_ICON,FANART,'')
	Common.addItem('[COLOR white]Base64 - Encode / Decode[/COLOR]','url',117,PASSWORD_ICON,FANART,'')
	Common.addItem('[COLOR white]Turn Debugging On/Off[/COLOR]','url',127,PASSWORD_ICON,FANART,'')
	Common.addItem("[COLOR aqua]----RESTORE KODI----------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addDir('[COLOR red]SYSTEM RESET (CAUTION)[/COLOR]','url',6,RESET_ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			BACKUP MENU MENU
#######################################################################
	
def BACKUPMENU():
	Common.addItem("[COLOR aqua][B]----BACKUP MENU-----------[/B][/COLOR]",'url',22,DIVIDER_ICON,FANART,'')	
	Common.addItem('[COLOR white]Full Backup (All Files and Folders Included)[/COLOR]','url',69,BACKUP_ICON,FANART,'')	
	Common.addItem('[COLOR white]Build Backup (No Thumbnails, Databases)[/COLOR]','url',70,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Addon Data Backup [/COLOR]','url',108,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Real Debrid & Trakt Backup[/COLOR]','url',103,BACKUP_ICON,FANART,'')
	#Common.addItem("[COLOR aqua][B]--------------------------[/B][/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem("[COLOR aqua][B]----RESTORE MENU----------[/B][/COLOR]",'url',22,DIVIDER_ICON,FANART,'')	
	Common.addDir('[COLOR white]Restore a Backup - (Full/Builds)[/COLOR]','url',71,BACKUP_ICON,FANART,'')
	Common.addDir('[COLOR white]Restore Addon Data[/COLOR]','url',71,BACKUP_ICON,FANART,'')
	Common.addDir('[COLOR white]Restore Real Debrid & Trakt Settings[/COLOR]','url',104,BACKUP_ICON,FANART,'')
	#Common.addItem("[COLOR aqua][B]--------------------------[/B][/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem("[COLOR aqua][B]----OTHER MENU------------[/B][/COLOR]",'url',22,DIVIDER_ICON,FANART,'')	
	Common.addDir('[COLOR white]Delete a Backup[/COLOR]','url',72,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Delete All Backups[/COLOR]','url',73,BACKUP_ICON,FANART,'')
	Common.addItem('[COLOR white]Select Backup Location[/COLOR]','url',9,BACKUP_ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			REAL DEBRID MENU
#######################################################################
	
def DEBRIDMENU():
	Common.addItem("[COLOR aqua][B]----DEBRID MENU-----------[/B][/COLOR]",'url',22,DIVIDER_ICON,FANART,'')	
	#Common.addItem('[COLOR white]Full Backup (All Files and Folders Included)[/COLOR]','url',69,BACKUP_ICON,FANART,'')	

	real = '[COLOR green]ON[/COLOR]' if KEEPREAL == 'true' else '[COLOR red]OFF[/COLOR]'
	last = str(REALSAVE) if not REALSAVE == '' else "Real Debrid Info hasn't been saved yet."
	Common.addFile('[I][COLOR %s]http://real-debrid.com[/COLOR] is a PAID service.[/I]' % COLOR1, '', icon=SETTINGS_ICON, themeit=THEME2)
	Common.addFile('Save My Real Debrid Info: %s' % real, 'togglesetting', 'keepdebrid', icon=BACKUP_ICON, themeit=THEME3)
	if KEEPREAL == 'true':  Common.addFile('Last Save: [COLOR %s]%s[/COLOR]' % (COLOR1, str(last)), '', icon=BACKUP_ICON, themeit=THEME2)
	Common.addFile(wiz.sep(), '', icon=BACKUP_ICON, themeit=THEME3)
	
	for debrid in debridit.ORDER:
		name   = DEBRIDID[debrid]['name']
		path   = DEBRIDID[debrid]['path']
		saved  = DEBRIDID[debrid]['saved']
		file   = DEBRIDID[debrid]['file']
		user   = wiz.getS(saved)
		auser  = debridit.debridUser(debrid)
		icon   = DEBRIDID[debrid]['icon']   if os.path.exists(path) else SETTINGS_ICON
		fanart = DEBRIDID[debrid]['fanart'] if os.path.exists(path) else FANART
		menu  = Common.createMenu('saveaddon', 'Debrid', debrid)
		menu2 = Common.createMenu('save', 'Debrid', debrid)
		menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=debrid)' %   (ADDON_ID, debrid)))
		
		Common.addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME2)
		if not os.path.exists(path): Common.addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
		elif not auser:              Common.addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
		else:                        Common.addFile('[COLOR green]Addon Data: %s[/COLOR]' % auser,'authdebrid', debrid, icon=icon, fanart=fanart, menu=menu)
		if user == "":
			if os.path.exists(file): Common.addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importdebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
			else :                   Common.addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savedebrid', debrid, icon=icon, fanart=fanart, menu=menu2)
		else:                        Common.addFile('[COLOR green]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)
	
	Common.addFile(wiz.sep(), '', themeit=THEME3)
	Common.addFile('Save All Real Debrid Info',          'savedebrid',    'all', icon=BACKUP_ICON,  themeit=THEME2)
	#Common.addItem('Save All Real Debrid Info','url',203,BACKUP_ICON,FANART,'')
	Common.addFile('Recover All Saved Real Debrid Info', 'restoredebrid', 'all', icon=BACKUP_ICON,  themeit=THEME2)
	Common.addFile('Import Real Debrid Info',            'importdebrid',  'all', icon=BACKUP_ICON,  themeit=THEME2)
	Common.addFile('Clear All Saved Real Debrid Info',   'cleardebrid',   'all', icon=BACKUP_ICON,  themeit=THEME2)
	Common.addFile('Clear All Addon Data',               'addondebrid',   'all', icon=BACKUP_ICON,  themeit=THEME2)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			TRAKT MENU
#######################################################################
def TRAKTMENU():
	Common.addItem("[COLOR aqua][B]----TRAKT MENU-----------[/B][/COLOR]",'url',22,DIVIDER_ICON,FANART,'')	
	trakt = '[COLOR green]ON[/COLOR]' if KEEPTRAKT == 'true' else '[COLOR red]OFF[/COLOR]'
	last = str(TRAKTSAVE) if not TRAKTSAVE == '' else "Trakt Info hasn't been saved yet."
	Common.addFile('[I]Create a FREE Account at [COLOR %s]http://trakt.tv[/I][/COLOR]' % COLOR1, '', icon=SETTINGS_ICON, themeit=THEME2)
	Common.addFile('Save My Trakt Info: %s' % trakt, 'togglesetting', 'keeptrakt', icon=BACKUP_ICON, themeit=THEME3)
	if KEEPTRAKT == 'true': Common.addFile('Last Save: [COLOR %s]%s[/COLOR]' % (COLOR1, str(last)), '', icon=BACKUP_ICON, themeit=THEME2)
	Common.addFile(wiz.sep(), '', icon=BACKUP_ICON, themeit=THEME3)
	
	for trakt in traktit.ORDER:
		name   = TRAKTID[trakt]['name']
		path   = TRAKTID[trakt]['path']
		saved  = TRAKTID[trakt]['saved']
		file   = TRAKTID[trakt]['file']
		user   = wiz.getS(saved)
		auser  = traktit.traktUser(trakt)
		icon   = TRAKTID[trakt]['icon']   if os.path.exists(path) else SETTINGS_ICON
		fanart = TRAKTID[trakt]['fanart'] if os.path.exists(path) else FANART
		menu =  Common.createMenu('saveaddon', 'Trakt', trakt)
		menu2 = Common.createMenu('save', 'Trakt', trakt)
		menu.append((THEME2 % '%s Settings' % name,              'RunPlugin(plugin://%s/?mode=opensettings&name=%s&url=trakt)' %   (ADDON_ID, trakt)))
		
		Common.addFile('[+]-> %s' % name,     '', icon=icon, fanart=fanart, themeit=THEME2)
		if not os.path.exists(path): Common.addFile('[COLOR red]Addon Data: Not Installed[/COLOR]', '', icon=icon, fanart=fanart, menu=menu)
		elif not auser:              Common.addFile('[COLOR red]Addon Data: Not Registered[/COLOR]','authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
		else:                        Common.addFile('[COLOR green]Addon Data: %s[/COLOR]' % auser,'authtrakt', trakt, icon=icon, fanart=fanart, menu=menu)
		if user == "":
			if os.path.exists(file): Common.addFile('[COLOR red]Saved Data: Save File Found(Import Data)[/COLOR]','importtrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
			else :                   Common.addFile('[COLOR red]Saved Data: Not Saved[/COLOR]','savetrakt', trakt, icon=icon, fanart=fanart, menu=menu2)
		else:                        Common.addFile('[COLOR green]Saved Data: %s[/COLOR]' % user, '', icon=icon, fanart=fanart, menu=menu2)
	
	Common.addFile(wiz.sep(), '', themeit=THEME3)
	Common.addFile('Save All Trakt Info',          'savetrakt',    'all', icon=BACKUP_ICON,  themeit=THEME2)
	Common.addFile('Recover All Saved Trakt Info', 'restoretrakt', 'all', icon=BACKUP_ICON,  themeit=THEME2)
	Common.addFile('Import Trakt Info',            'importtrakt',  'all', icon=BACKUP_ICON,  themeit=THEME2)
	Common.addFile('Clear All Saved Trakt Info',   'cleartrakt',   'all', icon=BACKUP_ICON,  themeit=THEME2)
	Common.addFile('Clear All Addon Data',         'addontrakt',   'all', icon=BACKUP_ICON,  themeit=THEME2)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)


#######################################################################
#			BUILD MENU
#######################################################################

def BUILDMENU():
	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])

	i=0
	dp.create(ADDONTITLE,"[COLOR blue]We are getting the list of builds from our server.[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]','')	
	dp.update(0)

	v = str(version)
	vv = v.split(".")[0]
	vvv = vv + ".9"
	www = vv + ".0"
	version_start = float(www)
	version_end   = float(vvv)

	namelist      = []
	urllist       = []
	deslist       = []
	countlist     = []
	totallist     = []
	iconlist      = []
	fanartlist    = []
	combinedlists = []

	LINKS = [NOLIMITS_BUILDS,NOLIMITS_BLUE_BUILDS]

	for BUILD_LINK in LINKS:
		BUILD_LINK,COLOR_CODE = BUILD_LINK.split('|SPLIT|')
		link = Common.OPEN_URL(BUILD_LINK).replace('\n','').replace('\r','').replace(',','')
		link = link.replace("<notice></notice>","<notice>null</notice>").replace("<platform></platform>","<platform>16.1</platform>").replace("<youtube></youtube>","<youtube>null</youtube>").replace("<thumbnail></thumbnail>","<thumbnail>null</thumbnail>").replace("<fanart></fanart>","<fanart>null</fanart>").replace("<version></version>","<version>null</version>").replace("<build_image></build_image>","<build_image>null</build_image>").replace("<hash></hash>","<hash>null</hash>")
		match= re.compile('<item>(.+?)</item>').findall(link)
		dis_links = len(match)

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
			try:
				hash=re.compile('<hash>(.+?)</hash>').findall(item)[0]
			except: hash = "null"
			if iconimage.lower() == "null":
				iconimage = ICON
			if fanart.lower() == "null":
				fanart = FANART
			if not "." in platform:
				platform = platform + ".0"
				platform = float(platform)
			else: platform = float(platform)

			skin = 'null'
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"Getting details from build " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]FOUND - [/B] " + name + "[/COLOR]")
			
			if platform >= version_start and platform < version_end:
				countlist.append(str(Common.count(name,TEMP_FILE)))  
				totallist.append(str(Common.count(name+"TOTAL_COUNT",TEMP_FILE)))    
				description = str(notice + "," + hash + "," + "1" + "," + youtube_id + "," + "null" + "," + build_image)
				name = name + "|SPLIT|" + COLOR_CODE + "|SPLIT|" + BUILD_LINK
				namelist.append(name)
				urllist.append(url)
				deslist.append(description) 
				iconlist.append(iconimage)
				fanartlist.append(fanart)
				combinedlists = list(zip(countlist,totallist,namelist,urllist,deslist,iconlist,fanartlist))
	
	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	dp.close()
	for count,total,name,url,description,iconimage,fanart in tup:
		name,COLOR_CODE,BUILD_LINK = name.split('|SPLIT|')
		url = name + "," + url + "," + BUILD_LINK
		countfail = count
		try:
			count2 = int(count)
			count3 = "{:,}".format(count2)
			count = str(count3)
		except: count = countfail
		#bname = " | [COLOR white] This Week:[/COLOR][COLOR aqua][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR aqua][B] " + total + "[/B][/COLOR]"
		bname = ""
		if COLOR_CODE == "dodgerblue":
			title = "[COLOR "+COLOR_CODE+"][B]" + name.upper() + " - BY KODENTV BLUE[/B][/COLOR]" + bname
		else: title = "[COLOR "+COLOR_CODE+"][B]" + name.upper() + " - BY KODENTV[/B][/COLOR]" + bname

		Common.addDir(title,url,83,iconimage,fanart,description)
	
#######################################################################
#		        KEYMAPS MENU for keymap.xml FILES
#######################################################################

def KEYMAPS():
	namelist      = []
	urllist       = []
	countlist     = []
	totallist     = []
	iconlist      = []
	fanartlist    = []
	combinedlists = []

	link = Common.OPEN_URL(KeymapsURL).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?ash="(.+?)"').findall(link)
	if os.path.isfile(KEYBOARD_FILE):
		Common.addItem('[COLOR white][B]Remove Current Keymap Configuration[/B][/COLOR]',BASEURL,128,ICON,FANART,'')
	for name,url,iconimage,fanart,version,description in match:
		name2 = name
		url = name2 + "|SPLIT|" + url
		name = "[COLOR white][B]" + name + "[/B][/COLOR]"
		namelist.append(name)
		urllist.append(url)
		countlist.append(str(Common.count(name2,TEMP_FILE)))
		totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))
		iconlist.append(iconimage)
		fanartlist.append(fanart)
		combinedlists = list(zip(countlist,totallist,namelist,urllist,iconlist,fanartlist))
	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	for count,total,name,url,iconimage,fanart in tup:
		#bname = " | [COLOR white] This Week:[/COLOR][COLOR aqua][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR aqua][B] " + total + "[/B][/COLOR]"
		bname = ""
		Common.addItem(name + bname,url,130,ADVANCED_SET_ICON,FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#		        ADVANCED SETTINGS MENU for advancedsettings.xml FILES
#######################################################################

def ADVANCEDSETTINGS():
	kodi_name = Common.GET_KODI_VERSION()

	namelist      = []
	urllist       = []
	countlist     = []
	totallist     = []
	iconlist      = []
	fanartlist    = []
	combinedlists = []

	link = Common.OPEN_URL(AdvancedSettings).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?escription="(.+?)"').findall(link)
	if os.path.isfile(ADVANCED_SET_FILE):
		Common.addItem('[COLOR white][B]Remove Current Advanced Settings Configuration[/B][/COLOR]',BASEURL,131,DELETE_ICON,FANART,'')
		Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	Common.addItem('[COLOR white][B]Calculated Buffering Fix[/B][/COLOR]',BASEURL,199,SETTINGS_ICON,FANART,'')
	Common.addItem("[COLOR aqua]--------------------------[/COLOR]",BASEURL,79,DIVIDER_ICON,FANART,'')
	for name,url,iconimage,fanart,version,description in match:
		name2 = name
		url = name2 + "|SPLIT|" + url
		name = "[COLOR white][B]" + name + "[/B][/COLOR]"
		description = " "
		Common.addItem(name,url,98,SETTINGS_ICON,FANART,' ')
	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

def ADVANCEDAETTINGSOLD():
	kodi_name = Common.GET_KODI_VERSION()

	namelist      = []
	urllist       = []
	countlist     = []
	totallist     = []
	iconlist      = []
	fanartlist    = []
	combinedlists = []

	link = Common.OPEN_URL(AdvancedSettings).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)".+?ash="(.+?)"').findall(link)
	if os.path.isfile(ADVANCED_SET_FILE):
		Common.addItem('[COLOR white][B]Remove Current Advanced Settings Configuration[/B][/COLOR]',BASEURL,131,ICON,FANART,'')
	for name,url,iconimage,fanart,version,description in match:
		name2 = name
		url = name2 + "|SPLIT|" + url
		name = "[COLOR white][B]" + name + "[/B][/COLOR]"
		namelist.append(name)
		urllist.append(url)
		countlist.append(str(Common.count(name2,TEMP_FILE)))
		totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))
		iconlist.append(iconimage)
		fanartlist.append(fanart)
		combinedlists = list(zip(countlist,totallist,namelist,urllist,iconlist,fanartlist))
	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	for count,total,name,url,iconimage,fanart in tup:
	
		if not kodi_name == "Krypton":
			if not "kodi 17" in name.lower():
				name = name.replace(' - Kodi 16','')
				#bname = " | [COLOR white] This Week:[/COLOR][COLOR aqua][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR aqua][B] " + total + "[/B][/COLOR]"
				bname = ""
				Common.addItem(name + bname,url,98,SETTINGS_ICON,FANART,description)
		else:
			if "kodi 17" in name.lower():
				name = name.replace(' - Kodi 17','')
				#bname = " | [COLOR white] This Week:[/COLOR][COLOR aqua][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR aqua][B] " + total + "[/B][/COLOR]"
				bname = ""
				Common.addItem(name + bname,url,98,SETTINGS_ICON,FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			GET FANRIFFIC THEMES SKINS
#######################################################################

def FANRIFFIC_THEMES():
	dp.create(ADDONTITLE, "[COLOR red][B]NOT CONNECTED![/B][/COLOR]", "[COLOR aqua]Attempting to connect to Fanriffic server.[/COLOR]")

	namelist      = []
	urllist       = []
	countlist     = []
	totallist     = []
	iconlist      = []
	fanartlist    = []
	combinedlists = []
	combinedlists2= []
	
	codename = Common.GET_KODI_VERSION()
	
	if codename == "Jarvis":
		urls = [FANRIFFIC_URL_NEW,FANRIFFIC_URL_OLD]
	elif codename == "Krypton": 
		urls = [FANRIFFIC_KRYPTON]
	else:
		dialog.ok(ADDONTITLE, "Sorry, there are no supported Fanriffic themes for " + codename)
		quit()

	url_count = len(urls)
	i=0
	j = 1

	for url_list in urls:
		dp.update(0, "[COLOR lime][B]CONNECTED![/B][/COLOR]", "[COLOR aqua]Getting themes from location " + str(j) + " of " + str(url_count) + "[/COLOR]")
		link = Common.OPEN_URL(url_list).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
		dis_links = 0
		dis_links = len(match)
		i = 0
		j = j + 1

		for name,url,iconimage,fanart,description in match:
			name2 = name
			url = name2 + "|SPLIT|" + url
			name = "[COLOR white][B]" + name + "[/B][/COLOR]"
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"","","[COLOR white]Getting details from theme " + str(dis_count) + " of " + str(dis_links) + "[/COLOR]")
			namelist.append(name)
			urllist.append(url)
			countlist.append(str(Common.count(name2,TEMP_FILE)))    
			totallist.append(str(Common.count(name2+"TOTAL_COUNT",TEMP_FILE)))    			
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			combinedlists = list(zip(countlist,totallist,namelist,urllist,iconlist,fanartlist))

	tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
	dp.close()

	for count,total,name,url,iconimage,fanart in tup:
		#bname = " | [COLOR white] This Week:[/COLOR][COLOR aqua][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR aqua][B] " + total + "[/B][/COLOR]"
		bname = ""
		Common.addItem(name + bname,url,145,iconimage,iconimage,description="")

#######################################################################
#			SPEEDTEST LIST
#######################################################################

def SPEEDTEST():
	link = Common.OPEN_URL('http://pastebin.com/raw/VECYSGBL').replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	for name,url,iconimage,fanart,description in match:
		Common.addItem('[COLOR ghostwhite]' + name + " | " + description + '[/COLOR]',url,15,SPEEDTEST_ICON,ART+'speedfanart.jpg','')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

def GET_COUNTS():
	get_now = 0
	
	if not os.path.exists(TEMP_FOLDER):
		os.makedirs(TEMP_FOLDER)
		get_now = 1
	if not os.path.isfile(TEMP_FILE):
		text_file = open(TEMP_FILE, 'w')
		text_file.close()
		get_now = 1
	if not os.path.isfile(TEMP_ADDONS):
		text_file = open(TEMP_ADDONS, 'w')
		text_file.close()
		get_now = 1
	if not os.path.isfile(KODIAPPS_FILE):
		text_file = open(KODIAPPS_FILE, 'w')
		text_file.close()
		get_now = 1

	api_interval = plugintools.get_setting("api_interval")

	if api_interval == "0":
		mark = 60
	elif api_interval == "1":
		mark = 50
	elif api_interval == "2":
		mark = 40
	elif api_interval == "3":
		mark = 30
	elif api_interval == "4":
		mark = 20
	elif api_interval == "5":
		mark = 10
	elif api_interval == "6":
		mark = 5
	else: mark = 60
	
	fileCreation = os.path.getmtime(TEMP_FILE)
	fileCreation2 = os.path.getmtime(TEMP_ADDONS)
	fileCreation3 = os.path.getmtime(KODIAPPS_FILE)

	now = time.time()
	check = now - 60*mark

	if get_now == 1:
		counts=Common.OPEN_URL_NORMAL(ECHO_API)

		text_file = open(TEMP_FILE, "w")
		text_file.write(counts)
		text_file.close()

	elif fileCreation < check:
		counts=Common.OPEN_URL_NORMAL(ECHO_API)

		text_file = open(TEMP_FILE, "w")
		text_file.write(counts)
		text_file.close()

	if get_now == 1:
		counts=Common.OPEN_URL_NORMAL(ADDONS_API)

		text_file = open(TEMP_ADDONS, "w")
		text_file.write(counts)
		text_file.close()

	elif fileCreation2 < check:

		counts=Common.OPEN_URL_NORMAL(ADDONS_API)
		text_file = open(TEMP_ADDONS, "w")
		text_file.write(counts)
		text_file.close()
		
	if get_now == 1:
		counts=Common.OPEN_URL_NORMAL(KODIAPPS_API)

		text_file = open(KODIAPPS_FILE, "w")
		text_file.write(counts)
		text_file.close()

	elif fileCreation3 < check:

		counts=Common.OPEN_URL_NORMAL(KODIAPPS_API)
		text_file = open(KODIAPPS_FILE, "w")
		text_file.write(counts)
		text_file.close()

#######################################################################
#			LATEST SPORTS LISTINGS
#######################################################################

def SPORT_LISTINGS():
	url = base64.b64decode(b'aHR0cDovL3d3dy53aGVyZXN0aGVtYXRjaC5jb20vdHYvaG9tZS5hc3A=')
	r = Common.OPEN_URL_NORMAL(url).replace('\r','').replace('\n','').replace('\t','')
	match = re.compile('href="http://www.wheresthematch.com/fixtures/(.+?).asp.+?class="">(.+?)</em> <em class="">v</em> <em class="">(.+?)</em>.+?time-channel ">(.+?)</span>').findall(r)
	for game,name1,name2,gametime in match:
		a,b = gametime.split(" on ")
		Common.addItem('[COLOR white]'+name1+' vs '+name2+' - '+a+' [/COLOR]','','',ICON,FANART,'')
		Common.addItem('[COLOR aqua][B]Watch on '+b+'[/B][/COLOR]','','',ICON,FANART,'')
		Common.addItem('------------------------------------------','','',ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#		        DISPLAYS USER INFO LIKE IP ADDRESS ETC
#######################################################################

def ACCOUNT():

	#######################################################################
	#		FIND WHAT VERSION OF KODI IS RUNNING
	#######################################################################

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])

	if version >= 11.0 and version <= 11.9:
		codename = 'Eden'
	if version >= 12.0 and version <= 12.9:
		codename = 'Frodo'
	if version >= 13.0 and version <= 13.9:
		codename = 'Gotham'
	if version >= 14.0 and version <= 14.9:
		codename = 'Helix'
	if version >= 15.0 and version <= 15.9:
		codename = 'Isengard'
	if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
	if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
	if version >= 18.0 and version <= 18.9:
		codename = 'Leia'
	f = urllib.urlopen("http://www.canyouseeme.org/")
	html_doc = f.read()
	f.close()
	m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))

	if check=="true":
		a = "[COLOR aqua]Yes[/COLOR]"
	else:
		a = "[COLOR aqua]No[/COLOR]"

	Common.addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR aqua]%s' % version + " " + codename + "[/COLOR]",BASEURL,200,SYSTEM_INFO_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]Check For Updates: [/COLOR]' + a,BASEURL,200,SYSTEM_INFO_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]Local IP: [/COLOR][COLOR white]' + s.getsockname()[0] + '[/COLOR]',BASEURL,200,SYSTEM_INFO_ICON,FANART,'')
	Common.addItem('[COLOR ghostwhite]External IP: [/COLOR][COLOR white]' + m.group(0) + '[/COLOR]',BASEURL,200,SYSTEM_INFO_ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#		        MUST HAVE KODI PROGRAMS AND TOOLS MENU
#######################################################################

def KODI_TOOLS():
	link = Common.OPEN_URL(TOOLS).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	for name,url,iconimage,fanart,description in match:
		Common.addItem(name,url,89,KODI_ICON,KODI_FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#		        LIST OF LATEST KODI INSTALLATION FILES
#######################################################################

def LATEST_LIST():
	if xbmc.getCondVisibility('system.platform.windows'):
		LATEST_WINDOWS()

	elif xbmc.getCondVisibility('system.platform.osx'):
		LATEST_OSX()

	elif xbmc.getCondVisibility('system.platform.darwin'):
		LATEST_OSX()

	elif xbmc.getCondVisibility('system.platform.ios'):
		LATEST_IOS()

	elif xbmc.getCondVisibility('system.platform.android'):
		LATEST_ANDROID()
	else:
	
		if xbmc.getCondVisibility('system.platform.linux'):
			platform_name = "Linux"
		elif xbmc.getCondVisibility('system.platform.linuxraspberrypi'):
			platform_name = "Raspberry Pi"
		elif xbmc.getCondVisibility('system.platform.darwin'):
			platform_name = "Linux"
		elif xbmc.getCondVisibility('system.platform.atv2'):
			platform_name = "Apple TV 2"
		elif xbmc.getCondVisibility('system.platform.atv4'):
			platform_name = "Apple TV 4"
		else: platform_name = "Unknown"
		
		Common.addItem('[COLOR white][B]Detected Platform: [/B][/COLOR][COLOR aqua]' + platform_name + '[/COLOR]',url,999,ICON,FANART,'')
		Common.addItem('No installation files found for this platform.',url,999,ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			GETS THE WINDOWS LIST
#######################################################################

def LATEST_WINDOWS():
	if not xbmc.getCondVisibility('system.platform.windows'):
		dialog = xbmcgui.Dialog()
		dialog.ok(ADDONTITLE + " - Windows", "[B][COLOR white]Sorry, this function is only available for Windows devices[/COLOR][/B]",'[COLOR white]Thank you for using KODENTV Tools[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(WINDOWS).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
		Common.addItem('[COLOR aqua][B]EXE Will Be Donwloaded to [COLOR aqua]special://Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		for name,url,iconimage,fanart,description in match:
			Common.addItem(name,url,89,KODI_ICON,KODI_FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			GETS THE OSX LIST
#######################################################################
			
def LATEST_OSX():
	if not xbmc.getCondVisibility('system.platform.osx'):
		dialog = xbmcgui.Dialog()
		dialog.ok(ADDONTITLE + " - OSX", "[B][COLOR white]Sorry, this function is only available for OSX devices[/COLOR][/B]",'[COLOR white]Thank you for using KODENTV Tools[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(OSX).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
		Common.addItem('[COLOR aqua][B].dmg Will Be Donwloaded to [COLOR aqua]special://Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		for name,url,iconimage,fanart,description in match:
			Common.addItem(name,url,89,KODI_ICON,KODI_FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)
	
#######################################################################
#			GETS THE IOS LIST
#######################################################################

def LATEST_IOS():
	if not xbmc.getCondVisibility('system.platform.ios'):
		dialog = xbmcgui.Dialog()
		dialog.ok(ADDONTITLE + " - iOS", "[B][COLOR white]Sorry, this function is only available for iOS devices[/COLOR][/B]",'[COLOR white]Thank you for using KODENTV Tools[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(IOS).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
		Common.addItem('[COLOR aqua][B].deb Will Be Donwloaded to [COLOR aqua]special://Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		for name,url,iconimage,fanart,description in match:
			Common.addItem(name,url,89,KODI_ICON,KODI_FANART,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			GETS THE ANDROID LIST
#######################################################################

def LATEST_ANDROID():
	if not xbmc.getCondVisibility('system.platform.android'):
		dialog = xbmcgui.Dialog()
		dialog.ok(ADDONTITLE + " - Android", "[B][COLOR white]Sorry, this function is only available for Android devices[/COLOR][/B]",'[COLOR white]Thank you for using KODENTV Tools[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(APKS).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
		Common.addItem('[COLOR aqua][B]APKS Will Be Donwloaded to [COLOR aqua]/sdcard/Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addDir('[COLOR aqua]CLICK FOR THE LATEST SIGNED KODI/SPMC APKS WITH UP TO DATE LIB FILE INCLUDED IN APK[/COLOR]',BASEURL,32,APK_ICON,FANART,'')
		for name,url,iconimage,fanart,description in match:
			Common.addItem(name,url,91,iconimage,fanart,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			INSTALLER LIST
#######################################################################

def INSTALLER_APKS():
	dialog = xbmcgui.Dialog()
	dialog.ok(ADDONTITLE, "This function is no longer supported in KODENTV Tools")
	quit()
	#FOR ADDON INSTALLER
	if not xbmc.getCondVisibility('system.platform.android'):
		dialog.ok(ADDONTITLE + " - Android", "[B][COLOR white]Sorry, this function is only available for Android devices[/COLOR][/B]",'[COLOR white]Thank you for using KODENTV Tools[/COLOR]')
		sys.exit(1)
	else:
		dp.create(ADDONTITLE,"[COLOR blue]We are getting the addons from our server.[/COLOR]",'','')	
		i=0
		namelist=[]
		countlist=[]
		iconlist=[]
		fanartlist=[]
		urllist=[]
		link = Common.OPEN_URL(APKS_INSTALLER).replace('\n','').replace('\r','')
		dp.update(0)
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
		dis_links = len(match)
		for name,url,iconimage,fanart in match:
			i = i + 1
			dis_count = str(i)
			progress = 100 * int(i)/int(dis_links)
			dp.update(progress,"Filtering pack " + str(dis_count) + " of " + str(dis_links),"[COLOR grey][B]Found " + name + "[/B][/COLOR]")
			namelist.append(name)
			countlist.append(str(Common.count_addons_week(name)))
			iconlist.append(iconimage)
			fanartlist.append(fanart)
			urllist.append(url)
			combinedlists = list(zip(countlist,namelist,iconlist,fanartlist,urllist))
		tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
		for count,name,iconimage,fanart,url in tup:
			url2 = name + "#!" + url
			#bname = " | [COLOR white] This Week:[/COLOR][COLOR aqua][B] " + count + "[/B][/COLOR]"
                        bname = ""
			Common.addItem("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,171,iconimage,fanart,description="None")

		view_mode = SET_VIEW("list")
		xbmc.executebuiltin(view_mode)
	
#######################################################################
#			GETS THE LATEST SIGNED APKS LIST
#######################################################################

def LATESTAPKSWITHLIB():
	link = Common.OPEN_URL(APKSLIB).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	Common.addItem('[COLOR aqua][B]APKS Will Be Donwloaded to [COLOR aqua]/sdcard/Downloads[/COLOR] You Will Need To Manually Install From There[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
	Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
	for name,url,iconimage,fanart,description in match:
		Common.addDir(name,url,91,iconimage,fanart,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			GETS THE LIBRTMP FILES LIST
#######################################################################

def DOWNLOADLIB():
	link = Common.OPEN_URL(LIB).replace('\n','').replace('\r','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?ersion="(.+?)"').findall(link)
	Common.addItem('[COLOR aqua][B]Lib Files Will Be Donwloaded to [COLOR aqua]the Kodi special directory[/COLOR] You Will Need To Manually Install From There. The Windows Lib File will Auto Install[/B][/COLOR]',BASEURL,79,LIB_ICON,FANART,'')
	Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,LIB_ICON,FANART,'')
	for name,url,iconimage,fanart,description in match:
		Common.addDir(name,url,94,LIB_ICON,fanart,description)

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			ANDROID APKS
#######################################################################

def ANDROID_APKS():
	if not xbmc.getCondVisibility('system.platform.android'):
		dialog = xbmcgui.Dialog()
		dialog.ok(ADDONTITLE + " - Android", "[B][COLOR white]Sorry, this function is only available for Android devices[/COLOR][/B]",'[COLOR white]Thank you for using KODENTV Tools[/COLOR]')
		sys.exit(1)
	else:
		link = Common.OPEN_URL(AND_APKS).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)"').findall(link)
		Common.addItem('[COLOR aqua][B]APKS Will Be Donwloaded to [COLOR aqua]/sdcard/Downloads[/COLOR][/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR dodgerblue][B]THIS LIST IS MAINTAINED BY @VULCAN_TDB [/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR dodgerblue][B]CONTACT HIM ON TWITTER WITH REQUESTS[/B][/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		Common.addItem('[COLOR white]-----------------------------------------------------------[/COLOR]',BASEURL,79,APK_ICON,FANART,'')
		for name,url,iconimage,fanart in match:
			Common.addItem(name,url,91,iconimage,fanart,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			ESSENTIAL CONTACTS LIST
#######################################################################

def KODI_CONTACTS():
	link = Common.OPEN_URL(CONTACTS)
	patron = "<video>(.*?)</video>"
	videos = re.findall(patron,link,re.DOTALL)
	items = []
	for video in videos:
		item = {}
		item["name"] = Common.find_single_match(video,"<name>([^<]+)</name>")
		item["url"] = Common.find_single_match(video,"<url>([^<]+)</url>")
		item["description"] = Common.find_single_match(video,"<description>([^<]+)</description>")

		if "NULL" in item["description"]:
			Common.addItem(item["name"] + '[COLOR white]@[/COLOR][COLOR white]' + item["url"] + '[/COLOR]',BASEURL,666,ICON,FANART,'')
		else:
			Common.addDir(item["name"] + '[COLOR white]@[/COLOR][COLOR white]' + item["url"] + '[/COLOR]',BASEURL,102,ICON,FANART,item["description"])

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

#######################################################################
#			SET VIEW
#######################################################################

def SET_VIEW(name):
	kodi_name = Common.GET_KODI_VERSION()

	if name == "list":
		if kodi_name == "Jarvis":
			command = '"Container.SetViewMode(50)"'
		elif kodi_name == "Krypton":
			command = '"Container.SetViewMode(55)"'
		elif kodi_name == "Leia":
			command = '"Container.SetViewMode(55)"'
		else: command = '"Container.SetViewMode(50)"'
	elif name == "thumbs":
		if kodi_name == "Jarvis":
			command = '"Container.SetViewMode(500)"'
		elif kodi_name == "Krypton":
			command = '"Container.SetViewMode(52)"'
		elif kodi_name == "Leia":
			command = '"Container.SetViewMode(52)"'
		else: command = '"Container.SetViewMode(500)"'
	else:
		if kodi_name == "Jarvis":
			command = '"Container.SetViewMode(50)"'
		elif kodi_name == "Krypton":
			command = '"Container.SetViewMode(55)"'
		elif kodi_name == "Leia":
			command = '"Container.SetViewMode(55)"'
		else: command = '"Container.SetViewMode(50)"'
		
	return command

#######################################################################
#			VIEW CHANGELOG
#######################################################################

def VIEW_CHANGELOG():
	f = open(CHANGELOG,mode='r'); msg = f.read(); f.close()
	Common.TextBox('[COLOR aqua][B]KODENTV Tools[/B][/COLOR]',msg)

#######################################################################
#			HOW TO GET SUPPORT
#######################################################################

def GET_SUPPORT():
	f = requests.get(SUPPORT)
	Common.TextBox('[COLOR aqua][B]KODENTV Tools[/B][/COLOR]',f.text)

#######################################################################
#			ADD TO COMMUNITY BUILDS
#######################################################################

def ADD_COMMUNITY_BUILD():
	f = requests.get(ADD_COMMUNITY)
	Common.TextBox('[COLOR aqua][B]KODENTV Tools[/B][/COLOR]',f.text)

#######################################################################
#			LATEST KODENTV NEWS
#######################################################################

def LATEST_NEWS():
	f = requests.get(NEWS)
	Common.TextBox('[COLOR aqua][B]KODENTV Tools[/B][/COLOR]',f.text)

#######################################################################
#			KODENTV DONATIONS
#######################################################################

def DONATIONS_LINK1():
	#f = requests.get(DONATIONS_URL1)
	#Common.TextBox('[COLOR aqua][B]KODENTV Tools[/B][/COLOR]',f.text)
	web.function27()

def DONATIONS_LINK2():
	#f = requests.get(DONATIONS_URL2)
	#Common.TextBox('[COLOR aqua][B]KODENTV Tools[/B][/COLOR]',f.text)
	web.function28()

def DONATIONS_LINK3():
	#f = requests.get(DONATIONS_URL3)
	#Common.TextBox('[COLOR aqua][B]KODENTV Tools[/B][/COLOR]',f.text)
	web.function29()

#######################################################################
#			KODENTV CREDITS
#######################################################################

def VIEW_CREDITS():
	f = requests.get(CREDITS)
	Common.TextBox('[COLOR aqua][B]KODENTV Tools[/B][/COLOR]',f.text)

#######################################################################
#			REMOVE KEYBOARD.XML FILE
#######################################################################

def REMOVE_KEYBOARD_FILE():
	try:
		os.remove(KEYBOARD_FILE)
	except:
		dialog.ok(ADDONTITLE, "[B][COLOR white]Sorry, KODENTV Tools encountered an error[/COLOR][/B]",'[COLOR white]We were unable to remove the keyboard.xml file.[/COLOR]')
		sys.exit(0)
		
	dialog.ok(ADDONTITLE, "[B][COLOR white]Success, we have removed the keyboards.xml file.[/COLOR][/B]",'[COLOR white]Thank you for using KODENTV Tools[/COLOR]')
	xbmc.executebuiltin("Container.Refresh")

#######################################################################
#			REMOVE ADVANCEDSETTINGS.XML FILE
#######################################################################

def REMOVE_ADVANCED_FILE():
	try:
		os.remove(ADVANCED_SET_FILE)
	except:
		dialog.ok(ADDONTITLE, "[B][COLOR white]Sorry, KODENTV Tools encountered an error[/COLOR][/B]",'[COLOR white]We were unable to remove the advancedsettings.xml file.[/COLOR]')
		sys.exit(0)
		
	dialog.ok(ADDONTITLE, "[B][COLOR white]Success, we have removed the advancedsettings.xml file.[/COLOR][/B]",'[COLOR white]Thank you for using KODENTV Tools[/COLOR]')
	xbmc.executebuiltin("Container.Refresh")

#######################################################################
#			REPO SOURCE CHECKER (BY KODIAPPS)
#######################################################################

def REPO_SOURCE_CHECKER():
	try:
		link=Common.OPEN_URL_NORMAL(KODIAPPS_API).replace('<tag></tag>','<tag>null</tag>')
		match=re.compile('<item>(.+?)</item>',re.DOTALL).findall(link)
		Common.addItem("[COLOR dodgerblue][B]THE FOLLOWING INFORMATION IS BROUGHT TO YOU BY KODIAPPS.COM[/B][/COLOR]","url",999,KODIAPPS_ICON,KODIAPPS_FANART,'This information is brought to you by kodiapps.com')
		Common.addItem("---------------------------------------------------------------","url",999,KODIAPPS_ICON,KODIAPPS_FANART,'This information is brought to you by kodiapps.com')
		for items in match:

			name=re.compile('<name>(.+?)</name>').findall(items)[0]    
			repo=re.compile('<repo>(.+?)</repo>').findall(items)[0]    
			source=re.compile('<sce>(.+?)</sce>').findall(items)[0]    
			try:
				iconimage=re.compile('<imge>(.+?)</imge>').findall(items)[0]    
			except: iconimage = KODIAPPS_ICON
			
			if "O" in source:
				source = "[COLOR lime][B]ONLINE[/B][/COLOR]"
			else: source = "[COLOR red][B]OFFLINE[/B][/COLOR]"
			if "O" in repo:
				repo = "[COLOR lime][B]ONLINE[/B][/COLOR]"
			else: repo = "[COLOR red][B]OFFLINE[/B][/COLOR]"
			
			name = "[COLOR aqua][B]" + name + "[/B][/COLOR]"
			Common.addItem(name + " - [COLOR white]Source: [/COLOR]" + source + "[COLOR white] | " + "Repo: [/COLOR]" + repo  ,"url",999,iconimage,KODIAPPS_FANART,'This information is brought to you by kodiapps.com')
	except:
		dialog.ok(ADDONTITLE,"There was an error getting the information from Kodiapps.com Please try again later.")
		quit()

def GET_KODIAPPS_RANKING():
	if not os.path.isfile(KODIAPPS_FILE):
		open(KODIAPPS_FILE, 'w')

	fileCreation = os.path.getmtime(KODIAPPS_FILE)

	now = time.time()
	check = now - 60*60
	
	text_file = open(KODIAPPS_FILE)
	compfile = text_file.read()  
	
	if len(compfile) == 0:
		counts=Common.OPEN_URL_NORMAL(KODIAPPS_API)

		text_file = open(KODIAPPS_FILE, "w")
		text_file.write(counts)
		text_file.close()

	elif fileCreation < check:

		counts=Common.OPEN_URL_NORMAL(KODIAPPS_API)

		text_file = open(KODIAPPS_FILE, "w")
		text_file.write(counts)
		text_file.close()

	get_file = open(KODIAPPS_FILE)
	get_data = get_file.read()  
	link=get_data.replace('<tag></tag>','<tag>null</tag>')
	match=re.compile('<item>(.+?)</item>',re.DOTALL).findall(link)
	for items in match:
		try:
			name=re.compile('<name>(.+?)</name>').findall(items)[0] 
			rank=re.compile('<rank>(.+?)</rank>').findall(items)[0] 
			iconimage=re.compile('<imge>(.+?)</imge>').findall(items)[0]    
			url2=re.compile('<link>(.+?)</link>').findall(items)[0]    
			Common.addItem("[COLOR aqua][B]" + rank + "[/COLOR] - [COLOR white]" + name + "[/B][/COLOR]",url2,186,iconimage,KODIAPPS_FANART,"")
		except: pass

def GET_KODIAPPS_INFORMATION(name,url,iconimage):
	name = name.split(' - ')[1]
	name = name.replace('[COLOR white]','') \
	.replace('[/COLOR]','') \
	.replace('[/B]','')
	
	choice = dialog.select("[COLOR aqua][B]" + str(name) + " - Please Select an Option[/B][/COLOR]", ['[COLOR blue]View ' + str(name) + ' Information[/COLOR]','[COLOR blue]Add ' + str(name) + ' Source to File Manager[/COLOR]'])

	link = Common.OPEN_URL_DIALOG(url).replace('\n',' ').replace('\r',' ')
	try:
		url2=re.compile('Enter (.+?) in the top box',re.DOTALL).findall(link)[0]
	except: url2="null"
	match=re.compile('<h1 style="padding:10px(.+?)</div>',re.DOTALL).findall(link)

	if choice == 0:
		display = ""
		link = Common.OPEN_URL_NORMAL(url).replace('\n',' ').replace('\r',' ')
		for items in match:
			
				heading = re.compile('>(.+?)</h1>').findall(items)[0]
				heading = "[COLOR aqua][B]" + heading + "[/B][/COLOR]"
				content = re.compile('<h4>(.+?)</h4>').findall(items)[0] 
				content = content.replace('</li>','\n')
				content = content.strip('	')
				content = content.strip(' ')
				heading = heading.strip(' ')
				heading = strip_tags(heading)
				content = strip_tags(content)
				display = display + heading + "\n\n" + content + "\n\n"
					
		display = display + "\n[COLOR dodgerblue][B]Information brought to you by Kodiapps.com[/B][/COLOR]"

		Common.TextBox("[COLOR aqua]Kodiapps Addon Information[/COLOR]",display)
	elif choice == 1:

		SOURCES     =  xbmc.translatePath(os.path.join('special://profile/userdata','sources.xml'))
		
		try:
			if not os.path.isfile(SOURCES):
				open(SOURCES, 'w')
			source_test = open(SOURCES).read().replace('/','')
		except:
			dialog.ok(ADDONTITLE, "Sorry, we could not access your sources.xml file.")
			quit()   
		url_test    = url2.replace('/','')

		if url_test in source_test:
			dialog.ok(ADDONTITLE, "Sorry, the source " + url2 + " is already in your file manager")
			quit()
		if not url_test in source_test:
			OLD = '<files>\n		<default pathversion="1"></default>'
			NEW = '<files>\n		<default pathversion="1"></default>\n		<source>\n			<name>'+name+'</name>\n			<path pathversion="1">'+url2+'</path>\n			<allowsharing>true</allowsharing>\n		</source>'
			a=open(SOURCES).read()
			b=a.replace(OLD, NEW)
			f= open((SOURCES), mode='w')
			f.write(str(b))
			f.close()
		if not url_test in source_test:
			OLD = '<files>\n        <default pathversion="1"></default>'
			NEW = '<files>\n        <default pathversion="1"></default>\n		<source>\n			<name>'+name+'</name>\n			<path pathversion="1">'+url2+'</path>\n			<allowsharing>true</allowsharing>\n		</source>'
			a=open(SOURCES).read()
			b=a.replace(OLD, NEW)
			f= open((SOURCES), mode='w')
			f.write(str(b))
			f.close()

		source_test = open(SOURCES).read().replace('/','')

		if url_test in source_test:
			dialog.ok(ADDONTITLE, "[COLOR white]Name: [/COLOR][COLOR aqua]" + str(name) + "[/COLOR]", "[COLOR white]Source: [/COLOR][COLOR aqua]" + str(url2) + "[/COLOR]","[COLOR dodgerblue]Succesfully added to file manager.[/COLOR]")
		else:
			dialog.ok(ADDONTITLE, "[COLOR white]Name: [/COLOR][COLOR aqua]" + str(name) + "[/COLOR]", "[COLOR white]Source: [/COLOR][COLOR aqua]" + str(url2) + "[/COLOR]","[COLOR red]Was NOT added to the File Manager, please try again later.[/COLOR]")

	else: quit()

#######################################################################
#			AUTO UPDATER
#######################################################################

def AUTO_UPDATER(name):
	GET_VERSION         =  xbmc.translatePath('special://home/addons/' + ADDON_ID + '/addon.xml')
	GET_REPO_VERSION    =  xbmc.translatePath('special://home/addons/repository.echo/addon.xml')
	BASE_UPDATE         = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2VjaG9jb2RlcmtvZGkvcmVwb3NpdG9yeS5lY2hvL3Jhdy9tYXN0ZXIvemlwcy9wbHVnaW4ucHJvZ3JhbS5lY2hvd2l6YXJkL3BsdWdpbi5wcm9ncmFtLmVjaG93aXphcmQt')
	BASE_REPO_UPDATE    = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2VjaG9jb2RlcmtvZGkvcmVwb3NpdG9yeS5lY2hvL3Jhdy9tYXN0ZXIvemlwcy9yZXBvc2l0b3J5LmVjaG8vcmVwb3NpdG9yeS5lY2hvLQ==')
	BASE_XXX_UPDATE     = base64.b64decode(b'aHR0cHM6Ly9naXRodWIuY29tL2VjaG9jb2RlcmtvZGkvcmVwb3NpdG9yeS54eHhlY2hvL3Jhdy9tYXN0ZXIvemlwcy9yZXBvc2l0b3J5Lnh4eGVjaG8vcmVwb3NpdG9yeS54eHhlY2hvLQ==')
	XXX_REPO            = xbmc.translatePath('special://home/addons/repository.xxxecho')
	GET_XXX_VERSION     =  xbmc.translatePath('special://home/addons/repository.xxxecho/addon.xml')
	found = 0

	try:
		Common.OPEN_URL_NORMAL("http://www.google.com")
	except:
		dialog.ok(ADDONTITLE,'[COLOR red][B]Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.[/B][/COLOR]')
		sys.exit(0)

	try:
		dp.create(ADDONTITLE,"Checking for repository updates",'', 'Please Wait...')	
		dp.update(0)
		a=open(GET_REPO_VERSION).read()
		b=a.replace('\n',' ').replace('\r',' ')
		match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
		for item in match:
			dp.update(25)
			new_version = float(item) + 0.01
			url = BASE_REPO_UPDATE + str(new_version) + '.zip'
			result = requests.get(url)
			if "Not Found" not in result.content:
				found = 1
				dp.update(75)
				path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
				if not os.path.exists(path):
					os.makedirs(path)
				lib=os.path.join(path, 'repoupdate.zip')
				try: os.remove(lib)
				except: pass
				dp.update(100)
				dp.update(0,"","Downloading Update Please Wait","")
				import downloader
				downloader.download(url, lib, dp)
				addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
				dp.update(0,"","Extracting Update Please Wait","")
				import extract
				extract.all(lib,addonfolder,dp)
				try: os.remove(lib)
				except: pass
				xbmc.executebuiltin("UpdateLocalAddons")
				xbmc.executebuiltin("UpdateAddonRepos")
				dialog.ok(ADDONTITLE,"ECHO repository was updated to " + str(new_version) + ', you may need to restart the addon for changes to take effect')

		if os.path.exists(XXX_REPO):
			dp.update(50,"Checking for XXX repository updates")
			a=open(GET_XXX_VERSION).read()
			b=a.replace('\n',' ').replace('\r',' ')
			match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
			for item in match:
				new_version = float(item) + 0.01
				url = BASE_XXX_UPDATE + str(new_version) + '.zip'
				result = requests.get(url)
				if "Not Found" not in result.content:
					found = 1
					dp.update(75)
					path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
					if not os.path.exists(path):
						os.makedirs(path)
					lib=os.path.join(path, 'repoupdate.zip')
					try: os.remove(lib)
					except: pass
					dp.update(100)
					dp.update(0,"","Downloading Update Please Wait","")
					import downloader
					downloader.download(url, lib, dp)
					addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
					dp.update(0,"","Extracting Update Please Wait","")
					import extract
					extract.all(lib,addonfolder,dp)
					try: os.remove(lib)
					except: pass
					xbmc.executebuiltin("UpdateLocalAddons")
					xbmc.executebuiltin("UpdateAddonRepos")
					dialog.ok(ADDONTITLE,"ECHO XXX repository was updated to " + str(new_version) + ', you may need to restart the addon for changes to take effect')

		dp.update(75,"Checking for addon updates")
		a=open(GET_VERSION).read()
		b=a.replace('\n',' ').replace('\r',' ')
		match=re.compile('name=".+?".+?version="(.+?)".+?provider-name=".+?">').findall(str(b))
		for item in match:
			new_version = float(item) + 0.01
			url = BASE_UPDATE + str(new_version) + '.zip'
			result = requests.get(url)
			if "Not Found" not in result.content:
				found = 1
				dp.update(75)
				path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
				if not os.path.exists(path):
					os.makedirs(path)
				lib=os.path.join(path, 'wizupdate.zip')
				try: os.remove(lib)
				except: pass
				dp.update(100)
				dp.update(0,"","Downloading Update Please Wait","")
				import downloader
				downloader.download(url, lib, dp)
				addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
				dp.update(0,"","Extracting Update Please Wait","")
				import extract
				extract.all(lib,addonfolder,dp)
				try: os.remove(lib)
				except: pass
				xbmc.executebuiltin("UpdateLocalAddons")
				xbmc.executebuiltin("UpdateAddonRepos")
				dp.update(100)
				dp.close
				dialog.ok(ADDONTITLE,"KODENTV Tools was updated to " + str(new_version) + ', you may need to restart the addon for changes to take effect')
	except:
		dialog.ok(ADDONTITLE,'Sorry! We encountered an error whilst checking for updates. You can make Kodi force check the repository for updates as an alternative if you wish.')
		quit()

	if dp.iscanceled():
		dp.close()
	else:
		if found == 0:
			if not name == "no dialog":
				dialog.ok(ADDONTITLE,"There are no updates at this time.")
				quit()

#######################################################################
#			PLAY VIDEO FUNCTION
#######################################################################

def PLAYVIDEO(url):
	xbmc.Player().play(url)
	
def GETTEMP():
	TEMP_FOLDER   =  xbmc.translatePath(os.path.join('special://profile/addon_data/' + ADDON_ID,'temp'))
	TEMP_BUILDS   =  xbmc.translatePath(os.path.join('special://profile/addon_data/' + ADDON_ID,'temp/temp.xml'))
	TEMP_ADDONS   =  xbmc.translatePath(os.path.join('special://profile/addon_data/' + ADDON_ID,'temp/temp_installer.xml'))
	BASEURL       =  base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
	BUILDS_API    =  BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1idWlsZHMmYWN0aW9uPWNvdW50')
	ADDONS_API    =  BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1hZGRvbnMmYWN0aW9uPWNvdW50')
	dialog        =  xbmcgui.Dialog()
	passed        =  0

	dp.create(ADDONTITLE, "[COLOR aqua][B]Connecting to the KODENTV Tools API....[/B][/COLOR]")
	dp.update(0)

	if os.path.exists(TEMP_FOLDER):
		
		try:
			shutil.rmtree(TEMP_FOLDER)
		except: pass

	try:
		if not os.path.exists(TEMP_FOLDER):
			os.makedirs(TEMP_FOLDER)

		if not os.path.isfile(TEMP_BUILDS):
			open(TEMP_BUILDS, 'w')
		if not os.path.isfile(TEMP_ADDONS):
			open(TEMP_ADDONS, 'w')
		if not os.path.isfile(KODIAPPS_FILE):
			open(KODIAPPS_FILE, 'w')
	except: pass
		
	try:
		dp.update(25, '[COLOR aqua][B]Connected![/B][/COLOR]','[COLOR white]Getting build information from the API.[/COLOR]')
		req = urllib2.Request(BUILDS_API)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
		response = urllib2.urlopen(req)
		counts=response.read()
		response.close()
		text_file = open(TEMP_BUILDS, "w")
		text_file.write(counts)
		text_file.close()

		dp.update(50, '','[COLOR white]Getting addon installer information from the API.[/COLOR]')
		req = urllib2.Request(ADDONS_API)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
		response = urllib2.urlopen(req)
		counts=response.read()
		response.close()
		text_file = open(TEMP_ADDONS, "w")
		text_file.write(counts)
		text_file.close()
		
		dp.update(75, '','[COLOR white]Getting addon installer information from the API.[/COLOR]')
		req = urllib2.Request(KODIAPPS_API)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
		response = urllib2.urlopen(req)
		counts=response.read()
		response.close()
		text_file = open(KODIAPPS_FILE, "w")
		text_file.write(counts)
		text_file.close()

		dp.update(100, '','[COLOR dodgerblue]Finishing up.[/COLOR]')
		dp.close()
		dialog.ok(ADDONTITLE, "We have successfully genenerated the KODENTV download counters.")
		passed = 1
		quit()
	except: pass
		
	if passed == 0:
		dp.close()
		dialog.ok(ADDONTITLE, "There was an error generating the download counters. Please try again later.")
		quit()

def CLEARTEMP():
	dp.create(ADDONTITLE, "[COLOR aqua]Removing KODENTV Tools temp files.[/COLOR]")
	
	TEMP_FOLDER      =  xbmc.translatePath(os.path.join('special://profile/addon_data/' + ADDON_ID,'temp'))

	if os.path.exists(TEMP_FOLDER):
		
		try:
			shutil.rmtree(TEMP_FOLDER)
		except:
			dp.close()
			dialog.ok(ADDONTITLE, "There was an error removing the KODENTV temp files.")
			quit()
		dp.close()
		dialog.ok(ADDONTITLE, "We have succesfully removed the KODENTV temp files.")
		quit()

	else:
		dp.close()
		dialog.ok(ADDONTITLE, "No temp files could be found.")
		quit()

#######################################################################
#			DISPLAY INFORMATION IN A DIALOG
#######################################################################

def DISPLAY_INFORMATION(url):
	dialog.ok(ADDONTITLE, str(url))

#######################################################################
#			OPEN THE SETTINGS DIALOG
#######################################################################

def OPEN_SETTINGS(params):
    plugintools.open_settings_dialog()

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#######################################################################
#			YOUTUBE FIX
#######################################################################

def youtubefix():
	dialog = xbmcgui.Dialog()
	if os.path.exists(YTDATA):
		try:
			shutil.rmtree(YTDATA)
		except:
			dialog.ok(ADDONTITLE,"[COLOR red]Oops, There Was An Error Removing Data![/COLOR]")
			sys.exit(0)
		dialog.ok(ADDONTITLE,"[COLOR aqua]Fixed!.[/COLOR]")
		xbmc.executebuiltin("Container.Refresh")
		sys.exit(0)
	else:
		dialog.ok(ADDONTITLE,"[COLOR orange]No YouTube Data Present![/COLOR]")
		sys.exit(0)

##################################################
### DELETE Total Clean, Clear Cache, Clear Thumbs
##################################################
def totalClean():
	choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Would you like to Clear Cache, Packages and Thumbnails?[/COLOR]' % COLOR2, nolabel='[B][COLOR %s]Cancel Process[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Clean All[/COLOR][/B]' % COLOR2)
	if choice == 1:
		wiz.clearCache()
		clearThumb('total')
		wiz.clearPackages('total')
	else: 
		wiz.log('Auto Clean Cancelled!')
		wiz.LogNotify("[COLOR %s]Total Cleanup[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		sys.exit()

def clearCache():
	choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Would you like to Clear Cache?[/COLOR]' % COLOR2, nolabel='[B][COLOR %s]No, Cancel[/COLOR][/B]' % COLOR1, yeslabel='[B][COLOR %s]Clear Cache[/COLOR][/B]' % COLOR2)
	if choice == 1:
		wiz.clearCache()
	else: 
		wiz.log('Clear Cache Cancelled!')
		wiz.LogNotify("[COLOR %s]Clear Cache[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		sys.exit()

def clearThumb(type=None):
	latest = wiz.latestDB('Textures')
	if not type == None: choice = 1
	else: choice = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to delete the %s file and Thumbnails folder?" % (COLOR2, latest), "[COLOR %s]Don't worry, they will repopulate on the next startup.[/COLOR]" % COLOR1, nolabel="[B][COLOR %s]Don't Delete[/COLOR][/B]" % COLOR1, yeslabel='[B][COLOR %s]Delete Thumbs[/COLOR][/B]' % COLOR2)
	if choice == 1:
		try: wiz.removeFile(os.join(DATABASE, latest))
		except: wiz.log('Failed to delete, Purging DB.'); wiz.purgeDb(latest)
		wiz.removeFolder(THUMBS)
		#if not type == 'total': wiz.killxbmc()   ### This is commented out so that a Force Close isn't performed after the Clear Thumbnails process completes! ###
		wiz.redoThumbs()
	else: 
		wiz.LogNotify("[COLOR %s]Clear Thumbnails[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		wiz.log('Clear Thumbnails Cancelled!')
		sys.exit()

#######################################################################
#			PURGE DB
#######################################################################

def purgeDb():
	DB = []; display = []
	KODIVERSION=Common.GET_KODI_VERSION()
	for dirpath, dirnames, files in os.walk(HOME):
		for f in fnmatch.filter(files, '*.db'):
			if f != 'Thumbs.db':
				found = os.path.join(dirpath, f)
				DB.append(found)
				dir = found.replace('\\', '/').split('/')
				display.append('(%s) %s' % (dir[len(dir)-2], dir[len(dir)-1]))
	if KODIVERSION >= 16:
		choice = dialog.multiselect("[COLOR %s]Select DB File to Purge:[/COLOR]" % COLOR1, display)
		if choice == None: wiz.LogNotify("[COLOR %s]Purge Databases[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		elif len(choice) == 0: wiz.LogNotify("[COLOR %s]Purge Databases[/COLOR]" % COLOR1, "[COLOR %s]None Selected![/COLOR]" % COLOR2)
		else: 
			for purge in choice: wiz.purgeDb(DB[purge])
	else:
		choice = dialog.select("[COLOR %s]Select DB File to Purge:[/COLOR]" % COLOR1, display)
		if choice == -1: wiz.LogNotify("[COLOR %s]Purge Databases[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
		elif choice == 0: wiz.LogNotify("[COLOR %s]Purge Databases[/COLOR]" % COLOR1, "[COLOR %s]None Selected![/COLOR]" % COLOR2)
		else: wiz.purgeDb(DB[purge])

#######################################################################
#			Addon Stuff
#######################################################################
def enableAddons():
	#addFile("[I][B][COLOR red]!!Notice: Disabling Some Addons Can Cause Issues!![/COLOR][/B][/I]", '', icon=ICONMAINT)
	Common.addItem("[I][B][COLOR red]!!Notice: Disabling Some Addons Can Cause Issues!![/COLOR][/B][/I]",BASEURL,22,UPDATE_ICON,FANART,'')
	fold = glob.glob(os.path.join(ADDONS, '*/'))
	x = 0
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		if foldername in EXCLUDES: continue
		if foldername in DEFAULTPLUGINS: continue
		addonxml = os.path.join(folder, 'addon.xml')
		if os.path.exists(addonxml):
			x += 1
			fold   = folder.replace(ADDONS, '')[1:-1]
			f      = open(addonxml)
			a      = f.read().replace('\n','').replace('\r','').replace('\t','')
			match  = wiz.parseDOM(a, 'addon', ret='id')
			match2 = wiz.parseDOM(a, 'addon', ret='name')
			try:
				pluginid = match[0]
				name = match2[0]
			except:
				continue
			try:
				add    = xbmcaddon.Addon(id=pluginid)
				state  = "[COLOR green][Enabled][/COLOR]"
				goto   = "false"
			except:
				state  = "[COLOR red][Disabled][/COLOR]"
				goto   = "true"
				pass
			icon   = os.path.join(folder, 'icon.png') if os.path.exists(os.path.join(folder, 'icon.png')) else ICON
			fanart = os.path.join(folder, 'fanart.jpg') if os.path.exists(os.path.join(folder, 'fanart.jpg')) else FANART
			#addFile("%s %s" % (state, name), 'toggleaddon', fold, goto, icon=icon, fanart=fanart)
			##Common.addFile("%s %s" % (state, name), 'toggleaddon', fold, goto, icon=icon, fanart=fanart)
			#Common.addItem("%s %s" % (state, name),BASEURL,197,fold,goto,UPDATE_ICON,FANART,'')
			Common.addItem("%s %s" % (state, name),BASEURL,197,UPDATE_ICON,FANART,'')
			f.close()
	if x == 0:
		#addFile("No Addons Found to Enable or Disable!", '', icon=ICONMAINT)
		Common.addItem("No Addons Found to Enable or Disable!",BASEURL,22,UPDATE_ICON,FANART,'')
	#setView('files', 'viewType')
	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

def removeAddon(addon, name, over=False):
	if not over == False:
		yes = 1
	else: 
		yes = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Are you sure you want to delete the addon:" % COLOR2, "Name: [COLOR %s]%s[/COLOR]" % (COLOR1, name), "ID: [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR1, addon), yeslabel="[B][COLOR %s]Remove Addon[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1)
	if yes == 1:
		folder = os.path.join(ADDONS, addon)
		wiz.log("Removing Addon %s" % addon)
		wiz.cleanHouse(folder)
		xbmc.sleep(200)
		try: shutil.rmtree(folder)
		except Exception ,e: wiz.log("Error removing %s" % addon, xbmc.LOGNOTICE)
		removeAddonData(addon, name, over)
	if over == False:
		wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s Removed[/COLOR]" % (COLOR2, name))

def removeAddonData(addon, name=None, over=False):
	if addon == 'all':
		if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in your Userdata folder?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR %s]Remove Data[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1):
			wiz.cleanHouse(ADDONDATA)
		else:
			wiz.LogNotify("[COLOR %s]Remove ALL Addon Data[/COLOR]" % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
			sys.exit()
	elif addon == 'uninstalled':
		if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in your Userdata folder for [COLOR %s]UNINSTALLED[/COLOR] addons?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR %s]Remove Data[/COLOR][/B]", nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1):
			total = 0
			for folder in glob.glob(os.path.join(ADDONDATA, '*')):
				foldername = folder.replace(ADDONDATA, '').replace('\\', '').replace('/', '')
				if foldername in EXCLUDES: pass
				elif os.path.exists(os.path.join(ADDONS, foldername)): pass
				else: wiz.cleanHouse(folder); total += 1; wiz.log(folder); shutil.rmtree(folder)
			wiz.LogNotify("[COLOR %s]Remove Uninstalled Data[/COLOR]" % COLOR1, "[COLOR %s]%s Folder(s) Removed[/COLOR]" % (COLOR2, total))
		else:
			wiz.LogNotify("[COLOR %s]Remove Uninstalled Data[/COLOR]" % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
			sys.exit()
	elif addon == 'empty':
		if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] EMPTY addon data folders in your Userdata folder?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR %s]Remove Data[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1):
			total = wiz.emptyfolder(ADDONDATA)
			wiz.LogNotify('[COLOR %s]Remove Empty Folders[/COLOR]' % COLOR1, '[COLOR %s]%s Folders(s) Removed[/COLOR]' % (COLOR2, total))
		else:
			wiz.LogNotify("[COLOR %s]Remove Empty Folders[/COLOR]" % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
			sys.exit()
	else:
		addon_data = os.path.join(USERDATA, 'addon_data', addon)
		if addon in EXCLUDES:
			wiz.LogNotify("[COLOR %s]Protected Plugin[/COLOR]" % COLOR1, "[COLOR %s]NOT allowed to remove this![/COLOR]" % COLOR2)
			sys.exit()
		elif os.path.exists(addon_data):  
			if DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to remove the addon data for:[/COLOR]" % COLOR2, "[COLOR %s]%s[COLOR %s]?[/COLOR]" % (COLOR1, addon, COLOR2), yeslabel="[B][COLOR %s]Remove Data[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Don't Remove[/COLOR][/B]" % COLOR1):
				wiz.cleanHouse(addon_data)
				try:
					shutil.rmtree(addon_data)
				except:
					wiz.log("Error deleting: %s" % addon_data)
			else: 
				wiz.LogNotify("[COLOR %s]Remove Addon Data[/COLOR]" % COLOR1, "[COLOR %s]NOT Removed![/COLOR]" % COLOR2)
				wiz.log('Addon data for %s was NOT removed' % addon)
				sys.exit()
	wiz.refresh()

def removeAddonMenu():
	KODIVERSION=Common.GET_KODI_VERSION()
	fold = glob.glob(os.path.join(ADDONS, '*/'))
	addonnames = []; addonids = []
	for folder in sorted(fold, key = lambda x: x):
		foldername = os.path.split(folder[:-1])[1]
		if foldername in EXCLUDES: continue
		elif foldername in DEFAULTPLUGINS: continue
		elif foldername == 'packages': continue
		xml = os.path.join(folder, 'addon.xml')
		if os.path.exists(xml):
			f      = open(xml)
			a      = f.read()
			match  = wiz.parseDOM(a, 'addon', ret='id')

			addid  = foldername if len(match) == 0 else match[0]
			try: 
				add = xbmcaddon.Addon(id=addid)
				addonnames.append(add.getAddonInfo('name'))
				addonids.append(addid)
			except:
				pass
	if len(addonnames) == 0:
		wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]None Found![/COLOR]" % COLOR2)
		sys.exit()
	if KODIVERSION > 16:
		selected = DIALOG.multiselect("[COLOR %s]Select the addons you wish to remove:[/COLOR]" % COLOR1, addonnames)
	else:
		selected = []; choice = 0
		tempaddonnames = ["-- Click here to Continue --"] + addonnames
		while choice == 0:
			choice = DIALOG.select("[COLOR %s]Select the addons you wish to remove:[/COLOR]" % COLOR1, tempaddonnames)
			if choice == -1: 
				wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
				sys.exit()
			elif choice == 0: 
				wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]None Selected![/COLOR]" % COLOR2)
				sys.exit()
			else: 
				choice2 = (choice-1)
				if choice2 in selected:
					selected.remove(choice2)
					tempaddonnames[choice] = addonnames[choice2]
				else:
					selected.append(choice2)
					tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
	if selected == None: 
			wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]Cancelled![/COLOR]" % COLOR2)
			sys.exit()
	if len(selected) > 0:
		wiz.addonUpdates('set')
		for addon in selected:
			removeAddon(addonids[addon], addonnames[addon], True)
		xbmc.sleep(500)
		if INSTALLMETHOD == 1: todo = 1
		elif INSTALLMETHOD == 2: todo = 0
		else: todo = DIALOG.yesno("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Would you like to [COLOR %s]Force Close[/COLOR] Kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR %s]Reload Profile[/COLOR][/B]" % COLOR2, nolabel="[B][COLOR %s]Force Close[/COLOR][/B]" % COLOR1)
		if todo == 1: wiz.reloadFix('remove addon')
		else: wiz.addonUpdates('reset'); wiz.killxbmc(True)
	else: wiz.LogNotify("[COLOR %s]Remove Addons[/COLOR]" % COLOR1, "[COLOR %s]None Selected![/COLOR]" % COLOR2)

def removeAddonDataMenu():
	#if os.path.exists(ADDONDATA):
	Common.addItem('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data','url',22,UPDATE_ICON,FANART,'')
	#else:
	Common.addItem('No Addon data folder found.','url',22,UPDATE_ICON,FANART,'')

	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

def removeAddonDataMenuJUNK():
	if os.path.exists(ADDONDATA):
		Common.addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data', 'removedata', 'all', themeit=THEME2)
		Common.addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Addon_Data for Uninstalled Addons', 'removedata', 'uninstalled', themeit=THEME2)
		Common.addFile('[COLOR red][B][REMOVE][/B][/COLOR] All Empty Folders in Addon_Data', 'removedata', 'empty', themeit=THEME2)
		Common.addFile('[COLOR red][B][REMOVE][/B][/COLOR] %s Addon_Data' % ADDONTITLE, 'resetaddon', themeit=THEME2)
		Common.addFile(wiz.sep(), '', themeit=THEME3)
		fold = glob.glob(os.path.join(ADDONDATA, '*/'))
		for folder in sorted(fold, key = lambda x: x):
			foldername = folder.replace(ADDONDATA, '').replace('\\', '').replace('/', '')
			icon = os.path.join(folder.replace(ADDONDATA, ADDONS), 'icon.png')
			fanart = os.path.join(folder.replace(ADDONDATA, ADDONS), 'fanart.png')
			folderdisplay = foldername
			replace = {'audio.':'[COLOR orange][AUDIO] [/COLOR]', 'metadata.':'[COLOR cyan][METADATA] [/COLOR]', 'module.':'[COLOR orange][MODULE] [/COLOR]', 'plugin.':'[COLOR blue][PLUGIN] [/COLOR]', 'program.':'[COLOR orange][PROGRAM] [/COLOR]', 'repository.':'[COLOR gold][REPO] [/COLOR]', 'script.':'[COLOR green][SCRIPT] [/COLOR]', 'service.':'[COLOR green][SERVICE] [/COLOR]', 'skin.':'[COLOR dodgerblue][SKIN] [/COLOR]', 'video.':'[COLOR orange][VIDEO] [/COLOR]', 'weather.':'[COLOR yellow][WEATHER] [/COLOR]'}
			for rep in replace:
				folderdisplay = folderdisplay.replace(rep, replace[rep])
			if foldername in EXCLUDES: folderdisplay = '[COLOR green][B][PROTECTED][/B][/COLOR] %s' % folderdisplay
			else: 
				folderdisplay = '[COLOR red][B][REMOVE][/B][/COLOR] %s' % folderdisplay
			Common.addFile(' %s' % folderdisplay, 'removedata', foldername, icon=icon, fanart=fanart, themeit=THEME2)
	else:
		Common.addFile('No Addon data folder found.', '', themeit=THEME3)
	##setView('files', 'viewType')
	view_mode = SET_VIEW("list")
	xbmc.executebuiltin(view_mode)

##############################    END    #########################################

##################################################################################
#			Which mode to select
#######################################################################

TEMP_FOLDER =  xbmc.translatePath(os.path.join('special://profile/addon_data/' + ADDON_ID,'temp'))
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)
TEMP_FILE =  xbmc.translatePath(os.path.join(TEMP_FOLDER,'temp.xml'))
if not os.path.isfile(TEMP_FILE):
	open(TEMP_FILE, 'w')
    
params=parameters.get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
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
        mode2=urllib.unquote_plus(params["mode"])
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

if mode==None:
#if mode==None or url==None or len(url)<1:
        INDEX()
        
elif mode==1:
        #maintenance.clearCache()
        clearCache(); wiz.refresh()
        
elif mode==2:
        #maintenance.deleteThumbnails()
        clearThumb(); wiz.refresh()
        Common.killxbmc()

elif mode==3:
        #maintenance.purgePackages()
        wiz.clearPackages(); wiz.refresh()

elif mode==4:
        ACCOUNT()
        
elif mode==5:
        MAINTENANCE_MENU()

elif mode==6:        
        wipe.FRESHSTART()
        
elif mode==7:
        COMINGSOON()

elif mode==8:
        BACKUPMENU()
        
elif mode==9:
        OPEN_SETTINGS(params)
        
elif mode==10:
        maintenance.deleteAddonDB()

elif mode==11:
        update.updateaddons()
        
elif mode==12:
        xbmc.executebuiltin("RunAddon(plugin.program.nolimitstools)")
        
elif mode==13:
        maintenance.Fix_Special(url)

elif mode==14:
        versioncheck.XBMC_Version()
        
elif mode==15:
        speedtest.runtest(url)
        
elif mode==16:
        SPEEDTEST()

elif mode==17:
       ADD_COMMUNITY_BUILD()

elif mode==18:
       community.CommunityUpdateNotice()

elif mode==22:
        #GET_SUPPORT()
        pass

elif mode==25:
        #maintenance.DeleteCrashLogs()
        wiz.clearCrash(); wiz.refresh()
        
elif mode==26:
        maintenance.HidePasswords()

elif mode==27:
        maintenance.lib()

elif mode==28:
        LATEST_LIST()
    
elif mode==29:
        DOWNLOADLIB()
        
elif mode==30:
        ADVANCEDSETTINGS()
        
elif mode==31:
        #Auto Clean Cache, Packages, Thumbnails
        #maintenance.autocleanask()
        totalClean(); wiz.refresh()
        
elif mode==32:
        LATESTAPKSWITHLIB()
        
elif mode==33:
        update.check()

elif mode==35:
        maintenance.viewLogFile()
        
elif mode==36:
        uploadlog.main(argv=None)

elif mode==37:
        maintenance.UnhidePasswords()
        
elif mode==40:
        LATEST_WINDOWS()
        
elif mode==41:
        LATEST_ANDROID()
        
elif mode==42:
        LATEST_IOS()
        
elif mode==43:
        LATEST_OSX()

elif mode==44:
        versioncheck.BUILD_Version()

elif mode==46:
        KODI_TOOLS()

elif mode==47:
        SPORT_LISTINGS()
        
elif mode==49:
        dialog.ok(ADDONTITLE, url )

elif mode==50:
        BUILDMENU()

elif mode==58:
        Common.WriteReview(url)

elif mode==59:
        Common.ListReview(url)

elif mode==60:
        youtube.MAINMENU()
        
elif mode==61:
        youtube.LOADLIST(name,url)
        
elif mode==62:
        youtube.LOADITEM(name,url)
        
elif mode==63:
        youtube.OTHER_CHANNELS(url)
        
elif mode==64:
        search.YOUTUBE()
        
elif mode==65:
        search.COMMUNITY()
        
elif mode==66:
        search.BUILDS()
        
elif mode==67:
        search.ALL()

elif mode==69:
        backuprestore.FullBackup()

elif mode==70:
        backuprestore.Backup()
        
elif mode==71:
        backuprestore.Restore()
    
elif mode==72:
        backuprestore.ListBackDel()
        
elif mode==73:
        backuprestore.DeleteAllBackups()
        
elif mode==74:
        extras.EXTRAS_MENU()
        
elif mode==75:
        extras.HORUS_INTRO()
        
elif mode==76:
        extras.ENABLE_HORUS_INTRO()

elif mode==77:
        extras.SPMC_MINIMIZE()

elif mode==79:
        #GET_SUPPORT()
        pass
        
elif mode==80:
        VIEW_CHANGELOG()
        
elif mode==81:
        VIEW_CREDITS()

elif mode==82:
        maintenance.viewLogFile()

elif mode==83:
        Common.BUILDER(name,url,iconimage,fanart,description)

elif mode==84:
        KODI_CONTACTS()

elif mode==85:
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        Common.killxbmc()

elif mode==86:
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        Common.KillKodi()

elif mode==87:
        community.COMMUNITY()

elif mode==88:
        BUILDMENU()
    
elif mode==89:
        installer.INSTALLEXE(name,url,description)

elif mode==90:
        installer.INSTALL(name,url,description)
        
elif mode==91:
        installer.INSTALLAPK(name,url,description)

elif mode==92:
        status.Check()
        
elif mode==93:
        community.SHOWCOMMUNITYBUILDS(name, url, description)
     
elif mode==94:
        installer.INSTALLLIB(name,url,description)

elif mode==95:
        PLAYVIDEO(url)
        
elif mode==96:
        installer.INSTALL_COMMUNITY(name,url,description)
     
elif mode==97:
        Common.BUILDER_COMMUNITY(name,url,iconimage,fanart,description)

elif mode==98:
        installer.INSTALL_ADVANCED(name,url,description)

elif mode==99:
        installer.INSTALL(name,url,description)

elif mode==100:
        backuprestore.READ_ZIP(url)
    
elif mode==101:
        backuprestore.DeleteBackup(url)

elif mode==102:
        xbmc.executebuiltin(description)
        sys.exit(0)

elif mode==103:
        backuprestore.BACKUP_RD_TRAKT()

elif mode==104:
        backuprestore.RESTORE_RD_TRAKT()

elif mode==105:
        backuprestore.READ_ZIP_TRAKT(url)

elif mode==106:
        LATEST_NEWS()

elif mode==107:
        backuprestore.TV_GUIDE_BACKUP()
        
elif mode==108:
        backuprestore.ADDON_DATA_BACKUP()
        
elif mode==109:
        maintenance.RUYA_FIX()

elif mode==110:
        extras.PLAYERCORE_ANDROID()

elif mode==111:
        dialog.ok(ADDONTITLE, '[COLOR aqua][B]Current Time: [/B][/COLOR][COLOR white]' + THE_TIME + '[/COLOR]', '[COLOR aqua][B]Current Date: [/B][/COLOR][COLOR white]' + THE_DATE + '[/COLOR]')

elif mode==112:
        maintenance.AUTO_CLEAN_ON_OFF()

elif mode==113:
        maintenance.AUTO_WEEKLY_CLEAN_ON_OFF()

elif mode==114:
        xbmc.executebuiltin("Container.Refresh")

elif mode==115:
        extras.PLAYERCORE_WINDOWS()

elif mode==116:
        Common.SHOW_PICTURE(fanart)

elif mode==117:
        maintenance.BASE64_ENCODE_DECODE()

elif mode==118:
        Common.WriteTicket()

elif mode==119:
        Common.ListTickets()

elif mode==120:
        dialog.ok(ADDONTITLE, url )
        xbmc.executebuiltin("Container.Refresh")

elif mode==121:
        get_addons.MENU_MAIN()

elif mode==122:
        get_addons.GET_SINGLE(name,url)
        
elif mode==123:
        get_addons.GET_MULTI(name,url)

elif mode==124:
        xbmc.executebuiltin("ReloadSkin()")

elif mode==125:
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.executebuiltin("UpdateLocalAddons")
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        
elif mode==126:
        maintenance.OPEN_EXTERNAL_SETTINGS()

elif mode==127:
        xbmc.executebuiltin("ToggleDebug")

elif mode==128:
        REMOVE_KEYBOARD_FILE()

elif mode==129:
        KEYMAPS()

elif mode==130:
        installer.INSTALL_KEYMAP(name,url,description)

elif mode==131:
        REMOVE_ADVANCED_FILE()

elif mode==132:
        extras.YOUTUBE_REMOVE()
        
elif mode==140:
        community.NEXT_PAGE_COMMUNITY(description)
        
elif mode==141:
        community.PROTECTED_FOLDER()
        
elif mode==142:
        community.NEXT_PAGE_PROTECTED(description)
        
elif mode==143:
        community.SHOWPROTECTEDBUILDS(name,url,description)

elif mode==144:
        FANRIFFIC_THEMES()

elif mode==145:
        installer.INSTALL_FANRIFFIC(name,url,description)

elif mode==146:
        extras.SPORTS_DEVIL_FIX()
        
elif mode==147:
        maintenance.CHECK_BROKEN_REPOS()

elif mode==148:
        maintenance.CHECK_BROKEN_SOURCES()

elif mode==149:
        ANDROID_APKS()

elif mode==150:
        get_addons.GET_LIST(description)

elif mode==151:
        get_addons.GET_MULTI(name,url)

elif mode==152:
        dialog = xbmcgui.Dialog()
        dialog.ok(ADDONTITLE, '[COLOR white][B]Please contact Kodi KODENTV on Twitter: [/B][/COLOR]','[COLOR dodgerblue][B]@kodentv[/B][/COLOR]')

elif mode==153:
        dialog = xbmcgui.Dialog()
        dialog.ok(ADDONTITLE, '[COLOR white][B]To get an addon added to the installer we must have permission from the developer. If you would like to add an addon please ask them for permission and if granted contact Kodi KODENTV on twitter @kodentv to let us know. We will get the addon added ASAP. Thank you![/B][/COLOR]')

elif mode==154:
        maintenance.view_LastError()

elif mode==155:
        maintenance.view_Errors()

elif mode==156:
        get_addons.GET_PAID(name,url)

elif mode==157:
        dialog = xbmcgui.Dialog()
        dialog.ok(ADDONTITLE, '[COLOR white][B]COMING SOON! Please contact Kodi KODENTV on Twitter for more information: [/B][/COLOR]','[COLOR dodgerblue][B]@kodentv[/B][/COLOR]')

elif mode==158:
        extras.REMOVE_GUIDE()

elif mode==159:
        get_addons.PARENTAL_CONTROLS()

elif mode==160:
        get_addons.PARENTAL_CONTROLS_PIN()

elif mode==161:
        get_addons.PARENTAL_CONTROLS_OFF()

elif mode==162:
        AUTO_UPDATER(name)

elif mode==163:
        maintenance.GET_ADDON_STATS()

elif mode==164:
        get_addons.GET_REPO(name,url)

elif mode==165:
        AUTO_UPDATER("dialog")

elif mode==170:
        INSTALLER_APKS()

elif mode==171:
        installer.INSTALLAPK_INSTALLER(name,url,description)


elif mode==173:
        get_addons.FINISH()

elif mode==174:
        dp.create(ADDONTITLE)
        dp.update(0, "Updating installed addons, please wait.")
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.executebuiltin("UpdateLocalAddons")
        time.sleep(5)
        dp.close()
        dialog.ok(ADDONTITLE, "All local addons have been updated. Thank you for using KODENTV Tools!")
        sys.exit(0)

elif mode==175:
        get_addons.MENU_MAIN()
    
elif mode==176:
        get_addons.ADDON_DECIDE(name,url,iconimage,fanart)
        
elif mode==177:
        get_addons.FILE_MANAGER_SOURCES(name,url,description)

elif mode==178:
        get_addons.WRITE_SOURCE_TO_FILE_MANAGER(name,url)

elif mode==179:
        GETTEMP()
        
elif mode==180:
        CLEARTEMP()

elif mode==181:
        security.check()

elif mode==182:
        DISPLAY_INFORMATION(url)

elif mode==183:
        Common.multi_youtube_videos(url)

elif mode==184:
        REPO_SOURCE_CHECKER()

elif mode==185:
        GET_KODIAPPS_RANKING()

elif mode==186:
        GET_KODIAPPS_INFORMATION(name,url,iconimage)

elif mode==187:
        get_addons.GET_ADDON_DESCRIPTION(name,url,iconimage)

elif mode==188:
        purgeDb()

elif mode==189:
        #WIZLOG = xbmc.translatePath('special://home/kodi.log')
        f = open(WIZLOG, 'w')
        f.close()
        #wizardM.LogNotify("Wizard Log ", "Cleared!")
        wiz.LogNotify("Wizard Log ", "Cleared!")

elif mode==190:
        #notifyM.contact(CONTACT)
        notify.contact(CONTACT)

elif mode==191:
        #maintenance.removeAddon(name)
        ##removeAddon(name)
        removeAddonMenu()

elif mode==192:
        #maintenance.removeAddonData(name)
        ##removeAddonData(name)
        removeAddonDataMenu()

elif mode==193:        
        youtubefix()

elif mode==194:
        # Clear Week Old Thumbnails
        wiz.oldThumbs()

elif mode==195: 
        totalClean(); wiz.refresh()

elif mode==196: 
        enableAddons()

elif mode==197: 
        wiz.toggleAddon(name, url); wiz.refresh()

elif mode2=='toggleaddon': 
        wiz.toggleAddon(name, url); wiz.refresh()

elif mode==198:
        removeAddonData(name)
            
elif mode2=='removedata': 
        removeAddonData(name)
        
elif mode2=='resetaddon': 
        total = wiz.cleanHouse(ADDONDATA, ignore=True); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Wizard Addon_Data Reset![/COLOR]" % COLOR2)

elif mode==199:
        notify.autoConfig()

elif mode==200:
        wiz.asciiCheck()

elif mode==201:
        TRAKTMENU()
elif mode2=='trakt'          : traktMenu()
elif mode2=='savetrakt'      : traktit.traktIt('update',      name)
elif mode2=='restoretrakt'   : traktit.traktIt('restore',     name)
elif mode2=='addontrakt'     : traktit.traktIt('clearaddon',  name)
elif mode2=='cleartrakt'     : traktit.clearSaved(name)
elif mode2=='authtrakt'      : traktit.activateTrakt(name); wiz.refresh()
elif mode2=='updatetrakt'    : traktit.autoUpdate('all')
elif mode2=='importtrakt'    : traktit.importlist(name); wiz.refresh()

elif mode==202:
        DEBRIDMENU()

elif mode==203:
        debridit.debridIt('update',name)

elif mode2=='realdebrid'     : realMenu()
elif mode2=='savedebrid'     : debridit.debridIt('update',      name)
elif mode2=='restoredebrid'  : debridit.debridIt('restore',     name)
elif mode2=='addondebrid'    : debridit.debridIt('clearaddon',  name)
elif mode2=='cleardebrid'    : debridit.clearSaved(name)
elif mode2=='authdebrid'     : debridit.activateDebrid(name); wiz.refresh()
elif mode2=='updatedebrid'   : debridit.autoUpdate('all')
elif mode2=='importdebrid'   : debridit.importlist(name); wiz.refresh()

elif mode==204:
        maintenance.OPEN_RESOLVER_SETTINGS()

elif mode==205:
        maintenance.OPEN_SCRAPER_SETTINGS()

elif mode==206:
        DONATIONS_LINK1()

elif mode==207:
        DONATIONS_LINK2()

elif mode==208:
        DONATIONS_LINK3()

#if mode==None or url==None or len(url)<1:
if mode==None:
    xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=False)
else: xbmcplugin.endOfDirectory(int(sys.argv[1]),cacheToDisc=True)

