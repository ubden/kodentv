# -*- coding: utf-8 -*-

import os, sys, re, urllib, urlparse
import json, datetime, base64
from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import cleangenre
from resources.lib.modules import control
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import trakt
from resources.lib.modules import utils
from resources.lib.modules import views
from resources.lib.modules import workers

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', ''))) if len(sys.argv) > 1 else dict()
action = params.get('action')
control.moderator()


class tvshows:
    def __init__(self):
        self.list = []
        self.tmdb_link = 'https://api.themoviedb.org'
        self.imdb_link = 'https://www.imdb.com'
        self.trakt_link = 'https://api.trakt.tv'
        self.tvmaze_link = 'http://www.tvmaze.com'
        self.tvdb_key = base64.urlsafe_b64decode('MUQ2MkYyRjkwMDMwQzQ0NA==')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.omdb_key = control.setting('omdb.key')
        self.tmdb_key = control.setting('tm.user')
        if self.tmdb_key == '' or self.tmdb_key == None:
            self.tmdb_key = base64.b64decode('YzhiN2RiNzAxYmFjMGIyNmVkZmNjOTNiMzk4NTg5NzI=')
        self.lang = control.apiLanguage()['tvdb']
        self.tmdb_lang = 'en'
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        self.year_date = (self.datetime - datetime.timedelta(days = 365)).strftime('%Y-%m-%d')
        self.info_lang = 'en'
        self.tmdb_info_link = 'https://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=credits,releases,external_ids' % ('%s', self.tmdb_key, self.tmdb_lang)
        self.tmdb_poster = 'http://image.tmdb.org/t/p/w500'
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tvmaze_info_link = 'http://api.tvmaze.com/shows/%s'
        self.tvdb_info_link = 'https://thetvdb.com/api/%s/series/%s/%s.zip.xml' % (self.tvdb_key, '%s', self.lang)
        self.tvdb_by_imdb = 'https://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tvdb_by_query = 'https://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.imdb_by_query = 'http://www.omdbapi.com/?i=%s&apikey=%s' % ("%s", self.omdb_key)
        self.tvdb_image = 'https://thetvdb.com/banners/'
        self.tmdb_by_query_imdb = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % ("%s", self.tmdb_key)

        self.person_link = 'https://api.themoviedb.org/3/person/%s?api_key=%s&append_to_response=tv_credits'
        self.genre_link = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&with_genres=%s&first_air_date.gte=date[365]&first_air_date.lte=date[0]&page=1'
        self.genres_link = 'https://api.themoviedb.org/3/genre/tv/list?api_key=%s&language=en' % self.tmdb_key
        self.network_link = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&with_networks=%s&page=1' % (self.tmdb_key, '%s')
        self.year_link = 'https://api.themoviedb.org/3/discover/movie?&api_key=%s&year=%s&primary_release_date.lte=date[0]&page=1'

        self.popular_link = 'https://api.themoviedb.org/3/tv/popular?api_key=%s&page=1' % self.tmdb_key
        self.featured_link = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&vote_count.gte=100&sort_by=first_air_date.desc&page=1'  % (self.tmdb_key)
        self.airing_link = 'https://api.themoviedb.org/3/tv/airing_today?api_key=%s&page=1' % self.tmdb_key
        self.premiere_link = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&first_air_date.gte=%s&first_air_date.lte=%s&page=1' % (self.tmdb_key, self.year_date, self.today_date)
        self.active_link = 'https://api.themoviedb.org/3/tv/on_the_air?api_key=%s&page=1' % self.tmdb_key
        self.rating_link = 'https://api.themoviedb.org/3/tv/top_rated?api_key=%s&page=1' % self.tmdb_key
        self.views_link = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&vote_count.gte=100&sort_by=vote_average.desc&page=1' % self.tmdb_key

        self.tmdbUserLists_link = 'https://api.themoviedb.org/4/list/%s?api_key=%s' % ("%s", self.tmdb_key)
        self.tmdbjew250tv_link = self.tmdbUserLists_link % ('86660')
        self.tmdbjewtestshows_link = self.tmdbUserLists_link % ('97124')
        self.tmdbhuluorig_link = self.tmdbUserLists_link % ('47716')  # TV Shows - Hulu Original
        self.tmdbnetflixorig_link = self.tmdbUserLists_link % ('47713')  # TV Shows - Netflix Original
        self.tmdbamazonorig_link = self.tmdbUserLists_link % ('47714')  # TV Shows - Amazon Original


    def get(self, url, idx=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass
            try:
                u = urlparse.urlparse(url).netloc.lower()
            except:
                pass
            if u in self.tmdb_link:
                self.list = cache.get(self.tmdb_list, 24, url)
                self.worker()
            elif u in self.trakt_link and '/users/' in url:
                try:
                    if not '/users/me/' in url:
                        raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user):
                        raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)
                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))
                if idx == True:
                    self.worker()
            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True:
                    self.worker(level=0)
            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True:
                    self.worker()
            if idx == True:
                self.tvshowDirectory(self.list)
            return self.list
        except:
            pass


    def my_tmdbUserLists(self):
        tvlist1 = control.setting('tmdb.tvlist_name1')
        tvlist1_link = control.setting('tmdb.tvlist_id1')
        if tvlist1:
            self.list.append({'name': tvlist1, 'url': self.tmdbUserLists_link % tvlist1_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist2 = control.setting('tmdb.tvlist_name2')
        tvlist2_link = control.setting('tmdb.tvlist_id2')
        if tvlist2:
            self.list.append({'name': tvlist2, 'url': self.tmdbUserLists_link % tvlist2_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist3 = control.setting('tmdb.tvlist_name3')
        tvlist3_link = control.setting('tmdb.tvlist_id3')
        if tvlist3:
            self.list.append({'name': tvlist3, 'url': self.tmdbUserLists_link % tvlist3_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist4 = control.setting('tmdb.tvlist_name4')
        tvlist4_link = control.setting('tmdb.tvlist_id4')
        if tvlist4:
            self.list.append({'name': tvlist4, 'url': self.tmdbUserLists_link % tvlist4_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist5 = control.setting('tmdb.tvlist_name5')
        tvlist5_link = control.setting('tmdb.tvlist_id5')
        if tvlist5:
            self.list.append({'name': tvlist5, 'url': self.tmdbUserLists_link % tvlist5_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist6 = control.setting('tmdb.tvlist_name6')
        tvlist6_link = control.setting('tmdb.tvlist_id6')
        if tvlist6:
            self.list.append({'name': tvlist6, 'url': self.tmdbUserLists_link % tvlist6_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist7 = control.setting('tmdb.tvlist_name7')
        tvlist7_link = control.setting('tmdb.tvlist_id7')
        if tvlist7:
            self.list.append({'name': tvlist7, 'url': self.tmdbUserLists_link % tvlist7_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist8 = control.setting('tmdb.tvlist_name8')
        tvlist8_link = control.setting('tmdb.tvlist_id8')
        if tvlist8:
            self.list.append({'name': tvlist8, 'url': self.tmdbUserLists_link % tvlist8_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist9 = control.setting('tmdb.tvlist_name9')
        tvlist9_link = control.setting('tmdb.tvlist_id9')
        if tvlist9:
            self.list.append({'name': tvlist9, 'url': self.tmdbUserLists_link % tvlist9_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        tvlist10 = control.setting('tmdb.tvlist_name10')
        tvlist10_link = control.setting('tmdb.tvlist_id10')
        if tvlist10:
            self.list.append({'name': tvlist10, 'url': self.tmdbUserLists_link % tvlist10_link, 'image': 'tmdb.png', 'action': 'tvshows2'})
        self.addDirectory(self.list)
        return self.list


    def tmdbUserLists(self):
        theUserLists = [
            ('Adult Animation', '47436'),
            ('Animation TV', '13573'),
            ('Based on a True Story', '36782'),
            ('Cartoons Blast From The Past', '13467'),
            ('CIA', '47880'),
            ('Classic TV', '37592'),
            ('Comedy', '48274'),
            ('Court', '48222'),
            ('Datenight', '48293'),
            ('FBI', '47877'),
            ('FG The Cars the Star TV Shows', '38851'),
            ('Kids Television', '13555'),
            ('Man and Machine', '48225'),
            ('Organised Crime', '47871'),
            ('Out of this World', '13388'),
            ('Preschool TV Shows', '13564'),
            ('Spotlight TV', '13427'),
            ('TV Elimination', '13391')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.tmdbUserLists_link % i[1], 'image': 'tmdb.png', 'action': 'tvshows2'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_list(self, url):
        next = url
        result = client.request(url)
        result = json.loads(result)
        items = result['results']
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            url2 = '%s&page=%s' % (url.split('&page=', 1)[0], str(page+1))
            result = client.request(url2 % self.tmdb_key)
            result = json.loads(result)
            items += result['results']
        except:
            pass
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in url:
                raise Exception()
            next = '%s&page=%s' % (next.split('&page=', 1)[0], str(page+1))
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                title = item['name']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['first_air_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                tmdb = item['id']
                if tmdb == '' or tmdb == None:
                    tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                imdb = '0'
                tvdb = '0'
                poster = item['poster_path']
                if poster == '' or poster == None:
                    poster = '0'
                else:
                    poster = self.tmdb_poster + poster
                poster = poster.encode('utf-8')
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None:
                    fanart = '0'
                if not fanart == '0':
                    fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                premiered = item['first_air_date']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')
                rating = str(item['vote_average'])
                if rating == '' or rating == None:
                    rating = '0'
                rating = rating.encode('utf-8')
                votes = str(item['vote_count'])
                try:
                    votes = str(format(int(votes),',d'))
                except:
                    pass
                if votes == '' or votes == None:
                    votes = '0'
                votes = votes.encode('utf-8')
                plot = item['overview']
                if plot == '' or plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try:
                    tagline = tagline.encode('utf-8')
                except:
                    pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': '0', 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


    def trakt_list(self, url, user):
        try:
            dupes = []
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            result = trakt.getTraktAsJson(str(u))
            items = []
            for i in result:
                try:
                    items.append(i['show'])
                except:
                    pass
            if len(items) == 0:
                items = result
        except:
            return
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            if not int(q['limit']) == len(items):
                raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                title = item['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')
                tvdb = item['ids']['tvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')
                if tvdb == None or tvdb == '' or tvdb in dupes:
                    raise Exception()
                dupes.append(tvdb)
                poster = '0'
                try:
                    poster = item['images']['poster']['medium']
                except:
                    pass
                if poster == None or not '/posters/' in poster:
                    poster = '0'
                poster = poster.rsplit('?', 1)[0]
                poster = poster.encode('utf-8')
                banner = poster
                try:
                    banner = item['images']['banner']['full']
                except:
                    pass
                if banner == None or not '/banners/' in banner:
                    banner = '0'
                banner = banner.rsplit('?', 1)[0]
                banner = banner.encode('utf-8')
                fanart = '0'
                try:
                    fanart = item['images']['fanart']['full']
                except:
                    pass
                if fanart == None or not '/fanarts/' in fanart:
                    fanart = '0'
                fanart = fanart.rsplit('?', 1)[0]
                fanart = fanart.encode('utf-8')
                try:
                    premiered = item['first_aired']
                except:
                    premiered = '0'
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')
                try:
                    studio = item['network']
                except:
                    studio = '0'
                if studio == None:
                    studio = '0'
                studio = studio.encode('utf-8')
                try:
                    genre = item['genres']
                except:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')
                try:
                    duration = str(item['runtime'])
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'
                duration = duration.encode('utf-8')
                try:
                    rating = str(item['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'
                rating = rating.encode('utf-8')
                try:
                    votes = str(item['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes),',d'))
                except:
                    pass
                if votes == None:
                    votes = '0'
                votes = votes.encode('utf-8')
                try:
                    mpaa = item['certification']
                except:
                    mpaa = '0'
                if mpaa == None:
                    mpaa = '0'
                mpaa = mpaa.encode('utf-8')
                try:
                    plot = item['overview']
                except:
                    plot = '0'
                if plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': '0', 'plot': plot, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


    def imdb_list(self, url):
        try:
            dupes = []
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))
            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url).decode('iso-8859-1').encode('utf-8'), 'meta', ret='content', attrs = {'property': 'pageId'})[0]
            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url
            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url
            result = client.request(url)
            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'div', attrs = {'class': 'lister-item mode-advanced'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
        except:
            return
        try:
            next = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'lister-page-next.+?'})
            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs = {'class': 'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]
            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = client.parseDOM(item, 'span', attrs = {'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs = {'class': 'year_type'})
                year = re.findall('(\d{4})', year[0])[0]
                year = year.encode('utf-8')
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')
                if imdb in dupes:
                    raise Exception()
                dupes.append(imdb)
                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    poster = '0'
                poster = re.sub('(?:_SX\d+?|)(?:_SY\d+?|)(?:_UX\d+?|)_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
                rating = '0'
                try:
                    rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
                except:
                    pass
                try:
                    rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
                except:
                    rating = '0'
                try:
                    rating = client.parseDOM(item, 'div', ret='data-value', attrs = {'class': '.*?imdb-rating'})[0]
                except:
                    pass
                if rating == '' or rating == '-':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')
                plot = '0'
                try:
                    plot = client.parseDOM(item, 'p', attrs = {'class': 'text-muted'})[0]
                except:
                    pass
                try:
                    plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                except:
                    pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '':
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': '0', 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': '0', 'mpaa': '0', 'cast': '0', 'plot': plot, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': '0', 'next': next})
            except:
                pass
        return self.list


    def worker(self):
        self.meta = []
        total = len(self.list)
        for i in range(0, total):
            self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.lang)
        for r in range(0, total, 40):
            threads = []
            for i in range(r, r+40):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            if len(self.meta) > 0:
                metacache.insert(self.meta)
        self.list = [i for i in self.list]


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                raise Exception()
            try:
                tmdb = self.list[i]['tmdb']
            except:
                tmdb = '0'
            if not tmdb == '0':
                url = self.tmdb_info_link % tmdb
            else:
                raise Exception()
            item = client.request(url, timeout='20')
            item = json.loads(item)
            title = item['name']
            if not title == '0':
                self.list[i].update({'title': title})
            year = item['first_air_date']
            try:
                year = re.compile('(\d{4})').findall(year)[0]
            except:
                year = '0'
            if year == '' or year == None:
                year = '0'
            year = year.encode('utf-8')
            if not year == '0':
                self.list[i].update({'year': year})
            tmdb = item['id']
            if tmdb == '' or tmdb == None:
                tmdb = '0'
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            if not tmdb == '0':
                self.list[i].update({'tmdb': tmdb})
            tvdb = item['external_ids']['tvdb_id']
            if tvdb == '' or tvdb == None:
                tvdb = '0'
            tvdb = re.sub('[^0-9]', '', str(tvdb))
            tvdb = tvdb.encode('utf-8')
            if not tvdb == '0':
                self.list[i].update({'tvdb': tvdb})
            imdb = item['external_ids']['imdb_id']
            if imdb == '' or imdb == None:
                imdb = '0'
            if not imdb == '0':
                self.list[i].update({'imdb': imdb})
            if not imdb == '0':
                url = self.imdb_by_query % imdb
            item2 = client.request(url, timeout='10')
            item2 = json.loads(item2)
            duration = item['episode_run_time']
            try: 
                duration = str(duration)
                duration = duration.split(",")
                duration = duration[0]
            except:
                pass
            duration = re.sub('[^0-9]', '', str(duration))
            if duration == None or duration == '' or duration == 'N/A':
                duration = '0'
            if not duration == '0':
                self.list[i].update({'duration': duration})
            premiered = item2['Released']
            if premiered == None or premiered == '' or premiered == 'N/A':
                premiered = '0'
            premiered = re.findall('(\d*) (.+?) (\d*)', premiered)
            try:
                premiered = '%s-%s-%s' % (premiered[0][2], {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}[premiered[0][1]], premiered[0][0])
            except:
                premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0':
                self.list[i].update({'premiered': premiered})
            rating = item2['imdbRating']
            if rating == None or rating == '' or rating == 'N/A' or rating == '0.0':
                rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0':
                self.list[i].update({'rating': rating})
            votes = item2['imdbVotes']
            try:
                votes = str(format(int(votes),',d'))
            except:
                pass
            if votes == None or votes == '' or votes == 'N/A':
                votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0':
                self.list[i].update({'votes': votes})
            mpaa = item2['Rated']
            if mpaa == None or mpaa == '' or mpaa == 'N/A':
                mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0':
                self.list[i].update({'mpaa': mpaa})
            director = item2['Director']
            if director == None or director == '' or director == 'N/A':
                director = '0'
            director = director.replace(', ', ' / ')
            director = re.sub(r'\(.*?\)', '', director)
            director = ' '.join(director.split())
            director = director.encode('utf-8')
            if not director == '0':
                self.list[i].update({'director': director})
            writer = item2['Writer']
            if writer == None or writer == '' or writer == 'N/A':
                writer = '0'
            writer = writer.replace(', ', ' / ')
            writer = re.sub(r'\(.*?\)', '', writer)
            writer = ' '.join(writer.split())
            writer = writer.encode('utf-8')
            if not writer == '0':
                self.list[i].update({'writer': writer})
            cast = item2['Actors']
            if cast == None or cast == '' or cast == 'N/A':
                cast = '0'
            cast = [x.strip() for x in cast.split(',') if not x == '']
            try:
                cast = [(x.encode('utf-8'), '') for x in cast]
            except:
                cast = []
            if cast == []:
                cast = '0'
            if not cast == '0':
                self.list[i].update({'cast': cast})
            plot = item2['Plot']
            if plot == None or plot == '' or plot == 'N/A':
                plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0':
                self.list[i].update({'plot': plot})
            poster = item['poster_path']
            if poster == '' or poster == None:
                poster = '0'
            if not poster == '0':
                poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            if not poster == '0':
                self.list[i].update({'poster': poster})
            fanart = item['backdrop_path']
            if fanart == '' or fanart == None:
                fanart = '0'
            if not fanart == '0':
                fanart = self.tmdb_image + fanart
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.list[i]['fanart'] == '0':
                self.list[i].update({'fanart': fanart})
            studio = item['networks']
            try:
                studio = [x['name'] for x in studio][0]
            except:
                studio = '0'
            if studio == '' or studio == None:
                studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0':
                self.list[i].update({'studio': studio})
            genre = item['genres']
            try:
                genre = [x['name'] for x in genre]
            except:
                genre = '0'
            if genre == '' or genre == None or genre == []:
                genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0':
                self.list[i].update({'genre': genre})
            tagline = '0'
            if not tagline == '0':
                self.list[i].update({'tagline': tagline})
            self.meta.append({'tmdb': tmdb, 'imdb': imdb, 'tvdb': tvdb, 'lang': 'en', 'item': {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}})
        except:
            pass


    def tvshowDirectory(self, items):
        if items == None or len(items) == 0:
            control.idle(); sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()
        try:
            isOld = False; control.item().getArt('type')
        except:
            isOld = True
        indicators = playcount.getTVShowIndicators(refresh=True) if action == 'tvshows' else playcount.getTVShowIndicators()
        flatten = True if control.setting('flatten.tvshows') == 'true' else False
        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')
        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        playRandom = control.lang(32535).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')
        for i in items:
            try:
                label = i['title']
                systitle = sysname = urllib.quote_plus(i['originaltitle'])
                sysimage = urllib.quote_plus(i['poster'])
                imdb, tvdb, year = i['imdb'], i['tvdb'], i['year']
                meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tvdb_id': tvdb})
                meta.update({'mediatype': 'tvshow'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})
                if not 'duration' in i:
                    meta.update({'duration': '60'})
                elif i['duration'] == '0':
                    meta.update({'duration': '60'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass
                try:
                    overlay = int(playcount.getTVShowOverlay(indicators, tvdb))
                    if overlay == 7:
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                if flatten == True:
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (sysaddon, systitle, year, imdb, tvdb)
                else:
                    url = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (sysaddon, systitle, year, imdb, tvdb)
                cm = []
                cm.append(('Find similar', 'ActivateWindow(10025,%s?action=tvshows&url=https://api.trakt.tv/shows/%s/related,return)' % (sysaddon, imdb)))
                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=season&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (sysaddon, urllib.quote_plus(systitle), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb))))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                cm.append((watchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=7)' % (sysaddon, systitle, imdb, tvdb)))
                cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=6)' % (sysaddon, systitle, imdb, tvdb)))
                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&tvdb=%s&content=tvshow)' % (sysaddon, sysname, tvdb)))
                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))
                cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (sysaddon, systitle, year, imdb, tvdb)))
                item = control.item(label=label)
                art = {}
                if 'poster' in i and not i['poster'] == '0':
                    art.update({'icon': i['poster'], 'thumb': i['poster'], 'poster': i['poster']})
                # elif 'poster2' in i and not i['poster2'] == '0':
                # art.update({'icon': i['poster2'], 'thumb': i['poster2'], 'poster': i['poster2']})
                else:
                    art.update({'icon': addonPoster, 'thumb': addonPoster, 'poster': addonPoster})
                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                # elif 'banner2' in i and not i['banner2'] == '0':
                # art.update({'banner': i['banner2']})
                elif 'fanart' in i and not i['fanart'] == '0':
                    art.update({'banner': i['fanart']})
                else:
                    art.update({'banner': addonBanner})
                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})
                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})
                if settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                # elif settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                # item.setProperty('Fanart_Image', i['fanart2'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels = control.metadataClean(meta))
                #item.setInfo(type='Video', infoLabels=meta) # old code
                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass
        try:
            url = items[0]['next']
            if url == '':
                raise Exception()
            icon = control.addonNext()
            url = '%s?action=tvshowPage&url=%s' % (sysaddon, urllib.quote_plus(url))
            item = control.item(label=nextMenu)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None:
                item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass
        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0:
            control.idle(); sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()
        queueMenu = control.lang(32065).encode('utf-8')
        playRandom = control.lang(32535).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')
        for i in items:
            try:
                name = i['name']
                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb
                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib.quote_plus(i['url'])
                except:
                    pass
                cm = []
                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=show&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))
                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowsToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
                except:
                    pass
                item = control.item(label=name)
                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


