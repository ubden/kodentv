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
import shutil
import urllib2,urllib
import re
import glob
import requests
from resources.lib.modules import common as Common
from resources.lib.modules import downloader
from resources.lib.modules import extract
import time
import os
from resources.lib.modules import installer
from resources.lib.modules import plugintools
#from resources.lib.modules import wizardM as wiz
from resources.lib.modules import wizard as wiz

ADDONTITLE     = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id') #'plugin.program.nolimitstools'
THUMBNAILPATH  = xbmc.translatePath('special://userdata/Thumbnails');
CACHEPATH      = os.path.join(xbmc.translatePath('special://home'), 'cache')
TEMPPATH       = os.path.join(xbmc.translatePath('special://home'), 'temp')
ADDONPATH      = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.program.nolimitstools')
MEDIAPATH      = os.path.join(ADDONPATH, 'resources/art')
ADDONS         = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'))
FANART         = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID , 'fanart.jpg'))
DATABASEPATH   = xbmc.translatePath('special://userdata/Database')
ICON           = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'icon.png'))
USERDATA       = xbmc.translatePath('special://userdata/')
ADDONDATA      = xbmc.translatePath('special://userdata/addon_data')
MAINTTITLE     = "[COLOR aqua]NO LIMITS[/COLOR] [COLOR white]Maintenance Tools[/COLOR]"
EXCLUDES       = ['plugin.program.nolimitstools','plugin.video.nolimitswizard','script.module.requests','temp','kodi.log','kodi.log.old','spmc.log','spmc.log.old','dbmc.log','dbmc.log.old']
dp             = xbmcgui.DialogProgress()
WINDOWS        = xbmc.translatePath('special://home')
WINDOWSCACHE   = xbmc.translatePath('special://home')
OTHERCACHE     = os.path.join(xbmc.translatePath('special://home'), 'temp')
dialog         = xbmcgui.Dialog()
BASEURL        = base64.b64decode(b'aHR0cDovL3RkYnJlcG8uY29tLw==')
KODIVERSION    = float(xbmc.getInfoLabel("System.BuildVersion")[:4])

#######################################################################
#                       Cache Functions
#######################################################################

class Gui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.header = kwargs.get("header")
        self.content = kwargs.get("content")

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.content)

path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi   

#######################################################################
#                       Maintenance Functions
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
                    "special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

#######################################################################
#                       Purge DB
#######################################################################
def purgeDb():
	DB = []
	display = []
	DIALOG = xbmcgui.Dialog()
	for dirpath, dirnames, files in os.walk(HOME):
		for f in fnmatch.filter(files, '*.db'):
			if f != 'Thumbs.db':
				found = os.path.join(dirpath, f)
				DB.append(found)
				dir = found.replace('\\', '/').split('/')
				display.append('(%s) %s' % (dir[len(dir)-2], dir[len(dir)-1]))
	if KODIVERSION >= 16: 
		choice = DIALOG.multiselect("Select DB File to Purge", display)
		if choice == None: wiz.LogNotify("Purge Database", "Cancelled")
		elif len(choice) == 0: wiz.LogNotify("Purge Database", "Cancelled")
		else: 
			for purge in choice: wiz.purgeDb(DB[purge])
	else:
		choice = DIALOG.select("Select DB File to Purge", display)
		if choice == -1: wiz.LogNotify("Purge Database", "Cancelled")
		else: wiz.purgeDb(DB[purge])

#######################################################################
#                       Clear Cache
#######################################################################

