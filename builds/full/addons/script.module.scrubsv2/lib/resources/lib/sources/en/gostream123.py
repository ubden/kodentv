# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  #  Old  movie-32.com  gostream-123.com
        self.domains = ['movie-32.online', 'gomovies123.today']
        self.base_link = 'http://movie-32.online'
        self.search_link = '/?s=%s+%s'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mvtitle = cleantitle.geturl(title)
            searchtit = mvtitle.replace('-', '+').replace('++', '+')
            url = self.base_link + self.search_link % (searchtit, year)
            r = self.scraper.get(url).content
            match = re.compile('<a href="(.+?)" title="(.+?)">').findall(r)
            for url, check in match:
                tity = '%s (%s)' % (title, year)
                if not cleantitle.get(tity) in cleantitle.get(check):
                    continue
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
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False}) 
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


