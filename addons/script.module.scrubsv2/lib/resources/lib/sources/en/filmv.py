# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urllib, urlparse, requests
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  #  Old  filmovizija.vip  filmovizija.fun
        self.domains = ['milversite.live']
        self.base_link = 'http://milversite.live'
        self.search_link = 'https://www.milversite.live/search.php?all=all&keywords=%s&vselect=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link %(clean_title, 'mov'))) + '$$$$$' + title + '$$$$$' + year + '$$$$$' + 'movie'
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = 'https://www.milversite.live/watch-%s-tvshows.html#' % tvshowtitle.replace(" ", "_")
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            x = client.request(url, timeout=10)
            regex = "dropdown'>Season %s<(.+?)</li> " % season
            match = re.compile(regex, re.DOTALL).findall(x)
            regex = " id='epiloader' class='(.+?)'><span style='.+?'>%s\." % episode
            match2 = re.compile(regex, re.DOTALL).findall(match[0])[0]
            url = match2 + '$$$$$' + title + '$$$$$' + premiered + '$$$$$' + 'tv'
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            self.sources = []
            if url == None:
                return self.sources
            data = url.split('$$$$$')
            url = data[0]
            title = data[1]
            year = data[2]
            type = data[3]
            if type == 'tv':
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                    'Accept': 'text/html, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': url,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'TE': 'Trailers',
                }
                params = (
                    ('vid',url),
                )
                response = requests.get('https://www.milversite.live/episode.php', headers=headers, params=params).content
                regex = 'class="fullm"><a href="(.+?)"'
                match2 = re.compile(regex).findall(response)
                for link_in in match2:
                    quality = "720p"
                    host = link_in.replace('\n', '').strip().split('//')[1].replace('www.', '')
                    host = host.split('/')[0].lower()
                    if source_utils.limit_hosts() is True and host in str(self.sources):
                        continue
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if valid:
                        self.sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link_in, 'direct': False, 'debridonly': False})
            else:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': url,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'TE': 'Trailers',
                }
                r = client.request(url, timeout=10)
                match = re.compile("<div id=\"hd_s_g\">SUBS</div><a title = '(.+?)' href='(.+?)'").findall(r)
                for items, link in match:
                    if title.lower() in items.lower() and year in items:
                        y = client.request(link, timeout=10)
                        match2 = re.compile('class="redirect" id="(.+?)"').findall(y)
                        for link_in in match2:
                            data = {'id': link_in}
                            response = requests.post('https://www.milversite.live/morgan.php', headers=headers, data=data).content
                            quality = "720p"
                            host = response.replace('\n', '').strip().split('//')[1].replace('www.', '')
                            host = host.split('/')[0].lower()
                            if source_utils.limit_hosts() is True and host in str(self.sources):
                                continue
                            valid, host = source_utils.is_host_valid(host, hostDict)
                            if valid:
                                self.sources.append({'source':host , 'quality': quality, 'language': 'en', 'url': response.replace('\n', '').strip(), 'direct': False, 'debridonly': False})
            return self.sources
        except:
            return self.sources


    def resolve(self, url):
        return url


