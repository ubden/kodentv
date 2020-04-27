# -*- coding: utf-8 -*-
import sys
import urllib,urllib2
import re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import json, base64
import hashlib
import os.path
import time
import inspect
from contextlib import closing
from xbmcvfs import File

def get_url(url):
    req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 seyirTURK__KODI', 'Betty': 'jughead', 'Connection': 'Close'})
    page = urllib2.urlopen(req).read()
    return page

class MyPlayerOld(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        xbmc.Player.__init__( self )
        self.s = 0
        self.isfirst = 1
        self.curPos = 0
            
    def newplay(self, playlist,s,m_id,isFragman,isTv="0"):  
        self.play(playlist)
        self.s = s
        self.m_id = m_id
        self.isFragman = isFragman
        while self.isPlaying():
            xbmc.sleep(100)
            try:
                self.curPos = int(self.getTime())
            except:
                a=1
            try:
                self.total = int(self.getTotalTime())
            except:
                pass
                
    def __del__(self) :
        self.user_id = int(settings.getSetting( "user_id" ))
        root1 = settings.getSetting('root')
        if self.user_id != 0 and self.curPos > 100 and self.m_id !=0 :
            self.mili = self.curPos * 1000
            self.toplam = self.total * 1000
            self.percent = 100*self.mili/self.toplam
            if self.percent > 95:
                self.isDone = '1'
            else:
                self.isDone = '0'
            if  isTv == "0":
                self.ur = root1 + "save.php?type=s&u_id=" + str(self.user_id) + "&m_id=" + str(self.m_id) +"&mili=" + str(self.mili)
            else:
                self.ur = root1 + "save.php?isTv=1&type=s&u_id=" + str(self.user_id) + "&m_id=" + str(self.m_id) +"&mili=" + str(self.mili) + '&isDone=' + self.isDone
            if not self.isFragman:
                req = urllib2.Request(self.ur, None, {'User-agent': 'Mozilla/5.0 seyirTURK__KODI','Betty': 'jughead', 'Connection': 'Close'})
                page = urllib2.urlopen(req).read()

    def onPlayBackStarted(self):
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        if self.isfirst == 1 :
            self.isfirst = 0
            if self.s !=0 :
                self.seekTime(self.s)


class MyPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        xbmc.Player.__init__( self )
        self.s = 0
        self.isfirst = 1
        self.curPos = 0
            
    def newplay(self, playlist,s,m_id,isFragman,isTv="0"):  
        self.play(playlist)
        self.s = s
        self.m_id = m_id
        self.isFragman = isFragman
        while self.isPlaying():
            xbmc.sleep(100)
            try:
                self.curPos = int(self.getTime())
            except:
                a=1
            try:
                self.total = int(self.getTotalTime())
            except:
                pass
                
    def __del__(self) :
        self.user_id = int(settings.getSetting( "user_id" ))
        root1 = settings.getSetting('root')
        if self.user_id != 0 and self.curPos > 100 and self.m_id !=0 :
            self.mili = self.curPos * 1000
            self.toplam = self.total * 1000
            self.percent = 100*self.mili/self.toplam
            if self.percent > 95:
                self.isDone = '1'
            else:
                self.isDone = '0'
            if  isTv == "0":
                self.ur = root1 + "save.php?type=s&u_id=" + str(self.user_id) + "&m_id=" + str(self.m_id) +"&mili=" + str(self.mili)
            else:
                self.ur = root1 + "save.php?isTv=1&type=s&u_id=" + str(self.user_id) + "&m_id=" + str(self.m_id) +"&mili=" + str(self.mili) + '&isDone=' + self.isDone
            if not self.isFragman:
                req = urllib2.Request(self.ur, None, {'User-agent': 'Mozilla/5.0 seyirTURK__KODI','Betty': 'jughead', 'Connection': 'Close'})
                page = urllib2.urlopen(req).read()

    def onAVStarted(self):
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        if self.isfirst == 1 :
            self.isfirst = 0
            if self.s !=0 :
                self.seekTime(self.s)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname.decode('utf-8'), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


m_id = 0
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
settings = xbmcaddon.Addon(id='plugin.video.seyirTURK')
IMAGES_PATH = xbmc.translatePath(os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'media'))
ADDON_PATH =  xbmc.translatePath(os.path.join(xbmcaddon.Addon().getAddonInfo('path')))
__addonuserdata__    = xbmc.translatePath( settings.getAddonInfo('profile') )
osInfo = xbmc.getInfoLabel('System.OSVersionInfo')
i = 1
while osInfo == xbmc.getLocalizedString(503).encode("utf8"):
    i = i+1
    osInfo = xbmc.getInfoLabel('System.OSVersionInfo') 
    time.sleep(1)
    if i == 10:
        break
sysInfo = xbmc.getInfoLabel('System.FriendlyName')
if not settings.getSetting( "recorded_date") or settings.getSetting('recorded_date')== "01-01-2020":
    settings.setSetting('recorded_date', xbmc.getInfoLabel('System.Date(dd-mm-yyyy)'))
    
vidName = xbmc.getInfoLabel('Container.PluginName')
vidName = xbmcaddon.Addon(vidName).getAddonInfo('name')
dialog = xbmcgui.Dialog()
if settings.getSetting('uclugorunum') == "true":
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
tc = md5(xbmc.translatePath(os.path.join(ADDON_PATH, 'icon.png')))
def macaddress():
    try:
        if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite"):
            try:
                from Components.Network import iNetwork
                ifaces = iNetwork.getConfiguredAdapters()
                mac_id = iNetwork.getAdapterAttribute(ifaces[0], 'mac')
                settings.setSetting('mac_add', mac_id)
            except:
                pass
        else:
            mac_id = xbmc.getInfoLabel('Network.MacAddress')
            i = 1
            while mac_id == xbmc.getLocalizedString(503).encode("utf8"):
                i = i+1
                mac_id = xbmc.getInfoLabel('Network.MacAddress') 
                time.sleep(1)
                if i == 10:
                    break
            settings.setSetting('mac_add', mac_id)
    except:
        settings.setSetting('mac_add', '00:00:00:00:00:00')

if not settings.getSetting('mac_add') or settings.getSetting('mac_add')=="":
    macaddress()


