# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    -Mofidied by The Crew
    -Copyright (C) 2019 lambda


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

import urlparse
import sys
import urllib
import xbmcgui
from resources.lib.modules import control, log_utils

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))

mode = params.get('mode')

subid = params.get('subid')

action = params.get('action')

docu_category = params.get('docuCat')

docu_watch = params.get('docuPlay')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')

windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ("0", "1") else 0


if action == None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    navigator.navigator().root()

elif action == '247movies':
    from resources.lib.indexers import lists
    lists.indexer().root_247movies()

elif action == '247tvshows':
    from resources.lib.indexers import lists
    lists.indexer().root_247tvshows()

elif action == 'iptv':
    from resources.lib.indexers import lists
    lists.indexer().root_iptv()

elif action == 'yss':
    from resources.lib.indexers import lists
    lists.indexer().root_yss()

elif action == 'weak':
    from resources.lib.indexers import lists
    lists.indexer().root_weak()

elif action == 'sportsbay':
    from resources.lib.indexers import lists
    lists.indexer().root_sportsbay()

elif action == 'sports24':
    from resources.lib.indexers import lists
    lists.indexer().root_sports24()

elif action == 'arconai':
    from resources.lib.indexers import lists
    lists.indexer().root_arconai()

elif action == 'iptv_lodge':
    from resources.lib.indexers import lists
    lists.indexer().root_iptv_lodge()

elif action == 'stratus':
    from resources.lib.indexers import lists
    lists.indexer().root_stratus()

elif action == 'spanish':
    from resources.lib.indexers import lists
    lists.indexer().root_spanish()

elif action == 'spanish2':
    from resources.lib.indexers import lists
    lists.indexer().root_spanish2()

elif action == 'gitNavigator':
    from resources.lib.indexers import lists
    lists.indexer().root_git()

elif action == 'bp':
    from resources.lib.indexers import lists
    lists.indexer().root_bp()

elif action == 'arabic':
    from resources.lib.indexers import lists
    lists.indexer().root_arabic()

elif action == 'arabic2':
    from resources.lib.indexers import lists
    lists.indexer().root_arabic2()

elif action == 'india':
    from resources.lib.indexers import lists
    lists.indexer().root_india()

elif action == 'chile':
    from resources.lib.indexers import lists
    lists.indexer().root_chile()

elif action == 'colombia':
    from resources.lib.indexers import lists
    lists.indexer().root_colombia()

elif action == 'argentina':
    from resources.lib.indexers import lists
    lists.indexer().root_argentina()

elif action == 'spain':
    from resources.lib.indexers import lists
    lists.indexer().root_spain()

elif action == 'iptv_git':
    from resources.lib.indexers import lists
    lists.indexer().root_iptv_git()

elif action == 'cctv':
    from resources.lib.indexers import lists
    lists.indexer().root_cctv()

elif action == 'titan':
    from resources.lib.indexers import lists
    lists.indexer().root_titan()

elif action == 'porn':
    from resources.lib.indexers import lists
    lists.indexer().root_porn()

elif action == 'faith':
    from resources.lib.indexers import lists
    lists.indexer().root_faith()

elif action == 'lust':
    from resources.lib.indexers import lists
    lists.indexer().root_lust()

elif action == 'greyhat':
    from resources.lib.indexers import lists
    lists.indexer().root_greyhat()

elif action == 'absolution':
    from resources.lib.indexers import lists
    lists.indexer().root_absolution()

elif action == 'eyecandy':
    from resources.lib.indexers import lists
    lists.indexer().root_eyecandy()

elif action == 'purplehat':
    from resources.lib.indexers import lists
    lists.indexer().root_purplehat()

elif action == 'retribution':
    from resources.lib.indexers import lists
    lists.indexer().root_retribution()

elif action == 'kiddo':
    from resources.lib.indexers import lists
    lists.indexer().root_kiddo()

elif action == 'redhat':
    from resources.lib.indexers import lists
    lists.indexer().root_redhat()

