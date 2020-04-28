import xbmcgui, xbmcaddon
import requests
import json
import time
from modules.fen_cache import cache_object
from modules.utils import to_utf8
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)

progressDialog = xbmcgui.DialogProgress()

class RealDebridAPI:
    def __init__(self):
        self.base_url = "https://api.real-debrid.com/rest/1.0/"
        self.auth_url = 'https://api.real-debrid.com/oauth/v2/'
        self.device_url = "device/code?%s"
        self.credentials_url = "device/credentials?%s"
        self.client_ID = __addon__.getSetting('rd.client_id')
        if self.client_ID == '': self.client_ID = 'X245A4XAIBGVM'
        self.enabled = __addon__.getSetting('rd.enabled')
        self.token = __addon__.getSetting('rd.token')
        self.refresh = __addon__.getSetting('rd.refresh')
        self.secret = __addon__.getSetting('rd.secret')
        self.device_code = ''
        self.auth_timeout = 0
        self.auth_step = 0
        self.timeout = 12.0

    def rd_enabled(self):
        if self.enabled in ('', 'false'): return False
        if self.token == '': return False
        else: return True

    def auth_loop(self):
        if progressDialog.iscanceled():
            progressDialog.close()
            return
        time.sleep(self.auth_step)
        url = "client_id=%s&code=%s" % (self.client_ID, self.device_code)
        url = self.auth_url + self.credentials_url % url
        response = json.loads(requests.get(url, timeout=self.timeout).text)
        if 'error' in response:
            return
        try:
            progressDialog.close()
            __addon__.setSetting('rd.client_id', response['client_id'])
            __addon__.setSetting('rd.secret', response['client_secret'])
            self.secret = response['client_secret']
            self.client_ID = response['client_id']
        except:
             xbmcgui.Dialog().ok('Real Debrid Authorization', 'Authorization Failed. Try Again.')
        return

    def auth(self):
        self.secret = ''
        self.client_ID = 'X245A4XAIBGVM'
        url = "client_id=%s&new_credentials=yes" % self.client_ID
        url = self.auth_url + self.device_url % url
        response = json.loads(requests.get(url, timeout=self.timeout).text)
        progressDialog.create('Real Debrid Authorization', '')
        progressDialog.update(-1, 'Real Debrid Authorization','Navigate to: [B]https://real-debrid.com/device[/B]',
                                    'Enter the following code: [B]%s[/B]'% response['user_code'])
        self.auth_timeout = int(response['expires_in'])
        self.auth_step = int(response['interval'])
        self.device_code = response['device_code']

        while self.secret == '':
            self.auth_loop()
        self.get_token()

    def get_token(self):
        if self.secret is '':
            return
        data = {'client_id': self.client_ID,
                'client_secret': self.secret,
                'code': self.device_code,
                'grant_type': 'http://oauth.net/grant_type/device/1.0'}
        url = '%stoken' % self.auth_url
        response = requests.post(url, data=data, timeout=self.timeout).text
        response = json.loads(response)
        self.token = response['access_token']
        self.refresh = response['refresh_token']
        __addon__.setSetting('rd.token', response['access_token'])
        __addon__.setSetting('rd.auth', response['access_token'])
        __addon__.setSetting('rd.refresh', response['refresh_token'])
        username = self.account_info()['username']
        __addon__.setSetting('rd.username', username)
        xbmcgui.Dialog().ok('Real Debrid Authorization', 'Authorization Successful.')

    def refreshToken(self):
        data = {'client_id': self.client_ID,
                'client_secret': self.secret,
                'code': self.refresh,
                'grant_type': 'http://oauth.net/grant_type/device/1.0'}
        url = self.auth_url + 'token'
        response = requests.post(url, data=data, timeout=self.timeout)
        response = json.loads(response.text)
        if 'access_token' in response: self.token = response['access_token']
        if 'refresh_token' in response: self.refresh = response['refresh_token']
        __addon__.setSetting('rd.token', self.token)
        __addon__.setSetting('rd.auth', self.token)
        __addon__.setSetting('rd.refresh', self.refresh)

    def account_info(self, username_only=False):
        url = "user"
        response = self._get(url)
        return response

    def check_cache(self, hashes):
        hash_string = '/'.join(hashes)
        url = 'torrents/instantAvailability/%s' % hash_string
        response = self._get(url)
        return response

    def check_hash(self, hash_string):
        url = 'torrents/instantAvailability/%s' % hash_string
        response = self._get(url)
        return response

    def check_single_magnet(self, hash_string):
        cache_info = self.check_hash(hash_string)
        cached = False
        if hash_string in cache_info:
            info = cache_info[hash_string]
            if isinstance(info, dict) and len(info.get('rd')) > 0:
                cached = True
        return cached

    def user_cloud(self):
        string = "fen_rd_user_cloud"
        url = "torrents"
        return cache_object(self._get, string, url, False, 2)

    def downloads(self):
        string = "fen_rd_downloads"
        url = "downloads"
        return cache_object(self._get, string, url, False, 2)

    def user_cloud_info(self, file_id):
        string = "fen_rd_user_cloud_info_%s" % file_id
        url = "torrents/info/%s" % file_id
        return cache_object(self._get, string, url, False)

    def torrent_info(self, file_id):
        url = "torrents/info/%s" % file_id
        return self._get(url)

    def unrestrict_link(self, link):
        url = 'unrestrict/link'
        post_data = {'link': link}
        response = self._post(url, post_data)
        try: return response['download']
        except: return None

    def add_magnet(self, magnet):
        post_data = {'magnet': magnet}
        url = 'torrents/addMagnet'
        response = self._post(url, post_data)
        return response

    def add_torrent_select(self, torrent_id, file_ids):
        self.clear_cache()
        url = "torrents/selectFiles/%s" % torrent_id
        post_data = {'files': file_ids}
        return self._post(url, post_data)

    def delete_torrent(self, folder_id):
        if self.token == '': return None
        url = "torrents/delete/%s&auth_token=%s" % (folder_id, self.token)
        response = requests.delete(self.base_url + url, timeout=self.timeout)

    def delete_download(self, download_id):
        if self.token == '': return None
        url = "dowwnloads/delete/%s" % (download_id,)
        response = requests.delete(self.base_url + url, timeout=self.timeout).json()
        return response

    def get_hosts(self):
        hosts_dict = {'Real-Debrid': []}
        hosts = []
        string = "fen_rd_valid_hosts"
        url = "hosts/status"
        try:
            result = cache_object(self._get, string, url, False, 8)
            for k, v in result.items():
                # if v['status'] == 'up' and v['supported'] == 1:
                if v['supported'] == 1:
                    hosts.append(k.split('.')[0])
            hosts_dict['Real-Debrid'] = list(set(hosts))
        except: pass
        return hosts_dict

    def resolve_magnet(self, magnet_url, info_hash, store_to_cloud):
        from modules.utils import supported_video_extensions
        try:
            torrent_id = None
            torrent_keys = []
            extensions = supported_video_extensions()
            torrent_files = self.check_hash(info_hash)
            if not info_hash in torrent_files: return None
            torrent_files = torrent_files[info_hash]['rd'][0]
            try: files_tuple = sorted([(k, v['filename'].lower()) for k,v in torrent_files.items() if v['filename'].lower().endswith(tuple(extensions))])
            except: return None
            files_tuple = sorted(files_tuple)
            for i in files_tuple: torrent_keys.append(i[0])
            if not torrent_keys: return None
            torrent_keys = ','.join(torrent_keys)
            torrent = self.add_magnet(magnet_url)
            torrent_id = torrent['id']
            self.add_torrent_select(torrent_id, torrent_keys)
            torrent_files = self.user_cloud_info(torrent_id)
            status = torrent_files.get('status')
            if not status == 'downloaded': return None
            media_id = torrent_files.get('links')[0]
            file_url = torrent_files['links'][0]
            if not store_to_cloud: self.delete_torrent(torrent_id)
            return self.unrestrict_link(file_url)
        except:
            if torrent_id: self.delete_torrent(torrent_id)
            return None

    def add_uncached_torrent(self, magnet_url):
        import xbmc
        from modules.nav_utils import show_busy_dialog, hide_busy_dialog
        from modules.utils import supported_video_extensions
        def _return_failed(message='Unknown Error.'):
            try:
                progressDialog.close()
            except Exception:
                pass
            self.delete_torrent(torrent_id)
            hide_busy_dialog()
            xbmc.sleep(500)
            xbmcgui.Dialog().ok('FEN Cloud Transfer', message)
            return False
        show_busy_dialog()
        extensions = supported_video_extensions()
        torrent = self.add_magnet(magnet_url)
        torrent_id = torrent['id']
        if not torrent_id: return _return_failed('ERROR Transferring Torrent.')
        interval = 5
        stalled = ['magnet_error', 'error', 'virus', 'dead']
        torrent_info = self.torrent_info(torrent_id)
        status = torrent_info['status']
        if status == 'magnet_conversion':
            line1 = 'Converting MAGNET...'
            line2 = torrent_info['filename']
            line3 = '%s seeders' % torrent_info['seeders']
            timeout = 100
            progressDialog.create('FEN Cloud Transfer', line1, line2, line3)
            while status == 'magnet_conversion' and timeout > 0:
                progressDialog.update(timeout, line3=line3)
                if xbmc.abortRequested == True: return sys.exit()
                try:
                    if progressDialog.iscanceled():
                        return _return_failed('Transfer Cancelled.')
                except Exception:
                    pass
                if any(x in status for x in stalled):
                    return _return_failed('ERROR Transferring Torrent.')
                timeout -= interval
                xbmc.sleep(1000 * interval)
                torrent_info = self.torrent_info(torrent_id)
                status = torrent_info['status']
                line3 = '%s seeders' % torrent_info['seeders']
            try:
                progressDialog.close()
            except Exception:
                pass
        if status == 'magnet_conversion':
            return _return_failed('ERROR Converting Magnet.')
        if status == 'waiting_files_selection':
            video_files = []
            all_files = torrent_info['files']
            for item in all_files:
                if any(item['path'].lower().endswith(x) for x in extensions):
                    video_files.append(item)
            try:
                video = max(video_files, key=lambda x: x['bytes'])
                file_id = video['id']
            except ValueError:
                return _return_failed('No Video File Found.')
            self.add_torrent_select(torrent_id, str(file_id))
            torrent_info = self.torrent_info(torrent_id)
            status = torrent_info['status']
            if status == 'downloaded':
                return True
            file_size = round(float(video['bytes']) / (1000 ** 3), 2)
            line1 = 'Saving Torrent to the Real-Debrid Cloud...'
            line2 = torrent_info['filename']
            line3 = status
            progressDialog.create('FEN Cloud Transfer', line1, line2, line3)
            while not status == 'downloaded':
                xbmc.sleep(1000 * interval)
                torrent_info = self.torrent_info(torrent_id)
                status = torrent_info['status']
                if status == 'downloading':
                    line3 = 'Downloading %s GB @ %s mbps from %s peers, %s %% completed' % (file_size, round(float(torrent_info['speed']) / (1000**2), 2), torrent_info['seeders'], torrent_info['progress'])
                else:
                    line3 = status
                progressDialog.update(int(float(torrent_info['progress'])), line3=line3)
                if xbmc.abortRequested == True: return sys.exit()
                try:
                    if progressDialog.iscanceled():
                        return _return_failed('Transfer Cancelled.')
                except Exception:
                    pass
                if any(x in status for x in stalled):
                    return _return_failed('ERROR Transferring Torrent.')
            try:
                progressDialog.close()
            except Exception:
                pass
            hide_busy_dialog()
            return True
        hide_busy_dialog()
        return False

    def _get(self, url):
        original_url = url
        url = self.base_url + url
        if self.token == '': return None
        if '?' not in url:
            url += "?auth_token=%s" % self.token
        else:
            url += "&auth_token=%s" % self.token
        response = requests.get(url, timeout=self.timeout).text
        if 'bad_token' in response or 'Bad Request' in response:
            self.refreshToken()
            response = self._get(original_url)
        try: return to_utf8(json.loads(response))
        except: return to_utf8(response)

    def _post(self, url, post_data):
        original_url = url
        url = self.base_url + url
        if self.token == '': return None
        if '?' not in url:
            url += "?auth_token=%s" % self.token
        else:
            url += "&auth_token=%s" % self.token
        response = requests.post(url, data=post_data, timeout=self.timeout).text
        if 'bad_token' in response or 'Bad Request' in response:
            self.refreshToken()
            response = self._post(original_url, post_data)
        try: return to_utf8(json.loads(response))
        except: return to_utf8(response)

    def revoke_auth(self):
        __addon__.setSetting('rd.auth', '')
        __addon__.setSetting('rd.client_id', '')
        __addon__.setSetting('rd.refresh', '')
        __addon__.setSetting('rd.secret', '')
        __addon__.setSetting('rd.token', '')
        __addon__.setSetting('rd.username', '')
        xbmcgui.Dialog().ok('Real Debrid', 'Revoke Authorization Successful.')

    def clear_cache(self):
        try:
            import xbmc, xbmcvfs
            import os
            RD_DATABASE = os.path.join(xbmc.translatePath(__addon__.getAddonInfo('profile')), 'fen_cache.db')
            if not xbmcvfs.exists(RD_DATABASE): return True
            try: from sqlite3 import dbapi2 as database
            except ImportError: from pysqlite2 import dbapi2 as database
            dbcon = database.connect(RD_DATABASE)
            dbcur = dbcon.cursor()
            dbcur.execute("""DELETE FROM fencache WHERE id LIKE ?""", ("fen_rd_user_cloud%",))
            dbcur.execute("""DELETE FROM fencache WHERE id LIKE ?""", ("fen_rd_downloads%",))
            dbcon.commit()
            dbcon.close()
            return True
        except: return False