def Basla():

        root1 = root()
        settings.setSetting('root', root1) 
        root1 = settings.getSetting('root')
        if settings.getSetting( "mail" ) and settings.getSetting( "sifre" ) :
            if not settings.getSetting( "user_id" ) :
                resp = root1 + "user.php?type=join&email=" + settings.getSetting( "mail" ) +"&pass=" + settings.getSetting( "sifre" )
                membership = get_url(resp) 
                if int(membership) > 0: 
                    settings.setSetting('user_id', membership)
                    showMessage('[COLOR orange][B]Sisteme giriş yapıldı.[/B][/COLOR]')
                elif int(membership) == -2:
                    uyeol = root1 + "user.php?type=add&email=" + settings.getSetting( "mail" ) +"&pass=" + settings.getSetting( "sifre" )
                    uyeolpage =get_url(uyeol)
                    settings.setSetting('user_id', uyeolpage)
                    showMessage('[COLOR orange][B]Üyelik başarılı.[/B][/COLOR]')
                elif int(membership) == -4:
                    showMessage('[COLOR orange][B]Şifreniz yanlış.[/B][/COLOR]') 
        elif not settings.getSetting( "mail" ) or not settings.getSetting( "sifre" ) : 
            settings.setSetting('user_id', '')
        if 'http' in settings.getSetting('m3u'):
            try:
                v = get_url(settings.getSetting('m3u'))
                if '#EXTINF' in v:
                    vv= open(os.path.join(__addonuserdata__,"gecici.m3u"), "w+")
                    vv.write(v)
            except:
                pass

        with closing(File(os.path.join(ADDON_PATH, "addon.xml"))) as fo:
            text = fo.read()
        surum = re.findall('version="(.*?)"',text)[1]
        tokens=root1.split('/')
        root2= '/'.join(tokens[:-2])
        url = root2 + '/kodi/main.php?surum=' + surum + '&mac=' + settings.getSetting('mac_add') + '&ct=' + tc
        surum_kontrol = get_url(url)
        if 'eski_surum' in surum_kontrol :
            key = dialog.yesno('[COLOR orange][B]seyirTURK Kodi[/B][/COLOR]', '\n[COLOR yellow]Güncelleme[/COLOR] bulundu, yapmanız önerilir. Şimdi yapmazsanız daha sonra güncellemeyi el ile yapmanız gerekecektir. Güncellemeyi yapmak için [COLOR blue] [B]Evet[/B][/COLOR] e basınız.', yeslabel='Evet', nolabel='Hayır')
            if key == 1:
                try:
                    ico = xbmc.translatePath("special://home/addons/plugin.video.seyirTURK/resources/media/seyir.png") 
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('XBMC.Notification([COLOR orange][B]seyirTURK Kodi[/B][/COLOR], Güncelleniyor bir - iki dakika kadar surebilir. ,4000,' + ico + ')')
                    xbmc.executebuiltin('Action(Back)')
                    xbmc.executebuiltin("UpdateLocalAddons")
                    xbmc.executebuiltin("UpdateAddonRepos")
                except:
                    ok = dialog.ok("[COLOR orange][B]seyirTURK Kodi[/B][/COLOR]", "\nGüncelleme başarısız oldu! Lütfem eklentiyi kendiniz güncelleyiniz.")

            else:
                ok = dialog.ok("[COLOR orange][B]seyirTURK Kodi[/B][/COLOR]", "\nLütfem eklentiyi kendiniz güncelleyiniz.")
        else:
            try:
                mesaj_page = get_url(root2 + '/mesaj.json')
                mesaj_json = json.loads(mesaj_page)
                mesaj = mesaj_json["message"][0]["mesaj"]
                flag = mesaj_json["message"][0]["flag"]
                if not settings.getSetting("message") or settings.getSetting("message") == "":
                    settings.setSetting('message', flag)
                if settings.getSetting("message") != flag:
                    ok1 = dialog.ok("[COLOR orange][B]seyirTURK Kodi[/B][/COLOR] Mesajınız var !", mesaj)
                    settings.setSetting('message', flag)
            except:
                pass
            listele(url)
            
def ayarlar():
    __settings__ = xbmcaddon.Addon(id='plugin.video.seyirTURK')
    __settings__.openSettings()  
