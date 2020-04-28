# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# Created by Tempest

import re, urllib, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['doublr.org']
        self.base_link = 'https://doublr.org'
        self.search_link = '/search?q=%s'


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
            if url is None:
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
            if url is None:
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
            try:
                r = client.request(url)
                posts = client.parseDOM(r, 'tr')
                for post in posts:
                    links = re.findall('<a href="(/torrent/.+?)">(.+?)<', post, re.DOTALL)
                    for link, data in links:
                        link = urlparse.urljoin(self.base_link, link)
                        link = client.request(link)
                        link = re.findall('a class=".+?" rel=".+?" href="(magnet:.+?)"', link, re.DOTALL)
                        try:
                            size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                            div = 1 if size.endswith('GB') else 1024
                            size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                            size = '%.2f GB' % size
                        except BaseException:
                            size = '0'
                        for url in link:
                            if hdlr not in url:
                                continue
                            url = url.split('&tr')[0]
                            quality, info = source_utils.get_release_quality(data)
                            if any(x in url for x in ['Tamil', 'FRENCH', 'Ita', 'italian', 'TRUEFRENCH', '-lat-', 'Dublado']):
                                continue
                            info.append(size)
                            info = ' | '.join(info)
                            sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
            except:
                return
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


