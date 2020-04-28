# -*- coding: utf-8 -*-
'''
BoxsetKings Add-on
Copyright (C) 2018 BoxsetKings
Rebranded from Schism's "Zen" at his request

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from schism_net import OPEN_URL
from resources.lib.modules import cache, cleangenre, cleantitle, client, control, favourites, metacache, playcount, trakt, utils, views, workers
import base64, datetime, json, os, re, sys, urllib, urlparse, xbmc

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
action = params.get('action')

class tvshows:
    def __init__(self):
        self.list                 = []
        self.tmdb_link            = 'http://api.themoviedb.org'
        self.imdb_link            = 'http://www.imdb.com'
        self.trakt_link           = 'http://api.trakt.tv'
        self.tvmaze_link          = 'http://www.tvmaze.com'
        self.tvdb_key             = base64.urlsafe_b64decode('M0MzNUI2OTNBRjE3NjVEMg==')
        self.datetime             = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.trakt_user           = control.setting('trakt.user').strip()
        self.imdb_user            = control.setting('imdb.user').replace('ur', '')
        self.lang                 = control.apiLanguage()['tvdb']
        self.tmdb_key             = control.setting('tmdb_apikey')
        if self.tmdb_key == '' or self.tmdb_key == None: self.tmdb_key = base64.b64decode('NDU5ZDMzN2ZkY2E4MGI0OTlkMmYwMTA2MDRjZWQ3MDk=')
        self.tmdb_lang            = 'en'
        self.datetime             = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.today_date           = (self.datetime).strftime('%Y-%m-%d')
        self.month_date           = (self.datetime - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        self.year_date            = (self.datetime - datetime.timedelta(days = 365)).strftime('%Y-%m-%d')
        self.info_lang            = 'en'
        self.tmdb_info_link       = 'http://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=credits,releases,external_ids' % ('%s', self.tmdb_key, self.tmdb_lang)
        self.tmdb_poster          = 'http://image.tmdb.org/t/p/w500'
        self.tmdb_image           = 'http://image.tmdb.org/t/p/original'
        self.tmdbtvlist_link      = control.setting('tmdb.tvlist')
        self.tvmaze_info_link     = 'http://api.tvmaze.com/shows/%s'
        self.tvdb_info_link       = 'http://thetvdb.com/api/%s/series/%s/%s.xml' % (self.tvdb_key, '%s', self.lang)
        self.tvdb_by_imdb         = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tvdb_by_query        = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.imdb_by_query        = 'http://www.omdbapi.com/?i=%s'
        self.tvdb_image           = 'http://thetvdb.com/banners/'
        self.tmdb_by_query_imdb   = 'http://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % ("%s", self.tmdb_key)
        self.persons_link         = 'http://www.imdb.com/search/name?count=100&name='
        self.personlist_link      = 'http://www.imdb.com/search/name?count=100&gender=male,female'
        self.popular_link         = 'http://api.themoviedb.org/3/tv/popular?api_key=%s&page=1' % self.tmdb_key
        self.featured_link        = 'http://api.themoviedb.org/3/discover/tv?api_key=%s&vote_count.gte=100&sort_by=first_air_date.desc&page=1'  % (self.tmdb_key)
        self.ontv_link            = 'http://api.themoviedb.org/3/discover/tv?api_key=%s&on-the-air.gte=100&page=1'  % (self.tmdb_key)		
        self.genres_link          = 'http://api.themoviedb.org/3/genre/tv/list?api_key=%s&language=en' % self.tmdb_key
        self.genre_link           = 'http://api.themoviedb.org/3/discover/tv?api_key=%s&with_genres=%s&first_air_date.gte=date[365]&first_air_date.lte=date[0]&page=1'
        self.airing_link          = 'http://api.themoviedb.org/3/tv/airing_today?api_key=%s&page=1' % self.tmdb_key
        self.premiere_link        = 'http://api.themoviedb.org/3/discover/tv?api_key=%s&first_air_date.gte=%s&first_air_date.lte=%s&page=1' % (self.tmdb_key, self.year_date, self.today_date)
        self.active_link          = 'http://api.themoviedb.org/3/tv/on_the_air?api_key=%s&page=1' % self.tmdb_key
        self.rating_link          = 'http://api.themoviedb.org/3/tv/top_rated?api_key=%s&page=1' % self.tmdb_key
        self.views_link           = 'http://api.themoviedb.org/3/discover/tv?api_key=%s&vote_count.gte=100&sort_by=vote_average.desc&page=1' % self.tmdb_key
        self.person_link          = 'http://api.themoviedb.org/3/person/%s?api_key=%s&append_to_response=tv_credits'
        self.network_link         = 'http://api.themoviedb.org/3/discover/tv?api_key=%s&with_networks=%s&page=1' % (self.tmdb_key, '%s')
        self.year_link            = 'http://api.themoviedb.org/3/discover/movie?&api_key=%s&year=%s&primary_release_date.lte=date[0]&page=1'
        self.traktlists_link      = 'http://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'http://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link       = 'http://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'http://api.trakt.tv/users/me/collection/shows'
        self.traktwatchlist_link  = 'http://api.trakt.tv/users/me/watchlist/shows'
        self.traktfeatured_link   = 'http://api.trakt.tv/recommendations/shows?limit=40'
        self.tmdbtvlist1_link     = control.setting('tmdb.tvlist_id1')
        self.tmdbtvlist2_link     = control.setting('tmdb.tvlist_id2')
        self.tmdbtvlist3_link     = control.setting('tmdb.tvlist_id3')
        self.tmdbtvlist4_link     = control.setting('tmdb.tvlist_id4')
        self.tmdbtvlist5_link     = control.setting('tmdb.tvlist_id5')
        self.tmdbtvlist6_link     = control.setting('tmdb.tvlist_id6')
        self.tmdbtvlist7_link     = control.setting('tmdb.tvlist_id7')
        self.tmdbtvlist8_link     = control.setting('tmdb.tvlist_id8')
        self.tmdbtvlist9_link     = control.setting('tmdb.tvlist_id9')
        self.tmdbtvlist10_link    = control.setting('tmdb.tvlist_id10')
        self.tmdbtvlist11_link    = control.setting('tmdb.tvlist_id11')
        self.tmdbtvlist12_link    = control.setting('tmdb.tvlist_id12')
        self.tmdbtvlist13_link    = control.setting('tmdb.tvlist_id13')
        self.tmdbtvlist14_link    = control.setting('tmdb.tvlist_id14')
        self.tmdbtvlist15_link    = control.setting('tmdb.tvlist_id15')
        self.tmdbtvlist16_link    = control.setting('tmdb.tvlist_id16')
        self.tmdbtvlist17_link    = control.setting('tmdb.tvlist_id17')
        self.tmdbtvlist18_link    = control.setting('tmdb.tvlist_id18')
        self.tmdbtvlist19_link    = control.setting('tmdb.tvlist_id19')
        self.tmdbtvlist20_link    = control.setting('tmdb.tvlist_id20')
        self.tmdbtvlist21_link    = control.setting('tmdb.tvlist_id21')
        self.tmdbtvlist22_link    = control.setting('tmdb.tvlist_id22')
        self.tmdbtvlist23_link    = control.setting('tmdb.tvlist_id23')
        self.tmdbtvlist24_link    = control.setting('tmdb.tvlist_id24')
        self.tmdbtvlist25_link    = control.setting('tmdb.tvlist_id25')
        self.tmdbtvlist26_link    = control.setting('tmdb.tvlist_id26')
        self.tmdbtvlist27_link    = control.setting('tmdb.tvlist_id27')
        self.tmdbtvlist28_link    = control.setting('tmdb.tvlist_id28')
        self.tmdbtvlist29_link    = control.setting('tmdb.tvlist_id29')
        self.tmdbtvlist30_link    = control.setting('tmdb.tvlist_id30')        
        self.mycustomlist1_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist1_link, self.tmdb_key)
        self.mycustomlist2_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist2_link, self.tmdb_key)
        self.mycustomlist3_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist3_link, self.tmdb_key)
        self.mycustomlist4_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist4_link, self.tmdb_key)
        self.mycustomlist5_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist5_link, self.tmdb_key)
        self.mycustomlist6_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist6_link, self.tmdb_key)
        self.mycustomlist7_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist7_link, self.tmdb_key)
        self.mycustomlist8_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist8_link, self.tmdb_key)
        self.mycustomlist9_link   = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist9_link, self.tmdb_key)
        self.mycustomlist10_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist10_link, self.tmdb_key)
        self.mycustomlist11_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist11_link, self.tmdb_key)
        self.mycustomlist12_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist12_link, self.tmdb_key)
        self.mycustomlist13_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist13_link, self.tmdb_key)
        self.mycustomlist14_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist14_link, self.tmdb_key)
        self.mycustomlist15_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist15_link, self.tmdb_key)
        self.mycustomlist16_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist16_link, self.tmdb_key)
        self.mycustomlist17_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist17_link, self.tmdb_key)
        self.mycustomlist18_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist18_link, self.tmdb_key)
        self.mycustomlist19_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist19_link, self.tmdb_key)
        self.mycustomlist20_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist20_link, self.tmdb_key)
        self.mycustomlist21_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist21_link, self.tmdb_key)
        self.mycustomlist22_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist22_link, self.tmdb_key)
        self.mycustomlist23_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist23_link, self.tmdb_key)
        self.mycustomlist24_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist24_link, self.tmdb_key)
        self.mycustomlist25_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist25_link, self.tmdb_key)
        self.mycustomlist26_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist26_link, self.tmdb_key)
        self.mycustomlist27_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist27_link, self.tmdb_key)
        self.mycustomlist28_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist28_link, self.tmdb_key)
        self.mycustomlist29_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist29_link, self.tmdb_key)
        self.mycustomlist30_link  = 'http://api.themoviedb.org/3/list/%s?api_key=%s' % (self.tmdbtvlist30_link, self.tmdb_key)        
        self.tmdbblast_link = 'http://api.themoviedb.org/3/list/37592?api_key=%s' % (self.tmdb_key)
        self.tmdbdatenighttv_link = 'http://api.themoviedb.org/3/list/48293?api_key=%s' % (self.tmdb_key)
        self.tmdbfasttv_link = 'http://api.themoviedb.org/3/list/38851?api_key=%s' % (self.tmdb_key)
        self.tmdbsouthptv_link = 'http://api.themoviedb.org/3/list/47436?api_key=%s' % (self.tmdb_key)
        self.tmdbchitv_link = 'http://api.themoviedb.org/3/list/48222?api_key=%s' % (self.tmdb_key)
        self.tmdbhulutv_link = 'http://api.themoviedb.org/3/list/47716?api_key=%s' % (self.tmdb_key)
        self.tmdbnettv_link = 'http://api.themoviedb.org/3/list/47713?api_key=%s' % (self.tmdb_key)
        self.tmdbsportstv_link = 'http://api.themoviedb.org/3/list/48225?api_key=%s' % (self.tmdb_key)
        self.tmdbspotlighttv_link = 'http://api.themoviedb.org/3/list/13427?api_key=%s' % (self.tmdb_key)
        self.tmdbufotv_link = 'http://api.themoviedb.org/3/list/13388?api_key=%s' % (self.tmdb_key)
        self.tmdbamaztv_link = 'http://api.themoviedb.org/3/list/47714?api_key=%s' % (self.tmdb_key)
        self.tmdb420tv_link = 'http://api.themoviedb.org/3/list/36782?api_key=%s' % (self.tmdb_key)
        self.tmdbtats_link = 'http://api.themoviedb.org/3/list/47871?api_key=%s' % (self.tmdb_key)
        self.tmdblmao_link = 'http://api.themoviedb.org/3/list/48274?api_key=%s' % (self.tmdb_key)
        self.tmdbelimination_link = 'http://api.themoviedb.org/3/list/13391?api_key=%s' % (self.tmdb_key)
        self.tmdbcooking_link = 'http://api.themoviedb.org/3/list/47877?api_key=%s' % (self.tmdb_key)
        self.tmdbgamers_link = 'http://api.themoviedb.org/3/list/47880?api_key=%s' % (self.tmdb_key)
        self.tmdbcartoon_link = 'http://api.themoviedb.org/3/list/13467?api_key=%s' % (self.tmdb_key)
        self.tmdblittle_link = 'http://api.themoviedb.org/3/list/13564?api_key=%s' % (self.tmdb_key)
        self.tmdbkids_link = 'http://api.themoviedb.org/3/list/13555?api_key=%s' % (self.tmdb_key)
        self.tmdbanimationtv_link = 'http://api.themoviedb.org/3/list/13573?api_key=%s' % (self.tmdb_key)

    def get(self, url, idx=True):
        try:
            try: url = getattr(self, url + '_link')
            except: pass
            try: u = urlparse.urlparse(url).netloc.lower()
            except: pass
            if u in self.tmdb_link and ('/user/' in url or '/list/' in url):
                self.list = self.tmdb_custom_list(url)
                self.worker()
            elif u in self.tmdb_link and not ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.tmdb_list, 24, url)
                # print ("LISTS TMDB", self.list)
                self.worker()
            elif u in self.trakt_link and '/users/' in url:
                try:
                    if not '/users/me/' in url: raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user): raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)
                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))
                if idx == True: self.worker()
            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True: self.worker(level=0)
            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True: self.worker()
            if idx == True: self.tvshowDirectory(self.list)
            return self.list
        except:
            pass

    def similar_shows(self, imdb):
        url = '%s?action=get_similar_shows&imdb=%s' % (sys.argv[0], imdb)
        control.execute('Container.Update(%s)' % url)

    def get_similar_shows(self, imdb):
                self.list = []
                try:
                    imdb_page = "http://www.imdb.com/title/%s/" % imdb
                    r = OPEN_URL(imdb_page).content
                    r = client.parseDOM(r, 'div', attrs = {'class': 'rec_item'})[:20]
                except:
                    return
                for u in r:
                        
                        imdb = client.parseDOM(u, 'a', ret='href')[0]
                        imdb = imdb.encode('utf-8')
                        imdb = re.findall('/tt(\d+)/', imdb)[0]
                        imdb = imdb.encode('utf-8')
                        if imdb == '0' or imdb == None or imdb == '': raise Exception()
                        imdb = 'tt' + imdb
                        try:
                            url_tmdb = self.tmdb_by_query_imdb % imdb
                            if not len(self.list) >= 40:
                                self.list = cache.get(self.tmdb_similar_list, 720, url_tmdb, imdb)
                        except:
                            pass
                self.list = self.list[:40]
                self.no_suggestions_Dir(self.list)

    def tmdb_similar_list(self, url,imdb):
        result = OPEN_URL(url).content
        result = json.loads(result)
        item = result['tv_results'][0]
        next = ''
        # print "TMDB STARTING ITEMS"
        try:
                title = item['name']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['first_air_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                tmdb = item['id']
                if tmdb == '' or tmdb == None: tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                tvdb = '0'
                poster = item['poster_path']
                if poster == '' or poster == None: poster = '0'
                else: poster = self.tmdb_poster + poster
                poster = poster.encode('utf-8')
                # print "TMDB %s" % poster
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None: fanart = '0'
                if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                # print "TMDB %s" % fanart
                premiered = item['first_air_date']
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')
                # print "TMDB %s" % premiered
                rating = str(item['vote_average'])
                if rating == '' or rating == None: rating = '0'
                rating = rating.encode('utf-8')
                # print "TMDB %s" % rating
                votes = str(item['vote_count'])
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == '' or votes == None: votes = '0'
                votes = votes.encode('utf-8')
                # print "TMDB %s" % votes
                plot = item['overview']
                if plot == '' or plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                # print "TMDB %s" % plot
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': '0', 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
        except:
                pass
        return self.list

    def tmdb_list(self, url):
        next = url
        result = client.request(url)
        result = json.loads(result)
        items = result['results']
        # print "TMDB RESULTS %s" % items
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total: raise Exception()
            url2 = '%s&page=%s' % (url.split('&page=', 1)[0], str(page+1))
            result = client.request(url2 % self.tmdb_key)
            result = json.loads(result)
            items += result['results']
        except:
            pass
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total: raise Exception()
            if not 'page=' in url: raise Exception()
            next = '%s&page=%s' % (next.split('&page=', 1)[0], str(page+1))
            next = next.encode('utf-8')
        except:
            next = ''
        # print "TMDB STARTING ITEMS"
        for item in items:
            try:
                title = item['name']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                # print "TMDB %s" % title
                year = item['first_air_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                # print "TMDB %s" % year
                tmdb = item['id']
                if tmdb == '' or tmdb == None: tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                # print "TMDB %s" % tmdb
                imdb = '0'
                tvdb = '0'
                poster = item['poster_path']
                if poster == '' or poster == None: poster = '0'
                else: poster = self.tmdb_poster + poster
                poster = poster.encode('utf-8')
                # print "TMDB %s" % poster
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None: fanart = '0'
                if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                # print "TMDB %s" % fanart
                premiered = item['first_air_date']
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')
                # print "TMDB %s" % premiered
                rating = str(item['vote_average'])
                if rating == '' or rating == None: rating = '0'
                rating = rating.encode('utf-8')
                # print "TMDB %s" % rating
                votes = str(item['vote_count'])
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == '' or votes == None: votes = '0'
                votes = votes.encode('utf-8')
                # print "TMDB %s" % votes
                plot = item['overview']
                if plot == '' or plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                # print "TMDB %s" % plot
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass
                # print "TMDB TV SHOWS LIST %s %s %s" % (title,year,premiered)
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': '0', 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
                # print self.list
            except:
                pass
        return self.list

    def tmdb_custom_list(self, url):
        result = client.request(url)
        result = json.loads(result)
        items = result['items']
        # print "TMDB RESULTS %s" % items
        next = ''
        # print "TMDB STARTING ITEMS"
        for item in items:
            try:
                title = item['name']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                # print "TMDB %s" % title
                year = item['first_air_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                # print "TMDB %s" % year
                tmdb = item['id']
                if tmdb == '' or tmdb == None: tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                # print "TMDB %s" % tmdb
                imdb = '0'
                tvdb = '0'
                poster = item['poster_path']
                if poster == '' or poster == None: poster = '0'
                else: poster = self.tmdb_poster + poster
                poster = poster.encode('utf-8')
                # print "TMDB %s" % poster
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None: fanart = '0'
                if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                # print "TMDB %s" % fanart
                premiered = item['first_air_date']
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')
                # print "TMDB %s" % premiered
                rating = str(item['vote_average'])
                if rating == '' or rating == None: rating = '0'
                rating = rating.encode('utf-8')
                # print "TMDB %s" % rating
                votes = str(item['vote_count'])
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == '' or votes == None: votes = '0'
                votes = votes.encode('utf-8')
                # print "TMDB %s" % votes
                plot = item['overview']
                if plot == '' or plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                # print "TMDB %s" % plot
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass
                print "TMDB TV SHOWS LIST %s %s %s" % (title,year,premiered)
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': '0', 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
                # print self.list
            except:
                pass
        return self.list

    def search(self):
        try:
            control.idle()
            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            q = k.getText() if k.isConfirmed() else None
            if (q == None or q == ''): return
            url = 'http://api.themoviedb.org/3/search/tv?&api_key=%s&query=%s'  % (self.tmdb_key, urllib.quote_plus(q))
            url = '%s?action=tvshows&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            control.execute('Container.Update(%s)' % url)
        except:
            return

    def years(self):
        year = (self.datetime.strftime('%Y'))
        for i in range(int(year)-0, int(year)-50, -1): self.list.append({'name': str(i), 'url': self.year_link % ('%s', str(i)), 'image': 'years.jpg', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def person(self):
        try:
            control.idle()
            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            q = k.getText() if k.isConfirmed() else None
            if (q == None or q == ''): return
            url = self.persons_link + urllib.quote_plus(q)
            url = '%s?action=tvPersons&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            control.execute('Container.Update(%s)' % url)
        except:
            return

    # def genres(self):
        # genres = [
        # ('Action', 'action'),
        # ('Adventure', 'adventure'),
        # ('Animation', 'animation'),
        # ('Biography', 'biography'),
        # ('Comedy', 'comedy'),
        # ('Crime', 'crime'),
        # ('Drama', 'drama'),
        # ('Family', 'family'),
        # ('Fantasy', 'fantasy'),
        # ('Game-Show', 'game_show'),
        # ('History', 'history'),
        # ('Horror', 'horror'),
        # ('Music ', 'music'),
        # ('Musical', 'musical'),
        # ('Mystery', 'mystery'),
        # ('News', 'news'),
        # ('Reality-TV', 'reality_tv'),
        # ('Romance', 'romance'),
        # ('Science Fiction', 'sci_fi'),
        # ('Sport', 'sport'),
        # ('Talk-Show', 'talk_show'),
        # ('Thriller', 'thriller'),
        # ('War', 'war'),
        # ('Western', 'western')
        # ]
        # for i in genres: self.list.append({'name': cleangenre.lang(i[0], self.lang), 'url': self.genre_link % i[1], 'image': 'tvboxsets.png', 'action': 'tvshows'})
        # self.addDirectory(self.list)
        # return self.list

    def genres(self):
        try:
            url = self.genres_link
            # url = re.sub('language=(fi|hr|no)', '', url)
            self.list = cache.get(self.tmdb_genre_list, 24, url)
            # print "TMDB GENERES %s" % self.list
            for i in range(0, len(self.list)): self.list[i].update({'image': 'tvboxsets.png', 'action': 'tvshows'})
            self.addDirectory(self.list)
            return self.list
        except:
            return

    def tmdb_genre_list(self, url):
        try:
            result = client.request(url)
            result = json.loads(result)
            items = result['genres']
        except:
            return
        for item in items:
            try:
                name = item['name']
                name = name.encode('utf-8')
                id = item['id']
                url = 'http://api.themoviedb.org/3/discover/tv?api_key=%s&with_genres=%s&primary_release_date.gte=date&page=1' %(self.tmdb_key,id)
                # print "TMDB GENERES PASSED LINKS %s" %url
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url})
            except:
                pass
        return self.list

    def networks(self):
        networks = [
        ('A&E', '129|567|891'), ('ABC', '2'), ('ABC Family', '75'), ('Amazon', '1024'), ('AMC', '174'), ('Animal Planet', '91'), ('AT-X', '173'), ('Bravo', '74|312|485'), ('Boomerang', '523'), ('Cartoon Network', '56|217|262'), ('CBBC', '15|104'),
        ('CBS', '16'), ('CBEEBIES', '166'), ('Cinemax', '359'), ('CITV', '112'), ('CNBC', '175'), ('CNN', '59'), ('Comedy Central', '47|278'), ('CW', '71|194'), ('Destination America', '625'), ('Discovery Channel', '64|106|755'),
        ('Discovery ID', '244'), ('Disney Channel', '54|515|539|730|1531'), ('Disney XD', '44'), ('Disney Junior', '281|497'), ('DIY', '625'), ('E! Entertainment', '76|407|645'), ('Fox', '303'), ('FX', '88'),
        ('FYI', '1080'), ('FOX', '19'), ('HBO', '49'), ('HGTV', '210|482'), ('Hallmark', '384'), ('History Channel', '65|238|893'), ('Hulu', '453'), ('ITV', '9'), ('Investigation Discovery', '244'),  
        ('Lifetime', '34|892'), ('MTV', '33|335|488'), ('NBC', '6|582'), ('National Geographic', '43|799'), ('Netflix', '213'), ('Nickelodeon', '13|35|234|259|416'), ('Nick Toons', '628|224'), ('PBS', '14'), ('Showtime', '67|643'), ('Spike', '55'),
        ('Starz', '318'), ('Syfy', '77|586'), ('TBS', '68'), ('The Lifestyle Channel', '683'),  ('The Movie Network', '245'), ('TLC', '84'), ('TNT', '41|613|939'), ('Travel Channel', '209'), ('TV Land', '397'),
        ('USA', '30'), ('VH1', '158'), ('Velocity', '435'), ('WWE', '1025')]
        for i in networks: self.list.append({'name': i[0], 'url': self.network_link % (i[1]), 'image': 'networks.jpg', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def certifications(self):
        certificates = ['TV-G', 'TV-PG', 'TV-14', 'TV-MA']
        for i in certificates: self.list.append({'name': str(i), 'url': self.certification_link % str(i).replace('-', '_').lower(), 'image': 'certificates.jpg', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 0, url)
        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            activity = trakt.getActivity()
        except:
            pass
        try:
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '': raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass
        self.list = userlists
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists.jpg', 'action': 'tvshows'})
        self.addDirectory(self.list)
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
                try: items.append(i['show'])
                except: pass
            if len(items) == 0:
                items = result
        except:
            return
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            if not int(q['limit']) == len(items): raise Exception()
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
                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()
                imdb = item['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0'
                else: imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')
                tvdb = item['ids']['tvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')
                if tvdb == None or tvdb == '' or tvdb in dupes: raise Exception()
                dupes.append(tvdb)
                poster = '0'
                try: poster = item['images']['poster']['medium']
                except: pass
                if poster == None or not '/posters/' in poster: poster = '0'
                poster = poster.rsplit('?', 1)[0]
                poster = poster.encode('utf-8')
                banner = poster
                try: banner = item['images']['banner']['full']
                except: pass
                if banner == None or not '/banners/' in banner: banner = '0'
                banner = banner.rsplit('?', 1)[0]
                banner = banner.encode('utf-8')
                fanart = '0'
                try: fanart = item['images']['fanart']['full']
                except: pass
                if fanart == None or not '/fanarts/' in fanart: fanart = '0'
                fanart = fanart.rsplit('?', 1)[0]
                fanart = fanart.encode('utf-8')
                try: premiered = item['first_aired']
                except: premiered = '0'
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')
                try: studio = item['network']
                except: studio = '0'
                if studio == None: studio = '0'
                studio = studio.encode('utf-8')
                try: genre = item['genres']
                except: genre = '0'
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')
                try: duration = str(item['runtime'])
                except: duration = '0'
                if duration == None: duration = '0'
                duration = duration.encode('utf-8')
                try: rating = str(item['rating'])
                except: rating = '0'
                if rating == None or rating == '0.0': rating = '0'
                rating = rating.encode('utf-8')
                try: votes = str(item['votes'])
                except: votes = '0'
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == None: votes = '0'
                votes = votes.encode('utf-8')
                try: mpaa = item['certification']
                except: mpaa = '0'
                if mpaa == None: mpaa = '0'
                mpaa = mpaa.encode('utf-8')
                try: plot = item['overview']
                except: plot = '0'
                if plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': '0', 'plot': plot, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': tvdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list

    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            pass
        for item in items:
            try:
                try: name = item['list']['name']
                except: name = item['name']
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                try: url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except: url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass
        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
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
                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()
                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')
                if imdb in dupes: raise Exception()
                dupes.append(imdb)
                try: poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except: poster = '0'
                poster = re.sub('(?:_SX\d+?|)(?:_SY\d+?|)(?:_UX\d+?|)_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
                rating = '0'
                try: rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
                except: pass
                try: rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
                except: rating = '0'
                try: rating = client.parseDOM(item, 'div', ret='data-value', attrs = {'class': '.*?imdb-rating'})[0]
                except: pass
                if rating == '' or rating == '-': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')
                plot = '0'
                try: plot = client.parseDOM(item, 'p', attrs = {'class': 'text-muted'})[0]
                except: pass
                try: plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                except: pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': '0', 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': '0', 'mpaa': '0', 'cast': '0', 'plot': plot, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': '0', 'next': next})
            except:
                pass
        return self.list

    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'tr', attrs = {'class': '.+? detailed'})
        except:
            return
        for item in items:
            try:
                name = client.parseDOM(item, 'a', ret='title')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = client.parseDOM(item, 'img', ret='src')[0]
                if not ('._SX' in image or '._SY' in image): raise Exception()
                image = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass
        return self.list

    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'div', attrs = {'class': 'list_name'})
        except:
            pass
        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].replace('/', '')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass
        self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a )', '', k['name'].lower()))
        return self.list

    def worker(self):
        self.meta = []
        total = len(self.list)
        for i in range(0, total): self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.lang)
        for r in range(0, total, 40):
            threads = []
            for i in range(r, r+40):
                if i <= total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            if len(self.meta) > 0: metacache.insert(self.meta)
        self.list = [i for i in self.list]

    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()
            # print "TMDB SUPERINFO GOGO"
            try: tmdb = self.list[i]['tmdb']
            except: tmdb = '0'
            if not tmdb == '0': url = self.tmdb_info_link % tmdb
            else: raise Exception()
            # print "SUPERINFO %s" % url
            item = client.request(url, timeout='20')
            item = json.loads(item)
            # print "SELFMETA ITEM %s" % item
            title = item['name']
            if not title == '0': self.list[i].update({'title': title})
            # print "SELFMETA title %s" % title
            year = item['first_air_date']
            try: year = re.compile('(\d{4})').findall(year)[0]
            except: year = '0'
            if year == '' or year == None: year = '0'
            year = year.encode('utf-8')
            if not year == '0': self.list[i].update({'year': year})
            # print "SELFMETA year %s" % year
            tmdb = item['id']
            if tmdb == '' or tmdb == None: tmdb = '0'
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            if not tmdb == '0': self.list[i].update({'tmdb': tmdb})
            tvdb = item['external_ids']['tvdb_id']
            if tvdb == '' or tvdb == None: tvdb = '0'
            tvdb = re.sub('[^0-9]', '', str(tvdb))
            tvdb = tvdb.encode('utf-8')
            if not tvdb == '0': self.list[i].update({'tvdb': tvdb})
            # print "SELFMETA tvdb %s" % tvdb
            imdb = item['external_ids']['imdb_id']
            if imdb == '' or imdb == None: imdb = '0'
            if not imdb == '0': self.list[i].update({'imdb': imdb})
            # print "SELFMETA imdb %s" % imdb
            if not imdb == '0': url = self.imdb_by_query % imdb
            # print "IMDB INFOS %s" % url
            item2 = client.request(url, timeout='10')
            item2 = json.loads(item2)
            ######## IMDB INFOS #######
            duration = item['episode_run_time']
            try: 
                duration = str(duration)
                duration = duration.split(",")
                duration = duration[0]
                # print "SPLITTED DURATION %s" % duration
            except:
                pass
            duration = re.sub('[^0-9]', '', str(duration))
            # print "SPLITTED DURATION %s" % duration
            if duration == None or duration == '' or duration == 'N/A': duration = '0'
            if not duration == '0': self.list[i].update({'duration': duration})
            premiered = item2['Released']
            if premiered == None or premiered == '' or premiered == 'N/A': premiered = '0'
            premiered = re.findall('(\d*) (.+?) (\d*)', premiered)
            try: premiered = '%s-%s-%s' % (premiered[0][2], {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}[premiered[0][1]], premiered[0][0])
            except: premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})
            rating = item2['imdbRating']
            if rating == None or rating == '' or rating == 'N/A' or rating == '0.0': rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})
            votes = item2['imdbVotes']
            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == None or votes == '' or votes == 'N/A': votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})
            mpaa = item2['Rated']
            if mpaa == None or mpaa == '' or mpaa == 'N/A': mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})
            director = item2['Director']
            if director == None or director == '' or director == 'N/A': director = '0'
            director = director.replace(', ', ' / ')
            director = re.sub(r'\(.*?\)', '', director)
            director = ' '.join(director.split())
            director = director.encode('utf-8')
            if not director == '0': self.list[i].update({'director': director})
            writer = item2['Writer']
            if writer == None or writer == '' or writer == 'N/A': writer = '0'
            writer = writer.replace(', ', ' / ')
            writer = re.sub(r'\(.*?\)', '', writer)
            writer = ' '.join(writer.split())
            writer = writer.encode('utf-8')
            if not writer == '0': self.list[i].update({'writer': writer})
            cast = item2['Actors']
            if cast == None or cast == '' or cast == 'N/A': cast = '0'
            cast = [x.strip() for x in cast.split(',') if not x == '']
            try: cast = [(x.encode('utf-8'), '') for x in cast]
            except: cast = []
            if cast == []: cast = '0'
            if not cast == '0': self.list[i].update({'cast': cast})
            plot = item2['Plot']
            if plot == None or plot == '' or plot == 'N/A': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})
            #### END IMDB INFOS #######    
            # print "SELFMETA IMDB TMDB TVDB %s %s %s" % (imdb,tmdb,tvdb)
            poster = item['poster_path']
            if poster == '' or poster == None: poster = '0'
            if not poster == '0': poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})
            # print "SELFMETA poster %s " % poster
            fanart = item['backdrop_path']
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = self.tmdb_image + fanart
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.list[i]['fanart'] == '0': self.list[i].update({'fanart': fanart})
            # print "SELFMETA fanart %s " % fanart
            studio = item['networks']
            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})
            # print "SELFMETA studio %s " % studio
            genre = item['genres']
            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})
            # print "SELFMETA genre %s " % genre
            tagline = '0'
            if not tagline == '0': self.list[i].update({'tagline': tagline})
            self.meta.append({'tmdb': tmdb, 'imdb': imdb, 'tvdb': tvdb, 'lang': 'en', 'item': {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}})
            # print "SELFMETA %s" % self.meta
        except:
            pass

    def favourites(self):
        try:
            items = favourites.getFavourites('tvshows')
            self.list = [i[1] for i in items]
            for i in self.list:
                # print "ZEEEEN SELF LIST %s" %i
                if not 'name' in i: i['name'] = '%s (%s)' % (i['title'], i['year'])
                try: i['title'] = i['title'].encode('utf-8')
                except: pass
                try: i['name'] = i['name'].encode('utf-8')
                except: pass
                if not 'duration' in i: i['duration'] = '0'
                if not 'imdb' in i: i['imdb'] = '0'
                if not 'tmdb' in i: i['tmdb'] = '0'
                if not 'tvdb' in i: i['tvdb'] = '0'
                if not 'tvrage' in i: i['tvrage'] = '0'
                if not 'poster' in i: i['poster'] = '0'
                if not 'banner' in i: i['banner'] = '0'
                if not 'fanart' in i: i['fanart'] = '0'
            self.worker()
            self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a )', '', k['title'].lower()))       
            self.tvshowDirectory(self.list)
        except:
            return

    def tvshowDirectory(self, items):
        if items == None or len(items) == 0: control.idle() ; sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()
        try: isOld = False ; control.item().getArt('type')
        except: isOld = True
        isEstuary = True if 'estuary' in control.skin else False
        indicators = playcount.getTVShowIndicators(refresh=True) if action == 'tvshows' else playcount.getTVShowIndicators()
        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')
        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        for i in items:
            try:
                if not 'originaltitle' in i: i['originaltitle'] = '%s' %(i['title'])
                label = '%s' % (i['title'])
                systitle = sysname = urllib.quote_plus(i['originaltitle'])
                sysimage = urllib.quote_plus(i['poster'])
                imdb, tvdb, title, year = i['imdb'].encode('utf-8'), i['tvdb'].encode('utf-8'), i['title'].encode('utf-8'), i['year'].encode('utf-8')
                title = i['originaltitle'].encode('utf-8')
                tmdb = i['tmdb'].encode('utf-8')
                poster, banner, fanart = i['poster'], i['banner'], i['fanart']
                if banner == '0' and not fanart == '0': banner = fanart
                elif banner == '0' and not poster == '0': banner = poster
                if poster == '0': poster = addonPoster
                if banner == '0': banner = addonBanner
                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'mediatype': 'tvshow'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                try: meta.update({'imdb': str(imdb)})
                except: pass
                try: meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except: pass
                if isEstuary == True:
                    try: del meta['cast']
                    except: pass
                try:
                    overlay = int(playcount.getTVShowOverlay(indicators, tvdb))
                    if overlay == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                try:
                    localwatched = control.setting('local.watched')
                    if not localwatched == 'true': raise Exception()
                    overlay = playcount.getShowLocalIndicator(imdb)
                    if '7' in overlay: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                sysmeta = urllib.quote_plus(json.dumps(meta))
                if not tvdb == "0" or tvdb == None: sysmetalliq = "plugin://plugin.video.metalliq-forqed/tv/add_to_library_parsed/%s/direct.bkr.cdtv" % tvdb
                elif "tt" in imdb: sysmetalliq = "plugin://plugin.video.metalliq-forqed/tv/add_to_library_parsed/%s/direct.bkr.cdtv" % imdb
                else: sysmetalliq = "0"
                url = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s&tmdb=%s' % (sysaddon, systitle, year, imdb, tvdb,tmdb)
                cm = []
                cm.append(('Trailer', 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, sysname)))
                if "tt" in imdb:  cm.append(('People Also Liked...', 'RunPlugin(%s?action=similar_shows&imdb=%s)' % (sysaddon, imdb)))                    
                if not action == 'tvFavourites':cm.append(('Add to Watchlist', 'RunPlugin(%s?action=addFavourite&meta=%s&content=tvshows)' % (sysaddon, sysmeta)))
                if action == 'tvFavourites': cm.append(('Remove From Watchlist', 'RunPlugin(%s?action=deleteFavourite&meta=%s&content=tvshows)' % (sysaddon, sysmeta)))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                cm.append((watchedMenu, 'RunPlugin(%s?action=tvPlaycountShow&name=%s&imdb=%s&tvdb=%s&query=7)' % (sysaddon, systitle, imdb, tvdb)))
                cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvPlaycountShow&name=%s&imdb=%s&tvdb=%s&query=6)' % (sysaddon, systitle, imdb, tvdb)))
                if not sysmetalliq == '0' or sysmetalliq == None:cm.append(('Add To Library', 'RunPlugin(%s)' % (sysmetalliq)))
                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&tvdb=%s&content=tvshow)' % (sysaddon, sysname, tvdb)))
                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))
                item = control.item(label=label)
                item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels = meta)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass
        try:
            url = items[0]['next']
            if url == '': raise Exception()
            icon = control.addonNext()
            url = '%s?action=tvshowPage&url=%s' % (sysaddon, urllib.quote_plus(url))
            item = control.item(label=nextMenu)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'tvshow.poster': icon, 'season.poster': icon, 'banner': icon, 'tvshow.banner': icon, 'season.banner': icon})
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass
        control.content(syshandle, 'tvshows')
        # control.do_block_check(False)
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.confluence': 500})

    def no_suggestions_Dir(self, items):
        if items == None or len(items) == 0: control.idle() ; sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()
        try: isOld = False ; control.item().getArt('type')
        except: isOld = True
        isEstuary = True if 'estuary' in control.skin else False
        indicators = playcount.getTVShowIndicators(refresh=True) if action == 'tvshows' else playcount.getTVShowIndicators()
        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')
        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        for i in items:
            try:
                if not 'originaltitle' in i: i['originaltitle'] = '%s' %(i['title'])
                label = '%s' % (i['title'])
                systitle = sysname = urllib.quote_plus(i['originaltitle'])
                sysimage = urllib.quote_plus(i['poster'])
                imdb, tvdb, title, year = i['imdb'], i['tvdb'], i['title'], i['year']
                title = i['originaltitle']
                tmdb = i['tmdb']
                poster, banner, fanart = i['poster'], i['banner'], i['fanart']
                if banner == '0' and not fanart == '0': banner = fanart
                elif banner == '0' and not poster == '0': banner = poster
                if poster == '0': poster = addonPoster
                if banner == '0': banner = addonBanner
                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'mediatype': 'tvshow'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})
                if i['duration'] == '0': meta.update({'duration': '60'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                try: meta.update({'imdb': str(imdb)})
                except: pass
                try: meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except: pass
                if isEstuary == True:
                    try: del meta['cast']
                    except: pass
                try:
                    overlay = int(playcount.getTVShowOverlay(indicators, tvdb))
                    if overlay == 7: meta.update({'playcount': 1, 'overlay': 7})
                    else: meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                sysmeta = urllib.quote_plus(json.dumps(meta))
                if not tvdb == "0" or tvdb == None: sysmetalliq = "plugin://plugin.video.metalliq-forqed/tv/add_to_library_parsed/%s/direct.bkr.cdtv" % tvdb
                else: sysmetalliq = "0"
                url = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s&tmdb=%s' % (sysaddon, systitle, year, imdb, tvdb,tmdb)
                cm = []
                cm.append(('Trailer', 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, sysname)))
                if not action == 'tvFavourites':cm.append(('Add to Watchlist', 'RunPlugin(%s?action=addFavourite&meta=%s&content=tvshows)' % (sysaddon, sysmeta)))
                if action == 'tvFavourites': cm.append(('Remove From Watchlist', 'RunPlugin(%s?action=deleteFavourite&meta=%s&content=tvshows)' % (sysaddon, sysmeta)))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                cm.append((watchedMenu, 'RunPlugin(%s?action=tvPlaycountShow&name=%s&imdb=%s&tvdb=%s&query=7)' % (sysaddon, systitle, imdb, tvdb)))
                cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvPlaycountShow&name=%s&imdb=%s&tvdb=%s&query=6)' % (sysaddon, systitle, imdb, tvdb)))
                if not sysmetalliq == '0' or sysmetalliq == None:cm.append(('Add To Library', 'RunPlugin(%s)' % (sysmetalliq)))
                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&tvdb=%s&content=tvshow)' % (sysaddon, sysname, tvdb)))
                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))
                item = control.item(label=label)
                item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                if settingFanart == 'true' and not fanart == '0':
                    item.setProperty('Fanart_Image', fanart)
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels = meta)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass
        try:
            url = items[0]['next']
            if url == '': raise Exception()
            icon = control.addonNext()
            url = '%s?action=tvshowPage&url=%s' % (sysaddon, urllib.quote_plus(url))
            item = control.item(label=nextMenu)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'tvshow.poster': icon, 'season.poster': icon, 'banner': icon, 'tvshow.banner': icon, 'season.banner': icon})
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass
        control.content(syshandle, 'tvshows')
        # control.do_block_check(False)
        control.directory(syshandle, cacheToDisc=True)
        views.setView('tvshows', {'skin.confluence': 500})

    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0: control.idle() ; sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()
        queueMenu = control.lang(32065).encode('utf-8')
        for i in items:
            try:
                name = i['name']
                if i['image'].startswith('http://'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb
                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass
                cm = []
                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                item = control.item(label=name)
                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass
        # control.do_block_check(False)
        control.directory(syshandle, cacheToDisc=True)