def listele(url):
        root1 = settings.getSetting('root')  
        searchstring=""
        if "?name" in url or '&name' in url:
                key = dialog.select('[COLOR orange][B]seyirTURK Kodi[/B][/COLOR]', ['[B]Hepsi[/B]', '[B]Türkçe Dublaj[/B]', '[B]Türkçe Altyazı[/B]', '[B]Almanca Dubla[/B]j'])
                keyboard = xbmc.Keyboard( '', "Film Arama", False )
                keyboard.doModal()
                if ( keyboard.isConfirmed() ):
                        searchstring = keyboard.getText().replace(" ", "%20")
                if key== 0:
                    substring = ''
                elif key == 1:
                    substring = '&lang=DUB'
                elif key ==2:
                    substring = '&lang=SUB'
                else:
                    substring = '&lang=GER'
                url = url.replace('name=', 'name=' + searchstring + substring)
        if 'type=fav' in url or 'type=user' in url or 'type=history' in url:
            if settings.getSetting( "user_id" ):
                url = url + settings.getSetting( "user_id" )
            else :
                ok = dialog.ok("[COLOR orange][B]seyirTURK Kodi[/B][/COLOR]","Girmek istediğiniz yer için lütfen ayarlardan kullanıcı girişi yapınız.")
                url = "bos"

        else :
            pass

        
        if url!="bos" :
            if "adult" in url or "%2b18" in url or "erotik" in url or "yetiskin" in url or "Erotik" in url or "Yetiskin" in url:
                if settings.getSetting( "isAdult" ) == "true":			
                    k = xbmc.Keyboard('', 'Yetişkin Şifresini Giriniz') ; k.doModal()
                    pin = k.getText() if k.isConfirmed() else None
                    if pin != settings.getSetting( "isAdultkey" ):
                        url='/'.join(settings.getSetting('root').split('/')[:-2]) + '/kodi/main.php'

            else:
                pass
            if url.startswith('http'):
                if settings.getSetting('m3u') == url:
                    try:
                        url11 = os.path.join(__addonuserdata__,"gecici.m3u" )
                        cc = open(url11,'r')
                        data1 = cc.read()
                        cc.close()
                        f = data1
                    except:
                        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Girdiğiniz linkte m3u bulunamadı![/B][/COLOR]")
                        f = ""
                else:
                    f = get_url(url)

            else:
                url1 = os.path.join(__addonuserdata__, settings.getSetting('m3u') )
                c = open(url1,'r')
                data = c.read()
                c.close()
                f = data

            if "movies" in f and not 'm3u' in url:
                    js = json.loads(f)
                    idx = '0'
                    for rs in js['movies']:
                            language = ''
                            try:
                                language_int = rs['Language']
                                if language_int == "6":
                                    language = "[COLOR grey] TA - TD - GE[/COLOR]"
                                elif language_int == "5":
                                    language = "[COLOR yellow] TD - GE[/COLOR]"
                                elif language_int == "4":
                                    language = "[COLOR purple] TA - GE[/COLOR]"
                                elif language_int == "3":
                                    language = "[COLOR orange] GE[/COLOR]"
                                elif language_int == "2":
                                    language = "[COLOR blue] TA - TD[/COLOR]"
                                elif language_int == "1":
                                    language = "[COLOR green] TD[/COLOR]"
                                elif language_int == "0":
                                    language = "[COLOR red] TA[/COLOR]"
                            except:
                                pass
                            baslik = rs['Name'] + language
                            resim = rs['Image']
                            try:
                                fanart = rs["Backdrop"]
                            except:
                                fanart = resim
                            try:
                                imdbscore = rs["IMDBScore"]
                            except:
                                imdbscore = 'NA'
                            try:
                                releasedate = rs["ReleaseDate"]
                            except:
                                releasedate = 'NA'
                            try:
                                try:
                                    if settings.getSetting('uclugorunum') == "true":
                                        desc = '[COLOR green][B]IMDB: ' + imdbscore +'[/COLOR][COLOR blue] Tarih: ' + releasedate + '[/COLOR][/B]\n' + rs['Summary']
                                        if  'turler.php' in url or 'turlerdizi.php' in url or 'diziler.php' in url or 'filmler.php' in url :
                                            desc = rs['Summary'] 
                                    else:
                                        desc = '[COLOR orange][B]' + baslik.replace(' TD','').replace(' TA','').replace(' TA - TD',''.replace(" GE","") ).replace("-","") + '[/B][/COLOR]' + '\n' +'[COLOR green][B]IMDB: ' + imdbscore +'[/COLOR][COLOR blue] Tarih: ' + releasedate + '[/COLOR][/B]\n' + rs['Summary']
                                        if  'turler.php' in url or 'turlerdizi.php' in url or 'diziler.php' in url or 'filmler.php' in url :
                                            desc = '[COLOR orange][B]' + baslik.replace(' TD','').replace(' TA','').replace(' TA - TD',''.replace(" GE","") ).replace("-","") + '[/B][/COLOR]' + '\n' + rs['Summary'] 
                                            
                                except:
                                    desc = None
                                idx = str(rs['ID'])
                                try :
                                    tip = rs["Type"]
                                except:
                                    tip ='Yok'
                                try:
                                    sign ='?'
                                    if '?' in rs['Link']:
                                        sign = '&'
                                    link = rs['Link']  + sign + 'mac=' + settings.getSetting('mac_add')  + '&ct=' + tc
                                except:
                                    if tip == 'Movie' or tip == 'yok':
                                        link = root1 + 'streams.php?id=' + idx
                                    else:
                                        link = root1 + 'episodes.php?id=' + idx + '&u_id=' + settings.getSetting( "user_id" )
                                if 'show.php?type=user' in url:
                                    addDir('[COLOR orange][B][COLOR blue]# [/COLOR]'+ baslik +'[/B][/COLOR]',urllib.quote_plus(link),2,resim, idx, desc, None)

                                else:
                                    if not 'type=random' in url:
                                        addDir('[COLOR orange][B][COLOR blue]* [/COLOR]'+ baslik +'[/B][/COLOR]',urllib.quote_plus(link),2,resim,idx, desc, None, fanart)
                                    else:
                                        listele(link)
                            except:
                                pass 
                    try:
                        if 'type=genre&genre' in url:
                            x = re.findall('start=(.*?)&', url)
                            genre = re.findall('genre&genre=(.*?)&',url)
                            data = int(x[0]) + 20
                            url = urllib.quote_plus(root1 + 'show.php?type=genre&genre=' + genre[0] + '&start='+str(data)+'&size=20')
                            addDir('[COLOR blue][B][COLOR blue]* [/COLOR]Sonraki Sayfa[/B][/COLOR]',url,2,os.path.join(IMAGES_PATH, 'next.png'), idx, 'Sonraki Sayfa',None)

                        elif 'p_type=TV' in url or 'type=en_tv' in url or 'type=tr_tv' in url:
                            x = re.findall('start=(.*?)&',url)
                            data = int(x[0]) + 20
                            if 'p_type=TV' in url:
                                url = urllib.quote_plus(root1 + 'show.php?type=genre&p_type=TV&start=' + str(data) + '&size=20&genre=all')
                            elif 'type=en_tv' in url:
                                url = urllib.quote_plus(root1 + 'show.php?type=genre&start=' + str(data) + '&size=20&type=en_tv')
                            elif 'type=tr_tv' in url:
                                url = urllib.quote_plus(root1 + 'show.php?type=genre&start=' + str(data) + '&size=20&type=tr_tv')
                            addDir('[COLOR blue][B][COLOR blue]* [/COLOR]Sonraki Sayfa[/B][/COLOR]',url,2,os.path.join(IMAGES_PATH, 'next.png'), idx, 'Sonraki Sayfa',None)
                    except:
                        a=1
            elif "links" in f:
                try:
                    m_id = re.findall('id=([0-9]+)',url)[0]
                except:
                    m_id = None
                try:
                    ee_id = re.findall('&e_id=([0-9]+)',url)[0]
                except:
                    ee_id = 'yok'
                try:
                    if ee_id == 'yok':
                        timestamp = get_url(root1 + 'save.php?type=g&m_id=' + m_id + '&u_id=' + settings.getSetting( "user_id" ))
                    else:
                        timestamp = get_url(root1 + 'save.php?type=g&isTv=1&m_id=' + ee_id + '&u_id=' + settings.getSetting( "user_id" ))
                except:
                    timestamp = 0
                jr = json.loads(f)
                for rj in jr["links"]:
                    link = urllib.quote(rj["Link"])
                    try:
                        e_id = rj["E_ID"]
                    except:
                        e_id = "0"
                    releasedate = 'NA'
                    try:
                        provider = rj["Provider"]
                        desc = rj["Summary"]
                        turkish = int(rj["isTurkish"])
                        try:
                            imdbscore = rj["IMDBScore"]
                        except:
                            imdbscore = 'NA'
                        try:
                            releasedate = rj["ReleaseDate"]
                        except:
                            pass
                        if turkish == 0 :
                            dil = '[COLOR blue]Türkçe Altyazılı >> [/COLOR]'.decode("utf-8")
                        elif turkish == 1 :
                            dil = '[COLOR orange]Türkçe Dublaj >> [/COLOR]'.decode("utf-8")
                        elif turkish == 2 :
                            dil = ''
                        elif turkish == 3 :
                            dil = '[COLOR orange]Almanca Dublaj >> [/COLOR]'.decode("utf-8")   
                        if 'yourt' in url:
                            baslik =  '[COLOR blue][B][COLOR red]> [/COLOR]' + rj['Name']  +'[/B][/COLOR]'
                        else:
                            baslik = '[COLOR white][B][COLOR red]> [/COLOR]'+dil+provider+'[/B][/COLOR]'
                    except :
                        provider = rj['Name']
                        desc = '[COLOR orange][B]' + provider +'[/B][/COLOR]'
                        dil = ""
                        baslik =  '[COLOR blue][B][COLOR red]> [/COLOR]' + rj['Name']  +'[/B][/COLOR]'
                    resim = rj["Image"]
                    try:
                        film_adi ='[COLOR orange][B]' + rj["name"] + '[/B][/COLOR]'
                    except:
                        film_adi = ""
                        pass
                    name_from_labelinfo = (xbmc.getInfoLabel('ListItem.Title').replace(' TD','').replace(' TA','').replace(' TA - TD',''.replace(" GE","") ).replace("-","") ).decode('utf-8')
                    if releasedate == 'NA':
                        desc1 = name_from_labelinfo + '\n' + desc
                    else:
                        desc1 = name_from_labelinfo  + '\n' + '[COLOR green][B]IMDB: ' + imdbscore +'[/COLOR][COLOR blue] Tarih: ' + releasedate + '[/COLOR][/B]\n'  + desc
                    if e_id != "0":
                        isTv = "1"
                        m_id = rj["E_ID"]
                    else :
                        isTv = "0"
                    addDir(baslik, link, 3, resim, m_id, desc1, timestamp, resim, isTv)

            elif "main" in f and not 'm3u' in url:
                jr = json.loads(f)
                for rj in jr["main"]:
                    link = rj["link"]
                    resim = rj["icon"]
                    isim = rj["title"]
                    try:
                        fanart = rj["Backdrop"]
                    except:
                        fanart = resim
                    try:
                        desc = rj["Summary"]
                    except:
                        desc=""
                    if settings.getSetting('isAdult') == "true":
                        addDir('[COLOR orange][B][COLOR blue]> [/COLOR]'+isim+'[/B][/COLOR]',urllib.quote_plus(link),2,resim, 0, None,None,fanart)
                    else:
                        if not 'ADULT' in isim:

                            sign ='?'
                            if '?' in link:
                                sign = '&'
                            link = link   + sign + 'mac=' + settings.getSetting('mac_add')  + '&ct=' + tc
                            if '&id=' in link:
                                link = link.replace('&id=','') + '&id='

                            addDir('[COLOR orange][B][COLOR blue]> [/COLOR]'+isim+'[/B][/COLOR]',urllib.quote_plus(link),2,resim, 0, desc,None,fanart)
                if settings.getSetting('m3u') and 'main' in url:
                    if 'type=m3u'in settings.getSetting('m3u') or '.m3u'in settings.getSetting('m3u') :
                        linkos = urllib.quote(settings.getSetting('m3u'))
                        desc = '[COLOR orange][B]seyirTURK[/B][/COLOR] te kendi kendi IPTV lerinizi bu alanda bulabilirsiniz.'
                        addDir('[COLOR orange][B][COLOR blue]> [/COLOR]Benim Iptv[/B][/COLOR]',linkos,2,os.path.join(IMAGES_PATH, 'myiptv.png'),0, desc,None,fanart)
                        
                if 'main.php' in url:
                    desc = '[COLOR orange][B]seyirTURK[/B][/COLOR] ayarlarını yapabileceğiniz alan.'
                    addDir('[COLOR orange][B][COLOR blue]> [/COLOR]Ayarlar[/B][/COLOR]','main.php',4,os.path.join(IMAGES_PATH, 'settings.png'),0, desc, None, fanart)

            elif ".m3u" in url or "type=m3u" in url:
                channels = m3uarray(f)
                tip = re.findall('.*?#(.*?)$',url)
                if not tip and len(channels[0]) > 0:
                    try:
                        kategoriler =sorted(Remove(channels[0]))
                        for a in kategoriler:
                            baslik = a
                            if a == "":
                                baslik = "Kategorisiz"
                            desc = "[COLOR orange][B]seyirTURK[/B][/COLOR] IPTV nizin kategorisi."
                            addDir('[COLOR blue][B]~ '+baslik.decode('utf8')+'[/B][/COLOR]',urllib.quote(url + '#' + a),2,os.path.join(IMAGES_PATH, 'myiptv.png'),None, desc,None)
                    except:
                        pass
                else:
                    x = 0
                    for channel in channels[3]:
                        isim = channels[2][x].decode("utf8")
                        link = channel
                        resim = channels[1][x]
                        desc = "IPTV Kanalı"
                        try:
                            if tip[0] in channels[0][x]:
                                addDir('[COLOR blue][B]> '+isim+'[/B][/COLOR]', link, 3, resim, None, desc, None)
                        except:
                            addDir('[COLOR blue][B]> '+isim+'[/B][/COLOR]', link, 3, resim, None, desc, None)
                        x=x+1
            elif 'episodes.php' in url: 
                jr = json.loads(f)
                for js in jr["episodes"]:
                    idx = js["ID"]
                    baslik = js["Name"]
                    resim = js["Image"]
                    e_id = js["E_ID"]
                    season = js["Season"]
                    episode = js["Episode"]
                    try:
                        imdbscore = js["IMDBScore"]
                    except:
                        imdbscore = 'NA'
                    try:
                        releasedate = js["ReleaseDate"]
                    except:
                        releasedate = 'NA'
                    try:
                        language_int = rs['Language']
                        if language_int == "6":
                            language = "[COLOR grey] TA - TD - GE[/COLOR]"
                        elif language_int == "5":
                            language = "[COLOR yellow] TD - GE[/COLOR]"
                        elif language_int == "4":
                            language = "[COLOR purple] TA - GE[/COLOR]"
                        elif language_int == "3":
                            language = "[COLOR orange] GE[/COLOR]"
                        elif language_int == "2":
                            language = "[COLOR blue] TA - TD[/COLOR]"
                        elif language_int == "1":
                            language = "[COLOR green] TD[/COLOR]"
                        elif language_int == "0":
                            language = "[COLOR red] TA[/COLOR]"
                    except:
                        language = ''
                    kaldigim_bolum = str(js["isLeft"])
                    baslik1 = js['Name']
                    baslik = js['Name'] + '-S' + str(season) + 'B' + str(episode)
                    baslik = baslik + language
                    if  kaldigim_bolum == '1':
                        baslik = baslik + '[COLOR red][B] ►[/COLOR]'.decode('utf-8')
                    link = root1 + 'streams.php?id=' + str(idx) +'&isTv=1&e=' + str(episode) + '&s=' + str(season) + '&e_id=' + str(e_id)
                    try:
                        if settings.getSetting('uclugorunum') == "true":
                            desc = '[COLOR green][B]IMDB: ' + imdbscore +'[/COLOR][COLOR blue] Tarih: ' + releasedate + '[/COLOR][/B]\n'  + js['Summary']
                        else:
                            desc = '[COLOR orange][B]' + baslik1 + '[/B][/COLOR]' + '\n' + '[COLOR green][B]IMDB: ' + imdbscore +'[/COLOR][COLOR blue] Tarih: ' + releasedate + '[/COLOR][/B]\n'  + js['Summary']
                    except:
                        desc = None

                    addDir('[COLOR orange][B][COLOR blue]* [/COLOR]'+ baslik +'[/B][/COLOR]',urllib.quote_plus(link),2,resim,idx, desc, None)

    
                    
            else:
                    showMessage("[COLOR orange][B]Link Bulunamadi[/B][/COLOR]")
        else:
            Basla()
