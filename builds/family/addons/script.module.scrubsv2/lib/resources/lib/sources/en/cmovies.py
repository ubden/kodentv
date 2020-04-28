# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cmovies.cc']
        self.base_link = 'https://cmovies.cc'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url  % (search_id.replace(':', ' ').replace(' ', '+'))
            search_results = client.request(url)
            match = re.compile('<span class="project-details"><a href="(.+?)">(.+?)</a>', re.DOTALL).findall(search_results)
            for row_url, row_title in match:
                if cleantitle.get(title) in cleantitle.get(row_title):
                    if year in str(row_title):
                        return row_url
            return
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostDict + hostprDict
            if url == None:
                return sources
            html = client.request(url)
            links = re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(html)
            for link in links:
                if not link.startswith('http'):
                    link =  "https:" + link
                valid, host = source_utils.is_host_valid(link, hostDict)
                quality,info = source_utils.get_release_quality(link, link)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            links2 = re.compile('<li><a href="//(.+?)"', re.DOTALL).findall(html)
            for link2 in links2:
                if 'watchseriestv.tv' in link2 or 'watchlivesport.ws' in link2:
                    continue
                link2 =  "https://" + link2
                valid, host = source_utils.is_host_valid(link2, hostDict)
                if valid:
                    quality,info = source_utils.get_release_quality(link2, link2)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link2, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


