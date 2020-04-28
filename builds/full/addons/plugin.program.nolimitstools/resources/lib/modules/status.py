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
from resources.lib.modules import plugintools
import re
from resources.lib.modules import common as Common
from urllib import FancyURLopener

class MyOpener(FancyURLopener):
	version = 'TheWizardIsHere'

myopener = MyOpener()
urlretrieve = MyOpener().retrieve
urlopen = MyOpener().open

ADDONTITLE = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
BASEURL    = base64.b64decode(b"aHR0cDovL3RlYW10ZGJidWlsZHMuY28udWsv")
REPO       = BASEURL + base64.b64decode(b"cmVwb3NpdG9yeS9hZGRvbnMueG1s")
FORUM      = base64.b64decode(b"aHR0cDovL3RkYndpemFyZC5jby51ay9mb3J1bQ==")
COM        = BASEURL + base64.b64decode(b"Y29tbXVuaXR5L3dpemFyZHMudHh0")

def Check():

	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	codename = "Decline"
	
	if version >= 16.0 and version <= 16.9:
		codename = 'Jarvis'
	if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
		
	if codename == "Jarvis":
		TDB =  BASEURL + base64.b64decode(b"YnVpbGRzL3dpemFyZC93aXphcmRfcmVsX2phcnZpcy50eHQ=")
		LEETV =  BASEURL + base64.b64decode(b"YnVpbGRzL2xlZXR2L3dpemFyZF9yZWxfamFydmlzLnR4dA==")
		DONERIGHT =  BASEURL + base64.b64decode(b"YnVpbGRzL2RvbmVyaWdodC93aXphcmRfcmVsX2phcnZpcy50eHQ=")
		KODIHEAVEN =  BASEURL + base64.b64decode(b"YnVpbGRzL2tvZGloZWF2ZW4vd2l6YXJkX3JlbF9qYXJ2aXMudHh0")
		MYSTIC =  BASEURL + base64.b64decode(b"YnVpbGRzL215c3RpYy93aXphcmRfcmVsX2phcnZpcy50eHQ=")
		KIDDO =  BASEURL + base64.b64decode(b"YnVpbGRzL2tpZGRvL3dpemFyZF9yZWxfamFydmlzLnR4dA==")
		VULCAN =  BASEURL + base64.b64decode(b"YnVpbGRzL3Z1bGNhbi93aXphcmRfcmVsX2phcnZpcy50eHQ=")
		DEMONSTRATORZ =  BASEURL + base64.b64decode(b"YnVpbGRzL2RlbW9uc3RyYXRvcnovd2l6YXJkX3JlbF9qYXJ2aXMudHh0")
		GUIDE =  BASEURL + base64.b64decode(b"Z3VpZGUvZ3VpZGUuemlw")

	if codename == "Krypton":
		TDB =  BASEURL + base64.b64decode(b"YnVpbGRzL3dpemFyZC93aXphcmRfcmVsX2tyeXB0b24udHh0")
		LEETV =  BASEURL + base64.b64decode(b"YnVpbGRzL2xlZXR2L3dpemFyZF9yZWxfa3J5cHRvbi50eHQ=")
		DONERIGHT =  BASEURL + base64.b64decode(b"YnVpbGRzL2RvbmVyaWdodC93aXphcmRfcmVsX2tyeXB0b24udHh0")
		KODIHEAVEN =  BASEURL + base64.b64decode(b"YnVpbGRzL2tvZGloZWF2ZW4vd2l6YXJkX3JlbF9rcnlwdG9uLnR4dA==")
		MYSTIC =  BASEURL + base64.b64decode(b"YnVpbGRzL215c3RpYy93aXphcmRfcmVsX2tyeXB0b24udHh0")
		KIDDO =  BASEURL + base64.b64decode(b"YnVpbGRzL2tpZGRvL3dpemFyZF9yZWxfa3J5cHRvbi50eHQ=")
		VULCAN =  BASEURL + base64.b64decode(b"YnVpbGRzL3Z1bGNhbi93aXphcmRfcmVsX2tyeXB0b24udHh0")
		DEMONSTRATORZ =  BASEURL + base64.b64decode(b"YnVpbGRzL2RlbW9uc3RyYXRvcnovd2l6YXJkX3JlbF9rcnlwdG9uLnR4dA==")
		GUIDE =  BASEURL + base64.b64decode(b"Z3VpZGUvZ3VpZGUuemlw")

	if codename == "Decline":
		TDB =  BASEURL + base64.b64decode(b"YnVpbGRzL3dpemFyZC93aXphcmRfcmVsX2phcnZpcy50eHQ=")
		LEETV =  BASEURL + base64.b64decode(b"YnVpbGRzL2xlZXR2L3dpemFyZF9yZWxfamFydmlzLnR4dA==")
		DONERIGHT =  BASEURL + base64.b64decode(b"YnVpbGRzL2RvbmVyaWdodC93aXphcmRfcmVsX2phcnZpcy50eHQ=")
		KODIHEAVEN =  BASEURL + base64.b64decode(b"YnVpbGRzL2tvZGloZWF2ZW4vd2l6YXJkX3JlbF9qYXJ2aXMudHh0")
		MYSTIC =  BASEURL + base64.b64decode(b"YnVpbGRzL215c3RpYy93aXphcmRfcmVsX2phcnZpcy50eHQ=")
		KIDDO =  BASEURL + base64.b64decode(b"YnVpbGRzL2tpZGRvL3dpemFyZF9yZWxfamFydmlzLnR4dA==")
		VULCAN =  BASEURL + base64.b64decode(b"YnVpbGRzL3Z1bGNhbi93aXphcmRfcmVsX2phcnZpcy50eHQ=")
		DEMONSTRATORZ =  BASEURL + base64.b64decode(b"YnVpbGRzL2RlbW9uc3RyYXRvcnovd2l6YXJkX3JlbF9qYXJ2aXMudHh0")
		GUIDE =  BASEURL + base64.b64decode(b"Z3VpZGUvZ3VpZGUuemlw")

	RepoStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	ForumStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	CommunityStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	TDBStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	LeeTVStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	DoneRightStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	KodiHeavenStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	MysticStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	KiddoStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	VulcanStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	DemonstratorzStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"
	GuideStatus = "[COLOR yellowgreen]ONLINE[/COLOR]"

	dialog = xbmcgui.Dialog()

	xbmc.executebuiltin( "ActivateWindow(busydialog)" )

	try:
		response = urlopen(REPO)
	except:
		RepoStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
	
	try:
		response = urlopen(FORUM)
	except:
		ForumStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
	
	try:
		response = urlopen(COM)
	except:
		CommunityStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
	
	try:
		response = urlopen(TDB)
	except:
		TDBStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
	
	try:
		response = urlopen(LEETV)
	except:
		LeeTVStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
	
	try:
		response = urlopen(DONERIGHT)
	except:
		DoneRightStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
	
	try:
		response = urlopen(KODIHEAVEN)
	except:
		KodiHeavenStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
	
	try:
		response = urlopen(MYSTIC)
	except:
		MysticStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
		
	try:
		response = urlopen(KIDDO)
	except:
		KiddoStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"
		
	try:
		response = urlopen(VULCAN)
	except:
		VulcanStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"

	try:
		response = urlopen(DEMONSTRATORZ)
	except:
		DemonstratorzStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"

	try:
		response = urlopen(GUIDE)
	except:
		GuideStatus = "[COLOR lightskyblue]OFFLINE[/COLOR]"

	xbmc.executebuiltin( "Dialog.Close(busydialog)" ) 

	dialog.ok(ADDONTITLE + " - Page 1 of 4","[COLOR lightsteelblue]TDB TV Guide: " + GuideStatus ,"TDB Wizard Builds: " + TDBStatus ,"LeeTV Builds: " + LeeTVStatus)
	dialog.ok(ADDONTITLE + " - Page 2 of 4","[COLOR lightsteelblue]Kodi Heaven Builds: " + KodiHeavenStatus ,"Mystic Builds: " + MysticStatus, "Kiddo Builds: " + KiddoStatus)
	dialog.ok(ADDONTITLE + " - Page 3 of 4","[COLOR lightsteelblue]Vulcan Builds: " + VulcanStatus, "Done Right Builds: " + DoneRightStatus, "Demonstratorz Builds: " + DemonstratorzStatus)
	dialog.ok(ADDONTITLE + " - Page 4 of 4","[COLOR lightsteelblue]Repository: " + RepoStatus ,"TDB Forum: " + ForumStatus, "3rd Party Builds: " + CommunityStatus)