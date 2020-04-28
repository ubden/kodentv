# -*- coding: utf-8 -*-
import urllib, urllib2, os, io, xbmc, xbmcaddon, xbmcgui, json, re, base64, xbmcvfs

AddonID = 'plugin.video.kodilivetv'
Addon = xbmcaddon.Addon(AddonID)
icon = Addon.getAddonInfo('icon')
AddonName = Addon.getAddonInfo("name")
addonDir = Addon.getAddonInfo('path')
chanDir = os.path.join(addonDir, 'resources', 'channels')
localizedString = Addon.getLocalizedString

def OpenURL(url, headers={}, user_data={}, justCookie=False):
    
    try:
        pw = False
        if url.find("@")>0 and not url.find("tp.srgssr.ch")>-1:
            
            URL1 = url.split("@")[0]
            
            if url.startswith("http"):
                nurl = "http://" + url.split("@")[1]
            else:
                nurl = "https://" + url.split("@")[1]
                
            URL1 = url.replace("http://","").replace("https://","")
            us = URL1.split(":")[0]
            pw = URL1.split(":")[1]
            pw = pw.split("@")[0]
            url = nurl
        
        req = urllib2.Request(url)
        if pw:
            base64string = base64.encodestring('%s:%s' % (us, pw)).replace('\n', '')
            req.add_header("Authorization", "Basic %s" % base64string)
        
        if len(headers)<1:
            req.add_header('User-Agent', 'Kodi Live TV')
            req.add_header('referer', url)
        
        for k, v in headers.items():
                req.add_header(k, v)
                xbmc.log("OpenURL --> req.add_header('"+k+"', '"+v+"')")
                
        response = urllib2.urlopen(req, timeout=20)
        
        if justCookie == True:
                if response.info().has_key("Set-Cookie"):
                        data = response.info()['Set-Cookie']
                else:
                        data = None
        else:
                data = response.read().replace("\r", "")
        
        response.close()
        return data
    except:
        xbmc.log(url + " <-- OpenURL fail connection!!")
        return ""
        pass

def ReadFile(fileName):    
    try:
        f = open(fileName,'r')
        content = f.read().replace("\n\n", "\n")
        f.close()
    except:
        content = ""

    return content
	
def ReadList(fileName):
  
    try:
        with open(fileName, 'r') as handle:
            content = json.load(handle)
    except:
        content=[]

    return content

def SaveList(filname, list):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    try:
        with io.open(filname, 'w', encoding='utf-8') as handle:
                handle.write(unicode(json.dumps(list, indent=4, ensure_ascii=False)))
        success = True
    except Exception as ex:
        print ex
        success = False
            
    return success

def OKmsg(title, line1, line2 = None, line3 = None):
    dlg = xbmcgui.Dialog()
    dlg.ok(title, line1, line2, line3)
	

def m3u2list(url):
    if check_url(url):
        response = OpenURL(url)
    else:
        if not os.path.isfile(os.path.join(chanDir ,url)):
            url = url.replace(os.path.join(chanDir) + "/","")
            url = url.replace(os.path.join(chanDir) + "\\","")
            try:
                url = base64.decodestring(url)
                response = OpenURL(url)
            except:
                url = ""
                response = ""
                pass
        else:    
            response = ReadFile(url)
		
    matches=re.compile('^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)$',re.I+re.M+re.U+re.S).findall(response)
    li = []
    for params, display_name, url in matches:
        item_data = {"params": params, "display_name": display_name, "url": url}
        li.append(item_data)

    list = []
    for channel in li:
        item_data = {"params": channel["params"], "display_name": channel["display_name"], "url": channel["url"]}
        matches=re.compile(' (.+?)="(.+?)"',re.I+re.M+re.U+re.S).findall(channel["params"])
        for field, value in matches:
            item_data[field.strip().lower().replace('-', '_')] = value.strip()
        list.append(item_data)
    return list
	
