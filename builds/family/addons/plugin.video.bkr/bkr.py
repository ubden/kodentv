# -*- coding: utf-8 -*-
'''
boxsetkings Add-on
Copyright (C) 2018 boxsetkings

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

import json, ntpath, os, sys, urlparse, resolveurl, xbmc, xbmcaddon, xbmcgui, zipfile
from resources.lib.indexers import channels, episodes, movies, navigator, tvshows
from resources.lib.modules  import changelog, control, debrid, downloader, favourites, playcount, trailer, trakt, views
from resources.lib.sources  import sources

addonInfo   = xbmcaddon.Addon().getAddonInfo
datapath    = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
thumbnail   = xbmc.translatePath(addonInfo('icon'))
dialog      = xbmcgui.Dialog()
params      = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
action      = params.get('action')
content     = params.get('content')
episode     = params.get('episode')
image       = params.get('image')
imdb        = params.get('imdb')
meta        = params.get('meta')
name        = params.get('name')
premiered   = params.get('premiered')
query       = params.get('query')
season      = params.get('season')
select      = params.get('select')
source      = params.get('source')
title       = params.get('title')
tmdb        = params.get('tmdb')
tvdb        = params.get('tvdb')
tvshowtitle = params.get('tvshowtitle')
url         = params.get('url')
year        = params.get('year')

if   action == None                    : navigator.navigator().root()
elif action == 'addFavourite'          : favourites.addFavourite(meta, content)
elif action == 'addItem'               : sources().addItem(title)
elif action == 'addView'               : views.addView(content)
elif action == 'alterSources'          : sources().alterSources(url, meta)
elif action == 'artwork'               : control.artwork()
elif action == 'authTrakt'             : trakt.authTrakt()
elif action == 'backupwatchlist'       :
        fn                    = os.path.join(datapath, 'favourites.db')
        if os.path.exists(fn):
                backupdir         = control.setting('remote_path')
                if not backupdir == '':
                        to_backup     = xbmc.translatePath(os.path.join('special://', 'profile/addon_data/'))
                        rootlen       = len(datapath)
                        backup_ui_zip = xbmc.translatePath(os.path.join(backupdir, 'bkr_watchlist.zip'))
                        zipobj        = zipfile.ZipFile(backup_ui_zip , 'w', zipfile.ZIP_DEFLATED)
                        zipobj.write(fn, fn[rootlen:])
                        dialog.ok('Backup Watchlist', 'Backup complete', '', '')
                else:
                        dialog.ok('Backup Watchlist', 'No backup location found: Please setup your Backup location in the addon settings', '', '')
                        xbmc.executebuiltin('RunPlugin(%s?action=openSettings&query=7.0)' % sys.argv[0])
elif action == 'calendar'              : episodes.episodes().calendar(url)
elif action == 'calendars'             : episodes.episodes().calendars()
elif action == 'channels'              : channels.channels().get()
elif action == 'clearCache'            : navigator.navigator().clearCache()
elif action == 'clearProgress':
        progressFile = os.path.join(datapath, 'progress.db')
        if os.path.exists(progressFile):
                if control.yesnoDialog(control.lang(32056).encode('utf-8'), '', ''):
                        try:
                                os.remove(progressFile)
                                dialog.ok('Clear Progress', 'Clear Progress Complete', '', '')
                        except:
                                dialog.ok('Clear Progress', 'There was an error Deleting the Database', '', '')
        else:
                control.infoDialog(control.lang2(161).encode('utf-8'), heading='"Progress Database"', sound=False, icon=thumbnail)
elif action == 'clearSources'          :
    import universalscrapers
    universalscrapers.clear_cache()
elif action == 'deleteFavourite'       : favourites.deleteFavourite(meta, content)
elif action == 'deleteProgress'        : favourites.deleteProgress(meta, content)
elif action == 'download':
        try   : downloader.download(name, image, sources().sourcesResolve(json.loads(source)[0], True))
        except: pass
elif action == 'actionNavigator'       : navigator.navigator().action()
elif action == 'adventureNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().adventure()
elif action == 'animationNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().animation()
elif action == 'comedyNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().comedy()
elif action == 'crimeNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().crime()
elif action == 'dramaNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().drama()
elif action == 'familyNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().family()
elif action == 'fantasyNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().fantasy()
elif action == 'horrorNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().horror()
elif action == 'mysteryNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mystery() 
elif action == 'romanceNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().romance()
elif action == 'scifiNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().scifi()
elif action == 'thrillerNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().thriller()
elif action == 'downloadNavigator'     : navigator.navigator().downloads()
elif action == 'episodePlaycount'      : playcount.episodes(imdb, tvdb, season, episode, query)
elif action == 'episodes'              : episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)
elif action == 'episodeUserlists'      : episodes.episodes().userlists()
elif action == 'get_similar_movies'    : movies.movies().get_similar_movies(imdb)
elif action == 'get_similar_shows'     : tvshows.tvshows().get_similar_shows(imdb)
elif action == 'lists_navigator'       : navigator.navigator().lists_navigator()
elif action == 'movieCertificates'     : movies.movies().certifications()
elif action == 'movieFavourites'       : movies.movies().favourites()
elif action == 'movieGenres'           : movies.movies().genres()
elif action == 'movieLanguages'        : movies.movies().languages()
elif action == 'movielist'             : navigator.navigator().mymovies()
elif action == 'movieliteNavigator'    : navigator.navigator().movies(lite=True)
elif action == 'movieNavigator'        : navigator.navigator().movies()
elif action == 'moviePage'             : movies.movies().get(url)
elif action == 'moviePerson'           : movies.movies().person(query)
elif action == 'moviePersons'          : movies.movies().persons()
elif action == 'moviePlaycount'        : playcount.movies(imdb, query)
elif action == 'movieProgress'         : movies.movies().in_progress()
elif action == 'movies'                : movies.movies().get(url)
elif action == 'movieSearch'           : movies.movies().search(query)
elif action == 'movieToLibrary'        : sources().movieToLibrary(title,year,imdb,meta)
elif action == 'movieUserlists'        : movies.movies().userlists()
elif action == 'movieWidget'           : movies.movies().widget()
elif action == 'movieYears'            : movies.movies().years()
elif action == 'mymovieliteNavigator'  : navigator.navigator().mymovies(lite=True)
elif action == 'mymovieNavigator'      : navigator.navigator().mymovies()
elif action == 'mytvliteNavigator'     : navigator.navigator().mytvshows(lite=True)
elif action == 'mytvNavigator'         : navigator.navigator().mytvshows()
elif action == 'collectionsMovies'     : navigator.navigator().collectionsMovies()
elif action == 'kingscollections'     : navigator.navigator().kingscollections()
elif action == 'kidsCollections'       : navigator.navigator().kidsCollections()
elif action == 'docuMentaries'         : navigator.navigator().docuMentaries()
elif action == 'tvboxsets'         : navigator.navigator().tvboxsets()
elif action == 'standupcomedy'         : navigator.navigator().standupcomedy()
elif action == 'holidayCollections'    : navigator.navigator().holidayCollections()
elif action == 'openSettings'          : control.openSettings(query)
elif action == 'play':
        select = control.setting('hosts.mode')
        if   select == '3' and 'plugin' in control.infoLabel('Container.PluginName'): sources().play_dialog(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
        elif select == '4' and 'plugin' in control.infoLabel('Container.PluginName'): sources().play_dialog_list(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
        else                                                                        : sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
elif action == 'play_alter'            : sources().play_alter(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta)
elif action == 'play_library'          : sources().play_library(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)
elif action == 'playItem'              : sources().playItem(title, source)
elif action == 'queueItem'             : control.queueItem()
elif action == 'rdAuthorize'           : debrid.rdAuthorize()
elif action == 'refresh'               : control.refresh()
elif action == 'restorewatchlist':
        zipdir = control.setting('remote_restore_path')
        if not zipdir == '':
                with zipfile.ZipFile(zipdir, "r") as z:
                        z.extractall(datapath)
                        dialog.ok('Restore Watchlist', 'Restore complete', '', '')
        else:
                dialog.ok('Restore Watchlist', 'No item found: Please select your zipfile location in the addon settings', '', '')
                xbmc.executebuiltin('RunPlugin(%s?action=openSettings&query=7.1)' % sys.argv[0])
elif action == 'searchNavigator'       : navigator.navigator().search()
elif action == 'seasons'               : episodes.seasons().get(tvshowtitle, year, imdb, tvdb)
elif action == 'ShowChangelog'         : changelog.get()
elif action == 'showsProgress'         : episodes.episodes().in_progress()
elif action == 'similar_movies'        : movies.movies().similar_movies(imdb)
elif action == 'similar_shows'         : tvshows.tvshows().similar_shows(imdb)
elif action == 'soullessliteNavigator' : navigator.navigator().soulless(lite=True)
elif action == 'soullessNavigator'     : navigator.navigator().soulless()
elif action == 'toolNavigator'         : navigator.navigator().tools()
elif action == 'trailer'               : trailer.trailer().play(name, url)
elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)
elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()
elif action == 'tvCertificates'        : tvshows.tvshows().certifications()
elif action == 'tvFavourites'          : tvshows.tvshows().favourites()
elif action == 'tvGenres'              : tvshows.tvshows().genres()
elif action == 'tvlist'                : navigator.navigator().mytv()
elif action == 'tvliteNavigator'       : navigator.navigator().tvshows(lite=True)
elif action == 'tvNavigator'           : navigator.navigator().tvshows()
elif action == 'tvNetworks'            : tvshows.tvshows().networks()
elif action == 'tvPerson'              : tvshows.tvshows().person()
elif action == 'tvPersons'             : tvshows.tvshows().persons(url)
elif action == 'tvPlaycount'           : playcount.tvshows(name, imdb, tvdb, season, query)
elif action == 'tvPlaycountShow'       : playcount.marktvshows(name, imdb, tvdb, query)
elif action == 'tvSearch'              : tvshows.tvshows().search()
elif action == 'tvshowPage'            : tvshows.tvshows().get(url)
elif action == 'tvshows'               : tvshows.tvshows().get(url)
elif action == 'tvshowstliteNavigator' : navigator.navigator().tvshowst(lite=True)
elif action == 'tvshowstNavigator'     : navigator.navigator().tvshowst()
elif action == 'tvCollections'         : navigator.navigator().tvCollections()
elif action == 'kidstvCollections'     : navigator.navigator().kidstvCollections()
elif action == 'tvUserlists'           : tvshows.tvshows().userlists()
elif action == 'tvWidget'              : episodes.episodes().widget()
elif action == 'resolveurlsettings'   : control.openSettings(query, id="script.module.resolveurl")
elif action == 'universalscrapersettings'    : control.openSettings(query, id="script.module.universalscrapers")
elif action == 'viewsNavigator'        : navigator.navigator().views()
