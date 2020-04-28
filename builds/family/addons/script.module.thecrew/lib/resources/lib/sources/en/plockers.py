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

import re, urlparse, urllib, base64

from resources.lib.modules import client, cleantitle
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www1.putlockers.fm']
        self.base_link = 'http://www7.putlockers.fm/'
        self.search_link = 'search-movies/%s.html'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
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
            if url is None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []   
            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s season %d' % (title, int(data['season'])) if 'tvshowtitle' in data else data['title']
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            query = urllib.quote_plus(query)

            url = urlparse.urljoin(self.base_link, self.search_link % query)

            self.s = cfscrape.create_scraper()

            self.ua = {'User-Agent': client.agent(),
                       'Referer': self.base_link}
            r = self.s.get(url, headers=self.ua).text
            posts = client.parseDOM(r, 'div', attrs={'class': 'item'})
            posts = [(client.parseDOM(i, 'a', ret='href')[1],
                      client.parseDOM(i, 'a')[1]) for i in posts if i]

            posts = [(i[0], client.parseDOM(i[1], 'i')[0]) for i in posts if i]

            if 'tvshowtitle' in data:
                sep = 'season %d' % int(data['season'])
                sepi = 'season-%1d/episode-%1d.html' % (int(data['season']), int(data['episode']))
                post = [i[0] for i in posts if sep in i[1].lower()][0]
                data = self.s.get(post, headers=self.ua).content
                link = client.parseDOM(data, 'a', ret='href')
                link = [i for i in link if sepi in i][0]
            else:
                link = [i[0] for i in posts if cleantitle.get(i[1]) == cleantitle.get(title) and hdlr in i[1]][0]

            r = self.s.get(link, headers=self.ua).content
            try:
                v = re.findall('document.write\(Base64.decode\("(.+?)"\)', r)[0]
                b64 = base64.b64decode(v)
                url = client.parseDOM(b64, 'iframe', ret='src')[0]
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    sources.append({
                        'source': host,
                        'quality': 'SD',
                        'language': 'en',
                        'url': url.replace('\/', '/'),
                        'direct': False,
                        'debridonly': False
                    })
                except:
                    pass
            except:
                pass
            r = client.parseDOM(r, 'div', {'class': 'server_line'})
            r = [(client.parseDOM(i, 'a', ret='href')[0],
                  client.parseDOM(i, 'p', attrs={'class': 'server_servername'})[0]) for i in r]
            if r:
                for i in r:
                    try:
                        host = re.sub('Server|Link\s*\d+', '', i[1]).lower()
                        url = i[0]
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        if 'other' in host: continue
                        sources.append({
                            'source': host,
                            'quality': 'SD',
                            'language': 'en',
                            'url': url.replace('\/', '/'),
                            'direct': False,
                            'debridonly': False
                        })
                    except:
                        pass
            return sources
        except:
            return

    def resolve(self, url):
        if 'putlockers' in url:
            try:
                r = self.s.get(url, headers=self.ua).text
                v = re.findall('document.write\(Base64.decode\("(.+?)"\)', r)[0]
                b64 = v.decode('base64')
                url = client.parseDOM(b64, 'iframe', ret='src')[0]
            except:
                r = self.s.get(url, headers=self.ua)
                r = client.parseDOM(r, 'div', attrs={'class': 'player'})
                url = client.parseDOM(r, 'a', ret='href')[0]

            return url
        else:
            return url