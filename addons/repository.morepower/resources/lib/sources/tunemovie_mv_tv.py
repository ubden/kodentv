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


import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['tunemovies.to', 'tunemovie.tv']
        self.base_link = 'http://tunemovies.to'
        self.search_link = '/search/%s.html'


    def movie(self, imdb, title, year):
        try:
            query = urlparse.urljoin(self.base_link, self.search_link)
            query = query % urllib.quote_plus(title)

            t = cleantitle.get(title)

            r = client.request(query)

            r = client.parseDOM(r, 'div', attrs = {'id': 'post-\d+'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), re.findall('(\d{4})', i)) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]

            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
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
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = '%s/watch/%s-season-%01d-%s.html' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(season), str((int(data['year']) + int(season)) - 1))
            url = client.request(url, output='geturl')
            if url == None: raise Exception()

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url += '?episode=%01d' % int(episode)
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

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            headers = {'X-Requested-With': 'XMLHttpRequest', 'Referer': url}

            for i in range(3):
                result = client.request(url)
                if not result == None: break

            if not episode == None:
                mid = client.parseDOM(result, 'input', ret='value', attrs = {'name': 'phimid'})[0]
                url = urlparse.urljoin(self.base_link, '/ajax.php')
                post = {'ipos_server': 1, 'phimid': mid, 'keyurl': episode}
                post = urllib.urlencode(post)

                for i in range(3):
                    result = client.request(url, post=post, headers=headers, timeout='10')
                    if not result == None: break

            r = client.parseDOM(result, 'div', attrs = {'class': '[^"]*server_line[^"]*'})

            links = []

            for u in r:
                try:
                    host = client.parseDOM(u, 'p', attrs = {'class': 'server_servername'})[0]
                    host = host.strip().lower().split(' ')[-1]

                    url = urlparse.urljoin(self.base_link, '/ip.temp/swf/plugins/ipplugins.php')

                    p1 = client.parseDOM(u, 'a', ret='data-film')[0]
                    p2 = client.parseDOM(u, 'a', ret='data-server')[0]
                    p3 = client.parseDOM(u, 'a', ret='data-name')[0]
                    post = {'ipplugins': 1, 'ip_film': p1, 'ip_server': p2, 'ip_name': p3}
                    post = urllib.urlencode(post)

                    if not host in ['google', 'putlocker', 'megashare']: raise Exception()

                    for i in range(3):
                        result = client.request(url, post=post, headers=headers, timeout='10')
                        if not result == None: break

                    result = json.loads(result)['s']

                    url = urlparse.urljoin(self.base_link, '/ip.temp/swf/ipplayer/ipplayer.php')

                    post = {'u': result, 'w': '100%', 'h': '420'}
                    post = urllib.urlencode(post)

                    for i in range(3):
                        result = client.request(url, post=post, headers=headers)
                        if not result == None: break

                    url = json.loads(result)['data']

                    if type(url) is list:
                        url = [i['files'] for i in url]
                        for i in url:
                            try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Tunemovie', 'url': i, 'direct': True, 'debridonly': False})
                            except: pass

                    else:
                        url = client.request(url)
                        url = client.parseDOM(url, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
                        url += '|%s' % urllib.urlencode({'User-agent': client.randomagent()})
                        sources.append({'source': 'cdn', 'quality': 'HD', 'provider': 'Tunemovie', 'url': url, 'direct': False, 'debridonly': False})

                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


