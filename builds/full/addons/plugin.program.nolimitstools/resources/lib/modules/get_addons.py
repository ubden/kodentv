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
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys,xbmcvfs
import shutil
import base64
import re
import shutil
import time
import plugintools
from resources.lib.modules import common as Common
from resources.lib.modules import downloader
from resources.lib.modules import maintenance
import zipfile
import urllib,urllib2
from HTMLParser import HTMLParser

dialog           = xbmcgui.Dialog()
dp               = xbmcgui.DialogProgress()
ADDONTITLE       = "[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"
ADDON_ID         = 'plugin.program.nolimitstools'
FANART           = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'fanart.jpg'))
ICON             = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
XXX_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
VIDEO_ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
TOP_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
SUPPORT_ICON     = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
PROGRAM_ICON     = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
PICTURE_ICON     = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
PC_ICON          = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
PAID_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
PACKS_ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
MUSIC_ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
DEP_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
ALL_ICON         = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
UPDATE_ICON      = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
REPO_ICON        = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'resources/art/installer.png'))
TEMP_FILE        = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID,'temp/temp_installer.xml'))
ADDON_DATA       = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID, 'packs/'))
PARENTAL_FILE    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID , 'controls.txt'))
PARENTAL_FOLDER  = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID))
BASEURL          = base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20v')
ECHO_API         = BASEURL + base64.b64decode(b'YXBpL2FwaS5waHA/c2VydmljZT1hZGRvbnMmYWN0aW9uPWNvdW50')
ADDON_LIST       = BASEURL + base64.b64decode(b'YWRkb25zL2FkZG9uX2xpc3QueG1s')
ADDON_LIST_PAID  = BASEURL + base64.b64decode(b'YWRkb25zL2FkZG9uX2xpc3RfcGFpZC54bWw=')
DEPENDENCIES     = BASEURL + base64.b64decode(b'YWRkb25zL2RlcGVuZGVuY2llc19saXN0LnhtbA==')
REPO_LIST        = BASEURL + base64.b64decode(b'YWRkb25zL3JlcG9zLnhtbA==')
PASSWD           = BASEURL + base64.b64decode(b'b3RoZXIvYWR1bHRwYXNzLnR4dA==')
PACKS_LIST       = BASEURL + base64.b64decode(b'YWRkb25zL2FkZG9uX3BhY2tzLnhtbA==')
SOURCES_URL      = BASEURL + base64.b64decode(b'YWRkb25zL3NvdXJjZXMueG1s')
DEP_LIST         = BASEURL + base64.b64decode(b'YWRkb25zL2RlcHMueG1s')
PAID_DESC        = BASEURL + base64.b64decode(b'YWRkb25zL3BhaWRfZGVzY3JpcHRpb25zLw==')
DESC             = BASEURL + base64.b64decode(b'YWRkb25zL2Rlc2NyaXB0aW9ucy8=')
KODIAPPS_FILE    = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID,'temp/kodiapps.xml'))
KODIAPPS_ICON    = "http://echocoder.com/images/addons/plugin.video.etherealtv/icon.png"
KODIAPPS_FANART  = "http://echocoder.com/images/addons/plugin.video.etherealtv/fanart.jpg"
USER_AGENT       = base64.b64decode(b'VGhlV2l6YXJkSXNIZXJl')

