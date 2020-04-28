# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_tools
from resources.lib.modules import source_utils
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animeshow.tv']
        self.base_link = 'http://www.animeshow.tv'
        self.search_link = '/find.html?key=%s'
        self.episode_link = '/%s-episode-%s'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tv_maze = tvmaze.tvMaze()
            tvshowtitle = tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']
            t = cleantitle.get(tvshowtitle)
            q = self.base_link + self.search_link %(tvshowtitle)
            r = client.request(q)
            match = re.compile('<div class="genres_result"><a href="(.+?)">',re.DOTALL).findall(r)
            for url in match:
                if t in cleantitle.get(url):
                    return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            tv_maze = tvmaze.tvMaze()
            num = tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            url = self.episode_link % (url.replace('http://www.animeshow.tv/', '').replace('/', ''), num)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            if url == None:
                return sources
            try:
                vurl = urlparse.urljoin(self.base_link, url)
                r = client.request(vurl)
                links = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(r)
                for u in links:
                    if not 'http' in u:
                        continue
                    quality = source_tools.get_quality(u)
                    info = source_tools.get_info(u)
                    valid, host = source_utils.is_host_valid(u, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': u, 'info': info, 'direct': False, 'debridonly': False})
            except:
                pass
            try:
                vurl2 = urlparse.urljoin(self.base_link, url + '-mirror-2/')
                r2 = client.request(vurl2)
                links2 = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(r2)
                for u2 in links2:
                    if not 'http' in u2:
                        continue
                    quality2 = source_tools.get_quality(u2)
                    info2 = source_tools.get_info(u2)
                    valid, host2 = source_utils.is_host_valid(u2, hostDict)
                    if valid:
                        sources.append({'source': host2, 'quality': quality2, 'language': 'en', 'url': u2, 'info': info2, 'direct': False, 'debridonly': False})
            except:
                pass
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