def clearCache():
    if os.path.exists(CACHEPATH)==True:    
        for root, dirs, files in os.walk(CACHEPATH):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(TEMPPATH)==True:    
        for root, dirs, files in os.walk(TEMPPATH):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno(MAINTTITLE,str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            try:
                                if (f.endswith(".log")): continue
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
                        for d in dirs:
                            try:
                                checker = (os.path.join(root, d))
                                if not "archive_cache" in str(checker):
                                    shutil.rmtree(os.path.join(root, d))
                            except:
                                pass
                            
                else:
                    pass
                

    dialog = xbmcgui.Dialog()
    dialog.ok(MAINTTITLE, "Done Clearing Cache files")
    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#                       Delete AddonDB
#######################################################################
    
def deleteAddonDB():
    dialog = xbmcgui.Dialog()
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])

    if version >= 17.0 and version <= 17.9:
        codename = 'Krypton'
    else:
        codename = 'Pass'
    
    if codename == "Pass":
        try:
            for root, dirs, files in os.walk(DATABASEPATH,topdown=True):
                dirs[:] = [d for d in dirs]
                for name in files:
                    if "addons" in name.lower():
                        try:
                            os.remove(os.path.join(root,name))
                            dialog.ok(MAINTTITLE,str(name)+  "removed!",'','[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
                        except: 
                            dialog.ok(MAINTTITLE,'Error Removing ' + str(name),'','[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')
                            pass
                    else:
                        continue
        except:
            pass
    else:
        dialog.ok(MAINTTITLE,'This feature is not available in Kodi 17 Krypton','','[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]')

#######################################################################
#                       Delete Thumbnails
#######################################################################

def deleteThumbnails():
    if os.path.exists(THUMBNAILPATH)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
                for root, dirs, files in os.walk(THUMBNAILPATH):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
    else:
        pass
    
    text13 = os.path.join(DATABASEPATH,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass

    dialog.ok(MAINTTITLE, 'Thumbnails have been deleted.','')
    xbmc.executebuiltin("Container.Refresh")

    Common.killxbmc()


def GET_ADDON_STATS():
    dp.create(ADDONTITLE,'Counting total addons installed')
    dp.update(0)
    i=0
    for item in os.listdir(ADDONS):
        i=i+1
    Common.addItem('[COLOR white]Total Addons = [/COLOR][COLOR aqua]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(10,'[COLOR white]Counting the installed video addons.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "video" in item.lower():
            i=i+1
    Common.addItem('[COLOR white]Video Addons = [/COLOR][COLOR aqua]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(20,'[COLOR white]Counting the installed program addons.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "program" in item.lower():
            i=i+1
    Common.addItem('[COLOR white]Program Addons = [/COLOR][COLOR aqua]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(30,'[COLOR white]Counting the installed music addons.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "music" in item.lower():
            i=i+1
    Common.addItem('[COLOR white]Music Addons = [/COLOR][COLOR aqua]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(40,'[COLOR white]Counting the installed image addons.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):

        if "image" in item.lower():
            i=i+1
    Common.addItem('[COLOR white]Picture Addons = [/COLOR][COLOR aqua]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(50,'[COLOR white]Counting the installed scripts.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "script" in item.lower():
            i=i+1
    Common.addItem('[COLOR white]Scripts = [/COLOR][COLOR aqua]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(55,'[COLOR white]Counting the installed skins.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "skin" in item.lower():
            i=i+1
    Common.addItem('[COLOR white]Skins = [/COLOR][COLOR aqua]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')


    dp.update(60,'[COLOR white]Counting the installed repositories.[/COLOR]')
    i=0
    for root, dirs, files in os.walk(ADDONS,topdown=True):
        dirs[:] = [d for d in dirs]
        for name in dirs:
            if "repo" in name.lower():
                i=i+1
    Common.addItem('[COLOR white]Repositories = [/COLOR][COLOR aqua]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    dp.update(70,'[COLOR white]Finding which version of Kodi is installed.[/COLOR]')
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

    dp.update(80,'[COLOR white]Getting your IP address.[/COLOR]')
    f = urllib.urlopen("http://www.canyouseeme.org/")
    html_doc = f.read()
    f.close()
    m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    check = plugintools.get_setting("checkaddonupdates")
    check_build = plugintools.get_setting("checkupdates")

    dp.update(90,'[COLOR white]Getting your update preferences.[/COLOR]')
    if check=="true":
        a = "[COLOR aqua]Yes[/COLOR]"
    else:
        a = "[COLOR lightskyblue]No[/COLOR]"
    if check_build=="true":
        b = "[COLOR aqua]Yes[/COLOR]"
    else:
        b = "[COLOR lightskyblue]No[/COLOR]"
    Common.addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR aqua]%s' % version + " " + codename + "[/COLOR]",BASEURL,200,ICON,FANART,'')
    Common.addItem('[COLOR ghostwhite]Check For Updates on Start: [/COLOR]' + a,BASEURL,200,ICON,FANART,'')
    Common.addItem('[COLOR ghostwhite]Check For Build Updates on Kodi launch: [/COLOR]' + b,BASEURL,200,ICON,FANART,'')
    Common.addItem('[COLOR ghostwhite]Local IP: [/COLOR][COLOR aqua]' + s.getsockname()[0] + '[/COLOR]',BASEURL,200,ICON,FANART,'')
    Common.addItem('[COLOR ghostwhite]External IP: [/COLOR][COLOR aqua]' + m.group(0) + '[/COLOR]',BASEURL,200,ICON,FANART,'')

    dp.update(100)
    dp.close()
    xbmc.executebuiltin('Container.SetViewMode(50)')

def CHECK_BROKEN_SOURCES():
    dialog = xbmcgui.Dialog()
    SOURCES_FILE =  xbmc.translatePath('special://home/userdata/sources.xml')

    if not os.path.isfile(SOURCES_FILE):
        dialog.ok(ADDONTITLE,'[COLOR red][B]Error: It appears you do not currently have a sources.xml file on your system. We are unable to perform this test.[/B][/COLOR]')
        sys.exit(0)

    dp.create(ADDONTITLE,"Testing Internet Connection...",'', 'Please Wait...') 

    try:
        Common.OPEN_URL_NORMAL("http://www.google.com")
    except:
        dialog.ok(ADDONTITLE,'[COLOR red][B]Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.[/B][/COLOR]')
        sys.exit(0)
    found = 0
    passed = 0
    dp.update(0,"Checking Sources...",'', 'Please Wait...') 
    a=open(SOURCES_FILE).read() 
    b=a.replace('\n','U').replace('\r','F')
    match=re.compile('<source>(.+?)</source>').findall(str(b))
    counter = 0
    try:
        for item in match:
            name=re.compile('<name>(.+?)</name>').findall(item)[0]
            checker=re.compile('<path pathversion="1">(.+?)</path>').findall(item)[0]
            if "http" in str(checker):
                dp.update(0,"","[COLOR aqua][B]Checking: " + name + "[/B][/COLOR]", "")
                try:
                    checkme = requests.get(checker)
                except:
                    checkme = "null"
                    pass
                try:
                    error_out = 0
                    if not "this does not matter its just a test" in ("%s" % checkme.text):
                        error_out = 0
                except:
                    error_out = 1

                if error_out == 0:
                    if not ".zip" in ("%s" % checkme.text):     
                        if not "repo" in ("%s" % checkme.text):
                            if not "<title>Index of /</title>" in ("%s" % checkme.text):
                                choice = dialog.select("[COLOR red][B]Error connecting to " + name + " (" + checker + ")[/B][/COLOR]", ['[COLOR lightskyblue][B]Edit the source URL.[/B][/COLOR]','[COLOR lightskyblue][B]Remove the source.[/B][/COLOR]','[COLOR lightskyblue][B]Do Nothing (Leave the source)[/B][/COLOR]'])
                                if choice == 0:
                                    found = 1
                                    counter = counter + 1
                                    string =''
                                    keyboard = xbmc.Keyboard(string, 'Enter New Source URL')
                                    keyboard.doModal()
                                    if keyboard.isConfirmed():
                                        string = keyboard.getText().replace(' ','')
                                    if len(string)>1:
                                        if not "http://" in string:
                                            if not "htts://" in string:
                                                string = "http://" + string
                                        h=open(SOURCES_FILE).read()
                                        i=h.replace('\n','U').replace('\r','F')
                                        j=i.replace(str(checker), str(string))
                                        k=j.replace('U','\n').replace('F','\r')
                                        f= open(SOURCES_FILE, mode='w')
                                        f.write(k)
                                        f.close()
                                    else: quit()
                                elif choice == 1:
                                    found = 1
                                    counter = counter + 1
                                    h=open(SOURCES_FILE).read()
                                    i=h.replace('\n','U').replace('\r','F')
                                    j=i.replace(str(item), '')
                                    k=j.replace('U','\n').replace('F','\r')
                                    l=k.replace('<source></source>','').replace('        \n','')
                                    f= open(SOURCES_FILE, mode='w')
                                    f.write(l)
                                    f.close()
                                else:
                                    found = 1
                                    counter = counter + 1
                            else:
                                passed = passed + 1
                        else:
                            passed = passed + 1
                    else:
                        passed = passed + 1
                else:
                    choice = dialog.select("[COLOR red][B]Error connecting to " + name + " (" + checker + ")[/B][/COLOR]", ['[COLOR lightskyblue][B]Edit the source URL.[/B][/COLOR]','[COLOR lightskyblue][B]Remove the source.[/B][/COLOR]','[COLOR lightskyblue][B]Do Nothing (Leave the source)[/B][/COLOR]'])
                    if choice == 0:
                        found = 1
                        counter = counter + 1
                        string =''
                        keyboard = xbmc.Keyboard(string, 'Enter New Source URL')
                        keyboard.doModal()
                        if keyboard.isConfirmed():
                            string = keyboard.getText().replace(' ','')
                        if len(string)>1:
                            if not "http://" in string:
                                if not "htts://" in string:
                                    string = "http://" + string
                            h=open(SOURCES_FILE).read()
                            i=h.replace('\n','U').replace('\r','F')
                            j=i.replace(str(checker), str(string))
                            k=j.replace('U','\n').replace('F','\r')
                            f= open(SOURCES_FILE, mode='w')
                            f.write(k)
                            f.close()
                        else: quit()
                    elif choice == 1:
                        found = 1
                        counter = counter + 1
                        h=open(SOURCES_FILE).read()
                        i=h.replace('\n','U').replace('\r','F')
                        j=i.replace(str(item), '')
                        k=j.replace('U','\n').replace('F','\r')
                        l=k.replace('<source></source>','').replace('        \n','')
                        f= open(SOURCES_FILE, mode='w')
                        f.write(l)
                        f.close()
                    else:
                        found = 1
                        counter = counter + 1
            dp.update(0,"","","[COLOR blue][B]Alive: " + str(passed) + "[/B][/COLOR][COLOR red][B]        Dead: " + str(counter) + "[/B][/COLOR]")
            if dp.iscanceled():
                dialog.ok(ADDONTITLE, 'The source check was cancelled')
                dp.close()
                quit()
    except:
        dialog.ok(ADDONTITLE, "Sorry we could not perform this test on your device.")
        dp.close()
        quit()


    dialog.ok(ADDONTITLE,'[COLOR white]We have checked your sources and found:[/COLOR]', '[COLOR aqua][B]WORKING SOURCES: ' + str(passed) + ' [/B][/COLOR]','[COLOR red][B]DEAD SOURCES: ' + str(counter) + ' [/B][/COLOR]')


def CHECK_BROKEN_REPOS():
    dialog = xbmcgui.Dialog()

    dp.create(ADDONTITLE,"Testing Internet Connection...",'', 'Please Wait...') 

    try:
        Common.OPEN_URL_NORMAL("http://www.google.com")
    except:
        dialog.ok(ADDONTITLE,'[COLOR red][B]Error: It appears you do not currently have an active internet connection. This will cause false positives in the test. Please try again with an active internet connection.[/B][/COLOR]')
        sys.exit(0)
    passed = 0
    failed = 0
    HOME =  xbmc.translatePath('special://home/addons/')
    dp.update(0,"[COLOR aqua][B]We are currently checking:[/B][/COLOR]",'',"[COLOR aqua][B]Alive: 0[/B][/COLOR][COLOR red][B]        Dead: 0[/B][/COLOR]")
    url = HOME
    for root, dirs, files in os.walk(url):
        for file in files:
            if file == "addon.xml":
                a=open((os.path.join(root, file))).read()   
                if "info compressed=" in str(a):
                    match = re.compile('<info compressed="false">(.+?)</info>').findall(a)
                    for checker in match:
                        dp.update(0,"","[COLOR aqua][B]" + checker + "[/B][/COLOR]", "")
                        try:
                            Common.OPEN_URL_NORMAL(checker)
                            passed = passed + 1
                        except:
                            try:
                                checkme = requests.get(checker)
                            except:
                                pass
                        
                            try:
                                error_out = 0
                                if not "this does not matter its just a test" in ("%s" % checkme.text):
                                    error_out = 0
                            except:
                                error_out = 1

                            if error_out == 0:
                                if not "addon id=" in ("%s" % checkme.text):    
                                    failed = failed + 1
                                    match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
                                    for repo_id,repo_name in match:
                                        dialog = xbmcgui.Dialog()
                                        default_path = xbmc.translatePath("special://home/addons/")
                                        file_path = xbmc.translatePath(file)
                                        full_path = default_path + repo_id
                                        choice = xbmcgui.Dialog().yesno(ADDONTITLE,"[COLOR white]The [/COLOR][COLOR aqua]" + repo_name + "[/COLOR] [COLOR white] appears to be broken. We attempted to connect to the repo but it was unsuccessful.[/COLOR]",'[COLOR red]To remove this repository please click YES[/COLOR]',yeslabel='[B][COLOR aqua]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
                                        if choice == 1:
                                            try:
                                                shutil.rmtree(full_path)
                                            except:
                                                dialog.ok(ADDONTITLE,"[COLOR white]Sorry we were unable to remove " + repo_name + "[/COLOR]")
                                else:
                                    passed = passed + 1
                            else:
                                failed = failed + 1
                                match = re.compile('<addon id="(.+?)".+?ame="(.+?)" version').findall(a)
                                for repo_id,repo_name in match:
                                    dialog = xbmcgui.Dialog()
                                    default_path = xbmc.translatePath("special://home/addons/")
                                    file_path = xbmc.translatePath(file)
                                    full_path = default_path + repo_id
                                    choice = xbmcgui.Dialog().yesno(ADDONTITLE,"[COLOR white]The [/COLOR][COLOR aqua]" + repo_name + "[/COLOR] [COLOR white] appears to be broken. We attempted to connect to the repo but it was unsuccessful.[/COLOR]",'[COLOR red]To remove this repository please click YES[/COLOR]',yeslabel='[B][COLOR aqua]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
                                    if choice == 1:
                                        try:
                                            shutil.rmtree(full_path)
                                        except:
                                            dialog.ok(ADDONTITLE,"[COLOR white]Sorry we were unable to remove " + repo_name + "[/COLOR]")
            
                        if dp.iscanceled():
                            dialog = xbmcgui.Dialog()
                            dialog.ok(ADDONTITLE, 'The repository check was cancelled')
                            dp.close()
                            sys.exit()
                        dp.update(0,"","","[COLOR aqua][B]Alive: " + str(passed) + "[/B][/COLOR][COLOR red][B]        Dead: " + str(failed) + "[/B][/COLOR]")
                        
    dialog.ok(ADDONTITLE,'[COLOR white]We have checked your repositories and found:[/COLOR]', '[COLOR aqua][B]WORKING SOURCES: ' + str(passed) + ' [/B][/COLOR]','[COLOR red][B]DEAD SOURCES: ' + str(failed) + ' [/B][/COLOR]')

#######################################################################
#                       Purge Packages
#######################################################################

def purgePackages():
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    if dialog.yesno("Delete Package Cache Files", "%d packages found."%file_count, "Delete Them?"):  
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                try:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                except: pass
                dialog = xbmcgui.Dialog()
                dialog.ok(MAINTTITLE, "Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok(MAINTTITLE, "No Packages to Purge")

    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#                       Convert physical to special
####################################################################### 

def Fix_Special(url):
    HOME =  xbmc.translatePath('special://home')
    dialog = xbmcgui.Dialog()
    dp.create(ADDONTITLE,"Renaming paths...",'', '')
    url = xbmc.translatePath('special://userdata')
    try:
        for root, dirs, files in os.walk(url):
            for file in files:
                if file.endswith(".xml"):
                     dp.update(0,"Fixing","[COLOR aqua]" + file + "[/COLOR]", "Please wait.....")
                     a=open((os.path.join(root, file))).read()
                     b=a.replace(HOME, 'special://home/')
                     f= open((os.path.join(root, file)), mode='w')
                     f.write(str(b))
                     f.close()
    except: pass

    dialog.ok(MAINTTITLE, "All physical paths have been converted to special","To complete this process you must force close Kodi now!")
    Common.KillKodi()

#######################################################################
#                       Autoclean Function
#######################################################################

def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
                    "special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries

#######################################################################
#                       Delete Crash Log Function
#######################################################################

def DeleteCrashLogs():  
    HomeDir = xbmc.translatePath('special://home')
    WINDOWSCACHE = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OTHERCACHE = xbmc.translatePath('special://temp')
    
    if os.path.exists(HomeDir)==True:   
        dialog = xbmcgui.Dialog()
        if dialog.yesno(MAINTTITLE, '', "Do you want to delete old crash logs?"):
            path=WINDOWS
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)
                
        if os.path.exists(WINDOWSCACHE)==True:   
            path=WINDOWSCACHE
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

        if os.path.exists(OTHERCACHE)==True:   
            path=OTHERCACHE
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)
        
        dialog = xbmcgui.Dialog()
        dialog.ok(MAINTTITLE, "Crash logs deleted", "[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]")
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok(MAINTTITLE, "An error occured", "[COLOR smokewhite]Please report this to No Limits Tools[/COLOR]")

def HidePasswords():
    dialog = xbmcgui.Dialog()
    HOME         =  xbmc.translatePath('special://home')
    if dialog.yesno(MAINTTITLE, "Are You Sure You Want To Hide Passwords?", ""):
        dialog = xbmcgui.Dialog()
        dp.create(MAINTTITLE,"Renaming paths...",'', 'Please Wait')
        for root, dirs, files in os.walk(HOME):
            for f in files:
                if f == "settings.xml":
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if not 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('/',' option="hidden"/') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:pass
            
        dialog.ok(MAINTTITLE, "All Passowrds are now hidden!", "[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]") 
        
                                            
def UnhidePasswords():
    dialog = xbmcgui.Dialog()
    HOME         =  xbmc.translatePath('special://home')
    if dialog.yesno(MAINTTITLE, "Are You Sure You Want To Make All Passwords Visable?", ""):
        dialog = xbmcgui.Dialog()
        dp.create(MAINTTITLE,"Renaming paths...",'', 'Please Wait')
        for root, dirs, files in os.walk(HOME):
            for f in files:
                if f == "settings.xml":
                    FILE=open(os.path.join(root, f)).read()
                    match=re.compile('<setting id=(.+?)>').findall (FILE)
                    for LINE in match:
                        if 'pass' in LINE:
                            if 'option="hidden"' in LINE:
                                try:
                                    CHANGEME=LINE.replace('option="hidden"','') 
                                    f = open(os.path.join(root, f), mode='w')
                                    f.write(str(FILE).replace(LINE,CHANGEME))
                                    f.close()
                                except:pass
            
        dialog.ok(MAINTTITLE, "All Passowrds are now visable!", "[COLOR smokewhite]Thank you for using No Limits Tools[/COLOR]") 

        
def view_LastError():
    CACHEPATH = os.path.join(xbmc.translatePath('special://home'), 'cache')
    TEMPPATH = os.path.join(xbmc.translatePath('special://home'), 'temp')
    WINDOWSCACHE = xbmc.translatePath('special://home')
    found = 0
    get_log = 0

    if os.path.exists(TEMPPATH):
        for root, dirs, files in os.walk(TEMPPATH,topdown=True):
            dirs[:] = [d for d in dirs]
            for name in files:
                if ".old.log" not in name.lower():
                    if ".log" in name.lower():
                        got_log = 1
                        a=open((os.path.join(root, name))).read()   
                        b=a.replace('\n','NEW_L').replace('\r','NEW_R')
                        match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
                        for checker in match:
                            found = 1
                            THE_ERROR = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n" + checker + '\n'
                        if found == 0:
                            dialog.ok(MAINTTITLE,'Great news! We did not find any errors in your log.')
                        else:
                            c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
                            Common.TextBoxError('[COLOR aqua][B]No Limits Tools - ERRORS[/B][/COLOR]',"%s" % c)
                            sys.exit(0)

    if os.path.exists(WINDOWSCACHE):
        for root, dirs, files in os.walk(WINDOWSCACHE,topdown=True):
            dirs[:] = [d for d in dirs]
            for name in files:
                if ".old.log" not in name.lower():
                    if ".log" in name.lower():
                        got_log = 1
                        a=open((os.path.join(root, name))).read()   
                        b=a.replace('\n','NEW_L').replace('\r','NEW_R')
                        match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
                        for checker in match:
                            found = 1
                            THE_ERROR = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n" + checker + '\n'
                        if found == 0:
                            dialog.ok(MAINTTITLE,'Great news! We did not find any errors in your log.')
                        else:
                            c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
                            Common.TextBoxError('[COLOR aqua][B]No Limits Tools - ERRORS[/B][/COLOR]',"%s" % c)
                            sys.exit(0)
    if got_log == 0:
        dialog.ok(MAINTTITLE,'Sorry we could not find a log file on your system')

def grab_Log(file=False, old=False):
    LOG = xbmc.translatePath('special://logpath/')
    finalfile   = 0
    logfilepath = os.listdir(LOG)
    logsfound   = []

    for item in logfilepath:
        if old == True and item.endswith('.old.log'): logsfound.append(os.path.join(LOG, item))
        elif old == False and item.endswith('.log') and not item.endswith('.old.log'): logsfound.append(os.path.join(LOG, item))

    if len(logsfound) > 0:
        logsfound.sort(key=lambda f: os.path.getmtime(f))
        if file == True: return logsfound[-1]
        else:
            filename    = open(logsfound[-1], 'r')
            logtext     = filename.read()
            filename.close()
            return logtext
    else: 
        return False

def errorList(file):
    errors = []
    a=open(file).read()
    b=a.replace('\n','NEW_L').replace('\r','NEW_R')
    match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
    for item in match:
        errors.append(item)
    return errors

def view_LastError():
    curr = grab_Log(True, False)
    old = grab_Log(True, True)
    errors = []; error1 = []; error2 = [];
    if not old == False: 
        error2 = errorList(old)
        if len(error2) > 0: 
            for item in error2: errors.append(item)
    if not curr == False: 
        error1 = errorList(curr)
        if len(error1) > 0: 
            for item in error1: errors.append(item)
    if len(errors) > 0:
        msg = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n%s" % (str(errors[-1]).replace('NEW_L','\n').replace('NEW_R','\r'))
        Common.TextBoxError('[COLOR aqua][B]No Limits Tools - ERRORS[/B][/COLOR]',msg)
    else: 
        dialog.ok(MAINTTITLE,'Great news! We did not find any errors in your log.')

def view_Errors():
    curr = grab_Log(True, False)
    old = grab_Log(True, True)
    errors = []; error1 = []; error2 = [];
    if old == False and curr == False:
        dialog.ok(MAINTTITLE, 'Sorry we where unable to find a log file.')
    if not curr == False: 
        error1 = errorList(curr)
    if not old == False: 
        error2 = errorList(old)
    
    
    if len(error2) > 0: 
        for item in error2: errors = [item] + errors
    if len(error1) > 0: 
        for item in error1: errors = [item] + errors

    if len(errors) > 0:
        i = 0; string = ''
        for item in errors:
            i += 1
            string += "[B][COLOR red]ERROR NUMBER %s[/B][/COLOR]\n\n%s\n" % (str(i), item)
        Common.TextBoxError('[COLOR aqua][B]No Limits Tools - ERRORS[/B][/COLOR]',string.replace('NEW_L','\n').replace('NEW_R','\r'))
    else:
        dialog.ok(MAINTTITLE,'Great news! We did not find any errors in your log.')

def viewLogFile():
    LOG = xbmc.translatePath('special://logpath/')
    finalfile   = 0
    gotold = 0
    logfilepath = os.listdir(LOG)
    logsfound_old       = []
    logsfound_current   = []

    for item in logfilepath:
        if item.endswith('.old.log'): 
            logsfound_old.append(os.path.join(LOG, item))
            name_old = item
            gotold = 1
        elif item.endswith('.log'):
            name_current = item
            logsfound_current.append(os.path.join(LOG, item))

    if len(logsfound_old) > 0:
        choice = xbmcgui.Dialog().yesno(MAINTTITLE, '[COLOR white]Found: [/COLOR]' + '[COLOR aqua][B]' + str(name_current) + ' (CURRENT)[/B][/COLOR]','[COLOR white]Found: [/COLOR]' + '[COLOR aqua][B]' + str(name_old) + ' (OLD)[/B][/COLOR]','Which log would you like to view?',nolabel='[B]CURRENT[/B]', yeslabel='[B]OLD[/B]')
        if choice == 0:
            logsfound_current.sort(key=lambda f: os.path.getmtime(f))
            if file == True: return logsfound_current[-1]
            else:
                filename    = open(logsfound_current[-1], 'r')
                logtext     = filename.read()
                filename.close()
                Common.TextBoxError('[COLOR aqua]No Limits Tools - Viewing ' + name_current + '[/COLOR]',logtext)
        else:
            logsfound_old.sort(key=lambda f: os.path.getmtime(f))
            if file == True: return logsfound_old[-1]
            else:
                filename    = open(logsfound_old[-1], 'r')
                logtext     = filename.read()
                filename.close()
                Common.TextBoxError('[COLOR aqua]No Limits Tools - Viewing ' + name_old + '[/COLOR]',logtext)
    else:
        logsfound_current.sort(key=lambda f: os.path.getmtime(f))
        if file == True: return logsfound_current[-1]
        else:
            filename    = open(logsfound_current[-1], 'r')
            logtext     = filename.read()
            filename.close()
            Common.TextBoxError('[COLOR aqua]No Limits Tools - Viewing ' + name_current + '[/COLOR]',logtext)
    
def autocleanask():
    choice = xbmcgui.Dialog().yesno(MAINTTITLE, 'Selecting [COLOR green]YES[/COLOR] will delete your cache, thumbnails and packages.','[I][COLOR lightsteelblue]Do you wish to continue?[/I][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
    if choice == 1:
        autocleannow()
    
def autocleannow():
    HomeDir = xbmc.translatePath('special://home')
    WINDOWSCACHE = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OTHERCACHE = os.path.join(xbmc.translatePath('special://home'), 'temp')
    
    if os.path.exists(HomeDir)==True:   
        path=WINDOWS
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
            
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)
                
        if os.path.exists(WINDOWSCACHE)==True:   
            path=WINDOWSCACHE
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

        if os.path.exists(OTHERCACHE)==True:   
            path=OTHERCACHE
            import glob
            for infile in glob.glob(os.path.join(path, '*.dmp')):
                File=infile
                print infile
                os.remove(infile)
                
            for infile in glob.glob(os.path.join(path, '*.txt')):
                File=infile
                print infile
                os.remove(infile)

    if os.path.exists(CACHEPATH)==True:    
        for root, dirs, files in os.walk(CACHEPATH):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
                
    if os.path.exists(TEMPPATH)==True:    
        for root, dirs, files in os.walk(TEMPPATH):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass
        
    if os.path.exists(THUMBNAILPATH)==True:  
                for root, dirs, files in os.walk(THUMBNAILPATH):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
    else:
        pass
    
    text13 = os.path.join(DATABASEPATH,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass
        
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
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

    xbmc.executebuiltin("Container.Refresh")

    xbmcgui.Dialog().ok(MAINTTITLE,"Auto clean finished.","Your cache, thumbnails and packages have all been deleted")

################################
###   AUTO CLEAR MB
################################
def AUTO_CLEAR_CACHE_MB():
    HomeDir = xbmc.translatePath('special://home')
    WINDOWSCACHE = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OTHERCACHE = os.path.join(xbmc.translatePath('special://home'), 'temp')

    if os.path.exists(CACHEPATH)==True:    
        for root, dirs, files in os.walk(CACHEPATH):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
                
    if os.path.exists(TEMPPATH)==True:    
        for root, dirs, files in os.walk(TEMPPATH):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass

    xbmc.executebuiltin("Container.Refresh")

def AUTO_CLEAR_PACKAGES_MB():
    time.sleep(60)

    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                try:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                except: pass

def AUTO_CLEAR_THUMBS_MB():
    if os.path.exists(THUMBNAILPATH)==True:  
                for root, dirs, files in os.walk(THUMBNAILPATH):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass
    else:
        pass
    
    text13 = os.path.join(DATABASEPATH,"Textures13.db")
    try:
        os.unlink(text13)
    except OSError:
        pass

################################
###   AUTO STARTUP
################################
def Auto_Startup():
    #AutoThumbs()
    wiz.oldThumbs()
    #AutoCache()
    wiz.clearCache(); wiz.refresh()
    time.sleep(60)
    #AutoPackages()
    wiz.clearPackages(); wiz.refresh()

def AutoCache():
    if os.path.exists(CACHEPATH)==True:    
        for root, dirs, files in os.walk(CACHEPATH):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
                
    if os.path.exists(TEMPPATH)==True:    
        for root, dirs, files in os.walk(TEMPPATH):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:                
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            checker = (os.path.join(root, d))
                            if not "archive_cache" in str(checker):
                                shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                            
                else:
                    pass

def AutoThumbs():
    if os.path.exists(THUMBNAILPATH)==True:  
                for root, dirs, files in os.walk(THUMBNAILPATH):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except: pass
    else: pass
    
    text13 = os.path.join(DATABASEPATH,"Textures13.db")
    try:
        os.unlink(text13)
    except: pass

def AutoPackages():
    time.sleep(60)
    purgePath = xbmc.translatePath('special://home/addons/packages')
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                try:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                except: pass

def AutoCrash():  
    HomeDir = xbmc.translatePath('special://home')
    WINDOWSCACHE = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OTHERCACHE = os.path.join(xbmc.translatePath('special://home'), 'temp')
    
    if os.path.exists(HomeDir)==True:   
        path=WINDOWS
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
                
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)
                
    if os.path.exists(WINDOWSCACHE)==True:   
        path=WINDOWSCACHE
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
                
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)

    if os.path.exists(OTHERCACHE)==True:   
        path=OTHERCACHE
        import glob
        for infile in glob.glob(os.path.join(path, '*.dmp')):
            File=infile
            print infile
            os.remove(infile)
                
        for infile in glob.glob(os.path.join(path, '*.txt')):
            File=infile
            print infile
            os.remove(infile)
            
def OPEN_EXTERNAL_SETTINGS():
    POSEIDON     = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.poseidon')
    BOBUNLEASHED = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.bob.unleashed')
    DEATHSTREAMS = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.blamo')
    ELYSIUM      = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.elysium')
    EXENDEDINFO  = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.extendedinfo')
    METALLIQ     = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.metalliq')
    OCULUS       = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.oculus')
    STARTEC      = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.StarTec')
    STREAMHUB    = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.streamhub')
    UKTURK       = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.ukturk')
    YOUTUBE      = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.youtube')
    MADEINCANADA = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.mic')
    GLOBETV      = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.israelive')
    COVENANT     = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.covenant')
    EXODUS       = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.exodus')
    SPECTO       = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.specto')
    
    if os.path.exists(POSEIDON):
        POSEIDON_SELECT = '[COLOR white][B]Open Poseidon Settings[/B][/COLOR]'
    else:
        POSEIDON_SELECT = '[COLOR gray][B]Poseidon (Not Installed)[/B][/COLOR]'

    if os.path.exists(BOBUNLEASHED):
        BOBUNLEASHED_SELECT = '[COLOR white][B]Open Bob Unleashed Settings[/B][/COLOR]'
    else:
        BOBUNLEASHED_SELECT = '[COLOR gray][B]Bob Unleashed (Not Installed)[/B][/COLOR]'

    if os.path.exists(DEATHSTREAMS):
        DEATHSTREAMS_SELECT = '[COLOR white][B]Open Death Streams Settings[/B][/COLOR]'
    else:
        DEATHSTREAMS_SELECT = '[COLOR gray][B]Death Streams (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        ELYSIUM_SELECT = '[COLOR white][B]Open Elysium Settings[/B][/COLOR]'
    else:
        ELYSIUM_SELECT = '[COLOR gray][B]Elysium (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        EXENDEDINFO_SELECT = '[COLOR white][B]Open Exended Info Mod Settings[/B][/COLOR]'
    else:
        EXENDEDINFO_SELECT = '[COLOR gray][B]Exended Info Mod (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        METALLIQ_SELECT = '[COLOR white][B]Open MetalliQ Settings[/B][/COLOR]'
    else:
        METALLIQ_SELECT = '[COLOR gray][B]MetalliQ (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        OCULUS_SELECT = '[COLOR white][B]Open Oculus Settings[/B][/COLOR]'
    else:
        OCULUS_SELECT = '[COLOR gray][B]Oculus (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        STARTEC_SELECT = '[COLOR white][B]Open Star Tec Settings[/B][/COLOR]'
    else:
        STARTEC_SELECT = '[COLOR gray][B]Star Tec (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        STREAMHUB_SELECT = '[COLOR white][B]Open StreamHUB Settings[/B][/COLOR]'
    else:
        STREAMHUB_SELECT = '[COLOR gray][B]StreamHUB (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        UKTURK_SELECT = '[COLOR white][B]Open UK Turks Settings[/B][/COLOR]'
    else:
        UKTURK_SELECT = '[COLOR gray][B]UK Turks (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        YOUTUBE_SELECT = '[COLOR white][B]Open YouTube Settings[/B][/COLOR]'
    else:
        YOUTUBE_SELECT = '[COLOR gray][B]YouTube (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        MADEINCANADA_SELECT = '[COLOR white][B]Open Made in Canada Settings[/B][/COLOR]'
    else:
        MADEINCANADA_SELECT = '[COLOR gray][B]Made in Canada (Not Installed)[/B][/COLOR]'

    if os.path.exists(ELYSIUM):
        GLOBETV_SELECT = '[COLOR white][B]Open Globe TV Settings[/B][/COLOR]'
    else:
        GLOBETV_SELECT = '[COLOR gray][B]Globe TV (Not Installed)[/B][/COLOR]'

    if os.path.exists(COVENANT):
        COVENANT_SELECT = '[COLOR white][B]Open Covenant Settings[/B][/COLOR]'
    else:
        COVENANT_SELECT = '[COLOR gray][B]Covenant (Not Installed)[/B][/COLOR]'

    if os.path.exists(EXODUS):
        EXODUS_SELECT = '[COLOR white][B]Open Exodus Settings[/B][/COLOR]'
    else:
        EXODUS_SELECT = '[COLOR gray][B]Exodus (Not Installed)[/B][/COLOR]'

    if os.path.exists(SPECTO):
        SPECTO_SELECT = '[COLOR white][B]Open Specto Settings[/B][/COLOR]'
    else:
        SPECTO_SELECT = '[COLOR gray][B]Specto (Not Installed)[/B][/COLOR]'

    choice = dialog.select(ADDONTITLE, [POSEIDON_SELECT,BOBUNLEASHED_SELECT,DEATHSTREAMS_SELECT,ELYSIUM_SELECT,EXENDEDINFO_SELECT,METALLIQ_SELECT,OCULUS_SELECT,STARTEC_SELECT,STREAMHUB_SELECT,UKTURK_SELECT,YOUTUBE_SELECT,MADEINCANADA_SELECT,GLOBETV_SELECT,COVENANT_SELECT,EXODUS_SELECT,SPECTO_SELECT])
    if choice == 0:
        if os.path.exists(POSEIDON):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.poseidon)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Poseidon is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 1:
        if os.path.exists(BOBUNLEASHED):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.bob.unleashed)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Bob Unleashed is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 2:
        if os.path.exists(DEATHSTREAMS):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.blamo)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Death Streams is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 3:
        if os.path.exists(ELYSIUM):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.elysium)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Elysium is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 4:
        if os.path.exists(EXENDEDINFO):
            xbmc.executebuiltin("Addon.OpenSettings(script.extendedinfo)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Exended Info Mod is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 5:
        if os.path.exists(METALLIQ):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.metalliq)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, MetalliQ is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 6:
        if os.path.exists(OCULUS):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.oculus)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Oculus is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 7:
        if os.path.exists(STARTEC):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.StarTec)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Star Tec is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 8:
        if os.path.exists(STREAMHUB):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.streamhub)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, StreamHUB is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 9:
        if os.path.exists(UKTURK):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.ukturk)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, UK Turk is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 10:
        if os.path.exists(YOUTUBE):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.youtube)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, YouTube is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 11:
        if os.path.exists(MADEINCANADA):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.mic)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Made in Canada is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 12:
        if os.path.exists(GLOBETV):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.israelive)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Globe TV is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 13:
        if os.path.exists(COVENANT):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.covenant)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Covenant is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 14:
        if os.path.exists(EXODUS):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.exodus)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Exodus is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 15:
        if os.path.exists(SPECTO):
            xbmc.executebuiltin("Addon.OpenSettings(plugin.video.specto)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Specto is not installed on this system so we cannot open the settings.[/COLOR]")

 
