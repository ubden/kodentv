# -*- coding: utf-8 -*-

import sys,urllib,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin
from resources.lib.modules import control

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
action = params.get('action')
mode = params.get('mode')
subid = params.get('subid')
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
docu_category = params.get('docuCat')
docu_watch = params.get('docuPlay')
podcast_show = params.get('podcastshow')
podcast_cat = params.get('podcastlist')
podcast_cats = params.get('podcastcategories')
podcast_episode = params.get('podcastepisode')
arconai_cable = params.get('arconai_cable')
arconai_shows = params.get('arconai_shows')
arconai_movies = params.get('arconai_movies')
arconai_play = params.get('arconai_play')
selection = params.get('selection')
url = params.get('url')
image = params.get('image')
meta = params.get('meta')
select = params.get('select')
query = params.get('query')
source = params.get('source')
content = params.get('content')
folder = params.get('folder')
poster = params.get('poster')
setting = params.get('setting')
windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ("0","1") else 0


if action == None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    navigator.navigator().root()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'mylistsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mylists()

elif action == 'myTraktMoviesNav':
    from resources.lib.indexers import navigator
    navigator.navigator().mytraktmovies()

elif action == 'myTraktTvShowsNav':
    from resources.lib.indexers import navigator
    navigator.navigator().mytrakttvshows()

elif action == 'myIMDbMoviesNav':
    from resources.lib.indexers import navigator
    navigator.navigator().myimdbmovies()

elif action == 'myIMDbTvShowsNav':
    from resources.lib.indexers import navigator
    navigator.navigator().myimdbtvshows()

elif action == 'channels':
    from resources.lib.indexers import channels
    channels.channels().get()

elif action == 'moreplugs':
    from resources.lib.indexers import navigator
    navigator.navigator().moreplugs()

elif action == 'movieMosts':
    from resources.lib.indexers import navigator
    navigator.navigator().movieMosts()

elif action == 'showMosts':
    from resources.lib.indexers import navigator
    navigator.navigator().showMosts()

elif action == 'imdbLists':
    from resources.lib.indexers import navigator
    navigator.navigator().imdbLists()

elif action == 'tmdbLists':
    from resources.lib.indexers import navigator
    navigator.navigator().tmdbLists()

elif action == 'myimdbMovieLists':
    from resources.lib.indexers import movies
    movies.movies().my_imdbUserLists()

elif action == 'mytmdbMovieLists':
    from resources.lib.indexers import movies2
    movies2.movies().my_tmdbUserLists()

elif action == 'myimdbTvLists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().my_imdbUserLists()

elif action == 'mytmdbTvLists':
    from resources.lib.indexers import tvshows2
    tvshows2.tvshows().my_tmdbUserLists()

elif action == 'hellaLifeTimeHallMark':
    from resources.lib.indexers import movies
    movies.movies().hellaLifeTimeHallMark()

elif action == 'tmdbUserLists':
    from resources.lib.indexers import tvshows2
    tvshows2.tvshows().tmdbUserLists()

elif action == 'tmdbActorCollections':
    from resources.lib.indexers import movies2
    movies2.movies().tmdbUserLists_ActorCollections()

elif action == 'tmdbDCvsMarvel':
    from resources.lib.indexers import movies2
    movies2.movies().tmdbUserLists_DCvsMarvel()

elif action == 'tmdbHolidays':
    from resources.lib.indexers import movies2
    movies2.movies().tmdbUserLists_Holidays()

elif action == 'tmdbAssortment':
    from resources.lib.indexers import movies2
    movies2.movies().tmdbUserLists_Assortment()

elif action == 'tmdbCollections':
    from resources.lib.indexers import movies2
    movies2.movies().tmdbUserLists_Collections()

elif action == 'tmdbCollectionsDupes':
    from resources.lib.indexers import movies2
    movies2.movies().tmdbUserLists_CollectionsDupes()

elif action == 'movies2':
    from resources.lib.indexers import movies2
    movies2.movies().get(url)

elif action == 'tvshows2':
    from resources.lib.indexers import tvshows2
    tvshows2.tvshows().get(url)

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

elif action == 'movieExploreKeywords':
    from resources.lib.indexers import movies
    movies.movies().exploreKeywords()

elif action == 'tvshowExploreKeywords':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().exploreKeywords()

