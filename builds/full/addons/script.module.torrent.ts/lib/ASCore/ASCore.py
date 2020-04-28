#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys
import re
import gc
import random
import urllib2
import json
import base64
import socket
import BaseHTTPServer
import SocketServer
import threading
from datetime import datetime
import collections
import xbmcgui
import xbmc
import xbmcaddon
import xbmcplugin


def fs_enc(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode('utf-8').encode(sys_enc)


def fs_dec(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode(sys_enc).encode('utf-8')


class StreamReader(threading.Thread):
    chunk_size = 128 * 1024
    max_queue = 200

    class _DataStat(object):
        def __init__(self):
            self._count = 0
            self._data = 0
            self._max = 0

        def add(self, d):
            self._data += int(d)
            self._count += 1
            self._max = int(d) if int(d) > self._max else self._max

        @property
        def max(self):
            return self._max

        @property
        def total(self):
            return self._data

        @property
        def count(self):
            return self._count

        @property
        def avg(self):
            return self._data / self._count if self._count > 0 else 0

    def __init__(self, uri):
        threading.Thread.__init__(self)
        self._headers = {'User-Agent': 'VLC 2.0.5', 'Accept': '*/*', 'Connection': 'keep-alive'}
        self._resp_headers = dict()
        res = re.findall(r'^http://(.+):(\d+)/(.+)', uri)
        self._ip = res[0][0]
        self._port = int(res[0][1])
        self._request = res[0][2]
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ds_bytes = self._DataStat()
        self._ds_queue = self._DataStat()
        self.active = True
        self.opened = False
        try:
            memoryview(bytearray())
            self._data = bytearray(self.chunk_size)
            self._data_len = 0
        except:
            self._data = None
            self._read = self._read_alt
            self._get_data = self._get_data_alt
            TSengine.log.out('HTTPD: using alternative reading cycle')
        self.data_q = collections.deque()

    def __del__(self):
        self.close()

    def set_range_header(self, r):
        self._headers['Range'] = r

    def _get_headers(self):
        try:
            h = bytearray()
            while True:
                res = self._s.recv(self.chunk_size)
                h += res
                if b'\r\n\r\n' in h:
                    break
                else:
                    xbmc.sleep(1)
            h = h.split(b'\r\n\r\n', 1)
            for i in str(h[0]).split('\r\n'):
                sh = i.split(': ')
                if len(sh) == 2:
                    self._resp_headers[sh[0]] = sh[1]
            if len(h) > 1:
                if len(h[1]):
                    self.data_q.append(h[1])
        except Exception, e:
            TSengine.log.out('HTTPD: headers recv error %s' % e)

    def start_stream(self):
        try:
            self._s.connect((self._ip, self._port))
            h = ''
            for i in self._headers:
                h += '%s: %s\r\n' % (i, self._headers[i])
            self._s.send('GET /%s HTTP/1.0\r\n%s\r\n' % (self._request, h))
            self._get_headers()
            self._s.settimeout(15)
            self.opened = True
            TSengine.log.out('HTTPD: stream started')
        except Exception, e:
            TSengine.log.out('HTTPD: start stream error %s' % e)

    def close(self):
        try:
            self.active = False
            if self.isAlive():
                self.join()
            if self.opened:
                self.opened = False
                self._s.close()
                TSengine.log.out('HTTPD: stream closed')
                TSengine.log.out('HTTPD:     total bytes readed from stream: %d' % self._ds_bytes.total)
                TSengine.log.out('HTTPD:     max bpp: %d' % self._ds_bytes.max)
                TSengine.log.out('HTTPD:     average bpp: %d' % self._ds_bytes.avg)
                TSengine.log.out('HTTPD:     max queue load: %d' % self._ds_queue.max)
                TSengine.log.out('HTTPD:     average queue load: %d' % self._ds_queue.avg)
        except Exception, e:
            TSengine.log.out('HTTPD: closing error %s' % e)

    def run(self):
        TSengine.log.out('HTTPD: reading thread started')
        try:
            while self.active:
                if not self.opened:
                    continue
                if len(self.data_q) < self.max_queue:
                    if self._read():
                        self.data_q.append(self._get_data())
                    elif len(self.data_q) > 0:
                        xbmc.sleep(1)
                        continue
                    else:
                        self.active = False
                else:
                    xbmc.sleep(1)
                self._ds_queue.add(len(self.data_q))
            self.active = False
        except Exception, e:
            TSengine.log.out('HTTPD: reading thread error %s' % e)
        TSengine.log.out('HTTPD: reading thread closed')

    def _get_data(self):
        return self._data[:self._data_len]

    def _get_data_alt(self):
        return self._data

    def _read(self):
        view = memoryview(self._data)
        while self.opened:
            try:
                l = self._s.recv_into(view, len(view))
            except socket.timeout:
                TSengine.log.out('HTTPD: read timeout reached')
            except Exception, e:
                TSengine.log.out('HTTPD: read error: %s' % e)
                self.active = False
                return False
            else:
                if l == 0:
                    return False
                else:
                    self._data_len = l
                    self._ds_bytes.add(l)
                    return True

    def _read_alt(self):
        while self.opened:
            try:
                self._data = self._s.recv(self.chunk_size)
            except socket.timeout:
                TSengine.log.out('HTTPD: read timeout reached')
            except Exception, e:
                TSengine.log.out('HTTPD: read error: %s' % e)
                self.active = False
                return False
            else:
                if len(self._data) == 0:
                    return False
                else:
                    self._ds_bytes.add(len(self._data))
                    return True

    def get_content_range_header(self):
        if self.opened:
            return self._resp_headers.get('Content-Range')

    def get_content_length_header(self):
        if self.opened:
            return self._resp_headers.get('Content-Length')


class StreamManager(object):
    def __init__(self):
        self._stream_list = list()

    def open(self, uri):
        for s in self._stream_list:
            s[1].close()
        self._stream_list = list()
        sr = StreamReader(uri)
        self._stream_list.append([uri, sr])
        return sr

    def __del__(self):
        for s in self._stream_list:
            s[1].close()


class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    def handle_error(self, *args, **kwargs):
        pass


class HttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    mime_types = {'webm': 'video/webm', 'mkv': 'video/x-matroska ', 'flv': 'video/x-flv', 'mp4': 'video/mp4',
                  'm4v': 'video/x-m4v', 'mpeg': 'video/mpg', 'mpg': 'video/mpg', 'mts': 'video/mpg', 'm2v': 'video/mpg',
                  'm2ts': 'video/m2ts', 'ogm': 'video/ogg', 'ogv': 'video/ogg', 'vob': 'video/dvd', 'avi': 'video/avi',
                  'mov': 'video/quicktime', 'qt': 'video/quicktime', 'wmv': 'video/x-ms-wmv', '3gp': 'video/3gpp',
                  'rm': 'application/vnd.rn-realmedia', 'asf': 'video/x-ms-asf', 'divx': 'video/x-divx',
                  'bdmv': 'video/x-bdmv', 'ts': 'video/mp2t'}

    def log_request(self, *args, **kwargs):
        pass

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        try:
            if self.server.file_name == urllib2.unquote(self.path[1:]):
                TSengine.log.out('HTTPD: new get request: %s' % self.path)
                st = self.server.stream_manager.open(self.server.ace_stream_uri)
                if 'range' in self.headers:
                    self.send_response(206, 'Partial Content')
                    st.set_range_header(self.headers['range'])
                else:
                    self.send_response(200)
                st.start_stream()
                st.start()
                if st.opened:
                    _, ext = os.path.splitext(self.server.file_name)
                    ext = ext[1:]
                    if ext == '' or ext not in HttpHandler.mime_types:
                        self.send_header('Content-type', 'application/octet-stream')
                    else:
                        self.send_header('Content-type', HttpHandler.mime_types[ext])
                    self.send_header('Accept-Ranges', 'bytes')
                    self.send_header('Content-Range', st.get_content_range_header())
                    self.send_header('Content-Length', st.get_content_length_header())
                    self.end_headers()
                    while st.active:
                        try:
                            if len(st.data_q) > 0:
                                self.wfile.write(st.data_q.popleft())
                            else:
                                xbmc.sleep(1)
                        except socket.timeout:
                            TSengine.log.out('HTTPD: write timeout reached')
                        except Exception, e:
                            TSengine.log.out('HTTPD: write error: %s' % e)
                            break
                    st.close()
            else:
                self.send_response(404, 'not found')
                self.end_headers()
        except Exception, e:
            TSengine.log.out('HTTPD: get request error: %s' % e)


class _TSPlayer(xbmc.Player):
    def __init__(self):
        self.tsserv = None
        self.active = True
        self.started = False
        self.ended = False
        self.paused = False
        self.buffering = False
        xbmc.Player.__init__(self)
        width, height = _TSPlayer.get_skin_resolution()
        w = width
        h = int(0.14 * height)
        x = 0
        y = (height - h) / 2
        self._ov_window = xbmcgui.Window(12005)
        self._ov_label = xbmcgui.ControlLabel(x, y, w, h, '', alignment=6)
        self._ov_background = xbmcgui.ControlImage(x, y, w, h, fs_dec(_TSPlayer.get_ov_image()))
        self._ov_background.setColorDiffuse('0xD0000000')
        self.ov_visible = False

    def __del__(self):
        self.ov_hide()

    @staticmethod
    def get_ov_image():
        ov_image = fs_enc(os.path.join(xbmc.translatePath('special://temp'), 'bg.png'))
        if not os.path.isfile(ov_image):
            fl = open(ov_image, 'wb')
            fl.write(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAA'
                                      'AC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='))
            fl.close()
        return ov_image

    @staticmethod
    def get_skin_resolution():
        import xml.etree.ElementTree as Et
        skin_path = fs_enc(xbmc.translatePath('special://skin/'))
        tree = Et.parse(os.path.join(skin_path, 'addon.xml'))
        res = tree.findall('./extension/res')[0]
        return int(res.attrib['width']), int(res.attrib['height'])

    def ov_show(self):
        if not self.ov_visible:
            self._ov_window.addControls([self._ov_background, self._ov_label])
            self.ov_visible = True

    def ov_hide(self):
        if self.ov_visible:
            self._ov_window.removeControls([self._ov_background, self._ov_label])
            self.ov_visible = False

    def ov_update(self):
        if self.ov_visible:
            if int(self.tsserv.status[0]) == 100 and self.tsserv.status[1] == TSengine.ls(30030):
                self._ov_label.setLabel('%s\n[B]%s[/B]' % (TSengine.ls(30035),
                                                           TSengine.ls(30036)))
            else:
                self._ov_label.setLabel('%s\n%s [B]%d%%[/B]\n%s' % (self.tsserv.status[1],
                                                                    TSengine.ls(30037),
                                                                    int(self.tsserv.status[0]),
                                                                    self.tsserv.status[2]))

    def onPlayBackPaused(self):
        self.ov_show()
        if not self.buffering:
            self.paused = True
        self.tsserv.push('EVENT pause position=%d' % int(self.getTime()))

    def onPlayBackStarted(self):
        TSengine.log.out('TSPLAYER: playback started')
        xbmc.executebuiltin('XBMC.ActivateWindow(12005)')
        try:
            if self.tsserv.vod:
                self.tsserv.push('DUR %s %d' % (self.tsserv.content_url, int(xbmc.Player().getTotalTime() * 1000)))
        except:
            self.started = False
            return
        self.tsserv.push('EVENT play')
        self.tsserv.push('PLAYBACK %s 0' % self.tsserv.content_url)
        self.started = True
        xbmc.sleep(1000)

    def onPlayBackResumed(self):
        self.ov_hide()
        self.paused = False
        self.tsserv.push('EVENT play')

    def onPlayBackEnded(self):
        self.active = False
        self.ended = True

    def onPlayBackStopped(self):
        self.ov_hide()
        self.tsserv.push('STOP')
        self.tsserv.push('EVENT stop')
        self.active = False

    def onPlayBackSeek(self, time, _):
        self.tsserv.push('EVENT seek position=%d' % int(time / 1000))


class TSengine(object):
    class _Logger(object):
        def __init__(self):
            self.enable = True if xbmcaddon.Addon(id='script.module.torrent.ts').getSetting('debug') == 'true' else False
            self.file_name = os.path.join(fs_enc(xbmc.translatePath('special://home')), 'ASCore.log')
            if os.path.isfile(self.file_name):
                if os.path.getsize(self.file_name) > 512 * 1024:
                    os.remove(self.file_name)

        def out(self, txt):
            if self.enable:
                log = open(self.file_name, 'a')
                log.write('%s: %s\r\n' % (str(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]), str(txt)))
                log.close()

        def out_cut(self, txt, l=150):
            if len(txt) > l:
                self.out('%s...%s' % (txt[:int(l / 2)], txt[-int(l / 2):]))
            else:
                self.out(txt)

    addon = xbmcaddon.Addon(id='script.module.torrent.ts')
    sys_enc = sys.getfilesystemencoding()
    win_platform = True if sys.platform == 'win32' or sys.platform == 'win64' else False
    log = _Logger()

    def __init__(self):
        TSengine.log.out('TSENGINE: init...')
        self._server_ip = TSengine.addon.getSetting('address')
        self._server_port = int(TSengine.addon.getSetting('port'))
        self._saving_path = None
        self._progress = xbmcgui.DialogProgress()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(3)
        self._tsserv = None
        self._media_info = dict()
        self._torrent_mode = None
        self._torrent_url = None
        self._stream_url = None
        self._connected = False
        self._file_saved = False
        self._pos = [25, 50, 75, 100]
        self._progress.create('AceStream', TSengine.ls(30010))
        self._httpd = None
        self._httpd_thread = None
        self._save_files = True if TSengine.addon.getSetting('save') == 'true' and TSengine.addon.getSetting('path') else False
        self._resume_saved = True if TSengine.addon.getSetting('switch_playback') == 'true' else False
        self._buf_pause = True if TSengine.addon.getSetting('auto_pause_buf') == 'true' else False
        self._use_httpd = True if TSengine.addon.getSetting('httpd') == 'true' else False
        self.player = None
        self.files = dict()
        self.local = False
        self.filename = None
        if xbmc.Player().isPlaying():
            xbmc.Player().stop()
        TSengine.addon.setSetting('active', 'true')

    def _ts_init(self):
        self._tsserv = _TSServ(self._sock)
        self._tsserv.start()
        self._tsserv.push('HELLOBG version=6')
        self._progress.update(10, TSengine.ls(30011), ' ')
        while not self._tsserv.version:
            if xbmc.abortRequested or self._progress.iscanceled():
                return False
            xbmc.sleep(200)
        if self._tsserv.err:
            return False
        if not self._tsserv.key:
            return True
        import hashlib
        sha1 = hashlib.sha1()
        pkey = self._tsserv.pkey
        sha1.update(self._tsserv.key + pkey)
        key = sha1.hexdigest()
        pk = pkey.split('-')[0]
        ready_key = 'READY key=%s-%s' % (pk, key)
        self._tsserv.push(ready_key)
        self._progress.update(30, TSengine.ls(30012), ' ')
        while not self._tsserv.auth_ok:
            if xbmc.abortRequested or self._progress.iscanceled():
                return False
            xbmc.sleep(200)
        return True

    @staticmethod
    def sm(msg, timeout=3000):
        xbmc.executebuiltin('XBMC.Notification("AceStream", "%s", %d, "")' % (msg, timeout))

    @staticmethod
    def ls(s_id):
        return TSengine.addon.getLocalizedString(s_id).encode('utf-8')

    def _connect(self):
        self._progress.update(0, TSengine.ls(30013), ' ')
        try:
            socket.inet_aton(self._server_ip)
        except:
            self._server_ip = '127.0.0.1'
        if self._server_port not in range(1024, 65535):
            self._server_port = 62062
        if TSengine.win_platform:
            if not self._start_windows():
                return False
        else:
            try:
                self._sock.connect((self._server_ip, self._server_port))
                self._sock.settimeout(None)
                return True
            except:
                if not self._start_linux():
                    return False
        for i in range(1, 100, 1):
            self._progress.update(i, TSengine.ls(30013), ' ')
            try:
                if self.win_platform and self._server_ip == '127.0.0.1':
                    self._server_port = self._get_aceport_windows()
                if self._server_port:
                    self._sock.connect((self._server_ip, self._server_port))
                    self._sock.settimeout(None)
                    self._connected = True
                    return True
            except:
                pass
            if self._progress.iscanceled():
                return False
            xbmc.sleep(500)
        return False

    def _start_linux(self):
        import subprocess
        try:
            subprocess.Popen(['acestreamengine', '--client-console'])
        except:
            try:
                subprocess.Popen('acestreamengine-client-console')
            except: 
                try:
                    xbmc.executebuiltin('XBMC.StartAndroidActivity("org.acestream.engine")')
                except:
                    TSengine.sm(TSengine.ls(30014))
                    self._progress.update(0, TSengine.ls(30014), ' ')
                    return False
        return True
    
    def _start_windows(self):
        try:
            import _winreg
            try:
                t = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\AceStream')
            except:
                t = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\TorrentStream')
            path = _winreg.QueryValueEx(t, r'EnginePath')[0]
            self._progress.update(0, TSengine.ls(30015), ' ')
            os.startfile(path)
            return True
        except:
            TSengine.sm(TSengine.ls(30014))
            self._progress.update(0, TSengine.ls(30014), ' ')
            return False

    def _get_aceport_windows(self):
        try:
            import _winreg
            try:
                t = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\AceStream')
            except:
                t = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\TorrentStream')
            port_file = os.path.join(os.path.dirname(_winreg.QueryValueEx(t, 'EnginePath')[0]), r'acestream.port')
            gf = open(port_file, 'r')
            return int(gf.read())
        except:
            return None

    def _get_local_file(self, index):
        if not self._save_files:
            return False
        for k, v in self.files.iteritems():
            if v == index:
                self.filename = k.replace('/', '_').replace('\\', '_')
        if not self._saving_path:
            self._saving_path = fs_enc(TSengine.addon.getSetting('path'))
        self.filename = os.path.join(self._saving_path, fs_enc(self.filename))
        if os.path.exists(self.filename):
            return fs_dec(self.filename)
        return False

    def _start_stream(self, index):
        self._tsserv.index = index
        self._tsserv.push('START %s %s %s 0 0 0' % (self._torrent_mode, self._torrent_url, str(index)))
        while not self._tsserv.state == 2:
            self._progress.update(int(self._tsserv.status[0]), self._tsserv.status[1], self._tsserv.status[2])
            if xbmc.abortRequested or self._progress.iscanceled() or self._tsserv.err:
                return False
            xbmc.sleep(200)
        self._tsserv.content_url.replace('127.0.0.1', self._server_ip)
        return True

    def _save_file(self):
        if self._tsserv.can_save and self._save_files:
            if not os.path.exists(self.filename):
                self._progress.update(0, TSengine.ls(30016), ' ')
                save_name = urllib2.quote(fs_dec(self.filename))
                self._tsserv.push('SAVE %s path=%s' % (self._tsserv.save_info[0] + ' ' + self._tsserv.save_info[1], save_name))
                self._tsserv.can_save = False
                while not os.path.exists(self.filename):
                    if xbmc.abortRequested or self._progress.iscanceled():
                        return False
                    xbmc.sleep(200)
                return fs_dec(self.filename)
        return False

    def _start_httpd(self, uri, file_name):
        port = TSengine.get_random_open_port()
        self._httpd = ThreadingHTTPServer(('127.0.0.1', port), HttpHandler)
        self._httpd.stream_manager = StreamManager()
        self._httpd.ace_stream_uri = uri
        self._httpd.file_name = file_name
        self._httpd_thread = threading.Thread(target=self._httpd.serve_forever)
        self._httpd_thread.start()
        TSengine.log.out('HTTPD: started at http://127.0.0.1:%d/' % port)
        return 'http://127.0.0.1:%d/%s' % (port, urllib2.quote(file_name))

    @staticmethod
    def get_random_open_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return int(port)

    def play_url_ind(self, index=0, title='', icon='', thumb='', use_resolved_url=False):
        self._progress.update(50, TSengine.ls(30017), ' ')
        if isinstance(title, unicode):
            title = title.encode('utf-8')
        self._media_info = {'title': title, 'icon': icon, 'thumb': thumb}
        if len(self.files) == 1 and int(index) != 0:
            index = 0
        local_file = self._get_local_file(index)
        if not local_file:
            self._progress.update(70, TSengine.ls(30018), '')
            if not self._start_stream(index):
                return False
            xbmc.sleep(700)
            TSengine.log.out('TSENGINE: starting playback')
            self._progress.update(100, TSengine.ls(30019), ' ')
            local_file = self._save_file()
            if not local_file:
                if self._use_httpd:
                    self._stream_url = self._start_httpd(self._tsserv.content_url, title)
                else:
                    self._stream_url = self._tsserv.content_url
                self.player = _TSPlayer()
                self.player.tsserv = self._tsserv
                self._progress.close()
                item = xbmcgui.ListItem(title, thumb, icon, path=self._stream_url)
                if use_resolved_url:
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
                else:
                    self.player.play(self._stream_url, item)
                while self.player.active:
                    xbmc.sleep(200)
                    self.loop()
                    if xbmc.abortRequested:
                        break
                TSengine.log.out('TSENGINE: playback ended')
                return self.player.started
        if local_file:
            TSengine.log.out('TSENGINE: local playback started')
            self._progress.update(100, TSengine.ls(30019), ' ')
            xbmc.sleep(700)
            item = xbmcgui.ListItem(title, thumb, icon, path=local_file)
            self._progress.close()
            if use_resolved_url:
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
            else:
                xbmc.Player().play(local_file, item)
            TSengine.log.out('TSENGINE: local playback ended')
            return True

    def get_link(self, index=0, title='', icon='', thumb=''):
        TSengine.log.out('TSENGINE: using deprecated function get_link')
        if isinstance(title, unicode):
            title = title.encode('utf-8')
        self._progress.close()
        self.player = _TSPlayer()
        self.player.tsserv = self._tsserv
        local_file = self._get_local_file(index)
        if local_file:
            self.local = True
            return local_file
        if not self._start_stream(index):
            return False
        xbmc.sleep(500)
        local_file = self._save_file()
        if local_file:
            self.local = True
            return local_file
        else:
            if self._use_httpd:
                self._stream_url = self._start_httpd(self._tsserv.content_url, title)
            else:
                self._stream_url = self._tsserv.content_url
            return self._stream_url

    @property
    def version(self):
        return self.addon.getAddonInfo('version')

    def loop(self):
        if self.player.isPlaying():
            if self.player.getTotalTime() > 0:
                cpos = int((1 - (self.player.getTotalTime() - self.player.getTime()) / self.player.getTotalTime()) * 100) + 1
            else:
                cpos = 0
            if cpos in self._pos:
                self._pos.remove(cpos)
                self._tsserv.push('PLAYBACK %s %d' % (self._tsserv.content_url, cpos))
        if self._tsserv.can_save and self._save_files:
            save_name = urllib2.quote(fs_dec(self.filename))
            self._tsserv.push('SAVE %s path=%s' % (self._tsserv.save_info[0] + ' ' + self._tsserv.save_info[1], save_name))
            self._tsserv.can_save = False
            self._file_saved = True
            TSengine.log.out('TSENGINE: saving file')
        if self._resume_saved and self._file_saved and self.player.started:
            if self.player.isPlaying() and os.path.exists(self.filename) and not self.player.paused:
                TSengine.log.out('TSENGINE: switching to local file')
                xbmc.sleep(2000)
                local_file = fs_dec(self.filename)
                time1 = self.player.getTime()
                item = xbmcgui.ListItem(self._media_info['title'], self._media_info['thumb'],
                                        self._media_info['icon'], path=local_file)
                item.setProperty('StartOffset', str(time1))
                self._tsserv.push('STOP')
                self.player.ov_hide()
                xbmc.Player().play(local_file, item)
                self.player.active = False
                self.local = True
        if self._buf_pause:
            if self._tsserv.state == 3 and self._tsserv.pause:
                self.player.buffering = True
                if not self.player.ov_visible:
                    self.player.pause()
            if self._tsserv.state == 2 and self.player.buffering:
                if not self.player.paused:
                    self.player.pause()
                self.player.buffering = False
        if self.player.ov_visible and self.player.started:
            self.player.ov_update()

    def load_torrent(self, torrent, mode, host=None, port=None):
        self._torrent_mode = mode
        self._torrent_url = torrent
        if host:
            self._server_ip = host
        if port:
            self._server_port = port
        if not self._connect():
            TSengine.sm(TSengine.ls(30020))
            TSengine.log.out('TSENGINE: connection failed')
            return False
        TSengine.log.out('TSENGINE: connected')
        if not self._ts_init():
            TSengine.sm(TSengine.ls(30021))
            return False
        self._progress.update(10, TSengine.ls(30022), ' ')
        self._tsserv.push('LOADASYNC %s %s %s 0 0 0' % (str(random.randint(0, 0x7fffffff)), mode, torrent))
        while not self._tsserv.files:
            if xbmc.abortRequested or self._progress.iscanceled() or self._tsserv.err:
                return False
            xbmc.sleep(200)
        self._progress.update(50, TSengine.ls(30023), '')
        if not self._tsserv.files:
            return False
        file_list = json.loads(self._tsserv.files)
        try:
            for l in file_list['files']:
                self.files[urllib2.unquote(l[0].encode('utf-8'))] = l[1]
            self._progress.update(100, TSengine.ls(30024), '')
        except:
            TSengine.sm(TSengine.ls(30025))
            return False
        TSengine.log.out('TSENGINE: files loaded')
        return 'Ok'

    def set_saving_settings(self, save=False, saving_path=None, resume_saved=False):
        self._save_files = save
        self._resume_saved = resume_saved
        if save and saving_path:
            self._saving_path = fs_enc(saving_path)

    def end(self):
        if self._httpd:
            self._httpd.shutdown()
            self._httpd.server_close()
        if self._httpd_thread:
            self._httpd_thread.join()
        if self._progress:
            self._progress.close()
        if self._connected:
            self._connected = False
            self._tsserv.push('SHUTDOWN')
        if self._tsserv:
            self._tsserv.active = False
            self._tsserv.join()
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self._sock.close()
        TSengine.addon.setSetting('active', 'false')

    def __del__(self):
        self.end()
        TSengine.log.out('TSENGINE: garbage collected: %s' % repr(gc.get_count()))
        gc.collect()


