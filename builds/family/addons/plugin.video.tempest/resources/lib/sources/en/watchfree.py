# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 04-14-2020 by Tempest.

import re
import urllib
import urlparse
import base64

from resources.lib.modules import client, cleantitle, directstream
from resources.lib.modules import dom_parser
from resources.lib.sources import cfscrape


class source:
    def __init__(self):

        self.priority = 1
        self.language = ['en']
        self.domains = ['watchfree.biz']
        self.base_link = 'http://watchfree.biz'
        self.search_link = '/search-movies/%s.html'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title).replace('-', '+')
            url = urlparse.urljoin(self.base_link, (self.search_link % clean_title))
            r = cfscrape.get(url, headers=self.headers).content
            r = dom_parser.parse_dom(r, 'div', {'class': 'item'})
            r = [dom_parser.parse_dom(i, 'a', req=['href']) for i in r if i]
            r = [(i[0].attrs['href'], re.search('Release:\s*(\d+)', i[0].content)) for i in r if i]
            r = [(i[0], i[1].groups()[0]) for i in r if i[0] and i[1]]
            r = [(i[0], i[1]) for i in r if i[1] == year]
            if r[0]:
                url = r[0][0]
                return url
            else:
                return
        except Exception:
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
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['premiered'], url['season'], url['episode'] = premiered, season, episode
            try:
                clean_title = cleantitle.geturl(url['tvshowtitle']) + '-season-%d' % int(season)
                search_url = urlparse.urljoin(self.base_link, self.search_link % clean_title.replace('-', '+'))
                r = cfscrape.get(search_url, headers=self.headers).content
                r = client.parseDOM(r, 'div', {'class': 'item'})
                r = [(client.parseDOM(i, 'a', ret='href'),
                      re.findall('<b><i>(.+?)</i>', i)) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if
                     cleantitle.get(i[1][0]) == cleantitle.get(clean_title)]
                url = r[0][0]
            except:
                pass
            data = cfscrape.get(url, headers=self.headers).content
            data = client.parseDOM(data, 'div', attrs={'id': 'details'})
            data = zip(client.parseDOM(data, 'a'), client.parseDOM(data, 'a', ret='href'))
            url = [(i[0], i[1]) for i in data if i[0] == str(int(episode))]

            return url[0][1]
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = cfscrape.get(url, headers=self.headers).content
            try:
                v = re.findall('document.write\(Base64.decode\("(.+?)"\)', r)[0]
                b64 = base64.b64decode(v)
                url = client.parseDOM(b64, 'iframe', ret='src')[0]
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url.replace('\/', '/'), 'direct': False, 'debridonly': False})
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
                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url.replace('\/', '/'), 'direct': False, 'debridonly': False})
                    except:
                        pass
            return sources
        except Exception:
            return sources

    def resolve(self, url):
        if self.base_link in url:
            url = cfscrape.get(url, headers=self.headers).content
            v = re.findall('document.write\(Base64.decode\("(.+?)"\)', url)[0]
            b64 = base64.b64decode(v)
            url = client.parseDOM(b64, 'iframe', ret='src')[0]
        return url