elif action == 'movieimdbUserLists':
    from resources.lib.indexers import movies
    movies.movies().imdbUserLists()

elif action == 'tvshowimdbUserLists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().imdbUserLists()

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

elif action == 'tvNetworksNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvNetworksNavigator()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvCanadanetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tvCanadanetworks()

elif action == 'tvUnitedKingdomnetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tvUnitedKingdomnetworks()

elif action == 'tvAustralianetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tvAustralianetworks()

elif action == 'tvOthers1networks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tvOthers1networks()

elif action == 'tvOthers2networks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().tvOthers2networks()

elif action == 'tvWebChannels':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().webchannels()

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

elif action == 'tvReviews':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'movieReviews':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

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

elif action == 'smuSettings':
    try: import resolveurl
    except: pass
    resolveurl.display_settings()

elif action == 'urlResolver':
    try: import resolveurl
    except: pass
    resolveurl.display_settings()

elif action == 'download':
    import json
    from resources.lib.modules import sources,downloader
    try:
        downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except:
        pass

elif action == 'docuHeaven':
    from resources.lib.indexers import docu
    if not docu_category == None:
        docu.documentary().docu_list(docu_category)
    elif not docu_watch == None:
        docu.documentary().docu_play(docu_watch)
    else:
        docu.documentary().root()

elif action == 'kidscorner':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'fitness':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'legends':
    from resources.lib.indexers import youtube
    if subid == None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'podcastNavigator':
    from resources.lib.indexers import podcast
    podcast.podcast().root()

elif action == 'podbay':
    from resources.lib.indexers import podcast
    if not podcast_show == None:
        podcast.podcast().pb_show(podcast_show)
    elif not podcast_cat == None:
        podcast.podcast().pb_cat(podcast_cat)
    elif not podcast_cats == None:
        podcast.podcast().pb_root()
    elif not podcast_episode == None:
        podcast.podcast().podcast_play(action, podcast_episode)
    else:
        podcast.podcast().pb_root()

elif action == 'podcastOne':
    from resources.lib.indexers import podcast
    if not podcast_show == None:
        podcast.podcast().pco_show(podcast_show)
    elif not podcast_cat == None:
        podcast.podcast().pco_cat(podcast_cat)
    elif not podcast_cats == None:
        podcast.podcast().pcocats_list()
    elif not podcast_episode == None:
        podcast.podcast().podcast_play(action, podcast_episode)
    else:
        podcast.podcast().pco_root()

elif action == 'wrestlingNavigator':
    from resources.lib.indexers import watchwrestling
    watchwrestling.WatchWrestling().root()

elif action == 'wrestlingMenuLA':
    from resources.lib.indexers import watchwrestling
    watchwrestling.WatchWrestling().rootLA()

elif action == 'wrestlingMenuCZ':
    from resources.lib.indexers import watchwrestling
    watchwrestling.WatchWrestling().rootCZ()

elif action == 'wrestlingMenu24':
    from resources.lib.indexers import watchwrestling
    watchwrestling.WatchWrestling().root24()

elif action == 'wrestlingMenuAWL':
    from resources.lib.indexers import watchwrestling
    watchwrestling.WatchWrestling().rootAWL()

elif action == 'wrestlingScrape':
    from resources.lib.indexers import watchwrestling
    watchwrestling.WatchWrestling().scrape(url)

elif action == 'wrestlingPlay':
    from resources.lib.indexers import watchwrestling
    watchwrestling.WatchWrestling().play(url)

elif action == 'iptvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().iptvplug()

elif action == 'acronaitv_menu':
    from resources.lib.indexers import acronaitv
    acronaitv.acronaitv().list_categories()

elif action == 'arconai_cable':
    from resources.lib.indexers import acronaitv
    acronaitv.acronaitv().list_cable()

elif action == 'arconai_shows':
    from resources.lib.indexers import acronaitv
    acronaitv.acronaitv().list_shows()

elif action == 'arconai_movies':
    from resources.lib.indexers import acronaitv
    acronaitv.acronaitv().list_movies()

elif action == 'arconai_play':
    from resources.lib.indexers import acronaitv
    acronaitv.acronaitv().play_video(params['selection'])

elif action == 'ustvgoNavigator':
    from resources.lib.indexers import ustvgo
    ustvgo.ustvgo().root()

elif action == 'ustvgoPlay':
    from resources.lib.indexers import ustvgo
    ustvgo.ustvgo().play(url)