elif action == 'greenhat':
    from resources.lib.indexers import lists
    lists.indexer().root_greenhat()

elif action == 'yellowhat':
    from resources.lib.indexers import lists
    lists.indexer().root_yellowhat()

elif action == 'plist':
    from resources.lib.indexers import lists
    lists.indexer().root_personal()

elif action == 'blackhat':
    from resources.lib.indexers import lists
    lists.indexer().root_blackhat()

elif action == 'food':
    from resources.lib.indexers import lists
    lists.indexer().root_food()

elif action == 'ncaa':
    from resources.lib.indexers import lists
    lists.indexer().root_ncaa()

elif action == 'ncaab':
    from resources.lib.indexers import lists
    lists.indexer().root_ncaab()

elif action == 'lfl':
    from resources.lib.indexers import lists
    lists.indexer().root_lfl()

elif action == 'xfl':
    from resources.lib.indexers import lists
    lists.indexer().root_xfl()

elif action == 'misc_sports':
    from resources.lib.indexers import lists
    lists.indexer().root_misc_sports()

elif action == 'boxing':
    from resources.lib.indexers import lists
    lists.indexer().root_boxing()

elif action == 'tennis':
    from resources.lib.indexers import lists
    lists.indexer().root_tennis()

elif action == 'mlb':
    from resources.lib.indexers import lists
    lists.indexer().root_mlb()

elif action == 'nfl':
    from resources.lib.indexers import lists
    lists.indexer().root_nfl()

elif action == 'nhl':
    from resources.lib.indexers import lists
    lists.indexer().root_nhl()

elif action == 'nba':
    from resources.lib.indexers import lists
    lists.indexer().root_nba()

elif action == 'ufc':
    from resources.lib.indexers import lists
    lists.indexer().root_ufc()

elif action == 'fifa':
    from resources.lib.indexers import lists
    lists.indexer().root_fifa()

elif action == 'wwe':
    from resources.lib.indexers import lists
    lists.indexer().root_wwe()

elif action == 'motogp':
    from resources.lib.indexers import lists
    lists.indexer().root_motogp()

elif action == 'f1':
    from resources.lib.indexers import lists
    lists.indexer().root_f1()

elif action == 'pga':
    from resources.lib.indexers import lists
    lists.indexer().root_pga()

elif action == 'nascar':
    from resources.lib.indexers import lists
    lists.indexer().root_nascar()

elif action == 'cricket':
    from resources.lib.indexers import lists
    lists.indexer().root_cricket()

elif action == 'sports_channels':
    from resources.lib.indexers import lists
    lists.indexer().root_sports_channels()

elif action == 'sreplays':
    from resources.lib.indexers import lists
    lists.indexer().root_sreplays()

elif action == 'directory':
    from resources.lib.indexers import lists
    lists.indexer().get(url)

elif action == 'qdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import lists
    lists.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexers import lists
    lists.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import lists
    lists.indexer().youtube(url, action)

elif action == 'browser':
    from resources.lib.indexers import lists
    sports.resolver().browser(url)

elif action == 'docuNavigator':
    from resources.lib.indexers import docu
    docu.documentary().root()

elif action == 'docuHeaven':
    from resources.lib.indexers import docu
    if not docu_category == None:
        docu.documentary().docu_list(docu_category)
    elif not docu_watch == None:
        docu.documentary().docu_play(docu_watch)
    else:
        docu.documentary().root()

elif action == "furkNavigator":
    from resources.lib.indexers import navigator
    navigator.navigator().furk()

elif action == "furkMetaSearch":
    from resources.lib.indexers import furk
    furk.furk().furk_meta_search(url)

elif action == "furkSearch":
    from resources.lib.indexers import furk
    furk.furk().search()

elif action == "furkUserFiles":
    from resources.lib.indexers import furk
    furk.furk().user_files()

elif action == "furkSearchNew":
    from resources.lib.indexers import furk
    furk.furk().search_new()

