import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import sys, os
import json
import importlib
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
from modules.nav_utils import build_url, setView, remove_unwanted_info_keys, cached_page
from modules.indicators_bookmarks import get_watched_status, get_resumetime, get_watched_info_movie
from apis.trakt_api import sync_watched_trakt_to_fen, get_trakt_movie_id
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

class Movies:
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
                if self.action == 'tmdb_movies_discover':
                    self.cache_page_string = params['name']
                if not 'new_page' in params:
                    silent = True if is_widget else False
                    retrieved_page = cached_page(self.cache_page_string, silent=silent)
                    if retrieved_page: page_no = retrieved_page
            letter = params.get('new_letter', 'None')
            content_type = 'movies'
            self.exit_list_params = params.get('exit_list_params', None)
            if not self.exit_list_params: self.exit_list_params = xbmc.getInfoLabel('Container.FolderPath')
            var_module = 'tmdb_api' if 'tmdb' in self.action else 'trakt_api' if 'trakt' in self.action else 'imdb_api' if 'imdb' in self.action else ''
            if var_module:
                try:
                    module = 'apis.%s' % (var_module)
                    function = getattr(importlib.import_module(module), self.action)
                except: pass
            if self.action in ('tmdb_movies_popular','tmdb_movies_blockbusters','tmdb_movies_in_theaters',
                'tmdb_movies_top_rated','tmdb_movies_upcoming','tmdb_movies_latest_releases','tmdb_movies_premieres',
                'trakt_movies_trending','trakt_movies_anticipated','trakt_movies_top10_boxoffice'):
                data = function(page_no)
                if 'tmdb' in self.action:
                    data = function(page_no)
                    for item in data['results']: self.list.append(item['id'])
                else:
                    data = function(page_no)
                    for item in data: self.list.append(get_trakt_movie_id(item['movie']['ids']))
                if self.action not in ('trakt_movies_top10_boxoffice'): self.new_page = {'mode': mode, 'action': self.action, 'new_page': str((data['page'] if 'tmdb' in self.action else page_no) + 1), 'foldername': self.action}
            elif self.action == 'tmdb_movies_discover':
                from indexers.discover import set_history
                name = params['name']
                query = params['query']
                if page_no == 1: set_history('movie', name, query)
                data = function(query, page_no)
                for item in data['results']: self.list.append(item['id'])
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'query': query, 'name': name, 'new_page': str(data['page'] + 1), 'foldername': self.action}
            elif self.action in ('trakt_collection', 'trakt_watchlist', 'trakt_collection_widgets'):
                data, total_pages = function('movies', page_no, letter)
                self.list = [i['media_id'] for i in data]
                if total_pages > 2: self.total_pages = total_pages
                if total_pages > page_no: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'foldername': self.action}
            elif self.action == 'imdb_movies_oscar_winners':
                from modules.nav_utils import oscar_winners_tmdb_ids
                self.list = oscar_winners_tmdb_ids
            elif self.action == ('trakt_movies_mosts'):
                for item in (function(params['period'], params['duration'], page_no)): self.list.append(get_trakt_movie_id(item['movie']['ids']))
                self.new_page = {'mode': mode, 'action': self.action, 'period': params['period'], 'duration': params['duration'], 'new_page': str(page_no + 1), 'foldername': self.action}
            elif self.action == 'trakt_movies_related':
                self.sim_recom_name = params.get('sim_recom_name')
                self.sim_recom_tmdb = params.get('sim_recom_tmdb')
                self.sim_recom_imdb = params.get('sim_recom_imdb')
                data, total_pages = function(self.sim_recom_imdb, page_no)
                for item in data: self.list.append(get_trakt_movie_id(item['ids']))
                if total_pages > page_no: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'sim_recom_name': self.sim_recom_name, 'sim_recom_tmdb': self.sim_recom_tmdb, 'sim_recom_imdb': self.sim_recom_imdb, 'foldername': self.action, 'imdb_id': params.get('imdb_id')}
            elif self.action == 'tmdb_movies_genres':
                genre_id = params['genre_id'] if 'genre_id' in params else self.multiselect_genres(params.get('genre_list'))
                if not genre_id: return
                data = function(genre_id, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'genre_id': genre_id, 'foldername': genre_id}
            elif self.action == 'tmdb_movies_languages':
                language = params['language']
                if not language: return
                data = function(language, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'language': language, 'foldername': language}
            elif self.action == 'tmdb_movies_year':
                data = function(params['year'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'year': params.get('year'), 'foldername': params.get('year')}
            elif self.action == 'tmdb_movies_certifications':
                data = function(params['certification'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'certification': params.get('certification'), 'foldername': params.get('certification')}
            elif self.action in ('in_progress_movies', 'favourites_movies', 'subscriptions_movies', 'kodi_library_movies', 'watched_movies'):
                (var_module, import_function) = ('in_progress', 'in_progress_movie') if 'in_progress' in self.action else ('favourites', 'retrieve_favourites') if 'favourites' in self.action else ('subscriptions', 'retrieve_subscriptions') if 'subscriptions' in self.action else ('indicators_bookmarks', 'get_watched_items') if 'watched' in self.action else ('kodi_library', 'retrieve_kodi_library') if 'library' in self.action else ''
                try:
                    module = 'modules.%s' % (var_module)
                    function = getattr(importlib.import_module(module), import_function)
                except: pass
                if self.action == 'kodi_library_movies': self.id_type = 'imdb_id'
                data, total_pages = function('movie', page_no, letter)
                self.list = [i['media_id'] for i in data]
                if total_pages > 2: self.total_pages = total_pages
                if total_pages > page_no: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'foldername': self.action}
            elif self.action in ('tmdb_movies_similar', 'tmdb_movies_recommendations'):
                self.sim_recom_name = params.get('sim_recom_name')
                self.sim_recom_tmdb = params.get('sim_recom_tmdb')
                self.sim_recom_imdb = params.get('sim_recom_imdb')
                data = function(self.sim_recom_tmdb, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'sim_recom_name': self.sim_recom_name, 'sim_recom_tmdb': self.sim_recom_tmdb, 'sim_recom_imdb': self.sim_recom_imdb, 'foldername': self.action}
            elif self.action == 'trakt_recommendations':
                for item in function('movies'): self.list.append(get_trakt_movie_id(item['ids']))
            elif self.action == 'tmdb_popular_people':
                import os
                worker = False
                icon_directory = settings.get_theme()
                data = function(page_no)
                content_type = 'addons'
                fanart = __addon__.getAddonInfo('fanart')
                for item in data['results']:
                    cm = []
                    actor_poster = "http://image.tmdb.org/t/p/w185%s" % item['profile_path'] if item['profile_path'] else os.path.join(icon_directory, 'genre_family.png')
                    url_params = {'mode': 'people_search.main', 'actor_id': item['id'], 'actor_name': item['name'], 'actor_image': actor_poster.replace('w185', 'h632')}
                    url = build_url(url_params)
                    cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedactorinfo,id=%s)' % item['id']))
                    listitem = xbmcgui.ListItem(item['name'])
                    listitem.setArt({'icon': actor_poster, 'poster': actor_poster, 'thumb': actor_poster, 'fanart': fanart, 'banner': actor_poster})
                    listitem.addContextMenuItems(cm)
                    xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(int(data['page']) + 1), 'foldername': self.action}
            elif self.action  == 'tmdb_movies_search':
                try: from urllib import unquote
                except ImportError: from urllib.parse import unquote
                if params.get('query') == 'NA':
                    search_title = dialog.input("Search Fen", type=xbmcgui.INPUT_ALPHANUM)
                    search_name = unquote(search_title)
                else: search_name = unquote(params.get('query'))
                if not search_name: return
                data = function(search_name, page_no)
                total_pages = data['total_pages']
                if total_pages > page_no: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'query': search_name, 'foldername': search_name}
                self.list = [i['id'] for i in data['results']]
            if self.total_pages and not is_widget:
                url_params = {'mode': 'build_navigate_to_page', 'db_type': 'Movies', 'current_page': page_no, 'total_pages': self.total_pages, 'transfer_mode': mode, 'transfer_action': self.action, 'foldername': self.action, 'query': params.get('search_name', ''), 'actor_id': params.get('actor_id', '')}
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
        setView('view.movies', content_type)

    def build_movie_content(self):
        def _process(item):
            try:
                listitem = xbmcgui.ListItem()
                cm = []
                item_no = item['item_no']
                rootname = item['rootname']
                tmdb_id = item['tmdb_id']
                imdb_id = item['imdb_id']
                title = item['title']
                trailer = item['trailer']
                playcount = item['playcount']
                poster = item['poster']
                if use_animated:
                    if item.get('gif_poster', False):
                        item['use_animated_poster'] = True
                        poster = item['gif_poster']
                meta_json = json.dumps(item)
                resumetime = get_resumetime('movie', tmdb_id) 
                openinfo_params = {'mode': 'extended_info_open', 'db_type': 'movie', 'tmdb_id': tmdb_id}
                play_params = {'mode': 'play_media', 'vid_type': 'movie', 'query': rootname, 'tmdb_id': tmdb_id, 'meta': meta_json}
                url_params = openinfo_params if default_openinfo else play_params
                url = build_url(url_params)
                playback_params = {'mode': 'playback_menu', 'suggestion': rootname, 'list_name': list_name, 'play_params': json.dumps(url_params)}
                (state, action) = ('Watched', 'mark_as_watched') if playcount == 0 else ('Unwatched', 'mark_as_unwatched')
                watched_unwatched_params = {"mode": "mark_movie_as_watched_unwatched", "action": action, "media_id": tmdb_id, "meta_user_info": meta_user_info, "title": title, "year": item['year']}
                add_remove_params = {"mode": "build_add_to_remove_from_list", "media_type": "movie", "meta": meta_json, "orig_mode": self.action}
                sim_recom_params = {"mode": "similar_recommendations_choice", "db_type": "movies", 'sim_recom_name': rootname, "sim_recom_tmdb": tmdb_id, "sim_recom_imdb": imdb_id, "meta_user_info": meta_user_info}
                cm.append(("[B]Mark %s %s[/B]" % (state, watched_title),"XBMC.RunPlugin(%s)" % build_url(watched_unwatched_params)))
                cm.append(("[B]Options[/B]","XBMC.RunPlugin(%s)" % build_url(playback_params)))
                if default_openinfo: cm.append(("[B]Sources Search...[/B]",'XBMC.RunPlugin(%s)' % build_url(play_params)))
                cm.append(("[B]Add/Remove[/B]","XBMC.RunPlugin(%s)" % build_url(add_remove_params)))
                cm.append(("[B]Similar/Recommended[/B]","XBMC.RunPlugin(%s)" % build_url(sim_recom_params)))
                if self.action in ('trakt_movies_related', 'tmdb_movies_recommendations'):
                    sim_recom_title = 'Similar to' if self.action == 'trakt_movies_related' else 'Recommended based on'
                    export_sim_recom_params = {'mode': 'navigator.adjust_main_lists', 'method': 'add_sim_recom_external', 'end_mode': 'build_movie_list',
                                    'end_action': self.action, 'db_type': 'movie', 'sim_recom_name': '[B]Movies[/B] | %s %s' % (sim_recom_title, self.sim_recom_name),
                                    'sim_recom_tmdb': self.sim_recom_tmdb, 'sim_recom_imdb': self.sim_recom_imdb}
                    cm.append(("[B]Export %s List[/B]" % sim_recom_title.split(' ')[0], "XBMC.RunPlugin(%s)" % build_url(export_sim_recom_params)))
                if trailer:
                    (trailer_params, trailer_title) = ({'mode': 'play_trailer', 'url': trailer, 'all_trailers': json.dumps(item['all_trailers'])}, 'Choose Trailer') if (all_trailers and item.get('all_trailers', False)) else ({'mode': 'play_trailer', 'url': trailer}, 'Trailer')
                    cm.append(("[B]%s[/B]" % trailer_title,"XBMC.RunPlugin(%s)" % build_url(trailer_params)))
                if resumetime != '0': cm.append(("[B]Clear Progress[/B]", 'XBMC.RunPlugin(%s)' % build_url({"mode": "watched_unwatched_erase_bookmark", "db_type": "movie", "media_id": tmdb_id, "refresh": "true"})))
                if self.action == 'trakt_recommendations':
                    hide_recommended_params = {'mode': 'trakt.hide_recommendations', 'db_type': 'movies', 'imdb_id': imdb_id}
                    cm.append(("[B]Hide from Recommendations[/B]", "XBMC.RunPlugin(%s)" % build_url(hide_recommended_params)))
                cm.append(("[B]Read Reviews[/B]","XBMC.RunPlugin(%s)" % build_url({'mode': 'movie_reviews', 'rootname': rootname, 'tmdb_id': tmdb_id, 'poster': poster})))
                cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedinfo,id=%s)' % tmdb_id))
                cm.append(("[B]Exit Movie List[/B]","XBMC.Container.Refresh(%s)" % self.exit_list_params))
                listitem.setLabel(title)
                listitem.addContextMenuItems(cm)
                listitem.setCast(item['cast'])
                listitem.setUniqueIDs({'imdb': str(imdb_id), 'tmdb': str(tmdb_id)})
                listitem.setArt({'poster': poster, 'fanart': item['fanart'], 'icon': poster, 'banner': item['banner'], 'clearart': item['clearart'], 'clearlogo': item['clearlogo'], 'landscape': item['landscape'], 'discart': item['discart']})
                listitem.setProperty("resumetime", resumetime)
                if is_widget:
                    listitem.setProperty('fen_playback_menu_params', json.dumps(playback_params))
                    listitem.setProperty('fen_widget', 'true')
                    listitem.setProperty('fen_playcount', str(playcount))
                listitem.setInfo('Video', remove_unwanted_info_keys(item))
                if use_threading: item_list.append({'list_item': (url, listitem, False), 'item_position': item_no})
                else: xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=False)
            except: pass
        watched_indicators = settings.watched_indicators()
        all_trailers = settings.all_trailers()
        watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
        meta_user_info = json.dumps(self.meta_user_info)
        list_name = self.cache_page_string
        use_animated = tikimeta.use_animated_artwork()
        use_threading = settings.thread_main_menus()
        default_openinfo = True if settings.default_openinfo() in (1, 3) else False
        if use_threading:
            item_list = []
            threads = []
            for item in self.items: threads.append(Thread(target=_process, args=(item,)))
            [i.start() for i in threads]
            [i.join() for i in threads]
            item_list.sort(key=lambda k: k['item_position'])
            xbmcplugin.addDirectoryItems(__handle__, [i['list_item'] for i in item_list])
        else:
            for item in sorted(self.items, key=lambda k: k['item_no']): _process(item)

    def set_info(self, item_no, item):
        meta = tikimeta.movie_meta(self.id_type, item, self.meta_user_info)
        playcount, overlay = get_watched_status(self.watched_info, self.use_trakt, 'movie', meta['tmdb_id'])
        meta.update({'item_no': item_no, 'playcount': playcount, 'overlay': overlay})
        if not 'rootname' in meta: meta['rootname'] = '{0} ({1})'.format(meta['title'], meta['year'])
        self.items.append(meta)

    def worker(self):
        threads = []
        if not self.exit_list_params: self.exit_list_params = xbmc.getInfoLabel('Container.FolderPath')
        self.watched_indicators = settings.watched_indicators()
        self.all_trailers = settings.all_trailers()
        self.watched_info, self.use_trakt = get_watched_info_movie()
        self.meta_user_info = tikimeta.retrieve_user_info()
        window.clearProperty('fen_fanart_error')
        for item_position, item in enumerate(self.list): threads.append(Thread(target=self.set_info, args=(item_position, item)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        self.build_movie_content()

    def multiselect_genres(self, genre_list):
        import os
        dialog = xbmcgui.Dialog()
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
        if url_params['mode'] == 'build_navigate_to_page':
            listitem.addContextMenuItems([("[B]Switch Jump To Action[/B]","XBMC.RunPlugin(%s)" % build_url({'mode': 'toggle_jump_to'}))])
        xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=True)
