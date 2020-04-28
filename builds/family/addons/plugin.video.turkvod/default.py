# -*- coding: utf-8 -*-
import os
import xbmc, xbmcaddon, xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import time
import re
from htmlentitydefs import name2codepoint as n2cp
import httplib
import urlparse
import threading
import socket
from urllib2 import Request, URLError, urlopen
from datetime import datetime
from urlparse import parse_qs
from urllib import unquote_plus
from resources import TURKvodKodiPrsr

thisPlugin = int(sys.argv[1])
addonId = "plugin.video.turkvod"
dataPath = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
busystring = xbmc.getLocalizedString(503).encode("utf8")

try:
    from os import path, system
    if not path.exists(dataPath):
        cmd = "mkdir -p " + dataPath
        system(cmd)
except:
    pass
	   
addon = xbmcaddon.Addon(id=addonId)
adultPIN = addon.getSetting("adultPIN")       
adultPINonoff = addon.getSetting( "adultPINonoff" )
serverId = addon.getSetting( "serverId" )
listegorunumu = addon.getSetting( "listegorunumu" )
mac_id = addon.getSetting( "mac" )
s_key = addon.getSetting( "security_key" )
downloadonoff = addon.getSetting( "downloadonoff" )


def get_runtime_path():
    return xbmc.translatePath(addon.getAddonInfo('Path'))

def sec_to_hms(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


if mac_id == "":
    try:
        from os import path
        if path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"):
            try:
                from Components.Network import iNetwork
                ifaces = iNetwork.getConfiguredAdapters()
                mac_id = iNetwork.getAdapterAttribute(ifaces[0], 'mac')
                addon.setSetting('mac', mac_id)
            except:
                pass
        else:
            mac_id = xbmc.getInfoLabel('Network.MacAddress')
            i = 1
            while mac_id == busystring:
                print "while: %s" % i
                i = i+1
                mac_id = xbmc.getInfoLabel('Network.MacAddress') 
                time.sleep(1)
                if i == 10:
                    break
            addon.setSetting('mac', mac_id)	
    except:
        pass
		

mac = mac_id+'_'+TURKvodKodiPrsr.VER	
TURKVOD_PARSER = TURKvodKodiPrsr.turkvod_parsers()
TRModules = TURKvodKodiPrsr.modules()

if addon.getSetting('serverId') == "1":
    server = 'co'
elif addon.getSetting('serverId') == "2":
    server = 'site'
else:
    server = 'org'
if addon.getSetting('listegorunumu') == "true":
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
else:
    pass
Host = 'http://turkvod.' + server + '/10/kodik.php'
		
def Url_Al(url, mac = None):
    sign = '?'
    url = url.strip(' \t\n\r')
    if url.find('?') > -1:
        sign = '&'
    if mac != None:
        security_key = s_key
        security_param = ""
        url = url + sign + 'box_mac=' + mac + '&key=' + security_key
    if url.find('|') > -1:
        parts = url.split('|')
        url = parts[0]
        cookie = parts[1]
        req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 TURKvod-10 Kodi',
        'Connection': 'Close',
        'Cookie': cookie})
    else:
        req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 TURKvod-10 Kodi',
        'Connection': 'Close'})
    xmlstream = urllib2.urlopen(req).read()
    return xmlstream
	
def Anamenu():
    content = Url_Al(Host, mac)
    start = 0
    i = 0
    while i < 100:
        n1 = content.find("<channel>", start)
        if n1 < 0:
            break
        n2 = content.find("</channel>", start)
        if n2 < 0:
            break
        ch = content[n1:n2]
        regexvideo = '<title>(.*?)</title>.*?description>.*?>(.*?)</description>.*?<playlist_url>(.*?)</playlist_url>'
        match = re.compile(regexvideo,re.DOTALL).findall(ch)
        name = match[0][0]
        name = name.replace("<![CDATA[", "")
        name = name.replace("]]>", "")
        url = match[0][2]
        url = url.replace("<![CDATA[", "")
        url = url.replace("]]>", "")
        pic = ""
        description = match[0][1]
        description = description.replace("]]>", "")
        ListeyeEkle(name, {"name":name, "url":url, "mode":1}, pic, description)
        start = n2+5       
        i = i+1
    xbmcplugin.endOfDirectory(thisPlugin)