def GetEncodeString(string):
    try:
        import chardet
        string = string.decode(chardet.detect(string)["encoding"]).encode("utf-8")
    except:
        pass
    return string

def DelFile(filname):
    try:
        if os.path.isfile(filname):
            os.unlink(filname)
    except Exception as e:
        print e

def BBTagRemove(string):
    string = re.sub(r"\[/COLOR]|\[COLOR.*?]","",string)
    string = re.sub(r"\[/B]|\[B]","",string)
    string = re.sub(r"\[/I]|\[I]","",string)
    string = re.sub(r"\[/UPPERCASE]|\[UPPERCASE]","",string)
    string = re.sub(r"\[/LOWERCASE]|\[LOWERCASE]","",string)
    string = re.sub(r"\[/LIGHT]|\[LIGHT]","",string)
    string = re.sub(r"\[/CAPITALIZE]|\[CAPITALIZE]","",string)
    return string

        
def Open_Netflix():
    import subprocess, sys
    xbmc.audioSuspend()
    ret = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.getSettingValue", "params": {"setting":"screensaver.mode" } }')
    jsn = json.loads(ret)
    saver_mode = jsn['result']['value']
    xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method":"Settings.setSettingValue", "params": {"setting":"screensaver.mode", "value":""} } ' )
    browser = xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('browser')
    if 'linux' in sys.platform:
        if browser == "Chrome" :
            CHROME = os.path.join('/', 'opt', 'google', 'chrome', 'google-chrome')
            if not os.path.isfile(CHROME): CHROME = os.path.join('/', 'usr', 'bin', 'google-chrome')
            subprocess.call([CHROME , '--start-maximized','--disable-translate','--disable-new-tab-first-run','--no-default-browser-check','--no-first-run','--kiosk','--app=https://www.netflix.com/browse'])
            #process = subprocess.Popen(os.path.join(os.path.join(addonDir),"chrome.sh"), shell=True)
        else :
            CHROMIUM = os.path.join('/', 'usr', 'bin', 'chromium')
            if not os.path.isfile(CHROMIUM): CHROMIUM = os.path.join('/', 'usr', 'bin', 'chromium-browser')
            subprocess.call([CHROMIUM , '--start-maximized','--disable-translate','--disable-new-tab-first-run','--no-default-browser-check','--no-first-run','--kiosk','--app=https://www.netflix.com/browse'])
            #process = subprocess.Popen(os.path.join(os.path.join(addonDir),"chromium.sh"), shell=True)
        #process.wait()
    if 'win32' in sys.platform:
        if browser == "Chrome" :
            process = subprocess.Popen(os.path.join(os.path.join(addonDir),"chrome.cmd"), shell=True)
        else :
            process = subprocess.Popen(os.path.join(os.path.join(addonDir),"iexplore.cmd"), shell=True)
        process.wait()
    if 'darwin' in sys.platform:
        CHROME = os.path.join('/', 'Applications', 'Google Chrome.app', 'Contents', 'MacOS', 'Google Chrome')
        subprocess.call([CHROMIUM , '--start-fullscreen','--kiosk','https://www.netflix.com/browse'])
        #process = subprocess.Popen(os.path.join(os.path.join(addonDir),"darwin.sh"), shell=True)
        #process.wait()
    xbmc.audioResume()
    xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.SetSettingValue", "params": {"setting":"screensaver.mode", "value": "'+saver_mode+'" } }')