class _TSServ(threading.Thread):
    def __init__(self, socket):
        self.pkey = 'n51LvQoTlJzNGaFxseRK-uvnvX-sD4Vm5Axwmc4UcoD-jruxmKsuJaH0eVgE'
        threading.Thread.__init__(self)
        self._sock = socket
        self._buffer = 65 * 1024
        self._last_received = ''
        self.active = True
        self.err = False
        self.auth_ok = False
        self.version = None
        self.files = None
        self.key = None
        self.index = None
        self.content_url = None
        self.can_save = False
        self.save_info = None
        self.state = 0
        self.status = [0, '', '']
        self.pause = False
        self.vod = True

    def push(self, command):
        TSengine.log.out_cut('TSSERV: [%s]' % command)
        try:
            self._sock.send(command + '\r\n')
        except:
            self.err = True

    def run(self):
        while self.active and not self.err:
            try:
                self.temp = self._sock.recv(self._buffer)
            except:
                self.temp = ''
            self._last_received += self.temp
            ind = self._last_received.find('\r\n')
            if ind != -1:
                fcom = self._last_received
                while ind != -1:
                    self._last_received = fcom[:ind]
                    self.exec_com()
                    fcom = fcom[(ind + 2):]
                    ind = fcom.find('\r\n')
                self._last_received = ''

    def exec_com(self):
        line = self._last_received
        cmd = self._last_received.split(' ')[0]
        params = self._last_received.split(' ')[1::]
        if cmd != 'STATUS':
            TSengine.log.out('TSSERV: {%s}' % self._last_received)
        if cmd == 'HELLOTS':
            try:
                self.version = params[0].split('=')[1]
            except:
                self.version = '1.0.6'
            try:
                if params[2].split('=')[0] == 'key':
                    self.key = params[2].split('=')[1]
            except: 
                try:
                    self.key = params[1].split('=')[1]
                except:
                    TSengine.log.out('TSSERV: no HELLO key received')
        elif cmd == 'AUTH':
            self.auth_ok = True
        elif cmd == 'LOADRESP':
            self.files = line[line.find('{'):len(line)]
        elif cmd == 'EVENT':
            if params[0] == 'cansave':
                if int(self.index) == int(params[1].split('=')[1]):
                    self.can_save = True
                    self.save_info = [params[1], params[2]]
            elif params[0] == 'getuserdata':
                self.push('USERDATA [{"gender": 1}, {"age": 3}]')
                self.err = True
        elif cmd == 'START':
            try:
                self.content_url = urllib2.unquote(params[0].split('=')[1])
            except:
                self.content_url = params[0]
        elif cmd == 'RESUME':
            self.pause = False
        elif cmd == 'PAUSE':
            self.pause = True
        elif cmd == 'SHUTDOWN':
            self.active = False
        elif cmd == 'STATE':
            self.state = int(params[0])
            if self.state == 6:
                self.err = True
        elif cmd == 'STATUS':
            self._get_status(params[0])

    def _get_status(self, params):
        ss = re.compile(r'main:[a-z]+', re.S)
        s1 = re.findall(ss, params)[0]
        st = s1.split(':')[1]
        if st == 'idle':
            self.status[1] = TSengine.ls(30026)
        elif st == 'starting':
            self.status[1] = TSengine.ls(30027)
        elif st == 'check':
            self.status[1] = TSengine.ls(30028)
            self.status[0] = int(params.split(';')[1])
        elif st == 'prebuf':
            self.status[0] = int(params.split(';')[1])
            self.status[1] = TSengine.ls(30029)
            self.status[2] = TSengine.ls(30034) % (params.split(';')[8], params.split(';')[5])
        elif st == 'loading':
            self.status[1] = TSengine.ls(30017)
        elif st == 'dl':
            self.status[0] = int(params.split(';')[1])
            self.status[1] = TSengine.ls(30030)
            self.status[2] = TSengine.ls(30034) % (params.split(';')[6], params.split(';')[3])
        elif st == 'buf':
            self.status[0] = int(params.split(';')[1])
            self.status[1] = TSengine.ls(30031)
            self.status[2] = TSengine.ls(30034) % (params.split(';')[8], params.split(';')[5])
        elif st == 'wait':
            self.status[0] = 99
            self.status[1] = TSengine.ls(30032)
            self.status[2] = TSengine.ls(30033)

    def end(self):
        self.active = False


