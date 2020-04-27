
import requests
import gzip
try: from StringIO import StringIO ## for Python 2
except ImportError: from io import StringIO ## for Python 3
try: from urllib import quote ## for Python 2
except ImportError: from urllib.parse import quote ## for Python 3
import json
import time
from modules.nav_utils import notification
from modules.utils import to_utf8
# from modules.utils import logger


class OpenSubtitlesAPI:
    def __init__(self):
        self.base_url = 'https://rest.opensubtitles.org/search'
        self.user_agent = 'Fen v1.0'
        self.headers = {'User-Agent': self.user_agent}

    def search(self, query, imdb_id, language, season=None, episode=None):
        url = '/imdbid-%s/query-%s' % (imdb_id, quote(query))
        if season: url += '/season-%d/episode-%d' % (season, episode)
        url += '/sublanguageid-%s' % language
        url = self.base_url + url
        response = self._get(url, retry=True)
        response = to_utf8(json.loads(response.text))
        return response

    def download(self, url):
        response = self._get(url, stream=True, retry=True)
        content = gzip.GzipFile(fileobj=StringIO(response.content)).read()
        return content

    def _get(self, url, stream=False, retry=False):
        response = requests.get(url, headers=self.headers, stream=stream)
        if '200' in str(response):
            return response
        elif '429' in str(response) and retry:
            notification('OpenSubtitles Rate Limited. Retrying in 10 secs..', 3500)
            time.sleep(10)
            return self._get(url, stream)
        else: return
