# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

from resources.lib.modules import cleantitle
from resources.lib.modules import getSum
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watchseries4k.com']
        self.base_link = 'https://www.watchseries4k.com'
        self.tvshow_link = '/%s/season_%s/episode_%s/'


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
            if url == None:
                return sources
            hostDict = hostprDict + hostDict
            page = getSum.get(url)
            match = getSum.findEm(page, 'rel="nofollow" target="_blank" href="(.+?)">(.+?)</a>')
            for url, hoster in match:
                if 'font14' in hoster:
                    continue
                url = self.base_link + url
                valid, host = source_utils.is_host_valid(hoster, hostDict)
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            get = getSum.get(url)
            url = getSum.findEm(get, '<a target="_blank" href="(.+?)"')[0]
            url = self.base_link + url
            url = getSum.get(url, Type='redirect')
            return url
        except:
            return url


