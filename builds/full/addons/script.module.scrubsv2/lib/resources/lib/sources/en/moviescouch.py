# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  #  Old  moviescouch.xyz  moviescouch.pro  moviescouch.pw
        self.domains = ['moviescouch.vip']
        self.base_link = 'https://moviescouch.vip'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search_id.replace(':', ' ').replace(' ', '+'))
            search_results = client.request(url)
            match = re.compile('<h1 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h1>', re.DOTALL).findall(search_results)
            for row_url, row_title in match:
                if cleantitle.get(title) in cleantitle.get(row_title) and year in cleantitle.get(row_title):
                    return row_url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            html = client.request(url)
            links = re.compile('<iframe src="(.+?)"', re.DOTALL).findall(html)
            for link in links:
                try:
                    quality = re.compile('<li>Quality: – (.+?)</li>', re.DOTALL).findall(html)[0]
                    info = re.compile('<li>Size: – (.+?)</li>', re.DOTALL).findall(html)[0]
                except:
                    quality, info = source_utils.get_release_quality(link, link)
                valid, host = source_utils.is_host_valid(link, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


