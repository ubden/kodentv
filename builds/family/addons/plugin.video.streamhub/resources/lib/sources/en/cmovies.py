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


import re,urllib,urlparse,json,base64,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream
from resources.lib.modules import source_utils
from resources.lib.modules import jsunpack

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cmovieshd.is']
        self.base_link = 'http://www.cmovieshd.is/'
        self.search_link = '?c=movie&m=filter&keyword=%s&per_page=%s'

    def matchAlias(self, title, aliases):
        try:
            for alias in aliases:
                if cleantitle.get(title) == cleantitle.get(alias['title']):
                    return True
        except:
            return False

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
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

    def sources(self, url, hostDict, locDict):
        sources = []

        try:
            if url == None: return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']            
            for p in {'','10','20','30','40','50'}:
                query = self.search_link % (urllib.quote_plus(title), p)
                query = urlparse.urljoin(self.base_link, query)          
                result = client.request(query)
                r = zip(client.parseDOM(result, 'a', ret='href', attrs={'class':'clip-link'}), client.parseDOM(result, 'a', ret='title', attrs={'class':'clip-link'}))
                try:
                    if 'episode' in data:            
                        r = [i for i in r if cleantitle.get(title+'season%s'%data['season']) == cleantitle.get(i[1])][0][0]
                    else:
                        r = [i for i in r if cleantitle.get(title) == cleantitle.get(i[1]) and data['year'] in i[1]][0][0]

                    break
                except:
                    if p == '50': raise Exception
                    else: pass
                
            
            url = r if 'http' in r else urlparseF.urljoin(self.base_link, r)
            result = client.request(url)    
            url = re.findall(u'<iframe.*?src="([^"]+)', result)[0]
            id = re.compile('id=(\d+)').findall(url)[0]
                      
            if 'episode' in data:
                post = {'id': id, 'e': data['episode'], 'lang': '3', 'cat': 'episode'}          
                                  
            else:
                post = {'id': id, 'e': '', 'lang': '3', 'cat': 'movie'}                

            url = "%s://%s/embed/movieStreams?"%(urlparse.urlsplit(url)[0],urlparse.urlsplit(url)[1]) + urllib.urlencode(post) 
            result = client.request(url, post={})
            links = re.findall(r'show_player\(.*?,.*?"([^"\\]+)',result)

            sources = []
            i = 0
            for url in links:
                if i == 10: break
                try:
                    if 'google' in url:
                        valid, hoster = source_utils.is_host_valid(url, hostDict)
                        urls, host, direct = source_utils.check_directstreams(url, hoster)
                        for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})
             
                    else:
                        valid, hoster = source_utils.is_host_valid(url, hostDict)
                        sources.append({'source': hoster, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                    i+=1

                except:
                    pass

            return sources
        except Exception as e:
            return sources

    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url
