# -*- coding: utf-8 -*-

import re,urllib,urlparse
import traceback
from resources.lib.modules import log_utils, source_utils
from resources.lib.modules import client, rd_check
from resources.lib.modules import debrid, control
from resources.lib.sources import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['rlsbb.ru']
        self.base_link = 'http://rlsbb.ru'
        self.search_base_link = 'http://search.rlsbb.ru'
        self.search_cookie = 'serach_mode=rlsbb'
        self.search_link = '/lib/search526049.php?phrase=%s&pindex=1&content=true'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False: return
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() is False: return
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status() is False: return
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
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            premDate = ''

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])

            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)
            query = query.replace("&", "and")
            query = query.replace("  ", " ")
            query = query.replace(" ", "-")

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            url = "http://rlsbb.ru/" + query
            if 'tvshowtitle' not in data:
                url = url + "-1080p"

            r = cfscrape.get(url, headers=self.headers).content

            if r is None and 'tvshowtitle' in data:
                season = re.search('S(.*?)E', hdlr)
                season = season.group(1)
                query = title
                query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)
                query = query + "-S" + season
                query = query.replace("&", "and")
                query = query.replace("  ", " ")
                query = query.replace(" ", "-")
                url = "http://rlsbb.ru/" + query
                r = cfscrape.get(url, headers=self.headers).content

            for loopCount in range(0, 2):
                if loopCount == 1 or (r is None and 'tvshowtitle' in data):

                    premDate = re.sub('[ \.]','-',data['premiered'])
                    query = re.sub('[\\\\:;*?"<>|/\-\']', '', data['tvshowtitle'])
                    query = query.replace("&", " and ").replace("  ", " ").replace(" ", "-")
                    query = query + "-" + premDate

                    url = "http://rlsbb.ru/" + query
                    url = url.replace('The-Late-Show-with-Stephen-Colbert','Stephen-Colbert')

                    r = cfscrape.get(url, headers=self.headers).content

                posts = client.parseDOM(r, "div", attrs={"class": "content"})
                hostDict = hostprDict + hostDict
                if control.setting('deb.rd_check') == 'true':
                    limit = 25
                    items = []
                    for index, post in enumerate(posts):
                        if index == limit:
                            break
                        try:
                            u = client.parseDOM(post, 'a', ret='href')
                            for i in u:
                                try:
                                    name = str(i)
                                    if hdlr in name.upper(): items.append(name)
                                    elif len(premDate) > 0 and premDate in name.replace(".","-"): items.append(name)

                                except:
                                    pass
                        except:
                            pass

                    if len(items) > 0:
                        break
                else:
                    items = []
                    for post in posts:
                        try:
                            u = client.parseDOM(post, 'a', ret='href')
                            for i in u:
                                try:
                                    name = str(i)
                                    if hdlr in name.upper(): items.append(name)
                                    elif len(premDate) > 0 and premDate in name.replace(".","-"): items.append(name)

                                except:
                                    pass
                        except:
                            pass

                    if len(items) > 0:
                        break

            seen_urls = set()

            for item in items:
                try:
                    info = []

                    url = str(item)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    if url in seen_urls: continue
                    seen_urls.add(url)

                    host = url.replace("\\", "")
                    host2 = host.strip('"')
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(host2.strip().lower()).netloc)[0]

                    if host not in hostDict:
                        raise Exception()
                    if any(x in host2 for x in ['.rar', '.zip', '.iso']): continue

                    quality, info = source_utils.get_release_quality(host2, host2)

                    info = ' | '.join(info)
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    if control.setting('deb.rd_check') == 'true':
                        check = rd_check.rd_deb_check(host2)
                        if check:
                            info = 'RD Checked' + ' | ' + info
                            sources.append(
                                {'source': host, 'quality': quality, 'language': 'en', 'url': check,
                                 'info': info, 'direct': False, 'debridonly': True})
                    else:
                        sources.append(
                            {'source': host, 'quality': quality, 'language': 'en', 'url': host2,
                             'info': info, 'direct': False, 'debridonly': True})

                except:
                    pass
            check = [i for i in sources if not i['quality'] == 'CAM']
            if check:
                sources = check
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Rlsb Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
