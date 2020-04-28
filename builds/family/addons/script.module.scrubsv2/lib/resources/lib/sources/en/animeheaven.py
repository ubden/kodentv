# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import getSum
from resources.lib.modules import source_tools
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animeheaven.cc']
        self.base_link = 'https://animeheaven.cc'
        self.search_link = '/anime?search_name=%s'
        self.tv_maze = tvmaze.tvMaze()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = self.tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']
            t = tvshowtitle.replace(' ', '+').lower()
            q = self.base_link + self.search_link % t
            r = client.request(q)
            match = re.compile('<a class="cona" href="(.+?)">(.+?)</a>', re.DOTALL).findall(r)
            for url, title in match:
                if cleantitle.get(tvshowtitle) in cleantitle.get(title):
                    return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            num = self.tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            check = 'episode-%s' % num
            r = client.request(url)
            match = re.compile('<a class="infovan" href="(.+?)">', re.DOTALL).findall(r)
            for url in match:
                if url.endswith(check):
                    return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = client.request(url)
            links = re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(r)
            for u in links:
                r = client.request(u)
                match = getSum.findSum(r)
                for link in match:
                    valid, host = source_tools.checkHost(link, hostDict)
                    if valid:
                        info = source_tools.get_info(link)
                        quality = source_tools.get_quality(link)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