def Open_Paypal():
    import subprocess, sys, json
    xbmc.audioSuspend()
    ret = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.getSettingValue", "params": {"setting":"screensaver.mode" } }')
    jsn = json.loads(ret)
    saver_mode = jsn['result']['value']
    xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method":"Settings.setSettingValue", "params": {"setting":"screensaver.mode", "value":""} } ' )
    browser = xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('browser')
    if 'linux' in sys.platform:
        if browser == "Chrome" :
            CHROME = os.path.join('/', 'opt', 'google', 'chrome', 'google-chrome')
            if not os.path.isfile(CHROME): CHROME = os.path.join('/', 'usr', 'bin', 'google-chrome')
            subprocess.call([CHROME , '--start-maximized','--disable-translate','--disable-new-tab-first-run','--no-default-browser-check','--no-first-run','--kiosk','--app=http://paypal.me/kodilivetv'])
            #process = subprocess.Popen(os.path.join(os.path.join(addonDir),"chrome.sh"), shell=True)
        else :
            CHROMIUM = os.path.join('/', 'usr', 'bin', 'chromium')
            if not os.path.isfile(CHROMIUM): CHROMIUM = os.path.join('/', 'usr', 'bin', 'chromium-browser')
            subprocess.call([CHROMIUM , '--start-maximized','--disable-translate','--disable-new-tab-first-run','--no-default-browser-check','--no-first-run','--kiosk','--app=http://paypal.me/kodilivetv'])
            #process = subprocess.Popen(os.path.join(os.path.join(addonDir),"chromium.sh"), shell=True)
        #process.wait()
    if 'win32' in sys.platform:
        if browser == "Chrome" :
            process = subprocess.Popen(os.path.join(os.path.join(addonDir),"offer.cmd"), shell=True)
        else :
            process = subprocess.Popen(os.path.join(os.path.join(addonDir),"offeri.cmd"), shell=True)
        process.wait()
    if 'darwin' in sys.platform:
        CHROME = os.path.join('/', 'Applications', 'Google Chrome.app', 'Contents', 'MacOS', 'Google Chrome')
        subprocess.call([CHROMIUM , '--start-fullscreen','--kiosk','http://paypal.me/kodilivetv'])
    xbmc.audioResume()
    xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Settings.SetSettingValue", "params": {"setting":"screensaver.mode", "value": "'+saver_mode+'" } }')

def check_url(url):
    import urlparse
    parts = urlparse.urlsplit(url)
    if not parts.scheme or not parts.netloc:
        return False
    else:
        return True

def cachelist(url,cdir,tcache=108000):
    
    TempName = base64.standard_b64encode(url)
    tmp = os.path.join(cdir, TempName)
    
    list = [ ]
    
    if check_url(url):
        import time
        if os.path.isfile(tmp):
            t = time.time() - os.path.getmtime(tmp)
        else :
            t = 0
        
	if os.path.isfile(tmp) and t < tcache:
            list = m3u2list(tmp)
        else :
            try:
                surl,playheaders=url.split('|')
                content = OpenURL(surl)
            except:
                content = OpenURL(url)
            
            if len(content)>0:
                try:
                    write_file(tmp, content)
                    list = m3u2list(tmp)
                except:
                    pass
            
            if len(list)<1:
                list = m3u2list(url)
    else:            
        list = m3u2list(url)        
    
    return list    
        
def find_param(pattern,data):
    
    try:
        result = re.search(pattern,data)
        return result.group(1)
    except:
        return ""
 
