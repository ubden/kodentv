# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.
# -Cleaned and Checked on 04-14-2020 by Tempest.

import urlparse, re
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['fmoviesto.to']
        self.base_link = 'https://www4.fmovies2.io'
        self.search_link = '/search.html?keyword=%s'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search_id.replace(':', ' ').replace(' ', '+'))
            search_results = client.request(url, headers=self.headers)
            match = re.compile('<a href="/watch/(.+?)" title="(.+?)">').findall(search_results)
            for row_url, row_title in match:
                row_url = self.base_link + '/watch/%s' % row_url
                if cleantitle.get(title) in cleantitle.get(row_title):
                    return row_url
            return
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostDict + hostprDict
            if url is None:
                return sources
            html = client.request(url, headers=self.headers)
            quality = re.compile('<div>Quanlity: <span class="quanlity">(.+?)</span></div>').findall(html)
            for qual in quality:
                quality = source_utils.check_url(qual)
                info = qual
            links = re.compile('var link_.+? = "(.+?)"').findall(html)
            for url in links:
                if not url.startswith('http'):
                    url = "https:" + url
                if 'load.php' not in url:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