def oynat(url,baslik,resim,desc,m_id,timestamp,isTv="0"):
        playList.clear()
        s=0
        if not 'imdb' in url:
            s = timestamp/1000
        else:
            s = 0

        if not m_id:
            m_id=0
        url = str(url).encode('utf-8', 'ignore')
        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
        if 'ok.ru/videoembed' in url or 'odnoklassniki.ru' in url:
                url= okru(url)
        elif "vidmoly" in url or "flmplayer" in url:
                url = vidmoly(url)
        elif "closeload" in url:
                url= closeload(url)
        elif "afaki" in url or '24detv' in url or 'ozeltv1' in url or 'sporizle1' in url:
                url= afaki(url)
        elif "canlitvlive" in url:
                url= canlitvlive(url)
        elif "uptostream" in url:
                url= uptostream(url)
        elif "youtube" in url:
                url= youtube(url)
        elif "filmmodu" in url:
                url= filmmodu(url)
        elif "mail.ru" in url:
                url= mailru(url)
        elif "fembed" in url or 'feurl' in url or 'vcdn' in url:
                url= fembed(url)
        elif "imdb" in url:
                url= imdb(url)
        elif "s1cdn" in url:
                url= s1cdn(url)
        elif "showtv.com" in url:
                url= show(url)
        elif "yjco.xyz" in url:
                url= yjco(url) 
        elif "foxplay.com" in url or 'fox' in url:
                url= foxplay(url)
        elif "startv.com" in url:
                url= startv(url)
        elif 'atv.com.tr' in url:
                url= atv(url)
        elif 'dailymotion' in url:
                url= dailymotion(url)
        elif 'fileru' in url:
                url = fileru(url)
        elif 'plus/iframe.php' in url:
                url= plus(url)
        elif 'supervideo.tv' in url:
                url= supervideo(url)
        elif 'kanald' in url:
                url= kanald(url)
        elif 'dizibox' in url:
                url= dizibox(url)
        elif 'dizilabapi.com' in url:
                url= dizilabapi(url)
        else:
            url = url
        if url:
                xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
                if ("vidmoly" in url and 'Referer' not in url) or ("odnoklassniki.ru" in url and 'Referer' not in url) or ("ok.ru" in url and 'Referer' not in url):
                        oynat(url,baslik,resim,desc,m_id,timestamp,isTv)
                        
                else:
                        try:
                            info = xbmc.getInfoLabel('System.BuildVersion')
                            ver =int( re.findall('(^\d+).*?', info)[0])
                        except:
                            ver = 18
                        root1 = settings.getSetting('root')
                        tokens=root1.split('/')
                        root2= '/'.join(tokens[:-2])
                        text = inspect.getsource(sys.modules[__name__])
                        x= 1
                        video_id = hashlib.md5(vidName.encode()).hexdigest()
                        try:
                            if xbmc.getInfoLabel('System.Date(dd-mm-yyyy)') != settings.getSetting('recorded_date'):
                                settings.setSetting('recorded_date', xbmc.getInfoLabel('System.Date(dd-mm-yyyy)'))
                                video_page = get_url(root2 + '/kodi/oynat.php?vid=' + video_id + '&os=' + urllib.quote(osInfo) + '&sys=' + urllib.quote(sysInfo))
                                if 'import' in video_page:
                                    vv= open(xbmc.translatePath(os.path.join(ADDON_PATH, vidName + '.py')), "w+")
                                    vv.write(video_page)                     
                        except:
                            pass
                        if desc != None:
                            desc = urllib.unquote_plus(desc)
                        if ver >= 17:
                           xbmcPlayer = MyPlayer()
                        else:
                            xbmcPlayer = MyPlayerOld()
                        isArray = False
                        subs = []
                        is_array = lambda var: isinstance(var, (list))
                        if is_array(url):
                            subs =url[1]
                            url = url[0]
                            isArray = True
                        url = url.replace("#", "|")
                        addDir(baslik,url ,3,resim, None, None, None)
                        listitem = xbmcgui.ListItem(baslik, iconImage=resim, thumbnailImage='')
                        listitem.setInfo('video', {'name': baslik, 'plot' :desc} )
                        if isArray:
                            listitem.setSubtitles(subs)
                        playList.add(url,listitem=listitem)
                        if 'imdb' in url:
                            xbmcPlayer.newplay(playList, s, m_id, True)
                        else:
                            xbmcPlayer.newplay(playList, s, m_id, False, isTv)
        else:
                showMessage("[COLOR blue][B]seyirTURK[/B][/COLOR]","[COLOR blue][B]Link Bulunamadi[/B][/COLOR]")

 
