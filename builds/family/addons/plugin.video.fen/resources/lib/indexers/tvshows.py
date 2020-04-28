import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import sys, os
import json
import importlib
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
from datetime import date
from modules.nav_utils import build_url, setView, remove_unwanted_info_keys, cached_page
from modules.utils import adjust_premiered_date, make_day
from modules.indicators_bookmarks import get_watched_status, get_resumetime, \
                                            get_watched_status_season, get_watched_status_tvshow, get_watched_info_tv
from apis.trakt_api import sync_watched_trakt_to_fen, get_trakt_tvshow_id
from modules.trakt_cache import clear_all_trakt_cache_data
from threading import Thread
from modules import settings
import tikimeta
# from modules.utils import logger


__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])

dialog = xbmcgui.Dialog()
is_widget = False if 'plugin' in xbmc.getInfoLabel('Container.PluginName') else True
window = xbmcgui.Window(10000)

class TVShows:
    def __init__(self, _list=None, idtype=None, action=None):
        tikimeta.check_meta_database()
        clear_all_trakt_cache_data(confirm=False)
        sync_watched_trakt_to_fen()
        self.list = [] if not _list else _list
        self.items = []
        self.new_page = None
        self.total_pages = None
        self.exit_list_params = None
        self.id_type = 'tmdb_id' if not idtype else idtype
        self.action = action
        self.cache_page_string = self.action

    def fetch_list(self):
        try:
            params = dict(parse_qsl(sys.argv[2].replace('?','')))
            worker = True
            mode = params.get('mode')
            cache_page = settings.cache_page()
            try: page_no = int(params.get('new_page', '1'))
            except ValueError: page_no = params.get('new_page')
            if cache_page:
                if self.action == 'tmdb_tv_discover':
                    self.cache_page_string = params['name']
                if not 'new_page' in params:
                    silent = True if is_widget else False
                    retrieved_page = cached_page(self.cache_page_string, silent=silent)
                    if retrieved_page: page_no = retrieved_page
            letter = params.get('new_letter', 'None')
            content_type = 'tvshows'
            self.exit_list_params = params.get('exit_list_params', None)
            if not self.exit_list_params: self.exit_list_params = xbmc.getInfoLabel('Container.FolderPath')
            var_module = 'tmdb_api' if 'tmdb' in self.action else 'trakt_api' if 'trakt' in self.action else 'imdb_api' if 'imdb' in self.action else None
            if var_module:
                try:
                    module = 'apis.%s' % (var_module)
                    function = getattr(importlib.import_module(module), self.action)
                except: pass
            if self.action in ('tmdb_tv_popular','tmdb_tv_top_rated', 'tmdb_tv_premieres','tmdb_tv_upcoming',
                'tmdb_tv_airing_today','tmdb_tv_on_the_air','trakt_tv_anticipated','trakt_tv_trending'):
                data = function(page_no)
                if 'tmdb' in self.action:
                    for item in data['results']: self.list.append(item['id'])
                else:
                    for item in data: self.list.append(get_trakt_tvshow_id(item['show']['ids']))
                self.new_page = {'mode': mode, 'action': self.action, 'new_page': str((data['page'] if 'tmdb' in self.action else page_no) + 1), 'foldername': self.action}
            elif self.action == 'tmdb_tv_discover':
                from indexers.discover import set_history
                name = params['name']
                query = params['query']
                if page_no == 1: set_history('tvshow', name, query)
                data = function(query, page_no)
                for item in data['results']: self.list.append(item['id'])
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'query': query, 'name': name, 'new_page': str(data['page'] + 1), 'foldername': self.action}
            elif self.action in ('trakt_collection', 'trakt_watchlist', 'trakt_collection_widgets'):
                data, total_pages = function('shows', page_no, letter)
                self.list = [i['media_id'] for i in data]
                if total_pages > 2: self.total_pages = total_pages
                if total_pages > page_no: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'foldername': self.action}
            elif self.action == 'trakt_tv_mosts':
                for item in function(params['period'], params['duration'], page_no): self.list.append((get_trakt_tvshow_id(item['show']['ids'])))
                self.new_page = {'mode': mode, 'action': self.action, 'period': params['period'], 'duration': params['duration'], 'new_page': str(page_no + 1), 'foldername': self.action}
            elif self.action == 'trakt_tv_related':
                self.sim_recom_name = params.get('sim_recom_name')
                self.sim_recom_tmdb = params.get('sim_recom_tmdb')
                self.sim_recom_imdb = params.get('sim_recom_imdb')
                data, total_pages = function(self.sim_recom_imdb, page_no)
                for item in data: self.list.append(get_trakt_tvshow_id(item['ids']))
                if total_pages > page_no: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'sim_recom_name': self.sim_recom_name, 'sim_recom_tmdb': self.sim_recom_tmdb, 'sim_recom_imdb': self.sim_recom_imdb, 'foldername': self.action, 'imdb_id': params.get('imdb_id')}
            elif self.action == 'tmdb_tv_genres':
                genre_id = params['genre_id'] if 'genre_id' in params else self.multiselect_genres(params.get('genre_list'))
                if not genre_id: return
                data = function(genre_id, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'genre_id': genre_id, 'foldername': genre_id}
            elif self.action == 'tmdb_tv_languages':
                language = params['language']
                if not language: return
                data = function(language, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'language': language, 'foldername': language}
            elif self.action == 'tmdb_tv_networks':
                data = function(params['network_id'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'network_id': params['network_id'], 'foldername': params['network_id']}
            elif self.action == 'trakt_tv_certifications':
                for item in function(params['certification'], page_no): self.list.append((get_trakt_tvshow_id(item['show']['ids'])))
                self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'foldername': params['certification'], 'certification': params['certification']}
            elif self.action == 'tmdb_tv_year':
                data = function(params['year'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'year': params['year'], 'foldername': params['year']}
            elif self.action in ('in_progress_tvshows', 'favourites_tvshows', 'subscriptions_tvshows', 'kodi_library_tvshows', 'watched_tvshows'):
                (var_module, import_function) = ('in_progress', 'in_progress_tvshow') if 'in_progress' in self.action else ('favourites', 'retrieve_favourites') if 'favourites' in self.action else ('subscriptions', 'retrieve_subscriptions') if 'subscriptions' in self.action else ('indicators_bookmarks', 'get_watched_items') if 'watched' in self.action else ('kodi_library', 'retrieve_kodi_library') if 'library' in self.action else ''
                try:
                    module = 'modules.%s' % (var_module)
                    function = getattr(importlib.import_module(module), import_function)
                except: pass
                if self.action == 'kodi_library_tvshows': self.id_type = 'tvdb_id'
                data, total_pages = function('tvshow', page_no, letter)
                self.list = [i['media_id'] for i in data]
                if total_pages > 2: self.total_pages = total_pages
                if total_pages > page_no: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'foldername': self.action}
            elif self.action in ('tmdb_tv_similar', 'tmdb_tv_recommendations'):
                self.sim_recom_name = params.get('sim_recom_name')
                self.sim_recom_tmdb = params.get('sim_recom_tmdb')
                self.sim_recom_imdb = params.get('sim_recom_imdb')
                data = function(self.sim_recom_tmdb, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'sim_recom_name': self.sim_recom_name, 'sim_recom_tmdb': self.sim_recom_tmdb, 'sim_recom_imdb': self.sim_recom_imdb, 'foldername': self.action}
            elif self.action == 'trakt_recommendations':
                for item in function('shows'): self.list.append(get_trakt_tvshow_id(item['ids']))
            elif self.action == 'tmdb_popular_people':
                import os
                worker = False
                icon_directory = settings.get_theme()
                data = function(page_no)
                content_type = 'addons'
                fanart = __addon__.getAddonInfo('fanart')
                for item in data['results']:
                    cm = []
                    actor_poster = "http://image.tmdb.org/t/p/original%s" % item['profile_path'] if item['profile_path'] else os.path.join(icon_directory, 'genre_family.png')
                    url_params = {'mode': 'people_search.main', 'actor_id': item['id'], 'actor_name': item['name'], 'actor_image': actor_poster.replace('w185', 'h632')}
                    cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedactorinfo,id=%s)' % item['id']))
                    url = build_url(url_params)
                    listitem = xbmcgui.ListItem(item['name'])
                    listitem.setArt({'icon': actor_poster, 'poster': actor_poster, 'thumb': actor_poster, 'fanart': fanart, 'banner': actor_poster})
                    listitem.addContextMenuItems(cm)
                    xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(int(data['page']) + 1), 'foldername': self.action}
            elif self.action == 'tmdb_tv_search':
                try: from urllib import unquote
                except ImportError: from urllib.parse import unquote
                if params.get('query') == 'NA':
                    search_title = dialog.input("Search Fen", type=xbmcgui.INPUT_ALPHANUM)
                    search_name = unquote(search_title)
                else: search_name = unquote(params.get('query'))
                if not search_name: return
                params['search_name'] = search_name
                data = function(search_name, page_no)
                total_pages = data['total_pages']
                if total_pages > page_no: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'query': search_name, 'foldername': search_name}
                self.list = [i['id'] for i in data['results']]
            if self.total_pages and not is_widget:
                url_params = {'mode': 'build_navigate_to_page', 'db_type': 'TV Shows', 'current_page': page_no, 'total_pages': self.total_pages, 'transfer_mode': mode, 'transfer_action': self.action, 'foldername': self.action, 'query': params.get('search_name', ''), 'actor_id': params.get('actor_id', '')}
                self.add_dir(url_params, 'Jump To...', 'Jump To a Certain Page/Letter...', 'item_jump.png')
            if cache_page: cached_page(self.cache_page_string, page_no=page_no)
            if worker: self.worker()
            if self.new_page:
                self.new_page['exit_list_params'] = self.exit_list_params
                self.add_dir(self.new_page)
        except: pass
        xbmcplugin.setContent(__handle__, content_type)
        xbmcplugin.endOfDirectory(__handle__)
        if params.get('refreshed') == 'true': xbmc.sleep(1500)
        setView('view.tvshows', content_type)

    def build_tvshow_content(self):
        def _build(item):
            try:
                listitem = xbmcgui.ListItem()
                cm = []
                item_no = item['item_no']
                tmdb_id = item['tmdb_id']
                tvdb_id = item['tvdb_id']
                imdb_id = item['imdb_id']
                title = item['title']
                year = item['year']
                trailer = item['trailer']
                if not 'rootname' in item: item['rootname'] = '{0} ({1})'.format(title, year)
                meta_json = json.dumps(item)
                openinfo_params = {'mode': 'extended_info_open', 'db_type': 'tvshow', 'tmdb_id': tmdb_id}
                season_params = {'mode': 'build_season_list', 'meta': meta_json, 'tmdb_id': tmdb_id}
                all_episodes_params = {'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': 'all', 'meta': meta_json}
                url_params = openinfo_params if default_openinfo else all_episodes_params if all_episodes else season_params
                url = build_url(url_params)
                playback_menu_params = {'mode': 'playback_menu', 'list_name': list_name}
                watched_params = {"mode": "mark_tv_show_as_watched_unwatched", "action": 'mark_as_watched', "title": title, "year": year, "media_id": tmdb_id, "imdb_id": imdb_id, "tvdb_id": tvdb_id, "meta_user_info": meta_user_info}
                unwatched_params = {"mode": "mark_tv_show_as_watched_unwatched", "action": 'mark_as_unwatched', "title": title, "year": year, "media_id": tmdb_id, "imdb_id": imdb_id, "tvdb_id": tvdb_id, "meta_user_info": meta_user_info}
                add_remove_params = {"mode": "build_add_to_remove_from_list", "media_type": "tvshow", "meta": meta_json, "orig_mode": self.action}
                sim_recom_params = {"mode": "similar_recommendations_choice", "db_type": "tv", 'sim_recom_name': item['rootname'], "sim_recom_tmdb": tmdb_id, "sim_recom_imdb": imdb_id, "meta_user_info": meta_user_info}
                cm.append(("[B]Mark Watched %s[/B]" % watched_title, "XBMC.RunPlugin(%s)" % build_url(watched_params)))
                cm.append(("[B]Mark Unwatched %s[/B]" % watched_title, "XBMC.RunPlugin(%s)" % build_url(unwatched_params)))
                cm.append(("[B]Options[/B]",'XBMC.RunPlugin(%s)' % build_url(playback_menu_params)))
                if default_openinfo:
                    browse_params = all_episodes_params if all_episodes else season_params
                    cm.append(("[B]Browse...[/B]",'XBMC.Container.Update(%s)' % build_url(browse_params)))
                cm.append(("[B]Add/Remove[/B]", "XBMC.RunPlugin(%s)" % build_url(add_remove_params)))
                cm.append(("[B]Similar/Recommended[/B]", "XBMC.RunPlugin(%s)" % build_url(sim_recom_params)))
                if self.action in ('trakt_tv_related', 'tmdb_tv_recommendations'):
                    sim_recom_title = 'Similar to' if self.action == 'trakt_tv_related' else 'Recommended based on'
                    export_sim_recom_params = {'mode': 'navigator.adjust_main_lists', 'method': 'add_sim_recom_external', 'end_mode': 'build_tvshow_list',
                                    'end_action': self.action, 'db_type': 'tvshow', 'sim_recom_name': '[B]TV Shows[/B] | %s %s' % (sim_recom_title, self.sim_recom_name),
                                    'sim_recom_tmdb': self.sim_recom_tmdb, 'sim_recom_imdb': self.sim_recom_imdb}
                    cm.append(("[B]Export %s List[/B]" % sim_recom_title.split(' ')[0], "XBMC.RunPlugin(%s)" % build_url(export_sim_recom_params)))
                if trailer:
                    (trailer_params, trailer_title) = ({'mode': 'play_trailer', 'url': trailer, 'all_trailers': json.dumps(item['all_trailers'])}, 'Choose Trailer') if (all_trailers and item.get('all_trailers', False)) else ({'mode': 'play_trailer', 'url': trailer}, 'Trailer')
                    cm.append(("[B]%s[/B]" % trailer_title,"XBMC.RunPlugin(%s)" % build_url(trailer_params)))
                if self.action == 'trakt_recommendations':
                    hide_recommended_params = {'mode': 'trakt.hide_recommendations', 'db_type': 'shows', 'imdb_id': imdb_id}
                    cm.append(("[B]Hide from Recommendations[/B]", "XBMC.RunPlugin(%s)" % build_url(hide_recommended_params)))
                cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedtvinfo,id=%s)' % tmdb_id))
                cm.append(("[B]Exit TV Show List[/B]","XBMC.Container.Refresh(%s)" % self.exit_list_params))
                listitem.setLabel(title)
                listitem.addContextMenuItems(cm)
                listitem.setCast(item['cast'])
                listitem.setUniqueIDs({'imdb': str(imdb_id), 'tmdb': str(tmdb_id), 'tvdb': str(tvdb_id)})
                listitem.setArt({'poster': item['poster'], 'fanart': item['fanart'], 'icon': item['poster'], 'banner': item['banner'], 'clearart': item['clearart'], 'clearlogo': item['clearlogo'], 'landscape': item['landscape']})
                listitem.setProperty('watchedepisodes', item['total_watched'])
                listitem.setProperty('unwatchedepisodes', item['total_unwatched'])
                listitem.setProperty('totalepisodes', str(item['total_episodes']))
                listitem.setProperty('totalseasons', str(item['total_seasons']))
                if is_widget: listitem.setProperty("fen_widget", 'true')
                listitem.setInfo('video', remove_unwanted_info_keys(item))
                if use_threading: item_list.append({'list_item': (url, listitem, True), 'item_position': item_no})
                else: xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            except: pass
        all_trailers = settings.all_trailers()
        use_threading = settings.thread_main_menus()
        default_openinfo = True if settings.default_openinfo() in (2, 3) else False
        all_episodes = settings.default_all_episodes()
        watched_title = 'Trakt' if self.use_trakt else "Fen"
        meta_user_info = json.dumps(self.meta_user_info)
        list_name = self.cache_page_string
        if use_threading:
            item_list = []
            threads = []
            for item in self.items: threads.append(Thread(target=_build, args=(item,)))
            [i.start() for i in threads]
            [i.join() for i in threads]
            item_list.sort(key=lambda k: k['item_position'])
            xbmcplugin.addDirectoryItems(__handle__, [i['list_item'] for i in item_list])
        else:
            for item in sorted(self.items, key=lambda k: k['item_no']): _build(item)

    def set_info(self, item_no, item):
        meta = tikimeta.tvshow_meta(self.id_type, item, self.meta_user_info)
        if not meta: return
        playcount, overlay, total_watched, total_unwatched = get_watched_status_tvshow(self.watched_info, self.use_trakt, meta['tmdb_id'], meta.get('total_episodes'))
        meta.update({'item_no': item_no, 'playcount': playcount, 'overlay': overlay,
                     'total_watched': str(total_watched), 'total_unwatched': str(total_unwatched)})
        if not 'rootname' in meta: meta['rootname'] = '{0} ({1})'.format(meta['title'], meta['year'])
        self.items.append(meta)

    def worker(self):
        threads = []
        if not self.exit_list_params: self.exit_list_params = xbmc.getInfoLabel('Container.FolderPath')
        self.watched_info, self.use_trakt = get_watched_info_tv()
        self.meta_user_info = tikimeta.retrieve_user_info()
        window.clearProperty('fen_fanart_error')
        for item_position, item in enumerate(self.list): threads.append(Thread(target=self.set_info, args=(item_position, item)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        self.build_tvshow_content()

    def multiselect_genres(self, genre_list):
        import os
        genre_list = json.loads(genre_list)
        choice_list = []
        icon_directory = settings.get_theme()
        for genre, value in sorted(genre_list.items()):
            listitem = xbmcgui.ListItem(genre)
            listitem.setArt({'icon': os.path.join(icon_directory, value[1])})
            listitem.setProperty('genre_id', value[0])
            choice_list.append(listitem)
        chosen_genres = dialog.multiselect("Select Genres to Include in Search", choice_list, useDetails=True)
        if not chosen_genres: return
        genre_ids = [choice_list[i].getProperty('genre_id') for i in chosen_genres]
        return ','.join(genre_ids)

    def add_dir(self, url_params, list_name='Next Page >>', info='Navigate to Next Page...', iconImage='item_next.png'):
        icon = os.path.join(settings.get_theme(), iconImage)
        url = build_url(url_params)
        listitem = xbmcgui.ListItem(list_name)
        listitem.setArt({'icon': icon, 'fanart': __addon__.getAddonInfo('fanart')})
        listitem.setInfo('video', {'title': list_name, 'plot': info})
        if url_params['mode'] == 'build_navigate_to_page': listitem.addContextMenuItems([("[B]Switch Jump To Action[/B]","XBMC.RunPlugin(%s)" % build_url({'mode': 'toggle_jump_to'}))])
        xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=True)

def build_season_list():
    def _build(item, item_position=None):
        try:
            listitem = xbmcgui.ListItem()
            cm = []
            overview = item['overview']
            name = item['name']
            poster_path = item['poster_path']
            season_number = item['season_number']
            episode_count = item['episode_count']
            plot = overview if overview != '' else show_plot
            title = name if use_season_title and name != '' else 'Season %s' % str(season_number)
            season_poster = poster_path if poster_path is not None else show_poster
            playcount, overlay, watched, unwatched = get_watched_status_season(watched_info, use_trakt, tmdb_id, season_number, episode_count)
            watched_params = {"mode": "mark_season_as_watched_unwatched", "action": 'mark_as_watched', "title": show_title, "year": show_year, "media_id": tmdb_id, "imdb_id": imdb_id, "tvdb_id": tvdb_id, "season": season_number, "meta_user_info": meta_user_info}
            unwatched_params = {"mode": "mark_season_as_watched_unwatched", "action": 'mark_as_unwatched', "title": show_title, "year": show_year, "media_id": tmdb_id, "imdb_id": imdb_id, "tvdb_id": tvdb_id, "season": season_number, "meta_user_info": meta_user_info}
            playback_menu_params = {'mode': 'playback_menu'}
            cm.append(("[B]Mark Watched %s[/B]" % watched_title,'XBMC.RunPlugin(%s)' % build_url(watched_params)))
            cm.append(("[B]Mark Unwatched %s[/B]" % watched_title,'XBMC.RunPlugin(%s)' % build_url(unwatched_params)))
            cm.append(("[B]Options[/B]",'XBMC.RunPlugin(%s)' % build_url(playback_menu_params)))
            cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedtvinfo,id=%s)' % tmdb_id))
            url_params = {'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': season_number}
            url = build_url(url_params)
            listitem.setLabel(title)
            listitem.setProperty('watchedepisodes', str(watched))
            listitem.setProperty('unwatchedepisodes', str(unwatched))
            listitem.setProperty('totalepisodes', str(episode_count))
            listitem.addContextMenuItems(cm)
            listitem.setArt({'poster': season_poster, 'fanart': fanart, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape})
            listitem.setCast(cast)
            listitem.setUniqueIDs({'imdb': str(imdb_id), 'tmdb': str(tmdb_id), 'tvdb': str(tvdb_id)})
            listitem.setInfo(
                'video', {'mediatype': 'tvshow', 'trailer': trailer,
                    'title': show_title, 'size': '0', 'duration': episode_run_time, 'plot': plot,
                    'rating': rating, 'premiered': premiered, 'studio': studio,
                    'year': show_year,'genre': genre, 'mpaa': mpaa,
                    'tvshowtitle': show_title, 'imdbnumber': imdb_id,'votes': votes,
                    'episode': str(episode_count),'playcount': playcount, 'overlay': overlay})
            if use_threading: item_list.append({'list_item': (url, listitem, True), 'item_position': item_position})
            else: xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    meta_user_info = tikimeta.retrieve_user_info()
    if 'meta' in params:
        meta = json.loads(params.get('meta'))
    else:
        window.clearProperty('fen_fanart_error')
        meta = tikimeta.tvshow_meta('tmdb_id', params.get('tmdb_id'), meta_user_info)
    season_data = tikimeta.all_episodes_meta(meta['tmdb_id'], meta['tvdb_id'], meta['tvdb_summary']['airedSeasons'], meta['season_data'], meta_user_info)
    if not season_data: return
    meta_user_info = json.dumps(meta_user_info)
    tmdb_id = meta['tmdb_id']
    tvdb_id = meta['tvdb_id']
    imdb_id = meta['imdb_id']
    show_title = meta['title']
    show_year = meta['year']
    show_poster = meta['poster']
    show_plot = meta['plot']
    fanart = meta['fanart']
    banner = meta['banner']
    clearlogo = meta['clearlogo']
    clearart = meta['clearart']
    landscape = meta['landscape']
    cast = meta['cast']
    mpaa = meta['mpaa']
    trailer = str(meta['trailer'])
    episode_run_time = meta.get('episode_run_time')
    rating = meta.get('rating')
    premiered = meta.get('premiered')
    studio = meta.get('studio')
    genre = meta.get('genre')
    votes = meta.get('votes')
    if not settings.show_specials(): season_data = [i for i in season_data if not i['season_number'] == 0]
    season_data = sorted(season_data, key=lambda i: i['season_number'])
    use_season_title = settings.use_season_title()
    watched_indicators = settings.watched_indicators()
    watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
    use_threading = settings.thread_main_menus()
    watched_info, use_trakt = get_watched_info_tv()
    if use_threading:
        item_list = []
        threads = []
        for item_position, item in enumerate(season_data): threads.append(Thread(target=_build, args=(item, item_position)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        item_list.sort(key=lambda k: k['item_position'])
        xbmcplugin.addDirectoryItems(__handle__, [i['list_item'] for i in item_list])
    else:
        for item in season_data: _build(item)
    xbmcplugin.setContent(__handle__, 'seasons')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.seasons', 'seasons')
    window.setProperty('fen_media_meta', json.dumps(meta))

def build_episode_list():
    def _build(item):
        try:
            listitem = xbmcgui.ListItem()
            cm = []
            season = item['season']
            episode = item['episode']
            ep_name = item['title']
            premiered = item['premiered']
            try: episode_date, premiered = adjust_premiered_date(premiered, adjust_hours)
            except: episode_date = date(2000,1,1) if season == 0 else None
            playcount, overlay = get_watched_status(watched_info, use_trakt, 'episode', tmdb_id, season, episode)
            resumetime = get_resumetime('episode', tmdb_id, season, episode)
            query = title + ' S%.2dE%.2d' % (int(season), int(episode))
            display_name = '%s - %dx%.2d' % (title, season, episode)
            thumb = item['thumb'] if item.get('thumb', None) else fanart
            meta.update({'vid_type': 'episode', 'rootname': display_name, 'season': season,
                        'episode': episode, 'premiered': premiered, 'ep_name': ep_name,
                        'plot': item['plot']})
            item.update({'trailer': trailer, 'tvshowtitle': title, 'premiered': premiered,
                        'genre': genre, 'duration': duration, 'mpaa': mpaa,
                        'studio': studio, 'playcount': playcount, 'overlay': overlay})
            meta_json = json.dumps(meta)
            url_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': tmdb_id,
                        'query': query, 'tvshowtitle': meta['rootname'], 'season': season,
                        'episode': episode, 'meta': meta_json}
            url = build_url(url_params)
            display = ep_name
            unaired = False
            if not episode_date or current_adjusted_date < episode_date:
                unaired = True
                display = '[I][COLOR %s]%s[/COLOR][/I]' % (unaired_color, ep_name)
                item['title'] = display
            item['sortseason'] = season
            item['sortepisode'] = episode
            (state, action) = ('Watched', 'mark_as_watched') if playcount == 0 else ('Unwatched', 'mark_as_unwatched')
            playback_menu_params = {'mode': 'playback_menu', 'suggestion': query, 'play_params': json.dumps(url_params)}
            if not unaired:
                watched_unwatched_params = {"mode": "mark_episode_as_watched_unwatched", "action": action, "media_id": tmdb_id, "imdb_id": imdb_id, "tvdb_id": tvdb_id, "season": season, "episode": episode,  "title": title, "year": year}
                cm.append(("[B]Mark %s %s[/B]" % (state, watched_title),'RunPlugin(%s)' % build_url(watched_unwatched_params)))
            cm.append(("[B]Options[/B]",'RunPlugin(%s)' % build_url(playback_menu_params)))
            if not unaired and resumetime != '0': cm.append(("[B]Clear Progress[/B]", 'RunPlugin(%s)' % build_url({"mode": "watched_unwatched_erase_bookmark", "db_type": "episode", "media_id": tmdb_id, "season": season, "episode": episode, "refresh": "true"})))
            cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedtvinfo,id=%s)' % tmdb_id))
            listitem.setLabel(display)
            listitem.setProperty("resumetime", resumetime)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'poster': show_poster, 'fanart': fanart, 'thumb': thumb, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape})
            listitem.setCast(cast)
            listitem.setUniqueIDs({'imdb': str(imdb_id), 'tmdb': str(tmdb_id), 'tvdb': str(tvdb_id)})
            listitem.setInfo('video', remove_unwanted_info_keys(item))
            if is_widget:
                listitem.setProperty("fen_widget", 'true')
                listitem.setProperty("fen_playcount", str(playcount))
                listitem.setProperty("fen_playback_menu_params", json.dumps(playback_menu_params))
            if use_threading: item_list.append((url, listitem, False))
            else: xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=False)
        except: pass
    unaired_color = settings.unaired_episode_colour()
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    meta_user_info = tikimeta.retrieve_user_info()
    all_episodes = True if params.get('season') == 'all' else False
    if all_episodes:
        if 'meta' in params:
            meta = json.loads(params.get('meta'))
        else:
            window.clearProperty('fen_fanart_error')
            meta = tikimeta.tvshow_meta('tmdb_id', params.get('tmdb_id'), meta_user_info)
    else:
        try:
            meta = json.loads(window.getProperty('fen_media_meta'))
        except:
            window.clearProperty('fen_fanart_error')
            meta = tikimeta.tvshow_meta('tmdb_id', params.get('tmdb_id'), meta_user_info)
    tmdb_id = meta['tmdb_id']
    tvdb_id = meta['tvdb_id']
    imdb_id = meta['imdb_id']
    title = meta['title']
    year = meta['year']
    rootname = meta['rootname']
    show_poster = meta['poster']
    fanart = meta['fanart']
    banner = meta['banner']
    clearlogo = meta['clearlogo']
    clearart = meta['clearart']
    landscape = meta['landscape']
    cast = meta['cast']
    mpaa = meta['mpaa']
    duration = meta.get('duration')
    trailer = str(meta['trailer'])
    genre = meta.get('genre')
    studio = meta.get('studio')
    adjust_hours = int(__addon__.getSetting('datetime.offset'))
    watched_indicators = settings.watched_indicators()
    current_adjusted_date = settings.adjusted_datetime(dt=True)
    watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
    episodes_data = tikimeta.season_episodes_meta(tmdb_id, tvdb_id, params.get('season'), meta['tvdb_summary']['airedSeasons'], meta['season_data'], meta_user_info, all_episodes)
    if all_episodes:
        if not settings.show_specials(): episodes_data = [i for i in episodes_data if not i['season'] == 0]
    episodes_data = sorted(episodes_data, key=lambda i: i['episode'])
    watched_info, use_trakt = get_watched_info_tv()
    use_threading = settings.thread_main_menus()
    if use_threading:
        item_list = []
        threads = []
        for item in episodes_data: threads.append(Thread(target=_build, args=(item,)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        xbmcplugin.addDirectoryItems(__handle__, item_list)
    else:
        for item in episodes_data: _build(item)
    xbmcplugin.setContent(__handle__, 'episodes')
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_EPISODE)
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.episodes', 'episodes')

def build_episode(item, watched_info, use_trakt, meta_user_info):
    def check_for_unaired(premiered, season):
        if item.get('ignore_unaired', False): return False
        unaired = False
        adjust_hours = item.get('adjust_hours', None)
        if not adjust_hours : adjust_hours = int(__addon__.getSetting('datetime.offset'))
        current_adjusted_date = item.get('current_adjusted_date', None)
        if not current_adjusted_date : current_adjusted_date = settings.adjusted_datetime(dt=True)
        try: episode_date, premiered = adjust_premiered_date(premiered, adjust_hours)
        except: episode_date = date(2000,1,1) if season == 0 else None
        if not episode_date or current_adjusted_date < episode_date:
            unaired = True
        return unaired, current_adjusted_date, episode_date, premiered
    def build_display():
        if nextep_info:
            display_premiered = make_day(episode_date)
            airdate = '[[COLOR %s]%s[/COLOR]] ' % (nextep_info['airdate_colour'], display_premiered) if nextep_info['include_airdate'] else ''
            highlight_color = nextep_info['unwatched_colour'] if item.get('unwatched', False) else nextep_info['unaired_colour'] if unaired else ''
            italics_open, italics_close = ('[I]', '[/I]') if highlight_color else ('', '')
            if highlight_color: episode_info = '%s[COLOR %s]%dx%.2d - %s[/COLOR]%s' % (italics_open, highlight_color, info['season'], info['episode'], info['title'], italics_close)
            else: episode_info = '%s%dx%.2d - %s%s' % (italics_open, info['season'], info['episode'], info['title'], italics_close)
            display = '%s%s: %s' % (airdate, title, episode_info)
        elif trakt_calendar:
            display_premiered = make_day(episode_date)
            display = '[%s] %s: %dx%.2d - %s' % (display_premiered, title.upper(), info['season'], info['episode'], info['title'])
            if unaired:
                unaired_color = settings.unaired_episode_colour()
                displays = display.split(']')
                display = '[COLOR %s]' % unaired_color + displays[0] + '][/COLOR]' + displays[1]
        else:
            unaired_color = settings.unaired_episode_colour()
            color_tags = ('[COLOR %s]' % unaired_color, '[/COLOR]') if unaired else ('', '')
            display = '%s: %s%dx%.2d - %s%s' % (title.upper(), color_tags[0], info['season'], info['episode'], info['title'], color_tags[1])
        return display
    try:
        listitem = xbmcgui.ListItem()
        cm = []
        nextep_info = item.get('nextep_display_settings', None)
        trakt_calendar = item.get('trakt_calendar', False)
        action = item.get('action', '')
        meta = item['meta']
        tmdb_id = meta['tmdb_id']
        tvdb_id = meta['tvdb_id']
        imdb_id = meta["imdb_id"]
        title = meta['title']
        year = meta['year']
        episodes_data = tikimeta.season_episodes_meta(tmdb_id, tvdb_id, item['season'], meta['tvdb_summary']['airedSeasons'], meta['season_data'], meta_user_info)
        info = [i for i in episodes_data if i['episode'] == item['episode']][0]
        season = info['season']
        episode = info['episode']
        premiered = info['premiered']
        unaired, current_adjusted_date, episode_date, premiered = check_for_unaired(premiered, season)
        if unaired and not item.get('include_unaired', False): return
        thumb = info['thumb'] if info.get('thumb', None) else meta['fanart']
        playcount, overlay = get_watched_status(watched_info, use_trakt, 'episode', tmdb_id, season, episode)
        info.update({'trailer': str(meta.get('trailer')), 'tvshowtitle': title, 'premiered': premiered,
                    'genre': meta.get('genre'), 'duration': meta.get('duration'), 'mpaa': meta.get('mpaa'),
                    'studio': meta.get('studio'), 'playcount': playcount, 'overlay': overlay})
        resumetime = get_resumetime('episode', tmdb_id, season, episode)
        query = title + ' S%.2dE%.2d' % (season, episode)
        display = build_display()
        rootname = '{0} ({1})'.format(title, year)
        meta.update({'vid_type': 'episode', 'rootname': rootname, 'season': season,
                    'episode': episode, 'premiered': premiered, 'ep_name': info['title'],
                    'plot': info['plot']})
        meta_json = json.dumps(meta)
        url_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': tmdb_id, 'query': query,
                'tvshowtitle': meta['rootname'], 'season': season, 'episode': episode, 'meta': meta_json}
        url = build_url(url_params)
        browse_url = build_url({'mode': 'build_season_list', 'meta': meta_json})
        playback_menu_params = {'mode': 'playback_menu', 'suggestion': query, 'play_params': json.dumps(url_params)}
        if not unaired:
            watched_indicators = item['watched_indicators'] if 'watched_indicators' in item else settings.watched_indicators()
            (wstate, waction) = ('Watched', 'mark_as_watched') if playcount == 0 else ('Unwatched', 'mark_as_unwatched')
            watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
            watched_params = {"mode": "mark_episode_as_watched_unwatched", "action": waction, "media_id": tmdb_id, "imdb_id": imdb_id, "tvdb_id": tvdb_id, "season": season, "episode": episode,  "title": title, "year": year}
            cm.append(("[B]Mark %s %s[/B]" % (wstate, watched_title),'RunPlugin(%s)' % build_url(watched_params)))
        cm.append(("[B]Options[/B]",'RunPlugin(%s)' % build_url(playback_menu_params)))
        if action == 'next_episode':
            nextep_manage_params = {"mode": "next_episode_context_choice"}
            cm.append(("[B]Next Episode Manager[/B]",'RunPlugin(%s)'% build_url(nextep_manage_params)))
            if nextep_info['cache_to_disk']: cm.append(("[B]Refresh...[/B]", 'Container.Refresh()'))
        cm.append(("[B]Browse...[/B]",'Container.Update(%s)' % browse_url))
        cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedtvinfo,id=%s)' % tmdb_id))
        if not unaired and resumetime != '0': cm.append(("[B]Clear Progress[/B]", 'RunPlugin(%s)' % build_url({"mode": "watched_unwatched_erase_bookmark", "db_type": "episode", "media_id": tmdb_id, "season": season, "episode": episode, "refresh": "true"})))
        listitem.setLabel(display)
        listitem.setProperty("resumetime", resumetime)
        listitem.setArt({'poster': meta['poster'], 'fanart': meta['fanart'], 'thumb':thumb, 'banner': meta['banner'], 'clearart': meta['clearart'], 'clearlogo': meta['clearlogo'], 'landscape': meta['landscape']})
        listitem.addContextMenuItems(cm)
        listitem.setCast(meta['cast'])
        listitem.setUniqueIDs({'imdb': str(imdb_id), 'tmdb': str(tmdb_id), 'tvdb': str(tvdb_id)})
        info['title'] = display
        listitem.setInfo('video', remove_unwanted_info_keys(info))
        if is_widget:
            listitem.setProperty("fen_widget", 'true')
            listitem.setProperty("fen_playcount", str(playcount))
            listitem.setProperty("fen_playback_menu_params", json.dumps(playback_menu_params))
        return {'listitem': (url, listitem, False), 'curr_last_played_parsed': item.get('curr_last_played_parsed', ''), 'label': display, 'order': item.get('order', ''), 'name': query, 'first_aired': premiered}
    except: pass



