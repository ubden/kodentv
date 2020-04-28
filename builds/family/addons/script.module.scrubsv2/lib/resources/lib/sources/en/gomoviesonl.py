# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# host limit code is a must on this one, otherwise your getting 1000+ results for aquaman lol.

import re, requests
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['gomovies.onl']
        self.base_link = 'http://ww.gomovies.onl'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}
        self.session = requests.Session()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + '/movie/%s-%s/watching.html' % (title, imdb)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            tvshowtitle = url
            url = self.base_link + '/show/%s/season/%s/episode/%s' % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostDict + hostprDict
            r = self.session.get(url, headers=self.headers).content
            match = re.compile('<IFRAME.+?SRC="(.+?)"', re.DOTALL | re.IGNORECASE).findall(r)
            for url in match:
                url =  "https:" + url if not url.startswith('http') else url
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    if source_utils.limit_hosts() is True and host in str(sources):
                        continue
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


