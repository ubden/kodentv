# -*- coding: utf-8 -*-

import os,sys,re,json,urllib,urlparse,datetime,xbmc,base64
from resources.lib.modules import cache,client,control,cleangenre,cleantitle,trakt
from resources.lib.modules import utils,views,metacache,workers,playcount,favourites
from resources.lib.indexers import navigator

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', ''))) if len(sys.argv) > 1 else dict()
action = params.get('action')
control.moderator()


class tvshows:
    def __init__(self):
        self.list = []
        self.imdb_link = 'https://www.imdb.com'
        self.trakt_link = 'https://api.trakt.tv'
        self.tvmaze_link = 'http://www.tvmaze.com'
        self.logo_link = 'https://i.imgur.com/'
        self.tvdb_key = 'MUQ2MkYyRjkwMDMwQzQ0NA==' # Old MUQ2MkYyRjkwMDMwQzQ0NA==
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = control.setting('fanart.tv.user') + str('')
        self.lang = control.apiLanguage()['tvdb']
        
        self.tvmaze_info_link = 'http://api.tvmaze.com/shows/%s'
        self.tvdb_info_link = 'https://thetvdb.com/api/%s/series/%s/%s.xml' % (self.tvdb_key.decode('base64'), '%s', self.lang)
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/tv/%s'
        self.fanart_tv_level_link = 'http://webservice.fanart.tv/v3/level'
        self.tvdb_by_imdb = 'https://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tvdb_by_query = 'https://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.tvdb_image = 'https://www.thetvdb.com/banners/'
        
        self.imdblists_link = 'https://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'https://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=tvSeries,tvMiniSeries&start=1'
        self.imdblist2_link = 'https://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=tvSeries,tvMiniSeries&start=1'
        self.imdbwatchlist_link = 'https://www.imdb.com/user/ur%s/watchlist/?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'https://www.imdb.com/user/ur%s/watchlist/?sort=date_added,desc' % self.imdb_user
        
        self.traktlists_link = 'https://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'https://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'https://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'https://api.trakt.tv/users/me/collection/shows'
        self.traktwatchlist_link = 'https://api.trakt.tv/users/me/watchlist/shows'
        self.onDeckTV_link = 'https://api.trakt.tv/sync/playback/episodes?extended=full&limit=40'
        
        self.traktfeatured_link = 'https://api.trakt.tv/recommendations/shows?limit=40'
        self.trending_link = 'https://api.trakt.tv/shows/trending?limit=40&page=1'
        self.traktpopular_link = 'https://api.trakt.tv/shows/popular?limit=40&page=1'
        self.traktanticipated_link = 'https://api.trakt.tv/shows/anticipated?limit=40&page=1'
        
        self.popular_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=moviemeter,asc&count=40&start=1'
        self.airing_link = 'https://www.imdb.com/search/title?title_type=tv_episode&release_date=date[1],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.active_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=10,&production_status=active&sort=moviemeter,asc&count=40&start=1'
        # self.premiere_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.premiere_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=release_date,desc&count=40&start=1'
        self.rating_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=40&start=1'
        self.views_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=num_votes,desc&count=40&start=1'
        
        self.genre_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=40&start=1'
        self.keyword_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.language_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
        self.certification_link = 'https://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&certificates=us:%s&sort=moviemeter,asc&count=40&start=1'
        
        self.update_link = 'https://api.trakt.tv/shows/updates/%s?limit=40&page=1'
        self.search_link = 'https://api.trakt.tv/search/show?limit=20&page=1&query='
        self.person_link = 'https://www.imdb.com/search/title?title_type=tvSeries,tvMiniSeries&release_date=,date[0]&role=%s&sort=year,desc&count=40&start=1'
        self.persons_link = 'https://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'https://www.imdb.com/search/name?count=100&gender=male,female'
        
        self.played1_link = 'https://api.trakt.tv/shows/played/weekly?limit=40&page=1'
        self.played2_link = 'https://api.trakt.tv/shows/played/monthly?limit=40&page=1'
        self.played3_link = 'https://api.trakt.tv/shows/played/yearly?limit=40&page=1'
        self.played4_link = 'https://api.trakt.tv/shows/played/all?limit=40&page=1'
        self.collected1_link = 'https://api.trakt.tv/shows/collected/weekly?limit=40&page=1'
        self.collected2_link = 'https://api.trakt.tv/shows/collected/monthly?limit=40&page=1'
        self.collected3_link = 'https://api.trakt.tv/shows/collected/yearly?limit=40&page=1'
        self.collected4_link = 'https://api.trakt.tv/shows/collected/all?limit=40&page=1'
        self.watched1_link = 'https://api.trakt.tv/shows/watched/weekly?limit=40&page=1'
        self.watched2_link = 'https://api.trakt.tv/shows/watched/monthly?limit=40&page=1'
        self.watched3_link = 'https://api.trakt.tv/shows/watched/yearly?limit=40&page=1'
        self.watched4_link = 'https://api.trakt.tv/shows/watched/all?limit=40&page=1'

        self.exploreKeywords_link = 'https://www.imdb.com/search/keyword?keywords=%s&title_type=tvSeries,miniSeries&sort=moviemeter,asc&count=40&start=1'
        self.imdbUserLists_link = 'https://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=tvSeries,miniSeries&count=40&start=1'


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
            elif u in self.tvmaze_link:
                self.list = cache.get(self.tvmaze_list, 168, url)
                if idx == True:
                    self.worker()
            if idx == True and create_directory == True:
                self.tvshowDirectory(self.list)
            return self.list
        except:
            pass


    def search(self):
        navigator.navigator().addDirectoryItem(32603, 'tvSearchnew', 'search.png', 'DefaultTVShows.png')
        search_history = control.setting('tvsearch')
        if search_history:
            for term in search_history.split('\n'):
                if term:
                    navigator.navigator().addDirectoryItem(term, 'tvSearchterm&name=%s' % term, 'search.png', 'DefaultTVShows.png')
            navigator.navigator().addDirectoryItem(32605, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        navigator.navigator().endDirectory()


    def search_new(self):
        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t) ; k.doModal()
        q = k.getText().strip() if k.isConfirmed() else None
        if not q:
            return
        search_history = control.setting('tvsearch')
        if q not in search_history.split('\n'):
            control.setSetting('tvsearch', q + '\n' + search_history)
        url = self.search_link + urllib.quote_plus(q)
        self.get(url)


    def search_term(self, name):
        url = self.search_link + urllib.quote_plus(name)
        self.get(url)


    def person(self):
        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t) ; k.doModal()
        q = k.getText() if k.isConfirmed() else None
        if (q == None or q == ''):
            return
        url = self.persons_link + urllib.quote_plus(q)
        self.persons(url)


    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)
        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def genres(self):
        genres = [
            ('Action', 'action', True),
            ('Adventure', 'adventure', True),
            ('Animation', 'animation', True),
            ('Anime', 'anime', False),
            ('Biography', 'biography', True),
            ('Comedy', 'comedy', True),
            ('Crime', 'crime', True),
            ('Drama', 'drama', True),
            ('Family', 'family', True),
            ('Fantasy', 'fantasy', True),
            ('Game-Show', 'game_show', True),
            ('History', 'history', True),
            ('Horror', 'horror', True),
            ('Music ', 'music', True),
            ('Musical', 'musical', True),
            ('Mystery', 'mystery', True),
            ('News', 'news', True),
            ('Reality-TV', 'reality_tv', True),
            ('Romance', 'romance', True),
            ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True),
            ('Talk-Show', 'talk_show', True),
            ('Thriller', 'thriller', True),
            ('War', 'war', True),
            ('Western', 'western', True)
        ]
        for i in genres:
            self.list.append({'name': cleangenre.lang(i[0], self.lang), 'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1], 'image': 'genres.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def networks(self):  # United States
        networks = [
            ('A&E', '/networks/29/ae'), ('ABC', '/networks/3/abc'),
            ('Adult Swim', '/networks/10/adult-swim'), ('AHC', '/networks/229/ahc'),
            ('Al Jazeera America', '/networks/169/al-jazeera-america'), ('AMC', '/networks/20/amc'),
            ('Animal Planet', '/networks/92/animal-planet'), ('Audience Network', '/networks/31/audience-network'),
            ('AXS TV', '/networks/170/axs-tv'), ('BBC America', '/networks/15/bbc-america'),
            ('BET', '/networks/56/bet'), ('Bloomberg TV', '/networks/172/bloomberg-tv'),
            ('Boomerang', '/networks/456/boomerang'), ('BOUNCE TV', '/networks/261/bounce-tv'),
            ('Bravo', '/networks/52/bravo'), ('BYU Television', '/networks/467/byu-television'),
            ('C-SPAN2', '/networks/1514/c-span2'), ('Cartoon Network', '/networks/11/cartoon-network'),
            ('CBS', '/networks/2/cbs'), ('CBS Sports Network', '/networks/272/cbs-sports-network'),
            ('Cinemax', '/networks/19/cinemax'), ('CMT', '/networks/173/cmt'),
            ('CNBC', '/networks/93/cnbc'), ('CNN', '/networks/40/cnn'),
            ('Comedy Central', '/networks/23/comedy-central'), ('Cooking Channel', '/networks/174/cooking-channel'),
            ('Create', '/networks/175/create'), ('Destination America', '/networks/107/destination-america'),
            ('Discovery Channel', '/networks/66/discovery-channel'), ('Discovery Family', '/networks/176/discovery-family'),
            ('Discovery Life', '/networks/177/discovery-life'), ('Disney Channel', '/networks/78/disney-channel'),
            ('Disney Junior', '/networks/1039/disney-junior'), ('Disney XD', '/networks/25/disney-xd'),
            ('DIY Network', '/networks/90/diy-network'), ('E!', '/networks/43/e'),
            ('El Rey Network', '/networks/21/el-rey-network'), ('Epix', '/networks/253/epix'),
            ('ESPN', '/networks/39/espn'), ('ESPN2', '/networks/180/espn2'),
            ('ESPNEWS', '/networks/181/espnews'), ('Esquire Network', '/networks/184/esquire-network'),
            ('Estrella TV', '/networks/535/estrella-tv'), ('Food Network', '/networks/81/food-network'),
            ('Fox', '/networks/4/fox'), ('Fox Business Network', '/networks/524/fox-business-network'),
            ('Fox News Channel', '/networks/185/fox-news-channel'), ('Fox Sports 1', '/networks/95/fox-sports-1'),
            ('Fox Sports SUN', '/networks/1047/fox-sports-sun'), ('FreeForm', '/networks/26/freeform'),
            ('FUSE TV', '/networks/186/fuse-tv'), ('Fusion', '/networks/187/fusion'),
            ('FX', '/networks/13/fx'), ('FXX', '/networks/47/fxx'),
            ('Fyi,', '/networks/125/fyi'), ('G4', '/networks/248/g4'),
            ('Game Show Network', '/networks/189/game-show-network'), ('Golf Channel', '/networks/188/golf-channel'),
            ('Great American Country', '/networks/103/great-american-country'), ('H2', '/networks/74/h2'),
            ('Hallmark Channel', '/networks/50/hallmark-channel'), ('Hallmark Movies & Mysteries', '/networks/252/hallmark-movies-mysteries'),
            ('HBO', '/networks/8/hbo'), ('HBO Family', '/networks/190/hbo-family'),
            ('HGTV', '/networks/192/hgtv'), ('History', '/networks/53/history'),
            ('HLN', '/networks/193/hln'), ('IFC', '/networks/65/ifc'),
            ('Insp', '/networks/660/insp'), ('Investigation Discovery', '/networks/89/investigation-discovery'),
            ('JTV', '/networks/1626/jtv'), ('KCET', '/networks/975/kcet'),
            ('Lifetime', '/networks/18/lifetime'), ('Lifetime Movies', '/networks/232/lifetime-movies'),
            ('Logo TV', '/networks/117/logo-tv'), ('MAVTV', '/networks/739/mavtv'),
            ('Me-TV', '/networks/198/me-tv'), ('MotorTrend', '/networks/142/motortrend'),
            ('MSNBC', '/networks/201/msnbc'), ('MTV', '/networks/22/mtv'),
            ('MTV2', '/networks/145/mtv2'), ('National Geographic Channel', '/networks/42/national-geographic-channel'),
            ('National Geographic WILD', '/networks/83/national-geographic-wild'), ('NBC', '/networks/1/nbc'),
            ('NBCSN', '/networks/104/nbcsn'), ('NFL Network', '/networks/205/nfl-network'),
            ('Nick Jr.', '/networks/206/nick-jr'), ('Nickelodeon', '/networks/27/nickelodeon'),
            ('Nicktoons', '/networks/73/nicktoons'), ('Oprah Winfrey Network', '/networks/236/oprah-winfrey-network'),
            ('Ora TV', '/networks/1368/ora-tv'), ('Outdoor Channel', '/networks/207/outdoor-channel'),
            ('Ovation', '/networks/208/ovation'), ('Oxygen', '/networks/79/oxygen'),
            ('Palladia', '/networks/736/palladia'), ('Paramount Network', '/networks/34/paramount-network'),
            ('Pay-Per-View', '/networks/138/pay-per-view'), ('PBS', '/networks/85/pbs'),
            ('Pivot', '/networks/211/pivot'), ('Playboy TV', '/networks/1035/playboy-tv'),
            ('Pop', '/networks/88/pop'), ('Pursuit Channel', '/networks/733/pursuit-channel'),
            ('Qubo', '/networks/212/qubo'), ('REELZ', '/networks/75/reelz'),
            ('REVOLT', '/networks/520/revolt'), ('Science', '/networks/77/science'),
            ('Showtime', '/networks/9/showtime'), ('Smithsonian Channel', '/networks/86/smithsonian-channel'),
            ('Spectrum', '/networks/1620/spectrum'), ('Sportsman Channel', '/networks/217/sportsman-channel'),
            ('Starz', '/networks/17/starz'), ('Sundance TV', '/networks/33/sundance-tv'),
            ('Syfy', '/networks/16/syfy'), ('Syndication', '/networks/72/syndication'),
            ('TBN', '/networks/758/tbn'), ('TBS', '/networks/32/tbs'),
            ('Telemundo', '/networks/219/telemundo'), ('The CW', '/networks/5/the-cw'),
            ('The Weather Channel', '/networks/228/the-weather-channel'), ('TLC', '/networks/80/tlc'),
            ('TNT', '/networks/14/tnt'), ('Travel Channel', '/networks/82/travel-channel'),
            ('truTV', '/networks/84/trutv'), ('TV Guide Channel', '/networks/455/tv-guide-channel'),
            ('TV Land', '/networks/57/tv-land'), ('TV One', '/networks/224/tv-one'),
            ('UniMás', '/networks/225/unimas'), ('Universal Kids', '/networks/342/universal-kids'),
            ('Univision', '/networks/226/univision'), ('UP TV', '/networks/227/up-tv'),
            ('USA Network', '/networks/30/usa-network'), ('VH1', '/networks/55/vh1'),
            ('VH1 Classic', '/networks/557/vh1-classic'), ('Viceland', '/networks/1006/viceland'),
            ('We tv', '/networks/122/we-tv'), ('WGBH-TV', '/networks/1089/wgbh-tv'),
            ('WGN America', '/networks/28/wgn-america'), ('World', '/networks/430/world')
        ]
        for i in networks:
            #self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': i[2], 'action': 'tvshows'})
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tvCanadanetworks(self):  # Canada
        networks = [
            ('Aboriginal Peoples Television Network', '/networks/792/aboriginal-peoples-television-network'),
            ('Bravo', '/networks/296/bravo'), ('CBC News Network', '/networks/808/cbc-news-network'),
            ('CBC', '/networks/36/cbc'), ('City', '/networks/151/city'),
            ('CMT', '/networks/809/cmt'), ('Cottage Life', '/networks/885/cottage-life'),
            ('CTV', '/networks/48/ctv'), ('Discovery Channel', '/networks/298/discovery-channel'),
            ('Documentary', '/networks/895/documentary'), ('E!', '/networks/814/e'),
            ('Family Channel', '/networks/100/family-channel'), ('Family Jr.', '/networks/854/family-jr'),
            ('Food Network', '/networks/325/food-network'), ('Global', '/networks/67/global'),
            ('HGTV', '/networks/726/hgtv'), ('History', '/networks/118/history'),
            ('ICI Radio-Canada Télé', '/networks/451/ici-radio-canada-tele'), ('Knowledge Network', '/networks/803/knowledge-network'),
            ('Love Nature', '/networks/622/love-nature'), ('MOI&cie', '/networks/964/moicie'),
            ('MusiquePlus', '/networks/837/musiqueplus'), ('OLN', '/networks/350/oln'),
            ('OMNI', '/networks/480/omni'), ('OUTtv', '/networks/659/outtv'),
            ('Space', '/networks/7/space'), ('Super Écran', '/networks/866/super-ecran'),
            ('T+E', '/networks/949/te'), ('Teletoon', '/networks/376/teletoon'),
            ('The Comedy Network', '/networks/821/the-comedy-network'), ('Treehouse', '/networks/823/treehouse'),
            ('TVA', '/networks/539/tva'), ('TVO', '/networks/489/tvo'),
            ('Télé-Québec', '/networks/805/tele-quebec'), ('V', '/networks/795/v'),
            ('Viceland', '/networks/945/viceland'), ('VisionTV', '/networks/827/visiontv'),
            ('W Network', '/networks/286/w-network'), ('YTV', '/networks/144/ytv')
        ]
        for i in networks:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tvUnitedKingdomnetworks(self):  # United Kingdom
        networks = [
            ('5Spike', '/networks/552/5spike'),
            ('5STAR', '/networks/553/5star'), ('Animal Planet', '/networks/635/animal-planet'),
            ('BBC Four', '/networks/51/bbc-four'), ('BBC News', '/networks/696/bbc-news'),
            ('BBC One London', '/networks/770/bbc-one-london'), ('BBC One Northern Ireland', '/networks/389/bbc-one-northern-ireland'),
            ('BBC One Scotland', '/networks/1042/bbc-one-scotland'), ('BBC One South West', '/networks/772/bbc-one-south-west'),
            ('BBC One Wales', '/networks/352/bbc-one-wales'), ('BBC One Yorkshire and Lincolnshire', '/networks/764/bbc-one-yorkshire-and-lincolnshire'),
            ('BBC One', '/networks/12/bbc-one'), ('BBC Parliament', '/networks/697/bbc-parliament'),
            ('BBC Scotland', '/networks/1648/bbc-scotland'), ('BBC Three', '/networks/49/bbc-three'),
            ('BBC Two Northern Ireland', '/networks/556/bbc-two-northern-ireland'), ('BBC Two Scotland', '/networks/1045/bbc-two-scotland'),
            ('BBC Two Wales', '/networks/353/bbc-two-wales'), ('BBC Two', '/networks/37/bbc-two'),
            ('BBC World News', '/networks/315/bbc-world-news'), ('BLAZE', '/networks/1279/blaze'),
            ('BT Sport 1', '/networks/620/bt-sport-1'), ('Cartoonito', '/networks/661/cartoonito'),
            ('CBBC', '/networks/60/cbbc'), ('CBeebies', '/networks/458/cbeebies'),
            ('CBS Reality', '/networks/566/cbs-reality'), ('Channel 4', '/networks/45/channel-4'),
            ('Channel 5', '/networks/135/channel-5'), ('CITV', '/networks/433/citv'),
            ('Comedy Central', '/networks/309/comedy-central'), ('Crime & Investigation', '/networks/346/crime-investigation'),
            ('Dave', '/networks/59/dave'), ('Discovery Channel', '/networks/143/discovery-channel'),
            ('Disney Channel', '/networks/312/disney-channel'), ('E4', '/networks/41/e4'),
            ('E!', '/networks/570/e'), ('Food Network', '/networks/649/food-network'),
            ('FOX', '/networks/359/fox'), ('Gold', '/networks/388/gold'),
            ('Good Food', '/networks/651/good-food'), ('H2', '/networks/640/h2'),
            ('History', '/networks/639/history'), ('Investigation Discovery', '/networks/634/investigation-discovery'),
            ('ITV2', '/networks/54/itv2'), ('ITV3', '/networks/550/itv3'),
            ('ITV4', '/networks/310/itv4'), ('ITV Be', '/networks/551/itv-be'),
            ('ITV Wales', '/networks/1459/itv-wales'), ('ITV', '/networks/35/itv'),
            ('Lifetime', '/networks/459/lifetime'), ('More4', '/networks/548/more4'),
            ('MTV', '/networks/94/mtv'), ('My5', '/networks/576/my5'),
            ('National Geographic Channel', '/networks/242/national-geographic-channel'), ('Nickelodeon', '/networks/243/nickelodeon'),
            ('Quest Red', '/networks/1369/quest-red'), ('Quest', '/networks/368/quest'),
            ('Really', '/networks/343/really'), ('S4C', '/networks/64/s4c'),
            ('Sky 1', '/networks/63/sky-1'), ('Sky Arts', '/networks/69/sky-arts'),
            ('Sky Atlantic', '/networks/113/sky-atlantic'), ('Sky Sports 1', '/networks/445/sky-sports-1'),
            ('Sky Witness', '/networks/44/sky-witness'), ('STV', '/networks/777/stv'),
            ('TLC', '/networks/645/tlc'), ('Together', '/networks/1591/together'),
            ('W', '/networks/295/w'), ('Yesterday', '/networks/345/yesterday')
        ]
        for i in networks:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tvAustralianetworks(self):  # Australia
        networks = [
            ('7mate', '/networks/485/7mate'), ('7TWO', '/networks/728/7two'),
            ('9Gem', '/networks/1144/9gem'), ('9Go!', '/networks/1145/9go'),
            ('9Life', '/networks/1146/9life'), ('10 Peach', '/networks/729/10-peach'),
            ('A&E', '/networks/775/ae'), ('ABC Comedy', '/networks/301/abc-comedy'),
            ('ABC KIDS', '/networks/1154/abc-kids'), ('ABC ME', '/networks/116/abc-me'),
            ('ABC', '/networks/114/abc'), ('Arena', '/networks/294/arena'),
            ('C31', '/networks/730/c31'), ('Crime + Investigation', '/networks/483/crime-investigation'),
            ('Discovery CHANNEL', '/networks/1051/discovery-channel'), ('FOX8', '/networks/411/fox8'),
            ('HISTORY', '/networks/722/history'), ('LifeStyle', '/networks/313/lifestyle'),
            ('LifeStyle Food', '/networks/1059/lifestyle-food'), ('National Geographic Channel', '/networks/723/national-geographic-channel'),
            ('Network 10', '/networks/149/network-10'), ('Nine Network', '/networks/120/nine-network'),
            ('SBS VICELAND', '/networks/1152/sbs-viceland'), ('SBS', '/networks/140/sbs'),
            ('Seven Network', '/networks/251/seven-network'), ('Showcase', '/networks/270/showcase'),
            ('The Comedy Channel', '/networks/330/the-comedy-channel'), ('Universal Channel', '/networks/1162/universal-channel')
        ]
        for i in networks:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tvOthers1networks(self):  # Other Countries 1
        networks = [
            ('1+1', '/networks/423/11'),
            ('#0', '/networks/1529/-'), ('ABS-CBN', '/networks/278/abs-cbn'),
            ('Antena 3', '/networks/97/antena-3'), ('Arirang TV', '/networks/1349/arirang-tv'),
            ('AT-X', '/networks/167/at-x'), ('ATV', '/networks/504/atv'),
            ('AXN', '/networks/440/axn'), ('AXN', '/networks/1665/axn'),
            ('Azteca', '/networks/998/azteca'), ('BBC Earth', '/networks/1298/bbc-earth'),
            ('BBC Lifestyle', '/networks/477/bbc-lifestyle'), ('Bravo', '/networks/1027/bravo'),
            ('BS11', '/networks/133/bs11'), ('C More', '/networks/1367/c-more'),
            ('Canal+', '/networks/273/canal'), ('Canal+', '/networks/407/canal'),
            ('Canale 5', '/networks/364/canale-5'), ('Channel 2', '/networks/781/channel-2'),
            ('Channel 3', '/networks/718/channel-3'), ('Channel 5', '/networks/521/channel-5'),
            ('Channel 7', '/networks/787/channel-7'), ('Channel A', '/networks/538/channel-a'),
            ('Colors', '/networks/438/colors'), ('Comedy Central', '/networks/974/comedy-central'),
            ('Comedy Central', '/networks/1263/comedy-central'), ('CTV', '/networks/465/ctv'),
            ('Cuatro', '/networks/98/cuatro'), ('Discovery Channel', '/networks/1496/discovery-channel'),
            ('Dlife', '/networks/1363/dlife'), ('e.tv', '/networks/1240/etv'),
            ('EBS', '/networks/714/ebs'), ('FEM', '/networks/1566/fem'),
            ('Fox Life', '/networks/1617/fox-life'), ('FOX Türkiye', '/networks/499/fox-turkiye'),
            ('Fuji TV', '/networks/131/fuji-tv'), ('FYI Asia', '/networks/1269/fyi-asia'),
            ('Geo Entertainment', '/networks/1022/geo-entertainment'), ('GMM25', '/networks/1095/gmm25'),
            ('GTV', '/networks/416/gtv'), ('Hakka TV', '/networks/1065/hakka-tv'),
            ('HBO Asia', '/networks/362/hbo-asia'), ('HBO Polska', '/networks/399/hbo-polska'),
            ('HBO România', '/networks/1014/hbo-romania'), ('History', '/networks/776/history'),
            ('HOT3', '/networks/1033/hot3'), ('jTBC', '/networks/268/jtbc'),
            ('Kanal 5', '/networks/1281/kanal-5'), ('Kanal 7', '/networks/1607/kanal-7'),
            ('Kanal 11', '/networks/1307/kanal-11'), ('Kanal D', '/networks/417/kanal-d'),
            ('KBS1', '/networks/262/kbs1'), ('KBS2', '/networks/128/kbs2'),
            ('Keshet 12', '/networks/305/keshet-12'), ('La 1', '/networks/146/la-1'),
            ('La Sexta', '/networks/148/la-sexta'), ('Las Estrellas', '/networks/529/las-estrellas'),
            ('M-Net', '/networks/1030/m-net'), ('MAX', '/networks/1378/max'),
            ('MBC1', '/networks/410/mbc1'), ('MBC', '/networks/166/mbc'),
            ('MBS', '/networks/24/mbs'), ('Mnet', '/networks/247/mnet'),
            ('MTV Polska', '/networks/464/mtv-polska'), ('MTV Portugal', '/networks/1322/mtv-portugal'),
            ('MTV', '/networks/978/mtv'), ('MTV', '/networks/1235/mtv'),
            ('MTV', '/networks/1319/mtv'), ('National Geographic Abu Dhabi', '/networks/457/national-geographic-abu-dhabi'),
            ('Net5', '/networks/290/net5'), ('NHK BS Premium', '/networks/1292/nhk-bs-premium'),
            ('NHK Eductational TV', '/networks/1570/nhk-eductational-tv'), ('NHK World', '/networks/1096/nhk-world'),
            ('NHK', '/networks/281/nhk'), ('Nickelodeon', '/networks/436/nickelodeon'),
            ('NPO 1', '/networks/1018/npo-1'), ('NPO 2', '/networks/1019/npo-2'),
            ('NPO 3', '/networks/1020/npo-3'), ('NRK1', '/networks/91/nrk1'),
            ('NRK3', '/networks/494/nrk3'), ('NRK Super', '/networks/1526/nrk-super'),
            ('NTV', '/networks/137/ntv'), ('OCN', '/networks/267/ocn'),
            ('On Style', '/networks/431/on-style'), ('One HD 31', '/networks/1262/one-hd-31'),
            ('Planet TV', '/networks/1539/planet-tv'), ('Polsat', '/networks/335/polsat'),
            ('Prime', '/networks/358/prime'), ('PRO TV', '/networks/344/pro-tv'),
            ('Prva Srpska Televizija', '/networks/1387/prva-srpska-televizija'), ('RAI 1', '/networks/390/rai-1'),
            ('RAI 2', '/networks/437/rai-2'), ('Real Time', '/networks/1343/real-time'),
            ('Reshet 13', '/networks/1579/reshet-13'), ('RSI', '/networks/1583/rsi'),
            ('RTL4', '/networks/112/rtl4'), ('RTL5', '/networks/373/rtl5'),
            ('RTL7', '/networks/361/rtl7'), ('RTP1', '/networks/102/rtp1'),
            ('RTS1', '/networks/1315/rts1'), ('RTS Un', '/networks/985/rts-un'),
            ('RTVE', '/networks/147/rtve'), ('RTÉ2', '/networks/1054/rte2'),
            ('RTÉ ONE', '/networks/165/rte-one'), ('Ríkisútvarpið', '/networks/740/rikisutvarpid'),
            ('SBS 6', '/networks/139/sbs-6'), ('SBS MTV', '/networks/1265/sbs-mtv'),
            ('SBS', '/networks/127/sbs'), ('SET TV', '/networks/347/set-tv'),
            ('SET TV', '/networks/1055/set-tv'), ('Show TV', '/networks/755/show-tv'),
            ('SIC', '/networks/1312/sic'), ('Sjuan', '/networks/1462/sjuan'),
            ('Sjónvarp Símans', '/networks/1581/sjonvarp-simans'), ('Sky Atlantic', '/networks/231/sky-atlantic'),
            ('Sky Cinema', '/networks/370/sky-cinema'), ('Sky Uno', '/networks/299/sky-uno'),
            ('Sony Pal', '/networks/502/sony-pal'), ('Spike', '/networks/1495/spike'),
            ('SRF 1', '/networks/1008/srf-1'), ('Star TV', '/networks/409/star-tv'),
            ('Star World', '/networks/487/star-world'), ('SVT1', '/networks/155/svt1'),
            ('SVT2', '/networks/1341/svt2'), ('TBS', '/networks/159/tbs'),
            ('Telecinco', '/networks/96/telecinco'), ('Television Maldives', '/networks/1026/television-maldives'),
            ('Televisión de Galicia', '/networks/1308/television-de-galicia'), ('TET', '/networks/542/tet'),
            ('TG4', '/networks/275/tg4'), ('Three', '/networks/292/three'),
            ('TNT', '/networks/1659/tnt'), ('Tokai TV', '/networks/1327/tokai-tv'),
            ('Tokyo MX', '/networks/132/tokyo-mx'), ('TOP', '/networks/1651/top'),
            ('TRT1', '/networks/976/trt1'), ('TTV', '/networks/506/ttv'),
            ('TV2 Zebra', '/networks/491/tv2-zebra'), ('TV3', '/networks/152/tv3'),
            ('TV3', '/networks/492/tv3'), ('TV3', '/networks/558/tv3'),
            ('TV4', '/networks/123/tv4'), ('TV5', '/networks/1507/tv5'),
            ('TV8', '/networks/1251/tv8'), ('TV 2', '/networks/339/tv-2'),
            ('TV Aichi', '/networks/475/tv-aichi'), ('TV Asahi', '/networks/263/tv-asahi'),
            ('TV Norge', '/networks/314/tv-norge'), ('TV Tokyo', '/networks/76/tv-tokyo'),
            ('TVBS', '/networks/1324/tvbs'), ('TVE', '/networks/99/tve'),
            ('TVI', '/networks/1294/tvi'), ('tvN', '/networks/280/tvn'),
            ('TVN', '/networks/334/tvn'), ('TVNZ 1', '/networks/1031/tvnz-1'),
            ('TVNZ 2', '/networks/452/tvnz-2'), ('TVNZ Kidzone24', '/networks/1605/tvnz-kidzone24'),
            ('TVP1', '/networks/336/tvp1'), ('TVP2', '/networks/333/tvp2'),
            ('TyataTV', '/networks/1662/tyatatv'), ('Veronica', '/networks/972/veronica'),
            ('Viasat 4', '/networks/1373/viasat-4'), ('Virgin Media One', '/networks/323/virgin-media-one'),
            ('Workpoint TV', '/networks/1396/workpoint-tv'), ('WOWOW', '/networks/158/wowow'),
            ('Yes', '/networks/554/yes'), ('YTV', '/networks/476/ytv'),
            ('ZEE5', '/networks/1645/zee5'), ('À Punt', '/networks/1669/a-punt'),
            ('СТБ', '/networks/380/stb'), ('Інтер', '/networks/379/inter')
        ]
        for i in networks:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def tvOthers2networks(self):  # Other Countries 2
        networks = [
            ('2x2', '/networks/530/2x2'), ('Alpha', '/networks/1236/alpha'),
            ('Anhui Television', '/networks/1278/anhui-television'), ('Arte', '/networks/414/arte'),
            ('Beijing Television', '/networks/481/beijing-television'), ('BR Fernsehen', '/networks/1490/br-fernsehen'),
            ('bTV', '/networks/435/btv'), ('C8', '/networks/1641/c8'),
            ('Canal J', '/networks/1050/canal-j'), ('Canal+', '/networks/105/canal'),
            ('Canvas', '/networks/441/canvas'), ('Caracol Televisión', '/networks/1002/caracol-television'),
            ('Cartoon Network', '/networks/1653/cartoon-network'), ('CCTV-1', '/networks/1282/cctv-1'),
            ('Comedy Central', '/networks/1063/comedy-central'), ('СТС Kids', '/networks/1670/sts-kids'),
            ('СТС', '/networks/304/sts'), ('Das Erste', '/networks/360/das-erste'),
            ('Disney Channel', '/networks/1260/disney-channel'), ('DR1', '/networks/115/dr1'),
            ('DR2', '/networks/1501/dr2'), ('DR3', '/networks/141/dr3'),
            ('DR Ultra', '/networks/1635/dr-ultra'), ('Dragon Television', '/networks/302/dragon-television'),
            ('Duna TV', '/networks/413/duna-tv'), ('El Trece', '/networks/460/el-trece'),
            ('Fox Action Movies', '/networks/1588/fox-action-movies'), ('Fox Brasil', '/networks/1248/fox-brasil'),
            ('Fox Telecolombia', '/networks/1297/fox-telecolombia'), ('France 2', '/networks/106/france-2'),
            ('France 3', '/networks/249/france-3'), ('France 4', '/networks/405/france-4'),
            ('France 5', '/networks/980/france-5'), ('GNT', '/networks/1037/gnt'),
            ('HBO Latin America', '/networks/266/hbo-latin-america'), ('History', '/networks/1658/history'),
            ('HRT', '/networks/1255/hrt'), ('НТВ', '/networks/300/ntv'),
            ('Hunan Television', '/networks/276/hunan-television'), ('Jiangsu Television', '/networks/444/jiangsu-television'),
            ('Jim', '/networks/1537/jim'), ('Kanal 4', '/networks/1384/kanal-4'),
            ('Kanal 5', '/networks/246/kanal-5'), ('Карусель', '/networks/989/karusel'),
            ('Ketnet', '/networks/973/ketnet'), ('KiKa', '/networks/979/kika'),
            ('La Une', '/networks/1222/la-une'), ('Liaoning Television', '/networks/1097/liaoning-television'),
            ('Liv', '/networks/1538/liv'), ('M6', '/networks/478/m6'),
            ('Mega', '/networks/1587/mega'), ('МИР ТВ', '/networks/1519/mir-tv'),
            ('MTV3', '/networks/372/mtv3'), ('MTV Brasil', '/networks/1366/mtv-brasil'),
            ('Multishow', '/networks/282/multishow'), ('МУЛЬТ', '/networks/1316/mult'),
            ('NDR', '/networks/398/ndr'), ('Nelonen', '/networks/1329/nelonen'),
            ('Nolife', '/networks/986/nolife'), ('Nova TV', '/networks/332/nova-tv'),
            ('NRJ12', '/networks/1625/nrj12'), ('OCS City', '/networks/1613/ocs-city'),
            ('OCS Max', '/networks/432/ocs-max'), ('ORF 1', '/networks/235/orf-1'),
            ('ORF 2', '/networks/912/orf-2'), ('Planète+', '/networks/1333/planete'),
            ('Россия 1', '/networks/239/rossia-1'), ('Prima televize', '/networks/1484/prima-televize'),
            ('ProSieben', '/networks/348/prosieben'), ('PULS4', '/networks/1242/puls4'),
            ('Rede Bandeirantes', '/networks/1083/rede-bandeirantes'), ('Rede Globo', '/networks/374/rede-globo'),
            ('Rede Record', '/networks/375/rede-record'), ('RMC Découverte', '/networks/1036/rmc-decouverte'),
            ('RTL2', '/networks/442/rtl2'), ('RTL Klub', '/networks/426/rtl-klub'),
            ('RTL', '/networks/164/rtl'), ('Sat.1', '/networks/397/sat1'),
            ('Sky 1', '/networks/1355/sky-1'), ('Space', '/networks/1076/space'),
            ('Spektrum', '/networks/498/spektrum'), ('Star', '/networks/1456/star'),
            ('ТВ-3', '/networks/514/tv-3'), ('Telefe', '/networks/422/telefe'),
            ('TF1', '/networks/129/tf1'), ('TFX', '/networks/1624/tfx'),
            ('ТНТ', '/networks/308/tnt'), ('TMC', '/networks/1091/tmc'),
            ('TNT Serie', '/networks/462/tnt-serie'), ('TV2 Zulu', '/networks/1013/tv2-zulu'),
            ('TV2', '/networks/322/tv2'), ('TV2', '/networks/403/tv2'),
            ('TV3', '/networks/1058/tv3'), ('TV 2 Charlie', '/networks/1639/tv-2-charlie'),
            ('TV Nova', '/networks/1328/tv-nova'), ('TV Pública', '/networks/1046/tv-publica'),
            ('TVB HD Jade', '/networks/279/tvb-hd-jade'), ('TVB', '/networks/241/tvb'),
            ('VIASAT3', '/networks/401/viasat3'), ('VIASAT6', '/networks/1098/viasat6'),
            ('VIER', '/networks/381/vier'), ('VIJF', '/networks/408/vijf'),
            ('VOX', '/networks/518/vox'), ('VTM', '/networks/156/vtm'),
            ('W9', '/networks/1303/w9'), ('WDR', '/networks/508/wdr'),
            ('Yle TV1', '/networks/1385/yle-tv1'), ('Yle TV2', '/networks/534/yle-tv2'),
            ('ZDF', '/networks/109/zdf'), ('ZDFneo', '/networks/512/zdfneo'),
            ('Zhejiang Television', '/networks/1012/zhejiang-television'), ('één', '/networks/121/een'),
            ('Первый канал', '/networks/307/pervyj-kanal'), ('Пятница', '/networks/377/patnica'),
            ('ЦТ СССР', '/networks/1075/ct-sssr'), ('ΣΚΑΪ Τηλεόραση', '/networks/1351/skai-teleorase')
        ]
        for i in networks:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def webchannels(self):
        webchannels = [
            ('ABC iView', '/webchannels/149/abc-iview'), ('AbemaTV', '/webchannels/135/abematv'),
            ('Acorn TV', '/webchannels/129/acorn-tv'), ('AdultSwim.com', '/webchannels/110/adultswimcom'),
            ('All 4', '/webchannels/52/all-4'), ('AMC Premiere', '/webchannels/250/amc-premiere'),
            ('Amazon', '/webchannels/3/amazon'), ('AOL On', '/webchannels/28/aol-on'),
            ('Apple TV+', '/webchannels/310/apple-tv'), ('BBC iPlayer', '/webchannels/26/bbc-iplayer'),
            ('BBC Three', '/webchannels/71/bbc-three'), ('Bilibili', '/webchannels/51/bilibili'),
            ('Blackpills', '/webchannels/186/blackpills'), ('Blim', '/webchannels/197/blim'),
            ('Blip', '/webchannels/40/blip'), ('BluTV', '/webchannels/222/blutv'),
            ('Bon Appétit Video', '/webchannels/303/bon-appetit-video'), ('Brat', '/webchannels/274/brat'),
            ('C More', '/webchannels/170/c-more'), ('C More Finland', '/webchannels/306/c-more-finland'),
            ('Cartoon Hangover', '/webchannels/284/cartoon-hangover'), ('CBC', '/webchannels/108/cbc'),
            ('CBC Gem', '/webchannels/300/cbc-gem'), ('CBS All Access', '/webchannels/107/cbs-all-access'),
            ('CC: Studios', '/webchannels/73/cc-studios'), ('Collegehumor', '/webchannels/228/collegehumor'),
            ('Crackle', '/webchannels/4/crackle'), ('CraveTV', '/webchannels/109/cravetv'),
            ('CuriosityStream', '/webchannels/188/curiositystream'), ('CW Seed', '/webchannels/13/cw-seed'),
            ('DC Universe', '/webchannels/187/dc-universe'), ('Dekkoo', '/webchannels/174/dekkoo'),
            ('DisneyNOW', '/webchannels/83/disneynow'), ('Dropout', '/webchannels/311/dropout'),
            ('Elisa Viihde', '/webchannels/293/elisa-viihde'), ('EntertainTV', '/webchannels/247/entertaintv'),
            ('ESPN+', '/webchannels/265/espn'), ('Eyeslicer.com', '/webchannels/236/eyeslicercom'),
            ('FemininFeminin.com', '/webchannels/61/femininfeminincom'), ('France TV Slash', '/webchannels/252/france-tv-slash'),
            ('Funny or Die', '/webchannels/36/funny-or-die'), ('Globo Play', '/webchannels/131/globo-play'),
            ('Go90', '/webchannels/85/go90'), ('Hallmark Channel Everywhere', '/webchannels/98/hallmark-channel-everywhere'),
            ('HBO Go', '/webchannels/22/hbo-go'), ('History Channel', '/webchannels/94/history-channel'),
            ('Hotstar', '/webchannels/164/hotstar'), ('Hulu', '/webchannels/2/hulu'),
            ('Hulu Japan', '/webchannels/235/hulu-japan'), ('ICI Tou.tv', '/webchannels/301/ici-toutv'),
            ('iQiyi', '/webchannels/67/iqiyi'), ('ITV Hub', '/webchannels/54/itv-hub'),
            ('KPN Presenteert', '/webchannels/130/kpn-presenteert'), ('LINE TV', '/webchannels/88/line-tv'),
            ('Mango TV', '/webchannels/226/mango-tv'), ('Maxdome', '/webchannels/137/maxdome'),
            ('Melon', '/webchannels/240/melon'), ('Motor Trend On Demand', '/webchannels/200/motor-trend-on-demand'),
            ('Movistar+', '/webchannels/169/movistar'), ('MTV.com', '/webchannels/260/mtvcom'),
            ('Munchies', '/webchannels/225/munchies'), ('MyLifetime.com', '/webchannels/181/mylifetimecom'),
            ('Naver TVCast', '/webchannels/30/naver-tvcast'), ('Netflix', '/webchannels/1/netflix'),
            ('Nick.com', '/webchannels/263/nickcom'), ('Niconico', '/webchannels/93/niconico'),
            ('NRK.no', '/webchannels/238/nrkno'), ('Null Video', '/webchannels/296/null-video'),
            ('Olleh TV', '/webchannels/258/olleh-tv'), ('Puhu TV', '/webchannels/153/puhu-tv'),
            ('Rooster Teeth', '/webchannels/32/rooster-teeth'), ('RTBF Webcréation', '/webchannels/101/rtbf-webcreation'),
            ('Rutube', '/webchannels/99/rutube'), ('ScreenMagic TV', '/webchannels/201/screenmagic-tv'),
            ('Seeso', '/webchannels/77/seeso'), ('ShahrzadSeries.com', '/webchannels/80/shahrzadseriescom'),
            ('Showtime on Demand', '/webchannels/315/showtime-on-demand'), ('Sky Go', '/webchannels/117/sky-go'),
            ('Sky Go (DE)', '/webchannels/295/sky-go-de'), ('Sohu TV', '/webchannels/50/sohu-tv'),
            ('Spectrum On Demand', '/webchannels/316/spectrum-on-demand'), ('Stan', '/webchannels/64/stan'),
            ('StarzPlay', '/webchannels/46/starz-play'), ('Stream.cz', '/webchannels/38/streamcz'),
            ('Studio 4', '/webchannels/297/studio-4'), ('SVT Play', '/webchannels/190/svt-play'),
            ('Syfy', '/webchannels/49/syfy'), ('TBS.com', '/webchannels/224/tbscom'),
            ('Tencent QQ', '/webchannels/104/tencent-qq'), ('The Fantasy Network', '/webchannels/305/the-fantasy-network'),
            ('ToonsTV', '/webchannels/192/toonstv'), ('TV4 Play', '/webchannels/155/tv4-play'),
            ('TVFPlay', '/webchannels/152/tvfplay'), ('TWiT', '/webchannels/102/twit'),
            ('TYT', '/webchannels/189/tyt'), ('UFC Fight Pass', '/webchannels/45/ufc-fight-pass'),
            ('UMC', '/webchannels/209/umc'), ('V LIVE', '/webchannels/122/v-live'),
            ('Videoland', '/webchannels/12/videoland'), ('VRV Select', '/webchannels/221/vrv-select'),
            ('WOW Presents', '/webchannels/195/wow-presents'), ('WWE Network', '/webchannels/15/wwe-network'),
            ('Yle Areena', '/webchannels/220/yle-areena'), ('Youku', '/webchannels/118/youku'),
            ('YouTube', '/webchannels/21/youtube'), ('YouTube Premium', '/webchannels/43/youtube-premium')
        ]
        for i in webchannels:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': 'networks.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def languages(self):
        languages = [('Arabic', 'ar'), ('Bosnian', 'bs'), ('Bulgarian', 'bg'), ('Chinese', 'zh'), ('Croatian', 'hr'), ('Dutch', 'nl'),
            ('English', 'en'), ('Finnish', 'fi'), ('French', 'fr'), ('German', 'de'), ('Greek', 'el'), ('Hebrew', 'he'), ('Hindi ', 'hi'),
            ('Hungarian', 'hu'), ('Icelandic', 'is'), ('Italian', 'it'), ('Japanese', 'ja'), ('Korean', 'ko'), ('Norwegian', 'no'),
            ('Persian', 'fa'), ('Polish', 'pl'), ('Portuguese', 'pt'), ('Punjabi', 'pa'), ('Romanian', 'ro'), ('Russian', 'ru'),
            ('Serbian', 'sr'), ('Spanish', 'es'), ('Swedish', 'sv'), ('Turkish', 'tr'), ('Ukrainian', 'uk')
        ]
        for i in languages:
            self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'languages.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = ['TV-G', 'TV-PG', 'TV-14', 'TV-MA']
        for i in certificates:
            self.list.append({'name': str(i), 'url': self.certification_link % str(i).replace('-', '-'), 'image': 'certificates.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def my_imdbUserLists(self):
        tvlist1 = control.setting('imdb.tvlist_name1')
        tvlist1_link = control.setting('imdb.tvlist_id1')
        if tvlist1:
            self.list.append({'name': tvlist1, 'url': self.imdbUserLists_link % tvlist1_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist2 = control.setting('imdb.tvlist_name2')
        tvlist2_link = control.setting('imdb.tvlist_id2')
        if tvlist2:
            self.list.append({'name': tvlist2, 'url': self.imdbUserLists_link % tvlist2_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist3 = control.setting('imdb.tvlist_name3')
        tvlist3_link = control.setting('imdb.tvlist_id3')
        if tvlist3:
            self.list.append({'name': tvlist3, 'url': self.imdbUserLists_link % tvlist3_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist4 = control.setting('imdb.tvlist_name4')
        tvlist4_link = control.setting('imdb.tvlist_id4')
        if tvlist4:
            self.list.append({'name': tvlist4, 'url': self.imdbUserLists_link % tvlist4_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist5 = control.setting('imdb.tvlist_name5')
        tvlist5_link = control.setting('imdb.tvlist_id5')
        if tvlist5:
            self.list.append({'name': tvlist5, 'url': self.imdbUserLists_link % tvlist5_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist6 = control.setting('imdb.tvlist_name6')
        tvlist6_link = control.setting('imdb.tvlist_id6')
        if tvlist6:
            self.list.append({'name': tvlist6, 'url': self.imdbUserLists_link % tvlist6_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist7 = control.setting('imdb.tvlist_name7')
        tvlist7_link = control.setting('imdb.tvlist_id7')
        if tvlist7:
            self.list.append({'name': tvlist7, 'url': self.imdbUserLists_link % tvlist7_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist8 = control.setting('imdb.tvlist_name8')
        tvlist8_link = control.setting('imdb.tvlist_id8')
        if tvlist8:
            self.list.append({'name': tvlist8, 'url': self.imdbUserLists_link % tvlist8_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist9 = control.setting('imdb.tvlist_name9')
        tvlist9_link = control.setting('imdb.tvlist_id9')
        if tvlist9:
            self.list.append({'name': tvlist9, 'url': self.imdbUserLists_link % tvlist9_link, 'image': 'imdb.png', 'action': 'tvshows'})
        tvlist10 = control.setting('imdb.tvlist_name10')
        tvlist10_link = control.setting('imdb.tvlist_id10')
        if tvlist10:
            self.list.append({'name': tvlist10, 'url': self.imdbUserLists_link % tvlist10_link, 'image': 'imdb.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def imdbUserLists(self):
        theUserLists = [
            ('12 Binge-worthy TV Series for the Entire Family', 'ls074445642'),
            ('15 Most Popular Shows on Prime Video - December 2018', 'ls024969858'),
            ('20 Top-Rated Shows on Prime Video', 'ls029077018'),
            ('Animated TV Shows to Stream Now With Prime Video', 'ls026477582'),
            ('BABYLON 5', 'ls021151794'),
            ('BATTLESTAR GALACTICA', 'ls021157840'),
            ('Best Animated TV Series:The Ultimate List', 'ls051776122'),
            ('Best Detective Films and TV series:The Ultimate List', 'ls059511321'),
            ('Best TV Drama:The Ultimate List', 'ls008946393'),
            ('Binge-Worthy TV Shows on Amazon Video', 'ls063527487'),
            ('DOCTOR WHO', 'ls021157820'),
            ('Favorite TV Shows to Binge-Watch', 'ls070237860'),
            ('FIREFLY/SERENITY', 'ls021151557'),
            ('FLASH GORDON', 'ls021151066'),
            ('Globe-Nominated TV Shows on Amazon Video', 'ls062059342'),
            ('Great Late-Night TV on Amazon Instant Video', 'ls002595589'),
            ('Holiday TV Viewing Guide', 'ls016086573'),
            ('IMDb 25: Top 25 TV Shows by User Rating From the Last 25 Years', 'ls079394864'),
            ('Popular on Amazon Video: Top TV Shows', 'ls036998982'),
            ('STAR TREK', 'ls021157975'),
            ('STAR WARS', 'ls021157942'),
            ('STARGATE', 'ls021151078'),
            ('Streaming TV Trending Title List', 'ls069851333'),
            ('The 30 Best Daytime Soaps of All Time', 'ls000719664'),
            ('THE OUTER LIMITS', 'ls021157853'),
            ('The Top 200 TV Shows as Rated by Women on IMDb in 2018', 'ls023589152'),
            ('THE TWILIGHT ZONE', 'ls021157816'),
            ('THE X-FILES', 'ls021151086'),
            ('toddler', 'ls021175534'),
            ('Top 100 TV Shows as Rated by Women on IMDb in 2016', 'ls033953812'),
            ('Top Picks for Weekend Binge-Watching', 'ls020221909'),
            ('Where to Watch Your Favorite DC, Marvel, and Other Superhero TV Shows', 'ls021847943')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.imdbUserLists_link % i[1], 'image': 'imdb.png', 'action': 'tvshows'})
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
            ('spirituality'), ('spoof'), ('star-wars'), ('steampunk'), ('subjective-camera'), ('superhero'),
            ('supernatural'), ('surprise-ending'), ('survival-horror'), ('swashbuckler'), ('sword-and-sandal'), ('tech-noir'),
            ('thanksgiving'), ('time-travel'), ('title-spoken-by-character'), ('told-in-flashback'), ('vampire'), ('virtual-reality'),
            ('voice-over-narration'), ('war-violence'), ('whistleblower'), ('wilhelm-scream'), ('wuxia'), ('zombie')
        ]
        for i in interestingKeywords:
            self.list.append({'name': i.replace('-', ' '), 'url': self.exploreKeywords_link % i, 'image': 'imdb.png', 'action': 'tvshows'})
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
            self.list[i].update({'image': 'userlists.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def trakt_list(self, url, user):
        try:
            dupes = []
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            result = trakt.getTraktAsJson(u)
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
                year = item['year']
                year = re.sub('[^0-9]', '', str(year))
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                tvdb = item['ids']['tvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                if tvdb == None or tvdb == '' or tvdb in dupes:
                    raise Exception()
                dupes.append(tvdb)
                try:
                    premiered = item['first_aired']
                except:
                    premiered = '0'
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                try:
                    studio = item['network']
                except:
                    studio = '0'
                if studio == None:
                    studio = '0'
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
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot, 'imdb': imdb, 'tvdb': tvdb, 'poster': '0', 'next': next})
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
            dupes = []
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
                if '/nopicture/' in poster:
                    poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
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
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'rating': rating, 'plot': plot, 'imdb': imdb, 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass
        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs = {'class': '.+? mode-detail'})
        except:
            return
        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = client.replaceHTMLCodes(name)
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
                url = url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass
        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def tvmaze_list(self, url):
        try:
            result = client.request(url)
            result = client.parseDOM(result, 'section', attrs={'id': 'this-seasons-shows'})
            items = client.parseDOM(result, 'div', attrs={'class': 'content auto cell'})
            items = [client.parseDOM(i, 'a', ret='href') for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = [re.findall('/(\d+)/', i) for i in items]
            items = [i[0] for i in items if len(i) > 0]
            items = items[:50]
        except:
            return


        def items_list(i):
            try:
                url = self.tvmaze_info_link % i
                item = client.request(url)
                item = json.loads(item)
                title = item['name']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['premiered']
                year = re.findall('(\d{4})', year)[0]
                year = year.encode('utf-8')
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                imdb = item['externals']['imdb']
                if imdb == None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')
                tvdb = item['externals']['thetvdb']
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = tvdb.encode('utf-8')
                if tvdb == None or tvdb == '':
                    raise Exception()
                try:
                    poster = item['image']['original']
                except:
                    poster = '0'
                if poster == None or poster == '':
                    poster = '0'
                poster = poster.encode('utf-8')
                premiered = item['premiered']
                try:
                    premiered = re.findall('(\d{4}-\d{2}-\d{2})', premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')
                try:
                    studio = item['network']['name']
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
                    duration = item['runtime']
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'
                duration = str(duration)
                duration = duration.encode('utf-8')
                try:
                    rating = item['rating']['average']
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'
                rating = str(rating)
                rating = rating.encode('utf-8')
                try:
                    plot = item['summary']
                except:
                    plot = '0'
                if plot == None:
                    plot = '0'
                plot = re.sub('<.+?>|</.+?>|\n', '', plot)
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                try:
                    content = item['type'].lower()
                except:
                    content = '0'
                if content == None or content == '':
                    content = '0'
                content = content.encode('utf-8')
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'plot': plot, 'imdb': imdb, 'tvdb': tvdb, 'poster': poster, 'content': content})
            except:
                pass
        try:
            threads = []
            for i in items:
                threads.append(workers.Thread(items_list, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            filter = [i for i in self.list if i['content'] == 'scripted']
            filter += [i for i in self.list if not i['content'] == 'scripted']
            self.list = filter
            return self.list
        except:
            return


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
        self.list = [i for i in self.list if not i['tvdb'] == '0']
        if self.fanart_tv_user == '':
            for i in self.list:
                i.update({'clearlogo': '0', 'clearart': '0'})


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                raise Exception()
            imdb = self.list[i]['imdb'] if 'imdb' in self.list[i] else '0'
            tvdb = self.list[i]['tvdb'] if 'tvdb' in self.list[i] else '0'
            if imdb == '0':
                try:
                    imdb = \
                    trakt.SearchTVShow(urllib.quote_plus(self.list[i]['title']), self.list[i]['year'], full=False)[0]
                    imdb = imdb.get('show', '0')
                    imdb = imdb.get('ids', {}).get('imdb', '0')
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    if not imdb:
                        imdb = '0'
                except:
                    imdb = '0'
            if tvdb == '0' and not imdb == '0':
                url = self.tvdb_by_imdb % imdb
                result = client.request(url, timeout='10')
                try:
                    tvdb = client.parseDOM(result, 'seriesid')[0]
                except:
                    tvdb = '0'
                try:
                    name = client.parseDOM(result, 'SeriesName')[0]
                except:
                    name = '0'
                dupe = re.findall('[***]Duplicate (\d*)[***]', name)
                if dupe:
                    tvdb = str(dupe[0])
                if tvdb == '':
                    tvdb = '0'
            if tvdb == '0':
                url = self.tvdb_by_query % (urllib.quote_plus(self.list[i]['title']))
                years = [str(self.list[i]['year']), str(int(self.list[i]['year']) + 1), str(int(self.list[i]['year']) - 1)]
                tvdb = client.request(url, timeout='10')
                tvdb = re.sub(r'[^\x00-\x7F]+', '', tvdb)
                tvdb = client.replaceHTMLCodes(tvdb)
                tvdb = client.parseDOM(tvdb, 'Series')
                tvdb = [(x, client.parseDOM(x, 'SeriesName'), client.parseDOM(x, 'FirstAired')) for x in tvdb]
                tvdb = [(x, x[1][0], x[2][0]) for x in tvdb if len(x[1]) > 0 and len(x[2]) > 0]
                tvdb = [x for x in tvdb if cleantitle.get(self.list[i]['title']) == cleantitle.get(x[1])]
                tvdb = [x[0][0] for x in tvdb if any(y in x[2] for y in years)][0]
                tvdb = client.parseDOM(tvdb, 'seriesid')[0]
                if tvdb == '':
                    tvdb = '0'
            url = self.tvdb_info_link % tvdb
            item = client.request(url, timeout='10')
            if item == None:
                raise Exception()
            if imdb == '0':
                try:
                    imdb = client.parseDOM(item, 'IMDB_ID')[0]
                except:
                    pass
                if imdb == '':
                    imdb = '0'
                imdb = imdb.encode('utf-8')
            try:
                title = client.parseDOM(item, 'SeriesName')[0]
            except:
                title = ''
            if title == '':
                title = '0'
            title = client.replaceHTMLCodes(title)
            title = title.encode('utf-8')
            try:
                year = client.parseDOM(item, 'FirstAired')[0]
            except:
                year = ''
            try:
                year = re.compile('(\d{4})').findall(year)[0]
            except:
                year = ''
            if year == '':
                year = '0'
            year = year.encode('utf-8')
            try:
                premiered = client.parseDOM(item, 'FirstAired')[0]
            except:
                premiered = '0'
            if premiered == '':
                premiered = '0'
            premiered = client.replaceHTMLCodes(premiered)
            premiered = premiered.encode('utf-8')
            try:
                studio = client.parseDOM(item, 'Network')[0]
            except:
                studio = ''
            if studio == '':
                studio = '0'
            studio = client.replaceHTMLCodes(studio)
            studio = studio.encode('utf-8')
            try:
                genre = client.parseDOM(item, 'Genre')[0]
            except:
                genre = ''
            genre = [x for x in genre.split('|') if not x == '']
            genre = ' / '.join(genre)
            if genre == '':
                genre = '0'
            genre = client.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')
            try:
                duration = client.parseDOM(item, 'Runtime')[0]
            except:
                duration = ''
            if duration == '':
                duration = '0'
            duration = client.replaceHTMLCodes(duration)
            duration = duration.encode('utf-8')
            try:
                rating = client.parseDOM(item, 'Rating')[0]
            except:
                rating = ''
            if 'rating' in self.list[i] and not self.list[i]['rating'] == '0':
                rating = self.list[i]['rating']
            if rating == '':
                rating = '0'
            rating = client.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')
            try:
                votes = client.parseDOM(item, 'RatingCount')[0]
            except:
                votes = ''
            if 'votes' in self.list[i] and not self.list[i]['votes'] == '0':
                votes = self.list[i]['votes']
            if votes == '':
                votes = '0'
            votes = client.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')
            try:
                mpaa = client.parseDOM(item, 'ContentRating')[0]
            except:
                mpaa = ''
            if mpaa == '':
                mpaa = '0'
            mpaa = client.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')
            try:
                cast = client.parseDOM(item, 'Actors')[0]
            except:
                cast = ''
            cast = [x for x in cast.split('|') if not x == '']
            try:
                cast = [(x.encode('utf-8'), '') for x in cast]
            except:
                cast = []
            if cast == []:
                cast = '0'
            try:
                plot = client.parseDOM(item, 'Overview')[0]
            except:
                plot = ''
            if plot == '':
                plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')
            try:
                poster = client.parseDOM(item, 'poster')[0]
            except:
                poster = ''
            if not poster == '':
                poster = self.tvdb_image + poster
            else:
                poster = '0'
            if 'poster' in self.list[i] and poster == '0':
                poster = self.list[i]['poster']
            poster = client.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')
            try:
                banner = client.parseDOM(item, 'banner')[0]
            except:
                banner = ''
            if not banner == '':
                banner = self.tvdb_image + banner
            else:
                banner = '0'
            banner = client.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')
            try:
                fanart = client.parseDOM(item, 'fanart')[0]
            except:
                fanart = ''
            if not fanart == '':
                fanart = self.tvdb_image + fanart
            else:
                fanart = '0'
            fanart = client.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')
            try:
                artmeta = True
                # if self.fanart_tv_user == '': raise Exception()
                art = client.request(self.fanart_tv_art_link % tvdb, headers=self.fanart_tv_headers, timeout='10', error=True)
                try:
                    art = json.loads(art)
                except:
                    artmeta = False
            except:
                pass
            try:
                poster2 = art['tvposter']
                poster2 = [x for x in poster2 if x.get('lang') == self.lang][::-1] + [x for x in poster2 if x.get('lang') == 'en'][::-1] + [x for x in poster2 if x.get('lang') in ['00', '']][::-1]
                poster2 = poster2[0]['url'].encode('utf-8')
            except:
                poster2 = '0'
            try:
                fanart2 = art['showbackground']
                fanart2 = [x for x in fanart2 if x.get('lang') == self.lang][::-1] + [x for x in fanart2 if x.get('lang') == 'en'][::-1] + [x for x in fanart2 if x.get('lang') in ['00', '']][::-1]
                fanart2 = fanart2[0]['url'].encode('utf-8')
            except:
                fanart2 = '0'
            try:
                banner2 = art['tvbanner']
                banner2 = [x for x in banner2 if x.get('lang') == self.lang][::-1] + [x for x in banner2 if x.get('lang') == 'en'][::-1] + [x for x in banner2 if x.get('lang') in ['00', '']][::-1]
                banner2 = banner2[0]['url'].encode('utf-8')
            except:
                banner2 = '0'
            try:
                if 'hdtvlogo' in art:
                    clearlogo = art['hdtvlogo']
                else:
                    clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == self.lang][::-1] + [x for x in clearlogo if x.get('lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = clearlogo[0]['url'].encode('utf-8')
            except:
                clearlogo = '0'
            try:
                if 'hdclearart' in art:
                    clearart = art['hdclearart']
                else:
                    clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == self.lang][::-1] + [x for x in clearart if x.get('lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = clearart[0]['url'].encode('utf-8')
            except:
                clearart = '0'
            item = {'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb, 'poster': poster, 'poster2': poster2, 'banner': banner, 'banner2': banner2, 'fanart': fanart, 'fanart2': fanart2, 'clearlogo': clearlogo, 'clearart': clearart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot}
            item = dict((k, v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)
            if artmeta == False:
                raise Exception()
            meta = {'imdb': imdb, 'tvdb': tvdb, 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
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


