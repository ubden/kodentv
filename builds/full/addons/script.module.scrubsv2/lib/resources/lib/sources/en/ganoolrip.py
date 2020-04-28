# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import cfscrape
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import more_sources
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  #  Old  ganool.rip  ganool.fun
        self.domains = ['ganool.cam']
        self.base_link = 'https://ganool.cam'
        self.search_link = '/?s=%s+%s'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            url = self.base_link + self.search_link % (title, year)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            r = self.scraper.get(url).content
            u = client.parseDOM(r, "div", attrs={"class": "ml-item"})
            for i in u:
                t = re.compile('<a href="(.+?)"').findall(i)
                for r in t:
                    t = self.scraper.get(r).content
                    results1 = re.compile('<a href="(.+?)" class="lnk').findall(t)
                    for url in results1:
                        if self.base_link in url:
                            continue
                        quality, info = source_utils.get_release_quality(url, url)
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
                    results2 = re.compile('<iframe src="(.+?)"').findall(t)
                    for link in results2:
                        if "gomostream.com" in link:
                            for source in more_sources.more_gomo(link, hostDict):
                                sources.append(source)
                        else:
                            if "//ouo.io/" in link:
                                continue
                            quality, info = source_utils.get_release_quality(link, link)
                            valid, host = source_utils.is_host_valid(link, hostDict)
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


