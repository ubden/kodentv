# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urlparse
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['timetowatch.video']
        self.base_link = 'https://www.timetowatch.video'
        self.search_link = '/?s=%s&3mh1='
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = title.lower()
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search_id.replace(':', '%3A').replace(',', '%2C').replace('&', '%26').replace("'", '%27').replace(' ', '+').replace('...', ' '))
            search_results = self.scraper.get(url).content
            match = re.compile('<div data-movie-id=.+?href="(.+?)".+?oldtitle="(.+?)".+?rel="tag">(.+?)</a></div>', re.DOTALL).findall(search_results)
            for movie_url, movie_title, movie_year in match:
                clean_title = cleantitle.get(title)
                movie_title = movie_title.replace('&#8230', ' ').replace('&#038', ' ').replace('&#8217', ' ').replace('...', ' ')
                clean_movie_title = cleantitle.get(movie_title)
                if clean_movie_title in clean_title:
                    if cleantitle.get(year) in cleantitle.get(movie_year):
                        return movie_url
            return
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            html = self.scraper.get(url).content
            links = re.compile('id="linkplayer.+?href="(.+?)"', re.DOTALL).findall(html)
            for link in links:
                valid, host = source_utils.is_host_valid(link, hostDict)
                if source_utils.limit_hosts() is True and host in str(sources):
                    continue
                if valid:
                    quality, info = source_utils.get_release_quality(link, link)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


