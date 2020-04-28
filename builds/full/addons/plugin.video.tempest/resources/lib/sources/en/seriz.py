# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
import traceback
from resources.lib.modules import client, log_utils
from resources.lib.modules import cleantitle, jsunpack


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['seriz.tn']
        self.base_link = 'https://seriz.tn'
        self.headers = {'User-Agent': client.agent()}

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, episode, year):
        try:
            season = '%s Season %01d' % (title, int(season))
            search = '%s/?s=%s' % (self.base_link, title)
            try:
                r = client.request(search, headers=self.headers)
                page = re.compile('<a class="page-numbers" href=".+?">(.+?)</a>').findall(r)[0]
                if page:
                    urls = [('https://seriz.tn/page/%s/?s=%s' % (page, title),
                            search)]
                    for url in urls[0]:
                        r = client.request(url, headers=self.headers)
                        r = re.compile('<a href="(.+?)" rel="bookmark"><span class=".+?"></span>(.+?)</a>').findall(r)
                        r = [i for i in r if season in i[1]][0][0]
                        r = client.request(r, headers=self.headers)
                        r = re.compile('<div role=".+?" class=".+?" id="tabs_desc_.+?_(.+?)">\s+<IFRAME SRC="(.+?)" .+?</IFRAME>').findall(r)
                        url = [i[1] for i in r if str(episode) in i[0]][0]
                        return url
            except:
                r = client.request(search, headers=self.headers)
                r = re.compile('<a href="(.+?)" rel="bookmark"><span class=".+?"></span>(.+?)</a>').findall(r)
                r = [i for i in r if season in i[1]][0][0]
                r = client.request(r, headers=self.headers)
                r = re.compile('<div role=".+?" class=".+?" id="tabs_desc_.+?_(.+?)">\s+<IFRAME SRC="(.+?)" .+?</IFRAME>').findall(r)
                url = [i[1] for i in r if str(episode) in i[0]][0]
                return url
        except:
            return self.sources

    def sources(self, url, hostDict, hostprDict):
        try:
            self.sources = []
            if url is None:
                return self.sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle']
            url = self.searchShow(title, int(data['season']), int(data['episode']), data['year'])
            self.sources.append({'source': 'Stream', 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return self.sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---SERIZ Testing - Exception: \n' + str(failure))
            return self.sources

    def resolve(self, url):
        try:
            url = client.request(url, headers=self.headers)
            url = re.findall(r'\s*(eval.+?)\s*</script', url, re.DOTALL)[0]
            url = jsunpack.unpack(url)
            url = re.findall('src:"http[s](.+?)"', url)[0]
            url = 'http' + url
            return url
        except:
            return url
