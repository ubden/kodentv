# -*- coding: utf-8 -*-
# -Rewrote on 4-14-2020 by Tempest.

"""
    **Created by Tempest**
    Thanks Jewbmx For the fix
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse, traceback
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.sources import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['streamdreams.org']
        self.base_link = 'https://streamdreams.org'
        self.headers = {'User-Agent': client.agent()}

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
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, episode, year):
        try:
            url = '%s/?s=%s' % (self.base_link, title)
            r = cfscrape.get(url, headers=self.headers).content
            r = client.parseDOM(r, 'div', attrs={'class': 'panel-body'})
            for r in r:
                r = re.findall('<a href="(.+?)" title="(.+?)><img .+? alt="(.+?)"', r)
                url = [i for i in r if str(title) in i[1] and str(year) in i[2]][0][0]
                url = '%s?session=%s&episode=%s' % (url, int(season), int(episode))
                return url
        except:
            return

    def searchMovie(self, title):
        try:
            url = '%s/?s=%s' % (self.base_link, title)
            r = cfscrape.get(url, headers=self.headers).content
            r = client.parseDOM(r, 'div', attrs={'class': 'panel-body'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            url = [i for i in r if title in i[1]][0][0]
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostDict + hostprDict
            if url is None:
                return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            if 'tvshowtitle' in data:
                url = self.searchShow(title, int(data['season']), int(data['episode']), int(data['year']))
            else:
                url = self.searchMovie(title)
            r = cfscrape.get(url, headers=self.headers).content
            u = client.parseDOM(r, "span", attrs={"class": "movie_version_link"})
            for t in u:
                match = client.parseDOM(t, 'a', ret='data-href')
                for url in match:
                    if url in str(sources):
                        continue
                    quality, info = source_utils.get_release_quality(url, url)
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Streamdreams Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
