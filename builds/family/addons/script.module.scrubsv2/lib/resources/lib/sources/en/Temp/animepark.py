# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urlparse, base64
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_tools
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animesim.com']
        self.base_link = 'https://animesim.com'
        self.show_link = '/%s-episode-%s/'
        self.tv_maze = tvmaze.tvMaze()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = self.tv_maze.showLookup('thetvdb', tvdb)
            url = tvshowtitle['name']
            url = cleantitle.geturl(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            num = self.tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            url = self.base_link + self.show_link % (url.lower(), num)
            url = url.replace(' ','-')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = client.request(url, headers=client.randommobileagent('android'))
            match = re.compile('<option data-em="(.+?)"', re.DOTALL).findall(r)
            for u in match:
                r = base64.b64decode(u)
                r = client.parseDOM(r, 'iframe', ret='src')[0]
                r = client.request(r, headers=client.randommobileagent('android'))
                try:
                    u = client.parseDOM(r, 'iframe', ret='src')[0]
                except:
                    u = client.parseDOM(r, 'source', ret='src')[0]
                valid, host = source_tools.checkHost(u, hostDict)
                if valid:
                    info = source_tools.get_info(u)
                    quality = source_tools.get_quality(u)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': u, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


