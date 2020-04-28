# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    -Mofidied by The Crew
    -Copyright (C) 2019 The Crew


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import base64
import urllib2

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

artPath = control.artPath()
addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
    HOMEPATH = xbmc.translatePath('special://home/')
    ADDONSPATH = os.path.join(HOMEPATH, 'addons')
    THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
    NEWSFILE = base64.b64decode(
        b'aHR0cHM6Ly9iaXRidWNrZXQub3JnL3RlYW0tY3Jldy90ZXh0X2ZpbGVzL3Jhdy9tYXN0ZXIvd2hhdHNuZXcueG1s')
    LOCALNEWS = os.path.join(THISADDONPATH, 'whatsnew.txt')

    def root(self):
        # if self.getMenuEnabled('navi.holidays') == True:
        #self.addDirectoryItem(90157, 'holidaysNavigator', 'holidays.png', 'holidays.png')
        # if self.getMenuEnabled('navi.halloween') == True:
        #self.addDirectoryItem(90144, 'halloweenNavigator', 'halloween.png', 'halloween.png')
        if self.getMenuEnabled('navi.movies') == True:
            self.addDirectoryItem(32001, 'movieNavigator','main_movies.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.tvshows') == True:
            self.addDirectoryItem(32002, 'tvNavigator','main_tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.sports') == True:
            self.addDirectoryItem(90006, 'bluehat', 'main_bluehat.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.iptv') == True:
            self.addDirectoryItem(90007, 'whitehat', 'main_whitehat.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.kids') == True:
            self.addDirectoryItem(90009, 'greyhat', 'main_greyhat.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.1clicks') == True:
            self.addDirectoryItem(90011, 'greenhat', 'main_greenhat.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.purplehat') == True:
            self.addDirectoryItem(90189, 'purplehat', 'main_purplehat.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.standup') == True:
                self.addDirectoryItem(90113, 'redhat', 'main_redhat.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.fitness') == True:
                self.addDirectoryItem(90010, 'blackhat', 'main_blackhat.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.food') == True:
                self.addDirectoryItem(90143, 'food', 'food.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.radio') == True:
                self.addDirectoryItem(90012, 'yellowhat','radio.png', 'radio.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.add_addons') == True:
                self.addDirectoryItem(90181, 'nav_add_addons', 'add_addon.png', 'DefaultMovies.png')
        adult = True if control.setting('adult_pw') == 'lol' else False
        if adult == True:
            self.addDirectoryItem(90008, 'porn', 'main_pinkhat.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.personal.list') == True:
            self.addDirectoryItem(90167, 'plist', 'userlists.png', 'userlists.png')
        if not control.setting('furk.ai') == '':
            self.addDirectoryItem('Furk.net', 'furkNavigator', 'movies.png', 'movies.png')
        self.addDirectoryItem(32008, 'toolNavigator','main_tools.png', 'DefaultAddonProgram.png')
        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting(
            'movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator','downloads.png', 'DefaultFolder.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(32010, 'searchNavigator','main_search.png', 'DefaultFolder.png')

        self.endDirectory()

    def furk(self):
        self.addDirectoryItem(90001, 'furkUserFiles',
                              'mytvnavigator.png', 'mytvnavigator.png')
        self.addDirectoryItem(90002, 'furkSearch', 'search.png', 'search.png')
        self.endDirectory()

    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'):
            return False
        return True
#######################################################################
# News and Update Code

    def news(self):
        message = self.open_news_url(self.NEWSFILE)
        r = open(self.LOCALNEWS)
        compfile = r.read()
        if len(message) > 1:
            if compfile == message:
                pass
            else:
                text_file = open(self.LOCALNEWS, "w")
                text_file.write(message)
                text_file.close()
                compfile = message
        self.showText('Information', compfile)

    def open_news_url(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'klopp')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        print link
        return link

    def showText(self, heading, text):
        id = 10147
        xbmc.executebuiltin('ActivateWindow(%d)' % id)
        xbmc.sleep(500)
        win = xbmcgui.Window(id)
        retry = 50
        while (retry > 0):
            try:
                xbmc.sleep(10)
                retry -= 1
                win.getControl(1).setLabel(heading)
                win.getControl(5).setText(text)
                quit()
                return
            except:
                pass
#######################################################################

    def movies(self, lite=False):
        self.count = int(control.setting('page.item.limit'))
        self.addDirectoryItem(32003, 'mymovieliteNavigator',
                              'mymovies.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.moviewidget') == True:
            self.addDirectoryItem(32005, 'movieWidget',
                                  'latest-movies.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movietheaters') == True:
            self.addDirectoryItem(
                32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.movietrending') == True:
            self.addDirectoryItem(
                32017, 'movies&url=trending', 'people-watching.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviepopular') == True:
            self.addDirectoryItem(
                32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.disneym') == True:
                self.addDirectoryItem(
                    90166, 'movies&url=https://api.trakt.tv/users/thenapolitan/lists/disneyplus/items?limit=%d ' % self.count, 'disney.png', 'disney.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.traktlist') == True:
                self.addDirectoryItem(90051, 'traktlist',
                                      'trakt.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.imdblist') == True:
                self.addDirectoryItem(
                    90141, 'imdblist', 'trakt.png', 'DefaultMovies.png')
       # if self.getMenuEnabled('navi.slim') == False:
            #if self.getMenuEnabled('navi.247movies') == True:
            #    self.addDirectoryItem(90014, '247movies',
            #                          '247_movies.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.collections') == True:
                self.addDirectoryItem(
                    32000, 'collectionsNavigator', 'boxsets.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.movieboxoffice') == True:
                self.addDirectoryItem(
                    32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.movieoscars') == True:
                self.addDirectoryItem(32021, 'movies&url=oscars',
                                    'oscar-winners.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.moviegenre') == True:
            self.addDirectoryItem(32011, 'movieGenres',
                                  'genres.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.movieyears') == True:
                self.addDirectoryItem(32012, 'movieYears',
                                    'years.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.moviepersons') == True:
                self.addDirectoryItem(32013, 'moviePersons',
                                    'people.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.movielanguages') == True:
                self.addDirectoryItem(32014, 'movieLanguages',
                                    'international.png', 'DefaultMovies.png')
        # if self.getMenuEnabled('navi.moviecerts') == True:
            #self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.movieviews') == True:
                self.addDirectoryItem(32019, 'movies&url=views',
                                    'most-voted.png', 'DefaultMovies.png')
        self.addDirectoryItem(32028, 'moviePerson',
                              'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32010, 'movieSearch',
                              'search.png', 'DefaultMovies.png')

        self.endDirectory()

    def mymovies(self, lite=False):
        self.accountCheck()

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(90050, 'movies&url=onDeck',
                                  'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(
                32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(90050, 'movies&url=onDeck',
                                  'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png',
                                  queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

        elif imdbCredentials == True:
            self.addDirectoryItem(
                32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(
                32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktCredentials == True:
            self.addDirectoryItem(
                32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            self.addDirectoryItem(
                32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators == True:
            self.addDirectoryItem(
                32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        self.addDirectoryItem(32039, 'movieUserlists',
                              'userlists.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(
                32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32028, 'moviePerson',
                                  'people-search.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch',
                                  'search.png', 'DefaultMovies.png')

        self.endDirectory()

    def tvshows(self, lite=False):
        self.count = int(control.setting('page.item.limit'))
        self.addDirectoryItem(32004, 'mytvliteNavigator',
                              'mytvshows.png', 'DefaultVideoPlaylists.png')
        if self.getMenuEnabled('navi.tvAdded') == True:
            self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png',
                                  'DefaultRecentlyAddedEpisodes.png', queue=True)
        if self.getMenuEnabled('navi.tvPremier') == True:
            self.addDirectoryItem(
                32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.tvAiring') == True:
                self.addDirectoryItem(
                    32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvTrending') == True:
            self.addDirectoryItem(32017, 'tvshows&url=trending',
                                  'people-watching2.png', 'DefaultRecentlyAddedEpisodes.png')
        if self.getMenuEnabled('navi.tvPopular') == True:
            self.addDirectoryItem(
                32018, 'tvshows&url=popular', 'most-popular2.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.disney') == True:
                self.addDirectoryItem(
                    90166, 'tvshows&url=https://api.trakt.tv/users/thenapolitan/lists/disneyplus/items?limit=%d ' % self.count, 'disney.png', 'disney.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.applet') == True:
                self.addDirectoryItem(
                    90170, 'tvshows&url=https://api.trakt.tv/users/mediashare2000/lists/apple-tv/items?limit=%d ' % self.count, 'apple.png', 'apple.png')
       # if self.getMenuEnabled('navi.slim') == False:
          #  self.addDirectoryItem(90015, '247tvshows',
           #                       '247_shows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(32700, 'docuNavigator',
                                  'documentaries.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.tvGenres') == True:
                self.addDirectoryItem(
                    32011, 'tvGenres', 'genres2.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvNetworks') == True:
            self.addDirectoryItem(32016, 'tvNetworks',
                                  'networks2.png', 'DefaultTVShows.png')
        # if self.getMenuEnabled('navi.tvCertificates') == True:
            #self.addDirectoryItem(32015, 'tvCertificates', 'certificates2.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.tvRating') == True:
                self.addDirectoryItem(
                    32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.tvViews') == True:
                self.addDirectoryItem(32019, 'tvshows&url=views',
                                    'most-voted2.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.tvLanguages') == True:
                self.addDirectoryItem(32014, 'tvLanguages',
                                    'international2.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.tvActive') == True:
                self.addDirectoryItem(
                    32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.slim') == False:
            if self.getMenuEnabled('navi.tvCalendar') == True:
                self.addDirectoryItem(
                    32027, 'calendars', 'calendar2.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(
            32028, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')
        self.addDirectoryItem(
            32010, 'tvSearch', 'search2.png', 'DefaultTVShows.png')

        self.endDirectory()

    def mytvshows(self, lite=False):
        try:
            self.accountCheck()

            if traktCredentials == True and imdbCredentials == True:
                self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt2.png', 'DefaultTVShows.png', context=(
                    32551, 'tvshowsToLibrary&url=traktcollection'))
                self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt2.png', 'DefaultTVShows.png', context=(
                    32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(
                    32034, 'tvshows&url=imdbwatchlist', 'imdb2.png', 'DefaultTVShows.png')

            elif traktCredentials == True:
                self.addDirectoryItem(
                    90050, 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt2.png', 'DefaultTVShows.png', context=(
                    32551, 'tvshowsToLibrary&url=traktcollection'))
                self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt2.png', 'DefaultTVShows.png', context=(
                    32551, 'tvshowsToLibrary&url=traktwatchlist'))

            elif imdbCredentials == True:
                self.addDirectoryItem(
                    32032, 'tvshows&url=imdbwatchlist', 'imdb2.png', 'DefaultTVShows.png')
                self.addDirectoryItem(
                    32033, 'tvshows&url=imdbwatchlist2', 'imdb2.png', 'DefaultTVShows.png')

            if traktCredentials == True:
                self.addDirectoryItem(
                    32035, 'tvshows&url=traktfeatured', 'trakt2.png', 'DefaultTVShows.png')

            elif imdbCredentials == True:
                self.addDirectoryItem(
                    32035, 'tvshows&url=trending', 'imdb2.png', 'DefaultMovies.png', queue=True)

            if traktIndicators == True:
                self.addDirectoryItem(
                    32036, 'calendar&url=trakthistory', 'trakt2.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt2.png',
                                      'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32038, 'calendar&url=mycalendar',
                                      'trakt2.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

            self.addDirectoryItem(32040, 'tvUserlists',
                                  'userlists2.png', 'DefaultTVShows.png')

            if traktCredentials == True:
                self.addDirectoryItem(
                    32041, 'episodeUserlists', 'userlists2.png', 'DefaultTVShows.png')

            if lite == False:
                self.addDirectoryItem(
                    32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
                self.addDirectoryItem(
                    32028, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')
                self.addDirectoryItem(
                    32010, 'tvSearch', 'search2.png', 'DefaultTVShows.png')

            self.endDirectory()
        except:
            print("ERROR")

    def tools(self):
        self.addDirectoryItem(90000, 'newsNavigator',
                              'info.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(90188, 'bugReports', 'bugs.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(32073, 'authTrakt',
                                  'trakt.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(32609, 'ResolveUrlTorrent',
                                  'resolveurl.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32043, 'openSettings&query=0.0',
                              'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(
                32628, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(
                32045, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(
                32047, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(
                32044, 'openSettings&query=8.0', 'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(
                32046, 'openSettings&query=11.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator',
                              'tools.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(32048, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator',
                              'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(32050, 'clearSources',
                                  'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(32604, 'clearCacheSearch',
                                  'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(32052, 'clearCache',
                                  'tools.png', 'DefaultAddonProgram.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(32614, 'clearMetaCache',
                                  'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32613, 'clearAllCache',
                              'tools.png', 'DefaultAddonProgram.png')

        self.endDirectory()

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=15.0',
                              'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool',
                              'library_update.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32559, control.setting(
            'library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting(
            'library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(
                32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(
                32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(
                32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(
                32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        self.endDirectory()

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(
                32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(
                32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()

    def search(self):
        self.addDirectoryItem(32001, 'movieSearch',
                              'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            32002, 'tvSearch', 'search2.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32029, 'moviePerson',
                              'people-search.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            32030, 'tvPerson', 'people-search2.png', 'DefaultTVShows.png')

        self.endDirectory()

    def views(self):
        try:
            control.idle()

            items = [(control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'),
                     (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes')]

            select = control.selectDialog(
                [i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1:
                return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(
            ), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels={'title': title})
            item.setArt({'icon': poster, 'thumb': poster,
                         'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(
                sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return

    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode(
                'utf-8'), sound=True, icon='WARNING')
            sys.exit()

    def infoCheck(self, version):
        try:
            control.infoDialog('', control.lang(32074).encode(
                'utf-8'), time=5000, sound=False)
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
        control.infoDialog(control.lang(32057).encode(
            'utf-8'), sound=True, icon='INFO')

    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057).encode(
            'utf-8'), sound=True, icon='INFO')

    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057).encode(
            'utf-8'), sound=True, icon='INFO')

    def clearCacheSearch(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_search()
        control.infoDialog(control.lang(32057).encode(
            'utf-8'), sound=True, icon='INFO')
        # TC 2/01/19 started

    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes:
            return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057).encode(
            'utf-8'), sound=True, icon='INFO')

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
            cm.append((control.lang(context[0]).encode(
                'utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart == None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url,
                        listitem=item, isFolder=isFolder)

    def add_addons(self):
        if self.getMenuEnabled('navi.eyecandy') == True:
            self.addDirectoryItem(90164, 'eyecandy', 'eyecandy.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.retribution') == True:
            self.addDirectoryItem(90165, 'retribution','retribution.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.titan') == True:
            self.addDirectoryItem(90155, 'titan', 'titan.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.purplehat') == True:
            self.addDirectoryItem(90150, 'absolution', 'absolution.png', 'DefaultMovies.png')

        self.endDirectory()

    def bluehat(self):
        self.addDirectoryItem(90025, 'nfl', 'nfl.png', 'nfl.png')
        self.addDirectoryItem(90026, 'nhl', 'nhl.png', 'nhl.png')
        self.addDirectoryItem(90027, 'nba', 'nba.png', 'nba.png')
        self.addDirectoryItem(90024, 'mlb', 'mlb.png', 'mlb.png')
        self.addDirectoryItem(90023, 'ncaa', 'ncaa.png', 'ncaa.png')
        self.addDirectoryItem(90156, 'ncaab', 'ncaab.png', 'ncaab.png')
        #self.addDirectoryItem(90193, 'xfl', 'xfl.png', 'xfl.png')
        self.addDirectoryItem(90028, 'ufc', 'ufc.png', 'ufc.png')
        self.addDirectoryItem(90049, 'wwe', 'wwe.png', 'wwe.png')
        self.addDirectoryItem(90115, 'boxing', 'boxing.png', 'boxing.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(90046, 'fifa', 'fifa.png', 'fifa.png')
        self.addDirectoryItem(90136, 'tennis', 'tennis.png', 'tennis.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(90047, 'motogp', 'motogp.png', 'motogp.png')
            self.addDirectoryItem(90151, 'f1', 'f1.png', 'f1.png')
            self.addDirectoryItem(90153, 'pga', 'pga.png', 'pga.png')
            self.addDirectoryItem(90154, 'cricket', 'cricket.png', 'cricket.png')
            self.addDirectoryItem(90152, 'nascar', 'nascar.png', 'nascar.png')
            self.addDirectoryItem(90142, 'lfl', 'lfl.png', 'lfl.png')
        self.addDirectoryItem(90114, 'misc_sports','misc_sports.png', 'misc_sports.png')
        #self.addDirectoryItem(90030, 'sports_channels', 'sports_schannels.png', 'sports_schannels.png')
        self.addDirectoryItem(
            90031, 'sreplays', 'sports_replays.png', 'sports_replays.png')

        self.endDirectory()

    def whitehat(self):
        self.addDirectoryItem(90199, 'arconai', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90013, 'swiftNavigator','swift.png', 'swift.png')
        self.addDirectoryItem(90187, 'gitNavigator', 'iptv.png', 'iptv.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(90184, 'fluxNavigator', 'iptv.png', 'iptv.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(90185, 'stratusNavigator','iptv.png', 'iptv.png')
        if self.getMenuEnabled('navi.slim') == False:
            self.addDirectoryItem(90186, 'lodgeNavigator', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90196, 'yss', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90197, 'weak', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90198, 'sports24', 'iptv.png', 'iptv.png')

        self.endDirectory()

    def iptv_fluxus(self):
        self.addDirectoryItem(90035, 'iptv', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90038, 'spanish', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90039, 'faith', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90040, 'cctv', 'iptv.png', 'iptv.png')
        adult = True if control.setting('adult_pw') == 'lol' else False
        if adult == True:
            self.addDirectoryItem(
                90171, 'lust', 'main_pinkhat.png', 'DefaultMovies.png')

        self.endDirectory()

    def iptv_stratus(self):
        self.addDirectoryItem(90037, 'stratus', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90179, 'arabic2', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90177, 'argentina', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90180, 'bp', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90174, 'chile', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90176, 'colombia', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90175, 'india', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90178, 'spain', 'iptv.png', 'iptv.png')
        self.endDirectory()

    def iptv_tvlodge(self):
        self.addDirectoryItem(90036, 'iptv_lodge', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90172, 'spanish2', 'iptv.png', 'iptv.png')
        self.addDirectoryItem(90173, 'arabic', 'iptv.png', 'iptv.png')
        self.endDirectory()

    def imdblist(self):

        self.addDirectoryItem(90085, 'movies&url=top100',
                              'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(90086, 'movies&url=top250',
                              'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(90087, 'movies&url=top1000',
                              'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(90089, 'movies&url=rated_g',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90090, 'movies&url=rated_pg',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90091, 'movies&url=rated_pg13',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90092, 'movies&url=rated_r',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90093, 'movies&url=rated_nc17',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90088, 'movies&url=bestdirector',
                              'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            90094, 'movies&url=national_film_board', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            90100, 'movies&url=dreamworks_pictures', 'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90095, 'movies&url=fox_pictures',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(
            90096, 'movies&url=paramount_pictures', 'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90097, 'movies&url=mgm_pictures',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(
            90099, 'movies&url=universal_pictures', 'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90100, 'movies&url=sony_pictures',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(
            90101, 'movies&url=warnerbrothers_pictures', 'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90102, 'movies&url=amazon_prime',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(
            90098, 'movies&url=disney_pictures', 'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90138, 'movies&url=family_movies',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90103, 'movies&url=classic_movies',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90104, 'movies&url=classic_horror',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(
            90105, 'movies&url=classic_fantasy', 'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(
            90106, 'movies&url=classic_western', 'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(
            90107, 'movies&url=classic_annimation', 'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90108, 'movies&url=classic_war',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90109, 'movies&url=classic_scifi',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90110, 'movies&url=eighties',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90111, 'movies&url=nineties',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90112, 'movies&url=thousands',
                              'movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(90139, 'movies&url=twentyten',
                              'movies.png', 'DefaultTVShows.png')

        self.endDirectory()

    def holidays(self):
        self.count = int(control.setting('page.item.limit'))
        self.addDirectoryItem(
            90161, 'movies&url=top50_holiday', 'holidays.png', 'holidays.png')
        self.addDirectoryItem(90162, 'movies&url=best_holiday',
                              'holidays.png', 'holidays.png')
        self.addDirectoryItem(90158, 'movies&url=https://api.trakt.tv/users/movistapp/lists/christmas-movies/items?limit=%d ' %
                              self.count, 'holidays.png', 'holidays.png')
        self.addDirectoryItem(90159, 'movies&url=https://api.trakt.tv/users/cjcope/lists/hallmark-christmas/items?limit=%d ' %
                              self.count, 'holidays.png', 'holidays.png')
        self.addDirectoryItem(90160, 'movies&url=https://api.trakt.tv/users/mkadam68/lists/christmas-list/items?limit=%d ' %
                              self.count, 'holidays.png', 'holidays.png')

        self.endDirectory()

    def halloween(self):
        self.count = int(control.setting('page.item.limit'))
        self.addDirectoryItem(
            90146, 'movies&url=halloween_imdb', 'halloween.png', 'halloween.png')
        self.addDirectoryItem(
            90147, 'movies&url=halloween_top_100', 'halloween.png', 'halloween.png')
        self.addDirectoryItem(
            90148, 'movies&url=halloween_best', 'halloween.png', 'halloween.png')
        self.addDirectoryItem(
            90149, 'movies&url=halloween_great', 'halloween.png', 'halloween.png')
        self.addDirectoryItem(90145, 'movies&url=https://api.trakt.tv/users/petermesh/lists/halloween-movies/items?limit=%d ' %
                              self.count, 'halloween.png', 'halloween.png')

        self.endDirectory()

    def traktlist(self):
        self.count = int(control.setting('page.item.limit'))
        self.addDirectoryItem(90041, 'movies&url=https://api.trakt.tv/users/giladg/lists/latest-releases/items?limit=%d ' %
                              self.count, 'fhd_releases.png', 'DefaultMovies.png')
        self.addDirectoryItem(90042, 'movies&url=https://api.trakt.tv/users/giladg/lists/latest-4k-releases/items?limit=%d ' %
                              self.count, '4k_releases.png', 'DefaultMovies.png')
        self.addDirectoryItem(90043, 'movies&url=https://api.trakt.tv/users/giladg/lists/top-10-movies-of-the-week/items?limit=%d ' %
                              self.count, 'top_10.png', 'DefaultMovies.png')
        self.addDirectoryItem(90044, 'movies&url=https://api.trakt.tv/users/giladg/lists/academy-award-for-best-cinematography/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90045, 'movies&url=https://api.trakt.tv/users/giladg/lists/stand-up-comedy/items?limit=%d ' %
                              self.count, 'standup.png', 'DefaultMovies.png')
        self.addDirectoryItem(90052, 'movies&url=https://api.trakt.tv/users/daz280982/lists/movie-boxsets/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90053, 'movies&url=https://api.trakt.tv/users/movistapp/lists/action/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90054, 'movies&url=https://api.trakt.tv/users/movistapp/lists/adventure/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90055, 'movies&url=https://api.trakt.tv/users/movistapp/lists/animation/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90056, 'movies&url=https://api.trakt.tv/users/ljransom/lists/comedy-movies/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90057, 'movies&url=https://api.trakt.tv/users/movistapp/lists/crime/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90058, 'movies&url=https://api.trakt.tv/users/movistapp/lists/drama/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90059, 'movies&url=https://api.trakt.tv/users/movistapp/lists/family/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90060, 'movies&url=https://api.trakt.tv/users/movistapp/lists/history/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90061, 'movies&url=https://api.trakt.tv/users/movistapp/lists/horror/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90062, 'movies&url=https://api.trakt.tv/users/movistapp/lists/music/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90063, 'movies&url=https://api.trakt.tv/users/movistapp/lists/mystery/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90064, 'movies&url=https://api.trakt.tv/users/movistapp/lists/romance/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90065, 'movies&url=https://api.trakt.tv/users/movistapp/lists/science-fiction/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90066, 'movies&url=https://api.trakt.tv/users/movistapp/lists/thriller/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90067, 'movies&url=https://api.trakt.tv/users/movistapp/lists/war/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90068, 'movies&url=https://api.trakt.tv/users/movistapp/lists/western/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90069, 'movies&url=https://api.trakt.tv/users/movistapp/lists/marvel/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90070, 'movies&url=https://api.trakt.tv/users/movistapp/lists/walt-disney-animated-feature-films/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90071, 'movies&url=https://api.trakt.tv/users/movistapp/lists/batman/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90072, 'movies&url=https://api.trakt.tv/users/movistapp/lists/superman/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90073, 'movies&url=https://api.trakt.tv/users/movistapp/lists/star-wars/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90074, 'movies&url=https://api.trakt.tv/users/movistapp/lists/007/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90075, 'movies&url=https://api.trakt.tv/users/movistapp/lists/pixar-animation-studios/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90076, 'movies&url=https://api.trakt.tv/users/movistapp/lists/quentin-tarantino-collection/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90077, 'movies&url=https://api.trakt.tv/users/movistapp/lists/rocky/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90078, 'movies&url=https://api.trakt.tv/users/movistapp/lists/dreamworks-animation/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90079, 'movies&url=https://api.trakt.tv/users/movistapp/lists/dc-comics/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90080, 'movies&url=https://api.trakt.tv/users/movistapp/lists/the-30-best-romantic-comedies-of-all-time/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90081, 'movies&url=https://api.trakt.tv/users/movistapp/lists/88th-academy-awards-winners/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90082, 'movies&url=https://api.trakt.tv/users/movistapp/lists/most-sexy-movies/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90083, 'movies&url=https://api.trakt.tv/users/movistapp/lists/dance-movies/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(90084, 'movies&url=https://api.trakt.tv/users/movistapp/lists/halloween-movies/items?limit=%d ' %
                              self.count, 'trakt.png', 'DefaultMovies.png')

        self.endDirectory()

    def collections(self, lite=False):
        self.addDirectoryItem(
            'Actor Collection', 'collectionActors', 'boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            'Movie Collection', 'collectionBoxset', 'boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            'Car Movie Collections', 'collections&url=carmovies', 'boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem(
            'Christmas Collection', 'collections&url=xmasmovies', 'boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('DC Comics Collection', 'collections&url=dcmovies',
                              'boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(
            'Kids Collections', 'collectionKids', 'boxsets.png', 'DefaultMovies.png')
        self.addDirectoryItem('Marvel Collection', 'collections&url=marvelmovies',
                              'boxsets.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(
            'Superhero Collections', 'collectionSuperhero', 'boxsets.png', 'DefaultMovies.png')

        self.endDirectory()

    def collectionActors(self):
        self.addDirectoryItem('Adam Sandler', 'collections&url=adamsandler',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Al Pacino', 'collections&url=alpacino',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Alan Rickman', 'collections&url=alanrickman',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anthony Hopkins', 'collections&url=anthonyhopkins',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Angelina Jolie', 'collections&url=angelinajolie',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Arnold Schwarzenegger', 'collections&url=arnoldschwarzenegger',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Charlize Theron', 'collections&url=charlizetheron',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Clint Eastwood', 'collections&url=clinteastwood',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Demi Moore', 'collections&url=demimoore',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Denzel Washington', 'collections&url=denzelwashington',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Eddie Murphy', 'collections&url=eddiemurphy',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Elvis Presley', 'collections&url=elvispresley',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gene Wilder', 'collections&url=genewilder',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gerard Butler', 'collections&url=gerardbutler',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Goldie Hawn', 'collections&url=goldiehawn',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jason Statham', 'collections&url=jasonstatham',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jean-Claude Van Damme', 'collections&url=jeanclaudevandamme',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jeffrey Dean Morgan', 'collections&url=jeffreydeanmorgan',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('John Travolta', 'collections&url=johntravolta',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Johnny Depp', 'collections&url=johnnydepp',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Julia Roberts', 'collections&url=juliaroberts',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kevin Costner', 'collections&url=kevincostner',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Liam Neeson', 'collections&url=liamneeson',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mel Gibson', 'collections&url=melgibson',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Melissa McCarthy', 'collections&url=melissamccarthy',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Meryl Streep', 'collections&url=merylstreep',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Michelle Pfeiffer', 'collections&url=michellepfeiffer',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nicolas Cage', 'collections&url=nicolascage',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nicole Kidman', 'collections&url=nicolekidman',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Paul Newman', 'collections&url=paulnewman',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Reese Witherspoon', 'collections&url=reesewitherspoon',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Robert De Niro', 'collections&url=robertdeniro',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Samuel L Jackson', 'collections&url=samueljackson',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sean Connery', 'collections&url=seanconnery',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Scarlett Johansson', 'collections&url=scarlettjohansson',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sharon Stone', 'collections&url=sharonstone',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sigourney Weaver', 'collections&url=sigourneyweaver',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Steven Seagal', 'collections&url=stevenseagal',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tom Hanks', 'collections&url=tomhanks',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Vin Diesel', 'collections&url=vindiesel',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wesley Snipes', 'collections&url=wesleysnipes',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Will Smith', 'collections&url=willsmith',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Winona Ryder', 'collections&url=winonaryder',
                              'collectionactors.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def collectionBoxset(self):
        self.addDirectoryItem('48 Hrs. (1982-1990)', 'collections&url=fortyeighthours',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ace Ventura (1994-1995)', 'collections&url=aceventura',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airplane (1980-1982)', 'collections&url=airplane',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Airport (1970-1979)', 'collections&url=airport',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('American Graffiti (1973-1979)', 'collections&url=americangraffiti',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anaconda (1997-2004)', 'collections&url=anaconda',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Analyze This (1999-2002)', 'collections&url=analyzethis',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Anchorman (2004-2013)', 'collections&url=anchorman',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Austin Powers (1997-2002)', 'collections&url=austinpowers',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Back to the Future (1985-1990)', 'collections&url=backtothefuture',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Boys (1995-2003)', 'collections&url=badboys',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bad Santa (2003-2016)', 'collections&url=badsanta',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Basic Instinct (1992-2006)', 'collections&url=basicinstinct',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beverly Hills Cop (1984-1994)', 'collections&url=beverlyhillscop',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Big Mommas House (2000-2011)', 'collections&url=bigmommashouse',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Blues Brothers (1980-1998)', 'collections&url=bluesbrothers',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bourne (2002-2016)', 'collections&url=bourne',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bruce Almighty (2003-2007)', 'collections&url=brucealmighty',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Caddyshack (1980-1988)', 'collections&url=caddyshack',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheaper by the Dozen (2003-2005)', 'collections&url=cheaperbythedozen',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cheech and Chong (1978-1984)', 'collections&url=cheechandchong',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Childs Play (1988-2004)', 'collections&url=childsplay',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('City Slickers (1991-1994)', 'collections&url=cityslickers',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Conan (1982-2011)', 'collections&url=conan',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crank (2006-2009)', 'collections&url=crank',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Crocodile Dundee (1986-2001)', 'collections&url=crodiledunde',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Da Vinci Code (2006-2017)', 'collections&url=davincicode',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Daddy Day Care (2003-2007)', 'collections&url=daddydaycare',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Death Wish (1974-1994)', 'collections&url=deathwish',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Delta Force (1986-1990)', 'collections&url=deltaforce',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Die Hard (1988-2013)', 'collections&url=diehard',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Dancing (1987-2004)', 'collections&url=dirtydancing',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dirty Harry (1971-1988)', 'collections&url=dirtyharry',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dumb and Dumber (1994-2014)', 'collections&url=dumbanddumber',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Escape from New York (1981-1996)', 'collections&url=escapefromnewyork',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Every Which Way But Loose (1978-1980)', 'collections&url=everywhichwaybutloose',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Exorcist (1973-2005)', 'collections&url=exorcist',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Expendables (2010-2014)', 'collections&url=theexpendables',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fast and the Furious (2001-2017)', 'collections&url=fastandthefurious',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Father of the Bride (1991-1995)', 'collections&url=fatherofthebride',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fletch (1985-1989)', 'collections&url=fletch',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday (1995-2002)', 'collections&url=friday',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Friday the 13th (1980-2009)', 'collections&url=fridaythe13th',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fugitive (1993-1998)', 'collections&url=fugitive',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('G.I. Joe (2009-2013)', 'collections&url=gijoe',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Get Shorty (1995-2005)', 'collections&url=getshorty',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gettysburg (1993-2003)', 'collections&url=gettysburg',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghost Rider (2007-2011)', 'collections&url=ghostrider',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gods Not Dead (2014-2016)', 'collections&url=godsnotdead',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godfather (1972-1990)', 'collections&url=godfather',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Godzilla (1956-2016)', 'collections&url=godzilla',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grown Ups (2010-2013)', 'collections&url=grownups',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Grumpy Old Men (2010-2013)', 'collections&url=grumpyoldmen',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Guns of Navarone (1961-1978)', 'collections&url=gunsofnavarone',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Halloween (1978-2009)', 'collections&url=halloween',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hangover (2009-2013)', 'collections&url=hangover',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hannibal Lector (1986-2007)', 'collections&url=hanniballector',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hellraiser (1987-1996)', 'collections&url=hellraiser',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey I Shrunk the Kids (1989-1995)', 'collections&url=honeyishrunkthekids',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Horrible Bosses (2011-2014)', 'collections&url=horriblebosses',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hostel (2005-2011)', 'collections&url=hostel',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hot Shots (1991-1996)', 'collections&url=hotshots',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Independence Day (1996-2016)', 'collections&url=independenceday',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Indiana Jones (1981-2008)', 'collections&url=indianajones',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Insidious (2010-2015)', 'collections&url=insidious',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Eagle (1986-1992)', 'collections&url=ironeagle',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Reacher (2012-2016)', 'collections&url=jackreacher',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jack Ryan (1990-2014)', 'collections&url=jackryan',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jackass (2002-2013)', 'collections&url=jackass',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('James Bond (1963-2015)', 'collections&url=jamesbond',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jaws (1975-1987)', 'collections&url=jaws',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jeepers Creepers (2001-2017)', 'collections&url=jeeperscreepers',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('John Wick (2014-2017)', 'collections&url=johnwick',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jumanji (1995-2005)', 'collections&url=jumanji',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kick-Ass (2010-2013)', 'collections&url=kickass',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kill Bill (2003-2004)', 'collections&url=killbill',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('King Kong (1933-2016)', 'collections&url=kingkong',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lara Croft (2001-2003)', 'collections&url=laracroft',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Legally Blonde (2001-2003)', 'collections&url=legallyblonde',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lethal Weapon (1987-1998)', 'collections&url=leathalweapon',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Look Whos Talking (1989-1993)', 'collections&url=lookwhostalking',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Machete (2010-2013)', 'collections&url=machete',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Magic Mike (2012-2015)', 'collections&url=magicmike',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Major League (1989-1998)', 'collections&url=majorleague',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Man from Snowy River (1982-1988)', 'collections&url=manfromsnowyriver',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mask (1994-2005)', 'collections&url=mask',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Matrix (1999-2003)', 'collections&url=matrix',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Mechanic (2011-2016)', 'collections&url=themechanic',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Meet the Parents (2000-2010)', 'collections&url=meettheparents',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Men in Black (1997-2012)', 'collections&url=meninblack',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mighty Ducks (1995-1996)', 'collections&url=mightyducks',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Miss Congeniality (2000-2005)', 'collections&url=misscongeniality',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Missing in Action (1984-1988)', 'collections&url=missinginaction',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mission Impossible (1996-2015)', 'collections&url=missionimpossible',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Naked Gun (1988-1994)', 'collections&url=nakedgun',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoon (1978-2006)', 'collections&url=nationallampoon',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Lampoons Vacation (1983-2015)', 'collections&url=nationallampoonsvacation',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('National Treasure (2004-2007)', 'collections&url=nationaltreasure',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Neighbors (2014-2016)', 'collections&url=neighbors',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Night at the Museum (2006-2014)', 'collections&url=nightatthemuseum',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nightmare on Elm Street (1984-2010)', 'collections&url=nightmareonelmstreet',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Now You See Me (2013-2016)', 'collections&url=nowyouseeme',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Nutty Professor (1996-2000)', 'collections&url=nuttyprofessor',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oceans Eleven (2001-2007)', 'collections&url=oceanseleven',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Odd Couple (1968-1998)', 'collections&url=oddcouple',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Oh, God (1977-1984)', 'collections&url=ohgod',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Olympus Has Fallen (2013-2016)', 'collections&url=olympushasfallen',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Omen (1976-1981)', 'collections&url=omen',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Paul Blart Mall Cop (2009-2015)', 'collections&url=paulblart',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pirates of the Caribbean (2003-2017)', 'collections&url=piratesofthecaribbean',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planet of the Apes (1968-2014)', 'collections&url=planetoftheapes',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Police Academy (1984-1994)', 'collections&url=policeacademy',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Poltergeist (1982-1988)', 'collections&url=postergeist',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Porkys (1981-1985)', 'collections&url=porkys',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Predator (1987-2010)', 'collections&url=predator',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Purge (2013-2016)', 'collections&url=thepurge',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rambo (1982-2008)', 'collections&url=rambo',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RED (2010-2013)', 'collections&url=red',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Revenge of the Nerds (1984-1987)', 'collections&url=revengeofthenerds',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Riddick (2000-2013)', 'collections&url=riddick',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ride Along (2014-2016)', 'collections&url=ridealong',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Ring (2002-2017)', 'collections&url=thering',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('RoboCop (1987-1993)', 'collections&url=robocop',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rocky (1976-2015)', 'collections&url=rocky',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Romancing the Stone (1984-1985)', 'collections&url=romancingthestone',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rush Hour (1998-2007)', 'collections&url=rushhour',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Santa Clause (1994-2006)', 'collections&url=santaclause',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Saw (2004-2010)', 'collections&url=saw',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sex and the City (2008-2010)', 'collections&url=sexandthecity',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shaft (1971-2000)', 'collections&url=shaft',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shanghai Noon (2000-2003)', 'collections&url=shanghainoon',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sin City (2005-2014)', 'collections&url=sincity',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sinister (2012-2015)', 'collections&url=sinister',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sister Act (1995-1993)', 'collections&url=sisteract',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Smokey and the Bandit (1977-1986)', 'collections&url=smokeyandthebandit',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Speed (1994-1997)', 'collections&url=speed',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stakeout (1987-1993)', 'collections&url=stakeout',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Trek (1979-2016)', 'collections&url=startrek',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Sting (1973-1983)', 'collections&url=thesting',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taken (2008-2014)', 'collections&url=taken',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Taxi (1998-2007)', 'collections&url=taxi',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ted (2012-2015)', 'collections&url=ted',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teen Wolf (1985-1987)', 'collections&url=teenwolf',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terminator (1984-2015)', 'collections&url=terminator',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Terms of Endearment (1983-1996)', 'collections&url=termsofendearment',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Texas Chainsaw Massacre (1974-2013)', 'collections&url=texaschainsawmassacre',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Thing (1982-2011)', 'collections&url=thething',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Thomas Crown Affair (1968-1999)', 'collections&url=thomascrownaffair',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Transporter (2002-2015)', 'collections&url=transporter',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Under Siege (1992-1995)', 'collections&url=undersiege',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Universal Soldier (1992-2012)', 'collections&url=universalsoldier',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wall Street (1987-2010)', 'collections&url=wallstreet',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Waynes World (1992-1993)', 'collections&url=waynesworld',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Weekend at Bernies (1989-1993)', 'collections&url=weekendatbernies',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Whole Nine Yards (2000-2004)', 'collections&url=wholenineyards',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Files (1998-2008)', 'collections&url=xfiles',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('xXx (2002-2005)', 'collections&url=xxx',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Young Guns (1988-1990)', 'collections&url=youngguns',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zoolander (2001-2016)', 'collections&url=zoolander',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Zorro (1998-2005)', 'collections&url=zorro',
                              'collectionboxset.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def collectionKids(self):
        self.addDirectoryItem('Disney Collection', 'collections&url=disneymovies',
                              'collectiondisney.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kids Boxset Collection', 'collectionBoxsetKids',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kids Movie Collection', 'collections&url=kidsmovies',
                              'collectionkids.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def collectionBoxsetKids(self):
        self.addDirectoryItem('101 Dalmations (1961-2003)', 'collections&url=onehundredonedalmations',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Addams Family (1991-1998)', 'collections&url=addamsfamily',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Aladdin (1992-1996)', 'collections&url=aladdin',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Alvin and the Chipmunks (2007-2015)', 'collections&url=alvinandthechipmunks',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Atlantis (2001-2003)', 'collections&url=atlantis',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Babe (1995-1998)', 'collections&url=babe',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Balto (1995-1998)', 'collections&url=balto',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Bambi (1942-2006)', 'collections&url=bambi',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beauty and the Beast (1991-2017)', 'collections&url=beautyandthebeast',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Beethoven (1992-2014)', 'collections&url=beethoven',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Brother Bear (2003-2006)', 'collections&url=brotherbear',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cars (2006-2017)', 'collections&url=cars',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cinderella (1950-2007)', 'collections&url=cinderella',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Cloudy With a Chance of Meatballs (2009-2013)',
                              'collections&url=cloudywithachanceofmeatballs', 'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Despicable Me (2010-2015)', 'collections&url=despicableme',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Finding Nemo (2003-2016)', 'collections&url=findingnemo',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fox and the Hound (1981-2006)', 'collections&url=foxandthehound',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Free Willy (1993-2010)', 'collections&url=freewilly',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ghostbusters (1984-2016)', 'collections&url=ghostbusters',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Gremlins (1984-2016)', 'collections&url=gremlins',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Happy Feet (2006-2011)', 'collections&url=happyfeet',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Harry Potter (2001-2011)', 'collections&url=harrypotter',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Home Alone (1990-2012)', 'collections&url=homealone',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Homeward Bound (1993-1996)', 'collections&url=homewardbound',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Honey, I Shrunk the Kids (1989-1997)', 'collections&url=honeyishrunkthekids',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hotel Transylvania (2012-2015)', 'collections&url=hoteltransylvania',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('How to Train Your Dragon (2010-2014)', 'collections&url=howtotrainyourdragon',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hunchback of Notre Dame (1996-2002)', 'collections&url=hunchbackofnotredame',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Ice Age (2002-2016)', 'collections&url=iceage',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Jurassic Park (1993-2015)', 'collections&url=jurassicpark',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Kung Fu Panda (2008-2016)', 'collections&url=kungfupanda',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lady and the Tramp (1955-2001)', 'collections&url=ladyandthetramp',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Lilo and Stitch (2002-2006)', 'collections&url=liloandstitch',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Madagascar (2005-2014)', 'collections&url=madagascar',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Monsters Inc (2001-2013)', 'collections&url=monstersinc',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Mulan (1998-2004)', 'collections&url=mulan',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Narnia (2005-2010)', 'collections&url=narnia',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('New Groove (2000-2005)', 'collections&url=newgroove',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Open Season (2006-2015)', 'collections&url=openseason',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Planes (2013-2014)', 'collections&url=planes',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Pocahontas (1995-1998)', 'collections&url=pocahontas',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Problem Child (1990-1995)', 'collections&url=problemchild',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Rio (2011-2014)', 'collections&url=rio',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Sammys Adventures (2010-2012)', 'collections&url=sammysadventures',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Scooby-Doo (2002-2014)', 'collections&url=scoobydoo',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Short Circuit (1986-1988)', 'collections&url=shortcircuit',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Shrek (2001-2011)', 'collections&url=shrek',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('SpongeBob SquarePants (2004-2017)', 'collections&url=spongebobsquarepants',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spy Kids (2001-2011)', 'collections&url=spykids',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Star Wars (1977-2015)', 'collections&url=starwars',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Stuart Little (1999-2002)', 'collections&url=stuartlittle',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tarzan (1999-2016)', 'collections&url=tarzan',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Teenage Mutant Ninja Turtles (1978-2009)', 'collections&url=teenagemutantninjaturtles',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Jungle Book (1967-2003)', 'collections&url=thejunglebook',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Karate Kid (1984-2010)', 'collections&url=thekaratekid',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Lion King (1994-2016)', 'collections&url=thelionking',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Little Mermaid (1989-1995)', 'collections&url=thelittlemermaid',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Neverending Story (1984-1994)', 'collections&url=theneverendingstory',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('The Smurfs (2011-2013)', 'collections&url=thesmurfs',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tooth Fairy (2010-2012)', 'collections&url=toothfairy',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tinker Bell (2008-2014)', 'collections&url=tinkerbell',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Tom and Jerry (1992-2013)', 'collections&url=tomandjerry',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Toy Story (1995-2014)', 'collections&url=toystory',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('VeggieTales (2002-2008)', 'collections&url=veggietales',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Winnie the Pooh (2000-2005)', 'collections&url=winniethepooh',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Wizard of Oz (1939-2013)', 'collections&url=wizardofoz',
                              'collectionkidsboxset.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def collectionSuperhero(self):
        self.addDirectoryItem('Avengers (2008-2017)', 'collections&url=avengers',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Batman (1989-2016)', 'collections&url=batman',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Captain America (2011-2016)', 'collections&url=captainamerica',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Dark Knight Trilogy (2005-2013)', 'collections&url=darkknight',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Fantastic Four (2005-2015)', 'collections&url=fantasticfour',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Hulk (2003-2008)', 'collections&url=hulk',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Iron Man (2008-2013)', 'collections&url=ironman',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Spider-Man (2002-2017)', 'collections&url=spiderman',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('Superman (1978-2016)', 'collections&url=superman',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem('X-Men (2000-2016)', 'collections&url=xmen',
                              'collectionsuperhero.png', 'DefaultRecentlyAddedMovies.png')

        self.endDirectory()

    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
