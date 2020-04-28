# -*- coding: utf-8 -*-

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['topnow.se']
        self.base_link = 'http://topnow.se'
        self.search_link = '/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.geturl(title)
            url = self.base_link + self.search_link % mtitle
            print url
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
            html = client.request(url)
            link = re.findall('href="(magnet:.+?)"', html, re.DOTALL)
            for link in link:
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
