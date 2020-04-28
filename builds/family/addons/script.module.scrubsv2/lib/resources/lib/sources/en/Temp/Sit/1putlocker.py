# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import more_sources
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['1putlocker.io']
        self.base_link = 'https://1putlocker.io'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + '/%s/' % title
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
            url = self.base_link + '/episode/%s-season-%s-episode-%s/' % (url, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = self.scraper.get(url).content
            match = re.compile('<iframe.+?src="(.+?)"').findall(r)
            for url in match:
                if 'gomostream.com' in url:
                    for source in more_sources.more_gomo(url, hostDict):
                        sources.append(source)
                else:
                    quality, info = source_utils.get_release_quality(url, url)
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