def pornHD(url):

    response = cachepage(url,200000,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
    urlvideo = re.search("'720p' *: *'([^',]+)", response)
    return urlvideo.group(1)

def urhd_list():
    
    from bs4 import BeautifulSoup
    
    data = cachepage("http://urhd.tv",300,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
    soup = BeautifulSoup(data, "html.parser")
    channels_tag = soup.find_all("channels")
    
    result = []
    for tag in channels_tag:
        json_str = tag.attrs[":channels"]
        channel_list = json.loads(json_str)
        result.extend(channel_list)
    
    return result

def find_lpanel(url):
    
    username = ""
    password = ""
    
    if url.find("get.php?username=")>0:
        
        server = url.split("/")[-2]
        username = find_param("username=([^,]+)&password=",url)
        password = find_param("password=([^,]+)&type=",url)
        
    else:
        if check_url(url):
            list = OpenURL(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
        else:
            list = ReadFile(url)
         
        string = find_param("http://([^,]+).ts",list)
        
        if not len(string)>0:
            string = find_param("http://([^,]+).m3u8",list)
            if not len(string)>0:
                string = find_param("http://([^,]+).mkv",list)
                if not len(string)>0:
                    string = find_param("http://([^,]+).avi",list)
        
        xbmc.log("----:" + string)
        xbmc.log("----:" + url)
        xbmc.log("----:" + str(len(list)))
        
        server = string.split("/")[-5]
        username = string.split("/")[-3] 
        password = string.split("/")[-2]

    if not username == "" and not password == "":
        link = "http://" + server + "/panel_api.php?username=" + username + "&password=" + password
        return link
    else:
        return ""

def urhd(url):
    list = cachepage(url,86380,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko'})
    urlvideo = re.search("file: *'([^',]+)",list)
    return urlvideo.group(1)
        
def entitiesfix(string):
    
    string = string.replace("&aacute","&aacute;")
    string = string.replace("&agrave","&agrave;")
    string = string.replace("&eacute","&eacute;")
    string = string.replace("&egrave","&egrave;")
    string = string.replace("&iacute","&iacute;")
    string = string.replace("&igrave","&igrave;")
    string = string.replace("&oacute","&oacute;")
    string = string.replace("&ograve","&ograve;")
    string = string.replace("&uacute","&uacute;")
    string = string.replace("&ugrave","&ugrave;")
    string = string.replace("&Aacute","&Aacute;")
    string = string.replace("&Agrave","&Agrave;")
    string = string.replace("&Eacute","&Eacute;")
    string = string.replace("&Egrave","&Egrave;")
    string = string.replace("&Iacute","&Iacute;")
    string = string.replace("&Igrave","&Igrave;")
    string = string.replace("&Oacute","&Oacute;")
    string = string.replace("&Ograve","&Ograve;")
    string = string.replace("&Uacute","&Uacute;")
    string = string.replace("&Ugrave","&Ugrave;")
    string = string.replace("&uuml"  ,"&uuml;")
    string = string.replace("&Uuml"  ,"&Uuml;")
    string = string.replace("&ntilde","&ntilde;")
    string = string.replace("&#191"  ,"&#191;")
    string = string.replace("&#161"  ,"&#161;")
    string = string.replace(";;"     ,";")
    return string

def decodeHtmlentities(string):
    string = entitiesfix(string)
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()
                
    return entity_re.subn(substitute_entity, string)[0]

########################
# Funzioni Download

def TestDownload(name):
    
    size1 = os.stat(name).st_size
    for x in range(0, 4):
        xbmc.sleep(1200)
        size2 = os.stat(name).st_size
        if not size1 == size2:
            return False
            break
    return True

def StartDowloader(url,name,mode,DFolder):
    
    origurl = None
    urlp = url
    if url.find("pornhd.com")>0:
        origurl = url
        url = pornHD(url)
        urlp = url
        try:
            urlp = urlp.split("?")[-2]
        except:
            pass
    
        ext = urlp.split('.')[-1]
    else:
        url1 = url
        try:
            url1 = url.split('?')[-2]
        except:
            pass
        
        ext = url1.split('.')[-1]
    
    if len(ext)<2 or len(ext)>4: 
        ext = "mp4" 
    
    if urlp.find("openload.co")>0:
        if mode == 6:
            LEN = len(name)-4
            name = name[0:LEN]               
    
    DF = xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('download_path')
    
    if not DF=='':  
        dpath = DF
    else:    
        dpath = DFolder
 
    res = None
    
    if mode == 6:
        res = 'yes'
 
    import fileDownloader
    file = dpath + name + '.' + ext
    xbmc.log("Download URL --> " + str(url))
    xbmc.log("Download file --> " + str(file))
    downloader = fileDownloader.DownloadFile( url , file, origurl = origurl, res = res)
    
    notifica = 2
    loc1 = file + ".resume"
    loc2 = file + ".stopped"
           
    if os.path.isfile(loc2) and (mode == 7 or mode == 6):
        try:
            os.rename(loc2,loc1)
        except:
            pass
    
    if os.path.isfile(file):
        size = os.stat(file).st_size
    else:
        size = 0
       
    if os.path.isfile( file ) and size>0:
        if not mode == 59:
            Resume = TestDownload( file )
            if  Resume:
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10211).encode('utf-8'), 5000, icon))
                xbmc.executebuiltin("XBMC.Container.Refresh()")
                downloader.resume()
                notifica = 2
            else:
                notifica = 1
        else:
            downloader.resume()
    else:
        downloader.download()
      
    if notifica == 1:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10210).encode('utf-8'), 5000, icon))
    else:
        fullsize = size
        
        if os.path.isfile(loc1):
            fsize = ReadFile(loc1).replace("\r","").split("\n")
            fullsize = int(fsize[0])
            
        if not int(size)==fullsize:
            xbmc.sleep(1000)
            xbmc.log("$$$  --  Download Retry --  $$$")
            xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.video.kodilivetv/?url=' + urllib.quote_plus(urlp) + '&name=' + name + '&mode=59)')
        else:
            if os.path.isfile(loc1):
                os.remove(loc1)
                xbmc.log("***  Download Complete ***")
                if not size == 0:
                    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10209).encode('utf-8'), 6000, icon))
                else:
                    if not urlp.find("vizplay.org")>0 and not urlp.find("openload.co")>0:
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, 'ERROR : file not found!', 6000, icon))
                        if os.path.isfile(file):
                            os.remove(file)
                    else:
                        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10209).encode('utf-8'), 6000, icon))

