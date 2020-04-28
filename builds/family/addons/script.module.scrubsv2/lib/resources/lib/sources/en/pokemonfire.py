# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['pokemonfire.com']
        self.base_link = 'https://www.pokemonfire.com'
        self.movie_link = '/movies/%s'
        self.tv_link = '/episodes/%s-season-%s-episode-%s/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            ctitle = cleantitle.geturl(title)
            url = self.base_link + self.movie_link % (ctitle)
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
            if not url:
                return
            url = self.base_link + self.tv_link % (url,season,episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = client.request(url)
            match = re.compile('<iframe.+?src="(.+?)"').findall(r)
            for url in match:
                valid, host = source_utils.is_host_valid(url, hostDict)
                quality, info = source_utils.get_release_quality(url, url)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False}) 
            return sources
        except:
            return sources


    def resolve(self, url):
        if 'veohb.net/vid.php?' in url:
            r = client.request(url)
            url = re.compile('<source src="(.+?)"').findall(r)[0]
            return url
        elif self.base_link in url:
            r = client.request(url)
            url = re.compile("file: '(.+?)'").findall(r)[0]
            return url
        else:
            return url