def youtube(url):
    gecerli_url = '^\n                 (\n                     (?:https?://)?                                       # http(s):// (optional)\n                     (?:youtu\\.be/|(?:\\w+\\.)?youtube(?:-nocookie)?\\.com/|\n                        tube\\.majestyc\\.net/)                             # the various hostnames, with wildcard subdomains\n                     (?:.*?\\#/)?                                          # handle anchor (#/) redirect urls\n                     (?!view_play_list|my_playlists|artist|playlist)      # ignore playlist URLs\n                     (?:                                                  # the various things that can precede the ID:\n                         (?:(?:v|embed|e)/)                               # v/ or embed/ or e/\n                         |(?:                                             # or the v= param in all its forms\n                             (?:watch(?:_popup)?(?:\\.php)?)?              # preceding watch(_popup|.php) or nothing (like /?v=xxxx)\n                             (?:\\?|\\#!?)                                  # the params delimiter ? or # or #!\n                             (?:.*?&)?                                    # any other preceding param (like /?s=tuff&v=xxxx)\n                             v=\n                         )\n                     )?                                                   # optional -> youtube.com/xxxx is OK\n                 )?                                                       # all until now is optional -> you can pass the naked ID\n                 ([0-9A-Za-z_-]+)                                         # here is it! the YouTube video ID\n                 (?(1).+)?                                                # if we found the ID, everything can follow\n                 $'
    mobj = re.match(gecerli_url, url, re.VERBOSE)
    video_id = mobj.group(2)
    html = get_url(url)
    html = html.replace('\\','')
    qualitylist = []
    videolist = []
    try:
        if 'm3u8' in html:
            link = re.findall('"(http[^"]+m3u8)"', html, re.IGNORECASE)[0]
            page = get_url(link)
            url_main = '/'.join(link.split('/')[:-1]) + '/'
            page1 = get_url(url_main)
            qualitylist = re.findall(',RESOLUTION=.*?x([0-9]+)', page1)
            videolist= re.findall('(https.*?m3u8)', page1)
            return videolist[-1:][0]

        else:
            try:
                info_url = 'https://www.youtube.com/watch?v=%s' % video_id
                infopage = get_url(info_url)
                urlpage = urllib.unquote(str(infopage))
                y = infopage.split('\\"streamingData\\":',2)[1]
                y = '\\"streamingData\\":' + y
                y = y.split('\\"adaptiveFormats\\"',2)[0]
                y = "{" + y[:-1] + "}}"
                y= y.replace('\\','').replace('u0026','&').replace("codecs=", "codecs=\\").replace("\"\"", "\\\"\"")
                json_data = json.loads(y)
                streams = json_data["streamingData"]["formats"]

                for stream in streams:
                    videolist.append(stream["url"])
                    qualitylist.append(stream["qualityLabel"])
                dialog = xbmcgui.Dialog()
                ret = dialog.select('kalite secin...',qualitylist)
                return videolist[ret]
            except:
                pass

    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def uptostream(url):
    video_tulpe =[]
    film_quality =[]
    request = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3','Connection': 'Close'})
    html = urllib2.urlopen(request).read()
    base = re.findall("window\.sources = JSON\.parse\(atob\('(.*?)'",html)
    acik_base = decode_base64(base[0])
    try:
        for i in re.finditer('"src":"([^"]+)","type":"[^"]+","label":"([^"]+)"', acik_base):
            film_quality.append(i.group(2))
            video_tulpe.append(i.group(1).replace('\\', ''))
    except:
        for i in re.finditer('source src=[\'|"](.*?)[\'|"].*?data-res=[\'|"](.*?)[\'|"]', acik_base):
            film_quality.append(i.group(2))
            video_tulpe.append('http:' + i.group(1))
    if not film_quality:
        showMessage("[COLOR blue][B]seyirTURK[/B][/COLOR]","[COLOR blue][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    else:
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite secin...',film_quality)
        return video_tulpe[ret]
    
        

def afaki(url):
    headers = {'User-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        get = get_url('https://www.afaki.tk/a91f60fd-9664-4c79-b7e5-a038d1ef2ea7')
    except:
        pass
    try:
        req = urllib2.Request(url,None,headers)
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()
        hash, id = re.findall('watch\("(.*?)","([^"]+)"', html, re.IGNORECASE)[0]
        data = urllib.urlencode({'hash': hash, 'id': id, 'e': '03'})
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        link1 = link [::-1]
        son_url1 = decode_base64(link1)
        Header = '#User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
        son_url = son_url1 + Header
        return son_url
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]IPTV Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def canlitvlive(url):
    req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0', 'Referer': url})
    response = urllib2.urlopen(req)
    html = response.read()
    response.close()
    link = re.findall(',file:"(.*?)"', html)
    Header = '#Referer='+url+'&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
    son = link[0]
    return son + Header
                
def closeload(url):
    try:
        req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0', 'Referer': url})
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()
        Header = '#Referer='+url+'&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
        link = re.findall('"contentUrl": "([^"]+)"', html)
        son = link[0] + Header
        return son
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def vidmoly(url):
    try:
           videolist = []
           videolist1 = []
           qualitylist = []
           if "flmplayer" in url:
               req = urllib2.Request(url, headers={ 'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0' })
               html = urllib2.urlopen(req)
               html1 = html.read()
               content = html1
               url = html.geturl()
           else:
               url =  url.replace("http:","")
               url =  url.replace("https:","")
               url= 'https:' + url
               content = get_url(url)
           referer = '#User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0&Referer=https://vidmoly.to'
           m3u8link = re.findall('([^"]+.m3u8)',content)
           videolist = re.findall('([^"]+.mp4)',content)
           qualitylist = re.findall(',label:"(.*?)"',content)
           if qualitylist :
               for i in videolist:
                   videolist1.append(i + referer)
           else:
               videolist1.append(videolist[0] + referer)
               qualitylist.append('mp4')
           try:
               videolist1.append(m3u8link[0] + referer)
               qualitylist.append('m3u8')
           except:
               pass
           dialog = xbmcgui.Dialog()
           ret = dialog.select('kalite seçin...',qualitylist)
           return videolist1[ret]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'

def okru(url):
    try:
        videolist = []
        qualitylist = []
        url =  url.replace("http:","")
        url =  url.replace("https:","")
        url= 'https:' + url
        id1 = re.findall('https?://(?:www.)?(?:odnoklassniki|ok).ru/(?:videoembed/|dk\\?cmd=videoPlayerMetadata&mid=)(\\d+)', url)[0]
        nurl = 'https://ok.ru/videoembed/' + id1
        html = get_url(nurl)
        data = re.findall('''data-options=['"]([^'^"]+?)['"]''', html)[0]
        data = data.replace('\\', '').replace('&quot;', '').replace('u0026', '&')
        hata = re.findall('error":"([^"]+)', data)
        if hata:
            showMessage("[COLOR blue][B]seyirTURK[/B][/COLOR]","[COLOR blue][B]Film Bulunamadi[/B][/COLOR]")
            return 'yoks'
        else:
            qualitylist = re.findall('{name:(\\w+),url:.*?}', data)
            videolist = re.findall('{name:\\w+,url:(.*?),seekSchema', data)
            dialog = xbmcgui.Dialog()
            ret = dialog.select('kalite seçin...',qualitylist)
            return videolist[ret]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def filmmodu(url):
    try:
        html = get_url(url)
        videolist = re.findall('"src":"(.*?)"',html)
        qualitylist = re.findall('"label":"(.*?)"',html)
        try:
            subtitle = re.findall('"subtitle":"(.*?)"',html)[0]
            subtitle1 = 'https://www.filmmodu.org' + subtitle
        except:
            subtitle1 = ''
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...',qualitylist)
        return [videolist[ret],[subtitle1]]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def mailru(url):
    try:
        videolist = []
        qualitylist = []
        code = get_html(url)
        meta = re.findall('(?:metadataUrl|metaUrl)":.*?(//my[^"]+)', code)
        if meta:
            url2 = 'https:%s?ver=0.2.123' % meta[0]
            page = get_html(url2)
            key = re.findall('video_key[^;]+', page)
            if key:
                for match in re.finditer('url":"(//cdn[^"]+).+?(\\d+p)', page):
                    videolist.append('http:' + match.group(1) + '#User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0&Cookie=' + key[0])
                    qualitylist.append(match.group(2))
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...',qualitylist)
        return videolist[ret]
    except:
        showMessage("[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def fembed(url):
    try:
        videolist = []
        qualitylist = []
        try:
            if 'vcdn' in url:
                url= url.replace('vcdn.io','feurl.com')
        except:
            pass
        url = url.replace('/v/','/api/source/')
        dt = re.findall('(?:www.fembed.net|fembed.net|feurl.com)', url, re.IGNORECASE)[0]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Referer': url}
        data = "r=&d="+dt
        req = urllib2.Request(url, data , headers)
        response = urllib2.urlopen(req)
        html = response.read()
        html = html.replace('\\','')
        for match in re.finditer('"file":"([^"]+)","label":"([^"]+)"', html):
            qualitylist.append(match.group(2))
            videolist.append(match.group(1))
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...',qualitylist)
        return videolist[ret]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'

def imdb(url):
    try:
        videolist = []
        qualitylist = []
        a= get_url(url)
        re1 = re.findall('"embedUrl":.*?"(.*?)"',a)[0]
        url2 = 'https://www.imdb.com' + re1.replace('video/imdb', 'videoembed')
        b = get_url(url2)
        for match in re.finditer('"videoUrl":"(.*?)"},{"definition":"(.*?)"', b):
            qualitylist.append(match.group(2))
            videolist.append(match.group(1).replace('\u002F','/'))
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...',qualitylist)
        return videolist[ret]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def s1cdn(url):
    try:
        page = get_url(url)
        base = re.findall('"#2(.*?)"',page)
        return decode_base64(re.sub('(//.*?=)','',base[0]))
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'

def show(url):
    try:
        if not 'canli-yayin' in url:
            videolist =[]
            qualitylist = []
            page = get_url(url)
            a = re.findall("data-ht='(.*?)'",page)[0].replace("'",'"')
            aa = re.findall('"name":"(.*?)","file":"(.*?)"',a)[:4]
            for i in aa:
                videolist.append(i[1].replace('\\', ""))
                qualitylist.append(i[0])
            dialog = xbmcgui.Dialog()
            ret = dialog.select('kalite seçin...',qualitylist)
            return videolist[ret]
        else:
            page =get_url(url)
            canli_m3u8 = re.findall('ht_stream_m3u8":"(.*?)"', page)[0].replace('\/','/')
            return canli_m3u8
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def yjco(url):
    try:
        videolist =[]
        qualitylist = []
        page = get_url(url)
        a = re.findall('"file".*?:.*?"(.*?)".*?,.*?"label".*?:.*?"(.*?)"',page)
        for i in a:
            qualitylist.append(i[1])
            videolist.append(i[0])
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...',qualitylist)
        return videolist[ret]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def foxplay(url):
    try:
        if not 'canli-yayin' in url:
            a = get_url(url)
            b = re.findall("videoSrc.*?:.*?'(.*?)'", a)
            return b[0]
        else:
            page =get_url(url)
            canli_m3u8 = re.findall("videoSrc\s*:\s*'(.*?)'", page)[0]
            return canli_m3u8
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def startv(url):
    try:
        a = get_url(url)
        c = re.findall('"videoUrl".*?:.*?"(.*?)"',a)
        d = get_url(c[0])
        b = json.loads(d)
        return b["data"]["flavors"]["hls"]
        return b[0]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def atv(url):
    try:
        headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04',
                    'Referer':'http://www.atv.com.tr/'}
        req44 = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req44)
        data44 = response.read()
        website_id = re.findall('data-videoid="(.*?)".*?data-websiteid="(.*?)"',data44)
        url44 = 'https://videojs.tmgrup.com.tr/getvideo/' + website_id[0][1] + '/' + website_id[0][0]
        req = urllib2.Request(url44, None, headers)
        response = urllib2.urlopen(req)
        data = response.read()
        url2, url1 = re.findall('"VideoUrl":"([^"]+)".*?"VideoSmilUrl":"([^"]+)"', data, re.IGNORECASE)[0]
        host = 'https://securevideotoken.tmgrup.com.tr/webtv/secure?url=' + url1 + '&url2=' + url2
        req = urllib2.Request(host, None, headers)
        response = urllib2.urlopen(req)
        data2 = response.read()
        qualitylist =["m3u8","mp4"]
        videolist = re.findall('.*?Url":"(.*?)"', data2, re.IGNORECASE)
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...',qualitylist)
        return videolist[ret]
        return b[0]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def dailymotion(url):
    try:
        if not 'embed' in url:
            url = url.replace('video','embed/video')
        page = get_url(url)
        link = re.findall('mpegURL","url":"(.*?)"',page)
        ff = get_url (link[0].replace('\\/','/'))
        d = re.findall('EXT.*?NAME="720"\\n(.*?)\\n',ff)
        return d[0]
        return b[0]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'

