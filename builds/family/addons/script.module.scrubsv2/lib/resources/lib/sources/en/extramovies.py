# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urllib, urlparse, base64
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['extramovies.blue']
        self.base_link = 'http://extramovies.blue'
        self.search_link = '/?s=%s'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            self.hostDict = hostDict + hostprDict
            if url == None:
                return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query(title)))
            html = self.scraper.get(url).content
            match = re.compile('<div class="thumbnail".+?href="(.+?)" title="(.+?)"', re.DOTALL | re.IGNORECASE).findall(html)
            for url, item_name in match:
                if cleantitle.getsearch(title).lower() in cleantitle.getsearch(item_name).lower():
                    quality, info = source_utils.get_release_quality(url, url)
                    result = self.scraper.get(url).content
                    regex = re.compile('href="/download.php.+?link=(.+?)"', re.DOTALL | re.IGNORECASE).findall(result)
                    for link in regex:
                        if 'server=' not in link:
                            try:
                                link = base64.b64decode(link)
                            except:
                                pass
                            valid, host = source_utils.is_host_valid(link, self.hostDict)
                            if valid:
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False, 'debridonly': False})
                    regexALT1 = re.compile('play.png" /> <a href="(.+?)"', re.DOTALL | re.IGNORECASE).findall(result)
                    for urlALT in regexALT1:
                        urlALT = self.base_link + urlALT
                        resultALT = self.scraper.get(urlALT).content
                        regexALT2 = re.compile('<IFRAME SRC="(.+?)"', re.DOTALL | re.IGNORECASE).findall(resultALT)
                        for link in regexALT2:
                            valid, host = source_utils.is_host_valid(link, self.hostDict)
                            if valid:
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


