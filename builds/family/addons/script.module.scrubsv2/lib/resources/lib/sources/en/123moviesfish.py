# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_tools


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movies.fish']
        self.base_link = 'https://www.123movies.fish'
        self.search_link = '/search/%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movietitle = cleantitle.geturl(title)
            url = self.base_link + self.search_link % movietitle
            page = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            items = client.parseDOM(page, 'div', attrs={'class': 'ml-item'})
            for item in items:
                match = re.compile('<a href="(.+?)".+?title="(.+?)">', re.DOTALL).findall(item)
                for row_url, row_title in match:
                    if cleantitle.get(title) in cleantitle.get(row_title):
                        url = row_url + 'watching.html'
                        return url
            return
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = cleantitle.geturl(tvshowtitle)
            url = self.base_link + self.search_link % tvshowtitle
            page = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            items = client.parseDOM(page, 'div', attrs={'class': 'ml-item'})
            for item in items:
                match = re.compile('<a href="(.+?)".+?title="(.+?)">', re.DOTALL).findall(item)
                for row_url, row_title in match:
                    if cleantitle.get(tvshowtitle) in cleantitle.get(row_title):
                        return row_url
            return
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + 'season/' + season + '/episode/' + episode + '/watching.html'
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            page = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            links = client.parseDOM(page, 'table', attrs={'class': 'movie_version'})
            for link in links:
                try:
                    qual = re.compile('<span class="quality_(.+?)"></span>', re.DOTALL).findall(link)[0]
                    hoster = re.compile('<span class="version_host">(.+?)</span>', re.DOTALL).findall(link)[0]
                    href = re.compile('<a href="(.+?)" class=', re.DOTALL).findall(link)[0]
                    vlink = self.base_link + href
                    valid, host = source_tools.checkHost(hoster, hostDict)
                    if valid and vlink not in str(sources):
                        quality = source_tools.get_quality(qual)
                        info = source_tools.get_info(qual)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': vlink, 'info': info, 'direct': False, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            link = client.request(url, timeout='6', output='geturl')
            return link
        except:
            return


