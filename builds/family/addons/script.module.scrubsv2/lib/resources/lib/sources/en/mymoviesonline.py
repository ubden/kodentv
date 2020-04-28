# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urlparse, urllib, base64
from resources.lib.modules import cfscrape
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviesonline.mn', 'moviesonline.la', 'moviesonline.fm', 'moviesonline.mx']
        self.base_link = 'http://moviesonline.mn'
        self.movies_search_path = ('/search-movies/%s.html')
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title).replace('-', '+')
            url = urlparse.urljoin(self.base_link, (self.movies_search_path % clean_title))
            r = self.scraper.get(url).content
            r = dom_parser.parse_dom(r, 'div', {'id': 'movie-featured'})
            r = [dom_parser.parse_dom(i, 'a', req=['href']) for i in r if i]
            r = [(i[0].attrs['href'], re.search('Release:\s*(\d+)', i[0].content)) for i in r if i]
            r = [(i[0], i[1].groups()[0]) for i in r if i[0] and i[1]]
            r = [(i[0], i[1]) for i in r if i[1] == year]
            if r[0]: 
                url = r[0][0]
                return url
            else:
                return
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
            if url == None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['premiered'], url['season'], url['episode'] = premiered, season, episode
            try:
                clean_title = cleantitle.geturl(url['tvshowtitle']) + '-season-%d' % int(season)
                search_url = urlparse.urljoin(self.base_link, self.search_link % clean_title.replace('-', '+'))
                r = self.scraper.get(search_url).content
                r = client.parseDOM(r, 'div', {'id': 'movie-featured'})
                r = [(client.parseDOM(i, 'a', ret='href'), re.findall('<b><i>(.+?)</i>', i)) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if cleantitle.get(i[1][0]) == cleantitle.get(clean_title)]
                url = r[0][0]
            except:
                pass
            data = self.scraper.get(url).content
            data = client.parseDOM(data, 'div', attrs={'id': 'details'})
            data = zip(client.parseDOM(data, 'a'), client.parseDOM(data, 'a', ret='href'))
            url = [(i[0], i[1]) for i in data if i[0] == str(int(episode))]
            return url[0][1]
        except:
            return



    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostDict + hostprDict
            if url == None:
                return sources
            r = self.scraper.get(url).content
            r = dom_parser.parse_dom(r, 'p', {'class': 'server_play'})
            r = [dom_parser.parse_dom(i, 'a', req=['href']) for i in r if i]
            r = [(i[0].attrs['href'], re.search('/(\w+).html', i[0].attrs['href'])) for i in r if i]
            r = [(i[0], i[1].groups()[0]) for i in r if i[0] and i[1]]
            for i in r:
                try:
                    host = i[1]
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if source_utils.limit_hosts() is True and host in str(sources):
                        continue
                    if valid:
                        sources.append({ 'source': host, 'quality': 'SD', 'language': 'en', 'url': i[0].replace('\/', '/'), 'direct': False, 'debridonly': False })
                except:
                    pass
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            r = self.scraper.get(url).content
            url = re.findall('document.write.+?"([^"]*)', r)[0]
            url = base64.b64decode(url)
            url = re.findall('src="([^"]*)', url)[0]
            return url
        except:
            return url


