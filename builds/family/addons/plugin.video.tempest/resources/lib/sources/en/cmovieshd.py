# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# -Cleaned and Checked on 04-14-2020 by Tempest.
# -Created by Tempest

import re
from resources.lib.modules import cleantitle, client, log_utils
from resources.lib.modules import source_utils
from resources.lib.sources import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cmovies.video', 'cmovieshd.bz']
        self.base_link = 'https://cmovies.tv'
        self.search_link = '/film/%s/watching.html?ep=0'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('--', '-')
            url = self.base_link + self.search_link % title
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            r = cfscrape.get(url, headers=self.headers)
            qual = re.compile('class="quality">(.+?)</span>').findall(r)
            quality = source_utils.check_url(qual)
            u = re.compile('data-video="(.+?)"').findall(r)
            for url in u:
                if not url.startswith('http'):
                    url = "https:" + url
                if 'load.php' not in url:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