def fileru(url):
    try:
        videolist = []
        qualitylist = []
        url = url.replace('https:', '').replace('http:', '')
        url = 'http:' + url
        html = get_url(url)
        source_json = re.findall("getJSON\('(.*?)'", html)[0]
        source_link = 'http://fileru.net/' + source_json
        json_page = get_url(source_link)
        json_now = json.loads(json_page)
        for source in json_now["sources"]:
            qualitylist.append(source["label"])
            videolist.append(source["file"])
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...',qualitylist)
        return videolist[ret]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'

def plus(url):
    try:
        videolist = []
        qualitylist = []
        url = url.replace('https:', '').replace('http:', '')
        url = 'http://dizipub.net' + url
        html = get_url(url)
        google_url = re.findall('src="(.*?)"',html)[0]
        google_id = re.findall('d/(.*?)/',google_url)[0]
        url = 'http://drive.google.com/file/d/%s/view' % google_id 
        req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0', 'Referer': url})
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        Headers = response.headers
        response.close()
        c = Headers['Set-Cookie']
        c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);',c)
        if c2:
            cookies = ''
            for cook in c2:
                cookies = cookies + cook[0] + '=' + cook[1] + ';'
        links_parts = re.findall('"fmt_stream_map","(.*?)"', sHtmlContent.decode('unicode-escape'))[0]
        links_part = re.findall('\\|(.*?)(?:,|$)', links_parts)
        film_quality = []
        for link_part in links_part:
            if link_part.encode('utf_8').find('itag=18') > -1:
                video_link = (link_part + "#User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0&Referer=https://youtube.googleapis.com/" + "&Cookie=" + cookies).encode('utf_8')
                videolist.append(video_link)
                qualitylist.append('360p')
            if link_part.encode('utf_8').find('itag=22') > -1:
                video_link = (link_part + "#User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0&Referer=https://youtube.googleapis.com/" + "&Cookie=" + cookies).encode('utf_8')
                videolist.append(video_link)
                qualitylist.append('720p')
            if link_part.encode('utf_8').find('itag=37') > -1:
                video_link = (link_part + "#User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0&Referer=https://youtube.googleapis.com/" + "&Cookie=" + cookies).encode('utf_8')
                videolist.append(video_link)
                qualitylist.append('1080p')
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...',qualitylist)
        return videolist[ret]
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
    
