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

try:
    import urlparse
except:
    import urllib.parse as urlparse
try:
    import HTMLParser
    from HTMLParser import HTMLParser
except:
    from html.parser import HTMLParser

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['filmy321']

        self.base_link = 'https://www.filmy321.pl'
        self.search_link = 'https://www.filmy321.pl/pokaz_film'

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
                data = {
                    'search': title,
                    'wyslij_szuk': 'Szukaj filmu'
                }
                result = client.request(self.search_link, post=data)
                result = client.parseDOM(result, 'div', attrs={'class': 'movie_info'})
                for item in result:
                    try:
                        import re
                        link = self.base_link + str(client.parseDOM(item, 'a', ret='href')[0])
                        nazwa = str(client.parseDOM(item, 'span', attrs={'class': 'movie_infot'})[0])
                        regexp = re.search(r"""(\S[a-z].*?\)).*?<strong>(.*?)<""",
                                           nazwa.replace('\t', '').replace('\n', ''))
                        nazwa = regexp.group(1)
                        lektor = regexp.group(2)
                        name = cleantitle.normalize(cleantitle.getsearch(nazwa))
                        name = name.replace("  ", " ")
                        title = title.replace("  ", " ")
                        words = title.split(" ")
                        if self.contains_all_words(name, words) and str(year) in name:
                            return link, lektor
                    except:
                        continue
        except:
            return

    def movie(self, imdb, title, localtitle, aliases, year):
        return self.search(title, localtitle, year, True)

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None: return sources
            url = url[0]
            headers = {
                'dnt': '1',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.75 Safari/537.36',
                'accept': 'text/html, */*; q=0.01',
                'referer': url,
                'authority': 'www.filmy321.pl',
                'x-requested-with': 'XMLHttpRequest',
            }
            import requests
            s = requests.Session()
            s.get(self.base_link)
            result = s.get('https://www.filmy321.pl/player.php', headers=headers).content
            url = client.parseDOM(result, 'iframe', ret='src')[0]
            lang, info = self.get_lang_by_type(url[1])
            valid, host = source_utils.is_host_valid(url, hostDict)
            if not valid: raise Exception('Niepoprawny host')
            sources.append(
                {'source': host, 'quality': 'SD', 'language': lang, 'url': url, 'info': info, 'direct': False,
                 'debridonly': False})
        except:
            return sources

    def get_lang_by_type(self, lang_type):
        if "dubbing" in lang_type.lower():
            if "kino" in lang_type.lower():
                return 'pl', 'Dubbing Kino'
            return 'pl', 'Dubbing'
        elif 'napisy pl' in lang_type.lower():
            return 'pl', 'Napisy'
        elif 'napisy' in lang_type.lower():
            return 'pl', 'Napisy'
        elif 'lektor pl' in lang_type.lower():
            return 'pl', 'Lektor'
        elif 'lektor' in lang_type.lower():
            return 'pl', 'Lektor'
        elif 'POLSKI' in lang_type.lower():
            return 'pl', None
        elif 'pl' in lang_type.lower():
            return 'pl', None
        return 'en', None

    def resolve(self, url):
        link = str(url).replace("//", "/").replace(":/", "://").split("?")[0]
        return str(link)