def Liste(name, url):
    if "/aramalar/" in url and 'aramalar_list.php' not in url:
        Ara(url)
    if "TEXT" in name:
        ModuldeAra(url)
    if "TURKvod%20HAKKINDA" in name or "TURKvod%20AYARLAR" in name or "TURKvod%20TEST%20IPTV" in name or "%2b18" in name or "erotik" in url or "yetiskin" in url or "Erotik" in url or "Yetiskin" in url:
        if adultPINonoff == "true":			
            if path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"):
                pin = adultPIN
                if pin != "1234":
                    return
            else:            
                k = xbmc.Keyboard('', 'PIN i giriniz') ; k.doModal()
                pin = k.getText() if k.isConfirmed() else None
                if pin != adultPIN:
                    return
        if adultPINonoff == "false":
            pass
    else:
        pass
		
    if url.endswith(".m3u") or "type=m3u" in url:
        content = Url_Al(url, mac)
        regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
        match = re.compile(regexcat,re.DOTALL).findall(content)
        for name, url in match:
            name = name.replace("\n", "")
            name = name.replace("\r", "")
            url = url.replace(" ", "")
            url = url.replace("\n", "")
            url = url.replace("\r", "")
            pic = ""
            ListeyeEkle(name, {"name":name, "url":url, "mode":3}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)
		
    if "TRModules" in url:
        try:
            url = url.replace('TRModules@', '')
            iptv_list_temp = TRModules.get_list(url)
            next_page_url = TRModules.next_page_url
            next_page_text = TRModules.next_page_text
            prev_page_url = TRModules.prev_page_url
            prev_page_text = TRModules.prev_page_text
            search_text = TRModules.search_text
            search_on = TRModules.search_on
            playlistname = TRModules.playlistname
            content = iptv_list_temp
            if "@start" in url or "@category" in url or "@film" in url: 
                for trm in range(len(content)): 
                    name_s = content[trm][1]
                    url_s = content[trm][5]
                    if content[trm][7] == None:
                        pic = ''
                    else:
                        pic = content[trm][7]
                    if content[trm][2] == None:
                        description = ''
                    else:
                        description = content[trm][2]
                    ListeyeEkle(name_s, {"name":name_s, "url":url_s, "mode":1}, pic, description)
            if "@parts" in url: 
                for trm in range(len(content)):
                    mode = 2
                    name_p = content[trm][1]
                    url_p = content[trm][4]
                    if url_p == None :
                        url_p = content[trm][5]
                        mode = 1
                    if content[trm][7] == None:
                        pic = ''
                    else:
                        pic = content[trm][7]
                    if content[trm][2] == None:
                        description = ''
                    else:
                        description = content[trm][2]
                    ListeyeEkle(name_p, {"name":name_p, "url":url_p, "mode":mode}, pic, description)
                xbmcplugin.endOfDirectory(thisPlugin)
            if next_page_url :
                name_n = "Next page..."
                nex_url = next_page_url
                pic = ""
                ListeyeEkle(name_n, {"name":name_n, "url":nex_url, "mode":1}, pic)		
            xbmcplugin.endOfDirectory(thisPlugin)
        except:
            pass
    else:
        if "AYARLAR" in name:
            addon.openSettings()
            xbmc.executebuiltin('Container.Refresh')
            return
    
        elif "LOKAL" in name:
            try:
                try:
                    lokal = os.path.join(os.path.join("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"), 'TURKvodLokal.xml' )
                    url = lokal
                    f = open(url,'r')
                    data2 = f.read().replace("\n\n", "")
                    f.close()
                    content = data2
                except:
                    lokal = os.path.join(os.path.join(dataPath), 'TURKvodLokal.xml' )
                    url = lokal
                    f = open(url,'r')
                    data2 = f.read().replace("\n\n", "")
                    f.close()
                    content = data2
            except:
                url = 'http://turkvod.' + server + '/10/TURKvodLokal.xml'
                content = Url_Al(url, mac)
        else:
            content = Url_Al(url, mac)
        start = 0
        i = 0
        while i < 100000:
            n1 = content.find("<channel>", start)
            if n1 < 0:
                break
            n2 = content.find("</channel>", start)
            if n2 < 0:
                break
            ch = content[n1:n2]
                    
            if "<stream_url>" in ch: 
                name = re.findall('<title>(.*?)</title>', ch, re.IGNORECASE)[0]
                url = re.findall('<stream_url>(.*?)</stream_url>', ch, re.IGNORECASE)[0]
                try:
                    pic = re.findall('<description><\!\[CDATA\[<img src=[\'|"](.*?)[\'|"]', ch, re.IGNORECASE)[0]
                except:
                    pic = ''
                try:
                    description = re.findall('<description><\!\[CDATA\[<img src=[\'|"].*?[\'|"].*?>(.*?)</description>', ch, re.IGNORECASE)[0]
                except:
                    description = ''
                name = name.replace("<![CDATA[", "")
                name = name.replace("]]>", "")
                name = name.replace("\n", "")
                name = name.replace("\r", "")
                url = url.replace("<![CDATA[", "")
                url = url.replace("]]>", "")
                url = url.replace("TURKvodModul@", "")
                url = url.replace("@m3u@TURKvod", "")
                description = description.replace("]]>", "")			
                ListeyeEkle(name, {"name":name, "url":url, "mode":2}, pic, description)
                            
            elif "<playlist_url>" in ch: 
                name = re.findall('<title>(.*?)</title>', ch, re.IGNORECASE)[0]
                url = re.findall('<playlist_url>(.*?)</playlist_url>', ch, re.IGNORECASE)[0]
                try:
                    pic = re.findall('<description><\!\[CDATA\[<img src=[\'|"](.*?)[\'|"]', ch, re.IGNORECASE)[0]
                except:
                    pic = ''
                try:
                    description = re.findall('<description><\!\[CDATA\[<img src=[\'|"].*?[\'|"].*?>(.*?)</description>', ch, re.IGNORECASE)[0]
                except:
                    description = ''
                name = name.replace("<![CDATA[", "")
                name = name.replace("]]>", "")
                name = name.replace("\n", "")
                name = name.replace("\r", "")
                url = url.replace("<![CDATA[", "")
                url = url.replace("]]>", "")
                url = url.replace("TURKvodModul@", "")
                url = url.replace("@m3u@TURKvod", "")
                description = description.replace("]]>", "")			
                ListeyeEkle(name, {"name":name, "url":url, "mode":1}, pic, description)
            else:
                pass
            start = n2+5       
            i = i+1
        if "<next_page_url" in content:
            regexvideo = '<next_page_url.*?http(.*?)\]'
            match = re.compile(regexvideo,re.DOTALL).findall(content)
            name = "Next page..."
            url = "http" + match[0]
            pic = ""
            ListeyeEkle(name, {"name":name, "url":url, "mode":1}, pic)
        xbmcplugin.endOfDirectory(thisPlugin)

