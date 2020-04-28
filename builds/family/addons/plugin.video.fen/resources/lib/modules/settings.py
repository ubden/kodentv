import xbmc, xbmcaddon
import os
# from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
ADDON_PATH = xbmc.translatePath(__addon__.getAddonInfo('path'))
DATA_PATH = xbmc.translatePath(__addon__.getAddonInfo('profile'))

def addon_installed(addon_id):
    if xbmc.getCondVisibility('System.HasAddon(%s)' % addon_id): return True
    else: return False

def get_theme():
    if __addon__.getSetting('theme_installed') == 'true':
        theme = __addon__.getSetting('fen.theme').lower()
        result = os.path.join(xbmcaddon.Addon('script.tiki.artwork').getAddonInfo('path'), 'resources', 'media', theme)
    elif addon_installed('script.tiki.artwork'):
        __addon__.setSetting('theme_installed', 'true')
        theme = __addon__.getSetting('fen.theme').lower()
        if theme in ['-', '']: theme = 'light'
        result = os.path.join(xbmcaddon.Addon('script.tiki.artwork').getAddonInfo('path'), 'resources', 'media', theme)
    else: result = 'null'
    return result

def tmdb_api_check():
    tmdb_api = __addon__.getSetting('tmdb_api')
    if not tmdb_api or tmdb_api == '':
        tmdb_api = '1b0d3c6ac6a6c0fa87b55a1069d6c9c8'
    return tmdb_api

def check_database(database):
    import xbmcvfs
    if not xbmcvfs.exists(database): initialize_databases()

def display_mode():
    try: return int(__addon__.getSetting('display_mode'))
    except: return 0

def addon():
    return __addon__

def store_resolved_torrent_to_cloud(debrid_service):
    if __addon__.getSetting('store_torrent.%s' % debrid_service.lower()) == 'true': return True
    return False

def active_store_torrent_to_cloud():
    active = []
    for debrid_service in [('real-debrid', 'RD', 'Real Debrid'), ('premiumize.me', 'PM', 'Premiumize'), ('alldebrid', 'AD', 'All Debrid')]:
        if __addon__.getSetting('store_torrent.%s' % debrid_service[0].lower()) == 'true':
            active.append(debrid_service)
    return active

def show_specials():
    if __addon__.getSetting('show_specials') == 'true': return True
    else: return False

def cache_page():
    if __addon__.getSetting('cache_browsed_page') == 'true': return True
    else: return False

def thread_main_menus():
    if __addon__.getSetting('thread_main_menus') == 'true': return True
    else: return False

def auto_start_fen():
    if __addon__.getSetting('auto_start_fen') == 'true': return True
    else: return False

def setview_delay():
    try: return float(int(__addon__.getSetting('setview_delay')))/1000
    except: return 800/1000

def adjusted_datetime(string=False, dt=False):
    from datetime import datetime, timedelta
    d = datetime.utcnow() + timedelta(hours=int(__addon__.getSetting('datetime.offset')))
    if dt: return d
    d = datetime.date(d)
    if string:
        try: d = d.strftime('%Y-%m-%d')
        except ValueError: d = d.strftime('%Y-%m-%d')
    else: return d

def date_to_timestamp(date_str, format="%Y-%m-%d"):
    import time
    if date_str:
        try:
            tt = time.strptime(date_str, format)
            return int(time.mktime(tt))
        except:
            return 0  # 1970
    return None

def add_release_date():
    if __addon__.getSetting('subscriptions.add_release_date') == "true": return True
    else: return False
    
def movies_directory():
    return xbmc.translatePath(__addon__.getSetting('movies_directory'))
    
def tv_show_directory():
    return xbmc.translatePath(__addon__.getSetting('tv_shows_directory'))

def download_directory(db_type):
    setting = 'movie_download_directory' if db_type == 'movie' \
        else 'tvshow_download_directory' if db_type == 'episode' \
        else 'premium_download_directory'
    if __addon__.getSetting(setting) != '': return xbmc.translatePath( __addon__.getSetting(setting))
    else: return False

def source_folders_directory(db_type, source):
    setting = '%s.movies_directory' % source if db_type == 'movie' else '%s.tv_shows_directory' % source
    if __addon__.getSetting(setting) not in ('', 'None', None): return xbmc.translatePath( __addon__.getSetting(setting))
    else: return False

def paginate():
    if __addon__.getSetting('paginate.lists') == "true": return True
    else: return False

def page_limit():
    try: page_limit = int(__addon__.getSetting('page_limit'))
    except: page_limit = 20
    return page_limit

def ignore_articles():
    if __addon__.getSetting('ignore_articles') == "true": return True
    else: return False

def default_openinfo():
    return int(__addon__.getSetting('default_openinfo'))

