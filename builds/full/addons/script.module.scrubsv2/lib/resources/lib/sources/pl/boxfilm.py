# -*- coding: utf-8 -*-

'''
    Covenant Add-on
    Copyright (C) 2017 homik

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
import requests

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['boxfilm.pl']

        self.base_link = 'https://www.boxfilm.pl'
        self.search_link = '/szukaj'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            titles = []
            title2 = title.split('.')[0]
            localtitle2 = localtitle.split('.')[0]
            titles.append(cleantitle.normalize(cleantitle.getsearch(title2)))
            titles.append(cleantitle.normalize(cleantitle.getsearch(localtitle2)))
            titles.append(title2)
            titles.append(localtitle2)

            for title in titles:
                headers = {
                    'Connection': 'keep-alive',
                    'Cache-Control': 'max-age=0',
                    'Origin': 'https://www.boxfilm.pl',
                    'Upgrade-Insecure-Requests': '1',
                    'DNT': '1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3555.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Referer': 'https://www.boxfilm.pl/szukaj',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                }
                data = {
                    'szukaj': title
                }
                cookies = {
                    'lektor': 'Wszystkie',
                    'cookies-accepted': '1',
                }
                r = requests.post('https://www.boxfilm.pl/szukaj', headers=headers, cookies=cookies, data=data).content
                r = client.parseDOM(r, 'div', attrs={'class': 'video_info'})

                local_simple = cleantitle.get(localtitle)
                for row in r:
                    name_found = client.parseDOM(row, 'h1')[0]
                    year_found = name_found[name_found.find("(") + 1:name_found.find(")")]
                    if cleantitle.get(name_found) == local_simple and year_found == year:
                        url = client.parseDOM(row, 'a', ret='href')[0]
                        return url
        except:
            return

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

    def sources(self, url, hostDict, hostprDict):

        sources = []
        try:

            if url == None: return sources
            result = client.request(urlparse.urljoin(self.base_link, url), redirect=False)
            cookies = client.request(urlparse.urljoin(self.base_link, url), output='cookie')
            headers = {
                'cookie': cookies,
                'dnt': '1',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.91 Safari/537.36',
                'accept': 'text/html, */*; q=0.01',
                'referer': self.base_link + url,
                'authority': 'www.boxfilm.pl',
                'x-requested-with': 'XMLHttpRequest',
            }

            response = requests.get('https://www.boxfilm.pl/include/player.php', headers=headers).content
            section = client.parseDOM(result, 'section', attrs={'id': 'video_player'})[0]
            link = client.parseDOM(response, 'iframe', ret='src')[0]
            valid, host = source_utils.is_host_valid(link, hostDict)
            if not valid: return sources
            spans = client.parseDOM(section, 'span')
            info = None
            for span in spans:
                if span == 'Z lektorem':
                    info = 'Lektor'

            q = source_utils.check_sd_url(link)
            sources.append({'source': host, 'quality': q, 'language': 'pl', 'url': link, 'info': info, 'direct': False,
                            'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url
