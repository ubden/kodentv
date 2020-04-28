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

class PremiumizeAPI:
    def __init__(self):
        self.client_id = '663882072'
        self.user_agent = 'Fen for Kodi'
        self.base_url = 'https://www.premiumize.me/api/'
        self.enabled = __addon__.getSetting('pm.enabled')
        self.token = __addon__.getSetting('pm.token')
        self.timeout = 12.0

    def pm_enabled(self):
        if self.enabled in ('', 'false'): return False
        if self.token == '': return False
        else: return True

    def auth_loop(self):
        if progressDialog.iscanceled():
            progressDialog.close()
            return
        time.sleep(5)
        url = "https://www.premiumize.me/token"
        data = {'grant_type': 'device_code', 'client_id': self.client_id, 'code': self.device_code}
        response = self._post(url, data)
        if 'error' in response:
            return
        try:
            progressDialog.close()
            self.token = str(response['access_token'])
            __addon__.setSetting('pm.token', self.token)
        except:
             xbmcgui.Dialog().ok('Premiumize Authorization', 'Authentication failed. Try Again.')
        return

    def auth(self):
        self.token = ''
        data = {'response_type': 'device_code', 'client_id': self.client_id}
        url = "https://www.premiumize.me/token"
        response = self._post(url, data)
        progressDialog.create('Premiumize Authorization', '')
        progressDialog.update(-1, 'Premiumize Authentication','Navigate to: [B]%s[/B]' % response.get('verification_uri'),
                                    'Enter the following code: [B]%s[/B]'% response.get('user_code'))
        self.device_code = response['device_code']
        while self.token == '':
            self.auth_loop()
        if self.token is None: return
        account_info = self.account_info()
        __addon__.setSetting('pm.account_id', str(account_info['customer_id']))
        xbmcgui.Dialog().ok('Premiumize Authorization', 'Authentication Successful.')

    def account_info(self):
        url = "account/info"
        response = self._post(url)
        return response

    def check_cache(self, hashes):
        url = "cache/check"
        data = {'items[]': hashes}
        response = self._post(url, data)
        return response

    def check_single_magnet(self, hash_string):
        cache_info = self.check_cache(hash_string)['response']
        return cache_info[0]

    def unrestrict_link(self, link):
        data = {'src': link}
        url = "transfer/directdl"
        response = self._post(url, data)
        try: return self.add_headers_to_url(response['content'][0]['link'])
        except: return None

    def resolve_magnet(self, magnet, store_to_cloud):
        from modules.utils import supported_video_extensions
        try:
            data = {'src': magnet}
            url = 'transfer/directdl'
            result = self._post(url, data)
            if not 'status' in result or result['status'] != 'success': return None
            end_results = []
            extensions = supported_video_extensions()
            for item in result.get('content'):
                if any(item.get('path').lower().endswith(x) for x in extensions) and not item.get('link', '') == '':
                    end_results.append(item)
            file_url = max(end_results, key=lambda x: x.get('size')).get('link', None)
            if store_to_cloud: self.create_transfer(magnet)
            return self.add_headers_to_url(file_url)
        except: return None

    def add_uncached_torrent(self, magnet_url):
        import xbmc
        from modules.nav_utils import show_busy_dialog, hide_busy_dialog
        from modules.utils import supported_video_extensions
        def _transfer_info(transfer_id):
            info = self.transfer_info()
            if 'status' in info and info['status'] == 'success':
                for item in info['transfers']:
                    if item['id'] == transfer_id:
                        return item
            return {}
        def _return_failed(message='Unknown Error.'):
            try:
                progressDialog.close()
            except Exception:
                pass
            self.delete_transfer(transfer_id)
            hide_busy_dialog()
            xbmc.sleep(500)
            xbmcgui.Dialog().ok('FEN Cloud Transfer', message)
            return False
        show_busy_dialog()
        extensions = supported_video_extensions()
        transfer_id = self.create_transfer(magnet_url)
        if not transfer_id['status'] == 'success':
            return _return_failed('ERROR Transferring Torrent.')
        transfer_id = transfer_id['id']
        transfer_info = _transfer_info(transfer_id)
        if not transfer_info: return _return_failed('ERROR Transferring Torrent.')
        interval = 5
        line1 = 'Saving Torrent to the Premiumize Cloud...'
        line2 = transfer_info['name']
        line3 = transfer_info['message']
        progressDialog.create('FEN Cloud Transfer', line1, line2, line3)
        while not transfer_info['status'] == 'seeding':
            xbmc.sleep(1000 * interval)
            transfer_info = _transfer_info(transfer_id)
            line3 = transfer_info['message']
            progressDialog.update(int(float(transfer_info['progress']) * 100), line3=line3)
            if xbmc.abortRequested == True: return sys.exit()
            try:
                if progressDialog.iscanceled():
                    return _return_failed('Transfer Cancelled.')
            except Exception:
                pass
            if transfer_info.get('status') == 'stalled':
                return _return_failed('ERROR Transferring Torrent.')
        xbmc.sleep(1000 * interval)
        try:
            progressDialog.close()
        except Exception:
            pass
        hide_busy_dialog()
        return True

    def user_cloud(self, folder_id=None):
        if folder_id:
            string = "fen_pm_user_cloud_%s" % folder_id
            url = "folder/list?id=%s" % folder_id
        else:
            string = "fen_pm_user_cloud_root"
            url = "folder/list"
        return cache_object(self._get, string, url, False, 2)

    def user_cloud_all(self):
        string = "fen_pm_user_cloud_all_files"
        url = "item/listall"
        return cache_object(self._get, string, url, False, 2)

    def transfers_list(self):
        string = "fen_pm_transfers_list"
        url = "transfer/list"
        return cache_object(self._get, string, url, False, 2)

    def transfer_info(self):
        url = "transfer/list"
        return self._get(url)

    def rename_cache_item(self, file_type, file_id, new_name):
        if file_type == 'folder': url = "folder/rename"
        else: url = "item/rename"
        data = {'id': file_id , 'name': new_name}
        response = self._post(url, data)
        return response['status']

    def create_transfer(self, magnet):
        data = {'src': magnet, 'folder_id': 0}
        url = "transfer/create"
        return self._post(url, data)

    def delete_transfer(self, transfer_id):
        data = {'id': transfer_id}
        url = "transfer/delete"
        return self._post(url, data)

    def get_item_details(self, item_id):
        string = "fen_pm_item_details_%s" % item_id
        url = "item/details"
        data = {'id': item_id}
        args = [url, data]
        return cache_object(self._post, string, args, False, 24)

    def get_hosts(self):
        hosts_dict = {'Premiumize.me': []}
        hosts = []
        string = "fen_pm_valid_hosts"
        url = "services/list"
        try:
            result = cache_object(self._get, string, url, False, 8)
            for x in result['directdl']:
                for alias in result['aliases'][x]:
                    hosts.append(alias.split('.')[0])
            hosts_dict['Premiumize.me'] = list(set(hosts))
        except: pass
        return hosts_dict

    def add_headers_to_url(self, url):
        import urllib
        headers = {'User-Agent': self.user_agent, 'Authorization': 'Bearer %s' % self.token}
        return url + '|' + urllib.urlencode(to_utf8(headers))

    def _get(self, url, data={}):
        if self.token == '': return None
        headers = {'User-Agent': self.user_agent, 'Authorization': 'Bearer %s' % self.token}
        url = self.base_url + url
        response = requests.get(url, data=data, headers=headers, timeout=self.timeout).text
        try: return to_utf8(json.loads(response))
        except: return to_utf8(response)

    def _post(self, url, data={}):
        if self.token == '' and not 'token' in url: return None
        headers = {'User-Agent': self.user_agent, 'Authorization': 'Bearer %s' % self.token}
        if not 'token' in url: url = self.base_url + url
        response = requests.post(url, data=data, headers=headers, timeout=self.timeout).text
        try: return to_utf8(json.loads(response))
        except: return to_utf8(response)

    def revoke_auth(self):
        __addon__.setSetting('pm.account_id', '')
        __addon__.setSetting('pm.token', '')
        xbmcgui.Dialog().ok('Premiumize', 'Revoke Authentication Successful.')

    def clear_cache(self):
        try:
            import xbmc, xbmcvfs
            import os
            PM_DATABASE = os.path.join(xbmc.translatePath(__addon__.getAddonInfo('profile')), 'fen_cache.db')
            if not xbmcvfs.exists(PM_DATABASE): return True
            try: from sqlite3 import dbapi2 as database
            except ImportError: from pysqlite2 import dbapi2 as database
            dbcon = database.connect(PM_DATABASE)
            dbcur = dbcon.cursor()
            dbcur.execute("""DELETE FROM fencache WHERE id LIKE ?""", ("fen_pm_user_cloud%",))
            dbcon.commit()
            dbcon.close()
            return True
        except: return False
