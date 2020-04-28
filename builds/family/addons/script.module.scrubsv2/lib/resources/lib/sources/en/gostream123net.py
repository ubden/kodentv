# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['gostream123.net']
        self.base_link = 'https://www.gostream123.net'
        self.search_link = '/?s=%s+%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            movietitle = cleantitle.geturl(title)
            url = self.base_link + self.search_link % (movietitle, year)
            page = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            items = client.parseDOM(page, 'div', attrs={'class': 'item'})
            for item in items:
                match = re.compile('<a href="(.+?)">', re.DOTALL).findall(item)
                for url in match:
                    if cleantitle.get(title) in cleantitle.get(url):
                        return url
            return
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostprDict + hostDict
            sources = []
            if url == None:
                return sources
            page = client.request(url, headers=client.randommobileagent('android'), timeout='3')
            links = re.compile('<IFRAME SRC="(.+?)"', re.DOTALL).findall(page)
            for link in links:
                valid, host = source_utils.is_host_valid(link, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(link, link)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


