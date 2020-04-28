import xbmcaddon
import requests
import re
try: from urllib import urlencode # Python 2
except ImportError: from urllib.parse import urlencode # Python 3
try: from urllib import quote # Python 2
except ImportError: from urllib.parse import quote # Python 3
import json
import datetime
import base64
from modules import fen_cache
from modules.utils import to_utf8
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
_cache = fen_cache.FenCache()

SORT = {'s1': 'relevance', 's1d': '-', 's2': 'dsize', 's2d': '-', 's3': 'dtime', 's3d': '-'}
SEARCH_PARAMS = {'st': 'adv', 'sb': 1, 'fex': 'mkv, mp4, avi, mpg, wemb', 'fty[]': 'VIDEO', 'spamf': 1, 'u': '1', 'gx': 1, 'pno': 1, 'sS': 3}
SEARCH_PARAMS.update(SORT)

class EasyNewsAPI:
    def __init__(self):
        self.base_url = 'https://members.easynews.com'
        self.search_link = '/2.0/search/solr-search/advanced'
        self.username = __addon__.getSetting('easynews_user')
        self.password = __addon__.getSetting('easynews_password')
        self.moderation = 1 if __addon__.getSetting('easynews_moderation') == 'true' else 0
        self.auth = self._get_auth()
        self.account_link = 'https://account.easynews.com/editinfo.php'
        self.usage_link = 'https://account.easynews.com/usageview.php'
        self.timeout = 12.0

    def _get_auth(self):
        try:
            auth = 'Basic ' + base64.b64encode('%s:%s' % (self.username, self.password))
        except:
            user_info = '%s:%s' % (self.username, self.password)
            user_info = user_info.encode('utf-8')
            auth = 'Basic ' + base64.b64encode(user_info).decode('utf-8')
        return auth

    def search(self, query):
        self.search_url, self.params = self._translate_search(query)
        cache_name = 'fen_EASYNEWS_SEARCH_' + urlencode(self.params)
        cache = _cache.get(cache_name)
        if cache:
            files = cache
        else:
            results = self._get(self.search_url, self.params)
            files = to_utf8(self._process_files(results))
            _cache.set(cache_name, files,
                expiration=datetime.timedelta(hours=2))
        return files

    def account(self):
        try:
            from bs4 import BeautifulSoup
            account_html = self._get(self.account_link)
            if account_html == None or account_html == '': raise Exception()
            account_html = BeautifulSoup(account_html, "html.parser")
            account_html = account_html.find_all('form', id='accountForm')[0]
            account_html = account_html.find_all('table', recursive=False)[0]
            account_html = account_html.find_all('tr', recursive=False)
            usage_html = self._get(self.usage_link)
            if usage_html == None or usage_html == '': raise Exception()
            usage_html = BeautifulSoup(usage_html, "html.parser")
            usage_html = usage_html.find_all('div', class_='table-responsive')[0]
            usage_html = usage_html.find_all('table', recursive=False)[0]
            usage_html = usage_html.find_all('tr', recursive=False)
            return account_html, usage_html
        except Exception as e:
            from modules.utils import logger
            logger('easynews API account error', e)

    def _process_files(self, files):
        results = []
        down_url = files.get('downURL')
        dl_farm = files.get('dlFarm')
        dl_port = files.get('dlPort')
        files = files.get('data', [])
        for item in files:
            try:
                post_hash, size, post_title, ext, duration = item['0'], item['4'], item['10'], item['11'], item['14']
                checks = [False] * 5
                if 'alangs' in item and item['alangs'] and 'eng' not in item['alangs']: checks[1] = True
                if re.match('^\d+s', duration) or re.match('^[0-5]m', duration): checks[2] = True
                if 'passwd' in item and item['passwd']: checks[3] = True
                if 'virus' in item and item['virus']: checks[4] = True
                if 'type' in item and item['type'].upper() != 'VIDEO': checks[5] = True
                if any(checks):
                    continue
                stream_url = down_url + quote('/%s/%s/%s%s/%s%s' % (dl_farm, dl_port, post_hash, ext, post_title, ext))
                file_name = post_title
                file_dl = stream_url + '|Authorization=%s' % (quote(self.auth))
                results.append({'name': file_name,
                                'size': size,
                                'rawSize': item['rawSize'],
                                'url_dl': file_dl,
                                'full_item': item})
            except: pass
        return results

    def _translate_search(self, query):
        params = SEARCH_PARAMS
        params['pby'] = 100
        params['safeO'] = self.moderation
        params['gps'] = params['sbj'] = query
        url = self.base_url + self.search_link
        return url, params

    def _get(self, url, params={}):
        headers = {'Authorization': self.auth}
        response = requests.get(url, params=params, headers=headers, timeout=self.timeout).text
        try: return to_utf8(json.loads(response))
        except: return to_utf8(response)

def clear_media_results_database():
    import xbmc
    try: from sqlite3 import dbapi2 as database
    except ImportError: from pysqlite2 import dbapi2 as database
    profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
    try: fen_cache_file = xbmc.translatePath("%s/fen_cache.db" % profile_dir).decode('utf-8')
    except: fen_cache_file = xbmc.translatePath("%s/fen_cache.db" % profile_dir)
    dbcon = database.connect(fen_cache_file)
    dbcur = dbcon.cursor()
    try:
        dbcur.execute("DELETE FROM fencache WHERE id LIKE 'fen_EASYNEWS_SEARCH_%'")
        dbcon.commit()
        dbcon.close()
        return 'success'
    except: return 'failed'

