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
        self.domains = ['movie4k.to']
        self.base_link = 'http://movie4k.to'
        self.search_link = '/movies.php?list=search&search=%s'


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)
            y = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1), '0']

            q = self.search_link % urllib.quote_plus(cleantitle.query(title))
            q = urlparse.urljoin(self.base_link, q)

            r = proxy.request(q, 'flag')
            r = client.parseDOM(r, 'TR', attrs = {'id': 'coverPreview.+?'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'), client.parseDOM(i, 'div', attrs = {'style': '.+?'}), client.parseDOM(i, 'img', ret='src')) for i in r]
            r = [(i[0][0].strip(), i[1][0].strip(), i[2], i[3]) for i in r if i[0] and i[1] and i[3]]
            r = [(i[0], i[1], [x for x in i[2] if x.isdigit() and len(x) == 4], i[3]) for i in r]
            r = [(i[0], i[1], i[2][0] if i[2] else '0', i[3]) for i in r]
            r = [i for i in r if any('us_flag_' in x for x in i[3])]
            r = [(i[0], i[1], i[2], [re.findall('(\d+)', x) for x in i[3] if 'smileys' in x]) for i in r]
            r = [(i[0], i[1], i[2], [x[0] for x in i[3] if x]) for i in r]
            r = [(i[0], i[1], i[2], int(i[3][0]) if i[3] else 0) for i in r]
            r = sorted(r, key=lambda x: x[3])[::-1]
            r = [(i[0], i[1], i[2], re.findall('\((.+?)\)$', i[1])) for i in r]
            r = [(i[0], i[1], i[2]) for i in r if not i[3]]
            r = [i for i in r if i[2] in y]

            r = [(proxy.parse(i[0]), i[1], i[2]) for i in r]

            match = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if match: url = match[0] ; break
                    r = proxy.request(urlparse.urljoin(self.base_link, i), 'tablemoviesindex2')
                    r = re.findall('(tt\d+)', r)
                    if imdb in r: url = i ; break
                except:
                    pass

            url = urlparse.urljoin(self.base_link, url)

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = proxy.request(url, 'tablemoviesindex2')
            r = r.replace('\\"', '"')

            links = client.parseDOM(r, 'tr', attrs = {'id': 'tablemoviesindex2'})

            locDict = [(i.rsplit('.', 1)[0], i) for i in hostDict]

            for i in links:
                try:
                    host = client.parseDOM(i, 'img', ret='alt')[0]
                    host = host.split()[0].rsplit('.', 1)[0].strip().lower()
                    host = [x[1] for x in locDict if host == x[0]][0]
                    if not host in hostDict: raise Exception()
                    host = host.encode('utf-8')

                    url = client.parseDOM(i, 'a', ret='href')[0]
                    url = proxy.parse(url)
                    url = urlparse.urljoin(self.base_link, url)
                    url = url.encode('utf-8')

                    sources.append({'source': host, 'quality': 'SD', 'provider': 'Movie4K', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            r = proxy.request(url, 'gotoHosterlistLink2')
            r = r.split('gotoHosterlistLink2')[0].split('<BR>')[-1]

            url = []
            try: url += [client.parseDOM(r, 'a', ret='href')[0]]
            except: pass
            try: url += [client.parseDOM(r, 'iframe', ret='src')[0]]
            except: pass

            url = url[0]
            url = proxy.parse(url)
            url = url.encode('utf-8')

            return url
        except:
            return


