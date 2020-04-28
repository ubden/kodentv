# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urllib, urlparse
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
        self.domains = ['gogoanime.video', 'animego.to']
        self.base_link = 'https://gogoanime.video'
        self.search_link = '/search.html?keyword=%s'
        self.episode_link = '/%s-episode-%s'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tv_maze = tvmaze.tvMaze()
            tvshowtitle = tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']
            t = cleantitle.get(tvshowtitle)
            q = urlparse.urljoin(self.base_link, self.search_link)
            q = q % urllib.quote_plus(tvshowtitle)
            r = client.request(q)
            r = client.parseDOM(r, 'ul', attrs={'class': 'items'})
            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('\d{4}', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][-1]) for i in r if i[0] and i[1] and i[2]]
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]
            r = r[0][0]
            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            tv_maze = tvmaze.tvMaze()
            num = tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            url = [i for i in url.strip('/').split('/')][-1]
            url = self.episode_link % (url, num)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            if url == None:
                return sources
            url = urlparse.urljoin(self.base_link, url)
            r = client.request(url)
            r = client.parseDOM(r, 'a', ret='data-video')
            for u in r:
                if not u.startswith('http'):
                    u =  "https:" + u
                info = source_tools.get_info(u)
                quality = source_tools.get_quality(u)
                valid, host = source_utils.is_host_valid(u, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': u, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