elif action == 'bluehat':
    from resources.lib.indexers import navigator
    navigator.navigator().bluehat()

elif action == 'whitehat':
    from resources.lib.indexers import navigator
    navigator.navigator().whitehat()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'fluxNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().iptv_fluxus()

elif action == 'stratusNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().iptv_stratus()

elif action == 'lodgeNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().iptv_tvlodge()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'nav_add_addons':
    from resources.lib.indexers import navigator
    navigator.navigator().add_addons()

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'traktlist':
    from resources.lib.indexers import navigator
    navigator.navigator().traktlist()

elif action == 'imdblist':
    from resources.lib.indexers import navigator
    navigator.navigator().imdblist()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'libraryNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'clearAllCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheAll()

elif action == 'clearMetaCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheMeta()

elif action == 'clearCacheSearch':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheSearch()

elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'movieSearchnew':
    from resources.lib.indexers import movies
    movies.movies().search_new()

elif action == 'movieSearchterm':
    from resources.lib.indexers import movies
    movies.movies().search_term(name)

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'channels':
    from resources.lib.indexers import channels
    channels.channels().get()

elif action == 'swiftNavigator':
    from resources.lib.indexers import swift
    swift.swift().root()

elif action == 'swiftCat':
    from resources.lib.indexers import swift
    swift.swift().swiftCategory(url)

elif action == 'swiftPlay':
    from resources.lib.indexers import swift
    swift.swift().swiftPlay(url)

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvSearchnew':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_new()

elif action == 'tvSearchterm':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term(name)

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url, windowedtrailer)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'ResolveUrlTorrent':
    from resources.lib.modules import control
    control.openSettings(query, "script.module.resolveurl")

elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try:
        downloader.download(name, image, sources.sources(
        ).sourcesResolve(json.loads(source)[0], True))
    except:
        pass

elif action == 'play':
    from resources.lib.indexers import lists
    if not content == None:
        lists.player().play(url, content)
    else:
        from resources.lib.modules import sources
        sources.sources().play(title, year, imdb, tvdb, season,
                               episode, tvshowtitle, premiered, meta, select)

elif action == 'play1':
    from resources.lib.indexers import lists
    if not content == None:
        lists.player().play(url, content)
    else:
        from resources.lib.modules import sources
        sources.sources().play(title, year, imdb, tvdb, season,
                               episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb,
                                        season, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb,
                                       tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1, len(rlist))-1
        for p in ['title', 'year', 'imdb', 'tvdb', 'season', 'episode', 'tvshowtitle', 'premiered', 'select']:
            if rtype == "show" and p == "tvshowtitle":
                try:
                    r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except:
                    pass
            else:
                try:
                    r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except:
                    pass
        try:
            r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except:
            r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try:
                control.infoDialog(rlist[rand]['title'], control.lang(
                    32536).encode('utf-8'), time=30000)
            except:
                pass
        elif rtype == "episode":
            try:
                control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season'] +
                                   " - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except:
                pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)

elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'moviesToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libmovies().silent(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'tvshowsToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libtvshows().silent(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()

elif action == 'urlResolver':
    try:
        import resolveurl
    except:
        pass
    resolveurl.display_settings()

elif action == 'newsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().news()

elif action == 'collectionsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().collections()

elif action == 'collectionActors':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionActors()

elif action == 'collectionBoxset':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionBoxset()

elif action == 'collectionBoxsetKids':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionBoxsetKids()

elif action == 'collectionKids':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionKids()

elif action == 'collectionSuperhero':
    from resources.lib.indexers import navigator
    navigator.navigator().collectionSuperhero()

elif action == 'collections':
    from resources.lib.indexers import collections
    collections.collections().get(url)

elif action == 'holidaysNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().holidays()

elif action == 'halloweenNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().halloween()

elif action == 'bugReports':
    from resources.lib.reports import bugreports
    bugreports.BugReporter()