def MENU_MAIN():
    
    GET_COUNTS()

    if os.path.exists(PARENTAL_FILE):
        vq = Common._get_keyboard( heading="Please Enter Your Password" )
        if ( not vq ): 
            dialog.ok(ADDONTITLE,"Sorry, no password was entered.")
            quit()
        pass_one = vq

        vers = open(PARENTAL_FILE, "r")
        regex = re.compile(r'<password>(.+?)</password>')
        for line in vers:
            file = regex.findall(line)
            for current_pin in file:
                password = base64.b64decode(current_pin)
                if not password == pass_one:
                    dialog.ok(ADDONTITLE,"Sorry, the password you entered was incorrect.")
                    quit()
                    
    number_of_addons = Common.count("NUMBER_OF_ADDONS",TEMP_FILE)
    total_addons_week = Common.count("TOTAL_ADDONS_WEEK",TEMP_FILE)
    total_addons_alltime = Common.count("TOTAL_ADDONS_ALLTIME",TEMP_FILE)
    Common.addDir("[COLOR white][B]Addons Downloaded (Week)  - [/COLOR][COLOR yellowgreen]" + str(total_addons_week) + "[/B][/COLOR]",BASEURL,121,ICON,FANART,'')
    Common.addDir("[COLOR white][B]Addons Downloaded (Total) - [/COLOR][COLOR yellowgreen]" + str(total_addons_alltime) + "[/B][/COLOR]",BASEURL,121,ICON,FANART,'')
    Common.addDir("[COLOR white][B]Addons Available In Addon Installer  - [/COLOR][COLOR yellowgreen]" + str(number_of_addons) + " Addons[/B][/COLOR]",BASEURL,121,ICON,FANART,'')
    Common.addDir("[COLOR yellowgreen][B]--------------------------------------------------------------------------------------------------[/B][/COLOR]",BASEURL,121,ALL_ICON,FANART,description='all')
    Common.addDir("[COLOR yellowgreen][B]Search for Addons[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description='search')
    Common.addDir("[COLOR white][B]All Addons[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description='all')
    Common.addDir("[COLOR white][B]Repositories[/B][/COLOR]",BASEURL,150,REPO_ICON,FANART,description='repos')
    Common.addDir("[COLOR white][B]File Manager Sources[/B][/COLOR]",BASEURL,177,REPO_ICON,FANART,description='')
    Common.addDir("[COLOR white][B]Top 14 Downloaded Addons This Week[/B][/COLOR]",BASEURL,150,TOP_ICON,FANART,description='top')
    Common.addDir("[COLOR white][B]Kodiapps Addon Chart[/B][/COLOR]",BASEURL,150,KODIAPPS_ICON,KODIAPPS_FANART,description='kodiapps')
    #Common.addDir("[COLOR white][B]APK Addons[/B][/COLOR]",BASEURL,170,XXX_ICON,FANART,description='Null')
    Common.addDir("[COLOR white][B]Video Addons[/B][/COLOR]",BASEURL,150,VIDEO_ICON,FANART,description='video')
    Common.addDir("[COLOR white][B]Program Addons[/B][/COLOR]",BASEURL,150,PROGRAM_ICON,FANART,description='program')
    Common.addDir("[COLOR white][B]Music Addons[/B][/COLOR]",BASEURL,150,MUSIC_ICON,FANART,description='audio')
    Common.addDir("[COLOR white][B]Picture Addons[/B][/COLOR]",BASEURL,150,PICTURE_ICON,FANART,description='image')
    Common.addDir("[COLOR white][B]Adult (XXX) Addons[/B][/COLOR]",BASEURL,150,XXX_ICON,FANART,description='xxx')
    #Common.addDir("[COLOR yellowgreen][B][I]Subscription Based Services (e.g IPTV,VPN,TV GUIDES).[/I][/B][/COLOR]",BASEURL,150,PAID_ICON,FANART,description='paid')
    Common.addDir("[COLOR dodgerblue][B]Report A Broken Addon[/B][/COLOR]",BASEURL,152,SUPPORT_ICON,FANART,'')
    Common.addDir("[COLOR dodgerblue][B]How To Get an Addon Added[/B][/COLOR]",BASEURL,153,SUPPORT_ICON,FANART,'')

    if not os.path.exists(PARENTAL_FILE):
        Common.addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR red]OFF[/COLOR][/B][/COLOR]","url",159,PC_ICON,FANART,'')
    else:
        Common.addDir("[COLOR orangered][B]PARENTAL CONTROLS - [COLOR yellowgreen]ON[/COLOR][/B][/COLOR]","url",159,PC_ICON,FANART,'')

    kodi_name = Common.GET_KODI_VERSION()

    if kodi_name == "Jarvis":
        xbmc.executebuiltin("Container.SetViewMode(50)")
    elif kodi_name == "Krypton":
        xbmc.executebuiltin("Container.SetViewMode(55)")
    else: xbmc.executebuiltin("Container.SetViewMode(50)")

def GET_LIST(description):

    try:
        matcher,sort = description.split("|SPLIT|")
    except:
        matcher = description
        sort = "count"

    SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))
    i = 0
    a = 0
    b = 0
    if not os.path.isfile(SOURCES):
        f = open(SOURCES,'w')
        f.write('<sources>\n    <files>\n        <default pathversion="1"></default>\n    </files>\n</sources>')
        f.close()

    dp.create(ADDONTITLE,"[COLOR blue]We are getting the addons from our server.[/COLOR]",'','')    

    combinedlists = []

    if matcher == "search":
        vq = Common._get_keyboard( heading="Enter a name for this backup" )
        if ( not vq ): quit()
        term = vq.lower()
        url = ADDON_LIST
        url2 = ADDON_LIST
        link = open_url(url)
        dp.update(0)
        match= re.compile('<item>(.+?)</item>').findall(link)
        dis_links = len(match)
        namelist=[]
        countlist=[]
        totallist=[]
        iconlist=[]
        fanartlist=[]
        addonlist=[]
        repolist=[]
        for item in match:
            found = 0
            i = i + 1
            dis_count = str(i)
            progress = 100 * int(i)/int(dis_links)
            name=re.compile('<title>(.+?)</title>').findall(item)[0]
            dp.update(progress,"Filtering addon " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]Found " + name + "[/B][/COLOR]")
            addon_path=re.compile('<addon_path>(.+?)</addon_path>').findall(item)[0]
            repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0]
            if "<iconimage>" in item:
                iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(item)[0]
                fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
            else:
                zips=re.compile('<zips>(.+?)</zips>').findall(item)[0]
                if not zips.endswith("/"):
                    zips = zips + "/"
                iconimage = zips + addon_path + "/icon.png"
                fanart = zips + addon_path + "/fanart.jpg"
            try:
                tubes=re.compile('<youtube>(.+?)</youtube>').findall(item)
                if len(tubes) > 1:
                    youtube_id = "multi"
                else:
                    try:
                        youtube_id=re.compile('<youtube>(.+?)</youtube>').findall(item)[0]
                    except: youtube_id = "null"
            except: youtube_id = "null"
            addon_path2 = addon_path
            addon_path = addon_path + "|SPLIT|" + youtube_id    

            if not " " in term:
                if term in name.lower():
                    found = 1
                elif term in addon_path.lower():
                    found = 1
                elif term in repo_path.lower():
                    found = 1
            else:
                terms = term.split(" ")
                for term in terms:
                    if term in name.lower():
                        found = 1
                    elif term in addon_path.lower():
                        found = 1
                    elif term in repo_path.lower():
                        found = 1

            if found == 1:
                namelist.append(name)
                countlist.append(str(Common.count(addon_path2+"ADDON_INSTALLER",TEMP_FILE)))
                totallist.append(str(Common.count(addon_path2+"ADDON_TOTAL",TEMP_FILE)))
                iconlist.append(iconimage)
                fanartlist.append(fanart)
                addonlist.append(addon_path)
                repolist.append(repo_path)
                
                if sort == "count":
                    combinedlists = list(zip(countlist,totallist,namelist,iconlist,fanartlist,addonlist,repolist))
                else:
                    combinedlists = list(zip(namelist,totallist,countlist,iconlist,fanartlist,addonlist,repolist))

        tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
        for count,total,name,iconimage,fanart,addon_path,repo_path in tup:
            addon_path,youtube_id = addon_path.split("|SPLIT|")
            ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
            REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
            url2 = addon_path + "," + repo_path + "," + name  + "," + url + "," + youtube_id
            base_name = name
            countfail = count
            try:
                count2 = int(count)
                count3 = "{:,}".format(count2)
                count = str(count3)
            except: count = countfail   
            try:
                bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
            except:
                bname = "Unknown"
            if not os.path.exists(ADDON):
                Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
            else:
                Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')

    elif matcher == "repos":
        namelist=[]
        countlist=[]
        totallist=[]
        repolist=[]
        url = REPO_LIST
        link = open_url(url)
        dp.update(0)
        match= re.compile('<item>(.+?)</item>').findall(link)
        dis_links = len(match)
        for item in sorted(match):
            i = i + 1
            dis_count = str(i)
            progress = 100 * int(i)/int(dis_links)
            name=re.compile('<title>(.+?)</title>').findall(item)[0]
            repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0] 
            dp.update(progress,"Filtering repositories " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]Found " + name + "[/B][/COLOR]")
            namelist.append(name)
            countlist.append(str(Common.count(repo_path+"ADDON_INSTALLER",TEMP_FILE)))
            totallist.append(str(Common.count(repo_path+"ADDON_TOTAL",TEMP_FILE)))
            repolist.append(repo_path)
            
            if sort == "count":
                combinedlists = list(zip(countlist,totallist,namelist,repolist))
            else:
                combinedlists = list(zip(namelist,totallist,countlist,repolist))            
            
        if sort == "count":
            tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
        else:
            tup = sorted(combinedlists)

        if sort == "count":
            Common.addDir("[COLOR yellowgreen][B]Search for Addons[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description='search')
            Common.addDir("[COLOR blue][B]Order Alphabetically[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description=matcher+'|SPLIT|name')
            Common.addItem("[COLOR white][B]------------------------------------------------------[/B][/COLOR]",BASEURL,999,ALL_ICON,FANART,'')
            for count,total,name,repo_path in tup:
                REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
                url2 = repo_path + "," + name  + "," + url
                countfail = count
                try:
                    count2 = int(count)
                    count3 = "{:,}".format(count2)
                    count = str(count3)
                except: count = countfail
                try:
                    bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
                except:
                    bname = "Unknown"
                if not os.path.exists(REPO):
                    Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,ICON,FANART,'')
                else:
                    Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,ICON,FANART,'')
        else:
            Common.addDir("[COLOR yellowgreen][B]Search for Addons[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description='search')
            Common.addDir("[COLOR blue][B]Order By Download Counts[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description=matcher+'|SPLIT|count')
            Common.addItem("[COLOR white][B]------------------------------------------------------[/B][/COLOR]",BASEURL,999,ALL_ICON,FANART,'')
            for name,total,count,repo_path in tup:
                REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
                url2 = repo_path + "," + name  + "," + url
                countfail = count
                try:
                    count2 = int(count)
                    count3 = "{:,}".format(count2)
                    count = str(count3)
                except: count = countfail
                try:
                    bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
                except:
                    bname = "Unknown"
                if not os.path.exists(REPO):
                    Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,ICON,FANART,'')
                else:
                    Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,ICON,FANART,'')

    elif "top" in matcher:
        if not "xxx" in matcher:
            Common.addDir("[COLOR yellowgreen][B]Exclude XXX Addons From The List[/B][/COLOR]",BASEURL,150,TOP_ICON,FANART,description='top-xxx')
            Common.addItem("--------------------------------------------------------------------------------------------------",BASEURL,999,TOP_ICON,FANART,'')
        else:
            Common.addDir("[COLOR yellowgreen][B]Include XXX Addons In The List[/B][/COLOR]",BASEURL,150,TOP_ICON,FANART,description='top')
            Common.addItem("--------------------------------------------------------------------------------------------------",BASEURL,999,TOP_ICON,FANART,'')
        namelist=[]
        countlist=[]
        totallist=[]
        iconlist=[]
        fanartlist=[]
        addonlist=[]
        repolist=[]
        found_one = 0
        url = ADDON_LIST
        url2 = ADDON_LIST
        link = open_url(url)
        dp.update(0)
        match= re.compile('<item>(.+?)</item>').findall(link)
        dis_links = len(match)  
        for item in sorted(match):
            i = i + 1
            dis_count = str(i)
            progress = 100 * int(i)/int(dis_links)
            name=re.compile('<title>(.+?)</title>').findall(item)[0]
            dp.update(progress,"Filtering addon " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]Found " + name + "[/B][/COLOR]")
            addon_path=re.compile('<addon_path>(.+?)</addon_path>').findall(item)[0]
            repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0]
            if "<iconimage>" in item:
                iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(item)[0]
                fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
            else:
                zips=re.compile('<zips>(.+?)</zips>').findall(item)[0]
                if not zips.endswith("/"):
                    zips = zips + "/"
                iconimage = zips + addon_path + "/icon.png"
                fanart = zips + addon_path + "/fanart.jpg"
            try:
                tubes=re.compile('<youtube>(.+?)</youtube>').findall(item)
                if len(tubes) > 1:
                    youtube_id = "multi"
                else:
                    try:
                        youtube_id=re.compile('<youtube>(.+?)</youtube>').findall(item)[0]
                    except: youtube_id = "null"
            except: youtube_id = "null"
            addon_path2 = addon_path
            addon_path = addon_path + "|SPLIT|" + youtube_id
            if matcher == "top-xxx":
                if not "xxx" in name.lower():
                    namelist.append(name)
                    countlist.append(str(Common.count(addon_path2+"ADDON_INSTALLER",TEMP_FILE)))
                    totallist.append(str(Common.count(addon_path2+"ADDON_TOTAL",TEMP_FILE)))
                    iconlist.append(iconimage)
                    fanartlist.append(fanart)
                    addonlist.append(addon_path)
                    repolist.append(repo_path)
            else:
                namelist.append(name)
                countlist.append(str(Common.count(addon_path2+"ADDON_INSTALLER",TEMP_FILE)))
                totallist.append(str(Common.count(addon_path2+"ADDON_TOTAL",TEMP_FILE)))
                iconlist.append(iconimage)
                fanartlist.append(fanart)
                addonlist.append(addon_path)
                repolist.append(repo_path)
            combinedlists = list(zip(countlist,totallist,namelist,iconlist,fanartlist,addonlist,repolist))
        tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
        check = 1
        for count,total,name,iconimage,fanart,addon_path,repo_path in tup:
            addon_path,youtube_id = addon_path.split("|SPLIT|")
            ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
            REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
            url2 = addon_path + "," + repo_path + "," + name  + "," + url + "," + youtube_id
            countfail = count
            try:
                count2 = int(count)
                count3 = "{:,}".format(count2)
                count = str(count3)
            except: count = countfail   
            if check < 14:
                if check == 1:
                    bname = " | [COLOR gold][B] This Week:[/COLOR][COLOR gold] " + count + "[/B][/COLOR][COLOR gold][B] - Total:[/COLOR][COLOR gold] " + total + "[/B][/COLOR]"
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR gold][B]1st - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR gold][B]1st - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                elif check == 2:
                    bname = " | [COLOR silver][B] This Week:[/COLOR][COLOR silver] " + count + "[/B][/COLOR][COLOR silver][B] - Total:[/COLOR][COLOR silver] " + total + "[/B][/COLOR]"
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR silver][B]2nd - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR silver][B]2nd - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                elif check == 3:
                    bname = " | [COLOR orange][B] This Week:[/COLOR][COLOR orange] " + count + "[/B][/COLOR][COLOR orange][B] - Total:[/COLOR][COLOR orange] " + total + "[/B][/COLOR]"
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR orange][B]3rd - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                        Common.addItem("--------------------------------------------------------------------------------------------------",BASEURL,999,TOP_ICON,FANART,'')
                    else:
                        Common.addDir("[COLOR orange][B]3rd - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                        Common.addItem("--------------------------------------------------------------------------------------------------",BASEURL,999,TOP_ICON,FANART,'')
                else:
                    bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen] [B]" + total + "[/B][/COLOR]"
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
            check = check + 1
    elif matcher == "kodiapps":
        namelist=[]
        ranklist=[]
        countlist=[]
        totallist=[]
        iconlist=[]
        fanartlist=[]
        addonlist=[]
        repolist=[]
        found_one = 0
        url = ADDON_LIST
        url2 = ADDON_LIST
        link = open_url(url)
        dp.update(0)
        match= re.compile('<item>(.+?)</item>').findall(link)
        dis_links = len(match)  
        for item in sorted(match):
            i = i + 1
            dis_count = str(i)
            progress = 100 * int(i)/int(dis_links)
            name=re.compile('<title>(.+?)</title>').findall(item)[0]
            dp.update(progress,"Filtering addon " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]Found " + name + "[/B][/COLOR]")
            addon_path=re.compile('<addon_path>(.+?)</addon_path>').findall(item)[0]
            repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0]
            if "<iconimage>" in item:
                iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(item)[0]
                fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
            else:
                zips=re.compile('<zips>(.+?)</zips>').findall(item)[0]
                if not zips.endswith("/"):
                    zips = zips + "/"
                iconimage = zips + addon_path + "/icon.png"
                fanart = zips + addon_path + "/fanart.jpg"
            try:
                tubes=re.compile('<youtube>(.+?)</youtube>').findall(item)
                if len(tubes) > 1:
                    youtube_id = "multi"
                else:
                    try:
                        youtube_id=re.compile('<youtube>(.+?)</youtube>').findall(item)[0]
                    except: youtube_id = "null"
            except: youtube_id = "null"
            rank = GET_KODIAPPS_RANKING_LOCAL(addon_path)
            rank = rank.replace("[COLOR yellowgreen]","").replace("[/COLOR]","")
            addon_path2 = addon_path
            addon_path = addon_path + "|SPLIT|" + youtube_id
            namelist.append(name)
            countlist.append(str(Common.count(addon_path2+"ADDON_INSTALLER",TEMP_FILE)))
            totallist.append(str(Common.count(addon_path2+"ADDON_TOTAL",TEMP_FILE)))
            ranklist.append(rank)
            iconlist.append(iconimage)
            fanartlist.append(fanart)
            addonlist.append(addon_path)
            repolist.append(repo_path)
            combinedlists = list(zip(ranklist,countlist,totallist,namelist,iconlist,fanartlist,addonlist,repolist))
        tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=False)
        displayed = 0
        for rank,count,total,name,iconimage,fanart,addon_path,repo_path in tup:
            if displayed == 0:
                Common.addItem("[COLOR dodgerblue][B]KODIAPPS.COM ADDONS RANKING LIST[/B][/COLOR]",url2,999,KODIAPPS_ICON,KODIAPPS_FANART,'')
                Common.addItem("[COLOR white][B]If a rank is missing from the list it is because we do not have permission to have that addon in the installer.[/B][/COLOR]",url2,999,KODIAPPS_ICON,KODIAPPS_FANART,'')
                Common.addItem("[COLOR white]----------------------------------[/COLOR]",url2,999,ICON,FANART,'')
                displayed = 1
            if not rank == "0":
                addon_path,youtube_id = addon_path.split("|SPLIT|")
                ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
                REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
                url2 = addon_path + "," + repo_path + "," + name  + "," + url + "," + youtube_id
                countfail = count
                try:
                    count2 = int(count)
                    count3 = "{:,}".format(count2)
                    count = str(count3)
                except: count = countfail
                if rank == "4":
                    Common.addItem("[COLOR white]----------------------------------[/COLOR]",url2,999,ICON,FANART,'')
                if rank == "1":
                    bname = " | [COLOR gold][B] This Week:[/COLOR][COLOR gold] " + count + "[/B][/COLOR][COLOR gold][B] - Total:[/COLOR][COLOR gold] " + total + "[/B][/COLOR]"
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR gold][B]RANK 1 - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR gold][B]RANK 1 - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                elif rank == "2":
                    bname = " | [COLOR silver][B] This Week:[/COLOR][COLOR silver] " + count + "[/B][/COLOR][COLOR silver][B] - Total:[/COLOR][COLOR silver] " + total + "[/B][/COLOR]"
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR silver][B]RANK 2 - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR silver][B]RANK 2 - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                elif rank == "3":
                    bname = " | [COLOR orange][B] This Week:[/COLOR][COLOR orange] " + count + "[/B][/COLOR][COLOR orange][B] - Total:[/COLOR][COLOR orange] " + total + "[/B][/COLOR]"
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR orange][B]RANK 3 - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR orange][B]RANK 3 - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                else:
                    bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen] [B]" + total + "[/B][/COLOR]"
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR white][B]" + rank + " - " + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR yellowgreen][B]" + rank + " - " + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
    else:
        url = ADDON_LIST
        url2 = ADDON_LIST
        link = open_url(url)
        dp.update(0)
        match= re.compile('<item>(.+?)</item>').findall(link)
        dis_links = len(match)
        namelist=[]
        countlist=[]
        totallist=[]
        iconlist=[]
        fanartlist=[]
        addonlist=[]
        repolist=[]
        for item in match:
            i = i + 1
            dis_count = str(i)
            progress = 100 * int(i)/int(dis_links)
            name=re.compile('<title>(.+?)</title>').findall(item)[0]
            dp.update(progress,"Filtering addon " + str(dis_count) + " of " + str(dis_links),"[COLOR white][B]Found " + name + "[/B][/COLOR]")
            addon_path=re.compile('<addon_path>(.+?)</addon_path>').findall(item)[0]
            repo_path=re.compile('<repo_path>(.+?)</repo_path>').findall(item)[0]
            if "<iconimage>" in item:
                iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(item)[0]
                fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
            else:
                zips=re.compile('<zips>(.+?)</zips>').findall(item)[0]
                if not zips.endswith("/"):
                    zips = zips + "/"
                iconimage = zips + addon_path + "/icon.png"
                fanart = zips + addon_path + "/fanart.jpg"
            try:
                tubes=re.compile('<youtube>(.+?)</youtube>').findall(item)
                if len(tubes) > 1:
                    youtube_id = "multi"
                else:
                    try:
                        youtube_id=re.compile('<youtube>(.+?)</youtube>').findall(item)[0]
                    except: youtube_id = "null"
            except: youtube_id = "null"
            addon_path2 = addon_path
            addon_path = addon_path + "|SPLIT|" + youtube_id                    
            namelist.append(name)
            countlist.append(str(Common.count(addon_path2+"ADDON_INSTALLER",TEMP_FILE)))
            totallist.append(str(Common.count(addon_path2+"ADDON_TOTAL",TEMP_FILE)))
            iconlist.append(iconimage)
            fanartlist.append(fanart)
            addonlist.append(addon_path)
            repolist.append(repo_path)
            
            if sort == "count":
                combinedlists = list(zip(countlist,totallist,namelist,iconlist,fanartlist,addonlist,repolist))
            else:
                combinedlists = list(zip(namelist,totallist,countlist,iconlist,fanartlist,addonlist,repolist))
        
        if sort == "count":
            tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)
            string = "count,total,name,iconimage,fanart,addon_path,repo_path"
        else:
            tup = sorted(combinedlists)
            string = "name,total,count,iconimage,fanart,addon_path,repo_path"

        if sort == "count":
            Common.addDir("[COLOR yellowgreen][B]Search for Addons[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description='search')
            Common.addDir("[COLOR blue][B]Order Alphabetically[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description=matcher+'|SPLIT|name')
            Common.addItem("[COLOR white][B]------------------------------------------------------[/B][/COLOR]",BASEURL,999,ALL_ICON,FANART,'')
            for count,total,name,iconimage,fanart,addon_path,repo_path in tup:
                addon_path,youtube_id = addon_path.split("|SPLIT|")
                ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
                REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
                url2 = addon_path + "," + repo_path + "," + name  + "," + url + "," + youtube_id
                base_name = name
                countfail = count
                try:
                    count2 = int(count)
                    count3 = "{:,}".format(count2)
                    count = str(count3)
                except: count = countfail   
                try:
                    bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
                except:
                    bname = "Unknown"
                if matcher == "xxx":
                    if matcher in name.lower():
                        if not os.path.exists(ADDON):
                            Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                        else:
                            Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')

                elif matcher != "all":
                    if matcher in addon_path:
                        if not os.path.exists(ADDON):
                                Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                        else:
                                Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                else:
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
        else:
            Common.addDir("[COLOR yellowgreen][B]Search for Addons[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description='search')
            Common.addDir("[COLOR blue][B]Order by Download Counts[/B][/COLOR]",BASEURL,150,ALL_ICON,FANART,description=matcher+'|SPLIT|count')
            Common.addItem("[COLOR white][B]------------------------------------------------------[/B][/COLOR]",BASEURL,999,ALL_ICON,FANART,'')

            for name,total,count,iconimage,fanart,addon_path,repo_path in tup:
                addon_path,youtube_id = addon_path.split("|SPLIT|")
                ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
                REPO   =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
                url2 = addon_path + "," + repo_path + "," + name  + "," + url + "," + youtube_id
                base_name = name
                countfail = count
                try:
                    count2 = int(count)
                    count3 = "{:,}".format(count2)
                    count = str(count3)
                except: count = countfail   
                try:
                    bname = " | [COLOR white] This Week:[/COLOR][COLOR yellowgreen][B] " + count + "[/B][/COLOR][COLOR white] - Total:[/COLOR][COLOR yellowgreen][B] " + total + "[/B][/COLOR]"
                except:
                    bname = "Unknown"
                if matcher == "xxx":
                    if matcher in name.lower():
                        if not os.path.exists(ADDON):
                            Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                        else:
                            Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')

                elif matcher != "all":
                    if matcher in addon_path:
                        if not os.path.exists(ADDON):
                                Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                        else:
                                Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                else:
                    if not os.path.exists(ADDON):
                        Common.addDir("[COLOR white][B]" + name + " - NOT INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')
                    else:
                        Common.addDir("[COLOR yellowgreen][B]" + name + " - INSTALLED[/B][/COLOR]" + bname,url2,176,iconimage,fanart,'')

    kodi_name = Common.GET_KODI_VERSION()

    if kodi_name == "Jarvis":
        xbmc.executebuiltin("Container.SetViewMode(50)")
    elif kodi_name == "Krypton":
        xbmc.executebuiltin("Container.SetViewMode(55)")
    else: xbmc.executebuiltin("Container.SetViewMode(50)")

def ADDON_DECIDE(name,url,iconimage,fanart):

    paid = 0
    normal = 0
    repo = 0

    urla  = url
    paid_mark = "null"
    youtube_id="null"
    try:
        addon_path,repo_path,base_name,url,paid_mark,youtube_id   = url.split(',')
        normal = 1
        paid = 1
    except:
        try:
            addon_path,repo_path,base_name,url,youtube_id   = urla.split(',')
            normal = 1
        except: 
            repo_path,base_name,url   = urla.split(',')
            repo = 1

    if normal == 1:
    
        send_youtube_multi = base_name + "," + url

        RANKING = GET_KODIAPPS_RANKING_LOCAL(addon_path)

        if not youtube_id.lower() == "null":
            if "http" in youtube_id.lower():
                youtube_id = youtube_id.replace("https://www.youtube.com/watch?v=","")
            if not "multi" in youtube_id.lower():
                    youtube_id = base64.b64decode(b"cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnlvdXR1YmUvcGxheS8/dmlkZW9faWQ9")+youtube_id

        service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(addon_path)
        body = urllib2.urlopen(service_url).read()

        ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))
        if not os.path.exists(ADDON):
            Common.addItem("[COLOR yellowgreen][B]Install Addon[/B][/COLOR]",urla+",install_me",151,iconimage,fanart,'')
        else:
            Common.addItem("[COLOR yellowgreen][B]Uninstall Addon[/B][/COLOR]",urla+",uninstall_me",151,iconimage,fanart,'')
        if not RANKING.lower() == "0":
            Common.addItem("[COLOR white][B]Addon Information[/B][/COLOR]",ADDON,187,iconimage,fanart,'')
        if "multi" in youtube_id.lower():
            Common.addItem('[COLOR white][B]Watch YouTube Review of ' + base_name + '[/B][/COLOR]',send_youtube_multi,183,iconimage,fanart,'')
        elif "null" not in youtube_id.lower():
            Common.addItem('[COLOR white][B]Watch YouTube Review of ' + base_name + '[/B][/COLOR]',youtube_id,95,iconimage,fanart,'')
        if not RANKING.lower() == "0":
            Common.addItem('[COLOR white][B]Kodiapps Rank: ' + RANKING + '[/B][/COLOR]',youtube_id,95,iconimage,fanart,'')
        week  = (str(Common.count(addon_path+"ADDON_INSTALLER",TEMP_FILE)))
        total =(str(Common.count(addon_path+"ADDON_TOTAL",TEMP_FILE)))   
        countfail = week

        try:
            count2 = int(week)
            count3 = "{:,}".format(count2)
            week = str(count3)
        except: week = countfail    

        Common.addItem('[COLOR white][B]Downloads This Week -  [/COLOR][COLOR yellowgreen]' + str(week) + '[/B][/COLOR]',url,999,iconimage,fanart,'')
        Common.addItem('[COLOR white][B]All Time Downloads -  [/COLOR][COLOR yellowgreen]' + str(total) + '[/B][/COLOR]',url,999,iconimage,fanart,'')

        Common.addItem("[COLOR white][B]Leave Review[/B][/COLOR]",urla+",leavereview_me",151,iconimage,fanart,'')
        Common.addDir("[COLOR white][B]Read Addon Reviews - [COLOR yellowgreen]" + body + " [/COLOR][/B][/COLOR]",urla+",readreview_me",151,iconimage,fanart,'')

    elif repo == 1:
        service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(repo_path)
        body = urllib2.urlopen(service_url).read()
        ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))
        if not os.path.exists(ADDON):
            Common.addItem("[COLOR yellowgreen][B]Install Repository[/B][/COLOR]",urla+",install_me",164,iconimage,fanart,'')
        else:
            Common.addItem("[COLOR yellowgreen][B]Uninstall Repository[/B][/COLOR]",urla+",uninstall_me",164,iconimage,fanart,'')
        Common.addItem("[COLOR white][B]Repository Information[/B][/COLOR]",urla+",info_me",164,iconimage,fanart,'')
        
        week  = (str(Common.count(repo_path+"ADDON_INSTALLER",TEMP_FILE)))
        total =(str(Common.count(repo_path+"ADDON_TOTAL",TEMP_FILE)))   

        Common.addItem('[COLOR white][B]Downloads This Week -  [/COLOR][COLOR yellowgreen]' + str(week) + '[/B][/COLOR]',url,999,iconimage,fanart,'')
        Common.addItem('[COLOR white][B]All Time Downloads -  [/COLOR][COLOR yellowgreen]' + str(total) + '[/B][/COLOR]',url,999,iconimage,fanart,'')

        Common.addItem("[COLOR white][B]Leave Review[/B][/COLOR]",urla+",leavereview_me",164,iconimage,fanart,'')
        Common.addDir("[COLOR white][B]Read Repository Reviews - [COLOR yellowgreen]" + body + " [/COLOR][/B][/COLOR]",urla+",readreview_me",164,iconimage,fanart,'')

