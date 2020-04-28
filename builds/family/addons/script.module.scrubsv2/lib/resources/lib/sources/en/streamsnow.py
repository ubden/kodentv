# -*- coding: utf-8 -*-
# Created by Tempest

import re
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['streams-api.now.sh']
        self.base_link = 'https://streams-api.now.sh'
        self.search_link = '/?s=es&q=%s+%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % (title, year)
            url = url.lower().replace('+','%20').replace(': ','%20').replace(' ','%20')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile('"title":"(.+?)","url":"(.+?)","created"').findall(r)
                for qual, url in match:
                    quality, info = source_utils.get_release_quality(qual, qual)
                    sources.append({'source': 'verystream', 'quality': 'HD', 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            except:
                return
            try:
                match = re.compile('"links":\["(.+?)"\],').findall(r)
                for url in match:
                    qual = re.compile('"title":"(.+?)"').findall(r)
                    quality, info = source_utils.get_release_quality(qual, qual)
                    sources.append({'source': 'verystream', 'quality': 'HD', 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url
