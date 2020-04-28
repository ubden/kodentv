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
        self.domains = ['putlockerz.ch']
        self.base_link = 'http://putlockerz.ch'


    def movie(self, imdb, title, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

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

            if url == None: return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

                if 'tvshowtitle' in data:
                    episode = '%01d' % int(data['episode'])

                    u1 = '%s/watch-%s-s%02d-%s-online-free-putlocker.html' % (self.base_link, cleantitle.geturl(title), int(data['season']), str((int(data['year']) + int(data['season'])) - 1))
                    u2 = '%s/watch-%s-s%02d-%s-online-free-putlocker.html' % (self.base_link, cleantitle.geturl(title), int(data['season']), data['year'])
                    u3 = '%s/watch-%s-s%02d-%s-online-free-putlocker.html' % (self.base_link, cleantitle.geturl(title), int(data['season']), str(int(data['year'])+1))

                    r = client.request(u1, output='geturl')
                    if 'error.html' in r: r = client.request(u2, output='geturl')
                    if 'error.html' in r: r = client.request(u3, output='geturl')
                    if 'error.html' in r: raise Exception()
                    url = r
                else:
                    episode = None

                    u1 = '%s/watch-%s-%s-online-free-putlocker.html' % (self.base_link, cleantitle.geturl(title), data['year'])

                    r = client.request(u1, output='geturl')
                    if 'error.html' in r: raise Exception()
                    url = r

            else:
                try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
                except: episode = None
                try: episode = '%01d' % int(data['episode'])
                except: pass

            r = client.request(url)

            h = {'User-Agent': client.agent(), 'X-Requested-With': 'XMLHttpRequest'}

            ip = client.parseDOM(r, 'input', ret='value', attrs = {'name': 'phimid'})[0]
            ep = episode if not episode == None else '1'

            p = {'ip_film': ip, 'ip_name': ep, 'ipplugins': '1', 'ip_server': '11'}
            p = urllib.urlencode(p)

            u = '/ip.file/swf/plugins/ipplugins.php'
            u = urlparse.urljoin(self.base_link, u)

            r = client.request(u, post=p, headers=h, referer=url)
            r = json.loads(r)

            u = '/ip.file/swf/ipplayer/ipplayer.php'
            u = urlparse.urljoin(self.base_link, u)

            p = {'u': r['s'], 's': r['v'], 'w': '100%', 'h': '360', 'n':'0'}
            p = urllib.urlencode(p)

            r = client.request(u, post=p, headers=h, referer=url)
            r = json.loads(r)['data']

            u = [i['files'] for i in r if 'files' in i]

            for i in u:
                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Putlockerz', 'url': i, 'direct': True, 'debridonly': False})
                except: pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


