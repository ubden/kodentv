# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urlparse
from resources.lib.modules import client
from resources.lib.modules import source_tools
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animestreams.cc']
        self.base_link = 'https://animestreams.cc'
        self.show_link = '/episode/%s-episode-%s/'
        self.tv_maze = tvmaze.tvMaze()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = self.tv_maze.showLookup('thetvdb', tvdb)
            url = tvshowtitle['name']
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            num = self.tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            url = self.base_link + self.show_link % (url.lower(), num)
            url = url.replace(' ', '-')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = client.request(url, headers=client.randommobileagent('android'))
            match = re.compile('<input type="hidden" value="(.+?)"', re.DOTALL).findall(r)
            for url in match:
                url = "https:" + url if not url.startswith('http') else url
                if 'vidstreaming.io' in url:
                    r = client.request(url, headers=client.randommobileagent('android'))
                    match = re.compile('data-video="(.+?)"', re.DOTALL).findall(r)
                    for link in match:
                        link = "https:" + link if not link.startswith('http') else link
                        valid, host = source_tools.checkHost(link, hostDict)
                        if valid:
                            info = source_tools.get_info(link)
                            quality = source_tools.get_quality(link)
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
                else:
                    valid, host = source_tools.checkHost(url, hostDict)
                    if valid:
                        info = source_tools.get_info(url)
                        quality = source_tools.get_quality(url)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


