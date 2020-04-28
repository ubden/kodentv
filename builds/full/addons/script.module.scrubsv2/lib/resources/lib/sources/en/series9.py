# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, requests, urllib, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import directstream
from resources.lib.modules import getSum
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  # Removed  seriesonline.io  series9.co  series9.io
        self.domains = ['series9.to']
        self.base_link = 'https://www5.series9.to'
        self.search_link = '/movie/search/%s'


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
            if url == None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return  


    def searchShow(self, title, season, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            search = '%s Season %01d' % (title, int(season))
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(search))
            r = client.request(url, headers=headers, timeout='10')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            r = [(i[0], i[1], re.findall('(.*?)\s+-\s+Season\s+(\d)', i[1])) for i in r]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
            url = [i[0] for i in r if self.matchAlias(i[2][0], aliases) and i[2][1] == season][0]
            url = urlparse.urljoin(self.base_link, '%s/watching.html' % url)
            return url
        except:
            return  


    def searchMovie(self, title, year, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.search_link % cleantitle.geturl(title))
            r = client.request(url, headers=headers, timeout='10')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='oldtitle'))
            results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
            try:
                r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                url = [i[0] for i in r if self.matchAlias(i[1], aliases) and (year == i[2])][0]
            except:
                url = None
                pass
            if (url == None):
                url = [i[0] for i in results if self.matchAlias(i[1], aliases)][0]
            url = urlparse.urljoin(self.base_link, '%s/watching.html' % url)
            return url
        except:
            return  


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostDict + hostprDict
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            headers = {}
            if 'tvshowtitle' in data:
                ep = data['episode']
                url = '%s/film/%s-season-%01d/watching.html?ep=%s' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']), ep)
                r = client.request(url, headers=headers, timeout='10', output='geturl')
                if url == None:
                    url = self.searchShow(data['tvshowtitle'], data['season'], aliases, headers)
            else:
                url = self.searchMovie(data['title'], data['year'], aliases, headers)
                if url == None:
                    url = '%s/film/%s/watching.html?ep=0' % (self.base_link, cleantitle.geturl(data['title']))
            if url == None:
                raise Exception()
            r = client.request(url, headers=headers, timeout='10')
            r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})
            if 'tvshowtitle' in data:
                ep = data['episode']
                links = client.parseDOM(r, 'a', attrs={'episode-data': ep}, ret='player-data')
            else:
                links = client.parseDOM(r, 'a', ret='player-data')
            for link in links:
                link = "https:" + link if not link.startswith('http') else link
                if 'vidcloud' in link:
                    r = client.request(link, headers=headers, timeout='10')
                    match = getSum.findSum(r)
                    for url in match:
                        url = "https:" + url if not url.startswith('http') else url
                        url = requests.get(url).url if 'api.vidnode' in url else url
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            quality, info = source_utils.get_release_quality(url, url)
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
                elif '123movieshd' in link or 'seriesonline' in link:
                    r = client.request(link, headers=headers, timeout='10')
                    r = re.findall('(https:.*?redirector.*?)[\'\"]', r)
                    for i in r:
                        sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                else:
                    valid, host = source_utils.is_host_valid(link, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(link, link)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        elif 'vidcloud' in url:
            r = client.request(url)
            url = re.findall("file: '(.+?)'", r)[0]
            return url
        else:
            return url


