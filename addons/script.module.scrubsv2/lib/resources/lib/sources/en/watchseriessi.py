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
        self.domains = ['watchseries.fi', 'watchseries.si']
        self.base_link = 'http://watchseries.si'
        self.search_link = '/series/%s/season/%s/episode/%s/'


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
            url = self.base_link + self.search_link % (url, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = client.request(url)
            match = re.compile('href="(.+?)" rel="noindex\,nofollow">Watch This Link</a>').findall(r)
            for url in match:
                r = client.request(url)
                match = re.compile('<a href="(.+?)://(.+?)/(.+?)"><button class="wpb\_button  wpb\_btn\-primary wpb\_regularsize"> Click Here To Play</button> </a>').findall(r)
                for http, host, url in match:
                    url = '%s://%s/%s' % (http, host, url)
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False}) 
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