elif action == 'streamliveNavigator':
    from resources.lib.indexers import streamlive
    streamlive.streamlive().root()

elif action == 'streamlivePlay':
    from resources.lib.indexers import streamlive
    streamlive.streamlive().play(url)

elif action == 'hightimesNavigator':
    from resources.lib.indexers import hightimes
    hightimes.hightimes().root()

elif action == 'getFreeWeed':
    from resources.lib.indexers import hightimes
    hightimes.hightimes().getFreeWeed()

elif action == 'highPlay':
    from resources.lib.indexers import hightimes
    hightimes.hightimes().play(url)

elif action == 'radioNavigator':
    from resources.lib.indexers import tunes
    tunes.radionet().root()

elif action == 'radio':
    from resources.lib.indexers import tunes
    tunes.radionet().get_stations(url)

elif action == 'radioCat':
    from resources.lib.indexers import tunes
    tunes.radionet().get_categories(url)

elif action == 'radioCatStations':
    from resources.lib.indexers import tunes
    tunes.radionet().get_category_stations(url)

elif action == 'radioPlayStation':
    from resources.lib.indexers import tunes
    tunes.radionet().play_station(url)

if action == 'jewMC':
    from resources.lib.indexers import lists
    lists.indexer().rootMC()

if action == 'iptvChannels':
    from resources.lib.indexers import lists
    lists.indexer().root()

if action == 'navXXX':
    from resources.lib.indexers import lists
    lists.indexer().rootXXX()

if action == 'navCustom':
    from resources.lib.indexers import lists
    lists.indexer().rootCustom()

elif action == 'directory':
    from resources.lib.indexers import lists
    lists.indexer().get(url)

elif action == 'qdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import lists
    lists.indexer().getx(url)

elif action == 'listssearch':
    from resources.lib.indexers import lists
    lists.indexer().search(url)

elif action == 'tvtuner':
    from resources.lib.indexers import lists
    lists.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import lists
    lists.indexer().youtube(url, action)

elif action == 'browser':
    from resources.lib.indexers import lists
    lists.resolver().browser(url)

elif action == 'lists_play':
    from resources.lib.indexers import lists
    lists.player().play(url, content)

elif action == 'play':
    from resources.lib.modules import sources
    sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

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

elif action == 'disableAll':
    from resources.lib.modules import sources
    sources.sources().disableAll()

elif action == 'enableAll':
    from resources.lib.modules import sources
    sources.sources().enableAll()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0] + "?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0] + "?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0] + "?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0] + "?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1,len(rlist))-1
        for p in ['title', 'year', 'imdb', 'tvdb', 'season', 'episode', 'tvshowtitle', 'premiered', 'select']:
            if rtype == "show" and p == "tvshowtitle":
                try:
                    r += '&' + p + '=' + urllib.quote_plus(rlist[rand]['title'])
                except:
                    pass
            else:
                try:
                    r += '&' + p + '=' + urllib.quote_plus(rlist[rand][p])
                except:
                    pass
        try:
            r += '&meta=' + urllib.quote_plus(json.dumps(rlist[rand]))
        except:
            r += '&meta=' + urllib.quote_plus("{}")
        if rtype == "movie":
            try:
                control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except:
                pass
        elif rtype == "episode":
            try:
                control.infoDialog(rlist[rand]['tvshowtitle'] + " - Season " + rlist[rand]['season'] + " - " + rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
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

elif action == 'ShowChangelog':
    from resources.lib.modules import changelog
    changelog.get()	

elif action == 'PairEm':
    from resources.lib.indexers import pairem
    pairem.pairmenuoptions()

elif action == 'urlResolverRDTorrent':
     from resources.lib.modules import control
     control.openSettings(query, "script.module.resolveurl")

elif action == 'colorChoiceUI':
    from resources.lib.modules import colorChoice
    colorChoice.colorChoiceUI()

elif action == 'colorChoicePI':
    from resources.lib.modules import colorChoice
    colorChoice.colorChoicePI()

elif action == 'colorChoiceTI':
    from resources.lib.modules import colorChoice
    colorChoice.colorChoiceTI()

elif action == 'ToggleDbird':
     from resources.lib.indexers import navigator
     navigator.navigator().Toggle_Dbird()
     control.refresh()

elif action == 'ToggleAdbird':
     from resources.lib.indexers import navigator
     navigator.navigator().Toggle_Adbird()
     control.refresh()

elif action == 'TogglePreMe':
     from resources.lib.indexers import navigator
     navigator.navigator().Toggle_PreMe()
     control.refresh()

elif action == 'devtoolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().devtools()

elif action == 'TipsPlaceHolder':
    control.infoDialog(control.lang(101011).encode('utf-8'), sound=True, icon='INFO')

elif action == 'clearResolveURLcache':
    if control.condVisibility('System.HasAddon(script.module.resolveurl)'):
        control.execute('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache)')

def toggleAll(setting, query=None, sourceList=None):
    from resources.lib.sources import getAllHosters
    sourceList = getAllHosters() if not sourceList else sourceList
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, setting)
    control.openSettings(query)

