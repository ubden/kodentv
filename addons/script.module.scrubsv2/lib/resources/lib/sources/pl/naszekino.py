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

import urllib

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
from resources.lib.modules import client, cache


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['nasze-kino.tv']

        self.base_link = 'https://www.nasze-kino.tv/'
        self.search_link = 'wyszukiwarka?phrase=%s'

    def contains_word(self, str_to_check, word):
        if str(word).lower() in str(str_to_check).lower():
            return True
        return False

    def contains_all_wors(self, str_to_check, words):
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
                url = urlparse.urljoin(self.base_link, self.search_link)
                url = url % urllib.quote(title)
                cookies = client.request(self.base_link, output='cookie')
                cache.cache_insert('naszekino_cookie', cookies)
                result = client.request(url, cookie=cookies)
                result = result.decode('utf-8')

                result = client.parseDOM(result, 'div', attrs={'class': 'col-sm-4'})
                for item in result:
                    link = str(client.parseDOM(item, 'a', ret='href')[0])
                    nazwa = str(client.parseDOM(item, 'a', ret='title')[0])
                    # rok = str(client.parseDOM(result, 'div', attrs={'class': 'year'})[0])
                    names_found = nazwa.split('/')
                    names_found = [cleantitle.normalize(cleantitle.getsearch(i)) for i in names_found]
                    for name in names_found:
                        name = name.replace("  ", " ")
                        title = title.replace("  ", " ")
                        words = title.split(" ")
                        if self.contains_all_wors(name, words) and str(year) in link:
                            return link
        except:
            return

    def movie(self, imdb, title, localtitle, aliases, year):
        return self.search(title, localtitle, year, True)

    ## TODO
    #     def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
    #         return self.search(tvshowtitle, localtvshowtitle, year, False)
    #
    #     def episode(self, url, imdb, tvdb, title, premiered, season, episode):
    #         try:
    #             if url == None: return
    #
    #             url = urlparse.urljoin(self.base_link, url)
    #             result = self.getUrlRequestData(url,self.proxy)
    #             result = client.parseDOM(result, 'ul', attrs={'data-season-num': season})[0]
    #             result = client.parseDOM(result, 'li')
    #             for i in result:
    #                 s = client.parseDOM(i, 'a', attrs={'class': 'episodeNum'})[0]
    #                 e = int(s[7:-1])
    #                 if e == int(episode):
    #                     return client.parseDOM(i, 'a', attrs={'class': 'episodeNum'}, ret='href')[0]
    #
    #         except :
    #             return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            cookies = cache.cache_get('naszekino_cookie')
            result = client.request(url, cookie=cookies)

            result = client.parseDOM(result, 'table', attrs={'class': 'table table-bordered'})
            result = client.parseDOM(result, 'tr')
            for item in result:
                try:
                    link = client.parseDOM(item, 'td', attrs={'class': 'link-to-video'})
                    link = str(client.parseDOM(link, 'a', ret='href')[0])
                    temp = client.parseDOM(item, 'td')
                    wersja = str(temp[1])
                    lang, info = self.get_lang_by_type(wersja)
                    valid, host = source_utils.is_host_valid(link, hostDict)
                    jakosc = str(temp[2]).lower()
                    if "wysoka" in jakosc:
                        q = "HD"
                    else:
                        q = source_utils.check_sd_url(link)
                    sources.append(
                        {'source': host, 'quality': q, 'language': lang, 'url': link, 'info': info, 'direct': False,
                         'debridonly': False})
                except:
                    continue
            return sources
        except:
            return sources

    def get_lang_by_type(self, lang_type):
        if "dubbing" in lang_type.lower():
            if "kino" in lang_type.lower():
                return 'pl', 'Dubbing Kino'
            return 'pl', 'Dubbing'
        elif lang_type == 'Napisy PL':
            return 'pl', 'Napisy'
        elif lang_type == 'Napisy':
            return 'pl', 'Napisy'
        elif lang_type == 'Lektor PL':
            return 'pl', 'Lektor'
        elif lang_type == 'Lektor':
            return 'pl', 'Lektor'
        elif lang_type == 'LEKTOR_AMATOR':
            return 'pl', 'Lektor'
        elif lang_type == 'POLSKI':
            return 'pl', None
        return 'en', None

    def resolve(self, url):
        return url
