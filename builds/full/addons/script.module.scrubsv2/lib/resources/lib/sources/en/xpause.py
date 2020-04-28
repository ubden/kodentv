# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['xpau.se', 'topnow.se']
        self.base_link = 'http://xpau.se'
        self.base2_link = 'http://topnow.se'
        self.search_link = '/watch/%s'
        self.search2_link = '/%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = cleantitle.geturl(title)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            if debrid.status() is False:
                raise Exception()
            if debrid.tor_enabled() is False:
                raise Exception()
            try:
                s_url = self.base_link + self.search_link % (url + '666')
                html = client.request(s_url)
                links = re.findall('href="(magnet:.+?)"', html, re.DOTALL)
            except:
                s_url = self.base2_link + self.search2_link % url
                html = client.request(s_url)
                links = re.findall('href="(magnet:.+?)"', html, re.DOTALL)
            for link in links:
                link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                quality, info = source_utils.get_release_quality(link, link)
                try:
                    size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', html)[-1]
                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                    size = '%.2f GB' % size
                    info.append(size)
                except:
                    pass
                info = ' | '.join(info)
                sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': True})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


