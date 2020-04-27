# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urllib, urlparse
from resources.lib.modules import cfscrape
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_tools
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animedao.com']
        self.base_link = 'https://animedao.com'
        self.search_link = '/search/?key=%s'
        self.episode_link = '/watch-online/%s-episode-%s'
        self.tv_maze = tvmaze.tvMaze()
        self.scraper = cfscrape.create_scraper()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = self.tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']
            t = cleantitle.get(tvshowtitle)
            q = urlparse.urljoin(self.base_link, self.search_link)
            q = q % urllib.quote_plus(tvshowtitle)
            r = self.scraper.get(q).content
            r = client.parseDOM(r, 'div', attrs={'class': 'col-xs-12 col-sm-6 col-md-6 col-lg-4'})
            r = [(client.parseDOM(i, 'a', ret='href'), re.findall('<h4>(.+?)<br />', i), re.findall('\d{4}', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][-1]) for i in r if i[0] and i[1] and i[2]]
            r = [i for i in r if t in cleantitle.get(i[1]) and year == i[2]]
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
            num = self.tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            url = [i for i in url.strip('/').split('/')][-1]
            url = self.episode_link % (url, num)
            url = urlparse.urljoin(self.base_link, url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            if url == None:
                return sources
            r = self.scraper.get(url).content
            r = client.parseDOM(r, 'iframe', ret='src')
            for u in r:
                info = source_tools.get_info(u)
                quality = source_tools.get_quality(u)
                valid, host = source_tools.checkHost(u, hostDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': u, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        if 'proxydata.me' in url:
            url = url.replace('proxydata.me', 'animeproxy.info')
        return url