if mode == "toggleAllNormal":
    sourcelist = ['123123movies', '1movietv', '1putlocker', '5movies', 'allucxyz', 'bnwmovies',
            'cartoonhd', 'cartoonhdto', 'cartoonwire', 'cmovies', 'cmovieshd', 'cmovieshdbz', 'cooltvseries',
            'couchtuner2', 'extramovies', 'ffilms', 'filmxy', 'flenixonline', 'flixgo', 'fmoviesag', 'fmoviesio',
            'ganool123', 'geektv', 'gomo', 'gostream123', 'gostream123net', 'gostreamcool', 'gowatchseries',
            'hdbest', 'hdmto', 'hdpopcorns', 'hubmovie', 'iwannawatch', 'letmewatchthis', 'mkvhub', 'movie4kis',
            'moviescouch', 'mycoolmoviezone', 'mycouchtuner', 'myhdpopcorn', 'mymovie4k', 'myswatchseri',
            'mywatchep4', 'mywatchepseries', 'putlockerfree', 'putlockersio', 'putlockersonline', 'putlockersplus',
            'rarefilmm', 'seehd', 'series9', 'seriesfree', 'seriesonline', 'solarmoviefree', 'streamdreams', 'streamsnow',
            'telepisodes', 'timewatch', 'tvbox', 'tvmovieflix', 'watchseries', 'watchserieshd', 'watchseriessi',
            'watchseriestv', 'yesmoviesgg'
    ]
    toggleAll(params['setting'], params['query'], sourcelist)

if mode == "toggleAllSpares":
    sourcelist = ['0123putlocker', '123moviesfish', '123movieshubz', '4anime', 'anime1', 'animedao',
            'animefreak', 'animego', 'animeheaven', 'animepark', 'animeram', 'animeshow', 'animestreams',
            'animetoon', 'animexd', 'cartoonextra', 'cartoontab', 'filmv', 'fmovies', 'ganoolrip', 'getmywatchseries',
            'gogoanime', 'gogoanime1', 'gogoanimestv', 'gomoviesonl', 'goprojectfreetv', 'hdmo', 'hdmovie8',
            'hackimdb', 'hnmovies', 'megashare9', 'movies123', 'mymoviesonline', 'myprojectfreetv', 'myputlockers',
            'newepisodes', 'pokemonfire', 'putlockered', 'putlockeronl', 'solarmovienet', 'toonget', 'toonova',
            'watch32hd', 'watchanime', 'watchseries4k', 'watchseriessto', 'wsunblock', 'zmovies'
    ]
    toggleAll(params['setting'], params['query'], sourcelist)

if mode == "toggleAllDebrid":
    sourcelist = ['0day', '2ddl', '300mbdownload', '300mbfilms', 'ddlspot',
            'directdl', 'maxrls', 'mvrls', 'rapidmoviez', 'rlsb', 'rlsbb', 'sceneddl',
            'scenerls', 'tvdownload', 'ultrahdindir', 'warezmovies'
    ]
    toggleAll(params['setting'], params['query'], sourcelist)

if mode == "toggleAllTorrent":
    sourcelist = ['1337x', 'btdb', 'btscene', 'doublr', 'eztv', 'glodls', 'kickass2', 'limetorr', 'magnetdl',
            'mkvcage', 'piratebay', 'skytorrents', 'torrapi', 'torrdown', 'torrentquest', 'xpause', 'yifyddl',
            'ytsam', 'zoogle'
    ]
    toggleAll(params['setting'], params['query'], sourcelist)