def Ara(url):
    k = xbmc.Keyboard('', 'Search') ; k.doModal()
    query = k.getText() if k.isConfirmed() else None
    url = url + "?search=" + query.replace(' ','+')
    name = query
    pic = ""
    ListeyeEkle(name, {"name":name, "url":url, "mode":4}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def ModuldeAra(url):
    k = xbmc.Keyboard('', 'Search') ; k.doModal()
    query = k.getText() if k.isConfirmed() else None
    site = re.findall('site=(.*?)$', url, re.IGNORECASE)[0]	
    url = "http://turkvod.xyz/10/aramalar/moduldeara.php?site="+site+"&search=" + query.replace(' ','+')
    name = query
    pic = ""
    ListeyeEkle(name, {"name":name, "url":url, "mode":4}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)
	
def Aramasonucu(name1, url):
    content = Url_Al(url, mac)
    start = 0
    i = 0
    while i < 1000:
        n1 = content.find("<channel>", start)
        if n1 < 0:
              break
        n2 = content.find("</channel>", start)
        if n2 < 0:
              break
        ch = content[n1:n2]
        if "<stream_url>" in ch: 
            name = re.findall('<title>(.*?)</title>', ch, re.IGNORECASE)[0]
            url = re.findall('<stream_url>(.*?)</stream_url>', ch, re.IGNORECASE)[0]
            try:
                pic = re.findall('<description><\!\[CDATA\[<img src=[\'|"](.*?)[\'|"]', ch, re.IGNORECASE)[0]
            except:
                pic = ''
            try:
                description = re.findall('<description><\!\[CDATA\[<img src=[\'|"].*?[\'|"].*?>(.*?)</description>', ch, re.IGNORECASE)[0]
            except:
                description = ''
            name = name.replace("<![CDATA[", "")
            name = name.replace("]]>", "")
            name = name.replace("\n", "")
            name = name.replace("\r", "")
            url = url.replace("<![CDATA[", "")
            url = url.replace("]]>", "")
            url = url.replace("TURKvodModul@", "")
            url = url.replace("@m3u@TURKvod", "")
            description = description.replace("]]>", "")			
            ListeyeEkle(name, {"name":name, "url":url, "mode":2}, pic, description)
			
        elif "<playlist_url>" in ch: 
            name = re.findall('<title>(.*?)</title>', ch, re.IGNORECASE)[0]
            url = re.findall('<playlist_url>(.*?)</playlist_url>', ch, re.IGNORECASE)[0]
            try:
                pic = re.findall('<description><\!\[CDATA\[<img src=[\'|"](.*?)[\'|"]', ch, re.IGNORECASE)[0]
            except:
                pic = ''
            try:
                description = re.findall('<description><\!\[CDATA\[<img src=[\'|"].*?[\'|"].*?>(.*?)</description>', ch, re.IGNORECASE)[0]
            except:
                description = ''
            name = name.replace("<![CDATA[", "")
            name = name.replace("]]>", "")
            name = name.replace("\n", "")
            name = name.replace("\r", "")
            url = url.replace("<![CDATA[", "")
            url = url.replace("]]>", "")
            url = url.replace("TURKvodModul@", "")
            url = url.replace("@m3u@TURKvod", "")
            description = description.replace("]]>", "")			
            ListeyeEkle(name, {"name":name, "url":url, "mode":1}, pic, description)
        else:
            pass				   
        start = n2+5       
        i = i+1
    if "<next_page_url" in content:
        regexvideo = '<next_page_url.*?http(.*?)\]'
        match = re.compile(regexvideo,re.DOTALL).findall(content)
        name = "Next page..."
        url = "http" + match[0]
        pic = ""
        ListeyeEkle(name, {"name":name, "url":url, "mode":4}, pic)
    xbmcplugin.endOfDirectory(thisPlugin)

def VideoListe(name, url):
    play_url = TURKVOD_PARSER.get_parsed_link(url)
    if (play_url == []) or (play_url == ""):
        play_url = url
        Oynat(name, url)
    else:
        if type(play_url) == str:
            url = play_url
            Oynat(name, url)
        elif type(play_url) == tuple:
            names = []
            urls = []
            names = play_url[2]
            urls = play_url[1]
            if names == []:
                pic = ""
                url = url
                name = name
                Oynat(name, url)
            else:       
                i = 0
                for name in names:
                    pic = ""
                    url = urls[i]
                    i = i+1
                    ListeyeEkle(name, {"name":name, "url":url, "mode":3}, pic)
                xbmcplugin.endOfDirectory(thisPlugin)  

def download_and_play(url,file_name,download_path):
    download_thread = DownloadThread(url,file_name,download_path)
    download_thread.start()
    while True:
        cancelled=False
        dialog = xbmcgui.DialogProgress()
        dialog.create('Indiriliyor...', 'Oynatmaya baslamak icin iptal e basin')
        dialog.update(0)

        while not cancelled and download_thread.isAlive():
            dialog.update( download_thread.get_progress() , "Indirirken oynatmak icin iptal e basin", "Indirme durumu: "+str(int(download_thread.get_speed()/1024))+" KB/s "+str(download_thread.get_actual_size())+"MB de "+str(download_thread.get_total_size())+"MB" , "Kalan sure: "+str( sec_to_hms(download_thread.get_remaining_time())) )
            xbmc.sleep(1000)
            if dialog.iscanceled():
                cancelled=True
                break

        dialog.close()
        player = CustomPlayer()
        player.set_download_thread(download_thread)
        player.PlayStream( download_thread.get_file_name() )
        if player.is_stopped():
            print("[download_and_play.py] Kullanici tarafindan iptal edildi")
            break
        else:
            if not download_thread.isAlive():
                print("[download_and_play.py] Indirme bitti")
                break
            else:
                print("[download_and_play.py] Indirme devam ediyor")

    if download_thread.isAlive():
        print("[download_and_play.py] Killing download thread")
        download_thread.force_stop()


class CustomPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        self.actualtime=0
        self.totaltime=0
        self.stopped=False
        xbmc.Player.__init__( self )

    def PlayStream(self, url):  
        self.play(url)
        self.actualtime=0
        self.url=url
        while self.isPlaying():
            self.actualtime = self.getTime()
            self.totaltime = self.getTotalTime()
            xbmc.sleep(3000)

    def set_download_thread(self,download_thread):
        self.download_thread = download_thread

    def force_stop_download_thread(self):
        if self.download_thread.isAlive():
            self.download_thread.force_stop()
            #while self.download_thread.isAlive():
            #    xbmc.sleep(1000)

    def onPlayBackStarted(self):
        print("CustomPlayer.onPlayBackStarted PLAYBACK STARTED")

    def onPlayBackEnded(self):
        print("CustomPlayer.onPlayBackEnded PLAYBACK ENDED")

    def onPlayBackStopped(self):
        print("CustomPlayer.onPlayBackStopped PLAYBACK STOPPED")
        self.stopped=True
        self.force_stop_download_thread()

    def is_stopped(self):
        return self.stopped

class DownloadThread(threading.Thread):
    
    def __init__(self, url, file_name, download_path):
        self.url = url
        self.download_path = download_path
        self.file_name = os.path.join( download_path , file_name )
        self.progress = 0
        self.force_stop_file_name = os.path.join( self.download_path , "force_stop.tmp" )
        self.velocidad=0
        self.tiempofalta=0
        self.actual_size=0
        self.total_size=0
        if os.path.exists(self.force_stop_file_name):
            os.remove(self.force_stop_file_name)

        threading.Thread.__init__(self)

    def run(self):
        if "megacrypter.com" in self.url:
            self.download_file_megacrypter()
        else:
            self.download_file()

    def force_stop(self):
        force_stop_file = open( self.force_stop_file_name , "w" )
        force_stop_file.write("0")
        force_stop_file.close()

    def get_progress(self):
        return self.progress;

    def get_file_name(self):
        return self.file_name

    def get_speed(self):
        return self.velocidad

    def get_remaining_time(self):
        return self.tiempofalta

    def get_actual_size(self):
        return self.actual_size

    def get_total_size(self):
        return self.total_size

    def download_file_megacrypter(self):
        comando = "./megacrypter.sh"
        oldcwd = os.getcwd()
        cwd = os.path.join( get_runtime_path() , "tools")
        os.chdir(cwd)
        os.system( comando+" '"+self.url+ "' \"" + self.download_path+"\"" )
        os.chdir(oldcwd)

    def download_file(self):
        headers=[]
        self.file_name = xbmc.makeLegalFilename(self.file_name)   
        existSize = 0
        f = open(self.file_name, 'wb')
        grabado = 0

        if "|" in self.url:
            additional_headers = self.url.split("|")[1]
            if "&" in additional_headers:
                additional_headers = additional_headers.split("&")
            else:
                additional_headers = [ additional_headers ]
    
            for additional_header in additional_headers:
                name = re.findall( "(.*?)=.*?" , additional_header )[0]
                value = urllib.unquote_plus(re.findall( ".*?=(.*?)$" , additional_header )[0])
                headers.append( [ name,value ] )
    
            self.url = self.url.split("|")[0]
    
        socket.setdefaulttimeout(60)

        h=urllib2.HTTPHandler(debuglevel=0)
        request = urllib2.Request(self.url)
        for header in headers:
            request.add_header(header[0],header[1])
        opener = urllib2.build_opener(h)
        urllib2.install_opener(opener)
        try:
            connexion = opener.open(request)
        except urllib2.HTTPError,e:
            f.close()
            if e.code==416:
                return 0
            else:
                return -2
    
        try:
            totalfichero = int(connexion.headers["Content-Length"])
        except:
            totalfichero = 1

        self.total_size = int(float(totalfichero) / float(1024*1024))
        blocksize = 100*1024
        bloqueleido = connexion.read(blocksize)
        maxreintentos = 10

        while len(bloqueleido)>0:
            try:
                if os.path.exists(self.force_stop_file_name):
                    f.close()
                    xbmc.executebuiltin((u'XBMC.Notification("Iptal ediliyor..", "Arka planda indirme iptal ediliyor", 300)'))
                    return

                f.write(bloqueleido)
                grabado = grabado + len(bloqueleido)
                percent = int(float(grabado)*100/float(totalfichero))
                self.progress=percent;
                totalmb = float(float(totalfichero)/(1024*1024))
                descargadosmb = float(float(grabado)/(1024*1024))
                self.actual_size = int(descargadosmb)
                reintentos = 0
                while reintentos <= maxreintentos:
                    try:

                        before = time.time()
                        bloqueleido = connexion.read(blocksize)
                        after = time.time()
                        if (after - before) > 0:
                            self.velocidad=len(bloqueleido)/((after - before))
                            falta=totalfichero-grabado
                            if self.velocidad>0:
                                self.tiempofalta=falta/self.velocidad
                            else:
                                self.tiempofalta=0
                        break
                    except:
                        reintentos = reintentos + 1
                        for line in sys.exc_info():
                            print ( "%s" % line )
                
                if reintentos > maxreintentos:
                    f.close()
                    return -2
    
            except:
                import traceback,sys
                exc_type, exc_value, exc_tb = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_tb)
                for line in lines:
                    line_splits = line.split("\n")
                    for line_split in line_splits:
                        print(line_split)

                f.close()
                return -2
        return
        
