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


import re,urllib,urlparse,hashlib,string,time,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.language = ['en']
        self.domains = ['yesmovies.to']
        self.base_link = 'http://yesmovies.to'
        self.info_link = '/ajax/movie_info/%s.html'
        self.episode_link = '/ajax/v3_movie_get_episodes/%s/%s/%s/%s.html'
        self.playlist_link = '/ajax/v2_get_sources/%s.html?hash=%s'
        self.key1 = base64.b64decode('eHdoMzhpZjM5dWN4')
        self.key2 = base64.b64decode('OHFoZm05b3lxMXV4')
        self.key = base64.b64decode('Y3RpdzR6bHJuMDl0YXU3a3F2YzE1M3Vv')


    def movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            q = '/search/%s.html' % (urllib.quote_plus(cleantitle.query(title)))
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q)
            r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
            r = [i[0] for i in r if t == cleantitle.get(i[1])][:2]
            r = [(i, re.findall('(\d+)', i)[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.ymovies_info, 9000, i[1])
                    if not y == year: raise Exception()
                    return urlparse.urlparse(i[0]).path
                except:
                    pass
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

            t = cleantitle.get(data['tvshowtitle'])
            title = data['tvshowtitle']
            season = '%01d' % int(season) ; episode = '%01d' % int(episode)
            year = re.findall('(\d{4})', premiered)[0]
            years = [str(year), str(int(year)+1), str(int(year)-1)]

            r = cache.get(self.ymovies_info_season, 720, title, season)
            r = [(i[0], re.findall('(.+?)\s+(?:-|)\s+season\s+(\d+)$', i[1].lower())) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if i[1]]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and season == '%01d' % int(i[2])][:2]
            r = [(i, re.findall('(\d+)', i)[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.ymovies_info, 9000, i[1])
                    if not y == year: raise Exception()
                    return urlparse.urlparse(i[0]).path + '?episode=%01d' % int(episode)
                except:
                    pass
        except:
            return


    def ymovies_info_season(self, title, season):
        try:
            q = '%s Season %s' % (cleantitle.query(title), season)
            q = '/search/%s.html' % (urllib.quote_plus(q))
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q)
            r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]

            return r
        except:
            return


    def ymovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            u = client.request(u % url)

            q = client.parseDOM(u, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            url = urlparse.urljoin(self.base_link, url)

            vid_id = re.findall('-(\d+)', url)[-1]

            '''
            quality = cache.get(self.ymovies_info, 9000, vid_id)[1].lower()
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd': quality = 'HD'
            else: quality = 'SD'
            '''

            r = client.request(url)

            ref = client.parseDOM(r, 'a', ret='href', attrs = {'class': 'mod-btn mod-btn-watch'})[0]
            ref = urlparse.urljoin(self.base_link, ref)

            r = client.request(ref, referer=url)

            h = {'X-Requested-With': 'XMLHttpRequest'}

            server = re.findall('server\s*:\s*"(.+?)"', r)[0]

            type = re.findall('type\s*:\s*"(.+?)"', r)[0]

            episode_id = re.findall('episode_id\s*:\s*"(.+?)"', r)[0]

            r = self.episode_link % (vid_id, server, episode_id, type)
            r = urlparse.urljoin(self.base_link, r)

            r = client.request(r, headers=h, referer=ref)
            r = re.compile('(<li.+?/li>)', re.DOTALL).findall(r)
            r = [(client.parseDOM(i, 'li', ret='onclick'), client.parseDOM(i, 'a', ret='title')) for i in r]

            if not episode == None:
                r = [(i[0][0], i[1][0]) for i in r if i[0] and i[1]]
                r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]
                r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
            else:
                r = [i[0][0] for i in r if i[0]]

            r = [re.findall('(\d+)', i) for i in r]
            r = [i[:2] for i in r if len(i) > 1]
            r = [i[0] for i in r if 1 <= int(i[1]) <= 11][:3]

            for u in r:
                try:
                    t = self.__get_token(hash_len=6)
                    c = '%s%s%s=%s' % (self.key1, u, self.key2, t)
                    h = {'X-Requested-With':'XMLHttpRequest'}

                    p = urllib.quote(self.__uncensored(u + self.key, t))
                    p = self.playlist_link % (u, p)
                    p = urlparse.urljoin(self.base_link, p)

                    u = client.request(p, headers=h, referer=ref, cookie=c, timeout='10')
                    u = json.loads(u)['playlist'][0]['sources']
                    u = [i['file'] for i in u if 'file' in i]

                    for i in u:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Ymovies', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


    def __get_token(self, hash_len=16):
        chars = string.digits + string.ascii_uppercase + string.ascii_lowercase
        base = hashlib.sha512(str(int(time.time()) / 60 / 60)).digest()
        return ''.join([chars[int(ord(c) % len(chars))] for c in base[:hash_len]])

    def __uncensored(self, a, b):
        c = ''
        i = 0
        for i, d in enumerate(a):
            e = b[i % len(b) - 1]
            d = int(self.__jav(d) + self.__jav(e))
            c += chr(d)
    
        return base64.b64encode(c)
    
    def __jav(self, a):
        b = str(a)
        code = ord(b[0])
        if 0xD800 <= code and code <= 0xDBFF:
            c = code
            if len(b) == 1:
                return code
            d = ord(b[1])
            return ((c - 0xD800) * 0x400) + (d - 0xDC00) + 0x10000
    
        if 0xDC00 <= code and code <= 0xDFFF:
            return code
        return code


