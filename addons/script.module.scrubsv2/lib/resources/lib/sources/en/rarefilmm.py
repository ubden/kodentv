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
        self.domains = ['rarefilmm.com']
        self.base_link = 'http://rarefilmm.com'
        self.search_link = '/?s=%s+%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            url = self.base_link + self.search_link % (title, year)
            searchPage = client.request(url)
            section = client.parseDOM(searchPage, "h2", attrs={"class": "excerpt-title"})
            for item in section:
                results = re.compile('<a href="(.+?)">(.+?)</a>').findall(item)
                for url, checkit in results:
                    zcheck = '%s (%s)' % (title, year)
                    if zcheck.lower() in checkit.lower():
                        return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostDict + hostprDict
            sourcesPage = client.request(url)
            resultsA = re.compile('<iframe src="(.+?)"').findall(sourcesPage)
            for url in resultsA:
                url =  "https:" + url if not url.startswith('http') else url
                quality, info = source_utils.get_release_quality(url, url)
                valid, host = source_utils.is_host_valid(url, hostDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            resultsB = re.compile('href="(.+?)"><strong>').findall(sourcesPage)
            for url in resultsB:
                quality, info = source_utils.get_release_quality(url, url)
                valid, host = source_utils.is_host_valid(url, hostprDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


