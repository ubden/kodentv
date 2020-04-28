import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import os
import re
import json
from threading import Thread
from apis.trakt_api import get_trakt_movie_id, get_trakt_tvshow_id
from modules.kodi_library import get_library_video
from modules.nav_utils import notification, close_all_dialog
from modules.utils import adjust_premiered_date, to_utf8, clean_file_name
import tikimeta
from modules import settings
from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
window = xbmcgui.Window(10000)

class Subscriptions:
    def __init__(self, db_type=None, tmdb_id=None, action=None, orig_mode=None):
        tikimeta.check_meta_database()
        self.db_type = db_type
        self.tmdb_id = tmdb_id #str
        self.action = action
        self.orig_mode = orig_mode
        self.meta_user_info = tikimeta.retrieve_user_info()
        if self.db_type:
            self.path = settings.movies_directory() if self.db_type == 'movie' else settings.tv_show_directory()
        self.add_release_date = settings.add_release_date()
        window.setProperty('fen_fanart_error', 'true')

    def add_remove(self, silent=False):
        self.add_remove_constants()
        if self.check_exists() and self.action == 'add':
            return notification('[B]%s[/B] already in Subscriptions' % self.rootname, 4500)
        self.add_remove_movie(silent) if self.db_type == 'movie' else self.add_remove_tvshow(silent)
        if self.orig_mode in ('subscriptions_tvshows', 'subscriptions_movies') and self.action == 'remove':
            xbmc.executebuiltin('Container.Refresh')

    def add_remove_movie(self, silent=False):
        if self.action == 'add':
            in_library = get_library_video('movie', self.title, self.year) if settings.skip_duplicates() else False
            if in_library: return
            self.make_folder()
            self.make_nfo()
            stream_file = self.create_movie_strm_files()
            params = to_utf8({'mode': 'play_media', 'library': 'True', 'query': self.rootname, 'poster': self.meta['poster'], 'year': self.year, 'plot': self.meta['plot'], 'title': self.title, 'tmdb_id': self.meta['tmdb_id'], 'vid_type':'movie'})
            self.make_stream(stream_file, params)
        elif self.action == 'remove':
            self.remove_folder()
        if not silent: notification(self.notify % self.rootname, 4500)

    def add_remove_tvshow(self, silent=False):
        if self.action == 'add':
            self.make_folder()
            self.make_nfo()
            self.create_tvshow_strm_files()
        elif self.action == 'remove':
            self.remove_folder()
        if not silent: notification(self.notify % self.rootname, 4500)

    def get_subscriptions(self):
        from modules.utils import read_from_file
        def _folders(folder):
            item_path = os.path.join(self.path, folder)
            contents = xbmcvfs.listdir(item_path)[1]
            for c in contents:
                if c.endswith('.nfo'): files_list.append((c, item_path))
        def _files(file, path):
            try:
                address = read_from_file(os.path.join(path, file))
                info = address.split('/')[-1].split('-', 1)
                tmdb_id = info[0]
                title = info[1].replace('-', ' ')
                subscription_list.append({'media_id': tmdb_id, 'title': title})
            except Exception as e:
                logger('get_subscriptions Exception', e)
                pass
        files_list = []
        subscription_list = []
        dirs, files = xbmcvfs.listdir(self.path)
        threads1 = []
        threads2 = []
        for item in dirs: threads1.append(Thread(target=_folders, args=(item,)))
        [i.start() for i in threads1]
        [i.join() for i in threads1]
        for item in files_list: threads2.append(Thread(target=_files, args=(item[0], item[1])))
        [i.start() for i in threads2]
        [i.join() for i in threads2]
        return subscription_list

    def clear_subscriptions(self, confirm=True, silent=False, db_type=None):
        if confirm:
            if not self.subscription_choice('Choose Subscriptions to Erase', 'Continuing will erase all your %s'): return
        self.db_type = self.choice[1] if not db_type else db_type
        self.path = settings.movies_directory() if self.db_type == 'movie' else settings.tv_show_directory()
        subscriptions = self.get_subscriptions()
        if len(subscriptions) == 0:
            return notification('%s Subscriptions is already Empty' % self.db_type.upper(), 4500)
        self.remove_folder(self.path)
        self.make_folder(self.path)
        if not silent: notification('%s Subscriptions has been Cleared' % self.db_type.upper(), 4500)

    def update_subscriptions(self, suppress_extras=False):
        from datetime import datetime, timedelta
        self.db_type = 'tvshow'
        self.action = 'add'
        self.path = settings.tv_show_directory()
        subscriptions = self.get_subscriptions()
        if not subscriptions:
            return notification('No TV Show Subscriptions to Update', 1200)
        close_all_dialog()
        bg_dialog = xbmcgui.DialogProgressBG()
        bg_dialog.create('Please Wait', 'Preparing Subscription Update...')
        for count, item in enumerate(subscriptions, 1):
            try:
                self.tmdb_id = item['media_id']
                self.add_remove_constants()
                self.add_remove_tvshow(silent=True)
                display = 'Fen Updating - [B][I]%s[/I][/B]' % self.rootname
                bg_dialog.update(int(float(count) / float(len(subscriptions)) * 100), 'Please Wait', '%s' % display)
                xbmc.sleep(300)
            except Exception as e:
                logger('update subscriptions error', e)
                logger('title', item['title'])

        if int(__addon__.getSetting('subsciptions.update_type')) == 0:
            hours = settings.subscription_timer()
            __addon__.setSetting('service_time', str(datetime.now() + timedelta(hours=hours)).split('.')[0])
        xbmc.sleep(500)
        bg_dialog.close()
        notification('Fen Subscriptions Updated', 4500)
        if settings.update_library_after_service() and not suppress_extras: xbmc.executebuiltin('UpdateLibrary(video)')

    def add_trakt_subscription_listitem(self, db_type, ids, count, total, path, dialog):
        try:
            get_ids = get_trakt_movie_id if db_type in ('movie', 'movies') else get_trakt_tvshow_id
            meta_action = tikimeta.movie_meta if db_type in ('movie', 'movies') else tikimeta.tvshow_meta
            tmdb_id = get_ids(ids)
            address_insert = 'movie' if db_type in ('movie', 'movies') else 'tv'
            meta = meta_action('tmdb_id', tmdb_id, self.meta_user_info)
            title = clean_file_name(meta['title'])
            year = meta['year'] if 'year' in meta else '0'
            rootname = '{0} ({1})'.format(title, year) if year != '0' else title
            folder = os.path.join(path, rootname + '/')
            nfo_filename = rootname + '.nfo' if db_type in ('movie', 'movies') else 'tvshow.nfo'
            nfo_filepath = os.path.join(folder, nfo_filename)
            nfo_content = "https://www.themoviedb.org/%s/%s-%s" % (address_insert, str(meta['tmdb_id']), title.lower().replace(' ', '-'))
            self.make_folder(folder)
            self.make_nfo(nfo_filepath, nfo_content)
            if db_type in ('movie', 'movies'):
                in_library = get_library_video('movie', title, year) if settings.skip_duplicates() else False
                if in_library: return
                stream_file = self.create_movie_strm_files(folder, rootname)
                params = to_utf8({'mode': 'play_media', 'library': 'True', 'query': rootname, 'poster': meta['poster'], 'year': year, 'plot': meta['plot'], 'title': title, 'tmdb_id': meta['tmdb_id'], 'vid_type':'movie'})
                self.make_stream(stream_file, params)
            else:
                self.create_tvshow_strm_files(meta, folder, tmdb_id, title, year)
            dialog.update(int(float(count) / float(total) * 100), '', 'Adding: [B]%s[/B]' % rootname)
        except Exception as e:
            logger('add_trakt_subscription_listitem Exception', e)
            pass

    def remove_trakt_subscription_listitem(self, db_type, media_id, count, total, path, dialog):
        try:
            meta_action = tikimeta.movie_meta if db_type in ('movie', 'movies') else tikimeta.tvshow_meta
            tmdb_id = media_id
            meta = meta_action('tmdb_id', tmdb_id, self.meta_user_info)
            title = clean_file_name(meta['title'])
            year = meta['year'] if 'year' in meta else ''
            rootname = '{0} ({1})'.format(title, year) if year else title
            folder = os.path.join(path, rootname + '/')
            self.remove_folder(folder)
            dialog.update(int(float(count) / float(total) * 100), 'Please Wait...', 'Removing: [B]%s[/B]' % rootname)
        except: pass

    def create_movie_strm_files(self, folder=None, rootname=None):
        if not folder: folder = self.folder
        if not rootname: rootname = self.rootname
        return os.path.join(folder, rootname + '.strm')

    def create_tvshow_strm_files(self, meta=None, folder=None, tmdb_id=None, title=None, year=None):
        if not meta: meta = self.meta
        if not folder: folder = self.folder
        if not tmdb_id: tmdb_id = self.tmdb_id
        if not title: title = self.title
        if not year: year = self.year
        adjust_hours = int(__addon__.getSetting('datetime.offset'))
        current_adjusted_date = settings.adjusted_datetime(dt=True)
        add_unknown_airdate = settings.subscriptions_add_unknown_airdate()
        skip_duplicates = settings.skip_duplicates()
        season_data = tikimeta.all_episodes_meta(meta['tmdb_id'], meta['tvdb_id'], meta['tvdb_summary']['airedSeasons'], meta['season_data'], self.meta_user_info)
        season_data = [i for i in season_data if not i['season_number'] == 0]
        for i in season_data:
            try:
                season_path = os.path.join(folder, 'Season ' + str(i['season_number']))
                self.make_folder(season_path)
                ep_data = i['episodes_data']
                for item in ep_data:
                    try:
                        airdate_unknown = False
                        plot = item['overview']
                        season = item['airedSeason'] if 'airedSeason' in item else item['season_number']
                        episode = item['airedEpisodeNumber'] if 'airedEpisodeNumber' in item else item['episode_number']
                        ep_name = item['episodeName'] if 'episodeName' in item else item['name']
                        premiered = item['firstAired'] if 'firstAired' in item else item['air_date']
                        in_library = get_library_video('episode', title, year, season, episode) if skip_duplicates else None
                        if not in_library:                                
                            try: episode_date, premiered = adjust_premiered_date(premiered, adjust_hours)
                            except: episode_date = None
                            if not episode_date:
                                if not add_unknown_airdate:
                                    continue
                                else:
                                    airdate_unknown = True
                            if not airdate_unknown:
                                if not current_adjusted_date >= episode_date:
                                    continue
                            display = "%s S%.2dE%.2d" % (title, int(season), int(episode))
                            stream_file = os.path.join(season_path, str(display) + '.strm')
                            params = to_utf8({'mode': 'play_media', 'library': 'True', 'query': title, 'year': year, 'plot': plot, 'poster': meta['poster'], 'season': season, 'episode': episode, 'ep_name': ep_name, 'premiered': premiered, 'tmdb_id': tmdb_id, 'vid_type':'episode'})
                            self.make_stream(stream_file, params)
                    except Exception as e:
                        logger('create_tvshow_strm_files season_data item section', e)
                        logger('meta', meta['search_title'])
            except Exception as e:
                logger('create_tvshow_strm_files season_data section', e)
                logger('meta', meta['search_title'])

    def make_folder(self, folder=None):
        folder = self.folder if not folder else folder
        xbmcvfs.mkdir(folder)

    def remove_folder(self, folder=None):
        folder = self.folder if not folder else folder
        xbmcvfs.rmdir(folder, True)
    
    def make_nfo(self, nfo_filepath=None, nfo_content=None):
        nfo_filepath = self.nfo_filepath if not nfo_filepath else nfo_filepath
        nfo_content = self.nfo_content if not nfo_content else nfo_content
        if not xbmcvfs.exists(nfo_filepath):
            nfo_file = xbmcvfs.File(nfo_filepath, 'w')
            nfo_file.write(nfo_content)
            nfo_file.close()

    def make_stream(self, stream_file, params):
        if not xbmcvfs.exists(stream_file):
            from modules.nav_utils import build_url
            file = xbmcvfs.File(stream_file, 'w')
            content = build_url(params)
            file.write(str(content))
            file.close()
            if self.add_release_date:
                try:
                    premiered = params['premiered']
                    adjusted_time = settings.date_to_timestamp(premiered)
                    os.utime(stream_file, (adjusted_time,adjusted_time))
                except Exception as e:
                    logger('make_stream Exception', e)
                    logger('stream_file', params.get('query'))
                    pass

    def check_exists(self):
        tmdb_ids = [i['media_id'] for i in self.get_subscriptions()]
        if str(self.meta['tmdb_id']) in tmdb_ids: return True
        else: return False

    def add_remove_constants(self):
        meta_action = tikimeta.movie_meta if self.db_type == 'movie' else tikimeta.tvshow_meta
        address_insert = 'movie' if self.db_type == 'movie' else 'tv'
        self.meta = meta_action('tmdb_id', self.tmdb_id, self.meta_user_info)
        self.title = clean_file_name(self.meta['title'])
        self.year = self.meta['year'] if 'year' in self.meta else ''
        self.rootname = '{0} ({1})'.format(self.title, self.year) if self.year else self.title
        self.folder = os.path.join(self.path, self.rootname + '/')
        self.nfo_filename = self.rootname + '.nfo' if self.db_type == 'movie' else 'tvshow.nfo'
        self.nfo_filepath = os.path.join(self.folder, self.nfo_filename)
        self.nfo_content = "https://www.themoviedb.org/%s/%s-%s" % (address_insert, str(self.meta['tmdb_id']), self.title.lower().replace(' ', '-'))
        self.notify = '[B]%s[/B] added to Subscriptions' if self.action == 'add' else '[B]%s[/B] removed from Subscriptions'

    def subscription_choice(self, heading, message):
        sl = [('Movie Subscriptions', 'movie'), ('TV Show Subscriptions', 'tvshow')]
        choice = xbmcgui.Dialog().select(heading, [i[0] for i in sl])
        if choice < 0: return
        confirm = xbmcgui.Dialog().yesno('Are you sure?', message % sl[choice][0])
        if not confirm: return False
        self.choice = sl[choice]
        return True

