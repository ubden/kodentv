# -*- coding: utf-8 -*-

'''
    Simple XBMC Download Script
    Copyright (C) 2013 Sean Poyser (seanpoyser@gmail.com)

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
'''


import re
import json
import sys        
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import os
import inspect


try: from urllib import quote_plus
except ImportError: from urllib.parse import quote_plus
try: from urllib import unquote
except ImportError: from urllib.parse import unquote
try: from urllib import unquote_plus
except ImportError: from urllib.parse import unquote_plus
try: from urlparse import parse_qsl, urlparse
except ImportError: from urllib.parse import parse_qsl, urlparse
try: from urllib2 import Request, urlopen
except ImportError: from urllib.request import Request, urlopen


def download(url):
    from modules.nav_utils import hide_busy_dialog, notification
    from modules.utils import clean_file_name, clean_title
    from modules import settings
    # from modules.utils import logger
    
    if url == None:
        hide_busy_dialog()
        notification('No URL found for Download. Pick another Source', 6000)
        return
    
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    json_meta = params.get('meta')
    if json_meta:
        meta = json.loads(json_meta)
        db_type = meta.get('vid_type')
        title = meta.get('search_title')
        year = meta.get('year')
        image = meta.get('poster')
        season = meta.get('season')
        episode = meta.get('episode')
        name = params.get('name')
    else:
        db_type = params.get('db_type')
        image = params.get('image')
        title = params.get('name')
    title = clean_file_name(title)
    
    dest = settings.download_directory(db_type)
    if not dest:
        hide_busy_dialog()
        resp = xbmcgui.Dialog().yesno(
            "No Download folder set!",
            "Fen requires you to set Download Folders.",
            "Would you like to set a folder now?")
        if resp:
            from modules.nav_utils import open_settings
            return open_settings('7.0')
        else:
            return
    
    levels =['../../../..', '../../..', '../..', '..']
    for level in levels:
        try: control.makeFile(os.path.abspath(os.path.join(dest, level)))
        except: pass
    
    xbmcvfs.mkdir(dest)
    
    if db_type in ('movie', 'episode'):
        folder_rootname = '%s (%s)' % (title, year)
        dest = os.path.join(dest, folder_rootname)
        xbmcvfs.mkdir(dest)
    if db_type == 'episode':
        dest = os.path.join(dest, 'Season %02d' %  int(season))
        xbmcvfs.mkdir(dest)

    try: headers = dict(parse_qsl(url.rsplit('|', 1)[1]))
    except: headers = dict('')
    
    try: url = url.split('|')[0]
    except: pass

    if not 'http' in url:
        from apis.furk_api import FurkAPI
        from indexers.furk import filter_furk_tlist, seas_ep_query_list
        t_files = FurkAPI().t_files(url)
        t_files = [i for i in t_files if 'video' in i['ct'] and 'bitrate' in i]
        name, url = filter_furk_tlist(t_files, (None if db_type == 'movie' else seas_ep_query_list(season, episode)))[0:2]
        transname = name.translate(None, '\/:*?"<>|').strip('.')
    else:
        name_url = unquote(url)
        file_name = clean_title(name_url.split('/')[-1])
        if clean_title(title).lower() in file_name.lower():
            transname = os.path.splitext(urlparse(name_url).path)[0].split('/')[-1]
        else:
            try: transname = name.translate(None, '\/:*?"<>|').strip('.')
            except: transname = os.path.splitext(urlparse(name_url).path)[0].split('/')[-1]

    if db_type == 'archive':
        ext = 'zip'
    elif db_type == 'audio':
        ext = os.path.splitext(urlparse(url).path)[1][1:]
        if not ext in ['wav', 'mp3', 'ogg', 'flac', 'wma', 'aac']: ext = 'mp3'
    else:
        ext = os.path.splitext(urlparse(url).path)[1][1:]
        if not ext in ['mp4', 'mkv', 'flv', 'avi', 'mpg']: ext = 'mp4'

    folder_dest = dest
    dest = os.path.join(dest, transname + '.' + ext)
    
    sysheaders = quote_plus(json.dumps(headers))
    sysurl = quote_plus(url)
    systitle = quote_plus(transname)
    sysimage = quote_plus(image)
    sysfolder_dest = quote_plus(folder_dest)
    sysdest = quote_plus(dest)
    script = inspect.getfile(inspect.currentframe())
    cmd = 'RunScript(%s, %s, %s, %s, %s, %s, %s)' % (script, sysurl, sysfolder_dest, sysdest, systitle, sysimage, sysheaders)

    xbmc.executebuiltin(cmd)

def getResponse(url, headers, size):
    try:
        if size > 0:
            size = int(size)
            headers['Range'] = 'bytes=%d-' % size

        req = Request(url, headers=headers)

        resp = urlopen(req, timeout=30)
        return resp
    except:
        return None

def done(title, downloaded):
    playing = xbmc.Player().isPlaying()

    text = xbmcgui.Window(10000).getProperty('FEN-DOWNLOADED')

    if len(text) > 0:
        text += '[CR]'

    if downloaded:
        text += '[B]%s[/B] : %s' % (title, '[COLOR forestgreen]Download Succeeded[/COLOR]')
    else:
        text += '[B]%s[/B] : %s' % (title, '[COLOR red]Download Failed[/COLOR]')

    xbmcgui.Window(10000).setProperty('FEN-DOWNLOADED', text)

    if (not downloaded) or (not playing): 
        xbmcgui.Dialog().ok('FEN Downloader', text)
        xbmcgui.Window(10000).clearProperty('FEN-DOWNLOADED')

