# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['cooltvseries.com']
        self.base_link = 'https://cooltvseries.com'
        self.search_link = '/%s/season-%s/'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            http = self.base_link + self.search_link % (url, season)
            season = '%02d' % int(season)
            episode = '%02d' % int(episode)
            r = client.request(http)
            match = re.compile('<a href="(.+?)-S' + season + 'E' + episode + '-(.+?)">').findall(r)
            for url1, url2 in match:
                url = '%s-S%sE%s-%s' % (url1, season, episode, url2)
                return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = client.request(url)
            match = re.compile('<li><a href="(.+?)" rel="nofollow">(.+?)<').findall(r)
            for url, check in match:
                quality, info = source_utils.get_release_quality(check, check)
                sources.append({ 'source': 'Direct', 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': True, 'debridonly': False }) 
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