def StopDowloader(url,name,mode,DFolder):
    
    if url.find("pornhd.com")>0:
        url = pornHD(url)
        urlp = url
        try:
            urlp = urlp.split("?")[-2]
        except:
            pass
    
        ext = urlp.split('.')[-1]
    else:
        ext = url.split('.')[-1]
    
    if len(ext)<2 or len(ext)>4: 
        ext = "mp4"  
            
    if not xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('download_path') == "":
        dpath = xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('download_path')
    else:
        dpath = DFolder
    
    file = dpath + name + '.' + ext
    loc1 = file + ".resume"
    loc2 = file + ".stopped"
    try:
        os.rename(loc1,loc2)
    except:
        try:
            os.rename(loc2,loc1)
        except:
            pass
        
    xbmc.sleep(200)
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10208).encode('utf-8'), 6000, icon))
    if mode == 57:
        xbmc.executebuiltin("XBMC.Container.Refresh()")
        
def DeletePartialDowload(url,name,mode,DFolder):
    
    return_value = xbmcgui.Dialog().yesno(localizedString(10045).encode('utf-8'), localizedString(10046).encode('utf-8') + " " + name + "?")

    if not return_value == 0:
    
        if url.find("pornhd.com")>0:
            
            url = pornHD(url)
            urlp = url
            try:
                urlp = urlp.split("?")[-2]
            except:
                pass
        
            ext = urlp.split('.')[-1]
        else:
            ext = url.split('.')[-1]
        
        if len(ext)<2 or len(ext)>4: 
            ext = "mp4"
            
        if not xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('download_path') == "":
            dpath = xbmcaddon.Addon('plugin.video.kodilivetv').getSetting('download_path')
        else:
            dpath = DFolder
        
        try:
            file = os.path.join(dpath + name + '.' + ext)
            if os.path.isfile(file):
                xbmcvfs.delete(file)
            if os.path.isfile(file + ".stopped"):
                os.remove(file + ".stopped")
            if os.path.isfile(file + ".resume"):
                os.remove(file + ".resume") 
            if mode == 58:
                xbmc.executebuiltin("XBMC.Container.Refresh()")
            
            xbmc.sleep(800)
            if xbmcvfs.exists(file):
                xbmc.sleep(2000)
            if xbmcvfs.exists(file):
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10201).encode('utf-8'), 6700, icon))
            else:    
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10200).encode('utf-8'), 6700, icon))
        except:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10201).encode('utf-8'), 6700, icon))
            
