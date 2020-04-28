# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# Has shows but dont feel like coding it in.

import re, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['gostream.pw', 'gostream.cool']
        self.base_link = 'https://www.gostream.pw/'
        self.search_link = 'index.php?do=search'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title)
            search_url = urlparse.urljoin(self.base_link, self.search_link)
            post = ('do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s' % (clean_title.replace('-','+')))
            page = client.request(search_url, post=post)
            items = client.parseDOM(page, 'div', attrs={'class': 'ml-item'})
            for item in items:
                check = re.findall('<div class="jt-info jt-imdb"><a href="https://www.gostream.pw/search/year/(.+?)/">', item)[0]
                match = re.compile('<a href="(.+?)"', re.DOTALL).findall(item)
                for url in match:
                    if cleantitle.get(title) in cleantitle.get(url) and cleantitle.get(year) in cleantitle.get(check):
                        return url
            return
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            page = client.request(url)
            qual = re.compile('<span class="quality">(.+?)</span>', re.DOTALL).findall(page)[0]
            items = client.parseDOM(page, 'div', attrs={'class': 'les-content'})
            for item in items:
                link = re.compile('data-link="(.+?)"', re.DOTALL).findall(item)[0]
                link = "https:" + link if not link.startswith('http') else link
                valid, host = source_utils.is_host_valid(link, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(qual, link)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


