# -*- coding: utf-8 -*-

import os,base64,sys,urllib2,urlparse,xbmc,xbmcaddon,xbmcgui
from resources.lib.modules import control,cache,trakt

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; control.moderator()
artPath = control.artPath() ; addonFanart = control.addonFanart()
imdbCredentials = False if control.setting('imdb.user') == '' else True
traktCredentials = trakt.getTraktCredentialsInfo()
traktIndicators = trakt.getTraktIndicatorsInfo()
queueMenu = control.lang(32065).encode('utf-8')

DBIRDSTAT = (xbmcaddon.Addon('script.module.resolveurl').getSetting('RealDebridResolver_enabled'))
isDbird = 'lime' if DBIRDSTAT == 'true' else 'darkorange'
ADBIRDSTAT = (xbmcaddon.Addon('script.module.resolveurl').getSetting('AllDebridResolver_enabled'))
isAdbird = 'lime' if ADBIRDSTAT == 'true' else 'darkorange'
PREMESTAT = (xbmcaddon.Addon('script.module.resolveurl').getSetting('PremiumizeMeResolver_enabled'))
isPreMe = 'lime' if PREMESTAT == 'true' else 'darkorange'


class navigator:
    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'):
            return False
        return True


    def root(self):
        self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')
        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(32329, 'mylistsNavigator', 'mymovies.png', 'DefaultSets.png')
        if not control.setting('movie.widget') == '0':
            self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')
        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')
        if self.getMenuEnabled('navi.channels') == True:
            self.addDirectoryItem(32642, 'channels', 'channels.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.userlists') == True:
            self.addDirectoryItem(42003, 'imdbLists', 'imdb.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.userlists2') == True:
            self.addDirectoryItem(42001, 'tmdbLists', 'tmdb.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.morestuff') == True:
            self.addDirectoryItem(42004, 'moreplugs', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(42006, 'searchNavigator', 'search.png', 'DefaultFolder.png')
        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.changeLog') == True:
            self.addDirectoryItem(42007,  'ShowChangelog',  'icon.png',  'DefaultFolder.png', isFolder=False)
        if self.getMenuEnabled('navi.dev') == True:
            self.addDirectoryItem(32007, 'devtoolNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.endDirectory()


    def movies(self):
        if self.getMenuEnabled('navi.moviegenre') == True:
            self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieyears') == True:
            self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviepersons') == True:
            self.addDirectoryItem(32013, 'moviePersons', 'people.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movielanguages') == True:
            self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviecerts') == True:
            self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieMosts') == True:
            self.addDirectoryItem(42009, 'movieMosts', 'people-watching.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviefeat') == True:
            self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.png', 'imdb.png')
            self.addDirectoryItem(42010, 'movies2&url=featured', 'featured.png', 'DefaultMovies.png')
            self.addDirectoryItem(42011, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movietrending') == True:
            self.addDirectoryItem(32017, 'movies&url=trending', 'trakt.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.moviepopular') == True:
            self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
            self.addDirectoryItem(32323, 'movies&url=traktpopular', 'trakt.png', 'DefaultRecentlyAddedMovies.png')
            self.addDirectoryItem(42012, 'movies2&url=popular', 'most-popular.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieviews') == True:
            self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
            self.addDirectoryItem(42013, 'movies2&url=toprated', 'movies.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movieboxoffice') == True:
            self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
            self.addDirectoryItem(32020, 'movies&url=traktboxoffice', 'trakt.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.movieAnticipated') == True:
            self.addDirectoryItem(32322, 'movies&url=traktanticipated', 'trakt.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviepremiere') == True:
            self.addDirectoryItem(42014, 'movies2&url=premiere', 'movies.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movietheaters') == True:
            self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
            self.addDirectoryItem(42015, 'movies&url=theatersOld', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
            self.addDirectoryItem(42016, 'movies2&url=theaters', 'movies.png', 'DefaultRecentlyAddedMovies.png')
        if self.getMenuEnabled('navi.movieoscars') == True:
            self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
        self.endDirectory()


    def tvshows(self):
        if self.getMenuEnabled('navi.tvGenres') == True:
            self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvNetworks') == True:
            self.addDirectoryItem(32016, 'tvNetworksNavigator', 'networks.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvLanguages') == True:
            self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvCertificates') == True:
            self.addDirectoryItem(32015, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvfeat') == True:
            self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(42010, 'tvshows2&url=featured', 'featured.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvTrending') == True:
            self.addDirectoryItem(32017, 'tvshows&url=trending', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png')
        if self.getMenuEnabled('navi.tvPopular') == True:
            self.addDirectoryItem(42012, 'tvshows2&url=popular', 'most-popular.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32323, 'tvshows&url=traktpopular', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvRating') == True:
            self.addDirectoryItem(42017, 'tvshows2&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvViews') == True:
            self.addDirectoryItem(42018, 'tvshows2&url=views', 'movies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvshowMosts') == True:
            self.addDirectoryItem(42019, 'showMosts', 'people-watching.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAiring') == True:
            self.addDirectoryItem(42020, 'tvshows2&url=airing', 'airing-today.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvActive') == True:
            self.addDirectoryItem(42021, 'tvshows2&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAnticipated') == True:
            self.addDirectoryItem(32322, 'tvshows&url=traktanticipated', 'trakt.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvPremier') == True:
            self.addDirectoryItem(42022, 'tvshows2&url=premiere', 'movies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAdded') == True:
            self.addDirectoryItem(32031, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        if self.getMenuEnabled('navi.tvCalendar') == True:
            self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')
        self.endDirectory()


    def movieMosts(self):
		self.addDirectoryItem('Most Played This Week', 'movies&url=played1', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Played This Month', 'movies&url=played2', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Played This Year', 'movies&url=played3', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Played All Time', 'movies&url=played4', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Collected This Week', 'movies&url=collected1', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Collected This Month', 'movies&url=collected2', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Collected This Year', 'movies&url=collected3', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Collected All Time', 'movies&url=collected4', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Watched This Week', 'movies&url=watched1', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Watched This Month', 'movies&url=watched2', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Watched This Year', 'movies&url=watched3', 'most-popular.png', 'DefaultMovies.png')
		self.addDirectoryItem('Most Watched All Time', 'movies&url=watched4', 'most-popular.png', 'DefaultMovies.png')
		self.endDirectory()	


    def showMosts(self):
		self.addDirectoryItem('Most Played This Week', 'tvshows&url=played1', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Played This Month', 'tvshows&url=played2', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Played This Year', 'tvshows&url=played3', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Played All Time', 'tvshows&url=played4', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Collected This Week', 'tvshows&url=collected1', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Collected This Month', 'tvshows&url=collected2', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Collected This Year', 'tvshows&url=collected3', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Collected All Time', 'tvshows&url=collected4', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Watched This Week', 'tvshows&url=watched1', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Watched This Month', 'tvshows&url=watched2', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Watched This Year', 'tvshows&url=watched3', 'most-popular.png', 'DefaultTVShows.png')
		self.addDirectoryItem('Most Watched All Time', 'tvshows&url=watched4', 'most-popular.png', 'DefaultTVShows.png')
		self.endDirectory()


    def tvNetworksNavigator(self):
        self.addDirectoryItem('WebChannels', 'tvWebChannels', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem('United States', 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Canada', 'tvCanadanetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem('United Kingdom', 'tvUnitedKingdomnetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Australia', 'tvAustralianetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Other Countries 1', 'tvOthers1networks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Other Countries 2', 'tvOthers2networks', 'networks.png', 'DefaultTVShows.png')
        self.endDirectory()


    def imdbLists(self):
        self.addDirectoryItem('My IMDb Movie Lists', 'myimdbMovieLists', 'imdb.png', 'DefaultVideoPlaylists.png')
        self.addDirectoryItem('My IMDb TV Lists', 'myimdbTvLists', 'imdb.png', 'DefaultVideoPlaylists.png')
        self.addDirectoryItem('Explore Keywords(Movies)', 'movieExploreKeywords', 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('Explore Keywords(TV Shows)', 'tvshowExploreKeywords', 'imdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Explore UserLists(Movies)', 'movieimdbUserLists', 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('Explore UserLists(TV Shows)', 'tvshowimdbUserLists', 'imdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Hella LifeTime & HallMark Movies', 'hellaLifeTimeHallMark', 'imdb.png', 'DefaultVideoPlaylists.png')
        self.endDirectory()


    def tmdbLists(self):
        self.addDirectoryItem('My TMDb Movie Lists', 'mytmdbMovieLists', 'tmdb.png', 'DefaultVideoPlaylists.png')
        self.addDirectoryItem('My TMDb TV Lists', 'mytmdbTvLists', 'tmdb.png', 'DefaultVideoPlaylists.png')
        self.addDirectoryItem('Actor Collections(Movies)', 'tmdbActorCollections', 'tmdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('DC vs Marvel(Movies)', 'tmdbDCvsMarvel', 'tmdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('Holidays(Movies)', 'tmdbHolidays', 'tmdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('Assortment of Lists(Movies)', 'tmdbAssortment', 'tmdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('Collections(Movies)', 'tmdbCollections', 'tmdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('Collections Dupes(Movies)', 'tmdbCollectionsDupes', 'tmdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('TV Show Lists(TV Shows)', 'tmdbUserLists', 'tmdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Hulu Originals(TV Shows)', 'tvshows2&url=tmdbhuluorig', 'tmdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Netflix Originals(TV Shows)', 'tvshows2&url=tmdbnetflixorig', 'tmdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Amazon Originals(TV Shows)', 'tvshows2&url=tmdbamazonorig', 'tmdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Jew Movies', 'movies2&url=tmdbjewmovies', 'tmdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('Jew Top 250 TV Shows', 'tvshows2&url=tmdbjew250tv', 'tmdb.png', 'DefaultTVShows.png')
        self.endDirectory()


    def moreplugs(self):
        self.addDirectoryItem('WatchWrestling',  'wrestlingNavigator',  'highly-rated.png',  'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.customList') == True:
            self.addDirectoryItem('Custom List', 'navCustom', 'channels.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.iptvChannels') == True:
            self.addDirectoryItem(42023, 'iptvNavigator', 'channels.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.jewMC') == True:
            self.addDirectoryItem(42024, 'jewMC', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.radio') == True:
            self.addDirectoryItem(42025, 'radioNavigator', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        self.addDirectoryItem('High Times', 'hightimesNavigator', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.movieReviews') == True:
            self.addDirectoryItem(32623, 'movieReviews', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.tvReviews') == True:
            self.addDirectoryItem(326232, 'tvReviews', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.docuHeaven') == True:
            self.addDirectoryItem(32631, 'docuHeaven', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.kidscorner') == True:
            self.addDirectoryItem(32610, 'kidscorner', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.fitness') == True:
            self.addDirectoryItem(32611, 'fitness', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.legends') == True:
            self.addDirectoryItem(32612, 'legends', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.podcast') == True:
            self.addDirectoryItem(32620, 'podcastNavigator', 'highly-rated.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.xxx') == True:
            self.addDirectoryItem('[COLOR black]xxx[/COLOR]', 'navXXX', 'highly-rated.png', 'DefaultTVShows.png')
        self.endDirectory()


    def iptvplug(self):
        self.addDirectoryItem('AcronaiTV',  'acronaitv_menu',  'channels.png',  'DefaultTVShows.png')
        self.addDirectoryItem('usTVgo', 'ustvgoNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem('StreamLive', 'streamliveNavigator', 'channels.png', 'DefaultTVShows.png')
        self.addDirectoryItem(42023, 'iptvChannels', 'channels.png', 'DefaultTVShows.png')
        self.endDirectory()


    def mylists(self):
        self.addDirectoryItem(32003, 'myTraktMoviesNav', 'trakt.png', 'DefaultSets.png')
        self.addDirectoryItem(32004, 'myTraktTvShowsNav', 'trakt.png', 'DefaultSets.png')
        self.addDirectoryItem(32003, 'myIMDbMoviesNav', 'imdb.png', 'DefaultSets.png')
        self.addDirectoryItem(32004, 'myIMDbTvShowsNav', 'imdb.png', 'DefaultSets.png')
        self.addDirectoryItem(32541, 'libraryNavigator', 'mymovies.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')
        self.endDirectory()


    def mytraktmovies(self):
        if traktCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
        if traktIndicators == True:
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32028, 'movies&url=onDeckMovies', 'trakt.png', 'DefaultMovies.png', queue=True)
        self.addDirectoryItem(32039, 'movieUserlists', 'mymovies.png', 'DefaultMovies.png')
        self.endDirectory()


    def mytrakttvshows(self):
        if traktCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
        if traktIndicators == True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32028, 'tvshows&url=onDeckTV', 'trakt.png', 'DefaultTVShows.png', queue=True)
        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'mytvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32040, 'tvUserlists', 'mytvshows.png', 'DefaultTVShows.png')
        self.endDirectory()


    def myimdbmovies(self):
        if imdbCredentials == True:
            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)
        self.endDirectory()


    def myimdbtvshows(self):
        if imdbCredentials == True:
            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')
        self.endDirectory()


    def library(self):
        movie_library = control.setting('library.movie')
        tv_library = control.setting('library.tv')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
        if len(control.listDir(movie_library)[0]) > 0:
            self.addDirectoryItem(32559, movie_library, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_library)[0]) > 0:
            self.addDirectoryItem(32560, tv_library, 'tvshows.png', 'DefaultTVShows.png', isAction=False)
        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')
        self.endDirectory()


    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')
        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)
        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32047, 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32641, 'openSettings&query=7.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32540, 'urlResolver', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32613, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32614, 'clearMetaCache', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32604, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32051, 'clearResolveURLcache', 'urlresolver.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[COLOR %s][X][/COLOR]-Toggle RealDebrid (ResolveURL)' % isDbird, 'ToggleDbird', 'urlresolver.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[COLOR %s][X][/COLOR]-Toggle AllDebrid (ResolveURL)' % isAdbird, 'ToggleAdbird', 'urlresolver.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[COLOR %s][X][/COLOR]-Toggle PremiumizeMe (ResolveURL)' % isPreMe, 'TogglePreMe', 'urlresolver.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32073, 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(42026,  'PairEm',  'tools.png',  'DefaultAddonProgram.png', isFolder=False)
        self.endDirectory()


    def devtools(self):
        #self.addDirectoryItem('Toon Navigator', 'toonNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('Test Movies(TMDB)', 'movies2&url=tmdbjewtestmovies', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem('Test Shows(TMDB)', 'tvshows2&url=tmdbjewtestshows', 'tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32047, 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32641, 'openSettings&query=7.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32613, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32051, 'clearResolveURLcache', 'urlresolver.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32540, 'urlResolver', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[COLOR %s][X][/COLOR]-Toggle RealDebrid (ResolveURL)' % isDbird, 'ToggleDbird', 'urlresolver.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[COLOR %s][X][/COLOR]-Toggle AllDebrid (ResolveURL)' % isAdbird, 'ToggleAdbird', 'urlresolver.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[COLOR %s][X][/COLOR]-Toggle PremiumizeMe (ResolveURL)' % isPreMe, 'TogglePreMe', 'urlresolver.png', 'DefaultAddonProgram.png', isFolder=False)
        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
        self.endDirectory()


    def views(self):
        try:
            control.idle()
            items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]
            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))
            if select == -1:
                return
            content = items[select][1]
            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)
            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()
            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)
            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()


    def infoCheck(self, version):
        try:
            control.infoDialog('', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def clearCacheSearch(self):
        control.idle()
        if control.yesnoDialog(control.lang(32056).encode('utf-8'), '', ''):
            control.setSetting('tvsearch', '')
            control.setSetting('moviesearch', '')
            control.refresh()


    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


    def Toggle_Dbird(self):
        HMMMPATH = xbmc.translatePath(os.path.join('special://home/addons/', 'script.module.resolveurl'))
        ummmDialog = xbmcgui.Dialog()
        if not os.path.exists(HMMMPATH):
            ummmDialog("ummmm", "There was a error loading script.module.resolveurl.")
            sys.exit()
        try:
            if xbmcaddon.Addon('script.module.resolveurl').getSetting('RealDebridResolver_enabled') != 'true':
                try:
                    xbmcaddon.Addon('script.module.resolveurl') .setSetting(id='RealDebridResolver_enabled', value='true')
                    control.refresh()
                    ummmDialog.notification('[B]Turn On[/B] RealDebridResolver', 'Done, Setting [B]Enabled[/B].', xbmcgui.NOTIFICATION_INFO, 5000)
                except: pass
            elif xbmcaddon.Addon('script.module.resolveurl').getSetting('RealDebridResolver_enabled') != 'false':
                try:
                    xbmcaddon.Addon('script.module.resolveurl') .setSetting(id='RealDebridResolver_enabled', value='false')
                    control.refresh()
                    ummmDialog.notification('[B]Turn Off[/B] RealDebridResolver', 'Done, Setting [B]Disabled[/B].', xbmcgui.NOTIFICATION_INFO, 5000)
                except: pass
        except:
            pass


    def Toggle_Adbird(self):
        HMMMPATH = xbmc.translatePath(os.path.join('special://home/addons/', 'script.module.resolveurl'))
        ummmDialog = xbmcgui.Dialog()
        if not os.path.exists(HMMMPATH):
            ummmDialog("ummmm", "There was a error loading script.module.resolveurl.")
            sys.exit()
        try:
            if xbmcaddon.Addon('script.module.resolveurl').getSetting('AllDebridResolver_enabled') != 'true':
                try:
                    xbmcaddon.Addon('script.module.resolveurl') .setSetting(id='AllDebridResolver_enabled', value='true')
                    control.refresh()
                    ummmDialog.notification('[B]Turn On[/B] AllDebridResolver', 'Done, Setting [B]Enabled[/B].', xbmcgui.NOTIFICATION_INFO, 5000)
                except: pass
            elif xbmcaddon.Addon('script.module.resolveurl').getSetting('AllDebridResolver_enabled') != 'false':
                try:
                    xbmcaddon.Addon('script.module.resolveurl') .setSetting(id='AllDebridResolver_enabled', value='false')
                    control.refresh()
                    ummmDialog.notification('[B]Turn Off[/B] AllDebridResolver', 'Done, Setting [B]Disabled[/B].', xbmcgui.NOTIFICATION_INFO, 5000)
                except: pass
        except:
            pass


    def Toggle_PreMe(self):
        HMMMPATH = xbmc.translatePath(os.path.join('special://home/addons/', 'script.module.resolveurl'))
        ummmDialog = xbmcgui.Dialog()
        if not os.path.exists(HMMMPATH):
            ummmDialog("ummmm", "There was a error loading script.module.resolveurl.")
            sys.exit()
        try:
            if xbmcaddon.Addon('script.module.resolveurl').getSetting('PremiumizeMeResolver_enabled') != 'true':
                try:
                    xbmcaddon.Addon('script.module.resolveurl').setSetting(id='PremiumizeMeResolver_enabled', value='true')
                    control.refresh()
                    ummmDialog.notification('[B]Turn On[/B] PremiumizeMeResolver', 'Done, Setting [B]Enabled[/B].', xbmcgui.NOTIFICATION_INFO, 5000)
                except:
                    pass
            elif xbmcaddon.Addon('script.module.resolveurl').getSetting('PremiumizeMeResolver_enabled') != 'false':
                try:
                    xbmcaddon.Addon('script.module.resolveurl').setSetting(id='PremiumizeMeResolver_enabled', value='false')
                    control.refresh()
                    ummmDialog.notification('[B]Turn Off[/B] PremiumizeMeResolver', 'Done, Setting [B]Disabled[/B].', xbmcgui.NOTIFICATION_INFO, 5000)
                except:
                    pass
        except:
            pass


    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