def default_all_episodes():
    if __addon__.getSetting('default_all_episodes') == "true": return True
    else: return False

def quality_filter(setting):
    return __addon__.getSetting(setting).split(', ')

def include_prerelease_results():
    if __addon__.getSetting('include_prerelease_results') == "true": return True
    else: return False

def include_sources_in_filter(source_setting):
    if __addon__.getSetting('%s_in_filter' % source_setting) == "true": return True
    else: return False

def include_uncached_results():
    if __addon__.getSetting('include_uncached_results') == "true": return True
    else: return False

def auto_play():
    if __addon__.getSetting('auto_play') == "true": return True
    else: return False

def autoplay_next_episode():
    if auto_play() and __addon__.getSetting('autoplay_next_episode') == "true": return True
    else: return False

def autoplay_next_check_threshold():
    return int(__addon__.getSetting('autoplay_next_check_threshold'))

def autoplay_hevc():
    return __addon__.getSetting('autoplay_hevc')

def sync_kodi_library_watchstatus():
    if __addon__.getSetting('sync_kodi_library_watchstatus') == "true": return True
    else: return False

def refresh_trakt_on_startup():
    if __addon__.getSetting('refresh_trakt_on_startup') == "true": return True
    else: return False
    
def trakt_cache_duration():
    duration = (1, 24, 168)
    return duration[int(__addon__.getSetting('trakt_cache_duration'))]

def trakt_calendar_days():
    import datetime
    try: previous_days = int(__addon__.getSetting('trakt.calendar_previous_days'))
    except: previous_days = 3
    try: future_days = int(__addon__.getSetting('trakt.calendar_future_days'))
    except: future_days = 7
    current_date = adjusted_datetime()
    start = (current_date - datetime.timedelta(days=previous_days)).strftime('%Y-%m-%d')
    finish = previous_days + future_days
    return (start, finish)

def calendar_focus_today():
    if __addon__.getSetting('calendar_focus_today') == 'true': return True
    else: return False

def watched_indicators():
    if __addon__.getSetting('trakt_user') == '': return 0
    watched_indicators = __addon__.getSetting('watched_indicators')
    if watched_indicators == '0': return 0
    if watched_indicators == '1' and __addon__.getSetting('sync_fen_watchstatus') == 'true': return 1
    return 2

def check_prescrape_sources(scraper):
    if __addon__.getSetting('check.%s' % scraper) == "true" and __addon__.getSetting('auto_play') != "true": return True
    else: return False

def subscription_update():
    if __addon__.getSetting('subscription_update') == "true": return True
    else: return False

def subscription_service_time():
    time =  __addon__.getSetting('service_time')
    return time

def trakt_list_subscriptions():
    if __addon__.getSetting('trakt.subscriptions_active') == "true": return True
    else: return False

def skip_duplicates():
    if __addon__.getSetting('skip_duplicates') == "true": return True
    else: return False

def update_library_after_service():
    if __addon__.getSetting('update_library_after_service') == "true": return True
    else: return False

def clean_library_after_service():
    if __addon__.getSetting('clean_library_after_service') == "true": return True
    else: return False

def subscriptions_add_unknown_airdate():
    if __addon__.getSetting('subscriptions.add_unknown_airdate') == "true": return True
    else: return False

def internal_scraper_order():
    return __addon__.getSetting('internal_scrapers_order').split(', ')

def results_sort_order():
    results_sort_order = __addon__.getSetting('results.sort_order')
    if results_sort_order == '0': return ['quality_rank', 'name_rank', 'size']
    elif results_sort_order == '1': return ['name_rank', 'quality_rank', 'size']
    else: return ['', '', '']

def sorted_first(scraper_setting):
    if __addon__.getSetting('results.%s' % scraper_setting) == "true": return True
    else: return False

def provider_color(provider):
    return __addon__.getSetting('provider.%s_colour' % provider)

def active_scrapers(group_folders=False):
    folders = ['folder1', 'folder2', 'folder3', 'folder4', 'folder5']
    settings = ['provider.external', 'provider.furk', 'provider.easynews', 'provider.rd-cloud', 'provider.pm-cloud', 'provider.ad-cloud',
                'provider.local', 'provider.downloads']
    active = [i.split('.')[1] for i in settings if __addon__.getSetting(i) == 'true']
    if __addon__.getSetting('provider.folders') == 'true':
        if group_folders: active.append('folders')
        else: active += folders
    return active

def multiline_results():
    if __addon__.getSetting('results.multiline_label') == "true": return True
    else: return False

def show_extra_info():
    if __addon__.getSetting('results.show_extra_info') == 'true': return True
    return False

def show_filenames():
    if __addon__.getSetting('results.show_filenames') == 'true': return True
    return False

