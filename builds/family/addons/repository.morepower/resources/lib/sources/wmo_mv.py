# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

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


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['watchmovies-online.is', 'watchmovies.nz']
        self.base_link = 'http://watchmovies-online.is'

    def movie(self, imdb, title, year):
        try:
            url = '/%s-%s/' % (cleantitle.geturl(title), year)
            url = urlparse.urljoin(self.base_link, url)

            url = proxy.geturl(url)
            if url == None: raise Exception()

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = proxy.request(url, 'episode-meta')

            meta = client.parseDOM(r, 'div', attrs = {'class': 'wp-episode-meta'})[0]
            meta = urllib.unquote_plus(meta)

            if 'genre/coming-soon' in meta: raise Exception() 

            quality = client.parseDOM(meta, 'li')
            quality = [re.sub('<.+?>|</.+?>', '', i) for i in quality]
            quality = [i.split(':')[-1].strip().upper() for i in quality if 'quality' in i.lower()]
            quality = quality[0] if quality else 'SD'

            if 'CAM' in quality or 'TS' in quality: quality = 'CAM'
            elif quality == 'SCREENER': quality = 'SCR'
            else: quality = 'SD'

            links = client.parseDOM(r, 'a', ret='href', attrs = {'target': '.+?'})
            links = [x for y,x in enumerate(links) if x not in links[:y]]

            for i in links:
                try:
                    url = i
                    url = proxy.parse(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'provider': 'WMO', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url


