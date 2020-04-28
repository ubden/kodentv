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


import re,json,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['genvideos.org', 'genvideos.com']
        self.base_link = 'http://genvideos.com'
        self.search_link = '/watch_%s_%s.html'


    def movie(self, imdb, title, year):
        try:
            url = self.search_link % (cleantitle.geturl(title).replace('-', '_'), year)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, limit='2')
            r = client.parseDOM(r, 'meta', ret='content', attrs = {'property': 'og:title'})[0]
            if not year in r: raise Exception()

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            referer = urlparse.urljoin(self.base_link, url)

            h = {'X-Requested-With': 'XMLHttpRequest'}

            try: post = urlparse.parse_qs(urlparse.urlparse(referer).query).values()[0][0]
            except: post = referer.strip('/').split('/')[-1].split('watch_', 1)[-1].rsplit('#')[0].rsplit('.')[0]

            post = urllib.urlencode({'v': post})

            url = urlparse.urljoin(self.base_link, '/video_info/iframe')

            r = client.request(url, post=post, headers=h, referer=url)
            r = json.loads(r).values()
            r = [urllib.unquote(i.split('url=')[-1])  for i in r]

            for i in r:
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Genvideo', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


