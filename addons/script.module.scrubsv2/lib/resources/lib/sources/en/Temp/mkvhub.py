# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 06-17-2019 by JewBMX in Scrubs.

import re, urllib, urlparse
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils
from resources.lib.modules import workers
import traceback
from resources.lib.modules import log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['mkvhub.com']
        self.base_link = 'https://www.mkvhub.com'
        self.search_link = '/search/%s/feed/rss2/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []
            if url is None:
                return self._sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                    if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            r = client.request(url)
            posts = client.parseDOM(r, 'item')
            items = []
            for post in posts:
                try:
                    tit = client.parseDOM(post, 'title')[0]
                    t = tit.split(hdlr)[0].replace('(', '')
                    if not cleantitle.get(t) == cleantitle.get(title):
                        raise Exception()
                    try:
                        y = re.findall(r'(?:\.|\(|\[|\s*|)(S\d+E\d+|S\d+)(?:\.|\)|\]|\s*|)', tit, re.I)[-1].upper()
                    except Exception:
                        y = re.findall(r'(?:\.|\(|\[|\s*|)(\d{4})(?:\.|\)|\]|\s*|)', tit, re.I)[-1]
                    if not y == hdlr:
                        raise Exception()
                    urls = [(client.parseDOM(post, 'a', ret='href', attrs={'class': 'dbuttn watch'})[0],
                             client.parseDOM(post, 'a', ret='href', attrs={'class': 'dbuttn blue'})[0],
                             client.parseDOM(post, 'a', ret='href', attrs={'class': 'dbuttn magnet'})[0])]
                    try:
                        size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', post)[0]
                        div = 1 if size.endswith(('GB', 'GiB', 'Gb')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                        size = '%.2f GB' % size
                    except Exception:
                        size = '0'
                    items += [(tit, urls, size)]
                except Exception:
                    pass
            datos = []
            for title, urls, size in items:
                try:
                    name = client.replaceHTMLCodes(title)
                    quality, info = source_utils.get_release_quality(name, name)
                    info.append(size)
                    info = ' | '.join(info)
                    datos.append((urls[0], quality, info))
                except Exception:
                    pass
            threads = []
            for i in datos:
                threads.append(workers.Thread(self._get_sources, i[0], i[1], i[2], hostDict, hostprDict))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self._sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---MkvHub - Exception: \n' + str(failure))
            return self._sources


    def _get_sources(self, urls, quality, info, hostDict, hostprDict):
        try:
            for url in urls:
                r = client.request(url)
                if 'linkprotector' in url:
                    p_link = dom_parser.parse_dom(r, 'link', {'rel': 'canonical'},  req='href')[0]
                    p_link = p_link.attrs['href']
                    input_name = client.parseDOM(r, 'input', ret='name')[0]
                    input_value = client.parseDOM(r, 'input', ret='value')[0]
                    post = {input_name: input_value}
                    p_data = client.request(p_link, post=post)
                    links = client.parseDOM(p_data, 'a', ret='href', attrs={'target': '_blank'})
                    for i in links:
                        valid, host = source_utils.is_host_valid(i, hostDict)
                        if not valid:
                            valid, host = source_utils.is_host_valid(i, hostprDict)
                            if not valid:
                                continue
                            else:
                                rd = True
                        else:
                            rd = False
                        if i in str(self._sources):
                            continue
                        if 'rapidgator' in i:
                            rd = True
                        if rd:
                            self._sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': i, 'info': info, 'direct': False, 'debridonly': True})
                        else:
                            self._sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': i, 'info': info, 'direct': False, 'debridonly': False})
                elif 'torrent' in url:
                    data = client.parseDOM(r, 'a', ret='href')
                    url = [i for i in data if 'magnet:' in i][0]
                    url = url.split('&tr')[0]
                    self._sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---MkvHub - Exception: \n' + str(failure))
            pass


    def resolve(self, url):
        return url