def DeleteFile(url,name):
    
    return_value = xbmcgui.Dialog().yesno(localizedString(10045).encode('utf-8'), localizedString(10046).encode('utf-8') + " " + name + "?")

    if not return_value == 0:

        try:
            file = os.path.join(url)
            xbmcvfs.delete(file)
            if os.path.isfile(file + ".stopped"):
                os.remove(file + ".stopped")
            if os.path.isfile(file + ".resume"):
                os.remove(file + ".resume")
            
            xbmc.executebuiltin("XBMC.Container.Refresh()")
            xbmc.sleep(800)
            if xbmcvfs.exists(file):
                xbmc.sleep(2000)
            if xbmcvfs.exists(file):
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10201).encode('utf-8'), 6700, icon))
            else:    
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10200).encode('utf-8'), 6700, icon))
        except:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(name, localizedString(10201).encode('utf-8'), 6700, icon))

def url_to_SOD(url,name,server,action='play'):
    
    name = BBTagRemove(name)
    
    try:
        if type(url)== str:
            url = unicode(url,"utf8", "ignore").encode("utf8")
        else:
            url = url.encode("utf8")
    
        if type(name)== str:
            name = unicode(name,"utf8", "ignore").encode("utf8")
        else:
            name = name.encode("utf8")
    except:
        pass
    
    query =  '{"subtitle": "", "contentSeason": "", "extra": "", "duration": 0, "contentSerieName": "", "fulltitle": "' +name+'", "hasContentDetails": "false", "category": "", "contentEpisodeNumber": "", "title":"' +name+ '", "fanart": "/home/vania/.kodi/addons/plugin.video.kodilivetv/fanart.jpg", "show": "", "contentChannel": "list", "folder": false, "type": "", "thumbnail": "", "channel": "seriehd", "contentType": "", "contentEpisodeTitle": "", "plot": "", "contentTitle": "", "viewmode": "list", "password": "", "contentPlot": "", "language": "", "url": "' +url+ '", "contentThumbnail": "", "server": "' + server +'", "context": "", "action": "' +action+ '"}'
    query = urllib.quote(base64.b64encode(query))
    urltos = "plugin://plugin.video.streamondemand/?" + query
    xbmc.sleep(200)
    xbmc.executebuiltin('Dialog.Close(all, true)')
    xbmc.executebuiltin("xbmc.RunPlugin("+urltos+")")

def write_file(file_name, file_contents):
    fh = None
    try:
        fh = open(file_name, "wb")
        fh.write(file_contents)
        return True
    except:
        return False
    finally:
	if fh is not None:
	    fh.close()

def cachepage( url, s, headers={} ):
    
    import time
    
    t = 0
    content = ""
    
    cdir = os.path.join(xbmc.translatePath("special://temp"),"files")
    TempName = base64.standard_b64encode(url.replace("?","Z"))
    tmp = os.path.join(cdir, TempName)
    
    if os.path.isfile(tmp):
        t = time.time() - os.path.getmtime(tmp)
    
    if t > s or not os.path.isfile(tmp):
        content = OpenURL(url, headers)
        content = content.replace("   "," ").replace("  "," ").replace("  "," ").replace("\t"," ")
        
        if len(content) > 0 :
            write_file(tmp, content)
            xbmc.sleep(300)
            xbmc.log('Write temp file : ' + tmp + ' - size : ' + format( len(content) ) )    
    else:
        content = ReadFile(tmp)
        
    return content
