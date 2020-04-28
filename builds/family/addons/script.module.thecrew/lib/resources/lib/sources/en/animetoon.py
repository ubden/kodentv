# -*- coding: utf-8 -*-

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import directstream
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animetoon.org']
        self.base_link = 'http://animetoon.org'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = '%s %s' % (title,year)
            return url
        except:
            return
			
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return
 
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            if season == '1': 
                url = self.base_link + '/' + url + '-episode-' + episode
            else:
                url = self.base_link + '/' + url + '-season-' + season + '-episode-' + episode
            return url
        except:
            return

# videozoome
# playbbme
# easyvideo
# playpanda # playpandanet.gogoanime.to/
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile('Playlist .+?</span></div><div><iframe src="(.+?)"').findall(r)
                for url in match: 
                    r = client.request(url)
                    if 'gogoanime' in url:
                        match = re.compile("url: '(.+?)',").findall(r)
                    else:
                        match = re.compile('file: "(.+?)",').findall(r)
                    for url in match: 
                        sources.append({'source': 'Direct','quality': 'SD','language': 'en','url': url,'direct': False,'debridonly': False}) 
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url