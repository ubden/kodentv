import xbmc, xbmcvfs, xbmcaddon, xbmcplugin, xbmcgui
import sys, os
import json
import time
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
try: from urllib import urlencode
except ImportError: from urllib.parse import urlencode
from indexers.default_menus import DefaultMenus
from modules.utils import to_utf8
from modules import settings
try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
NAVIGATOR_DB = os.path.join(profile_dir, "navigator.db")
window = xbmcgui.Window(10000)

class Navigator:
    def __init__(self, list_name=None):
        self.view = 'view.main'
        self.icon_directory = settings.get_theme()
        self.list_name = list_name
        self.fanart = os.path.join(addon_dir, 'fanart.png')

    def main_lists(self):
        if self.list_name == 'RootList': self._changelog_info()
        self.build_main_lists()

    def downloads(self):
        movie_path = settings.download_directory('movie')
        episode_path = settings.download_directory('episode')
        premium_path = settings.download_directory('premium')
        self._add_dir({'mode': 'navigator.folder_navigator', 'folder_path': movie_path, 'foldername': 'Movie Downloads', 'list_name': 'Movie Downloads'}, '[B]DOWNLOADS: [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'navigator.folder_navigator', 'folder_path': episode_path, 'foldername': 'TV Show Downloads', 'list_name': 'TV Show Downloads'}, '[B]DOWNLOADS: [/B]TV Shows', iconImage='tv.png')
        self._add_dir({'mode': 'navigator.folder_navigator', 'folder_path': premium_path, 'foldername': 'Premium File Downloads', 'list_name': 'Premium File Downloads'}, '[B]DOWNLOADS: [/B]Premium Files', iconImage='premium.png')
        self._end_directory()

    def discover_main(self):
        self._add_dir({'mode': 'discover.movie', 'db_type': 'movie', 'foldername': 'Discover Movies', 'list_name': 'Discover Movies'}, '[B]DISCOVER : [/B]Movies', iconImage='discover.png')
        self._add_dir({'mode': 'discover.tvshow', 'db_type': 'tvshow', 'foldername': 'Discover TV Shows', 'list_name': 'Discover TV Shows'}, '[B]DISCOVER : [/B]TV Shows', iconImage='discover.png')
        self._add_dir({'mode': 'discover.history', 'db_type': 'movie', 'foldername': 'Discover Movie History', 'list_name': 'Discover Movie History'}, '[B]DISCOVER : [/B]Movie History', iconImage='discover.png')
        self._add_dir({'mode': 'discover.history', 'db_type': 'tvshow', 'foldername': 'Discover TV Show History', 'list_name': 'Discover TV Show History'}, '[B]DISCOVER : [/B]TV Show History', iconImage='discover.png')
        self._add_dir({'mode': 'discover.help', 'foldername': 'Discover Help', 'list_name': 'Discover Help'}, '[B]DISCOVER : [/B]Help', iconImage='discover.png')
        self._end_directory()

    def premium(self):
        from modules.debrid import debrid_enabled
        debrids = debrid_enabled()
        enable_fu = False if (__addon__.getSetting('furk_api_key'), __addon__.getSetting('furk_login'), __addon__.getSetting('furk_password')) == ('', '', '') else True
        enable_en = False if '' in (__addon__.getSetting('easynews_user'), __addon__.getSetting('easynews_password')) else True
        enable_debrids = (__addon__.getSetting('rd.enabled'), __addon__.getSetting('pm.enabled'), __addon__.getSetting('ad.enabled'))
        if enable_fu: self._add_dir({'mode': 'navigator.furk', 'foldername': 'Furk', 'list_name': 'Furk'}, '[B]PREMIUM : [/B]Furk', iconImage='furk.png')
        if enable_en: self._add_dir({'mode': 'navigator.easynews', 'foldername': 'Easynews', 'list_name': 'Easynews'}, '[B]PREMIUM : [/B]Easynews', iconImage='easynews.png')
        if 'Real-Debrid' in debrids: self._add_dir({'mode': 'navigator.real_debrid', 'foldername': 'Real Debrid', 'list_name': 'Real Debrid'}, '[B]PREMIUM : [/B]Real Debrid', iconImage='realdebrid.png')
        if 'Premiumize.me' in debrids: self._add_dir({'mode': 'navigator.premiumize', 'foldername': 'Premiumize', 'list_name': 'Premiumize'}, '[B]PREMIUM : [/B]Premiumize', iconImage='premiumize.png')
        if 'AllDebrid' in debrids: self._add_dir({'mode': 'navigator.alldebrid', 'foldername': 'All Debrid', 'list_name': 'All Debrid'}, '[B]PREMIUM : [/B]All Debrid', iconImage='alldebrid.png')
        self._end_directory()

    def furk(self):
        self._add_dir({'mode': 'furk.my_furk_files', 'list_type': 'file_get_video', 'foldername': 'My Furk Video Files', 'list_name': 'Furk Video Files'}, '[B]FURK: [/B]Video Files', iconImage='lists.png')
        self._add_dir({'mode': 'furk.my_furk_files', 'list_type': 'file_get_audio', 'foldername': 'My Furk Audio Files', 'list_name': 'Furk Audio Files'}, '[B]FURK: [/B]Audio Files', iconImage='lists.png')
        self._add_dir({'mode': 'furk.my_furk_files', 'list_type': 'file_get_active', 'foldername': 'My Furk Active Downloads', 'list_name': 'My Furk Active Downloads'}, '[B]FURK: [/B]Active Downloads', iconImage='lists.png')
        self._add_dir({'mode': 'furk.my_furk_files', 'list_type': 'file_get_failed', 'foldername': 'My Furk Failed Downloads', 'list_name': 'My Furk Failed Downloads'}, '[B]FURK: [/B]Failed Downloads', iconImage='lists.png')
        self._add_dir({'mode': 'furk.search_furk', 'db_type': 'video', 'foldername': 'Search Furk (Video)', 'list_name': 'Furk Search Video'}, '[B]FURK: [/B]Search (Video)', iconImage='search.png')
        self._add_dir({'mode': 'furk.search_furk', 'db_type': 'audio', 'foldername': 'Search Furk (Audio)', 'list_name': 'Furk Search Audio'}, '[B]FURK: [/B]Search (Audio)', iconImage='search.png')
        self._add_dir({'mode': 'search_history', 'action': 'furk_video', 'foldername': 'Video Search History', 'list_name': 'Furk Search History (Video)'}, '[B]FURK: [/B]Search History (Video)', iconImage='search.png')
        self._add_dir({'mode': 'search_history', 'action': 'furk_audio', 'foldername': 'Audio Search History', 'list_name': 'Furk Search History (Audio)'}, '[B]FURK: [/B]Search History (Audio)', iconImage='search.png')
        self._add_dir({'mode': 'furk.account_info', 'foldername': 'Account Info', 'list_name': 'Furk Account Info'}, '[B]FURK: [/B]Account Info', iconImage='furk.png')
        self._end_directory()

    def easynews(self):
        self._add_dir({'mode': 'easynews.search_easynews', 'foldername': 'Search Easynews (Video)', 'list_name': 'Search Easynews (Video)'}, '[B]EASYNEWS : [/B]Search (Video)', iconImage='search.png')
        self._add_dir({'mode': 'search_history', 'action': 'easynews_video', 'foldername': 'Easynews Video Search History', 'list_name': 'Search History Easynews (Video)'}, '[B]EASYNEWS: [/B]Search History (Video)', iconImage='search.png')
        self._add_dir({'mode': 'easynews.account_info', 'foldername': 'Account Info', 'list_name': 'Easynews Account Info'}, '[B]EASYNEWS: [/B]Account Info', iconImage='easynews.png')
        self._end_directory()

    def real_debrid(self):
        enable_rd = False if __addon__.getSetting('rd.token') == '' else True
        if enable_rd: self._add_dir({'mode': 'real_debrid.rd_torrent_cloud', 'foldername': 'Cloud Storage', 'list_name': 'Real Debrid Cloud Storage'}, '[B]REAL DEBRID: [/B]Cloud Storage', iconImage='realdebrid.png')
        if enable_rd: self._add_dir({'mode': 'real_debrid.rd_downloads', 'foldername': 'Download History', 'list_name': 'Real Debrid Download History'}, '[B]REAL DEBRID: [/B]Download History', iconImage='realdebrid.png')
        if enable_rd: self._add_dir({'mode': 'real_debrid.rd_account_info', 'foldername': 'Account Info', 'list_name': 'Real Debrid Account Info'}, '[B]REAL DEBRID: [/B]Account Info', iconImage='realdebrid.png')
        self._add_dir({'mode': 'real_debrid.authenticate', 'foldername': '(Re)Authorize Real-Debrid', 'list_name': 'Authorize Real-Debrid'}, '[B]REAL-DEBRID : [/B](Re)Authenticate Real-Debrid', iconImage='realdebrid.png')
        if enable_rd: self._add_dir({'mode': 'clear_cache', 'cache': 'rd_cloud', 'foldername': 'Clear Cache', 'list_name': 'Tools Clear Real Debrid Cache'}, '[B]REAL DEBRID: [/B]Clear Cloud Cache', iconImage='realdebrid.png')
        self._end_directory()

    def premiumize(self):
        enable_pm = False if __addon__.getSetting('pm.token') == '' else True
        if enable_pm: self._add_dir({'mode': 'premiumize.pm_torrent_cloud', 'foldername': 'Cloud Storage', 'list_name': 'Premiumize Cloud Storage'}, '[B]PREMIUMIZE: [/B]Cloud Storage', iconImage='premiumize.png')
        if enable_pm: self._add_dir({'mode': 'premiumize.pm_transfers', 'foldername': 'Transfer History', 'list_name': 'Premiumize Transfer History'}, '[B]PREMIUMIZE: [/B]Transfer History', iconImage='premiumize.png')
        if enable_pm: self._add_dir({'mode': 'premiumize.pm_account_info', 'foldername': 'Account Info', 'list_name': 'Premiumize Account Info'}, '[B]PREMIUMIZE: [/B]Account Info', iconImage='premiumize.png')
        self._add_dir({'mode': 'premiumize.authenticate', 'foldername': '(Re)Authorize Premiumize', 'list_name': 'Authorize Premiumize'}, '[B]PREMIUMIZE : [/B](Re)Authenticate Premiumize', iconImage='premiumize.png')
        if enable_pm: self._add_dir({'mode': 'clear_cache', 'cache': 'pm_cloud', 'foldername': 'Clear Cache', 'list_name': 'Tools Clear Premiumize Cache'}, '[B]PREMIUMIZE: [/B]Clear Cloud Cache', iconImage='premiumize.png')
        self._end_directory()

    def alldebrid(self):
        enable_ad = False if __addon__.getSetting('ad.token') == '' else True
        if enable_ad: self._add_dir({'mode': 'alldebrid.ad_torrent_cloud', 'foldername': 'Cloud Storage', 'list_name': 'All Debrid Cloud Storage'}, '[B]ALL DEBRID: [/B]Cloud Storage', iconImage='alldebrid.png')
        if enable_ad: self._add_dir({'mode': 'alldebrid.ad_account_info', 'foldername': 'Account Info', 'list_name': 'All Debrid Account Info'}, '[B]ALL DEBRID: [/B]Account Info', iconImage='alldebrid.png')
        self._add_dir({'mode': 'alldebrid.authenticate', 'foldername': '(Re)Authorize All Debrid', 'list_name': 'Authorize All Debrid'}, '[B]ALL DEBRID : [/B](Re)Authenticate All Debrid', iconImage='alldebrid.png')
        if enable_ad: self._add_dir({'mode': 'clear_cache', 'cache': 'ad_cloud', 'foldername': 'Clear Cache', 'list_name': 'Tools Clear All Debrid Cache'}, '[B]ALL DEBRID: [/B]Clear Cloud Cache', iconImage='alldebrid.png')
        self._end_directory()

    def favourites(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'favourites_movies', 'foldername': 'Movie Favourites', 'list_name': 'Movies Favourites'}, '[B]FAVOURITES : [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'favourites_tvshows', 'foldername': 'TV Show Favourites', 'list_name': 'TV Shows Favourites'}, '[B]FAVOURITES : [/B]TV Shows', iconImage='tv.png')
        self._end_directory()

    def subscriptions(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'subscriptions_movies', 'foldername': 'Fen Subscriptions', 'list_name': 'Movies Subscriptions'}, '[B]SUBSCRIPTIONS : [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'subscriptions_tvshows', 'foldername': 'Fen Subscriptions', 'list_name': 'TV Shows Subscriptions'}, '[B]SUBSCRIPTIONS : [/B]TV Shows', iconImage='tv.png')
        self._end_directory()

    def kodi_library(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'kodi_library_movies', 'foldername': 'Movies Kodi Library', 'list_name': 'Movies Kodi Library'}, '[B]KODI LIBRARY : [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'kodi_library_tvshows', 'foldername': 'TV Shows Kodi Library', 'list_name': 'TV Shows Kodi Library'}, '[B]KODI LIBRARY : [/B]TV Shows', iconImage='tv.png')
        self._add_dir({'mode': 'build_kodi_library_recently_added', 'db_type': 'movies', 'foldername': 'Recently Added Movies Kodi Library', 'list_name': 'Recently Added Movies Kodi Library'}, '[B]KODI LIBRARY : [/B]Recently Added Movies', iconImage='recently_added_movies.png')
        self._add_dir({'mode': 'build_kodi_library_recently_added', 'db_type': 'episodes', 'foldername': 'Recently Added Movies Kodi Library', 'list_name': 'Recently Added Episodes Kodi Library'}, '[B]KODI LIBRARY : [/B]Recently Added Episodes', iconImage='recently_added_episodes.png')
        self._end_directory()

    def in_progress(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'in_progress_movies', 'foldername': 'Movies In Progress', 'list_name': 'Movies In Progress'}, '[B]IN PROGRESS : [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'in_progress_tvshows', 'foldername': 'TV Shows In Progress', 'list_name': 'TV Shows In Progress'}, '[B]IN PROGRESS : [/B]TV Shows', iconImage='tv.png')
        self._add_dir({'mode': 'build_in_progress_episode', 'foldername': 'Episodes In Progress', 'list_name': 'Episodes In Progress'}, '[B]IN PROGRESS : [/B]Episodes', iconImage='episode.png')
        self._end_directory()

    def watched(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'watched_movies', 'foldername': 'Fen Watched Movies', 'list_name': 'Movies Watched'}, '[B]WATCHED : [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'watched_tvshows', 'foldername': 'Fen Watched Shows', 'list_name': 'TV Shows Watched'}, '[B]WATCHED : [/B]TV Shows', iconImage='tv.png')
        self._end_directory()

    def my_trakt_content(self):
        self._add_dir({'mode': 'navigator.trakt_collection', 'foldername': 'My Trakt Collections', 'list_name': 'Trakt My Collections'}, '[B]TRAKT: [/B]Collections', iconImage='traktcollection.png')
        self._add_dir({'mode': 'navigator.trakt_watchlist', 'foldername': 'My Trakt Watchlists', 'list_name': 'Trakt My Watchlists'}, '[B]TRAKT: [/B]Watchlists', iconImage='traktwatchlist.png')
        self._add_dir({'mode': 'trakt.get_trakt_my_lists', 'foldername': 'My Trakt Lists', 'list_name': 'Trakt My Lists'}, '[B]TRAKT: [/B]Lists', iconImage='traktmylists.png')
        self._add_dir({'mode': 'trakt.get_trakt_liked_lists', 'foldername': 'My Trakt Liked Lists', 'list_name': 'Trakt My Liked Lists'}, '[B]TRAKT: [/B]Liked Lists', iconImage='traktlikedlists.png')
        self._add_dir({'mode': 'navigator.trakt_recommendations', 'foldername': 'My Trakt Recommended Lists', 'list_name': 'Trakt My Recommended Lists'}, '[B]TRAKT: [/B]Recommended Lists', iconImage='traktrecommendations.png')
        self._add_dir({'mode': 'trakt.get_trakt_my_calendar', 'foldername': 'TV Show Calendar', 'list_name': 'TV Show Calendar'}, '[B]TRAKT: [/B]TV Show Calendar', iconImage='traktcalendar.png')
        self._add_dir({'mode': 'navigator.trakt_widgets', 'foldername': 'Trakt Widgets', 'list_name': 'Trakt Widgets'}, '[B]TRAKT: [/B]Widgets', iconImage='traktmylists.png')
        self._add_dir({'mode': 'trakt.get_trakt_trending_popular_lists', 'list_type': 'trending', 'foldername': 'Trakt Trending User Lists', 'list_name': 'Trending User Lists'}, '[B]TRAKT: [/B]Trending User Lists', iconImage='traktmylists.png')
        self._add_dir({'mode': 'trakt.get_trakt_trending_popular_lists', 'list_type': 'popular', 'foldername': 'Trakt Most Popular User Lists', 'list_name': 'Trakt Most Popular User Lists'}, '[B]TRAKT: [/B]Most Popular User Lists', iconImage='traktmylists.png')
        self._add_dir({'mode': 'trakt.search_trakt_lists', 'foldername': 'Search Trakt Lists', 'list_name': 'Trakt Search Lists'}, '[B]TRAKT: [/B]Search User Lists', iconImage='search_trakt_lists.png')
        self._end_directory()

    def trakt_collection(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'trakt_collection', 'foldername': 'My Trakt Movie Collection', 'list_name': 'Movies Trakt Collection'}, '[B]COLLECTION: [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'trakt_collection', 'foldername': 'My Trakt TV Show Collection', 'list_name': 'TV Shows Trakt Collection'}, '[B]COLLECTION: [/B]TV Shows', iconImage='tv.png')
        self._end_directory()

    def trakt_watchlist(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'trakt_watchlist', 'foldername': 'My Trakt Movie Watchlist', 'list_name': 'Movies Trakt Watchlist'}, '[B]WATCHLIST: [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'trakt_watchlist', 'foldername': 'My Trakt TV Show Watchlist', 'list_name': 'TV Shows Trakt Watchlist'}, '[B]WATCHLIST: [/B]TV Shows', iconImage='tv.png')
        self._end_directory()

    def trakt_recommendations(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'trakt_recommendations', 'foldername': 'My Trakt Movie Recommendations', 'list_name': 'Trakt My Movie Recommendations'}, '[B]RECOMMENDATIONS: [/B]Movies', iconImage='movies.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'trakt_recommendations', 'foldername': 'My Trakt TV Show Recommendations', 'list_name': 'Trakt My TV Show Recommendations'}, '[B]RECOMMENDATIONS: [/B]TV Shows', iconImage='tv.png')
        self._end_directory()

    def trakt_widgets(self):
        # use 'new_page' to pass the type of list to be processed when using 'trakt_collection_widgets'...
        self._add_dir({'mode': 'build_movie_list', 'action': 'trakt_collection_widgets', 'new_page': 'recent', 'foldername': 'Trakt Collection Recently Added Movies', 'list_name': 'Trakt Collection Recently Added Movies'}, '[B]TRAKT WIDGETS: [/B]Collection: Recently Added Movies', iconImage='trakt.png')
        self._add_dir({'mode': 'build_movie_list', 'action': 'trakt_collection_widgets', 'new_page': 'random', 'foldername': 'Trakt Collection Random Movies', 'list_name': 'Trakt Collection Random Movies'}, '[B]TRAKT WIDGETS: [/B]Collection: Random Movies', iconImage='trakt.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'trakt_collection_widgets', 'new_page': 'recent', 'foldername': 'Trakt Collection Recently Added TV Shows', 'list_name': 'Trakt Collection Recently Added TV Shows'}, '[B]TRAKT WIDGETS: [/B]Collection: Recently Added TV Shows', iconImage='trakt.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'trakt_collection_widgets', 'new_page': 'random', 'foldername': 'Trakt Collection Random TV Shows', 'list_name': 'Trakt Collection Random TV Shows'}, '[B]TRAKT WIDGETS: [/B]Collection: Random TV Shows', iconImage='trakt.png')
        self._add_dir({'mode': 'trakt.get_trakt_my_calendar', 'recently_aired': 'true', 'foldername': 'Trakt Collection Recently Aired Episodes', 'list_name': 'Trakt Collection Recently Aired Episodes'}, '[B]TRAKT WIDGETS: [/B]Collection: Recently Aired Episodes', iconImage='trakt.png')
        self._end_directory()

    def search(self):
        self._add_dir({'mode': 'build_movie_list', 'action': 'tmdb_movies_search', 'query': 'NA', 'foldername': 'Movie Search', 'list_name': 'Search Movies'}, '[B]SEARCH : [/B]Movies', iconImage='search_movie.png')
        self._add_dir({'mode': 'build_tvshow_list', 'action': 'tmdb_tv_search', 'query': 'NA', 'foldername': 'TV Show Search', 'list_name': 'Search TV Shows'}, '[B]SEARCH : [/B]TV Shows', iconImage='search_tv.png')
        self._add_dir({'mode': 'people_search.search', 'foldername': 'People Search', 'list_name': 'Search People'}, '[B]SEARCH : [/B]People', iconImage='genre_comedy.png')
        self._add_dir({'mode': 'search_history', 'action': 'movie', 'foldername': 'Movie Search', 'list_name': 'Search History Movies'}, '[B]HISTORY : [/B]Movie Search', iconImage='search.png')
        self._add_dir({'mode': 'search_history', 'action': 'tvshow', 'foldername': 'TV Show Search', 'list_name': 'Search History TV Shows'}, '[B]HISTORY : [/B]TV Show Search', iconImage='search.png')
        self._add_dir({'mode': 'search_history', 'action': 'people', 'foldername': 'People Search', 'list_name': 'Search History People'}, '[B]HISTORY : [/B]People Search', iconImage='search.png')
        self._end_directory()

    def tools(self):
        display_time = '' if settings.subscription_update() == False else '[COLOR=grey]| Next Update: %s[/COLOR]' % str(__addon__.getSetting('service_time'))
        self._add_dir({'mode': 'navigator.changelogs', 'foldername': 'Changelogs & Log Viewer', 'list_name': 'Tools Changelogs & Log Viewer'}, '[B]TOOLS : [/B]Changelogs & Log Viewer', iconImage='settings2.png')
        self._add_dir({'mode': 'navigator.tips', 'foldername': 'Tips for Fen Use', 'list_name': 'Tips for Fen Use'}, '[B]TOOLS : [/B]Tips for Fen Use', iconImage='settings2.png')
        self._add_dir({'mode': 'navigator.set_view_modes', 'foldername': 'Set Views', 'list_name': 'Tools Set Views'}, '[B]TOOLS : [/B]Set Views', iconImage='settings2.png')
        self._add_dir({'mode': 'navigator.backup_restore', 'foldername': 'Backup/Restore Fen User Data', 'list_name': 'Tools Backup/Restore Fen User Data'}, '[B]TOOLS : [/B]Backup/Restore Fen User Data', iconImage='settings2.png')
        self._add_dir({'mode': 'navigator.clear_info', 'foldername': 'Clear Databases and Clean Settings Files', 'list_name': 'Tools Clear Databases and Clean Settings Files'}, '[B]TOOLS : [/B]Clear Databases and Clean Settings Files', iconImage='settings2.png')
        self._add_dir({'mode': 'navigator.external_scrapers', 'foldername': 'External Scrapers Manager', 'list_name': 'Tools External Scrapers Manager'}, '[B]TOOLS : [/B]External Scrapers Manager', iconImage='settings2.png')
        self._add_dir({'mode': 'navigator.shortcut_folders', 'foldername': 'Shortcut Folders Manager', 'list_name': 'Tools Shortcut Folders Manager'}, '[B]TOOLS : [/B]Shortcut Folders Manager', iconImage='settings2.png')
        self._add_dir({'mode': 'navigator.next_episodes', 'foldername': 'Next Episode Manager', 'list_name': 'Tools Next Episode Manager'}, '[B]TOOLS : [/B]Next Episode Manager', iconImage='settings2.png')
        self._add_dir({'mode': 'update_subscriptions', 'foldername': 'Update Subscriptions', 'list_name': 'Tools Update Subscriptions'}, '[B]TOOLS : [/B]Update Subscriptions %s' % display_time, iconImage='settings2.png')
        if settings.watched_indicators() == 1: self._add_dir({'mode': 'trakt_sync_watched_to_fen', 'refresh': True, 'foldername': 'ReSync Fen Watched to Trakt Watched', 'list_name': '[B]TOOLS : [/B]ReSync Fen Watched to Trakt Watched'}, '[B]TOOLS : [/B]ReSync Fen Watched to Trakt Watched', iconImage='settings2.png')
        self._add_dir({'mode': 'navigator.debrid_authorize', 'foldername': '(Re)Authorize Debrid Services', 'list_name': 'Authorize Debrid Services'}, '[B]DEBRID : [/B](Re)Authorize Debrid Services', iconImage='settings2.png')
        self._add_dir({'mode': 'trakt_authenticate', 'foldername': '(Re)Authenticate Trakt', 'list_name': 'Tools (Re)Authenticate Trakt'}, '[B]TRAKT : [/B](Re)Authenticate Trakt', iconImage='settings2.png')
        self._end_directory()

    def settings(self):
        self._add_dir({'mode': 'open_settings', 'query': '0.0', 'foldername': 'General', 'list_name': 'Settings General'}, '[B]SETTINGS : [/B]General', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '1.0', 'foldername': 'Accounts', 'list_name': 'Settings Accounts'}, '[B]SETTINGS : [/B]Accounts', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '2.0', 'foldername': 'Next Episodes', 'list_name': 'Settings Next Episodes'}, '[B]SETTINGS : [/B]Next Episodes', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '3.0', 'foldername': 'Trakt', 'list_name': 'Trakt'}, '[B]SETTINGS : [/B]Trakt', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '4.0', 'foldername': 'Internal Scrapers', 'list_name': 'Settings Internal Scrapers'}, '[B]SETTINGS : [/B]Internal Scrapers', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '5.0', 'foldername': 'External Scrapers', 'list_name': 'Settings External Scrapers'}, '[B]SETTINGS : [/B]External Scrapers', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '6.0', 'foldername': 'Results', 'list_name': 'Settings Results'}, '[B]SETTINGS : [/B]Results', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '7.0', 'foldername': 'Playback', 'list_name': 'Settings Playback'}, '[B]SETTINGS : [/B]Playback', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '8.0', 'foldername': 'Subscriptions', 'list_name': 'Settings Subscriptions'}, '[B]SETTINGS : [/B]Subscriptions', iconImage='settings.png')
        self._add_dir({'mode': 'open_settings', 'query': '9.0', 'foldername': 'Downloads', 'list_name': 'Settings Downloads'}, '[B]SETTINGS : [/B]Downloads', iconImage='settings.png')
        self._add_dir({'mode': 'external_settings', 'ext_addon': 'script.module.openscrapers', 'foldername': 'OpenScrapers Settings', 'list_name': 'Settings OpenScrapers Settings'}, '[B]EXTERNAL (SCRAPER) : [/B]OpenScrapers Settings', iconImage='settings.png')
        self._add_dir({'mode': 'external_settings', 'ext_addon': 'script.module.tikimeta', 'foldername': 'Tiki Meta Settings', 'list_name': 'Settings Tiki Meta Settings'}, '[B]EXTERNAL (META) : [/B]Tiki Meta Settings', iconImage='settings.png')
        self._add_dir({'mode': 'resolveurl_settings', 'foldername': 'ResolveURL Settings', 'list_name': 'Settings ResolveURL Settings'}, '[B]EXTERNAL (RESOLVEURL) : [/B]ResolveURL Settings', iconImage='settings.png')
        self._end_directory()

    def backup_restore(self):
        self._add_dir({'mode': 'backup_settings', 'foldername': 'Backup Fen User Data', 'list_name': 'Tools Backup Fen User Data'}, '[B]TOOLS : [/B]Backup Fen User Data', iconImage='backup_export.png')
        self._add_dir({'mode': 'restore_settings', 'foldername': 'Restore Fen User Data', 'list_name': 'Tools Restore Fen User Data'}, '[B]TOOLS : [/B]Restore Fen User Data', iconImage='backup_import.png')
        self._end_directory()

    def clear_info(self):
        clear_all_amble = '[B][COLOR=grey] (Excludes Favourites, Subscriptions & Search History)[/COLOR][/B]'
        self._add_dir({'mode': 'clean_settings', 'foldername': 'Clean Settings Files', 'list_name': 'Clean Settings Files'}, '[B]CLEAN : [/B]Clean Settings Files', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_all_cache', 'foldername': 'Clear All Cache', 'list_name': 'Tools Clear All Cache'}, '[B]CLEAR ALL CACHE[/B] [I]%s[/I]' % clear_all_amble, iconImage='settings2.png')
        self._add_dir({'mode': 'clear_favourites', 'foldername': 'Clear Fen Favourites', 'list_name': 'Tools Clear Fen Favourites'}, '[B]CACHE : [/B]Clear Fen Favourites', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_subscriptions', 'foldername': 'Clear Fen Subscriptions', 'list_name': 'Tools Clear Fen Subscriptions'}, '[B]CACHE : [/B]Clear Fen Subscriptions', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_search_history', 'foldername': 'Clear Search History', 'list_name': 'Tools Clear Search History'}, '[B]CACHE : [/B]Clear Search History', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'meta', 'foldername': 'Clear Meta Cache', 'list_name': 'Tools Clear Meta Cache'}, '[B]CACHE : [/B]Clear Meta Cache', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'list', 'foldername': 'Clear List Cache', 'list_name': 'Tools Clear List Cache'}, '[B]CACHE : [/B]Clear List Cache', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'trakt', 'foldername': 'Clear Trakt Cache', 'list_name': 'Tools Clear Trakt Cache'}, '[B]CACHE : [/B]Clear Trakt Cache', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'pages', 'foldername': 'Clear Browsed Pages Cache', 'list_name': 'Tools Clear Browsed Pages Cache'}, '[B]CACHE : [/B]Clear Browsed Pages Cache', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'internal_scrapers', 'foldername': 'Clear Internal Scrapers Cache', 'list_name': 'Tools Clear Internal Scrapers Cache'}, '[B]CACHE : [/B]Clear Internal Scrapers Cache', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'external_scrapers', 'foldername': 'Clear External Scrapers Cache', 'list_name': 'Tools Clear External Scrapers Cache'}, '[B]CACHE : [/B]Clear External Scrapers Cache', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'rd_cloud', 'foldername': 'Clear Real Debrid Cache', 'list_name': 'Tools Clear Real Debrid Cache'}, '[B]CACHE : [/B]Clear Real Debrid Cache', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'pm_cloud', 'foldername': 'Clear Premiumize Cache', 'list_name': 'Tools Clear Premiumize Cache'}, '[B]CACHE : [/B]Clear Premiumize Cache', iconImage='settings2.png')
        self._add_dir({'mode': 'clear_cache', 'cache': 'ad_cloud', 'foldername': 'Clear Cache', 'list_name': 'Tools Clear All Debrid Cache'}, '[B]CACHE : [/B]Clear All Debrid Cache', iconImage='settings2.png')
        self._end_directory()

    def next_episodes(self):
        self._add_dir({'mode': 'build_next_episode_manager', 'action': 'manage_in_progress', 'foldername': 'Manage In Progress Shows', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage In Progress Shows', iconImage='settings.png')
        if settings.watched_indicators() == 0: self._add_dir({'mode': 'build_next_episode_manager', 'action': 'manage_unwatched', 'foldername': 'Manage Unwatched Shows', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Unwatched Shows', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_options_choice', 'setting': 'Sort Type', 'foldername': 'Manage Sort Type', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Sort Type', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_options_choice', 'setting': 'Sort Order', 'foldername': 'Manage Sort Order', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Sort Order', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_options_choice', 'setting': 'Include Unaired', 'foldername': 'Manage Unaired Episodes', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Unaired Episodes', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_options_choice', 'setting': 'Include Trakt or Fen Unwatched', 'foldername': 'Include Include Unwatched TV Shows', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Include Unwatched TV Shows', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_options_choice', 'setting': 'Cache To Disk', 'foldername': 'Manage Cache To Disk', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Cache To Disk', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_options_choice', 'setting': 'Include Airdate in Title', 'foldername': 'Include Airdate in title', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Include Airdate in title', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_options_choice', 'setting': 'Airdate Format', 'foldername': 'Manage Airdate Format', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Airdate Format', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_color_choice', 'setting': 'Airdate', 'foldername': 'Manage Airdate Color Highlight', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Airdate Color Highlight', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_color_choice', 'setting': 'Unaired', 'foldername': 'Manage Unaired Color Highlight', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Unaired Color Highlight', iconImage='settings.png')
        self._add_dir({'mode': 'next_episode_color_choice', 'setting': 'Unwatched', 'foldername': 'Manage Unwatched Color Highlight', 'exclude_external': 'true'}, '[B]NEXT EPISODE : [/B]Manage Unwatched Color Highlight', iconImage='settings.png')
        self._end_directory()

    def debrid_authorize(self):
        self._add_dir({'mode': 'real_debrid.authenticate', 'foldername': '(Re)Authorize Real-Debrid', 'list_name': 'Authorize Real-Debrid'}, '[B]REAL-DEBRID : [/B](Re)Authorize Real-Debrid', iconImage='realdebrid.png')
        self._add_dir({'mode': 'premiumize.authenticate', 'foldername': '(Re)Authorize Premiumize', 'list_name': 'Authorize Premiumize'}, '[B]PREMIUMIZE : [/B](Re)Authorize Premiumize', iconImage='premiumize.png')
        self._add_dir({'mode': 'alldebrid.authenticate', 'foldername': '(Re)Authorize All Debrid', 'list_name': 'Authorize All Debrid'}, '[B]ALL DEBRID : [/B](Re)Authorize All Debrid', iconImage='alldebrid.png')
        self._end_directory()

    def external_scrapers(self):
        icon = xbmcaddon.Addon(id='script.module.openscrapers').getAddonInfo('icon')
        fail_color = 'crimson'
        all_color = 'mediumvioletred'
        debrid_color = __addon__.getSetting('prem.identify')
        torrent_color = __addon__.getSetting('torrent.identify')
        self._add_dir({'mode': 'external_scrapers_disable', 'foldername': 'Disable Failing External Scrapers', 'list_name': 'Tools Disable Failing External Scrapers'}, '[COLOR %s][B]FAILURES : [/B][/COLOR][I]Disable Failing External Scrapers[/I]' % fail_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_reset_stats', 'foldername': 'Reset Failing External Scraper Stats', 'list_name': 'Tools Reset Failing External Scraper Stats'}, '[COLOR %s][B]FAILURES : [/B][/COLOR][I]Reset Failing External Scraper Stats[/I]' % fail_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_toggle_all', 'folder': 'all_eng', 'setting': 'true', 'foldername': 'Enable All Scrapers', 'list_name': 'Tools Enable All Scrapers'}, '[COLOR %s][B]ALL SCRAPERS : [/B][/COLOR][I]Enable All Scrapers[/I]' % all_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_toggle_all', 'folder': 'all_eng', 'setting': 'false', 'foldername': 'Disable All Scrapers', 'list_name': 'Tools Disable All Scrapers'}, '[COLOR %s][B]ALL SCRAPERS : [/B][/COLOR][I]Disable All Scrapers[/I]' % all_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_enable_disable_specific_all', 'folder': 'all_eng', 'foldername': 'Enable/Disable Specific Scrapers', 'list_name': 'Tools Enable/Disable Specific Scrapers'}, '[COLOR %s][B]ALL SCRAPERS : [/B][/COLOR][I]Enable/Disable Specific Scrapers[/I]' % all_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_toggle_all', 'folder': 'en_DebridOnly', 'setting': 'true', 'foldername': 'Enable All Debrid Scrapers', 'list_name': 'Tools Enable All Debrid Scrapers'}, '[COLOR %s][B]DEBRID SCRAPERS : [/B][/COLOR][I]Enable All Debrid Scrapers[/I]' % debrid_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_toggle_all', 'folder': 'en_DebridOnly', 'setting': 'false', 'foldername': 'Disable All Debrid Scrapers', 'list_name': 'Tools Disable All Debrid Scrapers'}, '[COLOR %s][B]DEBRID SCRAPERS : [/B][/COLOR][I]Disable All Debrid Scrapers[/I]' % debrid_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_enable_disable_specific_all', 'folder': 'en_DebridOnly', 'foldername': 'Enable/Disable Specific Debrid Scrapers', 'list_name': 'Tools Enable/Disable Specific Debrid Scrapers'}, '[COLOR %s][B]DEBRID SCRAPERS : [/B][/COLOR][I]Enable/Disable Specific Debrid Scrapers[/I]' % debrid_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_toggle_all', 'folder': 'en_Torrent', 'setting': 'true', 'foldername': 'Enable All Torrent Scrapers', 'list_name': 'Tools Enable All Torrent Scrapers'}, '[COLOR %s][B]TORRENT SCRAPERS : [/B][/COLOR][I]Enable All Torrent Scrapers[/I]' % torrent_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_toggle_all', 'folder': 'en_Torrent', 'setting': 'false', 'foldername': 'Disable All Torrent Scrapers', 'list_name': 'Tools Disable All Torrent Scrapers'}, '[COLOR %s][B]TORRENT SCRAPERS : [/B][/COLOR][I]Disable All Torrent Scrapers[/I]' % torrent_color, iconImage=icon)
        self._add_dir({'mode': 'external_scrapers_enable_disable_specific_all', 'folder': 'en_Torrent', 'foldername': 'Enable/Disable Specific Torrent Scrapers', 'list_name': 'Tools Enable/Disable Specific Torrent Scrapers'}, '[COLOR %s][B]TORRENT SCRAPERS : [/B][/COLOR][I]Enable/Disable Specific Torrent Scrapers[/I]' % torrent_color, iconImage=icon)
        self._end_directory()

    def set_view_modes(self):
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.main', 'title': 'Set Main List View', 'view_type': 'addons', 'exclude_external': 'true'},'[B]SET VIEW : [/B]Main List', iconImage='settings.png')
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.movies', 'title': 'Set Movies View', 'view_type': 'movies', 'exclude_external': 'true'},'[B]SET VIEW : [/B]Movies', iconImage='settings.png')
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.tvshows', 'title': 'Set TV Show View', 'view_type': 'tvshows', 'exclude_external': 'true'},'[B]SET VIEW : [/B]TV Shows', iconImage='settings.png')
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.seasons', 'title': 'Set Seasons View', 'view_type': 'seasons', 'exclude_external': 'true'},'[B]SET VIEW : [/B]Seasons', iconImage='settings.png')
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.episodes', 'title': 'Set Episodes View', 'view_type': 'episodes', 'exclude_external': 'true'},'[B]SET VIEW : [/B]Episodes', iconImage='settings.png')
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.episode_lists', 'title': 'Set Episode Lists View', 'view_type': 'episodes', 'exclude_external': 'true'},'[B]SET VIEW : [/B]Episode Lists View', iconImage='settings.png')
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.trakt_list', 'title': 'Set Trakt Lists View', 'view_type': 'movies', 'exclude_external': 'true'},'[B]SET VIEW : [/B]Trakt Lists', iconImage='settings.png')
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.search_results', 'title': 'Set Search Results View', 'view_type': 'files', 'exclude_external': 'true'},'[B]SET VIEW : [/B]Search Results', iconImage='settings.png')
        self._add_dir({'mode': 'navigator.view_chooser', 'view_setting_id': 'view.premium', 'title': 'Set Premium Files View', 'view_type': 'files', 'exclude_external': 'true'},'[B]SET VIEW : [/B]Premium Files', iconImage='settings.png')
        self._end_directory()

    def changelogs(self):
        fen_version = __addon__.getAddonInfo('version')
        scrapers_version = xbmcaddon.Addon(id='script.module.openscrapers').getAddonInfo('version')
        meta_version = xbmcaddon.Addon(id='script.module.tikimeta').getAddonInfo('version')
        main_text_file, main_heading = xbmc.translatePath(os.path.join(addon_dir, "resources", "text", "changelog.txt")), 'Fen Changelog  [I](v.%s)[/I]' % fen_version
        meta_text_file, meta_heading = xbmc.translatePath(os.path.join(xbmc.translatePath(xbmcaddon.Addon(id='script.module.tikimeta').getAddonInfo('path')), "changelog.txt")), 'Tiki Meta Changelog  [I](v.%s)[/I]' % meta_version
        scrapers_text_file, scrapers_heading = xbmc.translatePath(os.path.join(xbmc.translatePath(xbmcaddon.Addon(id='script.module.openscrapers').getAddonInfo('path')), "changelog.txt")), 'OpenScrapers Changelog  [I](v.%s)[/I]' % scrapers_version
        kodi_log_location = os.path.join(xbmc.translatePath('special://logpath/'), 'kodi.log')
        self._add_dir({'mode': 'show_text', 'text_file': main_text_file, 'heading': main_heading, 'foldername': main_heading, 'list_name': 'Fen Changelog'}, '[B]CHANGELOG : [/B] %s' % main_heading.replace(' Changelog', ''), iconImage='lists.png')
        self._add_dir({'mode': 'show_text', 'text_file': meta_text_file, 'heading': meta_heading, 'foldername': meta_heading, 'list_name': 'Tiki Meta Changelog'}, '[B]CHANGELOG : [/B] %s' % meta_heading.replace(' Changelog', ''), iconImage='lists.png')
        self._add_dir({'mode': 'show_text', 'text_file': scrapers_text_file, 'heading': scrapers_heading, 'foldername': scrapers_heading, 'list_name': 'Open Scrapers Changelog'}, '[B]CHANGELOG : [/B] %s' % scrapers_heading.replace(' Changelog', ''), iconImage='lists.png')
        self._add_dir({'mode': 'show_text', 'text_file': kodi_log_location, 'heading': 'Kodi Log Viewer', 'usemono': 'True', 'foldername': 'Kodi Log Viewer', 'list_name': 'Kodi Log Viewer'}, '[B]LOG : [/B]Kodi Log Viewer', iconImage='lists.png')
        self._end_directory()

    def certifications(self):
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        if params.get('menu_type') == 'movie': from modules.nav_utils import movie_certifications as certifications
        else: from modules.nav_utils import tvshow_certifications as certifications
        mode = 'build_movie_list' if params.get('menu_type') == 'movie' else 'build_tvshow_list'
        action = 'tmdb_movies_certifications' if params.get('menu_type') == 'movie' else 'trakt_tv_certifications'
        list_name_insert = self.make_list_name(params.get('menu_type'))
        for cert in certifications:
            self._add_dir({'mode': mode, 'action': action, 'certification': cert, 'foldername': cert.upper(), 'list_name': '%ss %s Certification' % (list_name_insert, cert.upper())}, cert.upper(), iconImage='certifications.png')
        self._end_directory()

    def languages(self):
        from modules.nav_utils import languages
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        mode = 'build_movie_list' if params.get('menu_type') == 'movie' else 'build_tvshow_list'
        action = 'tmdb_movies_languages' if params.get('menu_type') == 'movie' else 'tmdb_tv_languages'
        list_name_insert = self.make_list_name(params.get('menu_type'))
        for lang in languages:
            self._add_dir({'mode': mode, 'action': action, 'language': lang[1], 'foldername': lang, 'list_name': '%ss %s Language' % (list_name_insert, lang[0])}, lang[0], iconImage='languages.png')
        self._end_directory()

    def years(self):
        from modules.nav_utils import years
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        mode = 'build_movie_list' if params.get('menu_type') == 'movie' else 'build_tvshow_list'
        action = 'tmdb_movies_year' if params.get('menu_type') == 'movie' else 'tmdb_tv_year'
        list_name_insert = self.make_list_name(params.get('menu_type'))
        for i in years():
            self._add_dir({'mode': mode, 'action': action, 'year': str(i), 'foldername': '%s - %s' % (str(i), params.get('menu_type')), 'list_name': '%ss %s Premiered' % (list_name_insert, str(i))}, str(i), iconImage='calender.png')
        self._end_directory()

    def genres(self):
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        mode = 'build_movie_list' if params.get('menu_type') == 'movie' else 'build_tvshow_list'
        action = 'tmdb_movies_genres' if params.get('menu_type') == 'movie' else 'tmdb_tv_genres'
        list_name_insert = self.make_list_name(params.get('menu_type'))
        if params.get('menu_type') == 'movie':  from modules.nav_utils import movie_genres as genre_list
        else: from modules.nav_utils import tvshow_genres as genre_list
        self._add_dir({'mode': mode, 'action': action, 'genre_list': json.dumps(genre_list), 'exclude_external': 'true', 'foldername': 'Multiselect'}, '[B]Multiselect...[/B]', iconImage='genres.png')
        for genre, value in sorted(genre_list.items()):
            self._add_dir({'mode': mode, 'action': action, 'genre_id': value[0], 'foldername': genre, 'list_name': '%ss %s Genre' % (list_name_insert, genre)}, genre, iconImage=value[1])
        self._end_directory()

    def networks(self):
        from modules.nav_utils import networks
        for item in sorted(networks, key=lambda k: k['name']):
            self._add_dir({'mode': 'build_tvshow_list', 'action': 'tmdb_tv_networks', 'network_id': item['id'], 'foldername': item['name'], 'list_name': 'TV Shows %s Network' % item['name']}, item['name'], iconImage=item['logo'])
        self._end_directory()

    def trakt_mosts(self):
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        final_mode = 'build_movie_list' if params.get('menu_type') == 'movie' else 'build_tvshow_list'
        action = 'trakt_movies_mosts' if params.get('menu_type') == 'movie' else 'trakt_tv_mosts'
        list_name_insert = self.make_list_name(params.get('menu_type'))
        trakt_mosts = {'Played': ['played', 'most__played.png'],
        'Collected': ['collected', 'most__collected.png'],
        'Watched': ['watched', 'most__watched.png']}
        for most, value in trakt_mosts.items():
            self._add_dir({'mode': 'navigator.trakt_mosts_duration', 'action': action, 'period': value[0], 'menu_type': params.get('menu_type'), 'final_mode': final_mode, 'iconImage': value[1], 'foldername': 'Most %s' % most, 'list_name': '%ss Most %s' % (list_name_insert, most)}, '[B]MOST: [/B]%s' % most, iconImage=value[1])
        self._end_directory()

    def trakt_mosts_duration(self):
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        list_name_insert = self.make_list_name(params.get('menu_type'))
        durations = [('This Week', 'weekly'), ('This Month', 'monthly'), ('This Year', 'yearly'), ('All Time', 'all')]
        for duration, urlitem in durations:
            self._add_dir({'mode': params['final_mode'], 'action': params['action'], 'period': params['period'], 'duration': urlitem, 'foldername': duration, 'list_name': '%ss Most %s %s' % (list_name_insert, params.get('period').capitalize(), duration)}, '[B]MOST %s:[/B] %s' % (params.get('period').upper(), duration), iconImage=params['iconImage'])
        self._end_directory()

    def folder_navigator(self):
        from modules.utils import clean_file_name, normalize
        from modules import fen_cache
        def make_directory(isFolder=True):
            if sources_folders and isFolder:
                cm = []
                normalized_folder_name = normalize(item)
                link_folders_add = {'mode': 'link_folders', 'service': 'FOLDER', 'folder_name': normalized_folder_name, 'action': 'add'}
                link_folders_remove = {'mode': 'link_folders', 'service': 'FOLDER', 'folder_name': normalized_folder_name, 'action': 'remove'}
                string = 'FEN_FOLDER_%s' % normalized_folder_name
                current_link = _cache.get(string)
                if current_link: ending = '[COLOR=limegreen][B][I]\n(Linked to %s)[/I][/B][/COLOR]' % current_link
                else: ending = ''
            else: ending = ''
            display = '%s%s' % (item, ending)
            url = os.path.join(folder_path, item)
            listitem = xbmcgui.ListItem(display)
            listitem.setArt({'fanart': self.fanart})
            if sources_folders and isFolder:
                cm.append(("[B]Link Movie/TV Show[/B]",'RunPlugin(%s)' % self._build_url(link_folders_add)))
                cm.append(("[B]Clear Movie/TV Show Link[/B]",'RunPlugin(%s)' % self._build_url(link_folders_remove)))
                listitem.addContextMenuItems(cm)
            return xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=isFolder)
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        _cache = fen_cache.FenCache()
        folder_path = params['folder_path']
        sources_folders = params.get('sources_folders', None)
        if sources_folders:
            from modules.utils import normalize
        try:
            dirs, files = xbmcvfs.listdir(folder_path)
            for item in dirs: make_directory()
            for item in files: make_directory(isFolder=False)
        except: pass
        xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_FILE)
        self._end_directory()
    
    def sources_folders(self):
        for source in ('folder1', 'folder2', 'folder3', 'folder4', 'folder5'):
            for db_type in ('movie', 'tvshow'):
                folder_path = settings.source_folders_directory(db_type, source)
                if not folder_path: continue
                name = '[B]%s (%sS): %s[/B]\n     [I]%s[/I]' % (source.upper(), db_type.upper(), __addon__.getSetting('%s.display_name' % source).upper(), folder_path)
                self._add_dir({'mode': 'navigator.folder_navigator','sources_folders': 'True', 'folder_path': folder_path, 'foldername': name, 'list_name': name}, name, iconImage='most__collected.png')
        self._end_directory()

    def tips(self):
        tips_location = xbmc.translatePath(os.path.join(addon_dir, "resources", "text", "tips"))
        files = sorted(xbmcvfs.listdir(tips_location)[1])
        flags = ['HELP!!!', 'NEW!!!', 'SPOTLIGHT!!!']
        for tip in files:
            try:
                add_sort_top = False
                tip_name = tip.replace('.txt', '')[4:]
                if any(i in tip_name for i in flags):
                    for string in flags:
                        if string in tip_name:
                            add_sort_top = True
                            break
                    tip_name_replace = (flags[0], '[COLOR orange][B]HELP!!![/B][/COLOR]') if string == flags[0] else (flags[1], '[COLOR crimson][B]NEW!!![/B][/COLOR]') if string == flags[1] else (flags[2], '[COLOR chartreuse][B]SPOTLIGHT!!![/B][/COLOR]')
                    tip_name = tip_name.replace(tip_name_replace[0], tip_name_replace[1])
                dir_params = {'mode': 'show_text', 'text_file': xbmc.translatePath(os.path.join(tips_location, tip)), 'exclude_external': 'true', 'heading': 'Fen Tips', 'foldername': '[B]Fen Tips %s[/B]' % tip_name, 'list_name': 'Fen Tips [B]%s[/B]' % tip_name}
                if add_sort_top: dir_params['SpecialSort'] = 'top'
                self._add_dir(dir_params, '[B]TIPS : [/B] %s' % tip_name, iconImage='faq8.png')
            except: pass
        xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_FILE)
        self._end_directory()

    def because_you_watched(self):
        from modules.indicators_bookmarks import get_watched_info_movie, get_watched_info_tv
        def _convert_fen_watched_episodes_info():
            final_list = []
            used_names = []
            _watched, _trakt = get_watched_info_tv()
            if not _trakt:
                for item in _watched:
                    name = item[3]
                    if not name in used_names:
                        if item[3] == name:
                            tv_show = [i for i in _watched if i[3] == name]
                            season = max(tv_show)[1]
                            episode = max(tv_show)[2]
                            final_item = (tv_show[0][0], 'foo', [(season, episode),], tv_show[0][3], tv_show[0][4])
                            final_list.append(final_item)
                            used_names.append(name)
                _watched = final_list
            return _watched, _trakt
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        db_type = params['menu_type']
        func = get_watched_info_movie if db_type == 'movie' else _convert_fen_watched_episodes_info
        key_index = 2 if db_type == 'movie' else 4
        name_index = 1 if db_type == 'movie' else 3
        tmdb_index = 0
        mode = 'build_movie_list' if db_type == 'movie' else 'build_tvshow_list'
        action = 'tmdb_movies_recommendations' if db_type == 'movie' else 'tmdb_tv_recommendations'
        recently_watched = func()[0]
        recently_watched = sorted(recently_watched, key=lambda k: k[key_index], reverse=True)
        for item in recently_watched:
            if db_type == 'movie': name = '[I]Because You Watched...[/I]  [B]%s[/B]' % item[name_index]
            else:
                season, episode = item[2][-1]
                name = '[I]Because You Watched...[/I]  [B]%s - %sx%s[/B]' % (item[name_index], season, episode)
            tmdb_id = item[tmdb_index]
            self._add_dir({'mode': mode, 'action': action, 'sim_recom_name': name, 'sim_recom_tmdb': tmdb_id, 'sim_recom_imdb': None, 'foldername': name, 'list_name': name, 'exclude_external': 'true'}, name, iconImage='because_you_watched.png')
        self._end_directory()

    def view_chooser(self):
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        self._add_dir({'mode': 'navigator.set_views', 'view_setting_id': params.get('view_setting_id'), 'title': params.get('title'), 'view_type': params.get('view_type'), 'exclude_external': 'true'}, 'Set view and then click here', iconImage='settings.png')
        xbmcplugin.setContent(__handle__, params.get('view_type'))
        xbmcplugin.endOfDirectory(__handle__)
        self._setView(params.get('view_setting_id'), params.get('view_type'))

    def set_views(self):
        from modules.nav_utils import notification
        VIEWS_DB = os.path.join(profile_dir, "views.db")
        settings.check_database(VIEWS_DB)
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        view_type = params.get('view_setting_id')
        view_id = str(xbmcgui.Window(xbmcgui.getCurrentWindowId()).getFocusId())
        dbcon = database.connect(VIEWS_DB)
        dbcon.execute("DELETE FROM views WHERE view_type = '%s'" % (str(view_type)))
        dbcon.execute("INSERT INTO views VALUES (?, ?)", (str(view_type), str(view_id)))
        dbcon.commit()
        notification("%s set to %s" % (params.get('title')[3:], xbmc.getInfoLabel('Container.Viewmode').upper()), time=2000)

    def make_list_name(self, menu_type):
        return menu_type.replace('tvshow', 'TV Show').replace('movie', 'Movie')
    
    def shortcut_folders(self):
        def _make_new_item():
            display_name = '[I]Make New Shortcut Folder...[/I]'
            url_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_shortcut_folder'}
            url = self._build_url(url_params)
            listitem = xbmcgui.ListItem(display_name)
            listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon})
            xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=True)
        dbcon = database.connect(NAVIGATOR_DB)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT list_name, list_contents FROM navigator WHERE list_type = ?", ('shortcut_folder',))
        folders = dbcur.fetchall()
        try: folders = sorted([(str(i[0]), i[1]) for i in folders], key=lambda s: s[0].lower())
        except: folders = []
        icon = os.path.join(self.icon_directory, 'furk.png')
        _make_new_item()
        for i in folders:
            try:
                cm = []
                name = i[0]
                display_name = '[B]SHORTCUT FOLDER : [/B] %s ' % i[0]
                contents = json.loads(i[1])
                url_params = {"iconImage": "furk.png", 
                            "mode": "navigator.build_shortcut_folder_lists",
                            "action": name,
                            "name": name, 
                            "foldername": name,
                            "shortcut_folder": 'True',
                            "external_list_item": 'True',
                            "shortcut_folder": 'True',
                            "contents": contents}
                remove_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'delete_shortcut_folder', 'list_name': name}
                remove_all_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'remove_all_shortcut_folders'}
                url = self._build_url(url_params)
                listitem = xbmcgui.ListItem(display_name)
                listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon})
                cm.append(("[B]Delete Shortcut Folder[/B]",'XBMC.RunPlugin(%s)'% self._build_url(remove_params)))
                cm.append(("[B]Delete All Shortcut Folders[/B]",'XBMC.RunPlugin(%s)'% self._build_url(remove_all_params)))
                listitem.addContextMenuItems(cm)
                xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=True)
            except: pass
        self._end_directory()

    def adjust_main_lists(self, params=None):
        from modules.nav_utils import notification
        def db_execute():
            dbcon = database.connect(NAVIGATOR_DB)
            dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, 'edited'))
            dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'edited', json.dumps(li)))
            dbcon.commit()
            window.setProperty('fen_%s_edited' % list_name, json.dumps(li))
        def menu_select(heading, position_list=False):
            for item in choice_items:
                line = 'Place [B]%s[/B] below [B]%s[/B]' % (menu_name, item['name']) if position_list else ''
                icon = item.get('iconImage') if item.get('network_id', '') != '' else os.path.join(self.icon_directory, item.get('iconImage'))
                listitem = xbmcgui.ListItem(item['name'], line)
                listitem.setArt({'icon': icon})
                choice_list.append(listitem)
            if position_list:
                listitemTop = xbmcgui.ListItem('Top Position', 'Place [B]%s[/B] at Top of List' % menu_name)
                listitemTop.setArt({'icon': os.path.join(self.icon_directory, 'top.png')})
                choice_list.insert(0, listitemTop)
            return dialog.select(heading, choice_list, useDetails=True)
        def select_from_main_menus(current_list=[], item_list=[]):
            include_list = DefaultMenus().DefaultMenuItems()
            menus = DefaultMenus().RootList()
            menus.insert(0, {'name': 'Root', 'iconImage': 'fen.png', 'foldername': 'Root', 'mode': 'navigator.main', 'action': 'RootList'})
            include_list = [i for i in include_list if i != current_list]
            menus = [i for i in menus if i.get('action', None) in include_list and not i.get('name') == item_list]
            return menus
        def get_external_name():
            dialog = xbmcgui.Dialog()
            name_append_list = [('RootList', ''), ('MovieList', 'Movies '), ('TVShowList', 'TV Shows ')]
            orig_name = params.get('list_name', None)
            try: name = '%s%s' % ([i[1] for i in name_append_list if i[0] == orig_name][0], menu_item.get('name'))
            except: name = orig_name
            name = dialog.input('Choose Display Name', type=xbmcgui.INPUT_ALPHANUM, defaultt=name)
            return name
        def db_execute_shortcut_folder(action='add'):
            dbcon = database.connect(NAVIGATOR_DB)
            dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (menu_name, 'shortcut_folder'))
            if action == 'add': dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (menu_name, 'shortcut_folder', json.dumps(li)))
            dbcon.commit()
            window.setProperty('fen_%s_shortcut_folder' % menu_name, json.dumps(li))
        def db_execute_add_to_shortcut_folder():
            dbcon = database.connect(NAVIGATOR_DB)
            dbcur.execute("SELECT list_contents FROM navigator WHERE list_name = ?", (shortcut_folder_name,))
            dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (menu_name, 'shortcut_folder'))
            if action == 'add': dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (menu_name, 'shortcut_folder', json.dumps(li)))
            dbcon.commit()
            window.setProperty('fen_%s_shortcut_folder' % list_name, json.dumps(li))
        def select_shortcut_folders(make_new=False):
            dbcon = database.connect(NAVIGATOR_DB)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT list_name, list_contents FROM navigator WHERE list_type = ?", ('shortcut_folder',))
            folders = dbcur.fetchall()
            try: folders = sorted([(str(i[0]), i[1]) for i in folders], key=lambda s: s[0].lower())
            except: folders = []
            selection = 0
            if len(folders) > 0:
                folder_choice_list = []
                folder_names = ['[B]%s[/B]' % i[0] for i in folders]
                for item in folder_names:
                    icon = os.path.join(self.icon_directory, 'furk.png')
                    listitem = xbmcgui.ListItem(item, 'Existing Shortcut Folder')
                    listitem.setArt({'icon': icon})
                    folder_choice_list.append(listitem)
                if make_new:
                    make_new_item = xbmcgui.ListItem('[B]MAKE NEW FOLDER[/B]', 'Make New Shortcut Folder')
                    make_new_item.setArt({'icon': os.path.join(self.icon_directory, 'new.png')})
                    folder_choice_list.insert(0, make_new_item)
                selection = dialog.select('FEN - Shortcut Folder Choice', folder_choice_list, useDetails=True)
            return folders, selection
        window.clearProperty('fen_%s_default')
        window.clearProperty('fen_%s_edited')
        dialog = xbmcgui.Dialog()
        if not params: params = dict(parse_qsl(sys.argv[2].replace('?','')))
        menu_name = params.get('menu_name', '')
        list_name = params.get('list_name', '')
        li = None
        method = params.get('method')
        choice_list = []
        if not method in ('display_edit_menu', 'add_external', 'add_trakt_external', 'add_sim_recom_external', 'restore'):
            try:
                current_position = int(params.get('position', '0'))
                default_list, edited_list = self._db_lists(list_name)
                def_file = default_list if not edited_list else edited_list
                li, def_li = def_file, default_list
                choice_items = [i for i in def_li if i not in li]
            except: pass
        try:
            if method == 'display_edit_menu':
                from ast import literal_eval
                from modules.utils import selection_dialog
                default_menu = params.get('default_menu')
                edited_list = None if params.get('edited_list') == 'None' else params.get('edited_list')
                list_name = params.get('list_name') if 'list_name' in params else self.list_name
                menu_name = params.get('menu_name')
                position = params.get('position')
                external_list_item = literal_eval(params.get('external_list_item', 'False'))
                list_is_full = literal_eval(params.get('list_is_full', 'False'))
                list_slug = params.get('list_slug', '')
                menu_item = json.loads(params.get('menu_item'))
                shortcut_folder = literal_eval(menu_item.get('shortcut_folder', 'False'))
                menu_item['list_name'] = list_name
                list_heading = 'Root' if list_name == 'RootList' else 'Movies' if list_name == 'MovieList' else 'TV Shows'
                string = "Edit [B]'%s'[/B] Menu..." % list_heading
                listing = []
                if len(default_menu) != 1:
                    listing += [("Move [B]'%s'[/B] to a different position in the list" % menu_name, 'move')]
                    listing += [("Remove [B]'%s'[/B] from the list" % menu_name, 'remove')]
                if not shortcut_folder:
                    listing += [("Add [B]'%s'[/B] to a different Menu list" % menu_name, 'add_external')]
                    listing += [("Add [B]'%s'[/B] to a [B]Shortcut Folder[/B]" % menu_name, 'shortcut_folder_add')]
                if list_name in ('RootList', 'MovieList', 'TVShowList'): listing += [("Add a Trakt list to [B]'%s'[/B] Menu" % list_heading, 'add_trakt')]
                if not list_is_full: listing += [("Re-add a removed item from [B]'%s'[/B] Menu" % list_heading, 'add_original')]
                listing += [("Restore [B]'%s'[/B] Menu to default" % list_heading, 'restore')]
                listing += [("Check if [B]'%s'[/B] Menu has New Menu items" % list_heading, 'check_update')]
                if not list_slug and not external_list_item: listing += [("Reload [B]'%s'[/B]" % menu_name, 'reload')]
                if list_name in ('RootList', 'MovieList', 'TVShowList'): listing += [("Add [B]Shortcut Folder[/B]", 'shortcut_folder_new')]
                choice = selection_dialog([i[0] for i in listing], [i[1] for i in listing], string)
                if choice in (None, 'save_and_exit'): return
                elif choice == 'move': params = {'method': 'move', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
                elif choice == 'remove': params = {'method': 'remove', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
                elif choice == 'add_original': params = {'method': 'add_original', 'list_name': list_name, 'position': position}
                elif choice == 'restore': params = {'method': 'restore', 'list_name': list_name, 'position': position}
                elif choice == 'add_external': params = {'method': 'add_external', 'list_name': list_name, 'menu_item': json.dumps(menu_item)}
                elif choice == 'shortcut_folder_add': params = {'method': 'shortcut_folder_add', 'list_name': list_name, 'menu_item': json.dumps(menu_item)}
                elif choice == 'add_trakt': params = {'method': 'add_trakt', 'list_name': list_name, 'position': position}
                elif choice == 'reload': params = {'method': 'reload_menu_item', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
                elif choice == 'shortcut_folder_new': params = {'method': 'shortcut_folder_new', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
                elif choice == 'check_update': params = {'method': 'check_update_list', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
                return self.adjust_main_lists(params)
            elif method == 'move':
                choice_items = [i for i in li if i['name'] != menu_name]
                new_position = menu_select('Choose New Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                if new_position < 0 or new_position == current_position: return
                li.insert(new_position, li.pop(current_position))
                db_execute()
            elif method == 'remove':
                li = [x for x in li if x['name'] != menu_name]
                db_execute()
            elif method == 'add_original':
                selection = menu_select("Choose item to add to menu")
                if selection < 0: return
                selection = choice_items[selection]
                choice_list = []
                choice_items = li
                item_position = menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                if item_position < 0: return
                li.insert((item_position), selection)
                db_execute()
            elif method == 'shortcut_folder_add':
                menu_item = json.loads(params['menu_item'])
                if not menu_item: return
                name = get_external_name()
                if not name: return
                menu_item['name'] = name
                current_shortcut_folders, folder_selection = select_shortcut_folders()
                if folder_selection < 0: return
                folder_selection = current_shortcut_folders[folder_selection]
                shortcut_folder_name = folder_selection[0]
                shortcut_folder_contents = json.loads(folder_selection[1])
                choice_items = shortcut_folder_contents
                if len(choice_items) > 0: item_position = menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                else: item_position = 0
                if item_position < 0: return
                menu_item['external_list_item'] = 'True'
                shortcut_folder_contents.insert((item_position), menu_item)
                menu_name = shortcut_folder_name
                li = shortcut_folder_contents
                db_execute_shortcut_folder()
            elif method == 'add_external':
                menu_item = json.loads(params['menu_item'])
                if not menu_item: return
                name = get_external_name()
                if not name: return
                menu_item['name'] = name
                choice_items = select_from_main_menus(params.get('list_name'), name)
                selection = menu_select("Choose Menu to add %s Into.." % params.get('list_name'))
                if selection < 0: return
                add_to_menu_choice = choice_items[selection]
                list_name = add_to_menu_choice['action']
                default_list, edited_list = self._db_lists(list_name)
                def_file = default_list if not edited_list else edited_list
                li = def_file
                if menu_item in li: return
                choice_list = []
                choice_items = li
                item_position = menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                if item_position < 0: return
                menu_item['external_list_item'] = 'True'
                li.insert((item_position), menu_item)
                db_execute()
            elif method == 'add_trakt':
                from apis.trakt_api import get_trakt_list_selection
                trakt_selection = json.loads(params['trakt_selection']) if 'trakt_selection' in params else get_trakt_list_selection(list_choice='nav_edit')
                if not trakt_selection: return
                name = dialog.input('Choose Display Name', type=xbmcgui.INPUT_ALPHANUM, defaultt=trakt_selection['name'])
                if not name: return
                choice_list = []
                choice_items = li
                item_position = menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                if item_position < 0: return
                li.insert(item_position, {"iconImage": "traktmylists.png", "mode": "trakt.build_trakt_list", "name": name, "foldername": name, "user": trakt_selection['user'], "slug": trakt_selection['slug'], 'external_list_item': 'True'})
                db_execute()
            elif method == 'add_trakt_external':
                name = dialog.input('Choose Display Name', type=xbmcgui.INPUT_ALPHANUM, defaultt=params['name'])
                if not name: return
                if not li:
                    choice_items = select_from_main_menus()
                    selection = menu_select("Choose Menu to add %s  Into.." % name)
                    if selection < 0: return
                    add_to_menu_choice = choice_items[selection]
                    list_name = add_to_menu_choice['action']
                    default_list, edited_list = self._db_lists(list_name)
                    li = default_list if not edited_list else edited_list
                if name in [i['name'] for i in li]: return
                choice_list = []
                choice_items = li
                item_position = 0 if len(li) == 0 else menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                if item_position < 0: return
                li.insert(item_position, {"iconImage": "traktmylists.png", "mode": "trakt.build_trakt_list", "name": name, "foldername": name, "user": params['user'], "slug": params['slug'], 'external_list_item': 'True'})
                db_execute()
            elif method == 'add_sim_recom_external':
                name = dialog.input('Choose Display Name', type=xbmcgui.INPUT_ALPHANUM, defaultt=params['sim_recom_name'])
                if not name: return
                if not li:
                    choice_items = select_from_main_menus()
                    selection = menu_select("Choose Menu to add %s  Into.." % name)
                    if selection < 0: return
                    add_to_menu_choice = choice_items[selection]
                    list_name = add_to_menu_choice['action']
                    default_list, edited_list = self._db_lists(list_name)
                    li = default_list if not edited_list else edited_list
                if name in [i['name'] for i in li]: return
                choice_list = []
                choice_items = li
                item_position = 0 if len(li) == 0 else menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                if item_position < 0: return
                li.insert(item_position, {"iconImage": "discover.png", "mode": params['end_mode'], 'action': params['end_action'], "name": name, "sim_recom_name": name, "foldername": name, "sim_recom_tmdb": params['sim_recom_tmdb'], "sim_recom_imdb": params['sim_recom_imdb'], 'external_list_item': 'True'})
                db_execute()
            elif method == 'browse':
                heading = "Choose Removed Item to Browse Into.."
                selection = menu_select(heading)
                if selection < 0: return
                mode = choice_items[selection]['mode'] if 'mode' in choice_items[selection] else ''
                action = choice_items[selection]['action'] if 'action' in choice_items[selection] else ''
                url_mode = choice_items[selection]['url_mode'] if 'url_mode' in choice_items[selection] else ''
                menu_type = choice_items[selection]['menu_type'] if 'menu_type' in choice_items[selection] else ''
                query = choice_items[selection]['query'] if 'query' in choice_items[selection] else ''
                db_type = choice_items[selection]['db_type'] if 'db_type' in choice_items[selection] else ''
                xbmc.executebuiltin("XBMC.Container.Update(%s)" % self._build_url({'mode': mode, 'action': action, 'url_mode': url_mode,
                                                                                   'menu_type': menu_type, 'query': query, 'db_type': db_type}))
            elif method == 'reload_menu_item':
                default = eval('DefaultMenus().%s()' % list_name)
                default_item = [i for i in default if i['name'] == menu_name][0]
                li = [default_item if x['name'] == menu_name else x for x in def_file]
                list_type = 'edited' if self._db_lists(list_name)[1] else 'default'
                dbcon = database.connect(NAVIGATOR_DB)
                dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, list_type))
                dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, list_type, json.dumps(li)))
                dbcon.commit()
                window.setProperty('fen_%s_%s' % (list_name, list_type), json.dumps(li))
            elif method == 'shortcut_folder_new':
                make_new_folder = True
                current_shortcut_folders, folder_selection = select_shortcut_folders(make_new=True)
                if folder_selection < 0: return
                if folder_selection > 0:
                    make_new_folder = False
                    folder_selection = current_shortcut_folders[folder_selection-1] # -1 because we added the 'Make New' listitem
                    name = folder_selection[0]
                    contents = folder_selection[1]
                if make_new_folder:
                    name = dialog.input('Choose Folder Name', type=xbmcgui.INPUT_ALPHANUM)
                    if not name: return
                    contents = []
                if name in [i['name'] for i in li]: return
                menu_item = {"iconImage": "furk.png", 
                            "mode": "navigator.build_shortcut_folder_lists",
                            "action": name,
                            "name": name, 
                            "foldername": name,
                            "shortcut_folder": 'True',
                            "external_list_item": 'True',
                            "contents": contents}
                choice_list = []
                choice_items = li
                menu_name = name
                item_position = 0 if len(li) == 0 else menu_select('Choose Insert Position of [B]%s[/B] Folder (Insert Below Chosen Item)...' % name.upper(), position_list=True)
                if item_position < 0: return
                li.insert(item_position, menu_item)
                db_execute()
                li = []
                db_execute_shortcut_folder()
            elif method == 'check_update_list':
                dbcon = database.connect(NAVIGATOR_DB)
                dbcur = dbcon.cursor()
                new_contents = eval('DefaultMenus().%s()' % list_name)
                if default_list != new_contents:
                    new_entry = [i for i in new_contents if i not in default_list][0]
                    if not dialog.yesno("Fen", "New item [B]%s[/B] Exists." % new_entry.get('name'), "Would you like to add this to the Menu?", '', 'Yes', 'No') == 0: return
                    choice_items = def_file
                    item_position = menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                    if item_position < 0: return
                    if edited_list:
                        edited_list.insert(item_position, new_entry)
                        dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, 'edited'))
                        dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'edited', json.dumps(edited_list)))
                        window.setProperty('fen_%s_edited' % list_name, json.dumps(edited_list))
                    default_list.insert(item_position, new_entry)
                    dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, 'default'))
                    dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'default', json.dumps(default_list)))
                    window.setProperty('fen_%s_default' % list_name, json.dumps(default_list))
                    dbcon.commit()
                    dbcon.close()
                else:
                    return dialog.ok('Fen', 'No New Items for [B]%s[/B].' % list_name.upper())
            elif method == 'restore':
                confirm = dialog.yesno('Are you sure?', 'Continuing will load the default Menu.')
                if not confirm: return
                dbcon = database.connect(NAVIGATOR_DB)
                for item in ['edited', 'default']: dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, item))
                dbcon.commit()
                dbcon.execute("VACUUM")
                dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'default', json.dumps(eval('DefaultMenus().%s()' % list_name))))
                dbcon.commit()
                for item in ('edited', 'default'): window.clearProperty('fen_%s_%s' % (list_name, item))
            if not method in ('browse',):
                    notification("Process Successful", time=1500)
            if not method in ('browse', 'add_sim_recom_external'):
                    xbmc.sleep(200)
                    xbmc.executebuiltin('Container.Refresh')
        except:
            from modules.nav_utils import notification
            return notification('Error Performing Task')

    def build_main_lists(self):
        def _build(item_position, item):
            try:
                cm = []
                name = item.get('name', '')
                icon = item.get('iconImage') if item.get('network_id', '') != '' else os.path.join(self.icon_directory, item.get('iconImage'))
                url = self._build_url(item)
                cm.append(("[B]Edit Menu[/B]",'XBMC.RunPlugin(%s)' % self._build_url(
                    {'mode': 'navigator.adjust_main_lists', 'method': 'display_edit_menu', 'default_menu': self.default_menu, 'menu_item': json.dumps(item),
                    'edited_list': self.edited_list, 'list_name': self.list_name, 'menu_name': name,
                    'position': item_position, 'list_is_full': list_is_full, 'list_slug': item.get('slug', ''),
                    'external_list_item': item.get('external_list_item', 'False')})))
                if not list_is_full:
                    cm.append(("[B]Browse Removed item[/B]",'XBMC.RunPlugin(%s)' % \
                    self._build_url({'mode': 'navigator.adjust_main_lists', 'method': 'browse', 'list_name': self.list_name, 'position': item_position})))
                listitem = xbmcgui.ListItem(name)
                listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon})
                listitem.addContextMenuItems(cm)
                if use_threading: item_list.append({'list_item': (url, listitem, True), 'item_position': item_position})
                else: xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            except: return
        self.default_list, self.edited_list = self._db_lists()
        self.default_menu = self.default_list if not self.edited_list else self.edited_list
        current_items_from_default = [i for i in self.default_menu if not i.get('external_list_item', 'False') == 'True']
        list_is_full = True if len(current_items_from_default) >= len(self.default_list) else False
        cache_to_disc = False if self.list_name == 'RootList' else True
        use_threading = settings.thread_main_menus()
        if use_threading:
            from threading import Thread
            item_list = []
            threads = []
            for item_position, item in enumerate(self.default_menu): threads.append(Thread(target=_build, args=(item_position, item)))
            [i.start() for i in threads]
            [i.join() for i in threads]
            item_list.sort(key=lambda k: k['item_position'])
            xbmcplugin.addDirectoryItems(__handle__, [i['list_item'] for i in item_list])
        else:
            for item_position, item in enumerate(self.default_menu): _build(item_position, item)
        self._end_directory(cache_to_disc=cache_to_disc)

    def adjust_shortcut_folder_lists(self, params=None):
        from modules.nav_utils import notification
        def db_execute_shortcut_folder(action='add'):
            dbcon = database.connect(NAVIGATOR_DB)
            dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (menu_name, 'shortcut_folder'))
            if action == 'add': dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (menu_name, 'shortcut_folder', json.dumps(li)))
            dbcon.commit()
            window.setProperty('fen_%s_shortcut_folder' % menu_name, json.dumps(li))
        def menu_select(heading, position_list=False):
            for item in choice_items:
                line = 'Place [B]%s[/B] below [B]%s[/B]' % (name, item['name']) if position_list else ''
                icon = item.get('iconImage') if item.get('network_id', '') != '' else os.path.join(self.icon_directory, item.get('iconImage'))
                listitem = xbmcgui.ListItem(item['name'], line)
                listitem.setArt({'icon': icon})
                choice_list.append(listitem)
            if position_list:
                listitemTop = xbmcgui.ListItem('Top Position', 'Place [B]%s[/B] at Top of List' % name)
                listitemTop.setArt({'icon': os.path.join(self.icon_directory, 'top.png')})
                choice_list.insert(0, listitemTop)
            return dialog.select(heading, choice_list, useDetails=True)
        def select_shortcut_folders(select=True):
            dbcon = database.connect(NAVIGATOR_DB)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT list_name, list_contents FROM navigator WHERE list_type = ?", ('shortcut_folder',))
            folders = dbcur.fetchall()
            try: folders = sorted([(str(i[0]), i[1]) for i in folders], key=lambda s: s[0].lower())
            except: folders = []
            if not select: return folders
            selection = 0
            if len(folders) > 0:
                folder_choice_list = []
                folder_names = ['[B]%s[/B]' % i[0] for i in folders]
                for item in folder_names:
                    icon = os.path.join(self.icon_directory, 'furk.png')
                    listitem = xbmcgui.ListItem(item, 'Existing Shortcut Folder')
                    listitem.setArt({'icon': icon})
                    folder_choice_list.append(listitem)
                selection = dialog.select('FEN - Shortcut Folder Choice', folder_choice_list, useDetails=True)
            return folders, selection
        dialog = xbmcgui.Dialog()
        if not params: params = dict(parse_qsl(sys.argv[2].replace('?','')))
        menu_name = params.get('menu_name')
        list_name = params.get('list_name')
        li = None
        method = params.get('method')
        choice_list = []
        current_position = int(params.get('position', '0'))
        try:
            if method == 'display_edit_menu':
                from ast import literal_eval
                from modules.utils import selection_dialog
                position = params.get('position')
                menu_item = json.loads(params.get('menu_item'))
                contents = json.loads(params.get('contents'))
                external_list_item = literal_eval(params.get('external_list_item', 'False'))
                list_slug = params.get('list_slug', '')
                list_heading = 'Root' if list_name == 'RootList' else 'Movies' if list_name == 'MovieList' else 'TV Shows'
                string = "Edit [B]'%s'[/B] Folder..." % list_name
                listing = []
                if len(contents) != 1: listing += [("Move", 'move')]
                listing += [("Remove", 'remove')]
                listing += [("Add a Trakt list", 'add_trakt')]
                listing += [("Clear All", 'clear_all')]
                choice = selection_dialog([i[0] for i in listing], [i[1] for i in listing], string)
                if choice in (None, 'save_and_exit'): return
                elif choice == 'move': params = {'method': 'move', 'list_name': list_name, 'menu_name': menu_name, 'position': position, 'menu_item': json.dumps(menu_item), 'contents': json.dumps(contents)}
                elif choice == 'remove': params = {'method': 'remove', 'list_name': list_name, 'menu_name': menu_name, 'position': position, 'menu_item': json.dumps(menu_item), 'contents': json.dumps(contents)}
                elif choice == 'add_trakt': params = {'method': 'add_trakt', 'list_name': list_name, 'position': position, 'menu_item': json.dumps(menu_item), 'contents': json.dumps(contents)}
                elif choice == 'clear_all': params = {'method': 'clear_all', 'list_name': list_name, 'menu_name': menu_name, 'position': position, 'menu_item': json.dumps(menu_item), 'contents': json.dumps(contents)}
                return self.adjust_shortcut_folder_lists(params)
            elif method == 'move':
                menu_name = params.get('list_name')
                name = params.get('menu_name')
                li = json.loads(params.get('contents'))
                choice_items = [i for i in li if i['name'] != name]
                new_position = menu_select('Choose New Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                if new_position < 0 or new_position == current_position: return
                li.insert(new_position, li.pop(current_position))
                db_execute_shortcut_folder()
            elif method == 'remove':
                menu_name = params.get('list_name')
                name = params.get('menu_name')
                li = json.loads(params.get('contents'))
                li = [x for x in li if x['name'] != name]
                db_execute_shortcut_folder()
            elif method == 'add_external':
                menu_item = json.loads(params['menu_item'])
                if not menu_item: return
                name = dialog.input('Choose Display Name', type=xbmcgui.INPUT_ALPHANUM, defaultt=params['name'])
                if not name: return
                menu_item['name'] = name
                current_shortcut_folders, folder_selection = select_shortcut_folders()
                if folder_selection < 0: return
                folder_selection = current_shortcut_folders[folder_selection]
                shortcut_folder_name = folder_selection[0]
                shortcut_folder_contents = json.loads(folder_selection[1])
                choice_items = shortcut_folder_contents
                if len(choice_items) > 0: item_position = menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                else: item_position = 0
                if item_position < 0: return
                menu_name = shortcut_folder_name
                li = shortcut_folder_contents
                li.insert(item_position, menu_item)
                db_execute_shortcut_folder()
            elif method == 'add_trakt':
                from apis.trakt_api import get_trakt_list_selection
                trakt_selection = json.loads(params['trakt_selection']) if 'trakt_selection' in params else get_trakt_list_selection(list_choice='nav_edit')
                if not trakt_selection: return
                name = dialog.input('Choose Display Name', type=xbmcgui.INPUT_ALPHANUM, defaultt=trakt_selection['name'])
                if not name: return
                menu_name = params.get('list_name')
                li = json.loads(params.get('contents'))
                choice_items = li
                item_position = menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                if item_position < 0: return
                li.insert(item_position, {"iconImage": "traktmylists.png", "mode": "trakt.build_trakt_list", "name": name, "foldername": name, "user": trakt_selection['user'], "slug": trakt_selection['slug'], 'external_list_item': 'True'})
                db_execute_shortcut_folder()
            elif method == 'add_trakt_external':
                name = dialog.input('Choose Display Name', type=xbmcgui.INPUT_ALPHANUM, defaultt=params['name'])
                if not name: return
                current_shortcut_folders, folder_selection = select_shortcut_folders()
                if folder_selection < 0: return
                folder_selection = current_shortcut_folders[folder_selection]
                shortcut_folder_name = folder_selection[0]
                shortcut_folder_contents = json.loads(folder_selection[1])
                choice_items = shortcut_folder_contents
                if len(choice_items) > 0: item_position = menu_select('Choose Insert Position of Menu Item (Insert Below Chosen Item)...', position_list=True)
                else: item_position = 0
                if item_position < 0: return
                menu_name = shortcut_folder_name
                li = shortcut_folder_contents
                li.insert(item_position, {"iconImage": "traktmylists.png", "mode": "trakt.build_trakt_list", "name": name, "foldername": name, "user": params['user'], "slug": params['slug'], 'external_list_item': 'True'})
                db_execute_shortcut_folder()
            elif method == 'clear_all':
                confirm = dialog.yesno('Are you sure?', 'Continuing will clear this Shortcut Folder.')
                if not confirm: return
                menu_name = params.get('list_name')
                li = []
                db_execute_shortcut_folder()
            elif method == 'add_shortcut_folder':
                name = dialog.input('Choose Folder Name', type=xbmcgui.INPUT_ALPHANUM)
                if not name: return
                dbcon = database.connect(NAVIGATOR_DB)
                dbcur = dbcon.cursor()
                dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (name, 'shortcut_folder', json.dumps([])))
                dbcon.commit()
            elif method == 'delete_shortcut_folder':
                list_name = params['list_name']
                if not dialog.yesno("Fen", "Are you sure?", "Continuing will delete your [B]%s[/B] folder" % list_name) != 0: return
                dbcon = database.connect(NAVIGATOR_DB)
                dbcur = dbcon.cursor()
                dbcur.execute("DELETE FROM navigator WHERE list_name = ?", (list_name,))
                dbcon.commit()
                dialog.ok('FEN Shortcut Folders', 'You Must Also Remove Instances of this Shortcut Folder from any Lists Individually.')
            elif method == 'remove_all_shortcut_folders':
                if not dialog.yesno("Fen", "Are you sure?", "Continuing will delete all your Source Folders") == 0: return
                dbcon = database.connect(NAVIGATOR_DB)
                dbcur = dbcon.cursor()
                dbcon.execute("DELETE FROM navigator WHERE list_type=?", ('shortcut_folder',))
                dbcon.commit()
                dialog.ok('FEN Shortcut Folders', 'You Must Also Remove Instances of Shortcut Folders from any Lists Individually.')
            notification("Process Successful", time=1500)
            xbmc.sleep(200)
            if not method in ('add_external', 'add_trakt_external'):
                xbmc.sleep(200)
                xbmc.executebuiltin('Container.Refresh')
        except:
            from modules.nav_utils import notification
            return notification('Error Performing Task')
    
    def build_shortcut_folder_lists(self):
        def _build_default():
            icon = os.path.join(self.icon_directory, 'furk.png')
            url_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt', 'contents': [], 'menu_item': '',
                        'list_name': list_name, 'menu_name': '',
                        'position': '', 'list_slug': '',
                        'external_list_item': 'False'}
            url = self._build_url(url_params)
            listitem = xbmcgui.ListItem("[B][I]Add a Trakt List...[/I][/B]")
            listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon})
            xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=True)
        def _build(item_position, item):
            try:
                cm = []
                name = item.get('name', '')
                icon = item.get('iconImage') if item.get('network_id', '') != '' else os.path.join(self.icon_directory, item.get('iconImage'))
                url = self._build_url(item)
                cm.append(("[B]Edit Menu[/B]",'XBMC.RunPlugin(%s)' % self._build_url(
                    {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'display_edit_menu', 'contents': json.dumps(contents), 'menu_item': json.dumps(item),
                    'list_name': list_name, 'menu_name': name,
                    'position': item_position, 'list_slug': item.get('slug', ''),
                    'external_list_item': item.get('external_list_item', 'False')})))
                listitem = xbmcgui.ListItem(name)
                listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon})
                listitem.addContextMenuItems(cm)
                if use_threading: item_list.append({'list_item': (url, listitem, True), 'item_position': item_position})
                else: xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            except: return
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        contents = self._db_lists_shortcut_folder()
        list_name = params['name']
        if not contents:
            _build_default()
            return self._end_directory()
        use_threading = settings.thread_main_menus()
        if use_threading:
            from threading import Thread
            item_list = []
            threads = []
            for item_position, item in enumerate(contents): threads.append(Thread(target=_build, args=(item_position, item)))
            [i.start() for i in threads]
            [i.join() for i in threads]
            item_list.sort(key=lambda k: k['item_position'])
            xbmcplugin.addDirectoryItems(__handle__, [i['list_item'] for i in item_list])
        else:
            for item_position, item in enumerate(contents): _build(item_position, item)
        self._end_directory()

    def _build_url(self, query):
        return __url__ + '?' + urlencode(to_utf8(query))

    def _setView(self, view=None, content='addons'):
        if not 'fen' in xbmc.getInfoLabel('Container.PluginName'): return
        view_type = self.view if not view else view
        try:
            t = 0
            while not xbmc.getInfoLabel('Container.Content') == content:
                if xbmc.abortRequested == True: break
                if not 'fen' in xbmc.getInfoLabel('Container.PluginName'): break
                t += 0.01
                if t >= 60.0: break
                time.sleep(0.01)
            VIEWS_DB = os.path.join(profile_dir, "views.db")
            settings.check_database(VIEWS_DB)
            dbcon = database.connect(VIEWS_DB)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT view_id FROM views WHERE view_type = ?", (str(view_type),))
            view_id = dbcur.fetchone()[0]
            return xbmc.executebuiltin("Container.SetViewMode(%s)" % str(view_id))
        except: return

    def _changelog_info(self):
        if __addon__.getSetting('disable_changelog_popup') == 'true': return
        addon_version = __addon__.getAddonInfo('version')
        setting_version = __addon__.getSetting('version_number')
        if addon_version == setting_version: return
        __addon__.setSetting('version_number', addon_version)
        from modules.nav_utils import show_text
        changelog_file, changelog_heading = xbmc.translatePath(os.path.join(addon_dir, "resources", "text", "changelog.txt")), '[B]Fen Changelog[/B]  [I](v.%s)[/I]' % addon_version
        window.setProperty('FEN_changelog_shown', 'true')
        show_text(changelog_heading, changelog_file)

    def _db_lists(self, list_name=None):
        list_name = self.list_name if not list_name else list_name
        try:
            default_contents = json.loads(window.getProperty('fen_%s_default' % list_name))
            try: edited_contents = json.loads(window.getProperty('fen_%s_edited' % list_name))
            except: edited_contents = None
            return default_contents, edited_contents
        except: pass
        try:
            dbcon = database.connect(NAVIGATOR_DB)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?", (str(list_name), 'default'))
            default_contents = json.loads(dbcur.fetchone()[0])
            dbcur.execute("SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?", (str(list_name), 'edited'))
            try: edited_contents = json.loads(dbcur.fetchone()[0])
            except: edited_contents = None
            window.setProperty('fen_%s_default' % list_name, json.dumps(default_contents))
            window.setProperty('fen_%s_edited' % list_name, json.dumps(edited_contents))
            return default_contents, edited_contents
        except:
            self._build_database()
            return self._db_lists()
    
    def _db_lists_shortcut_folder(self, list_name=None):
        list_name = self.list_name if not list_name else list_name
        try:
            contents = json.loads(window.getProperty('fen_%s_shortcut_folder' % list_name))
            return contents
        except: pass
        try:
            dbcon = database.connect(NAVIGATOR_DB)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?", (str(list_name), 'shortcut_folder'))
            contents = json.loads(dbcur.fetchone()[0])
            window.setProperty('fen_%s_shortcut_folder' % list_name, json.dumps(contents))
            return contents
        except:
            return []

    def _rebuild_single_database(self, dbcon, list_name):
        dbcon.execute("DELETE FROM navigator WHERE list_type=? and list_name=?", ('default', list_name))
        dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'default', json.dumps(eval('DefaultMenus().%s()' % list_name))))
        dbcon.commit()

    def _build_database(self):
        settings.initialize_databases()
        default_menus = DefaultMenus().DefaultMenuItems()
        dbcon = database.connect(NAVIGATOR_DB)
        for content in default_menus:
            dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (content, 'default', json.dumps(eval('DefaultMenus().%s()' % content))))
        dbcon.commit()

    def _add_dir(self, url_params, list_name, iconImage='DefaultFolder.png', isFolder=True):
        cm = []
        icon = iconImage if 'network_id' in url_params else os.path.join(self.icon_directory, iconImage)
        url_params['iconImage'] = icon
        url = self._build_url(url_params)
        listitem = xbmcgui.ListItem(list_name)
        listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon})
        if 'SpecialSort' in url_params:
            listitem.setProperty("SpecialSort", url_params['SpecialSort'])
        if not 'exclude_external' in url_params:
            list_name = url_params['list_name'] if 'list_name' in url_params else self.list_name
            menu_params = {'mode': 'navigator.adjust_main_lists', 'method': 'add_external',
                        'list_name': list_name, 'menu_item': json.dumps(url_params)}
            folder_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_external',
                        'name': list_name, 'menu_item': json.dumps(url_params)}
            cm.append(("[B]Add to a Menu[/B]",'XBMC.RunPlugin(%s)'% self._build_url(menu_params)))
            cm.append(("[B]Add to a Shortcut Folder[/B]",'XBMC.RunPlugin(%s)' % self._build_url(folder_params)))
            listitem.addContextMenuItems(cm)
        xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=isFolder)

    def _end_directory(self, cache_to_disc=True):
        xbmcplugin.setContent(__handle__, 'addons')
        xbmcplugin.endOfDirectory(__handle__, cacheToDisc=cache_to_disc)
        self._setView(self.view)


