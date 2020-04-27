# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['putlocker.onl']
        self.base_link = 'http://ww.putlocker.onl'
        self.tv_link = '/show/%s/season/%s/episode/%s'
        self.scraper = cfscrape.create_scraper()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = cleantitle.geturl(tvshowtitle)
            url = tvshowtitle
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = url
            url = self.base_link + self.tv_link % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = self.scraper.get(url).content
            match = re.compile('<IFRAME.+?SRC=.+?//(.+?)/(.+?)"').findall(r)
            for host, url in match:
                url = 'http://%s/%s' % (host, url)
                host = host.replace('www.', '')
                valid, host = source_utils.is_host_valid(host, hostDict)
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                if valid:
                    sources.append({ 'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
            return sources
        except Exception:
            return sources


    def resolve(self, url):
        return url


