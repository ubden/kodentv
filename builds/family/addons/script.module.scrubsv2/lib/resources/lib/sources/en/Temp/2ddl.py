# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# Created by Tempest

import re, urllib, urlparse
from resources.lib.modules import cfscrape
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
import traceback
from resources.lib.modules import log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  #  Old  invictus.ws
        self.domains = ['twoddl.net', '2ddl.vg']
        self.base_link = 'https://2ddl.vg'
        self.search_link = '/?s=%s'
        self.scraper = cfscrape.create_scraper()


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
            if url == None:
                return
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
            if url == None:
                return sources
            if debrid.status() is False:
                raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).replace('-', '+')
            r = self.scraper.get(url).content
            if r == None and 'tvshowtitle' in data:
                season = re.search('S(.*?)E', hdlr)
                season = season.group(1)
                url = title
                r = self.scraper.get(url).content
            for loopCount in range(0,2):
                if loopCount == 1 or (r == None and 'tvshowtitle' in data):
                    r = self.scraper.get(url).content
                posts = client.parseDOM(r, "div", attrs={"class": "postpage_movie_download"})
                hostDict = hostprDict + hostDict
                items = []
                for post in posts:
                    try:
                        u = client.parseDOM(post, 'a', ret='href')
                        for i in u:
                            name = str(i)
                            items.append(name)
                    except:
                        pass
                if len(items) > 0:
                    break
            for item in items:
                try:
                    i = str(item)
                    r = self.scraper.get(i).content
                    u = client.parseDOM(r, "div", attrs={"class": "multilink_lnks"})
                    for t in u:
                        r = client.parseDOM(t, 'a', ret='href')
                        for url in r:
                            if 'www.share-online.biz' in url:
                                continue
                            if url in str(sources):
                                continue
                            quality, info = source_utils.get_release_quality(url, url)
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if valid:
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                except:
                    pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---2ddl - Exception: \n' + str(failure))
            return sources


    def resolve(self, url):
        return url