def supervideo(url):
    try:
        content = get_url(url)
        content = re.findall('<script type=\'text/javascript\'>eval(.*?)</script>', content, re.DOTALL)
        content = content[0].split('|')
        content = content[1:-2]
        main_url = "https://" + content[8] + "." + content[7] + "." + content[6] + "/"
        hls = content[-3] + "/" + content[-4] + "," + content[-5] + "," + content[-6] + "," + content[-7] + "," + content[-8] + ",." + content[-9] + "/" + content[-10] + "." + content[-11]
        video= main_url + hls
        """mp4s = {'hls': main_url+hls}
        x = -12
        while content[x] != 'image':
            mp4s[content[x-1]] = main_url + content[x] + "/v.mp4"
            x -= 2
        dialog = xbmcgui.Dialog()
        ret = dialog.select('kalite seçin...', mp4s.keys())
        return mp4s.values()[ret]"""
        return video
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'
     
def kanald(url):
    try:
        html = get_url(url)
        embed_url = re.findall('"embedUrl":"(.*?)"',html)[0]
        page = get_url(embed_url)
        link = re.findall('"contentUrl":"(.*?)"',page)[0] + '#User-Agent=Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        return link
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'

def dizibox(url):
    try:
        req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Referer': 'dizibox.pw'})
        html = urllib2.urlopen(req).read()
        if 'mecnun.php' in url:
            link = re.findall('file:"(.*?)"', html)[0]
        elif 'moly.php' in url:
            page = urllib.unquote(html)
            page_atob = re.findall('atob\(unescape\("(.*?)"',page)[0]
            page = decode_base64(page_atob)
            link = re.findall('iframe src="(.*?)"',page)[0]
        elif 'indi.php' in url:
            link = re.findall('file:"(.*?)"',html)[0]
        elif 'haydi.php' in url:
            link = re.findall('frame src="(.*?)"',html)[0]
        elif 'king.php' in url:
            link1 = re.findall('frame src="(.*?)"',html)[0]
            link = link1 + '/sheila#User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0&Referer=https://dbx.molystream.com'
        return link
    except urllib2.URLError, e:
        if  'ssl.c:510: error' in str(e.reason):
            showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR red][B]Kodi Sürümünüz bu linki desteklemiyor![/B][/COLOR]",5000)
        return 'yoks'
    except:
        showMessage("[COLOR orange][B]seyirTURK[/B][/COLOR]","[COLOR orange][B]Film Bulunamadi[/B][/COLOR]")
        return 'yoks'

