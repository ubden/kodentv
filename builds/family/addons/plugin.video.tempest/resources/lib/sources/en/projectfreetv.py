# -*- coding: utf-8 -*-
# -Cleaned and Checked on 04-14-2020 by Tempest.

import re
from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['my-project-free.tv', 'project-free-tv.ag']
        self.base_link = 'http://www1.projectfreetv.ag'
        self.search_link = '/episode/%s-season-%s-episode-%s'
        self.headers = {'User-Agent': client.agent()}

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
            r = client.request(url, headers=self.headers)
            try:
                data = re.compile("callvalue\('.+?','.+?','(.+?)://(.+?)/(.+?)'\)").findall(r)
                for http, host, url in data:
                    url = '%s://%s/%s' % (http, host, url)
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            except:
                pass
            return sources
        except Exception:
            return sources

    def resolve(self, url):
        return url