def doDownload(url, folder_dest, dest, title, image, headers):
    def _hide_busy_dialog():
        if kodi_version >= 18: return xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
        else: return xbmc.executebuiltin('Dialog.Close(busydialog)')
    kodi_version = int(xbmc.getInfoLabel("System.BuildVersion")[0:2])
    _addon__ = xbmcaddon.Addon(id='plugin.video.fen')
    headers = json.loads(unquote_plus(headers))
    url = unquote_plus(url)
    title = unquote_plus(title)
    image = unquote_plus(image)
    folder_dest = unquote_plus(folder_dest)
    dest = unquote_plus(dest)
    file = dest.rsplit(os.sep, 1)[-1]
    resp = getResponse(url, headers, 0)

    if not resp:
        _hide_busy_dialog()
        xbmcvfs.rmdir(folder_dest, True)
        xbmcgui.Dialog().ok(title, dest, 'Download failed', 'No response from server')
        return

    try:    content = int(resp.headers['Content-Length'])
    except: content = 0

    try:    resumable = 'bytes' in resp.headers['Accept-Ranges'].lower()
    except: resumable = False

    if resumable:
        print "Download is resumable"

    if content < 1:
        _hide_busy_dialog()
        xbmcgui.Dialog().ok(title, file, 'Unknown filesize', 'Unable to download')
        return

    size = 1024 * 1024
    mb   = content / (1024 * 1024)

    if content < size:
        size = content

    total   = 0
    notify  = 0
    errors  = 0
    count   = 0
    resume  = 0
    sleep   = 0

    _hide_busy_dialog()

    if xbmcgui.Dialog().yesno('Fen' + ' - Confirm Download', '[B]%s[/B]' % title.upper(), 'Complete file is [B]%dMB[/B]' % mb, 'Continue with download?', 'Confirm',  'Cancel') == 1:
        _hide_busy_dialog()
        xbmcvfs.rmdir(folder_dest, True)
        return

    f = xbmcvfs.File(dest, 'w')

    chunk  = None
    chunks = []

    notification_setting = _addon__.getSetting('download.notification')
    show_notifications = True if notification_setting == '1' else False
    persistent_notifications = True if notification_setting == '2' else False
    suppress_during_playback = True if _addon__.getSetting('download.suppress') == 'true' else False
    try: notification_frequency = int(_addon__.getSetting('download.frequency'))
    except: notification_frequency = 10

    if persistent_notifications:
        progressDialog = xbmcgui.DialogProgressBG()
        progressDialog.create('Downloading [B]%s[/B]' % title, '')
        progressDialog.update(0, 'Commencing Download')

    while True:
        playing = xbmc.Player().isPlaying()
        downloaded = total
        for c in chunks:
            downloaded += len(c)
        percent = min(100 * downloaded / content, 100)

        if persistent_notifications:
            progressDialog.update(percent, 'Downloading [B]%s[/B]' % title, '')

        elif show_notifications:
            if percent >= notify:
                if playing and not suppress_during_playback:
                    xbmc.executebuiltin( "XBMC.Notification([B]%s[/B],[I]%s[/I],%i,%s)" % ('Download Progress: ' + str(percent)+'%', title, 10000, image))
                elif (not playing):
                    xbmc.executebuiltin( "XBMC.Notification([B]%s[/B],[I]%s[/I],%i,%s)" % ('Download Progress: ' + str(percent)+'%', title, 10000, image))

                notify += notification_frequency

        chunk = None
        error = False

        try:        
            chunk  = resp.read(size)
            if not chunk:
                if percent < 99:
                    error = True
                else:
                    while len(chunks) > 0:
                        c = chunks.pop(0)
                        f.write(c)
                        del c

                    f.close()
                    try:
                        progressDialog.close()
                    except Exception:
                        pass
                    return done(title, True)

        except Exception, e:
            print str(e)
            error = True
            sleep = 10
            errno = 0

            if hasattr(e, 'errno'):
                errno = e.errno

            if errno == 10035: # 'A non-blocking socket operation could not be completed immediately'
                pass

            if errno == 10054: #'An existing connection was forcibly closed by the remote host'
                errors = 10 #force resume
                sleep  = 30

            if errno == 11001: # 'getaddrinfo failed'
                errors = 10 #force resume
                sleep  = 30

        if chunk:
            errors = 0
            chunks.append(chunk)
            if len(chunks) > 5:
                c = chunks.pop(0)
                f.write(c)
                total += len(c)
                del c

        if error:
            errors += 1
            count  += 1
            xbmc.sleep(sleep*1000)

        if (resumable and errors > 0) or errors >= 10:
            if (not resumable and resume >= 50) or resume >= 500:
                #Give up!
                try:
                    progressDialog.close()
                except Exception:
                    pass
                return done(title, False)

            resume += 1
            errors  = 0
            if resumable:
                chunks  = []
                #create new response
                resp = getResponse(url, headers, total)
            else:
                #use existing response
                pass


if __name__ == '__main__':
    if 'downloader.py' in sys.argv[0]:
        doDownload(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])


