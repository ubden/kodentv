# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 07-19-2018 by JewBMX in Scrubs.

import re
from resources.lib.modules import cleantitle
from resources.lib.modules import getSum, client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['telepisodes.org']
        self.base_link = 'https://www1.telepisodes.org'
        self.tvshow_link = '/tv-series/%s/season-%s/episode-%s/'
        self.headers = {'User-Agent': client.agent()}

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
            tvshowtitle = url
            url = self.base_link + self.tvshow_link % (tvshowtitle, season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict
            page = client.request(url, headers=self.headers)
            match = re.findall('<a class="linkdomx w3-button w3-blue w3-center" rel="nofollow" title="(.+?)" target="_blank" href="(.+?)"', page, flags=re.DOTALL|re.IGNORECASE)
            if match:
                for hoster, url in match:
                    url = self.base_link + url
                    valid, host = source_utils.is_host_valid(hoster, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            page2 = client.request(url, headers=self.headers)
            match2 = re.findall('class="mybutton vidlink button-link" target="_blank" href="/open/site/(.+?)"',page2, flags=re.DOTALL|re.IGNORECASE)
            if match2:
                for link in match2:
                    link = self.base_link + "/open/site/" + link
                    url = getSum.get(link, Type='redirect')
                    return url
        except:
            return
