# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urllib, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import control
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en', 'de', 'fr', 'ko', 'pl', 'pt', 'ru']
        self.domains = ['yts.lt', 'yts.am', 'yts.ag']
        self.base_link = 'https://yts.lt'
        self.search_link = '/browse-movies/%s/all/all/0/latest'
        self.min_seeders = int(control.setting('torrent.min.seeders'))


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            if debrid.status() is False:
                raise Exception()
            if debrid.tor_enabled() is False:
                raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            query = '%s %s' % (data['title'], data['year'])
            url = self.search_link % urllib.quote(query)
            url = urlparse.urljoin(self.base_link, url)
            html = client.request(url)
            try:
                results = client.parseDOM(html, 'div', attrs={'class': 'row'})[2]
            except:
                return sources
            items = re.findall('class="browse-movie-bottom">(.+?)</div>\s</div>', results, re.DOTALL)
            if items is None:
                return sources
            for entry in items:
                try:
                    try:
                        link, name = re.findall('<a href="(.+?)" class="browse-movie-title">(.+?)</a>', entry, re.DOTALL)[0]
                        name = client.replaceHTMLCodes(name)
                        if not cleantitle.get(name) == cleantitle.get(data['title']):
                            continue
                    except:
                        continue
                    y = entry[-4:]
                    if not y == data['year']:
                        continue
                    response = client.request(link)
                    try:
                        entries = client.parseDOM(response, 'div', attrs={'class': 'modal-torrent'})
                        for torrent in entries:
                            link, name = re.findall('href="magnet:(.+?)" class="magnet-download download-torrent magnet" title="(.+?)"', torrent, re.DOTALL)[0]
                            link = 'magnet:%s' % link
                            link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                            if link in str(sources):
                                continue
                            quality, info = source_utils.get_release_quality(name, name)
                            try:
                                size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', torrent)[-1]
                                div = 1 if size.endswith(('GB', 'GiB')) else 1024
                                size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                                size = '%.2f GB' % size
                                info.append(size)
                            except:
                                pass
                            info = ' | '.join(info)
                            sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': True})
                    except:
                        continue
                except:
                    continue
            return sources
        except:
            return sources


    def resolve(self, url):
        return url

