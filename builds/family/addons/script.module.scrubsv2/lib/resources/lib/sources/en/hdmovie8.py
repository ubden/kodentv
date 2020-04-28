# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdmovie8.com']
        self.base_link = 'https://hdmovie8.com'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movietitle = cleantitle.geturl(title)
            url = self.base_link + '/movies/%s-%s/' % (movietitle, year)
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
            url = self.base_link + '/episodes/%s-%sx%s/' % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostDict + hostprDict
            sourcePage = self.scraper.get(url).content
            thesources = re.compile('<tbody>(.+?)</tbody>', re.DOTALL).findall(sourcePage)[0]
            links = re.compile("<a href=\'(.+?)\' target=\'_blank\'>Download</a>", re.DOTALL).findall(thesources)
            for link in links:
                linkPage = self.scraper.get(link).content
                vlink = re.compile('<a id="link" rel="nofollow" href="(.+?)" class="btn"', re.DOTALL).findall(linkPage)
                for zlink in vlink:
                    valid, host = source_utils.is_host_valid(zlink, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(zlink, zlink)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': zlink, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


