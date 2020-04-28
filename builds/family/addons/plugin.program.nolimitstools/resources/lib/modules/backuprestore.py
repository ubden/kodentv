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
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
from resources.lib.modules import extract
import time
from resources.lib.modules import downloader
from resources.lib.modules import plugintools
import zipfile
import ntpath
import base64
from resources.lib.modules import common as Common
from os import listdir
from os.path import isfile, join
from resources.lib.modules import parameters
from resources.lib.modules import wipe
from resources.lib.modules import skinSwitch
from shutil import copyfile

from resources.lib.modules import common as Common

base            = base64.b64decode(b"aHR0cDovL2VjaG9jb2Rlci5jb20v")
BASEURL         = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
ADDONTITLE      = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
ADDON_ID        = xbmcaddon.Addon().getAddonInfo('id') #'plugin.program.nolimitstools'
SELFADDON       = xbmcaddon.Addon(id=ADDON_ID)
backupfull      = SELFADDON.getSetting('backup_database')
backupaddons    = SELFADDON.getSetting('backup_addon_data')
PACKAGES        = xbmc.translatePath(os.path.join('special://home/addons/' + 'packages'))

dialog          = xbmcgui.Dialog()
dp              = xbmcgui.DialogProgress()
ICON            = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'icon.png'))
mastercopy      = SELFADDON.getSetting('mastercopy')
HOME            = xbmc.translatePath('special://home/')
USERDATA        = xbmc.translatePath(os.path.join('special://home/userdata',''))
zip             = plugintools.get_setting("zip")
USB             = xbmc.translatePath(os.path.join(zip))
HOME            = xbmc.translatePath('special://home/')
EXCLUDES_FOLDER = xbmc.translatePath(os.path.join(USERDATA,'BACKUP'))
ADDON_DATA      = xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
GUIDE           = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.program.echotvguide'))
#DEBRIDTRAKT_WEB = 'http://pastebin.com/raw/CU2PSGze'
DEBRIDTRAKT_WEB  = 'http://nolimitsbuilds.com/xmls/debridtrakt.txt'
#DEBRIDTRAKT_FILE = 'special://home/addons/plugin.program.nolimitstools/resources/files/debridtrakt.txt'
DEBRIDTRAKT_FILE = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/resources/files/debridtrakt.txt')

def check_path():

	if not "backupdir" in USB:
		if HOME in USB:
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE, "Invalid path selected for your backups. The path you have selected will be removed during backup and cause an error. Please pick another path that is not in the Kodi directory")
			plugintools.open_settings_dialog()
			sys.exit(0)
	if not os.path.exists(USB):
		try:
			os.makedirs(USB)
		except:
			dialog = xbmcgui.Dialog()
			dialog.ok(ADDONTITLE, "Invalid path selected for your backups. The directory specified does not exist or is not writable.")
			plugintools.open_settings_dialog()
			sys.exit(0)

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

