# -*- coding: utf-8 -*-
'''
Uranus Add-on
Copyright (C) 2017 Uranus
Rebranded from Schism's "Zen"

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

import base64, os, sys, urlparse
from resources.lib.modules import control, trakt

inprogress_db    = control.setting('inprogress_db')
sysaddon         = base64.b64decode('cGx1Z2luOi8vcGx1Z2luLnZpZGVvLnVyYW51cy8=')
syshandle        = int(sys.argv[1])
artPath          = control.artPath()
addonFanart      = control.addonFanart()
imdbCredentials  = False if control.setting('imdb.user') == '' else True
traktCredentials = trakt.getTraktCredentialsInfo()
traktIndicators  = trakt.getTraktIndicatorsInfo()
queueMenu        = control.lang(32065).encode('utf-8')
movielist1       = control.setting('tmdb.movielist_name1')
movielist2       = control.setting('tmdb.movielist_name2')
movielist3       = control.setting('tmdb.movielist_name3')
movielist4       = control.setting('tmdb.movielist_name4')
movielist5       = control.setting('tmdb.movielist_name5')
movielist6       = control.setting('tmdb.movielist_name6')
movielist7       = control.setting('tmdb.movielist_name7')
movielist8       = control.setting('tmdb.movielist_name8')
movielist9       = control.setting('tmdb.movielist_name9')
movielist10      = control.setting('tmdb.movielist_name10')
movielist11      = control.setting('tmdb.movielist_name11')
movielist12      = control.setting('tmdb.movielist_name12')
movielist13      = control.setting('tmdb.movielist_name13')
movielist14      = control.setting('tmdb.movielist_name14')
movielist15      = control.setting('tmdb.movielist_name15')
movielist16      = control.setting('tmdb.movielist_name16')
movielist17      = control.setting('tmdb.movielist_name17')
movielist18      = control.setting('tmdb.movielist_name18')
movielist19      = control.setting('tmdb.movielist_name19')
movielist20      = control.setting('tmdb.movielist_name20')
movielist21      = control.setting('tmdb.movielist_name21')
movielist22      = control.setting('tmdb.movielist_name22')
movielist23      = control.setting('tmdb.movielist_name23')
movielist24      = control.setting('tmdb.movielist_name24')
movielist25      = control.setting('tmdb.movielist_name25')
movielist26      = control.setting('tmdb.movielist_name26')
movielist27      = control.setting('tmdb.movielist_name27')
movielist28      = control.setting('tmdb.movielist_name28')
movielist29      = control.setting('tmdb.movielist_name29')
movielist30      = control.setting('tmdb.movielist_name30')
tvlist1          = control.setting('tmdb.tvlist_name1')
tvlist2          = control.setting('tmdb.tvlist_name2')
tvlist3          = control.setting('tmdb.tvlist_name3')
tvlist4          = control.setting('tmdb.tvlist_name4')
tvlist5          = control.setting('tmdb.tvlist_name5')
tvlist6          = control.setting('tmdb.tvlist_name6')
tvlist7          = control.setting('tmdb.tvlist_name7')
tvlist8          = control.setting('tmdb.tvlist_name8')
tvlist9          = control.setting('tmdb.tvlist_name9')
tvlist10         = control.setting('tmdb.tvlist_name10')
tvlist11         = control.setting('tmdb.tvlist_name11')
tvlist12         = control.setting('tmdb.tvlist_name12')
tvlist13         = control.setting('tmdb.tvlist_name13')
tvlist14         = control.setting('tmdb.tvlist_name14')
tvlist15         = control.setting('tmdb.tvlist_name15')
tvlist16         = control.setting('tmdb.tvlist_name16')
tvlist17         = control.setting('tmdb.tvlist_name17')
tvlist18         = control.setting('tmdb.tvlist_name18')
tvlist19         = control.setting('tmdb.tvlist_name19')
tvlist20         = control.setting('tmdb.tvlist_name20')
tvlist21         = control.setting('tmdb.tvlist_name21')
tvlist22         = control.setting('tmdb.tvlist_name22')
tvlist23         = control.setting('tmdb.tvlist_name23')
tvlist24         = control.setting('tmdb.tvlist_name24')
tvlist25         = control.setting('tmdb.tvlist_name25')
tvlist26         = control.setting('tmdb.tvlist_name26')
tvlist27         = control.setting('tmdb.tvlist_name27')
tvlist28         = control.setting('tmdb.tvlist_name28')
tvlist29         = control.setting('tmdb.tvlist_name29')
tvlist30         = control.setting('tmdb.tvlist_name30')

class navigator:
        def root(self):
                self.addDirectoryItem('Merry Christmas', 'movies&url=tmdbxmas',  'holidaycollections.png',          'DefaultMovies.png')
                self.addDirectoryItem(32001,              'movieNavigator',       'movies.png',        'DefaultMovies.png')
                self.addDirectoryItem(32002,              'tvNavigator',          'tvshows.png',      'DefaultTVShows.png')
                if not control.setting('movie.widget') == '0':
                        self.addDirectoryItem('Spotlight',    'movieWidget',          'latest-movies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('TV Collections', 'tvCollections', 'collection.png', 'DefaultMovies.png')
                self.addDirectoryItem('Movie Collections',       'collectionsMovies',     'collection.png',    'DefaultMovies.png')
                self.addDirectoryItem(32026,              'tvshows&url=premiere', 'years.png',         'DefaultTVShows.png')
                self.addDirectoryItem('My Uranus',       'lists_navigator',      'mymovies.png',      'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(32027,              'calendars',            'networks.png',      'DefaultRecentlyAddedEpisodes.png')
                # self.addDirectoryItem(32007,              'channels',             'sly.png',      'DefaultMovies.png')
                self.addDirectoryItem(32008,              'toolNavigator',        'tools.png',         'DefaultAddonProgram.png')
                downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0) else False
                if downloads == True:
                        self.addDirectoryItem(32009,          'downloadNavigator',    'downloads.png',     'DefaultFolder.png')
                if not control.setting('lists.widget') == '0':
                        self.addDirectoryItem('Trakt Movies', 'soullessNavigator',    'trakt.png',      'DefaultVideoPlaylists.png')
                        self.addDirectoryItem('Trakt TV',     'tvshowstNavigator',    'trakt.png',     'DefaultVideoPlaylists.png')
                self.addDirectoryItem(32010,              'searchNavigator',      'search.png',        'DefaultFolder.png')
                self.addDirectoryItem('Changelog',        'ShowChangelog',        'icon.png',          'DefaultFolder.png')
                self.endDirectory()

        def movies(self, lite=False):
                if inprogress_db == 'true':
                        self.addDirectoryItem("In Progress",   'movieProgress',         'trending.png',      'DefaultMovies.png')
                self.addDirectoryItem('Featured',          'movies&url=featured',   'featured.png',      'DefaultRecentlyAddedMovies.png')
#		self.addDirectoryItem('Trending',          'movies&url=trending',   'trending.png',      'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Populars',          'movies&url=popular',    'populars.png',      'DefaultMovies.png')
                self.addDirectoryItem('New Movies',        'movies&url=premiere',   'trending.png',      'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Top Rated',         'movies&url=views',      'most-viewed.png',   'DefaultMovies.png')
                self.addDirectoryItem('In Theaters',       'movies&url=theaters',   'in-theaters.png',   'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Marvel Universe',   'movies&url=tmdbmarvel', 'collection.png',        'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Oscar Winners',     'movies&url=tmdboscars', 'oscars.png',        'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Disney Collection', 'movies&url=tmdbdisney', 'disney.png',        'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Kids Collections',  'kidsCollections',       'kidscollection.png', 'DefaultMovies.png')
                self.addDirectoryItem('Holiday',           'holidayCollections',    'holidaycollections.png', 'DefaultMovies.png')
                self.addDirectoryItem('Genres',            'movieGenres',           'genres.png',        'DefaultMovies.png')
                self.addDirectoryItem('Years',             'movieYears',            'years.png',         'DefaultMovies.png')
                self.addDirectoryItem('Persons',           'moviePersons',          'people.png',        'DefaultMovies.png')
                self.addDirectoryItem('Certificates',      'movieCertificates',     'certificates.png',  'DefaultMovies.png')
                self.addDirectoryItem(32028,               'moviePerson',           'people-search.png', 'DefaultMovies.png')
                self.addDirectoryItem(32010,               'movieSearch',           'search.png',        'DefaultMovies.png')
                self.endDirectory()

        def soulless(self, lite=False):
                self.accountCheck()
                asrch = "{0} - {1}".format(control.lang2(20337).encode('utf-8'), control.lang2(137).encode('utf-8'))
                if traktCredentials == True and imdbCredentials == True:
                        self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png',       'DefaultMovies.png')
                        self.addDirectoryItem(32033, 'movies&url=traktwatchlist',  'trakt.png',       'DefaultMovies.png')
                elif traktCredentials == True:
                        self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png',       'DefaultMovies.png')
                        self.addDirectoryItem(32033, 'movies&url=traktwatchlist',  'trakt.png',       'DefaultMovies.png')
                if traktCredentials == True:
                        self.addDirectoryItem(32035, 'movies&url=traktfeatured',   'trakt.png',       'DefaultMovies.png', queue=True)
                if traktIndicators == True:
                        self.addDirectoryItem(32036, 'movies&url=trakthistory',    'trakt.png',       'DefaultMovies.png', queue=True)
                self.addDirectoryItem("My Lists",     'movieUserlists',             'mymovies.png',    'DefaultMovies.png')
                if lite == False:
                        self.addDirectoryItem(32031, 'movieliteNavigator',         'movies.png',      'DefaultMovies.png')
                        self.addDirectoryItem(asrch, 'moviePerson',                'actorsearch.png', 'DefaultMovies.png')
                        self.addDirectoryItem(32010, 'movieSearch',                'search.png',      'DefaultMovies.png')
                self.endDirectory()

        def lists_navigator(self):
                self.addDirectoryItem('[WATCHLIST] Movies',   'movieFavourites', 'mymovies.png', 'DefaultMovies.png')
                self.addDirectoryItem('[WATCHLIST] TV Shows', 'tvFavourites',    'mymovies.png', 'DefaultMovies.png')
                self.addDirectoryItem('[TMDB LIST] Movies',   'movielist',       'movies.png',   'DefaultMovies.png')
                self.addDirectoryItem('[TMDB LIST] Tv Shows', 'tvlist',          'channels.png', 'DefaultTVShows.png')
                self.endDirectory()

        def mymovies(self):
                self.addDirectoryItem(movielist1,  'movies&url=mycustomlist1',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist2,  'movies&url=mycustomlist2',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist3,  'movies&url=mycustomlist3',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist4,  'movies&url=mycustomlist4',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist5,  'movies&url=mycustomlist5',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist6,  'movies&url=mycustomlist6',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist7,  'movies&url=mycustomlist7',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist8,  'movies&url=mycustomlist8',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist9,  'movies&url=mycustomlist9',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist10, 'movies&url=mycustomlist10', 'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist11, 'movies&url=mycustomlist11',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist12, 'movies&url=mycustomlist12',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist13, 'movies&url=mycustomlist13',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist14, 'movies&url=mycustomlist14',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist15, 'movies&url=mycustomlist15',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist16, 'movies&url=mycustomlist16',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist17, 'movies&url=mycustomlist17',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist18, 'movies&url=mycustomlist18',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist19, 'movies&url=mycustomlist19',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist20, 'movies&url=mycustomlist20', 'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist21, 'movies&url=mycustomlist21',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist22, 'movies&url=mycustomlist22',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist23, 'movies&url=mycustomlist23',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist24, 'movies&url=mycustomlist24',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist25, 'movies&url=mycustomlist25',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist26, 'movies&url=mycustomlist26',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist27, 'movies&url=mycustomlist27',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist28, 'movies&url=mycustomlist28',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist29, 'movies&url=mycustomlist29',  'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem(movielist30, 'movies&url=mycustomlist30', 'mymovies.png', 'DefaultRecentlyAddedMovies.png')
                self.endDirectory()

        def mytv(self):
                self.addDirectoryItem(tvlist1,  'tvshows&url=mycustomlist1',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist2,  'tvshows&url=mycustomlist2',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist3,  'tvshows&url=mycustomlist3',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist4,  'tvshows&url=mycustomlist4',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist5,  'tvshows&url=mycustomlist5',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist6,  'tvshows&url=mycustomlist6',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist7,  'tvshows&url=mycustomlist7',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist8,  'tvshows&url=mycustomlist8',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist9,  'tvshows&url=mycustomlist9',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist10, 'tvshows&url=mycustomlist10', 'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist11, 'tvshows&url=mycustomlist11',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist12, 'tvshows&url=mycustomlist12',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist13, 'tvshows&url=mycustomlist13',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist14, 'tvshows&url=mycustomlist14',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist15, 'tvshows&url=mycustomlist15',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist16, 'tvshows&url=mycustomlist16',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist17, 'tvshows&url=mycustomlist17',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist18, 'tvshows&url=mycustomlist18',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist19, 'tvshows&url=mycustomlist19',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist20, 'tvshows&url=mycustomlist20', 'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist21, 'tvshows&url=mycustomlist21',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist22, 'tvshows&url=mycustomlist22',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist23, 'tvshows&url=mycustomlist23',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist24, 'tvshows&url=mycustomlist24',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist25, 'tvshows&url=mycustomlist25',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist26, 'tvshows&url=mycustomlist26',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist27, 'tvshows&url=mycustomlist27',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist28, 'tvshows&url=mycustomlist28',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist29, 'tvshows&url=mycustomlist29',  'channels.png', 'DefaultTVShows.png')
                self.addDirectoryItem(tvlist30, 'tvshows&url=mycustomlist30', 'channels.png', 'DefaultTVShows.png')
                self.endDirectory()

        def tvshowst(self, lite=False):
                self.accountCheck()
                if traktCredentials == True and imdbCredentials == True:
                        self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
                        self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')
                elif traktCredentials == True:
                        self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
                        self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')
                if traktCredentials == True:
                        self.addDirectoryItem('Featured', 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')
                if traktIndicators == True:
                        self.addDirectoryItem('History', 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                        self.addDirectoryItem('Progress', 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                        self.addDirectoryItem('Calendar', 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem('My Lists', 'tvUserlists', 'mytvshows.png', 'DefaultTVShows.png')
                if traktCredentials == True:
                        self.addDirectoryItem('My Episodes', 'episodeUserlists', 'mytvshows.png', 'DefaultTVShows.png')
                if lite == False:
                        self.addDirectoryItem('TV Shows', 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
                        self.addDirectoryItem('Actor Search', 'tvPerson', 'actorsearch.png', 'DefaultTVShows.png')
                        self.addDirectoryItem('Search', 'tvSearch', 'search.png', 'DefaultTVShows.png')
                self.endDirectory()

        def tvshows(self, lite=False):
                if inprogress_db == 'true': self.addDirectoryItem("In Progress", 'showsProgress', 'trending.png', 'DefaultMovies.png')
                self.addDirectoryItem('Featured', 'tvshows&url=featured', 'populars.png', 'DefaultRecentlyAddedEpisodes.png')
                self.addDirectoryItem('Populars', 'tvshows&url=popular', 'most-viewed.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32019, 'tvshows&url=views', 'most-viewed.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32026, 'tvshows&url=premiere', 'years.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32025, 'tvshows&url=active', 'years.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Kids TV', 'kidstvCollections', 'kidscollection.png', 'DefaultMovies.png')
                self.addDirectoryItem('TV Collections', 'tvCollections', 'collection.png', 'DefaultMovies.png')
                self.addDirectoryItem(32023, 'tvshows&url=rating', 'featured.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32027, 'calendars', 'networks.png', 'DefaultRecentlyAddedEpisodes.png')
                self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')
                self.endDirectory()

        def tools(self):
                self.addDirectoryItem('[B]RESOLVE URL[/B]: Settings', 'resolveurlsettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem(32043, 'openSettings&query=0.1', 'tools.png', 'DefaultAddonProgram.png')
                # self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]SETTINGS[/B]: Accounts', 'openSettings&query=2.1', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]SETTINGS[/B]: Providers', 'universalscrapersettings&query=1.1', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]SETTINGS[/B]: Debrid', 'openSettings&query=2.8', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]SETTINGS[/B]: Downloads', 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]SETTINGS[/B]: Subtitles', 'openSettings&query=4.0', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]SETTINGS[/B]: Watchlist', 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]SETTINGS[/B]: Movie Lists', 'openSettings&query=6.1', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]SETTINGS[/B]: TVShow Lists', 'openSettings&query=7.1', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]Uranus[/B]: Views', 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]Uranus[/B]: Clear Providers', 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]Uranus[/B]: Clear Cache', 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]BACKUP[/B]: Watchlist', 'backupwatchlist', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]RESTORE[/B]: Watchlist', 'restorewatchlist', 'tools.png', 'DefaultAddonProgram.png')
                self.addDirectoryItem('[B]Uranus[/B]: Clear Progress Database', 'clearProgress', 'tools.png', 'DefaultAddonProgram.png')
                self.endDirectory()

        def downloads(self):
                movie_downloads = control.setting('movie.download.path')
                # tv_downloads = control.setting('tv.download.path')
                if len(control.listDir(movie_downloads)[0]) > 0:
                        self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
                self.endDirectory()

        def search(self):
                self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
                self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')
                # self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
                self.endDirectory()

        def views(self):
                try:
                        control.idle()
                        items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]
                        select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))
                        if select == -1: return
                        content = items[select][1]
                        title = control.lang(32059).encode('utf-8')
                        url = '%s?action=addView&content=%s' % (sys.argv[0], content)
                        poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()
                        item = control.item(label=title)
                        item.setInfo(type='Video', infoLabels = {'title': title})
                        item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})
                        item.setProperty('Fanart_Image', fanart)
                        control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
                        control.content(int(sys.argv[1]), content)
                        control.directory(int(sys.argv[1]), cacheToDisc=True)
                        from resources.lib.modules import cache
                        views.setView(content, {})
                except:
                        return

        def accountCheck(self):
                if traktCredentials == False:
                        control.idle()
                        control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
                        control.openSettings('2.12')
                        sys.exit()

        def clearCache(self):
                control.idle()
                yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
                if not yes: return
                from resources.lib.modules import cache
                cache.clear()
                control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

        def addDirectoryItem(self, name, query, thumb, icon, queue=False, isAction=True, isFolder=True):
                try: name = control.lang(name).encode('utf-8')
                except: pass
                url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
                thumb = os.path.join(artPath, thumb) if not artPath == None else icon
                cm = []
                if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                item = control.item(label=name)
                item.addContextMenuItems(cm)
                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

        def collectionsMovies(self):
                self.addDirectoryItem('Ass Kickin', 'movies&url=tmdbfight', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Based On A True Story', 'movies&url=tmdbbased', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('The Big Con', 'movies&url=tmdbconman', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('The Car is the Star', 'movies&url=tmdbfast', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Chick Flicks', 'movies&url=tmdbdatenight', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Cold War', 'movies&url=tmdbcold', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Comedy', 'movies&url=tmdbcomed', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Conspiracy', 'movies&url=tmdbconsp', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('DC Universe', 'movies&url=tmdbdc', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Drugs', 'movies&url=tmdb420', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('FBI', 'movies&url=tmdbanimal', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Gangsters', 'movies&url=tmdbmafia', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Hackers', 'movies&url=tmdbhack', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('The Heist', 'movies&url=tmdbheist', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('I Love the 1980s', 'movies&url=tmdbsnatched', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('I Love the 1990s', 'movies&url=tmdbsports', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Man and Machine', 'movies&url=tmdburban', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Marvel Universe', 'movies&url=tmdbmarvel', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Michael Moore', 'movies&url=tmdbimmortal', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Politics', 'movies&url=tmdbchi', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Sci-Fi', 'movies&url=tmdbufo', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Scottish', 'movies&url=tmdbgwg', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('See you in Court', 'movies&url=tmdbgamers', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Skateboarding', 'movies&url=tmdbbooks', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Spies', 'movies&url=tmdbspy', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Stand-Up', 'movies&url=tmdbstandup', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Star Trek', 'movies&url=tmdbvigilante', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('War', 'movies&url=tmdbtragedy', 'collection.png', 'DefaultRecentlyAddedMovies.png')
                self.endDirectory()

        def kidsCollections(self):
                self.addDirectoryItem('Disney', 'movies&url=tmdbdisney', 'disney.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Dreamworks', 'movies&url=tmdbdreamworks', 'dreamworks.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Lego Collection', 'movies&url=tmdblego', 'lego.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Princesses', 'movies&url=tmdbprincess', 'princess.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Super Heroes', 'movies&url=tmdbhero', 'hero.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('The Ultimate Kids Collection', 'movies&url=tmdbkidz', 'kidsfav.png', 'DefaultRecentlyAddedMovies.png')
                self.endDirectory()

        def holidayCollections(self):
                self.addDirectoryItem('Christmas', 'movies&url=tmdbchristmas', 'christmas.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Easter', 'movies&url=tmdbeaster', 'easter.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Halloween', 'movies&url=tmdbhalloween', 'halloween.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Independence Day', 'movies&url=tmdbfourth', 'thanks.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Thanksgiving', 'movies&url=tmdbthanks', 'thanks.png', 'DefaultRecentlyAddedMovies.png')
                self.addDirectoryItem('Valentines', 'movies&url=tmdbvalentines', 'valentines.png', 'DefaultRecentlyAddedMovies.png')
                self.endDirectory()

        def tvCollections(self):
                self.addDirectoryItem('Adult Animation', 'tvshows&url=tmdbsouthptv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Amazon Original', 'tvshows&url=tmdbamaztv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Based On A True Story', 'tvshows&url=tmdb420tv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('The Car is the Star', 'tvshows&url=tmdbfasttv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('CIA', 'tvshows&url=tmdbgamers', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Classics', 'tvshows&url=tmdbblast', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Comedy', 'tvshows&url=tmdblmao', 'collection.PNG', 'DefaultTVShows.png')
                self.addDirectoryItem('Datenight', 'tvshows&url=tmdbdatenighttv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('FBI', 'tvshows&url=tmdbcooking', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Hulu Original', 'tvshows&url=tmdbhulutv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Man and Machine', 'tvshows&url=tmdbsportstv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Netflix Original', 'tvshows&url=tmdbnettv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Organised Crime', 'tvshows&url=tmdbtats', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Out Of This World', 'tvshows&url=tmdbufotv', 'collection.png', 'DefaultTVShows.png')
                self.addDirectoryItem('See you in Court', 'tvshows&url=tmdbchitv', 'collection.png', 'DefaultTVShows.png')
                self.endDirectory()

        def kidstvCollections(self):
                self.addDirectoryItem('Animation Station', 'tvshows&url=tmdbanimationtv', 'lego.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Back In The Day Cartoons', 'tvshows&url=tmdbcartoon', 'cartoon.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Kids TV', 'tvshows&url=tmdbkids', 'kidsfav.png', 'DefaultTVShows.png')
                self.addDirectoryItem('Lil Ones', 'tvshows&url=tmdblittle', 'lil.png', 'DefaultTVShows.png')
                self.endDirectory()

        def endDirectory(self):
                # control.do_block_check(False)
                control.directory(syshandle, cacheToDisc=True)
