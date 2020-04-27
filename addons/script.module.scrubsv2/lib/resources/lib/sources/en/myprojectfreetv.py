# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  #  Old  project-free-tv.ag  my-project-free.tv
        self.domains = ['projectfreetv.ag']
        self.base_link = 'http://www1.projectfreetv.ag'
        self.search_link = '/episode/%s-season-%s-episode-%s'
        self.scraper = cfscrape.create_scraper()


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(tvshowtitle)
            url = clean_title
            return url
        except:
            return
 
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = url
            url = self.base_link + self.search_link % (tvshowtitle, int(season), int(episode))
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            r = self.scraper.get(url).content
            data = re.compile("callvalue\('.+?','.+?','(.+?)://(.+?)/(.+?)'\)", re.DOTALL).findall(r)
            for http, host, url in data:
                url = '%s://%s/%s' % (http, host, url)
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                if url in str(sources):
                    continue
                valid, host = source_utils.is_host_valid(host, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


