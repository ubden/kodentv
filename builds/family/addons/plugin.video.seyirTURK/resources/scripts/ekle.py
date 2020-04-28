# -*- coding: utf-8 -*-
import sys
import urllib,urllib2
import re,xbmcplugin,xbmcgui,xbmcaddon,xbmc
import json, base64
import hashlib
import os.path
import time
from xml.dom import minidom

settings = xbmcaddon.Addon(id='plugin.video.seyirTURK')
userdata = xbmc.translatePath('special://userdata')

def showMessage(heading='seyirTURK', message = '', times = 2000, pics = ''):
    try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, times, pics))
    except Exception, e:
        xbmc.log( '[%s]: showMessage: exec failed [%s]' % ('', e), 1 )
def Url_Al(url, mac = None):
    sign = '?'
    url = url.strip(' \t\n\r')
    req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0 seyirTURK_KODI Kodi','Betty': 'jughead', 'Connection': 'Close'})
    page = urllib2.urlopen(req).read()
    return page
user_id = settings.getSetting('user_id')
root = settings.getSetting('root')

if user_id != "":
    m_id = sys.argv[1]
    check =  Url_Al(root + 'user.php?type=check&u_id=' + user_id + '&f_id=' + m_id)
    if int(check) == 0:
        add = Url_Al(root + 'user.php?type=fav&do=0&u_id=' + user_id + '&f_id=' + m_id)
        if int(add) == 0:
            showMessage('seyirTURK','[COLOR orange][B]Film eklendi.[/B][/COLOR]', 3000,xbmc.translatePath('special://home/addons/plugin.video.seyirTURK/resources/media/plus.png'))
        else :
            showMessage('seyirTURK','[COLOR orange][B]İşlem başarısız oldu.[/B][/COLOR]', 3000, xbmc.translatePath('special://home/addons/plugin.video.seyirTURK/resources/media/x.png'))
    else :
        showMessage('seyirTURK','[COLOR orange][B]Film zaten var.[/B][/COLOR]', 3000, xbmc.translatePath('special://home/addons/plugin.video.seyirTURK/resources/media/unlem.png'))
else:
    showMessage('seyirTURK','[COLOR orange][B]Giriş yapmamışsınız.[/B][/COLOR]',3000, xbmc.translatePath('special://home/addons/plugin.video.seyirTURK/resources/media/x.png'))