def OPEN_RESOLVER_SETTINGS():
    URLRESOLVER        = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.module.urlresolver')
    RESOLVEURL         = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.module.resolveurl')
    
    if os.path.exists(URLRESOLVER):
        URLRESOLVER_SELECT = '[COLOR white][B]Open URLResolver Settings[/B][/COLOR]'
    else:
        URLRESOLVER_SELECT = '[COLOR gray][B]URLResolver (Not Installed)[/B][/COLOR]'

    if os.path.exists(RESOLVEURL):
        RESOLVEURL_SELECT = '[COLOR white][B]Open ResolveURL Settings[/B][/COLOR]'
    else:
        RESOLVEURL_SELECT = '[COLOR gray][B]ResolveURL (Not Installed)[/B][/COLOR]'
    choice = dialog.select(ADDONTITLE, [URLRESOLVER_SELECT,RESOLVEURL_SELECT])
    if choice == 0:
        if os.path.exists(URLRESOLVER):
            xbmc.executebuiltin("Addon.OpenSettings(script.module.urlresolver)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, URLRESOLVER is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 1:
        if os.path.exists(RESOLVEURL):
            xbmc.executebuiltin("Addon.OpenSettings(script.module.resolveurl)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, RESOLVEURL is not installed on this system so we cannot open the settings.[/COLOR]")

def OPEN_SCRAPER_SETTINGS():
    NANSCRAPERS       = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.module.nanscrapers')
    UNIVERSALSCRAPERS = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.module.universalscrapers')
    
    if os.path.exists(NANSCRAPERS):
        NANSCRAPERS_SELECT = '[COLOR white][B]Open NAN Scrapers Settings[/B][/COLOR]'
    else:
        NANSCRAPERS_SELECT = '[COLOR gray][B]NAN Scrapers (Not Installed)[/B][/COLOR]'

    if os.path.exists(UNIVERSALSCRAPERS):
        UNIVERSALSCRAPERS_SELECT = '[COLOR white][B]Open Universal Scrapers Settings[/B][/COLOR]'
    else:
        UNIVERSALSCRAPERS_SELECT = '[COLOR gray][B]Universal Scrapers (Not Installed)[/B][/COLOR]'
    choice = dialog.select(ADDONTITLE, [NANSCRAPERS_SELECT,UNIVERSALSCRAPERS_SELECT])
    if choice == 0:
        if os.path.exists(NANSCRAPERS):
            xbmc.executebuiltin("Addon.OpenSettings(script.module.nanscrapers)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, NAN Scrapers is not installed on this system so we cannot open the settings.[/COLOR]")
    if choice == 1:
        if os.path.exists(UNIVERSALSCRAPERS):
            xbmc.executebuiltin("Addon.OpenSettings(script.module.universalscrapers)")
        else:
            dialog.ok(ADDONTITLE,"[COLOR white]Sorry, Universal Scrapers is not installed on this system so we cannot open the settings.[/COLOR]")


def RUYA_FIX():
    name = "[COLOR white][B]Ruya Fix[/B][/COLOR]"
    url = BASEURL + base64.b64decode(b'bWFpbnRlbmFuY2UvcnV5YV9maXguemlw')
    description = "NULL"
    #Check is the packages folder exists, if not create it.
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    if not os.path.exists(path):
        os.makedirs(path)
    buildname = name
    dp = xbmcgui.DialogProgress()
    dp.create(ADDONTITLE,"","","Build: " + buildname)
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

    HomeDir = xbmc.translatePath('special://home')
    WINDOWSCACHE = os.path.join(xbmc.translatePath('special://home'), 'cache')
    OTHERCACHE = xbmc.translatePath('special://temp')

    if os.path.exists(WINDOWSCACHE)==True:   
        path=WINDOWSCACHE
        import glob
        for infile in glob.glob(os.path.join(path, '*.fi')):
            File=infile
            print infile
            os.remove(infile)

    if os.path.exists(OTHERCACHE)==True:   
        path=OTHERCACHE
        import glob
        for infile in glob.glob(os.path.join(path, '*.fi')):
            File=infile
            print infile
            os.remove(infile)

    dialog.ok(ADDONTITLE, "[COLOR white]RUYA Fix installed![/COLOR]",'',"[COLOR white]Thank you for using No Limits Tools![/COLOR]")


def BASE64_ENCODE_DECODE():
    dialog = xbmcgui.Dialog()
    choice = dialog.select(ADDONTITLE, ['Encode A String','Decode A String'])
    if choice == 0:
        vq = Common._get_keyboard( heading="Enter String to Encode" )
        if ( not vq ): return False, 0
        input = str(vq)
        output = base64.b64encode(input)
        dialog.ok(ADDONTITLE, '[COLOR lightskyblue]Orignal String: [/COLOR]' + input, '[COLOR lightskyblue]Encrypted String: [/COLOR]' + output)
    else:
        vq = Common._get_keyboard( heading="Enter String to Decode" )
        if ( not vq ): return False, 0
        input = str(vq)
        output = base64.b64decode(vq)
        dialog.ok(ADDONTITLE, '[COLOR lightskyblue]Encrypted String: [/COLOR]' + input, '[COLOR lightskyblue]Original String: [/COLOR]' + output)

#######################################################################
#               TURN AUTO CLEAN ON|OFF
####################################################################### 

def AUTO_CLEAN_ON_OFF():
    startup_clean = plugintools.get_setting("acstartup")

    if startup_clean == 'true':
        CURRENT = '    <setting id="acstartup" value="true" />'
        NEW     = '    <setting id="acstartup" value="false" />'
    else:
        CURRENT = '    <setting id="acstartup" value="false" />'
        NEW     = '    <setting id="acstartup" value="true" />'

    HOME         =  xbmc.translatePath('special://userdata/addon_data/plugin.program.nolimitstools')
    for root, dirs, files in os.walk(HOME):  #Search all xml files and replace physical with special
        for file in files:
            if file == "settings.xml":
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(CURRENT, NEW)
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

    xbmc.executebuiltin("Container.Refresh")

#######################################################################
#               TURN WEEKLY AUTO CLEAN ON|OFF
####################################################################### 

def AUTO_WEEKLY_CLEAN_ON_OFF():
    startup_clean = plugintools.get_setting("clearday")

    if startup_clean == '1':
        CURRENT = '    <setting id="clearday" value="1" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '2':
        CURRENT = '    <setting id="clearday" value="2" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '3':
        CURRENT = '    <setting id="clearday" value="3" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '4':
        CURRENT = '    <setting id="clearday" value="4" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '5':
        CURRENT = '    <setting id="clearday" value="5" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '6':
        CURRENT = '    <setting id="clearday" value="6" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '7':
        CURRENT = '    <setting id="clearday" value="7" />'
        NEW     = '    <setting id="clearday" value="0" />'
    if startup_clean == '0':
        CURRENT = '    <setting id="clearday" value="0" />'
        NEW     = '    <setting id="clearday" value="1" />'


    HOME         =  xbmc.translatePath('special://userdata/addon_data/plugin.program.nolimitstools')
    for root, dirs, files in os.walk(HOME):  #Search all xml files and replace physical with special
        for file in files:
            if file == "settings.xml":
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(CURRENT, NEW)
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

    xbmc.executebuiltin("Container.Refresh")
    
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def convertSize(size):
   import math
   if (size == 0):
       return '[COLOR aqua][B]0 MB[/COLOR][/B]'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if size_name[i] == "B":
        return '[COLOR aqua][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if size_name[i] == "KB":
        return '[COLOR aqua][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if size_name[i] == "GB":
        return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if size_name[i] == "TB":
        return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if s < 50:
        return '[COLOR yellowgreen][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if s >= 50:
        if s < 100:
            return '[COLOR orange][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if s >= 100:
        return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'

def convertSizeInstall(size):
   import math
   if (size == 0):
       return '[COLOR aqua][B]0 MB[/COLOR][/B]'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if size_name[i] == "B":
        return '[COLOR aqua][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if size_name[i] == "KB":
        return '[COLOR aqua][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if size_name[i] == "TB":
        return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if s < 1000:
        return '[COLOR yellowgreen][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if s >= 1000:
        if s < 1500:
            return '[COLOR orange][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'
   if s >= 1500:
        return '[COLOR red][B]%s %s' % (s,size_name[i]) + '[/COLOR][/B]'

def removeAddon(addon):
	if dialog.yesno(ADDONTITLE, 'Are you sure you want to delete the addon:', '[COLOR yellow]%s[/COLOR]' % addon, yeslabel='Yes, Remove', nolabel='No, Cancel'):
		wiz.cleanHouse(os.path.join(ADDONS, addon))
		removeAddonData(addon)
		wiz.LogNotify('Remove Addon', 'Complete!')
		dialog.ok(ADDONTITLE, 'The addon has been removed but will remain in the addons list until the next time you reload Kodi.')
	else: wiz.LogNotify('Remove Addon', 'Cancelled!')
	xbmc.executebuiltin('Container.Refresh')

def removeAddonData(addon):
	if addon == 'all':
		if dialog.yesno(ADDONTITLE, 'Would you like to remove ALL addon data stored in you Userdata folder?', yeslabel='Yes, Remove', nolabel='No, Cancel'):
			wiz.cleanHouse(ADDOND)
		else: wiz.LogNotify('Remove Addon Data', 'Cancelled!')
	elif addon == 'uninstalled':
		if dialog.yesno(ADDONTITLE, 'Would you like to remove ALL addon data stored in you Userdata folder for uninstalled addons?', yeslabel='Yes, Remove', nolabel='No, Cancel'):
			total = 0
			for folder in glob.glob(os.path.join(ADDOND, '*')):
				foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
				if foldername in EXCLUDES: pass
				elif os.path.exists(os.path.join(ADDONS, foldername)): pass
				else: wiz.cleanHouse(folder); total += 1; wiz.log(folder); shutil.rmtree(folder)
			wiz.LogNotify('Clean up Uninstalled', '[COLOR yellow]%s[/COLOR] Folders(s) Removed' % total)
		else: wiz.LogNotify('Remove Addon Data', 'Cancelled!')
	elif addon == 'empty':
		if dialog.yesno(ADDONTITLE, 'Would you like to remove ALL empty addon data folders in you Userdata folder?', yeslabel='Yes, Remove', nolabel='No, Cancel'):
			total = wiz.emptyfolder(ADDOND)
			wiz.LogNotify('Remove Empty Folders', '[COLOR yellow]%s[/COLOR] Folders(s) Removed' % total)
		else: wiz.LogNotify('Remove Empty Folders', 'Cancelled!')
	else:
		addon_data = os.path.join(USERDATA, 'addon_data', addon)
		if addon in EXCLUDES:
			wiz.LogNotify("Protected Plugin", "Not allowed to remove Addon_Data")
		elif os.path.exists(addon_data):  
			if dialog.yesno(ADDONTITLE, 'Would you also like to remove the addon data for:', '[COLOR yellow]%s[/COLOR]' % addon, yeslabel='Yes, Remove', nolabel='No, Cancel'):
				wiz.cleanHouse(addon_data)
				try:
					shutil.rmtree(addon_data)
				except:
					wiz.log("Error deleting: %s" % addon_data)
			else: 
				wiz.log('Addon data for %s was not removed' % addon)
	xbmc.executebuiltin('Container.Refresh')
