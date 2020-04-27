# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import directstream
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['watchcartoononline.info', 'cartoonwire.to']
        self.base_link = 'https://cartoonwire.to'
        self.search_link = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.geturl(title)
            intel = '/%s-%s' % (mtitle, year)
            url = self.base_link + intel
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            headers = {'User-Agent': client.randomagent()}
            tvtitle = cleantitle.geturl(tvshowtitle)
            url = self.base_link + self.search_link % tvtitle
            r = client.request(url, headers=headers, timeout='5')
            u = client.parseDOM(r, "div", attrs={"class": "ml-item"})
            for i in u:
                t = re.compile('<a href="(.+?)"').findall(i)
                for r in t:
                    if cleantitle.get(tvtitle) in cleantitle.get(r):
                        return source_utils.strip_domain(url)
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            if season == '1': 
                url = self.base_link + '/episode/' + url + '-episode-' + episode
            else:
                url = self.base_link + '/episode/' + url + '-season-' + season + '-episode-' + episode
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        headers = {'User-Agent': client.randomagent()}
        if url == None: return sources
        try:
            r = client.request(url, headers=headers, timeout='3')
            try:
                match = re.compile('var filmId = "(.+?)"').findall(r)
                for film_id in match:
                    server = 'vip'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url, headers=headers, timeout='3')
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        r = client.request(r, headers=headers, timeout='3')
                        match = re.compile('<iframe src="(.+?)"').findall(r)
                        for url in match:
                            sources.append({ 'source': server, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                    server = 'streamango'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url, headers=headers, timeout='3')
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        r = client.request(r, headers=headers, timeout='3')
                        match = re.compile('<iframe src="(.+?)"').findall(r)
                        for url in match:
                            sources.append({ 'source': server, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                    server = 'openload'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url)
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        r = client.request(r, headers=headers, timeout='3')
                        match = re.compile('<iframe src="(.+?)"').findall(r)
                        for url in match:
                            sources.append({ 'source': server, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                    server = 'rapidvideo'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url)
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        r = client.request(r, headers=headers, timeout='3')
                        match = re.compile('<iframe src="(.+?)"').findall(r)
                        for url in match:
                            sources.append({ 'source': server, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False })
                    server = 'photo'
                    url = self.base_link + '/ajax-get-link-stream/?server=' + server + '&filmId=' + film_id
                    r = client.request(url, headers=headers, timeout='3')
                    if r == '':
                        pass
                    else:
                        quality = source_utils.check_url(r)
                        sources.append({ 'source': 'GDrive', 'quality': quality, 'language': 'en', 'url': r, 'direct': False, 'debridonly': False })
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url


