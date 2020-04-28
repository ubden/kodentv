# -*- coding: utf-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# Created by Tempest

import re, urllib, urlparse
from resources.lib.modules import cfscrape
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en', 'de', 'fr', 'ko', 'pl', 'pt', 'ru']
        self.domains = ['mkvcage.nl', 'mkvcage.com', 'mkvcage.me', 'mkvcage.fun', 'mkvcage.cc']
        self.base_link = 'https://www.mkvcage.nl/'
        self.search_link = '?s=%s'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None:
                return sources
            if debrid.status() is False:
                raise Exception()
            if debrid.tor_enabled() is False:
                raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            r = self.scraper.get(url).content
            posts = client.parseDOM(r, 'h2', attrs={'class': 'entry-title'})
            for post in posts:
                data = client.parseDOM(post, 'a', ret='href')
                for u in data:
                    r = self.scraper.get(u).content
                    r = client.parseDOM(r, 'div', attrs={'class': 'clearfix entry-content'})
                    for t in r:
                        link = re.findall('a class="buttn magnet" href="(.+?)"', t)[0]
                        if link in str(sources):
                            continue
                        quality, info = source_utils.get_release_quality(u)
                        try:
                            size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:gb|gib|mb|mib))', str(data))[-1]
                            div = 1 if size.endswith(('gb')) else 1024
                            size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                            size = '%.2f gb' % size
                            info.append(size)
                        except:
                            pass
                        info = ' | '.join(info)
                        sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': True})
            return sources
        except :
            return sources


    def resolve(self, url):
        return url


