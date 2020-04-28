# -*- coding: utf-8 -*-

import os,sys,re,json,urllib,urlparse,datetime,xbmc
from resources.lib.modules import cleantitle,cleangenre,client,control,views,trakt
from resources.lib.modules import cache,metacache,playcount,utils,workers
from resources.lib.indexers import navigator

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', ''))) if len(sys.argv) > 1 else dict()
action = params.get('action')
control.moderator()


class movies:
    def __init__(self):
        self.list = []
        self.imdb_link = 'https://www.imdb.com'
        self.trakt_link = 'https://api.trakt.tv'
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.year_date = (self.datetime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tm_user = control.setting('tm.user')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))
        self.lang = control.apiLanguage()['trakt']
        self.hidecinema = control.setting('hidecinema')
        self.month_date = (self.datetime - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        self.hidecinema_rollback = int(control.setting('hidecinema.rollback'))
        self.hidecinema_rollback2 = self.hidecinema_rollback * 30
        self.hidecinema_date = (datetime.date.today() - datetime.timedelta(days = self.hidecinema_rollback2)).strftime('%Y-%m')

        self.search_link = 'https://api.trakt.tv/search/movie?limit=20&page=1&query='
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/movies/%s'
        self.fanart_tv_level_link = 'http://webservice.fanart.tv/v3/level'
        self.tm_art_link = 'https://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % ('%s', self.tm_user, self.lang)
        self.tm_img_link = 'http://image.tmdb.org/t/p/w%s%s'
        self.persons_link = 'https://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'https://www.imdb.com/search/name?count=100&gender=male,female'
        self.person_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&role=%s&sort=year,desc&count=40&start=1'
        self.keyword_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.oscars_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=40&start=1'
        self.year_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=40&start=1'

        self.theaters_link = 'https://www.imdb.com/showtimes/location?ref_=inth_ov_sh_sm'
        self.theatersOld_link = 'https://www.imdb.com/search/title?title_type=feature&num_votes=1000,&countries=us&languages=en&release_date=date[90],date[0]&sort=release_date,desc&count=40&start=1'
        self.onDeckMovies_link = 'https://api.trakt.tv/sync/playback/movies?extended=full&limit=40'
        if self.hidecinema == 'true':
            self.popular_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&release_date=,%s&sort=moviemeter,asc&count=40&start=1' % (self.hidecinema_date)
            self.views_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&release_date=,%s&count=40&start=1' % (self.hidecinema_date)
            self.featured_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=,%s&sort=moviemeter,asc&count=40&start=1' % (self.hidecinema_date)
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,%s&genres=%s&sort=moviemeter,asc&count=40&start=1' % (self.hidecinema_date, '%s')
            self.language_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&release_date=,%s&count=40&start=1' % ('%s', self.hidecinema_date)
            self.certification_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=us:%s&sort=moviemeter,asc&release_date=,%s&count=40&start=1' % ('%s', self.hidecinema_date)
            self.boxoffice_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&release_date=,%s&count=40&start=1' % (self.hidecinema_date)
        else:
            self.popular_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=40&start=1'
            self.views_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=40&start=1'
            self.featured_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=date[365],date[60]&sort=moviemeter,asc&count=40&start=1'
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=40&start=1'
            self.language_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
            self.certification_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=us:%s&sort=moviemeter,asc&count=40&start=1'
            self.boxoffice_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&count=40&start=1'

        self.added_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&languages=en&num_votes=500,&production_status=released&release_date=%s,%s&sort=release_date,desc&count=20&start=1' % (self.year_date, self.today_date)
        self.traktlists_link = 'https://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'https://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'https://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'https://api.trakt.tv/users/me/collection/movies'
        self.traktwatchlist_link = 'https://api.trakt.tv/users/me/watchlist/movies'
        self.traktfeatured_link = 'https://api.trakt.tv/recommendations/movies?limit=40'
        self.traktanticipated_link = 'https://api.trakt.tv/movies/anticipated?limit=40&page=1'
        self.trending_link = 'https://api.trakt.tv/movies/trending?limit=40&page=1'
        self.traktpopular_link = 'https://api.trakt.tv/movies/popular?limit=40&page=1'
        self.traktboxoffice_link = 'https://api.trakt.tv/movies/boxoffice?limit=40&page=1'
        self.trakthistory_link = 'https://api.trakt.tv/users/me/history/movies?limit=40&page=1'

        self.imdblists_link = 'https://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'https://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdblist2_link = 'https://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=movie,tvMovie&start=1'
        self.imdbwatchlist_link = 'https://www.imdb.com/user/ur%s/watchlist/?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'https://www.imdb.com/user/ur%s/watchlist/?sort=date_added,desc' % self.imdb_user

        self.update_link = 'https://api.trakt.tv/movies/updates/%s?limit=40&page=1'
        self.played1_link = 'https://api.trakt.tv/movies/played/weekly?limit=40&page=1'
        self.played2_link = 'https://api.trakt.tv/movies/played/monthly?limit=40&page=1'
        self.played3_link = 'https://api.trakt.tv/movies/played/yearly?limit=40&page=1'
        self.played4_link = 'https://api.trakt.tv/movies/played/all?limit=40&page=1'
        self.collected1_link = 'https://api.trakt.tv/movies/collected/weekly?limit=40&page=1'
        self.collected2_link = 'https://api.trakt.tv/movies/collected/monthly?limit=40&page=1'
        self.collected3_link = 'https://api.trakt.tv/movies/collected/yearly?limit=40&page=1'
        self.collected4_link = 'https://api.trakt.tv/movies/collected/all?limit=40&page=1'
        self.watched1_link = 'https://api.trakt.tv/movies/watched/weekly?limit=40&page=1'
        self.watched2_link = 'https://api.trakt.tv/movies/watched/monthly?limit=40&page=1'
        self.watched3_link = 'https://api.trakt.tv/movies/watched/yearly?limit=40&page=1'
        self.watched4_link = 'https://api.trakt.tv/movies/watched/all?limit=40&page=1'

        self.exploreKeywords_link = 'https://www.imdb.com/search/keyword?keywords=%s&title_type=movie,tvMovie&sort=moviemeter,asc&count=40&start=1'
        self.imdbUserLists_link = 'https://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&count=40&start=1'
        self.imdbTop1000y00to19_link = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&release_date=2000,2019&title_type=movie,tvMovie&sort=moviemeter,asc&count=40&start=1'
        self.imdbTop1000y90to99_link = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&release_date=1990,1999&title_type=movie,tvMovie&sort=moviemeter,asc&count=40&start=1'
        self.imdbTop1000y80to89_link = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&release_date=1980,1989&title_type=movie,tvMovie&sort=moviemeter,asc&count=40&start=1'


    def get(self, url, idx=True, create_directory=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass
            try:
                u = urlparse.urlparse(url).netloc.lower()
            except:
                pass
            if u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakthistory_link:
                        raise Exception()
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
            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True:
                    self.worker()
            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True:
                    self.worker()
            if idx == True and create_directory == True:
                self.movieDirectory(self.list)
            return self.list
        except:
            pass


    def widget(self):
        setting = control.setting('movie.widget')
        if setting == '2':
            self.get(self.trending_link)
        elif setting == '3':
            self.get(self.popular_link)
        elif setting == '4':
            self.get(self.theaters_link)
        elif setting == '5':
            self.get(self.theatersOld_link)
        elif setting == '6':
            self.get(self.added_link)
        else:
            self.get(self.featured_link)


    def search(self):
        navigator.navigator().addDirectoryItem(32603, 'movieSearchnew', 'search.png', 'DefaultMovies.png')
        search_history = control.setting('moviesearch')
        if search_history:
            for term in search_history.split('\n'):
                if term:
                    navigator.navigator().addDirectoryItem(term, 'movieSearchterm&name=%s' % term, 'search.png', 'DefaultMovies.png')
            navigator.navigator().addDirectoryItem(32605, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        navigator.navigator().endDirectory()        


    def search_new(self):
        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t) ; k.doModal()
        q = k.getText().strip() if k.isConfirmed() else None
        if not q:
            return
        search_history = control.setting('moviesearch')
        if q not in search_history.split('\n'):
            control.setSetting('moviesearch', q + '\n' + search_history)
        url = self.search_link + urllib.quote_plus(q)
        self.get(url)


    def search_term(self, name):
        url = self.search_link + urllib.quote_plus(name)
        self.get(url)


    def person(self):
        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t) ; k.doModal()
        q = k.getText().strip() if k.isConfirmed() else None
        if not q:
            return
        url = self.persons_link + urllib.quote_plus(q)
        self.persons(url)


    def genres(self):
        genres = [
            ('Action', 'action', True),
            ('Adventure', 'adventure', True),
            ('Animation', 'animation', True),
            ('Anime', 'anime', False),
            ('Biography', 'biography', True),
            ('Comedy', 'comedy', True),
            ('Crime', 'crime', True),
            ('Documentary', 'documentary', True),
            ('Drama', 'drama', True),
            ('Family', 'family', True),
            ('Fantasy', 'fantasy', True),
            ('History', 'history', True),
            ('Horror', 'horror', True),
            ('Music ', 'music', True),
            ('Musical', 'musical', True),
            ('Mystery', 'mystery', True),
            ('Romance', 'romance', True),
            ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True),
            ('Thriller', 'thriller', True),
            ('War', 'war', True),
            ('Western', 'western', True)]
        for i in genres:
            self.list.append({'name': cleangenre.lang(i[0], self.lang), 'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1], 'image': 'genres.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def languages(self):
        languages = [('Arabic', 'ar'), ('Bosnian', 'bs'), ('Bulgarian', 'bg'), ('Chinese', 'zh'), ('Croatian', 'hr'), ('Dutch', 'nl'),
            ('English', 'en'), ('Finnish', 'fi'), ('French', 'fr'), ('German', 'de'), ('Greek', 'el'),('Hebrew', 'he'), ('Hindi ', 'hi'),
            ('Hungarian', 'hu'), ('Icelandic', 'is'), ('Italian', 'it'), ('Japanese', 'ja'), ('Korean', 'ko'), ('Macedonian', 'mk'),
            ('Norwegian', 'no'), ('Persian', 'fa'), ('Polish', 'pl'), ('Portuguese', 'pt'), ('Punjabi', 'pa'), ('Romanian', 'ro'),
            ('Russian', 'ru'), ('Serbian', 'sr'), ('Slovenian', 'sl'), ('Spanish', 'es'), ('Swedish', 'sv'), ('Turkish', 'tr'), ('Ukrainian', 'uk')]
        for i in languages:
            self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'languages.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = ['G', 'PG', 'PG-13', 'R', 'NC-17']
        for i in certificates:
            self.list.append({'name': str(i), 'url': self.certification_link % str(i), 'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def years(self):
        year = (self.datetime.strftime('%Y'))
        for i in range(int(year) - 0, 1900, -1):
            self.list.append({'name': str(i), 'url': self.year_link % (str(i), str(i)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def my_imdbUserLists(self):
        movielist1 = control.setting('imdb.movielist_name1')
        movielist1_link = control.setting('imdb.movielist_id1')
        if movielist1:
            self.list.append({'name': movielist1, 'url': self.imdbUserLists_link % movielist1_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist2 = control.setting('imdb.movielist_name2')
        movielist2_link = control.setting('imdb.movielist_id2')
        if movielist2:
            self.list.append({'name': movielist2, 'url': self.imdbUserLists_link % movielist2_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist3 = control.setting('imdb.movielist_name3')
        movielist3_link = control.setting('imdb.movielist_id3')
        if movielist3:
            self.list.append({'name': movielist3, 'url': self.imdbUserLists_link % movielist3_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist4 = control.setting('imdb.movielist_name4')
        movielist4_link = control.setting('imdb.movielist_id4')
        if movielist4:
            self.list.append({'name': movielist4, 'url': self.imdbUserLists_link % movielist4_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist5 = control.setting('imdb.movielist_name5')
        movielist5_link = control.setting('imdb.movielist_id5')
        if movielist5:
            self.list.append({'name': movielist5, 'url': self.imdbUserLists_link % movielist5_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist6 = control.setting('imdb.movielist_name6')
        movielist6_link = control.setting('imdb.movielist_id6')
        if movielist6:
            self.list.append({'name': movielist6, 'url': self.imdbUserLists_link % movielist6_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist7 = control.setting('imdb.movielist_name7')
        movielist7_link = control.setting('imdb.movielist_id7')
        if movielist7:
            self.list.append({'name': movielist7, 'url': self.imdbUserLists_link % movielist7_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist8 = control.setting('imdb.movielist_name8')
        movielist8_link = control.setting('imdb.movielist_id8')
        if movielist8:
            self.list.append({'name': movielist8, 'url': self.imdbUserLists_link % movielist8_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist9 = control.setting('imdb.movielist_name9')
        movielist9_link = control.setting('imdb.movielist_id9')
        if movielist9:
            self.list.append({'name': movielist9, 'url': self.imdbUserLists_link % movielist9_link, 'image': 'imdb.png', 'action': 'movies'})
        movielist10 = control.setting('imdb.movielist_name10')
        movielist10_link = control.setting('imdb.movielist_id10')
        if movielist10:
            self.list.append({'name': movielist10, 'url': self.imdbUserLists_link % movielist10_link, 'image': 'imdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def imdbUserLists(self):
        self.list.append({'name': 'IMDb Top1000 (2000 - 2019)', 'url': self.imdbTop1000y00to19_link, 'image': 'imdb.png', 'action': 'movies'})
        self.list.append({'name': 'IMDb Top1000 (1990 - 1999)', 'url': self.imdbTop1000y90to99_link, 'image': 'imdb.png', 'action': 'movies'})
        self.list.append({'name': 'IMDb Top1000 (1980 - 1989)', 'url': self.imdbTop1000y80to89_link, 'image': 'imdb.png', 'action': 'movies'})
        theUserLists = [
            ('10 Most Popular Lifetime Movies on IMDb', 'ls063567036'),
            ('12 Top War Movies', 'ls075413367'),
            ('15 Best Live Action Kids Movies', 'ls074428464'),
            ('50 Inspirational movies and Motivational films', 'ls069754038'),
            ('50 Satirical Films', 'ls076464829'),
            ('80 of the Best Horror Movies to Stream Today', 'ls050104518'),
            ('100 Best Films About Alcoholism POL RUS', 'ls057104247'),
            ('100 Best Sci-Fi movies', 'ls009668082'),
            ('100 Greatest Worst Movies', 'ls021440543'),
            ('100 Movies set in winter time : Christmas time', 'ls057106830'),
            ('100+ Films about tech geeks and computer nerds and a few series', 'ls070949682'),
            ('101 Films Based In One Room', 'ls075785141'),
            ('200 BIOGRAPHY MOVIES : THE BEST FILMS', 'ls057785252'),
            ('2019: A MOVIE ODYSSEY', 'ls000643238'),
            ('Action and Adventure Titles to Discover on Amazon Video', 'ls069177164'),
            ('ACTUAL ONE-SHOT MOVIES', 'ls021290396'),
            ('Alien Invasion Movies (Chronological Order)', 'ls063259747'),
            ('All Kubrick Movies Ranked by IMDb Users', 'ls063329673'),
            ('ALL Movies Based On Video Games', 'ls070389024'),
            ('All Woody Allen Movies Ranked by IMDb User Ratings', 'ls063765351'),
            ('Asian Crime Films:The Ultimate List', 'ls058459196'),
            ('BABYLON 5', 'ls021151794'),
            ('Badass chicks/Girls with guns movies', 'ls050009305'),
            ('Based on actual events : True story movies', 'ls057631565'),
            ('BATTLESTAR GALACTICA', 'ls021157840'),
            ('Best Addiction Movies', 'ls066788382'),
            ('Best animated films:The Ultimate List', 'ls052206353'),
            ('Best BUDDY Movies:The Ultimate List', 'ls053711583'),
            ('Best character study films', 'ls053173569'),
            ('Best Charles Bronson Movies as Rated by IMDb Users', 'ls063429459'),
            ('BEST COMEDY MOVIES', 'ls040040015'),
            ('Best Coming of Age Films:The Ultimate List', 'ls070605453'),
            ('Best Costume Drama:The Ultimate List', 'ls059415760'),
            ('Best Courtroom Movies', 'ls066198904'),
            ('Best Crime Movies:The Ultimate List', 'ls051868612'),
            ('Best Cult/Horror Movies', 'ls004943234'),
            ('Best Dark Comedies:The Ultimate List', 'ls050510323'),
            ('Best Dirty Cop Movies:The Ultimate List', 'ls050549896'),
            ('Best Disaster & Apocalyptic & Post-Apocalyptic Movies', 'ls062746803'),
            ('Best Documentary:The Ultimate List', 'ls051776567'),
            ('Best Family Movies:The Ultimate List', 'ls052767261'),
            ('Best Fantasy Movies:The Ultimate List', 'ls050784999'),
            ('Best Father - Son Movies', 'ls068335911'),
            ('Best Gangster Movies', 'ls066176690'),
            ('Best Giallo Films (Italian Horror):The Ultimate List', 'ls051374549'),
            ('Best Heists & Cons & Scams & Robbers movies', 'ls066780524'),
            ('Best Inspirational & Motivational Movies', 'ls066222382'),
            ('Best Legal Drama:The Ultimate List', 'ls058510754'),
            ('Best Mental & Physical illness and Disability Movies', 'ls066746282'),
            ('Best Movies About Old Age', 'ls069248253'),
            ('Best Music or Musical Movies', 'ls066191116'),
            ('best obscure/underrated films', 'ls062760686'),
            ('Best of Croatian Cinema', 'ls050566435'),
            ('Best Prison & Escape Movies', 'ls066502835'),
            ('Best Psychological Thriller:The Ultimate List', 'ls058229527'),
            ('Best Revenge & Vigilante Movies:The Ultimate List', 'ls070560280'),
            ('Best Revenge Movies', 'ls066797820'),
            ('Best Road Trip & Travel Movies', 'ls066135354'),
            ('Best Serial Killers Movies', 'ls063841856'),
            ('Best Short Movies:The Ultimate List', 'ls050616277'),
            ('Best Silent Films:The Ultimate List', 'ls051374072'),
            ('Best Spy - CIA - MI5 - MI6 - KGB Movies', 'ls066367722'),
            ('Best Spy Movies:The Ultimate List', 'ls058532916'),
            ('Best Survival / Man Vs. Nature Movies', 'ls064685738'),
            ('Best Teen Movies:The Ultimate List', 'ls057112572'),
            ('Best Teenage Movies', 'ls066113037'),
            ('Best Thrillers:The Ultimate List', 'ls050169117'),
            ('Best Time Travel Movies', 'ls066184124'),
            ('Best TV Movies:The Ultimate List', 'ls055559957'),
            ('Best Twist Ending Movies', 'ls066370089'),
            ('Best War Films:The Ultimate List', 'ls051120791'),
            ('BEST WAR MOVIES', 'ls026329851'),
            ('BEST WESTERNS', 'ls021295847'),
            ('Best Westerns:The Ultimate List', 'ls008946126'),
            ('Beyond the Top 250: IMDb Staffs Favorite Movies', 'ls036294138'),
            ('Binge-Watch Star Wars on Amazon Video', 'ls074093523'),
            ('Biography Films:The Ultimate List', 'ls050374454'),
            ('Blaxplotation:The Ultimate List', 'ls058287184'),
            ('Classic Horror Films:The Ultimate List', 'ls054765242'),
            ('Classic Movies on Amazon Video', 'ls064459786'),
            ('Comedy Titles to Discover on Amazon Video', 'ls064848835'),
            ('Conspiracy Movies (Chronological Order)', 'ls062218265'),
            ('Contract Killer / Hitman Movies (chronological Order)', 'ls063204479'),
            ('Dead Of Night', 'ls026128485'),
            ('DISNEY MOVIES (all time)', 'ls000013316'),
            ('Disturbing,Controversial,Shocking and Unique', 'ls008941464'),
            ('DOCTOR WHO', 'ls021157820'),
            ('Drama Movies to Discover on Amazon Video', 'ls069453990'),
            ('EXISTENTIAL FILMS', 'ls027345204'),
            ('FILMS ABOUT ARTISTS , PAINTERS , WRITERS', 'ls008462416'),
            ('FIREFLY/SERENITY', 'ls021151557'),
            ('FLASH GORDON', 'ls021151066'),
            ('French Action Cinema', 'ls008946046'),
            ('Greatest films about love', 'ls057723258'),
            ('Heist Caper Movies (Chronological order)', 'ls062392787'),
            ('Heist Films:The Ultimate List', 'ls058450812'),
            ('Heroic Bloodshed Movies (Chronological Order)', 'ls062247190'),
            ('Hitman Movies:The Ultimate List', 'ls052167156'),
            ('Holiday Movies Streaming on Prime Video', 'ls066664782'),
            ('Holiday TV Specials and Movies', 'ls025227323'),
            ('Holiday TV Viewing Guide', 'ls016086573'),
            ('HORROR FILM SERIES AND FRANCHISES', 'ls022487858'),
            ('Horror of the Skull Posters', 'ls027849454'),
            ('Horror Titles on Amazon Video', 'ls038288732'),
            ('HORROR:The Ultimate List of Slasher Films', 'ls053988992'),
            ('IMDb 25: Top 25 Movies by User Rating From the Last 25 Years', 'ls079342176'),
            ('Investigation Movies', 'ls003062015'),
            ('Italian Crime Films:Polizioteschi', 'ls054153182'),
            ('James Bond: 50 Years of Main Title Design', 'ls023829130'),
            ('Juicys List of Horror Movie Series Trilogies', 'ls054656838'),
            ('List of Stephen King Movies, Films and TV Shows / Peliculas y Series basadas en ...', 'ls051289348'),
            ('Mockbusters, Movie Clones and Film Rip Offs', 'ls077141747'),
            ('MODERN HORROR: MY TOP 150 HORROR MOVIES (2000-2018)', 'ls004043006'),
            ('Modern Westerns:The Ultimate List', 'ls055895628'),
            ('Most Popular Titles on Amazon Video', 'ls063935150'),
            ('Most Visually Beautiful Movies', 'ls053226015'),
            ('Movie Box Sets', 'ls027255428'),
            ('MOVIE LONERS', 'ls027344218'),
            ('MOVIES ABOUT SUICIDE FILMS', 'ls064085103'),
            ('MOVIES AND RACISM', 'ls027604003'),
            ('Movies by Oscar-Winning Directors on Amazon Video', 'ls064052892'),
            ('Movies have taught me', 'ls051072059'),
            ('My favorite UNDERRATED movie gems', 'ls050673652'),
            ('New and Recent DVD/Blu-ray Releases', 'ls016522954'),
            ('New Releases on Amazon Video', 'ls033146151'),
            ('Nicolas Winding Refn Movies by IMDb User Ratings', 'ls063767071'),
            ('On TV: Holiday Specials and Movies', 'ls071809471'),
            ('Popular Fathers Day Movies on Amazon Video', 'ls063527705'),
            ('Popular Indie Movies on Amazon Video', 'ls062565164'),
            ('Popular Sci-Fi Movies to Stream Now With Prime', 'ls022575155'),
            ('Prison Films:The Ultimate List', 'ls054021431'),
            ('Puff Puff Pass', 'ls021557769'),
            ('Recommended: Great movies for intelligent people', 'ls058963815'),
            ('Samourai Films:The Ultimate List', 'ls058459400'),
            ('Science-Fiction:The Ultimate List', 'ls052680925'),
            ('Shakespeare in Cinema', 'ls059431052'),
            ('SHOCKING MOVIE SCENES', 'ls051708902'),
            ('Sleeper Hit Movies', 'ls027822154'),
            ('Smartest Heist/Caper/Con film', 'ls020387857'),
            ('Sports Movies:The Ultimate List', 'ls059998134'),
            ('STAR TREK', 'ls021157975'),
            ('STAR WARS', 'ls021157942'),
            ('STARGATE', 'ls021151078'),
            ('Superhero Movies:The Ultimate List', 'ls051226058'),
            ('The Marvel Universe on Amazon Instant Video', 'ls076497600'),
            ('THE OUTER LIMITS', 'ls021157853'),
            ('The smut we must cut, the trash we must smash', 'ls020576693'),
            ('The Top 200 Movies as Rated by Women on IMDb in 2018', 'ls023589784'),
            ('THE TWILIGHT ZONE', 'ls021157816'),
            ('THE X-FILES', 'ls021151086'),
            ('Top 12 Holiday Movies with Families More Dysfunctional than Yours', 'ls073125467'),
            ('Top 20 Most Awesome Streaming Family Movies', 'ls074243156'),
            ('Top 50 Kung Fu films', 'ls075582795'),
            ('Top 100 Movies as Rated by Women on IMDb in 2016', 'ls033953605'),
            ('TOP ACTION AND ADVENTURE MOVIES: 1970s', 'ls023368188'),
            ('TOP ACTION AND ADVENTURE MOVIES: 1980s', 'ls023364967'),
            ('TOP ACTION AND ADVENTURE MOVIES: 1990s', 'ls023364152'),
            ('TOP ACTION MOVIES: 2000-2019', 'ls027328830'),
            ('TOP ANIMATED MOVIES: 2000-2019', 'ls027345371'),
            ('TOP ANIMATED MOVIES: PRE-2000', 'ls024371623'),
            ('Top British Crime Movies', 'ls057116679'),
            ('TOP DOCUMENTARY MOVIES: 2000-2019', 'ls027340130'),
            ('TOP HORROR MOVIES: 2000-2019', 'ls026579006'),
            ('TOP HORROR MOVIES: PRE-2000', 'ls027347598'),
            ('TOP POLITICAL MOVIES', 'ls040168000'),
            ('TOP SCIENCE-FICTION MOVIES: 2000-2019', 'ls021424736'),
            ('Top-Rated Movies for a Solar Eclipse', 'ls020799130'),
            ('Trending Horror Movies on Amazon Video', 'ls066766366'),
            ('Trending Movies on Amazon Video', 'ls033617995'),
            ('Trending New Releases on Amazon Video', 'ls066054988'),
            ('Trending Titles on Amazon Video', 'ls066706013'),
            ('Valentines Day Suggestions on Amazon Video', 'ls033346558'),
            ('Vampire Movies:The Ultimate List', 'ls054799711'),
            ('World War II Movies:The Ultimate List', 'ls059324807')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.imdbUserLists_link % i[1], 'image': 'imdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def hellaLifeTimeHallMark(self):
        theUserLists = [
            ('2007 - 2009 Hallmark Movies', 'ls062648125'),
            ('2010 & 2011 Hallmark Movies', 'ls062648216'),
            ('2012 & 2013 Hallmark Movies', 'ls062690047'),
            ('2014 Hallmark Movies', 'ls062649887'),
            ('2015 Hallmark Movies', 'ls062649068'),
            ('2016 Hallmark Movies', 'ls062094214'),
            ('2017 Hallmark Movies', 'ls062719390'),
            ('2018 Hallmark Movies', 'ls027316430'),
            ('2019 Hallmark Movies', 'ls045286073'),
            ('Books Becomes Lifetime Movies', 'ls072496955'),
            ('Hallmark Movies - (2001 - PRESENT)', 'ls069761801'),
            ('Hallmark Movies of 2018', 'ls021376459'),
            ('Hallmark Movies of 2019', 'ls041248357'),
            ('Hallmark Movies', 'ls076776375'),
            ('Hallmark Movies Part II', 'ls069936307'),
            ('Lifetime Movies 2019', 'ls041158868'),
            ('Lifetime Movies - (Psycho & Crime)', 'ls069728825'),
            ('Lifetime Movies Ive Seen', 'ls062092121'),
            ('Lifetime Movies', 'ls045517819'),
            ('Lifetime Movies/Original Movies', 'ls073816184'),
            ('Lifetime Movies/Original Movies Part II', 'ls062591941')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.imdbUserLists_link % i[1], 'image': 'imdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def exploreKeywords(self):
        interestingKeywords = [('2d-animation'),
            ('action-hero'), ('alternate-history'), ('ambiguous-ending'), ('americana'), ('anime'), ('anti-hero'),
            ('avant-garde'), ('b-movie'), ('b-western'), ('bank-heist'), ('based-on-book'), ('based-on-comic'),
            ('based-on-comic-book'), ('based-on-novel'), ('based-on-novella'), ('based-on-play'), ('based-on-short-story'), ('based-on-true-story'),
            ('battle'), ('betrayal'), ('biker'), ('black-comedy'), ('blockbuster'), ('bollywood'),
            ('breaking-the-fourth-wall'), ('business'), ('caper'), ('car-accident'), ('car-chase'), ('car-crash'),
            ('character-name-in-title'), ('characters-point-of-view-camera-shot'), ('chick-flick'), ('christmas'), ('coming-of-age'), ('competition'),
            ('conspiracy'), ('cop'), ('corruption'), ('criminal-mastermind'), ('cult'), ('cult-film'),
            ('cyberpunk'), ('dark-hero'), ('dc-comics'), ('deus-ex-machina'), ('dialogue-driven'), ('dialogue-driven-storyline'),
            ('directed-by-star'), ('director-cameo'), ('documentary-subject'), ('double-cross'), ('dream-sequence'), ('drugs'),
            ('dystopia'), ('easter'), ('ensemble-cast'), ('epic'), ('espionage'), ('experimental'),
            ('experimental-film'), ('fairy-tale'), ('famous-line'), ('famous-opening-theme'), ('famous-score'), ('fantasy-sequence'),
            ('farce'), ('father-daughter-relationship'), ('father-son-relationship'), ('femme-fatale'), ('fictional-biography'), ('flashback'),
            ('french-new-wave'), ('futuristic'), ('gangster'), ('good-versus-evil'), ('halloween'), ('heist'),
            ('hero'), ('high-school'), ('horror-movie-remake'), ('husband-wife-relationship'), ('idealism'), ('independent-film'),
            ('investigation'), ('kidnapping'), ('knight'), ('kung-fu'), ('loner'), ('macguffin'),
            ('marvel-comics'), ('may-december-romance'), ('medieval-times'), ('mockumentary'), ('monster'), ('mother-daughter-relationship'),
            ('mother-son-relationship'), ('multiple-actors-playing-same-role'), ('multiple-endings'), ('multiple-perspectives'), ('multiple-storyline'), ('multiple-time-frames'),
            ('murder'), ('musical-number'), ('neo-noir'), ('neorealism'), ('new-year'), ('ninja'),
            ('no-background-score'), ('no-music'), ('no-opening-credits'), ('no-title-at-beginning'), ('nonlinear-timeline'), ('official-james-bond-series'),
            ('on-the-run'), ('one-against-many'), ('one-man-army'), ('opening-action-scene'), ('organized-crime'), ('parenthood'),
            ('parody'), ('plot-twist'), ('police-corruption'), ('police-detective'), ('post-apocalypse'), ('postmodern'),
            ('psychopath'), ('race-against-time'), ('redemption'), ('remake'), ('rescue'), ('road-movie'),
            ('robbery'), ('robot'), ('rotoscoping'), ('satire'), ('self-sacrifice'), ('serial-killer'),
            ('shakespeare'), ('shootout'), ('show-within-a-show'), ('slasher'), ('southern-gothic'), ('spaghetti-western'),
            ('spirituality'), ('spoof'), ('star-trek'), ('star-wars'), ('steampunk'), ('subjective-camera'), ('superhero'),
            ('supernatural'), ('surprise-ending'), ('survival-horror'), ('swashbuckler'), ('sword-and-sandal'), ('tech-noir'),
            ('thanksgiving'), ('time-travel'), ('title-spoken-by-character'), ('told-in-flashback'), ('vampire'), ('virtual-reality'),
            ('voice-over-narration'), ('war-violence'), ('whistleblower'), ('wilhelm-scream'), ('wuxia'), ('zombie')
        ]
        for i in interestingKeywords:
            self.list.append({'name': i.replace('-', ' '), 'url': self.exploreKeywords_link % i, 'image': 'imdb.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            activity = trakt.getActivity()
        except:
            pass
        try:
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '':
                raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass
        self.list = userlists
        for i in range(0, len(self.list)):
            self.list[i].update({'image': 'userlists.png', 'action': 'movies'})
        self.addDirectory(self.list, queue=True)
        return self.list


    def trakt_list(self, url, user):
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            result = trakt.getTraktAsJson(u)
            items = []
            for i in result:
                try:
                    items.append(i['movie'])
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
                title = client.replaceHTMLCodes(title)
                year = item['year']
                year = re.sub('[^0-9]', '', str(year))
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    raise Exception()
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                tmdb = str(item.get('ids', {}).get('tmdb', 0))
                try:
                    premiered = item['released']
                except:
                    premiered = '0'
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                try:
                    genre = item['genres']
                except:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)
                try:
                    duration = str(item['runtime'])
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'
                try:
                    rating = str(item['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'
                try:
                    votes = str(item['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes), ',d'))
                except:
                    pass
                if votes == None:
                    votes = '0'
                try:
                    mpaa = item['certification']
                except:
                    mpaa = '0'
                if mpaa == None:
                    mpaa = '0'
                try:
                    plot = item['overview']
                except:
                    plot = '0'
                if plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                try:
                    tagline = item['tagline']
                except:
                    tagline = '0'
                if tagline == None:
                    tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot, 'tagline': tagline, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': '0', 'next': next})
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
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client.replaceHTMLCodes(name)
                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass
        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def imdb_list(self, url):
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))
            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs={'property': 'pageId'})[0]
            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url
            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url
            result = client.request(url)
            result = result.replace('\n', ' ')
            items = client.parseDOM(result, 'div', attrs={'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs={'class': 'list_item.+?'})
        except:
            return
        try:
            next = client.parseDOM(result, 'a', ret='href', attrs={'class': '.+?ister-page-nex.+?'})
            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs={'class': 'pagination'})[0]
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
                year = client.parseDOM(item, 'span', attrs={'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs={'class': 'year_type'})
                try:
                    year = re.compile('(\d{4})').findall(year)[0]
                except:
                    year = '0'
                year = year.encode('utf-8')
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')
                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    poster = '0'
                if '/nopicture/' in poster:
                    poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
                try:
                    genre = client.parseDOM(item, 'span', attrs={'class': 'genre'})[0]
                except:
                    genre = '0'
                genre = ' / '.join([i.strip() for i in genre.split(',')])
                if genre == '':
                    genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                try:
                    duration = re.findall('(\d+?) min(?:s|)', item)[-1]
                except:
                    duration = '0'
                duration = duration.encode('utf-8')
                rating = '0'
                try:
                    rating = client.parseDOM(item, 'span', attrs={'class': 'rating-rating'})[0]
                except:
                    pass
                try:
                    rating = client.parseDOM(rating, 'span', attrs={'class': 'value'})[0]
                except:
                    rating = '0'
                try:
                    rating = client.parseDOM(item, 'div', ret='data-value', attrs={'class': '.*?imdb-rating'})[0]
                except:
                    pass
                if rating == '' or rating == '-':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')
                try:
                    votes = client.parseDOM(item, 'div', ret='title', attrs={'class': '.*?rating-list'})[0]
                except:
                    votes = '0'
                try:
                    votes = re.findall('\((.+?) vote(?:s|)\)', votes)[0]
                except:
                    votes = '0'
                if votes == '':
                    votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')
                try:
                    mpaa = client.parseDOM(item, 'span', attrs={'class': 'certificate'})[0]
                except:
                    mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED':
                    mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')
                try:
                    director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    director = '0'
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '':
                    director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')
                try:
                    cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    cast = '0'
                cast = client.replaceHTMLCodes(cast)
                cast = cast.encode('utf-8')
                cast = client.parseDOM(cast, 'a')
                if cast == []:
                    cast = '0'
                plot = '0'
                try:
                    plot = client.parseDOM(item, 'p', attrs={'class': 'text-muted'})[0]
                except:
                    pass
                try:
                    plot = client.parseDOM(item, 'div', attrs={'class': 'item_description'})[0]
                except:
                    pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                plot = re.sub('<.+?>|</.+?>', '', plot)
                if plot == '':
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'cast': cast, 'plot': plot, 'tagline': '0', 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass
        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs={'class': '.+?etail'})
        except:
            return
        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = name.encode('utf-8')
                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = client.parseDOM(item, 'img', ret='src')[0]
                # if not ('._SX' in image or '._SY' in image): raise Exception()
                image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass
        return self.list


    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
        except:
            pass
        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass
        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def worker(self, level=1):
        self.meta = []
        total = len(self.list)
        self.fanart_tv_headers = {'api-key': 'Y2IyZjc4MzkwYzZmN2NiYzVkMWM5YTI1N2UwMTNlNWM='.decode('base64')}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})
        for i in range(0, total):
            self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.lang, self.user)
        for r in range(0, total, 40):
            threads = []
            for i in range(r, r + 40):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            if self.meta:
                metacache.insert(self.meta)
        self.list = [i for i in self.list if not i['imdb'] == '0']
        self.list = metacache.local(self.list, self.tm_img_link, 'poster2', 'fanart2')
        if self.fanart_tv_user == '':
            for i in self.list:
                i.update({'clearlogo': '0', 'clearart': '0'})


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                raise Exception()
            imdb = self.list[i]['imdb']
            item = trakt.getMovieSummary(imdb)
            title = item.get('title')
            title = client.replaceHTMLCodes(title)
            originaltitle = title
            year = item.get('year', 0)
            year = re.sub('[^0-9]', '', str(year))
            imdb = item.get('ids', {}).get('imdb', '0')
            imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
            tmdb = str(item.get('ids', {}).get('tmdb', 0))
            premiered = item.get('released', '0')
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except:
                premiered = '0'
            genre = item.get('genres', [])
            genre = [x.title() for x in genre]
            genre = ' / '.join(genre).strip()
            if not genre:
                genre = '0'
            duration = str(item.get('Runtime', 0))
            rating = item.get('rating', '0')
            if not rating or rating == '0.0':
                rating = '0'
            votes = item.get('votes', '0')
            try:
                votes = str(format(int(votes), ',d'))
            except:
                pass
            mpaa = item.get('certification', '0')
            if not mpaa:
                mpaa = '0'
            tagline = item.get('tagline', '0')
            plot = item.get('overview', '0')
            people = trakt.getPeople(imdb, 'movies')
            director = writer = ''
            if 'crew' in people and 'directing' in people['crew']:
                director = ', '.join([director['person']['name'] for director in people['crew']['directing'] if director['job'].lower() == 'director'])
            if 'crew' in people and 'writing' in people['crew']:
                writer = ', '.join([writer['person']['name'] for writer in people['crew']['writing'] if writer['job'].lower() in ['writer', 'screenplay', 'author']])
            cast = []
            for person in people.get('cast', []):
                cast.append({'name': person['person']['name'], 'role': person['character']})
            cast = [(person['name'], person['role']) for person in cast]
            try:
                if self.lang == 'en' or self.lang not in item.get('available_translations', [self.lang]):
                    raise Exception()
                trans_item = trakt.getMovieTranslation(imdb, self.lang, full=True)
                title = trans_item.get('title') or title
                tagline = trans_item.get('tagline') or tagline
                plot = trans_item.get('overview') or plot
            except:
                pass
            try:
                artmeta = True
                # if self.fanart_tv_user == '': raise Exception()
                art = client.request(self.fanart_tv_art_link % imdb, headers=self.fanart_tv_headers, timeout='10', error=True)
                try:
                    art = json.loads(art)
                except:
                    artmeta = False
            except:
                pass
            try:
                poster2 = art['movieposter']
                poster2 = [x for x in poster2 if x.get('lang') == self.lang][::-1] + [x for x in poster2 if x.get('lang') == 'en'][::-1] + [x for x in poster2 if x.get('lang') in ['00', '']][::-1]
                poster2 = poster2[0]['url'].encode('utf-8')
            except:
                poster2 = '0'
            try:
                if 'moviebackground' in art:
                    fanart = art['moviebackground']
                else:
                    fanart = art['moviethumb']
                fanart = [x for x in fanart if x.get('lang') == self.lang][::-1] + [x for x in fanart if x.get('lang') == 'en'][::-1] + [x for x in fanart if x.get('lang') in ['00', '']][::-1]
                fanart = fanart[0]['url'].encode('utf-8')
            except:
                fanart = '0'
            try:
                banner = art['moviebanner']
                banner = [x for x in banner if x.get('lang') == self.lang][::-1] + [x for x in banner if x.get('lang') == 'en'][::-1] + [x for x in banner if x.get('lang') in ['00', '']][::-1]
                banner = banner[0]['url'].encode('utf-8')
            except:
                banner = '0'
            try:
                if 'hdmovielogo' in art:
                    clearlogo = art['hdmovielogo']
                else:
                    clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == self.lang][::-1] + [x for x in clearlogo if x.get('lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = clearlogo[0]['url'].encode('utf-8')
            except:
                clearlogo = '0'
            try:
                if 'hdmovieclearart' in art:
                    clearart = art['hdmovieclearart']
                else:
                    clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == self.lang][::-1] + [x for x in clearart if x.get('lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = clearart[0]['url'].encode('utf-8')
            except:
                clearart = '0'
            try:
                if self.tm_user == '':
                    raise Exception()
                art2 = client.request(self.tm_art_link % imdb, timeout='10', error=True)
                art2 = json.loads(art2)
            except:
                pass
            try:
                poster3 = art2['posters']
                poster3 = [x for x in poster3 if x.get('iso_639_1') == self.lang] + [x for x in poster3 if x.get('iso_639_1') == 'en'] + [x for x in poster3 if x.get('iso_639_1') not in [self.lang, 'en']]
                poster3 = [(x['width'], x['file_path']) for x in poster3]
                poster3 = [(x[0], x[1]) if x[0] < 300 else ('300', x[1]) for x in poster3]
                poster3 = self.tm_img_link % poster3[0]
                poster3 = poster3.encode('utf-8')
            except:
                poster3 = '0'
            try:
                fanart2 = art2['backdrops']
                fanart2 = [x for x in fanart2 if x.get('iso_639_1') == self.lang] + [x for x in fanart2 if x.get('iso_639_1') == 'en'] + [x for x in fanart2 if x.get('iso_639_1') not in [self.lang, 'en']]
                fanart2 = [x for x in fanart2 if x.get('width') == 1920] + [x for x in fanart2 if x.get('width') < 1920]
                fanart2 = [(x['width'], x['file_path']) for x in fanart2]
                fanart2 = [(x[0], x[1]) if x[0] < 1280 else ('1280', x[1]) for x in fanart2]
                fanart2 = self.tm_img_link % fanart2[0]
                fanart2 = fanart2.encode('utf-8')
            except:
                fanart2 = '0'
            item = {'title': title, 'originaltitle': originaltitle, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'poster': '0', 'poster2': poster2, 'poster3': poster3, 'banner': banner, 'fanart': fanart, 'fanart2': fanart2, 'clearlogo': clearlogo, 'clearart': clearart, 'premiered': premiered, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}
            item = dict((k, v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)
            if artmeta == False:
                raise Exception()
            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
        except:
            pass


    def movieDirectory(self, items):
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
        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'
        indicators = playcount.getMovieIndicators(refresh=True) if action == 'movies' else playcount.getMovieIndicators()
        playbackMenu = control.lang(32063).encode('utf-8') if control.setting('hosts.mode') == '2' else control.lang(32064).encode('utf-8')
        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')
        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')
        for i in items:
            try:
                label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                sysname = urllib.quote_plus('%s (%s)' % (title, year))
                systitle = urllib.quote_plus(title)
                meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})
                #meta.update({'trailer': 'plugin://script.extendedinfo/?info=playtrailer&&id=%s' % imdb})
                if not 'duration' in i:
                    meta.update({'duration': '120'})
                elif i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass
                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})
                sysmeta = urllib.quote_plus(json.dumps(meta))
                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)
                path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)
                cm = []
                cm.append(('Find similar', 'ActivateWindow(10025,%s?action=movies&url=https://api.trakt.tv/movies/%s/related,return)' % (sysaddon, imdb)))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' % (sysaddon, sysname, imdb)))
                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))
                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))
                cm.append((addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, sysname, systitle, year, imdb, tmdb)))
                item = control.item(label=label)
                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})
                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})
                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})
                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})
                if settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    item.setProperty('Fanart_Image', i['fanart2'])
                elif settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels = control.metadataClean(meta))
                #item.setInfo(type='Video', infoLabels=meta) # old code
                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass
        try:
            url = items[0]['next']
            if url == '':
                raise Exception()
            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))
            item = control.item(label=nextMenu)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None:
                item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass
        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})


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
                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=movie&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))
                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=moviesToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
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