def retrieve_subscriptions(db_type, page_no, letter):
    from modules.nav_utils import paginate_list
    from modules.utils import title_key
    paginate = settings.paginate()
    limit = settings.page_limit()
    data = Subscriptions(db_type).get_subscriptions()
    original_list = sorted(data, key=lambda k: title_key(k['title']))
    if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    else: final_list, total_pages = original_list, 1
    return final_list, total_pages

def subscriptions_add_list(db_type):
    from modules.trakt_cache import clear_trakt_list_data
    from apis.trakt_api import get_trakt_list_selection
    from modules.nav_utils import show_busy_dialog, hide_busy_dialog, open_settings
    movie_subscriptions = Subscriptions('movie')
    tvshow_subscriptions = Subscriptions('tvshow')
    variables = ('Movies', 'movies', 'movie', 'trakt.subscriptions_movie', 'trakt.subscriptions_movie_display', '8.14', movie_subscriptions) if db_type == 'movie' else ('TV Shows', 'shows', 'show', 'trakt.subscriptions_show', 'trakt.subscriptions_show_display', '8.15', tvshow_subscriptions)
    dialog_display = variables[0]
    trakt_list_type = variables[1]
    trakt_dbtype = variables[2]
    main_setting = variables[3]
    display_setting = variables[4]
    open_setting = variables[5]
    subscription_function = variables[6]
    clear_library, cancelled, supplied_list = (False for _ in range(3))
    path = settings.movies_directory() if db_type == 'movie' else settings.tv_show_directory()
    if xbmcgui.Dialog().yesno('Fen Subscriptions','Are you sure you have set your Fen [B]%s[/B] Subscription Folder as a Source for the Kodi Library?' % db_type.upper(), '', '', 'Already Done', 'I\'ll Do It Now'):
        return xbmc.executebuiltin('ActivateWindow(videos,files,return)')
    for i in ('my_lists', 'liked_lists'):
        try: clear_trakt_list_data(i)
        except: pass
    trakt_list = get_trakt_list_selection(list_choice='subscriptions')
    if not trakt_list: return open_settings(open_setting)
    __addon__.setSetting(main_setting, json.dumps(trakt_list))
    __addon__.setSetting(display_setting, trakt_list['name'])
    if trakt_list['name'].lower() == 'none': return open_settings(open_setting)
    if not xbmcgui.Dialog().yesno('Are you sure?','Fen will add all [B]%s[/B] from [B]%s[/B] to your Fen Subscriptions, and monitor this list for changes. Do you wish to continue?' % (dialog_display, trakt_list['name'])):
        __addon__.setSetting(main_setting, '')
        __addon__.setSetting(display_setting, 'none')
        return open_settings(open_setting)
    current_subscriptions = subscription_function.get_subscriptions()
    if len(current_subscriptions) > 0:
        if not xbmcgui.Dialog().yesno('Current Subscriptions Found!','You have items in your [B]%s[/B] Subscription. Fen will delete these before continuing (may take some time). Do you wish to continue?' % (dialog_display)):
            return open_settings(open_setting)
        clear_library = True
        show_busy_dialog()
        subscription_function.clear_subscriptions(confirm=False, silent=True, db_type=db_type)
        hide_busy_dialog()
    dialog = xbmcgui.DialogProgressBG()
    dialog.create('Please Wait', 'Preparing Trakt List Info...')
    if trakt_list['name'] in ('Collection', 'Watchlist'):
        from modules.trakt_cache import clear_trakt_collection_watchlist_data
        from apis.trakt_api import trakt_fetch_collection_watchlist
        list_contents = trakt_fetch_collection_watchlist(trakt_list['name'].lower(), trakt_list_type)
    else:
        from apis.trakt_api import get_trakt_list_contents
        from modules.trakt_cache import clear_trakt_list_contents_data
        list_contents = get_trakt_list_contents(trakt_list['user'], trakt_list['slug'])
        list_contents = [{'media_ids': i[trakt_dbtype]['ids'], 'title': i[trakt_dbtype]['title']} for i in list_contents if i['type'] == trakt_dbtype]
    for i in list_contents:
        if i['media_ids']['tmdb'] == None:
            i['media_ids']['tmdb'] = get_trakt_tvshow_id(i['media_ids'])
    threads = []
    list_length = len(list_contents)
    for count, item in enumerate(list_contents, 1):
        subscription_function.add_trakt_subscription_listitem(db_type, item['media_ids'], count, list_length, path, dialog)
    dialog.close()
    end_dialog = 'Operation Cancelled! Not all items from [B]%s[/B] were added.' if cancelled else '[B]%s[/B] added to Subscriptions.'
    xbmcgui.Dialog().ok('Fen Subscriptions', end_dialog % trakt_list['name'])
    if clear_library:
        if xbmcgui.Dialog().yesno('Fen Subscriptions','Do you wish to clear Kodi\'s Library of your previous Subscription items?'):
            import time
            xbmc.executebuiltin('CleanLibrary(video)')
            time.sleep(3)
            while xbmc.getCondVisibility("Window.IsVisible(ProgressDialog)"):
                time.sleep(1)
    if xbmcgui.Dialog().yesno('Fen Subscriptions','Do you wish to scan your new Subscription list into Kodi\'s Library?'):
        xbmc.executebuiltin('UpdateLibrary(video)')
    # return open_settings(open_setting)