def subscription_timer():
    if __addon__.getSetting('subsciptions.update_type') == '1': return 24
    return int(__addon__.getSetting('subscription_timer'))

def auto_resume():
    auto_resume = __addon__.getSetting('auto_resume')
    if auto_resume == '1': return True
    if auto_resume == '2' and auto_play(): return True
    else: return False

def set_resume():
    return float(__addon__.getSetting('resume.threshold'))

def set_watched():
    return float(__addon__.getSetting('watched.threshold'))

def nextep_threshold():
    return float(__addon__.getSetting('nextep.threshold'))

def nav_jump_use_alphabet():
    if __addon__.getSetting('cache_browsed_page') == 'true': return False
    if __addon__.getSetting('nav_jump') == '0': return False
    else: return True

def all_trailers():
    if __addon__.getSetting('all_trailers') == "true": return True
    else: return False

def use_season_title():
    if __addon__.getSetting('use_season_title') == "true": return True
    else: return False

def unaired_episode_colour():
    unaired_episode_colour = __addon__.getSetting('unaired_episode_colour')
    if not unaired_episode_colour or unaired_episode_colour == '': unaired_episode_colour = 'red'
    return unaired_episode_colour

def nextep_airdate_format():
    date_format = __addon__.getSetting('nextep.airdate_format')
    if date_format == '0': return '%d-%m-%Y'
    elif date_format == '1': return '%Y-%m-%d'
    elif date_format == '2': return '%m-%d-%Y'
    else: return '%Y-%m-%d'

def nextep_display_settings():
    from ast import literal_eval
    cache_to_disk = False
    include_airdate = True
    force_display = False
    airdate_colour = 'magenta'
    unaired_colour = 'red'
    unwatched_colour = 'darkgoldenrod'
    try: include_airdate = literal_eval(__addon__.getSetting('nextep.include_airdate').title())
    except: pass
    try: airdate_colour = __addon__.getSetting('nextep.airdate_colour')
    except: pass
    try: unaired_colour = __addon__.getSetting('nextep.unaired_colour')
    except: pass
    try: unwatched_colour = __addon__.getSetting('nextep.unwatched_colour')
    except: pass
    return {'include_airdate': include_airdate, 'airdate_colour': airdate_colour,
            'unaired_colour': unaired_colour, 'unwatched_colour': unwatched_colour}

def nextep_content_settings():
    from ast import literal_eval
    sort_type = int(__addon__.getSetting('nextep.sort_type'))
    sort_order = int(__addon__.getSetting('nextep.sort_order'))
    sort_direction = True if sort_order == 0 else False
    sort_key = 'curr_last_played_parsed' if sort_type == 0 else 'first_aired' if sort_type == 1 else 'name'
    cache_to_disk = literal_eval(__addon__.getSetting('nextep.cache_to_disk').title())
    include_unaired = literal_eval(__addon__.getSetting('nextep.include_unaired').title())
    include_unwatched = literal_eval(__addon__.getSetting('nextep.include_unwatched').title())
    return {'cache_to_disk': cache_to_disk, 'sort_key': sort_key, 'sort_direction': sort_direction, 'sort_type': sort_type, 'sort_order':sort_order,
            'include_unaired': include_unaired, 'include_unwatched': include_unwatched}

