# -*- coding: utf-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['2mycouchtuner.me', '2mycouchtuner.one', 'mycouchtuner.li', 'ecouchtuner.eu']
        self.base_link = 'https://2mycouchtuner.me'
        self.search_link = '/watch-%s-online/'
        self.scraper = cfscrape.create_scraper()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = cleantitle.geturl(tvshowtitle)
            url = self.base_link + self.search_link % tvshowtitle
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            r = self.scraper.get(url).content
            match = re.compile('2mycouchtuner\..+?/(.+?)/\' title=\'.+? Season ' + season + ' Episode ' + episode + '\:').findall(r)
            for url in match:
                url = 'https://mycouchtuner.li/' + url
                return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'Referer': url, 'User-Agent': 'Mozilla/5.0'}
            r = self.scraper.get(url, headers=headers).content
            match = re.compile('<iframe class=\'lazyload\' data-src=\'(.+?)\'').findall(r)
            for url in match:
                url =  "https:" + url if not url.startswith('http') else url
                valid, host = source_utils.is_host_valid(url, hostDict)
                quality, info = source_utils.get_release_quality(url, url)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


