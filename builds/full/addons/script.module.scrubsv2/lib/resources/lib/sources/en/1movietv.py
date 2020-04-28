# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, requests
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['1movietv.com']
        self.base_link = 'https://1movietv.com'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}
        self.session = requests.Session()
        self.tm_user = control.setting('tm.user')


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + '/playstream/' + imdb
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tmdburl = 'https://api.themoviedb.org/3/find/%s?external_source=tvdb_id&language=en-US&api_key=%s' % (tvdb, self.tm_user)
            tmdbresult = self.session.get(tmdburl, headers=self.headers).content
            tmdb_id = re.compile('"id":(.+?),', re.DOTALL).findall(tmdbresult)[0]
            url = '/playstream/' + tmdb_id
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = self.base_link + url + '-' + season + '-' + episode
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = self.session.get(url, headers=self.headers).content
            match = re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(r)
            for url in match:
                url =  "https:" + url if not url.startswith('http') else url
                valid, host = source_utils.is_host_valid(url, hostDict)
                quality, info = source_utils.get_release_quality(url, url)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


