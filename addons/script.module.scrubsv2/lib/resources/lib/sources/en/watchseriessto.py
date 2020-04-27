# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# Dupe of wsunblock. only real difference is search vs build.

import re, base64
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watchseriess.to']
        self.base_link = 'https://ww1.watchseriess.to'
        self.search_link = '/search/%s'
        self.show_link = '_s%s_e%s.html'
        self.scraper = cfscrape.create_scraper()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowTitle = cleantitle.geturl(tvshowtitle).replace(':', ' ').replace(' ', '+')
            url = self.base_link + self.search_link % tvshowTitle
            searchPage = self.scraper.get(url).content
            results = re.compile('<div valign="top" style="padding-left: 10px;">.+?<a href="(.+?)" title=".+?" target="_blank"><strong>(.+?)</strong></a>', re.DOTALL).findall(searchPage)
            for url, checkit in results:
                zcheck = '%s (%s)' % (tvshowtitle, year)
                if zcheck.lower() in checkit.lower():
                    url = url.replace('/serie/', '/episode/')
                    return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None:
                return
            url = self.base_link + url + self.show_link % (season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = self.scraper.get(url).content
            match = re.compile('cale\.html\?r=(.+?)" class="watchlink" title="(.+?)"').findall(r)
            for url, host in match:
                url  = base64.b64decode(url)
                valid, host = source_utils.is_host_valid(host, hostDict)
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                if valid:
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False}) 
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


