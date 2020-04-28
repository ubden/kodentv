# -*- coding: utf-8 -*-



import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import workers


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.mkvhub.com']
        self.base_link = 'https://www.mkvhub.net'
        self.search_link = '/?s=%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
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
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []

            if url is None:
                return self._sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

            hdlr = 'S%02d' % (int(data['season'])) if 'tvshowtitle' in data else data['year']

            query = '%s %s' % (title, hdlr)
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            # log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

            r = self.scraper.get(url).content

            posts = client.parseDOM(r, 'figure')

            items = []
            for post in posts:
                try:
                    tit = client.parseDOM(post, 'img', ret='title')[0]
                    tit = client.replaceHTMLCodes(tit)
                    t = tit.split(hdlr)[0].replace(data['year'], '').replace('(', '').replace(')', '').replace('&', 'and')
                    if cleantitle.get(t) != cleantitle.get(title):
                        continue

                    if hdlr not in tit:
                        continue

                    url = client.parseDOM(post, 'a', ret='href')[0]

                    items.append((url, tit))

                except:
                    pass

            threads = []
            for i in items:
                threads.append(workers.Thread(self._get_sources, i[0], i[1], hostDict, hostprDict))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self._sources
        except:
            return self._sources

    def _get_sources(self, url, name, hostDict, hostprDict):
        try:
            urls = []
            result = self.scraper.get(url).content

            urls = [(client.parseDOM(result, 'a', ret='href',
            attrs={'class': 'dbuttn watch'})[0],
                        client.parseDOM(result, 'a', ret='href', attrs={'class': 'dbuttn blue'})[0],
                        client.parseDOM(result, 'a', ret='href', attrs={'class': 'dbuttn magnet'})[0])]
                    
            quality, info = source_utils.get_release_quality(name, url)

            try:
                size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', result)[0]
                div = 1 if size.endswith(('GB', 'GiB', 'Gb')) else 1024
                size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                size = '%.2f GB' % size
                info.append(size)
            except:
                pass

            info = ' | '.join(info)

        except:
            return

        for url in urls[0]:
            try:
                r = self.scraper.get(url).content
                if r is None:
                    continue

                if 'linkomark' in url:
                    p_link = client.parseDOM(r, 'link', attrs={'rel': 'canonical'}, ret='href')[0]

                    input_name = client.parseDOM(r, 'input', ret='name')[0]
                    input_value = client.parseDOM(r, 'input', ret='value')[0]

                    post = {input_name: input_value}
                    p_data = self.scraper.get(p_link, post=post).content
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
                            self._sources.append({
                                'source': host, 'quality': quality, 'language': 'en', 'url': i,
                                'info': info, 'direct': False, 'debridonly': True
                            })
                        else:
                            self._sources.append({
                                'source': host, 'quality': quality, 'language': 'en', 'url': i,
                                'info': info, 'direct': False, 'debridonly': False
                            })

                elif 'torrent' in url:
                    data = client.parseDOM(r, 'a', ret='href')

                    url = [i for i in data if 'magnet:' in i][0]
                    url = urllib.unquote_plus(url).replace('&amp;', '&').replace(' ', '.')
                    url = url.split('&tr')[0]

                    self._sources.append({
                        'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                        'info': info, 'direct': False, 'debridonly': True
                    })

            except Exception:
                pass

    def resolve(self, url):
        return url