def scraping_settings():
    multiline = multiline_results()
    extra_info = show_extra_info()
    enable_filenames = show_filenames()
    try: multiline_highlight = __addon__.getSetting('secondline.identify')
    except: multiline_highlight = ''
    if multiline_highlight.lower() == 'no color': multiline_highlight = ''
    highlight_type = __addon__.getSetting('highlight.type')
    if highlight_type == '': highlight_type = '0'
    highlight_4K = __addon__.getSetting('scraper_4k_highlight')
    if highlight_4K == '': highlight_4K = 'magenta'
    highlight_1080p = __addon__.getSetting('scraper_1080p_highlight')
    if highlight_1080p == '': highlight_1080p = 'lawngreen'
    highlight_720p = __addon__.getSetting('scraper_720p_highlight')
    if highlight_720p == '': highlight_720p = 'gold'
    highlight_SD = __addon__.getSetting('scraper_SD_highlight')
    if highlight_SD == '': highlight_SD = 'lightsaltegray'
    premium_highlight = __addon__.getSetting('prem.identify')
    if premium_highlight == '': premium_highlight = 'blue'
    elif premium_highlight.lower() == 'no color': premium_highlight = ''
    torrent_highlight = __addon__.getSetting('torrent.identify')
    if torrent_highlight == '': torrent_highlight = 'magenta'
    elif torrent_highlight.lower() == 'no color': torrent_highlight = ''
    return {'multiline': multiline, 'extra_info': extra_info, 'show_filenames': enable_filenames,
            'multiline_highlight': multiline_highlight, 'highlight_type': highlight_type,
            'highlight_4K': highlight_4K, 'highlight_1080p': highlight_1080p, 'highlight_720p': highlight_720p,
            'highlight_SD': highlight_SD, 'premium_highlight': premium_highlight, 'torrent_highlight': torrent_highlight}

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def initialize_databases():
    import xbmcvfs
    try: from sqlite3 import dbapi2 as database
    except ImportError: from pysqlite2 import dbapi2 as database
    if not xbmcvfs.exists(DATA_PATH): xbmcvfs.mkdirs(DATA_PATH)
    NAVIGATOR_DB = os.path.join(DATA_PATH, "navigator.db")
    WATCHED_DB = os.path.join(DATA_PATH, "watched_status.db")
    FAVOURITES_DB = os.path.join(DATA_PATH, "favourites.db")
    VIEWS_DB = os.path.join(DATA_PATH, "views.db")
    TRAKT_DB = os.path.join(DATA_PATH, "fen_trakt.db")
    FEN_DB = os.path.join(DATA_PATH, "fen_cache.db")
    #Always check NAVIGATOR.
    dbcon = database.connect(NAVIGATOR_DB)
    dbcon.execute("""CREATE TABLE IF NOT EXISTS navigator
                      (list_name text, list_type text, list_contents text) 
                   """)
    if not xbmcvfs.exists(WATCHED_DB):
        dbcon = database.connect(WATCHED_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS progress
                          (db_type text, media_id text, season integer, episode integer,
                          resume_point text, curr_time text,
                          unique(db_type, media_id, season, episode)) 
                       """)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS watched_status
                          (db_type text, media_id text, season integer,
                          episode integer, last_played text, title text,
                          unique(db_type, media_id, season, episode)) 
                       """)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS exclude_from_next_episode
                          (media_id text, title text) 
                       """)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS unwatched_next_episode
                          (media_id text) 
                       """)
        dbcon.close()
    if not xbmcvfs.exists(FAVOURITES_DB):
        dbcon = database.connect(FAVOURITES_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS favourites
                          (db_type text, tmdb_id text, title text, unique (db_type, tmdb_id)) 
                       """)
        dbcon.close()
    if not xbmcvfs.exists(VIEWS_DB):
        dbcon = database.connect(VIEWS_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS views
                          (view_type text, view_id text, unique (view_type)) 
                       """)
        dbcon.close()
    if not xbmcvfs.exists(TRAKT_DB):
        dbcon = database.connect(TRAKT_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS fen_trakt
                           (id text UNIQUE, expires integer, data text)
                            """)
        dbcon.close()
    if not xbmcvfs.exists(FEN_DB):
        dbcon = database.connect(FEN_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS fencache
                           (id text UNIQUE, expires integer, data text, checksum integer)
                            """)
        dbcon.close()
    return True

def media_lists():
    ''' this list is for clearing list cache'''
    return (
        'tmdb_movies_popular%',
        'tmdb_movies_blockbusters%',
        'tmdb_movies_in_theaters%',
        'tmdb_movies_top_rated%',
        'tmdb_movies_upcoming%',
        'tmdb_movies_latest_releases%',
        'tmdb_movies_premieres%',
        'trakt_movies_trending%',
        'trakt_movies_anticipated%',
        'trakt_movies_top10_boxoffice%',
        'trakt_movies_top10_boxoffice%',
        'trakt_trending_user_lists%',
        'trakt_popular_user_lists',
        'imdb_movies_oscar_winners%',
        'tmdb_popular_people%'
        'trakt_movies_mosts%',
        'tmdb_movies_genres%',
        'tmdb_movies_languages%',
        'tmdb_movies_year%',
        'tmdb_movies_certifications%',
        'tmdb_movies_similar%',
        'tmdb_movies_recommendations%',
        'tmdb_movies_actor_roles%',
        'tmdb_movies_search%',
        'tmdb_movies_people_search%',
        'tmdb_tv_popular%',
        'tmdb_tv_top_rated%',
        'tmdb_tv_premieres%',
        'tmdb_tv_upcoming%',
        'tmdb_tv_airing_today%',
        'tmdb_tv_on_the_air%',
        'trakt_tv_anticipated%',
        'trakt_tv_trending%',
        'trakt_tv_mosts%',
        'tmdb_tv_genres%',
        'tmdb_tv_languages%',
        'tmdb_tv_networks%',
        'trakt_tv_certifications%',
        'tmdb_tv_year%',
        'tmdb_tv_similar%',
        'tmdb_tv_recommendations%',
        'tmdb_tv_actor_roles%',
        'tmdb_tv_search%',
        'tmdb_tv_people_search%',
        'tmdb_images_person%'
        )