def Oynat(name, url):
    url = url.replace('#', '|')
    if path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"): # enigma2 Kodidirect
        pic = "DefaultFolder.png"
        li = xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=pic)
        player = xbmc.Player()
        player.play(url, li)
    else:
        if ".ts" in url: 
            import F4mProxy
            from F4mProxy import f4mProxyHelper
            player=f4mProxyHelper()
            player.playF4mLink(url, name, streamtype='TSDOWNLOADER')
        if ".m3u8" in url: 
            pic = "DefaultFolder.png"
            li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=pic)
            player = xbmc.Player()
            player.play(url, li)
        else:
            if downloadonoff == "true":		
                if addon.getSetting('save_location') == "":
                    xbmc.executebuiltin("XBMC.Notification('TURKvod','Video indirme klasorunu seciniz.',5000,)")
                    addon.openSettings()
                dialog = xbmcgui.Dialog()
                ret = dialog.yesno('Download', 'Video indirilsin mi?\n\nNot: Bu pencerenin cikmasini istemiyorsaniz\nayarlardan kapatabilirsiniz.')
                if ret:
                    today = datetime.now().strftime('[%d.%m_%H:%M:%S]')
                    filename = today + name + '.mp4'
                    download_and_play(url, filename, addon.getSetting("save_location"))
                    return
            pic = "DefaultFolder.png"
            li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=pic)
            player = xbmc.Player()
            player.play(url, li)

def ListeyeEkle(name, parameters={},pic="", description = ""):
    li = xbmcgui.ListItem(name)
    li.setArt({'thumb': pic, 'icon': pic, 'fanart': pic})
    li.setInfo(type = 'video', infoLabels={'plot': description})
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True)

def Parametreler(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = Parametreler(sys.argv[2])
name =  str(params.get("name", ""))
url =  str(params.get("url", ""))
url = urllib.unquote(url)
mode =  str(params.get("mode", ""))

if not sys.argv[2]:
    ok = Anamenu()
else:
    if mode == str(1):
        ok = Liste(name, url)
    elif mode == str(2):
        ok = VideoListe(name, url)
    elif mode == str(3):
        ok = Oynat(name, url)
    elif mode == str(4):
        ok = Aramasonucu(name, url)