def subscriptions_update_list():
    def _get_trakt_list_contents(db_type, item):
        append_list = trakt_movie_list_contents if db_type in ('movie', 'movies') else trakt_tvshow_list_contents
        try:
            if item['name'].lower() == 'none': return append_list
            if item['name'] in ('Collection', 'Watchlist'):
                from modules.trakt_cache import clear_trakt_collection_watchlist_data
                from apis.trakt_api import trakt_fetch_collection_watchlist
                clear_trakt_collection_watchlist_data(item['name'].lower(), db_type)
                list_contents = trakt_fetch_collection_watchlist(item['name'].lower(), db_type)
            else:
                from apis.trakt_api import get_trakt_list_contents
                from modules.trakt_cache import clear_trakt_list_contents_data
                trakt_dbtype = 'movie' if db_type in ('movie', 'movies') else 'show'
                clear_trakt_list_contents_data(user=item['user'], list_slug=item['slug'])
                list_contents = get_trakt_list_contents(item['user'], item['slug'])
                list_contents = [{'media_ids': i[trakt_dbtype]['ids'], 'title': i[trakt_dbtype]['title']} for i in list_contents if i['type'] == trakt_dbtype]
            append_list.extend(list_contents)
        except: return append_list
    close_all_dialog()
    dialog = xbmcgui.DialogProgressBG()
    dialog.create('Please Wait', 'Preparing for Subscription Update...')
    trakt_dbtype = ('movie', 'show')
    main_setting = ('trakt.subscriptions_movie', 'trakt.subscriptions_show')
    display_setting = ('trakt.subscriptions_movie_display', 'trakt.subscriptions_show_display')
    trakt_movie_list_contents = []
    trakt_tvshow_list_contents = []
    update_movies, update_tvshows, movies_added, tvshows_added, movies_removed, tvshows_removed = (False for _ in range(6))
    movie_subscriptions_object = Subscriptions('movie')
    tvshow_subscriptions_object = Subscriptions('tvshow')
    movie_subscriptions = movie_subscriptions_object.get_subscriptions()
    tvshow_subscriptions = tvshow_subscriptions_object.get_subscriptions()
    try: movie_list = json.loads(__addon__.getSetting(main_setting[0]))
    except: movie_list = []
    try: tvshow_list = json.loads(__addon__.getSetting(main_setting[1]))
    except: tvshow_list = []
    movie_list_name = __addon__.getSetting(display_setting[0])
    tvshow_list_name = __addon__.getSetting(display_setting[1])
    for i in [('movies', movie_list), ('shows', tvshow_list)]: _get_trakt_list_contents(i[0], i[1])
    trakt_movie_compare_contents = sorted([str(get_trakt_movie_id(i['media_ids'])) for i in trakt_movie_list_contents])
    subscriptions_movie_compare_contents = sorted([str(i['media_id']) for i in movie_subscriptions])
    trakt_tvshow_compare_contents = sorted([str(get_trakt_tvshow_id(i['media_ids'])) for i in trakt_tvshow_list_contents])
    subscriptions_tvshow_compare_contents = sorted([str(i['media_id']) for i in tvshow_subscriptions])
    if not trakt_movie_compare_contents == subscriptions_movie_compare_contents:
        if len(trakt_movie_compare_contents) > 0: update_movies = True
    if not trakt_tvshow_compare_contents == subscriptions_tvshow_compare_contents:
        if len(trakt_tvshow_compare_contents) > 0: update_tvshows = True
    if any([update_movies, update_tvshows]):
        def _process_additions(db_type, ids, count, list_length, path, dialog):
            if db_type in ('movie', 'movies'): movie_subscriptions_object.add_trakt_subscription_listitem(db_type, ids, count, list_length, path, dialog)
            else: tvshow_subscriptions_object.add_trakt_subscription_listitem(db_type, ids, count, list_length, path, dialog)
        def _process_removals(db_type, ids, count, list_length, path, dialog):
            if db_type in ('movie', 'movies'): movie_subscriptions_object.remove_trakt_subscription_listitem(db_type, ids, count, list_length, path, dialog)
            else: tvshow_subscriptions_object.remove_trakt_subscription_listitem(db_type, ids, count, list_length, path, dialog)
        def _process_additions_removals(db_type, action, list_contents):
            function = _process_additions if action == 'add' else _process_removals
            media_id_key = 'media_ids' if action == 'add' else 'media_id'
            dialog_db = '[B]Movies[/B]' if db_type in ('movie', 'movies') else '[B]TV Shows[/B]'
            dialog_line2 = 'Adding [B]%s[/B] %s' if action == 'add' else 'Removing [B]%s[/B] %s'
            path = settings.movies_directory() if db_type in ('movie', 'movies') else settings.tv_show_directory()
            threads = []
            list_length = len(list_contents)
            dialog.update(0, dialog_db, dialog_line2 % (list_length, dialog_db))
            for count, item in enumerate(list_contents, 1):
                function(db_type, item[media_id_key], count, list_length, path, dialog)
        if update_movies:
            add_to_subscriptions = [i for i in trakt_movie_compare_contents if not i in subscriptions_movie_compare_contents]
            remove_from_subscriptions = [i for i in subscriptions_movie_compare_contents if not i in trakt_movie_compare_contents]
            if len(add_to_subscriptions) > 0:
                movies_added = True
                list_contents = [i for i in trakt_movie_list_contents if str(i['media_ids']['tmdb']) in add_to_subscriptions]
                _process_additions_removals('movies', 'add', list_contents)
            xbmc.sleep(1500)
            if len(remove_from_subscriptions) > 0:
                movies_removed = True
                list_contents = [i for i in movie_subscriptions if str(i['media_id']) in remove_from_subscriptions]
                _process_additions_removals('movies', 'remove', list_contents)
        if update_tvshows:
            add_to_subscriptions = [i for i in trakt_tvshow_compare_contents if not i in subscriptions_tvshow_compare_contents]
            remove_from_subscriptions = [i for i in subscriptions_tvshow_compare_contents if not i in trakt_tvshow_compare_contents]
            if len(add_to_subscriptions) > 0:
                tvshows_added = True
                list_contents = [i for i in trakt_tvshow_list_contents if str(i['media_ids']['tmdb']) in add_to_subscriptions]
                _process_additions_removals('tvshows', 'add', list_contents)
            xbmc.sleep(1500)
            if len(remove_from_subscriptions) > 0:
                tvshows_removed = True
                list_contents = [i for i in tvshow_subscriptions if str(i['media_id']) in remove_from_subscriptions]
                _process_additions_removals('tvshows', 'remove', list_contents)
    dialog.update(100, 'Please Wait..', 'Finished Syncing Subscriptions')
    xbmc.sleep(1500)
    dialog.close()
    tvshow_subscriptions_object.update_subscriptions(suppress_extras=True)
    if settings.clean_library_after_service():
        if any([movies_removed, tvshows_removed]):
            import time
            xbmc.executebuiltin('CleanLibrary(video)')
            time.sleep(3)
            while xbmc.getCondVisibility("Window.IsVisible(ProgressDialog)"):
                time.sleep(1)
        else:
            notification('Nothing Removed. Skipping Clean', 4500)
    if settings.update_library_after_service():
        return xbmc.executebuiltin('UpdateLibrary(video)')
    return