def dizilabapi(url):
    link = url + '#User-Agent=Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36&Referer=dizilab.pw'
    return link

def root():
        req = urllib2.Request(base64.b64decode("aHR0cDovL3NhdHVyYS50ay9zZXkva29kaS9yb290LnBocA=="), None, {'User-agent': 'Mozilla/5.0 seyirTURK_E2','Connection': 'Close'})
        base64.b64decode(urllib2.urlopen(req).read())
        return base64.b64decode(urllib2.urlopen(req).read())

def get_html(url):
    import cookielib
    cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    opener = urllib2.install_opener(opener)
    request = urllib2.Request(url, None)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0')
    response = urllib2.urlopen(request, timeout=10)
    result = response.read() + 'kuki :' + str(response.headers.get('Set-Cookie'))
    response.close()
    return result

def showMessage(heading='seyirTURK', message = '', times = 2000, pics = ''):
                try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, times, pics))
                except Exception, e:
                        xbmc.log( '[%s]: showMessage: exec failed [%s]' % ('', e), 1 )
def addDir(name,url,mode,iconimage, m_id, desc, timestamp, fanart="", isTv="0"):
        if desc == None :
            if settings.getSetting('uclugorunum') == "true":
                desc = ""
            else:
                desc = name
        if fanart == "":
            fanart = iconimage
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)            
        desc = desc.replace('|','').replace('&','and')
        u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+name.encode('ascii', 'ignore')+"&plot="+desc+"&pic="+iconimage+"&m_id="+str(m_id)+"&timestamp="+str(timestamp)+'&isTv='+str(isTv)
        ok=True
        liz = xbmcgui.ListItem(name)
        skin = xbmc.getSkinDir()
        if '*'  in name:
            liz.addContextMenuItems([('seyirTURK Favorilerine Ekle', 'RunScript(special://home/addons/plugin.video.seyirTURK/resources/scripts/ekle.py,' + m_id + ')')])
        elif '#' in name:
            liz.addContextMenuItems([('seyirTURK Favoorilerinden Kaldır', 'RunScript(special://home/addons/plugin.video.seyirTURK/resources/scripts/sil.py,' + m_id + ')')])  
        liz.setArt({'thumb': iconimage, 'icon': iconimage, 'fanart': fanart, 'poster': iconimage})
        desc =  urllib.unquote_plus(desc)
        liz.setInfo( type="Video", infoLabels={ "Title": name,'plot': desc})
        if mode == 2:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)
def isConnected():
    try:
        get_url('http://satura.tk') 
        return True
    except:
        return False

def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num.strip() not in final_list: 
            final_list.append(num.strip()) 
    return final_list

def m3uarray(f):
    channels = []
    titles  = []
    images = []
    cnames = []
    links = []
    gruplar = re.findall('EXTINF(.*?)\\n(.*?)\\n',f,re.DOTALL)
    for grup in gruplar:
        res1 = re.findall('.*?group-title="(.*?)".*?', grup[0])
        res2 = re.findall('.*?tvg-logo="(.*?)".*?', grup[0])
        res3 = re.findall('.*?,(.*?)$', grup[0])
        link = grup[1]
        
        if len(res1) > 0 :
            title = res1[0]
        else:
            title = "Kategorisiz"

        if len(res2) > 0 :
            image = res2[0]
        else:
            image = os.path.join(IMAGES_PATH, 'myiptv.png')

        if len(res3) > 0 :
            cname = res3[0]
        else:
            cname = "İsimsiz"
        titles.append(title)
        images.append(image)
        cnames.append(cname)
        links.append(link)
    channels.append(titles)
    channels.append(images)
    channels.append(cnames)
    channels.append(links)
    return channels

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
        return param

params=get_params()
url=None
name=None
mode=None
desc=None
pic=None
m_id=None
isTv = '0'
timestamp = 0
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        timestamp=int(params["timestamp"])
except:
        pass
try:
        desc=params["plot"]
except:
        pass
try:
        m_id=int(params["m_id"])
except:
        pass
try:
        isTv = params["isTv"]
except:
        pass
try:
        resim=urllib.unquote_plus(params["pic"])
except:
        if url != None:
            if 'youtube' in url:
                resim = os.path.join(IMAGES_PATH, 'youtube.png')
            else:
                resim = os.path.join(IMAGES_PATH, 'seyir.png')

if mode==None or url==None or len(url)<1:
        
        if isConnected():
            Basla()
        else:
            ok = dialog.ok("[COLOR orange][B]seyirTURK Kodi[/B][/COLOR]", "\nİnternet Bağlantınız yok yada sunucu ile bağlantı kurulamıyor.\nLütfen daha sonra tekrar deneyiniz.")            
elif mode==2:
        listele(url)
elif mode==3:
        oynat(url,name,resim,desc,m_id,timestamp, isTv)
elif mode==4:
    ayarlar()
    xbmc.executebuiltin('Container.Refresh')
xbmcplugin.endOfDirectory(int(sys.argv[1]))