def GET_MULTI(name,url):
    
    dp.create(ADDONTITLE, "[COLOR white]We are getting the required information from the relevent repository. Please wait...[/COLOR]")

    kodi_name = Common.GET_KODI_VERSION()
    urla  = url
    try:
        addon_path,repo_path,base_name,url,marker   = urla.split(',')
    except: addon_path,repo_path,base_name,url,disre,marker   = urla.split(',')
    count_id = addon_path
    get_url = url
    service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(addon_path)
    body = urllib2.urlopen(service_url).read()

    ADDON  =  xbmc.translatePath(os.path.join('special://home/addons',addon_path))

    if marker == "info_me":
        url = DESC + addon_path + ".txt"
        content = open_url_desc(url)
        string = str(content)
        if string == "None":
            dialog.ok(ADDONTITLE,"Sorry, there was an error getting the requested information.")
        Common.TextBox('[COLOR yellowgreen][B]ECHO Wizard Addon Installer[/B][/COLOR]',"%s" % string)
    elif marker == "paid_info":
        url = PAID_DESC + addon_path + ".txt"
        content = open_url_desc(url)
        string = str(content)
        if string == "None":
            dialog.ok(ADDONTITLE,"Sorry, there was an error getting the requested information.")
        Common.TextBox('[COLOR yellowgreen][B]ECHO Wizard Addon Installer[/B][/COLOR]',"%s" % string)
    elif marker == "readreview_me":
        Common.List_Addon_Review(addon_path)
    elif marker == "leavereview_me":
        Common.Write_Addon_Review(addon_path)
    elif marker == "uninstall_me":
        dp.create(ADDONTITLE,"[COLOR blue]Removing addon....[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]',' ')   
        dp.update(0,'','',' ')
        try:
            shutil.rmtree(ADDON)
            DISABLE_DATABASE_ADDON(addon_path)
        except: pass
        time.sleep(1)
        xbmc.executebuiltin("UpdateLocalAddons")
        time.sleep(0.5)
        xbmc.executebuiltin("UpdateAddonRepos")
        dp.close()
        dialog.ok(ADDONTITLE,"[COLOR white]" + base_name + " has been successfully removed from your system![/COLOR]")
        xbmc.executebuiltin("Container.Refresh")
    elif marker == "install_me":
        get_dep = 1
        get_addon = 1
        if get_dep == 1:
            try:
                streamurl=[]
                streamname=[]
                streamicon=[]
                link=open_url(DEPENDENCIES)
                urls=re.compile('<title>'+re.escape("Dependencies")+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
                iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(urls)[0]
                links=re.compile('<link>(.+?)</link>').findall(urls)
                i=1
                for sturl in links:
                    sturl2=sturl
                    if '(' in sturl:
                        sturl=sturl.split('(')[0]
                        caption=str(sturl2.split('(')[1].replace(')',''))
                        streamurl.append(sturl)
                        streamname.append(caption)
                        ADDON  =  xbmc.translatePath(os.path.join('special://home/addons/',str(caption)))
                        if not os.path.exists(ADDON):
                            url = str(sturl)
                            url = url.replace("https://","http://")
                            install_name = str("[COLOR yellowgreen][B]" + caption + "[/B][/COLOR]")
                            INSTALL(install_name,url)
                            if kodi_name == "Krypton":
                                ADD_DATABASE_ADDON(caption,"")
                        i=i+1
            except: pass
        if get_addon == 1:
            streamurl=[]
            streamname=[]
            streamicon=[]
            link=open_url(get_url)
            urls=re.compile('<title>'+re.escape(base_name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
            
            if not "<xml>" in urls:
                links=re.compile('<link>(.+?)</link>').findall(urls)
                iconimage=re.compile('<iconimage>(.+?)</iconimage>').findall(urls)[0]
                i=0
                for sturl in links:
                    try:
                        sturl2=sturl
                        if '(' in sturl:
                            sturl=sturl.split('(')[0]
                            caption=str(sturl2.split('(')[1].replace(')',''))
                            streamurl.append(sturl)
                            streamname.append(caption)
                            ADDON2  =  xbmc.translatePath(os.path.join('special://home/addons/',str(caption)))
                            if not "http" in caption:
                                if not os.path.exists(ADDON2):
                                    url = str(sturl)
                                    url = url.replace("https://","http://")
                                    install_name = str("[COLOR yellowgreen][B]" + caption + "[/B][/COLOR]")
                                    INSTALL(install_name,url)
                                    if kodi_name == "Krypton":
                                        if "repo" in caption.lower():
                                            ADD_DATABASE_REPO(repo_path)
                                            time.sleep(1)
                                            ADD_DATABASE_ADDON(repo_path,"")
                                        else:
                                            ADD_DATABASE_ADDON(str(caption),repo_path)
                                    i=i+1
                    except:
                        try:
                            shutil.rmtree(ADDON)
                            shutil.rmtree(REPO)
                        except: pass
                        time.sleep(2)
                        xbmc.executebuiltin("UpdateLocalAddons")
                        time.sleep(2)
                        xbmc.executebuiltin("UpdateAddonRepos")
                        time.sleep(2)
                        dialog.ok(ADDONTITLE,"There was an error installing " + install_name + " please report this to @EchoCoder on Twitter")
                        xbmc.executebuiltin("Container.Refresh")
                        quit()
            else:
        
                xml=re.compile('<xml>(.+?)</xml>').findall(urls)[0]
                zips=re.compile('<zips>(.+?)</zips>').findall(urls)[0]
                get_me=re.compile('<get>(.+?)</get>').findall(urls)
            
                get_me.append(addon_path)
                get_me.append(repo_path)
                for get in get_me:
                    check  =  xbmc.translatePath(os.path.join('special://home/addons/',get))
                    if not os.path.exists(check):
                        repo_data = open_url_normal(xml).replace('\n','').replace('\r','').replace('\t','')
                        version = re.compile('addon id="'+re.escape(get)+'".+?ersion="(.+?)"',re.DOTALL).findall(repo_data)[0]
                        if not zips.endswith("/"):
                            zips = zips + "/"
                        download_me = zips + str(get) + "/" + str(get) + "-" + version + ".zip"

                        install_name = str("[COLOR yellowgreen][B]" + get + "[/B][/COLOR]")
                        INSTALL(install_name,download_me)
                        if kodi_name == "Krypton":
                            if "repo" in get.lower():
                                ADD_DATABASE_REPO(get)
                                time.sleep(1)
                                ADD_DATABASE_ADDON(get,"")
                            else:
                                ADD_DATABASE_ADDON(get,repo_path)
 
        dp.create(ADDONTITLE,"[COLOR blue]Adding the download to the counters[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]',' ')  
        dp.update(0,'','','')
        add_download = Common.add_one(count_id+"ADDON_INSTALLER")
        dp.update(50,'Refreshing kodi addons to finish the installation process.','',' ')
        xbmc.executebuiltin("UpdateLocalAddons")
        xbmc.executebuiltin("UpdateAddonRepos")
        xbmc.executebuiltin("Container.Refresh")
        dp.update(100)
        dp.close

        xbmcgui.Dialog().ok(ADDONTITLE, "[COLOR white]" + base_name + " successfully installed![/COLOR]")

def GET_REPO(name,url):
    
    kodi_name = Common.GET_KODI_VERSION()

    urla  = url
    repo_path,base_name,url,marker   = urla.split(',')
    get_url = url

    service_url = BASEURL + base64.b64decode(b'YXBpL2FwaV9hZGRvbl9yZXZpZXcucGhwP2FjdGlvbj1jb3VudCZidWlsZD0=') + base64.b64encode(repo_path)
    body = urllib2.urlopen(service_url).read()

    REPO  =  xbmc.translatePath(os.path.join('special://home/addons',repo_path))

    if marker == "info_me":
        url = DESC + repo_path + ".txt"
        content = open_url_desc(url)
        string = str(content)
        if string == "None":
            dialog.ok(ADDONTITLE,"Sorry, there was an error getting the requested information.")
            quit()
        Common.TextBox('[COLOR yellowgreen][B]ECHO Wizard Addon Installer[/B][/COLOR]',"%s" % string)
    elif marker == "readreview_me":
        Common.List_Addon_Review(repo_path)
    elif marker == "leavereview_me":
        Common.Write_Addon_Review(repo_path)
    elif marker == "uninstall_me":
        dp.create(ADDONTITLE,"[COLOR blue]Removing addon....[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]',' ')   
        dp.update(0,'','',' ')
        try:
            shutil.rmtree(REPO)
        except: pass
        if kodi_name == "Krypton":
            DISABLE_DATABASE_ADDON(repo_path)
        time.sleep(2)
        xbmc.executebuiltin("UpdateLocalAddons")
        time.sleep(2)
        xbmc.executebuiltin("UpdateAddonRepos")
        time.sleep(2)
        dp.close()
        dialog.ok(ADDONTITLE,"[COLOR white]" + base_name + " has been successfully removed from your system![/COLOR]")
        xbmc.executebuiltin("Container.Refresh")

    elif marker == "install_me":
        streamurl=[]
        streamname=[]
        streamicon=[]
        link=open_url(get_url)
        urls=re.compile('<title>'+re.escape(base_name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
        
        try:
            xml=re.compile('<xml>(.+?)</xml>').findall(urls)[0]
            zips=re.compile('<zips>(.+?)</zips>').findall(urls)[0]
            get_me=re.compile('<repo_path>(.+?)</repo_path>').findall(urls)

            for get in get_me:
                install_name = str("[COLOR yellowgreen][B]" + get + "[/B][/COLOR]")
                check  =  xbmc.translatePath(os.path.join('special://home/addons/',get))
                if not os.path.exists(check):
                    repo_data = open_url_normal(xml)
                    version = re.compile('<addon id="'+re.escape(get)+'".+?version="(.+?)"').findall(repo_data)[0]
                    if not zips.endswith("/"):
                        zips = zips + "/"
                    download_me = zips + str(get) + "/" + str(get) + "-" + version + ".zip"

                    INSTALL(install_name,download_me)
                    if kodi_name == "Krypton":
                        ADD_DATABASE_ADDON(get,get)
        except:
            time.sleep(2)
            xbmc.executebuiltin("UpdateLocalAddons")
            time.sleep(2)
            xbmc.executebuiltin("UpdateAddonRepos")
            time.sleep(2)
            dialog.ok(ADDONTITLE,"There was an error installing " + install_name + " please report this to @EchoCoder on Twitter")
            xbmc.executebuiltin("Container.Refresh")
            quit()  
        dp.create(ADDONTITLE,"[COLOR blue]Adding the download to the counters[/COLOR]",'[COLOR yellow]Please Wait...[/COLOR]',' ')  
        dp.update(0,'','',' ')
        add_download = Common.add_one(repo_path+"ADDON_INSTALLER")
        dp.update(50,'Refreshing kodi addons to finish the installation process.','',' ')
        time.sleep(2)
        xbmc.executebuiltin("UpdateLocalAddons")
        time.sleep(2)
        xbmc.executebuiltin("UpdateAddonRepos")
        time.sleep(2)
        xbmc.executebuiltin("Container.Refresh")
        dp.update(100)
        dp.close

        xbmcgui.Dialog().ok(ADDONTITLE, "[COLOR white]" + base_name + " successfully installed![/COLOR]")

def FILE_MANAGER_SOURCES(name,url,description):
    
    SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))
    original = url
    namelist      = []
    sourcelist    = []
    countlist     = []
    combinedlists = []

    if not os.path.isfile(SOURCES):
        f = open(SOURCES,'w')
        f.write('<sources>\n    <files>\n        <default pathversion="1"></default>\n    </files>\n</sources>')
        f.close()

    f = open(SOURCES,mode='r'); msg = f.read(); f.close()
    i=0
    link = open_url(SOURCES_URL)
    match= re.compile('<item>(.+?)</item>').findall(link)
    for item in match:

        title=re.compile('<title>(.+?)</title>').findall(item)[0]
        source=re.compile('<source>(.+?)</source>').findall(item)[0]

        source = source.replace(" ","")
        
        source_test = open(SOURCES).read().replace('/','')
        url_test    = source.replace('/','')
    
        if not url_test in source_test:
            countlist.append("0")
        else: 
            countlist.append("1")
        namelist.append(title)
        sourcelist.append(source)

        combinedlists = list(zip(countlist,namelist,sourcelist))

    tup = sorted(combinedlists, key=lambda x: int(x[0]),reverse=True)

    marker = 0
    marker2 = 0

    Common.addItem('[COLOR dodgerblue][B]WRITE ALL SOURCES TO FILE MANAGER[/B][/COLOR]',original,178,ICON,FANART,"")
    Common.addItem('[COLOR dodgerblue][B]REMOVE ALL SOURCES FROM FILE MANAGER[/B][/COLOR]',original,178,ICON,FANART,"")

    for counter,name,url in tup:
        if counter == "1":
            url2 = name + '|SPLIT|REMOVE' + url
            if marker == 0:
                Common.addItem('[COLOR darkgray][B]------------------------------------------------[/B][/COLOR]',url2,999,ICON,FANART,"")
                Common.addItem('[COLOR yellowgreen][B]INSTALLED IN FILE MANAGER[/B][/COLOR]',url2,999,ICON,FANART,"")
                marker = 1
            Common.addItem('[COLOR yellowgreen][B]' + name + ' [/B][/COLOR][COLOR white]- ' + url +'[/COLOR]',url2,178,ICON,FANART,"")
        else: 
            url2 = name + '|SPLIT|' + url
            if marker2 == 0:
                Common.addItem('[COLOR darkgray][B]------------------------------------------------[/B][/COLOR]',url2,999,ICON,FANART,"")
                Common.addItem('[COLOR darkgray][B]NOT INSTALLED IN FILE MANAGER[/B][/COLOR]',url2,999,ICON,FANART,"")
                marker2 = 1
            Common.addItem('[COLOR darkgray][B]' + name + ' [/B][/COLOR][COLOR darkgray]- ' + url +'[/COLOR]',url2,178,ICON,FANART,"")

def WRITE_SOURCE_TO_FILE_MANAGER(name,url):

    SOURCES     =  xbmc.translatePath(os.path.join('special://home/userdata','sources.xml'))

    if "WRITE ALL SOURCES TO FILE MANAGER" in name:

        choice = xbmcgui.Dialog().yesno(ADDONTITLE, "[COLOR white]Write all the sources to your File Manager?[/COLOR]", yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
        if choice == 1:
            try:
                link = open_url(SOURCES_URL)
                match= re.compile('<item>(.+?)</item>').findall(link)
                for item in match:

                    name=re.compile('<title>(.+?)</title>').findall(item)[0]
                    source=re.compile('<source>(.+?)</source>').findall(item)[0]
                    source = source.replace(" ","")

                    if not source in open(SOURCES).read():
                        OLD = '<files>\n        <default pathversion="1"></default>'
                        NEW = '<files>\n        <default pathversion="1"></default>\n       <source>\n          <name>'+name+'</name>\n         <path pathversion="1">'+source+'</path>\n           <allowsharing>true</allowsharing>\n     </source>'
                        a=open(SOURCES).read()
                        b=a.replace(OLD, NEW)
                        f= open((SOURCES), mode='w')
                        f.write(str(b))
                        f.close()
                    if not source in open(SOURCES).read():
                        OLD = '<files>\n        <default pathversion="1"></default>'
                        NEW = '<files>\n        <default pathversion="1"></default>\n       <source>\n          <name>'+name+'</name>\n         <path pathversion="1">'+source+'</path>\n           <allowsharing>true</allowsharing>\n     </source>'
                        a=open(SOURCES).read()
                        b=a.replace(OLD, NEW)
                        f= open((SOURCES), mode='w')
                        f.write(str(b))
                        f.close()
            except: 
                dialog.ok(ADDONTITLE, '[COLOR white]Sorry, there was an error writing the source to the file manager.[/COLOR]')
                quit()
        else:
            quit()
    
        xbmc.executebuiltin("RereshSources")

        dialog.ok(ADDONTITLE, '[COLOR white]The sources have been written to your File Manager.', '[COLOR red][B]The Sources will NOT SHOW in the File Manager until Kodi has been restarted. [/B][/COLOR]', 'Thank you for using ECHO Wizard.[/COLOR]')

        xbmc.executebuiltin("Container.Refresh") 
    elif "REMOVE ALL SOURCES FROM FILE MANAGER" in name:
        try:
            os.remove(SOURCES)
            if not os.path.isfile(SOURCES):
                f = open(SOURCES,'w')
                f.write('<sources>\n    <files>\n        <default pathversion="1"></default>\n    </files>\n</sources>')
                f.close()
            xbmc.executebuiltin("Container.Refresh") 
            dialog.ok(ADDONTITLE, '[COLOR white]The sources have been removed from your File Manager.', '[COLOR red][B]The Sources will NOT REFRESH in the File Manager until Kodi has been restarted. [/B][/COLOR]', 'Thank you for using ECHO Wizard.[/COLOR]')
        except:
            xbmc.executebuiltin("Container.Refresh") 
            dialog.ok(ADDONTITLE, '[COLOR white]There was an error removing the sources. Please try again later.','Thank you for using ECHO Wizard.[/COLOR]')
            quit()
    else:
    
        name,source = url.split('|SPLIT|')
        source = source.replace(" ","")
        
        if "remove" in url.lower():
            source = source.replace("REMOVE","")
            
            choice = xbmcgui.Dialog().yesno(ADDONTITLE, "[COLOR white]Remove the following to your File Manager?[/COLOR]","[COLOR white]Name:[/COLOR][COLOR dodgerblue][B]" + name + "[/B][/COLOR]","[COLOR white]Source:[/COLOR][COLOR dodgerblue][B]" + source + "[/B][/COLOR]", yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
            if choice == 1:
                try:
                    OLD = '<source>\n           <name>'+name+'</name>\n         <path pathversion="1">'+source+'</path>\n           <allowsharing>true</allowsharing>\n     </source>'
                    NEW = ''
                    a=open(SOURCES).read()
                    b=a.replace(OLD, NEW)
                    f= open((SOURCES), mode='w')
                    f.write(str(b))
                    f.close()
                    OLD = '     \n'
                    NEW = ''
                    a=open(SOURCES).read()
                    b=a.replace(OLD, NEW)
                    f= open((SOURCES), mode='w')
                    f.write(str(b))
                    f.close()
                except: 
                    dialog.ok(ADDONTITLE, '[COLOR white]Sorry, there was an error removing the source to the file manager.[/COLOR]')
                    quit()
            else:
                quit()

            if source in open(SOURCES).read():
                try:
                    OLD = '<default pathversion="1"></default>\n        <source>\n          <name>'+name+'</name>\n         <path pathversion="1">'+source+'</path>\n           <allowsharing>true</allowsharing>\n     </source>'
                    NEW = '\n'
                    a=open(SOURCES).read()
                    b=a.replace(OLD, NEW)
                    f= open((SOURCES), mode='w')
                    f.write(str(b))
                    f.close()
                    OLD = '     \n'
                    NEW = ''
                    a=open(SOURCES).read()
                    b=a.replace(OLD, NEW)
                    f= open((SOURCES), mode='w')
                    f.write(str(b))
                    f.close()
                except: 
                    dialog.ok(ADDONTITLE, '[COLOR white]Sorry, there was an error removing the source to the file manager.[/COLOR]')
                    quit()
                    
            if source in open(SOURCES).read():
                dialog.ok(ADDONTITLE, '[COLOR white]Sorry, there was an error writing the source to the file manager.[/COLOR]')
                quit()
            
            xbmc.executebuiltin("RereshSources")

            dialog.ok(ADDONTITLE, '[COLOR white]The ' + name + ' source has been removed from your File Manager.', '[COLOR red][B]The Source will NOT SHOW in the File Manager until Kodi has been restarted. [/B][/COLOR]', 'Thank you for using ECHO Wizard.[/COLOR]')

            xbmc.executebuiltin("Container.Refresh") 

        else:

            choice = xbmcgui.Dialog().yesno(ADDONTITLE, "[COLOR white]Write the following to your File Manager?[/COLOR]","[COLOR white]Name:[/COLOR][COLOR dodgerblue][B]" + name + "[/B][/COLOR]","[COLOR white]Source:[/COLOR][COLOR dodgerblue][B]" + source + "[/B][/COLOR]", yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
            if choice == 1:
                try:
                    OLD = '<files>\n        <default pathversion="1"></default>'
                    NEW = '<files>\n        <default pathversion="1"></default>\n       <source>\n          <name>'+name+'</name>\n         <path pathversion="1">'+source+'</path>\n           <allowsharing>true</allowsharing>\n     </source>'
                    a=open(SOURCES).read()
                    b=a.replace(OLD, NEW)
                    f= open((SOURCES), mode='w')
                    f.write(str(b))
                    f.close()
                except: 
                    dialog.ok(ADDONTITLE, '[COLOR white]Sorry, there was an error writing the source to the file manager.[/COLOR]')
                    quit()
            else:
                quit()

            if not source in open(SOURCES).read():
                try:
                    OLD = '<files>\n        <default pathversion="1"></default>'
                    NEW = '<files>\n        <default pathversion="1"></default>\n       <source>\n          <name>'+name+'</name>\n         <path pathversion="1">'+source+'</path>\n           <allowsharing>true</allowsharing>\n     </source>'
                    a=open(SOURCES).read()
                    b=a.replace(OLD, NEW)
                    f= open((SOURCES), mode='w')
                    f.write(str(b))
                    f.close()
                except: 
                    dialog.ok(ADDONTITLE, '[COLOR white]Sorry, there was an error writing the source to the file manager.[/COLOR]')
                    quit()
                    
            if not source in open(SOURCES).read():
                dialog.ok(ADDONTITLE, '[COLOR white]Sorry, there was an error writing the source to the file manager.[/COLOR]')
                quit()
            
            xbmc.executebuiltin("RereshSources")

            dialog.ok(ADDONTITLE, '[COLOR white]The ' + name + ' source has been written to your File Manager.', '[COLOR red][B]The Source will NOT SHOW in the File Manager until Kodi has been restarted. [/B][/COLOR]', 'Thank you for using ECHO Wizard.[/COLOR]')

            xbmc.executebuiltin("Container.Refresh") 

def ADD_DATABASE_ADDON(name,url):

    Enabled = 1
    AddonID = name
    Origen = url

    import datetime
    installDate = str(datetime.datetime.now())[:-7]
 
    import sqlite3

    try:
        log_file = maintenance.grab_Log(True,False)
        
        log_text=open(log_file).read()
        db_version = re.compile('Running database version Addons(.+?)\n').findall(log_text)[0]
        DB_Path = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons'+str(db_version)+'.db'))
    except:
        i = 50
        got_db = 0
        while got_db == 0:
            DB_Path = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons'+str(i)+'.db'))
            if os.path.exists(DB_Path):
                got_db = 1
            else: i = i-1

    conn = sqlite3.connect(DB_Path)
    cursor = conn.cursor()

    try:
        q = """ INSERT INTO installed(addonID,enabled, installDate, origin) VALUES(?, ?, ?, ?) """
        cursor.execute(q, (str(AddonID), str(Enabled), str(installDate), str(Origen)))
        conn.commit()
    except:
        q = """ UPDATE installed SET enabled= ? WHERE addonID = ? """
        cursor.execute(q, (str(Enabled), str(AddonID)))
        conn.commit()
        pass
    
def ADD_DATABASE_REPO(name):

    try:
        Repo_Path = xbmc.translatePath(os.path.join('special://home/addons/', name + '/addon.xml'))
        a=open(Repo_Path).read()
        b=a.replace('\n',' ').replace('\r',' ')
        match=re.compile('version="(.+?)".+?<checksum>(.+?)</checksum>').findall(str(b))
        for version,checksum in match:
            checksum_id = open_url(checksum)
            AddonID = name
            version_id = version

        import datetime
        installDate = str(datetime.datetime.now())[:-7]
    
        import sqlite3

        try:
            log_file = maintenance.grab_Log(True,False)
            
            log_text=open(log_file).read()
            db_version = re.compile('Running database version Addons(.+?)\n').findall(log_text)[0]
            DB_Path = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons'+str(db_version)+'.db'))
        except:
            i = 50
            got_db = 0
            while got_db == 0:
                DB_Path = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons'+str(i)+'.db'))
                if os.path.exists(DB_Path):
                    got_db = 1
                else: i = i-1

        conn = sqlite3.connect(DB_Path)
        cursor = conn.cursor()
     
        q = """ INSERT INTO repo(addonID,checksum, lastcheck, version) VALUES(?, ?, ?, ?) """
        cursor.execute(q, (str(AddonID), "", str(installDate), str(version_id)))
        conn.commit()
    except: pass

def GET_ADDON_DESCRIPTION(name,url,iconimage):

    try:
        get_file = open(KODIAPPS_FILE)
        get_data = get_file.read()  
        link=get_data.replace('<tag></tag>','<tag>null</tag>')
        match=re.compile('<item>(.+?)</item>',re.DOTALL).findall(link)
        for items in match:
            id=re.compile('<tag>(.+?)</tag>').findall(items)[0]    
            url2=re.compile('<link>(.+?)</link>').findall(items)[0]    
            if id in url:
                url3 = url2

        link = Common.OPEN_URL_NORMAL(url3).replace('\n',' ').replace('\r',' ')
        match=re.compile('<h1 style="padding:10px(.+?)</div>',re.DOTALL).findall(link)
        string = str(match)
        heading = re.compile('>(.+?)</h1>').findall(string)[0]
        heading = "[COLOR yellowgreen][B]" + heading + "[/B][/COLOR]"
        content = re.compile('<h4>(.+?)</h4>').findall(string)[0]
        content = content.replace('</li>','\n')
        heading = strip_tags(heading)
        content = strip_tags(content)
        content = content.strip(' ')
        display = heading + "\n\n" + content + "\n\n" + "[B][COLOR blue]Brought to you by Kodiapps.com[/B][/COLOR]"

        Common.TextBox('[COLOR yellowgreen][B]ECHO Wizard Addon Installer[/B][/COLOR]',"%s" % display)
    except:
        dialog.ok(ADDONTITLE, "Sorry, we are unable to get the information at this time. Please try again later.")
        quit()

def GET_KODIAPPS_RANKING_LOCAL(ADDON_ID):

    try:
        if not os.path.isfile(KODIAPPS_FILE):
            open(KODIAPPS_FILE, 'w')

        fileCreation = os.path.getmtime(KODIAPPS_FILE)

        now = time.time()
        check = now - 60*60
        
        text_file = open(KODIAPPS_FILE)
        compfile = text_file.read()  
        
        if len(compfile) == 0:
            counts=Common.OPEN_URL_NORMAL("http://kodiapps.com/echos.xml")

            text_file = open(KODIAPPS_FILE, "w")
            text_file.write(counts)
            text_file.close()

        elif fileCreation < check:

            counts=Common.OPEN_URL_NORMAL("http://kodiapps.com/echos.xml")

            text_file = open(KODIAPPS_FILE, "w")
            text_file.write(counts)
            text_file.close()

        get_file = open(KODIAPPS_FILE)
        get_data = get_file.read()  
        found = 0
        link=get_data.replace('<tag></tag>','<tag>null</tag>')
        match=re.compile('<item>(.+?)</item>',re.DOTALL).findall(link)
        for items in match:
            id=re.compile('<tag>(.+?)</tag>').findall(items)[0]    
            rank=re.compile('<rank>(.+?)</rank>').findall(items)[0]    

            if ADDON_ID.lower() == id.lower():
                found = 1
                return "[COLOR yellowgreen]" + rank + "[/COLOR]"
        
        if found == 0:
            return "0"

    except: return "0"

def DISABLE_DATABASE_ADDON(name):

    Enabled = 0
    AddonID = name

    import sqlite3

    i = 50
    got_db = 0
    while got_db == 0:
        DB_File = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons'+str(i)+'.db'))
        if os.path.exists(DB_File):
            got_db = 1
        else: i = i-1

    DB_Path = DB_File 
    conn = sqlite3.connect(DB_Path)
    cursor = conn.cursor()
 
    try:
        q = """ UPDATE installed SET enabled= ? WHERE addonID = ? """
        cursor.execute(q, (str(Enabled), str(AddonID)))
        conn.commit()
    except: pass

def INSTALL(name, url):

    dp.close()
    #Check is the packages folder exists, if not create it.
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    if not os.path.exists(path):
        os.makedirs(path)
    dp.create(ADDONTITLE,"","","[COLOR white][B]Installing: [/B][/COLOR]" + str(name))

    lib=os.path.join(path, 'addon.zip')
    
    try:
        os.remove(lib)
    except:
        pass

    dialog = xbmcgui.Dialog()
    try:
        downloader.download(url, lib, dp)
    except:
        downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://home','addons'))
    time.sleep(2)
    dp.update(0,"","Extracting Zip Please Wait"," ")
    unzip(lib,addonfolder,dp)
    time.sleep(1)
    try:
        os.remove(lib)
    except:
        pass
    dp.close()

def GET_COUNTS():

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

    if not os.path.isfile(TEMP_FILE):
        text_file = open(TEMP_FILE, 'w')
        text_file.close()

    fileCreation = os.path.getmtime(TEMP_FILE)

    now = time.time()
    check = now - 60*mark
    
    text_file = open(TEMP_FILE)
    compfile = text_file.read()  
    text_file.close()

    if len(compfile) == 0:
        counts=Common.OPEN_URL_NORMAL(ECHO_API)

        text_file = open(TEMP_FILE, "w")
        text_file.write(counts)
        text_file.close()

    elif fileCreation < check:

        counts=Common.OPEN_URL_NORMAL(ECHO_API)

        text_file = open(TEMP_FILE, "w")
        text_file.write(counts)
        text_file.close()

def unzip(_in, _out, dp):
    __in = zipfile.ZipFile(_in,  'r')
    
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
                dp.update(int(update),'','','[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
                __in.extract(item, _out)
            
            except Exception, e:
                print str(e)

    except Exception, e:
        print str(e)
        return False
        
    return True 

def open_url_normal(url):

    try:
        if "github" in url:
            if "https" in url:
                url = url.replace("https","http")
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('\n',' ').replace('\r',' ')
        return link
    except: 
        dialog.ok(ADDONTITLE, "[COLOR red][B]There was an error connecting to the requested URL.[/B][/COLOR]", "[COLOR yellowgreen][I]Please try again later.[/I][/COLOR]")
        quit()

def open_url(url):

    try:
        if "github" in url:
            if "https" in url:
                url = url.replace("https","http")
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('\n',' ').replace('\r',' ')
        return link
    except: 
        dialog.ok(ADDONTITLE, "[COLOR red][B]There was an error connecting to the requested URL.[/B][/COLOR]", "[COLOR yellowgreen][I]Please try again later.[/I][/COLOR]")
        quit()
        
def open_url_desc(url):

    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
    except: 
        dialog.ok(ADDONTITLE, "[COLOR red][B]There was an error connecting to the requested URL.[/B][/COLOR]", "[COLOR yellowgreen][I]Please try again later.[/I][/COLOR]")
        quit()

def PARENTAL_CONTROLS():

    found = 0
    if not os.path.exists(PARENTAL_FILE):
        found = 1
        Common.addDir("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,ICON,FANART,'')
        Common.addDir("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",160,ICON,FANART,'')
    else:
        vers = open(PARENTAL_FILE, "r")
        regex = re.compile(r'<password>(.+?)</password>')
        for line in vers:
            file = regex.findall(line)
            for current_pin in file:
                password = base64.b64decode(current_pin)
                found = 1
                Common.addDir("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR yellowgreen]ON[/B][/COLOR]","url",999,ICON,FANART,'')
                Common.addDir("[COLOR yellow][B]Current Password - [/COLOR][COLOR orangered]" + str(password) + "[/B][/COLOR]","url",999,ICON,FANART,'')
                Common.addDir("[COLOR yellowgreen][B]Change Password[/B][/COLOR]","url",160,ICON,FANART,'')
                Common.addDir("[COLOR red][B]Disable Password[/B][/COLOR]","url",161,ICON,FANART,'')

    if found == 0:
        Common.addDir("[COLOR blue][B]PARENTAL CONTROLS - [/COLOR][COLOR red]OFF[/B][/COLOR]","url",999,ICON,FANART,'')
        Common.addDir("[COLOR yellow][B]Setup Parental Password[/B][/COLOR]","url",160,ICON,FANART,'')

def PARENTAL_CONTROLS_PIN():

    vq = Common._get_keyboard( heading="Please Set Password" )
    if ( not vq ):
        dialog.ok(ADDONTITLE,"Sorry, no password was entered.")
        quit()
    pass_one = vq

    vq = Common._get_keyboard( heading="Please Confirm Your Password" )
    if ( not vq ):
        dialog.ok(ADDONTITLE,"Sorry, no password was entered.")
        quit()
    pass_two = vq
        
    if not os.path.exists(PARENTAL_FILE):
        if not os.path.exists(PARENTAL_FOLDER):
            os.makedirs(PARENTAL_FOLDER)
        open(PARENTAL_FILE, 'w')

        if pass_one == pass_two:
            writeme = base64.b64encode(pass_one)
            f = open(PARENTAL_FILE,'w')
            f.write('<password>'+str(writeme)+'</password>')
            f.close()
            dialog.ok(ADDONTITLE,'Your password has been set and parental controls have been enabled.')
            xbmc.executebuiltin("Container.Refresh")
        else:
            dialog.ok(ADDONTITLE,'The passwords do not match, please try again.')
            quit()
    else:
        os.remove(PARENTAL_FILE)
        
        if pass_one == pass_two:
            writeme = base64.b64encode(pass_one)
            f = open(PARENTAL_FILE,'w')
            f.write('<password>'+str(writeme)+'</password>')
            f.close()
            dialog.ok(ADDONTITLE,'Your password has been set and parental controls have been enabled.')
            xbmc.executebuiltin("Container.Refresh")
        else:
            dialog.ok(ADDONTITLE,'The passwords do not match, please try again.')
            quit()

def PARENTAL_CONTROLS_OFF():

    try:
        os.remove(PARENTAL_FILE)
        dialog.ok(ADDONTITLE,'Parental controls have been disabled.')
        xbmc.executebuiltin("Container.Refresh")
    except:
        dialog.ok(ADDONTITLE,'There was an error disabling the parental controls.')
        xbmc.executebuiltin("Container.Refresh")

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