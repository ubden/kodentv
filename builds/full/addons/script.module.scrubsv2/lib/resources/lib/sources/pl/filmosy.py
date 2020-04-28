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

import requests

try:
    import HTMLParser
    from HTMLParser import HTMLParser
except:
    from html.parser import HTMLParser
try:
    import urlparse
except:
    import urllib.parse as urlparse
try:
    import urllib2
except:
    import urllib.request as urllib2

from resources.lib.modules import source_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['filmosy.tv']

        self.base_link = 'http://www.filmosy.tv'
        self.search_link = 'http://www.filmosy.tv/'  # post
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

    def search(self, title, localtitle, year, is_movie_search):
        try:
            titles = []
            titles.append(cleantitle.normalize(cleantitle.getsearch(title)))
            titles.append(cleantitle.normalize(cleantitle.getsearch(localtitle)))

            for title in titles:
                url = self.search_link
                data = {
                    'subaction': 'search',
                    'do': 'search',
                    'story': str(title)
                }
                result = self.session.post(url, data=data).content
                result = result.decode('utf-8')
                h = HTMLParser()
                result = h.unescape(result)
                result = client.parseDOM(result, 'article', attrs={'class': 'shortstory cf'})

                for item in result:
                    link = str(client.parseDOM(item, 'a', ret='href')[0])
                    if link.startswith('//'):
                        link = "https:" + link
                    nazwa = client.parseDOM(result, 'div', attrs={'class': 'short_header'})[0]
                    name = cleantitle.normalize(cleantitle.getsearch(nazwa))
                    rok = client.parseDOM(result, 'div', attrs={'class': 'short_info'})[0]
                    name = name.replace("  ", " ")
                    title = title.replace("  ", " ")
                    words = title.split(" ")
                    if self.contains_all_words(name, words) and str(year) in rok:
                        return link, name
        except:
            return

    def movie(self, imdb, title, localtitle, aliases, year):
        return self.search(title, localtitle, year, True)

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            result = self.session.get(url[0]).content
            result = result.decode('utf-8')
            h = HTMLParser()
            result = h.unescape(result)
            quality = str(client.parseDOM(result, 'div', attrs={'class': 'poster-qulabel'}))
            quality = source_utils.check_sd_url(quality)
            info = self.get_lang_by_type(url[1])
            video_link = str(client.parseDOM(result, 'iframe', ret='src')[0])
            valid, host = source_utils.is_host_valid(video_link, hostDict)
            sources.append(
                {'source': host, 'quality': quality, 'language': info[0], 'url': video_link, 'info': info[1],
                 'direct': False,
                 'debridonly': False})
            return sources
        except:
            return sources

    def get_lang_by_type(self, lang_type):
        if "dubbing" in lang_type.lower():
            if "kino" in lang_type.lower():
                return 'pl', 'Dubbing Kino'
            return 'pl', 'Dubbing'
        elif 'lektor pl' in lang_type.lower():
            return 'pl', 'Lektor'
        elif 'lektor' in lang_type.lower():
            return 'pl', 'Lektor'
        elif 'napisy pl' in lang_type.lower():
            return 'pl', 'Napisy'
        elif 'napisy' in lang_type.lower():
            return 'pl', 'Napisy'
        elif 'POLSKI' in lang_type.lower():
            return 'pl', None
        elif 'pl' in lang_type.lower():
            return 'pl', None
        return 'en', None

    def resolve(self, url):
        return str(url)