def Backup():
    guisuccess=1
    check_path()
    if os.path.exists(PACKAGES):
        shutil.rmtree(PACKAGES)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'.zip'))
    exclude_dirs =  ['backupdir','cache', 'Thumbnails','temp','Databases']
    exclude_files = ["spmc.log","spmc.old.log","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db"]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def FullBackup():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'.zip'))
    exclude_dirs =  ['backupdir','cache','temp']
    exclude_files = ["spmc.log","spmc.old.log","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log"]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def TV_GUIDE_BACKUP():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_tv_guide.zip'))
    exclude_dirs =  ['']
    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    ARCHIVE_CB(GUIDE, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def ADDON_DATA_BACKUP():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_addon_data.zip'))
    exclude_dirs =  ['']
    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(ADDON_DATA)
    ARCHIVE_CB(ADDON_DATA, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def BACKUP_RD_TRAKT():

	if not os.path.exists(USB):
		os.makedirs(USB)
	vq = _get_keyboard( heading="Enter a name for this backup" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	backup_zip = xbmc.translatePath(os.path.join(USB,title+'RD_Trakt_Settings.zip'))

	if not os.path.exists(EXCLUDES_FOLDER):
		os.makedirs(EXCLUDES_FOLDER)

	### Open Web File
	#link=Common.OPEN_URL('http://pastebin.com/raw/CU2PSGze')
	#link=Common.OPEN_URL(DEBRIDTRAKT_WEB)

	### Open Local Text File
	f = open(DEBRIDTRAKT_FILE,'r')
	link = f.read(); f.close()
	#Common.TextBoxError('[COLOR aqua][B]No Limits Tools[/B][/COLOR]',link)

	plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
	for match in plugins:
		ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
		ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
		EXCLUDEMOVE = xbmc.translatePath(os.path.join(EXCLUDES_FOLDER,match+'_settings.xml'))
		dialog = xbmcgui.Dialog()

		try:
			if os.path.exists(ADDONSETTINGS):
				copyfile(ADDONSETTINGS, EXCLUDEMOVE)
		except: pass

	exclude_dirs =  [' ']
	exclude_files = [" "]
	message_header = "Creating full backup..."
	message_header2 = "Creating full backup..."
	message1 = "Archiving..."
	message2 = ""
	message3 = ""
	try:
		ARCHIVE_CB(EXCLUDES_FOLDER, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
	except: pass
	time.sleep(1)
	try:
		shutil.rmtree(EXCLUDEMOVE)
		shutil.rmdir(EXCLUDEMOVE)
	except: pass
	Common.REMOVE_EMPTY_FOLDERS()
	Common.REMOVE_EMPTY_FOLDERS()
	Common.REMOVE_EMPTY_FOLDERS()
	Common.REMOVE_EMPTY_FOLDERS()
	Common.REMOVE_EMPTY_FOLDERS()
	Common.REMOVE_EMPTY_FOLDERS()
	Common.REMOVE_EMPTY_FOLDERS()
	Common.REMOVE_EMPTY_FOLDERS()
	dialog.ok("[COLOR green][B]SUCCESS![/B][/COLOR]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def AUTO_BACKUP_RD_TRAKT():

	TMP_TRAKT     =  xbmc.translatePath(os.path.join(HOME,'tmp_trakt'))

	if not os.path.exists(TMP_TRAKT):
		os.makedirs(TMP_TRAKT)

	backup_zip = xbmc.translatePath(os.path.join(TMP_TRAKT,'Restore_RD_Trakt_Settings.zip'))

	if not os.path.exists(EXCLUDES_FOLDER):
		os.makedirs(EXCLUDES_FOLDER)

	link=Common.OPEN_URL('http://pastebin.com/raw/CU2PSGze')
	plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
	for match in plugins:
		try:
			ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
			ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
			EXCLUDEMOVE = xbmc.translatePath(os.path.join(EXCLUDES_FOLDER,match+'_settings.xml'))
			if os.path.exists(ADDONSETTINGS):
				copyfile(ADDONSETTINGS, EXCLUDEMOVE)
				found = 2
		except: pass

	if found == 2:
		exclude_dirs =  [' ']
		exclude_files = [" "]
		message_header = "Creating full backup..."
		message_header2 = "Creating full backup..."
		message1 = "Archiving..."
		message2 = ""
		message3 = ""
		ARCHIVE_CB(EXCLUDES_FOLDER, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
		time.sleep(1)
		try:
			shutil.rmtree(EXCLUDES_FOLDER)
			shutil.rmdir(EXCLUDES_FOLDER)
		except: pass
		MARKER_TRAKT = xbmc.translatePath(os.path.join(TMP_TRAKT,'marker.xml'))
		open(MARKER_TRAKT, 'w')

def RESTORE_RD_TRAKT():

	for file in os.listdir(USB):
		if file.endswith("RD_Trakt_Settings.zip"):
			url =  xbmc.translatePath(os.path.join(USB,file))
			Common.addItem(file,url,105,ICON,ICON,'')

def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
   
    try:
        zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(sourcefile)
        for_progress = []
        ITEM =[]
        dp.create(message_header, message1, message2, message3)
        for base, dirs, files in os.walk(sourcefile):
            for file in files:
                try:
                    ITEM.append(file)
                except: pass
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(sourcefile):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            files[:] = [f for f in files if f not in exclude_files]
            for file in files:
                try:
                    for_progress.append(file) 
                    progress = len(for_progress) / float(N_ITEM) * 100  
                    dp.update(int(progress),"Backing Up",'[COLOR yellowgreen]%s[/COLOR]'%file, '')
                    fn = os.path.join(base, file)
                    zipobj.write(fn, fn[rootlen:]) 
                except: pass
        zipobj.close()
        dp.close()
    except: pass

def FIX_SPECIAL(url):

    HOME =  xbmc.translatePath('special://home')
    dialog = xbmcgui.Dialog()
    dp.create(ADDONTITLE,"Renaming paths...",'', '')
    url = xbmc.translatePath('special://userdata')
    for root, dirs, files in os.walk(url):
        for file in files:
            try:
                if file.endswith(".xml"):
                    dp.update(0,"Fixing","[COLOR dodgerblue]" + file + "[/COLOR]", "Please wait.....")
                    a=open((os.path.join(root, file))).read()
                    b=a.replace(HOME, 'special://home/')
                    f= open((os.path.join(root, file)), mode='w')
                    f.write(str(b))
                    f.close()
            except: pass

def Restore():

	for file in os.listdir(USB):
		if file.endswith(".zip"):
			url =  xbmc.translatePath(os.path.join(USB,file))
			Common.addItem(file,url,100,ICON,ICON,'')
		

def READ_ZIP(url):

	if not "_addon_data" in url:
		if not "tv_guide" in url:
			if dialog.yesno(ADDONTITLE,"[COLOR smokewhite]" + url + "[/COLOR]","Do you want to restore this backup?"):
				skinswap()
				wipe.WIPE_BACKUPRESTORE()
				_out = xbmc.translatePath(os.path.join('special://','home'))
			else:
				sys.exit(1)
		else:
			if dialog.yesno(ADDONTITLE,"[COLOR smokewhite]" + url + "[/COLOR]","Do you want to restore this backup?"):
				_out = GUIDE
			else:
				sys.exit(1)
	else:
		if dialog.yesno(ADDONTITLE,"[COLOR smokewhite]" + url + "[/COLOR]","Do you want to restore this backup?"):
			_out = ADDON_DATA
		else:
			sys.exit(1)

	_in = url
	dp.create(ADDONTITLE,"Restoring File:",_in,'')
	unzip(_in, _out, dp)
	
	if not "addon_data" in url:
		if not "tv_guide" in url:
			dialog.ok(ADDONTITLE,'Restore Successful, please restart XBMC/Kodi for changes to take effect.','','')
			Common.killxbmc()
		else:
			dialog.ok(ADDONTITLE,'Your TDB TV Guide settings have been restored.','','')
	else:
		dialog.ok(ADDONTITLE,'Your Addon Data settings have been restored.','','')

def READ_ZIP_TRAKT(url):

	dialog = xbmcgui.Dialog()
	if dialog.yesno(ADDONTITLE,"[COLOR smokewhite]" + url + "[/COLOR]","Do you want to restore this backup?"):
		_out = xbmc.translatePath(os.path.join('special://','home/tmp'))
		_in = url
		dp.create(ADDONTITLE,"Restoring File:",_in,'')
		unzip(_in, _out, dp)
		name = "[COLOR ghostwhite][B]RESTORE[/B][/COLOR]"
		link=Common.OPEN_URL('http://pastebin.com/raw/CU2PSGze')
		plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
		for match in plugins:
			ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
			ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
			EXCLUDEMOVE = xbmc.translatePath(os.path.join(_out,match+'_settings.xml'))
			if os.path.exists(EXCLUDEMOVE):
				if not os.path.exists(ADDONPATH):
					os.makedirs(ADDONPATH)
				if os.path.isfile(ADDONSETTINGS):
					os.remove(ADDONSETTINGS)
				os.rename(EXCLUDEMOVE, ADDONSETTINGS)
				try:
					os.remove(EXCLUDEMOVE)
				except: pass
		dialog = xbmcgui.Dialog()
		dialog.ok(ADDONTITLE,'RD and Trakt Settings Successfully Restored','','')
	else:
		sys.exit(1)

def AUTO_READ_ZIP_TRAKT(url):

	dialog = xbmcgui.Dialog()
	_out = xbmc.translatePath(os.path.join('special://','home/tmp_trakt'))
	_in = url
	dp.create(ADDONTITLE,"Restoring File:",_in,'')
	unzip(_in, _out, dp)
	name = "[COLOR ghostwhite][B]RESTORE[/B][/COLOR]"
	link=Common.OPEN_URL('http://kodinolimits.com/other/rd_trakt.xml')
	plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
	for match in plugins:
		try:
			ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
			ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
			EXCLUDEMOVE = xbmc.translatePath(os.path.join(_out,match+'_settings.xml'))
			if os.path.isfile(EXCLUDEMOVE):
				if not os.path.exists(ADDONPATH):
					os.makedirs(ADDONPATH)
				if os.path.isfile(ADDONSETTINGS):
					os.remove(ADDONSETTINGS)
				try:
					os.rename(EXCLUDEMOVE, ADDONSETTINGS)
				except: pass
				try:
					os.remove(EXCLUDEMOVE)
				except: pass
		except: pass
	try:
		shutil.rmtree(_out)
		shutil.rmdir(_out)
	except: pass

def unzip(_in, _out, dp):
    zin    = zipfile.ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0

    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update),'','','[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
            try:
                zin.extract(item, _out)
            except Exception, e:
                print str(e)

    except Exception, e:
        print str(e)
        return False

    return True
		
def ListBackDel():
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	for file in os.listdir(USB):
		if file.endswith(".zip"):
			url =  xbmc.translatePath(os.path.join(USB,file))
			Common.addDir(file,url,101,ICON,ICON,'')
			
def DeleteBackup(url):
	if dialog.yesno(ADDONTITLE,"[COLOR smokewhite]" + url + "[/COLOR]","Do you want to delete this backup?"):
		os.remove(url)
		dialog.ok(ADDONTITLE,"[COLOR smokewhite]" + url + "[/COLOR]","Successfully deleted.")
		
def DeleteAllBackups():
	if dialog.yesno(ADDONTITLE,"Do you want to delete all backups?"):
		shutil.rmtree(USB)
		os.makedirs(USB)
		dialog.ok(ADDONTITLE,"All backups successfully deleted.")

def skinswap():

	skin         =  xbmc.getSkinDir()
	KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])
	skinswapped = 0

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
		choice = xbmcgui.Dialog().yesno(ADDONTITLE, '[COLOR lightskyblue][B]ERROR: AUTOSWITCH WAS NOT SUCCESFULL[/B][/COLOR]','[COLOR lightskyblue][B]CLICK YES TO MANUALLY SWITCH TO CONFLUENCE NOW[/B][/COLOR]','[COLOR lightskyblue][B]YOU CAN PRESS NO AND ATTEMPT THE AUTO SWITCH AGAIN IF YOU WISH[/B][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
		if choice == 1:
			xbmc.executebuiltin("ActivateWindow(appearancesettings)")
			return
		else:
			sys.exit(1)

##############################    END    #########################################