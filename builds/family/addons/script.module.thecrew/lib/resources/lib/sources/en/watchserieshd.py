# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, requests
from resources.lib.modules import cleantitle
from resources.lib.modules import directstream
from resources.lib.modules import getSum
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  # watchserieshd.co got changed to a different source 
        self.domains = ['watchserieshd.cc']  # Old  watchserieshd.io
        self.base_link = 'http://www1.watchserieshd.tv'
        self.search_link = '/series/%s-season-%s-episode-%s'

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
            if url is None:
                return sources
            sources = []
            hostDict = hostprDict + hostDict
            r = getSum.get(url)
            match = getSum.findSum(r)
            for url in match:
                if 'vidcloud' in url:
                    result = getSum.get(url)
                    match = getSum.findSum(result)
                    for link in match:
                        link = "https:" + link if not link.startswith('http') else link
                        link = requests.get(link).url if 'vidnode' in link else link
                        valid, host = source_utils.is_host_valid(link, hostDict)
                        if valid:
                            quality, info = source_utils.get_release_quality(link, link)
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False, 'debridonly': False})
                else:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        if "google" in url:
            return directstream.googlepass(url)
        elif 'vidcloud' in url:
            r = getSum.get(url)
            url = re.findall("file: '(.+?)'", r)[0]
            return url
        else:
            return url
