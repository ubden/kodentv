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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['miradetodo.net']
        self.base_link = 'http://miradetodo.net'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, year):
        try:
            t = 'http://www.imdb.com/title/%s' % imdb
            t = client.request(t, headers={'Accept-Language':'ar-AR'})
            t = client.parseDOM(t, 'title')[0]
            t = re.sub('(?:\(|\s)\d{4}.+', '', t).strip()

            q = self.search_link % urllib.quote_plus(t)
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q)

            r = client.parseDOM(r, 'div', attrs = {'class': 'item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'class': 'tt'}), client.parseDOM(i, 'span', attrs = {'class': 'year'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [i[0] for i in r if cleantitle.get(t) == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            r = urlparse.urljoin(self.base_link, url)

            result = client.request(r)

            f = client.parseDOM(result, 'div', attrs = {'class': 'movieplay'})
            f = [re.findall('(?:\"|\')(http.+?miradetodo\..+?)(?:\"|\')', i) for i in f]
            f = [i[0] for i in f if len(i) > 0]


            dupes = []

            for u in f:
                try:
                    sid = urlparse.parse_qs(urlparse.urlparse(u).query)['id'][0]

                    if sid in dupes: raise Exception()
                    dupes.append(sid)

                    headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': u}

                    url = client.request(u, timeout='10', headers=headers)
                    url = client.parseDOM(url, 'a', ret='href')
                    url = [i for i in url if '.php' in i][0]
                    url = 'http:' + url if url.startswith('//') else url
                    url = client.request(url, timeout='10', headers=headers, referer=u)

                    url = re.findall('file\s*:\s*"(.+?)"', url)

                    for i in url:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'MiraDeTodo', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


