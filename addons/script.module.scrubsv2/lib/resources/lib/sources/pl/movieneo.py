# -*- coding: utf-8 -*-
'''
    Covenant Add-on
    Copyright (C) 2018 :)

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

import re
import requests
import sys

try:
    import urlparse
except:
    import urllib.parse as urlparse
try:
    import HTMLParser
    from HTMLParser import HTMLParser
except:
    from html.parser import HTMLParser
try:
    import urllib2
except:
    import urllib.request as urllib2

reload(sys)
sys.setdefaultencoding('utf8')

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['movieneo.com']

        self.base_link = 'https://movieneo.com'
        self.search_link = 'https://movieneo.com/search-results/'
        self.session = requests.Session()

    def contains_word(self, str_to_check, word):
        if str(word).lower() in str(str_to_check).lower():
            return True
        return False

    def contains_all_words(self, str_to_check, words):
        for word in words:
            if not self.contains_word(str_to_check, word):
                return False
        return True

    def movie(self, imdb, title, localtitle, aliases, year):
        return self.search(title, localtitle, year)

    def search(self, title, localtitle, year):
        try:
            titles = []
            titles.append(cleantitle.normalize(cleantitle.getsearch(title)))
            titles.append(cleantitle.normalize(cleantitle.getsearch(localtitle)))

            for title in titles:
                url = self.search_link + str(title)
                result = self.session.get(url).content
                result = result.decode('utf-8')
                h = HTMLParser()
                result = h.unescape(result)
                result = client.parseDOM(result, 'div', attrs={'class': 'item-detail-bigblock title title-bigblock'})
                for item in result:
                    if 'trailer' in item.lower():
                        continue
                    link = self.base_link + str(client.parseDOM(item, 'a', ret='href')[0])
                    nazwa = str(client.parseDOM(item, 'a')[0])
                    name = cleantitle.normalize(cleantitle.getsearch(nazwa))
                    name = name.replace("  ", " ")
                    title = title.replace("  ", " ")
                    words = title.split(" ")
                    if self.contains_all_words(name, words) and str(year) in name:
                        return link
        except:
            return

    def video_info(self, title):
        info = ''
        if 'lektor' in title.lower():
            info = 'Lektor'
        if 'pl' in title.lower():
            info = 'Lektor'
        if 'napisy' in title.lower():
            info = 'Napisy'
        if 'dub' in title.lower():
            info = 'Dubbing'
        if 'dubbing' in title.lower():
            info = 'Dubbing'
        return info

    def video_quality(self, title):
        quality = ''
        if '1080p'.lower() in title.lower():
            quality.append('1080p')
        if 'FHD'.lower() in title.lower():
            quality.append('1080p')
        if 'FULLHD'.lower() in title.lower():
            quality.append('1080p')
        if '720p'.lower() in title.lower():
            quality.append('720p')
        if 'HD'.lower() in title.lower():
            quality.append('720p')
        if '480p'.lower() in title.lower():
            quality.append('SD')
        if '360p'.lower() in title.lower():
            quality.append('SD')
        return quality

    def sources(self, url, hostDict, hostprDict):

        sources = []
        try:
            if url == None: return sources
            result = self.session.get(url).content
            result = result.decode('utf-8')
            h = HTMLParser()
            result = h.unescape(result)
            nazwa = str(client.parseDOM(result, 'title')[0])
            video_link = re.findall("""(http.*?\.mp4)""", result)[0]
            quality = int(re.findall("""n=(.*?)p_""", video_link)[0])
            if quality < 720:
                quality = 'SD'
            elif quality == 720:
                quality = 'HD'
            elif quality > 720:
                quality = '1080p'
            else:
                quality = 'SD'
            info = self.video_info(nazwa)
            sources.append({'source': 'Movieneo', 'quality': quality, 'language': 'pl', 'url': video_link, 'info': info,
                            'direct': True, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
