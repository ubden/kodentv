# -*- coding: utf-8 -*-

'''
    Covenant Add-on

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
from resources.lib.modules import debrid
from resources.lib.modules import control

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['allrls.me']
        self.base_link = 'http://allrls.me'
        self.search_link = '/search/%s/feed/rss2'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
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

            if debrid.status() == False: raise Exception()
      
            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            #web_pdb.set_trace()
            posts = []

            query = title
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            query = query.replace("&", "")
            
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            
            query = query + ' ' + hdlr
                  
            referer = self.search_link % urllib.quote_plus(query)
            referer = urlparse.urljoin(self.base_link, referer)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            
            r = client.request(url)

            posts = client.parseDOM(r, "item")
           
            urls = []
            for post in posts:
                try:

                    name = re.search('<title>(.*?)</title>', post)
                    name = name.group(1)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)

                    if not cleantitle.get(t) in cleantitle.get(title): raise Exception()

                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()

                    if not y == hdlr: raise Exception()
                    
                    urls = client.parseDOM(post, 'a', ret = 'href')
                    
                    if '720p' in name: quality = 'HD'
                    elif '1080p' in name: quality = '1080p'
                    else: quality = 'SD'
                    
                    for url in urls:
                        try:

                            host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                            if not host in hostDict: raise Exception()
                            
                            if any(x in url for x in ['.rar', '.zip', '.iso']): raise Exception()
                            
                            info = []
                            
                            if any(x in url.upper() for x in ['HEVC', 'X265', 'H265']): info.append('HEVC')
                            
                            info.append('ALLRLS')
                            
                            info = ' | '.join(info)
                            
                            host = client.replaceHTMLCodes(host)
                            host = host.encode('utf-8')

                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                             
                        except:
                            pass

                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url


