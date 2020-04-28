import xbmc, xbmcvfs, xbmcaddon
import requests
import json
import os
from tikimeta.metacache import cache_function
from tikimeta.utils import to_utf8
# from tikimeta.utils import logger

class KyraDBAPI:
    def __init__(self, api_key, user_key):
        self.gifs_path = 'special://userdata/addon_data/script.module.tikimeta/animated_gifs/'
        self.api_key = api_key
        self.user_key = user_key
        self.base_url = 'https://www.kyradb.com/api10/'
        self.posters_url = 'https://www.kyradb.com/posters/w342/'
        self.made_image_url = False

    def get_art(self, tmdb_id):
        self.tmdb_id = tmdb_id
        local_art = self._scrape_local()
        if local_art:
            return local_art
        art_data = None
        string = 'kyradb_%s' % self.tmdb_id
        url = 'movie/tmdbid/%s/images/animated' % self.tmdb_id
        try:
            results = cache_function(self._get, string, url, 24, False)
            if results['error'] == 4:
                return {'gif_poster': '',
                        'kyradb_added': True}
            art_data = {'gif_poster': self._get_query(results.get('posters')), 'kyradb_added': True}
        except: pass
        return art_data

    def _scrape_local(self):
        local_name = '%s.gif' % self.tmdb_id
        local_filename = xbmc.translatePath(os.path.join(self.gifs_path, local_name))
        if xbmcvfs.exists(local_filename):
            return {'gif_poster': local_filename, 'kyradb_added': True}
        return None

    def _get_query(self, results):
        if results == []: return ''
        try:
            result = [(x['name'], x['likes']) for x in results if x.get('language') == 'english']
            if not result: result = [(x['name'], x['likes']) for x in results]
            result = [(x[0], x[1]) for x in result]
            result = sorted(result, key=lambda x: int(x[1]), reverse=True)
            result = [x[0] for x in result][0]
            try: result = result.encode('utf-8')
            except: pass
            image_url = self.posters_url + result
            result = self._make_local(image_url)
        except:
            result = ''
        return result

    def _make_local(self, image_url):
        if not xbmcvfs.exists(self.gifs_path):
            xbmcvfs.mkdirs(self.gifs_path)
        local_name = '%s.gif' % self.tmdb_id
        local_filename = xbmc.translatePath(os.path.join(self.gifs_path, local_name))
        img = xbmcvfs.File(image_url)
        img_data = img.readBytes()
        img.close()
        img = xbmcvfs.File(local_filename, 'w')
        img.write(img_data)
        img.close()
        return local_filename

    def _get(self, url):
        headers = {'User-Agent': 'Fen Kodi', 'Content-type': 'application/json', 'Apikey': self.api_key, 'Userkey': self.user_key}
        url = self.base_url + url
        response = requests.get(url, headers=headers).text
        try: return to_utf8(json.loads(response))
        except: return to_utf8(response)

def add(remote_id, meta, api_key, user_key):
    try:
        gif_data = KyraDBAPI(api_key, user_key).get_art(remote_id)
        meta['gif_poster'] = gif_data['gif_poster']
        meta['kyradb_added'] = gif_data['kyradb_added']
    except: pass
    return meta

