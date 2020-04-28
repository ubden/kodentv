# -*- coding: utf-8 -*-

'''
    Covenant Add-on
    Copyright (C) 2018 CherryTeam

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

import json
import re
import urllib

try:
    import urlparse
except:
    import urllib.parse as urlparse

import requests
from resources.lib.modules import source_utils, client, cleantitle


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['filmowakraina.tv']
        self.base_link = 'https://filmowakraina.tv'
        self.search_link = 'https://filmowakraina.tv/titles/paginate?_token=%s&perPage=20&page=1&query=%s&type=%s'

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
            title2 = title.split('.')[0]
            localtitle2 = localtitle.split('.')[0]
            titles.append(cleantitle.normalize(cleantitle.getsearch(title2)))
            titles.append(cleantitle.normalize(cleantitle.getsearch(localtitle2)))
            titles.append(title2)
            titles.append(localtitle2)
            for title in titles:
                try:
                    token = client.request("https://filmowakraina.tv/movies")
                    token = re.findall("""token:.*'(.*?)'""", token)[0]
                    url = self.search_link % (token, urllib.quote_plus(cleantitle.query(title)), 'movie')
                    content = client.request(url)
                    content = json.loads(content)
                    for item in content[u'items']:
                        if year in item[u'release_date']:
                            return item[u'link']
                except:
                    pass

        except:
            return

    def search_ep(self, titles, season, episode):
        try:
            titles = list(titles)
            titles.sort()
            year = titles[0]
            for title in titles[1:]:
                try:
                    token = client.request("https://filmowakraina.tv/movies")
                    token = re.findall("""token:.*'(.*?)'""", token)[0]
                    url = self.search_link % (token, urllib.quote_plus(cleantitle.query(title)), 'series')
                    content = client.request(url)
                    content = json.loads(content)
                    for item in content[u'items']:
                        if year in item[u'release_date']:
                            test = [x for x in item[u'link'] if
                                    x[u'season'] == int(season) and x[u'episode'] == int(episode)]
                            return test
                except:
                    pass
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        return {tvshowtitle, localtvshowtitle, year}

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        return self.search_ep(url, season, episode)

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None: return sources
            for link in url:
                try:
                    lang = link[u'quality']
                    video_link = link[u'url']
                    lang, info = self.get_lang_by_type(lang)
                    q = source_utils.check_sd_url(video_link)
                    valid, host = source_utils.is_host_valid(video_link, hostDict)
                    if 'rapidvideo' in video_link:
                        content = requests.get(video_link, timeout=3, allow_redirects=True).content
                        q = re.findall("""data-res=\"(.*?)\"""", content)[0]
                        if int(q) == 720:
                            q = 'HD'
                        elif int(q) > 720:
                            q = '1080'
                        elif int(q) < 720:
                            q = 'SD'
                    if 'streamango' in video_link or 'openload' in video_link:
                        content = requests.get(video_link, timeout=3, allow_redirects=True).content
                        q = re.findall("""og:title\" content=\"(.*?)\"""", content)[0]
                        q = source_utils.get_release_quality('', q)[0]
                    if valid:
                        if 'ebd' in host.lower():
                            host = 'CDA'
                        sources.append({'source': host, 'quality': q, 'language': lang, 'url': video_link,
                                        'info': info, 'direct': False, 'debridonly': False})
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
