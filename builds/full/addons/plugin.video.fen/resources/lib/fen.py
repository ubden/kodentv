import sys
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
# from modules.utils import logger

params = dict(parse_qsl(sys.argv[2].replace('?','')))
mode = params.get('mode')

if not mode or 'navigator.' in mode:
    from indexers.navigator import Navigator
    if not mode or mode == 'navigator.main': Navigator(params.get('action', 'RootList')).main_lists()
    elif mode == 'navigator.build_shortcut_folder_lists': Navigator(params.get('action')).build_shortcut_folder_lists()
    else: exec('Navigator().%s()' % mode.split('.')[1])
elif 'discover.' in mode:
    from indexers.discover import Discover
    db_type = params['db_type'] if 'db_type' in params else None
    sim_recom_key = params.get('key', None)
    if sim_recom_key: action_code = 'Discover("%s").%s("%s")' % (db_type, mode.split('.')[1], sim_recom_key)
    else: action_code = 'Discover("%s").%s()' % (db_type, mode.split('.')[1])
    action_object = compile(action_code, 'discover_string', 'exec')
    exec(action_object)
elif 'furk.' in mode:
    if mode == 'furk.browse_packs':
        from modules.sources import Sources
        Sources().furkTFile(params['file_name'], params['file_id'])
    else:
        exec('from indexers.furk import %s as function' % mode.split('.')[1])
        function()
elif 'easynews.' in mode:
    exec('from indexers.easynews import %s as function' % mode.split('.')[1])
    function()
elif 'trakt.' in mode or 'trakt_' in mode:
    if 'trakt.' in mode:
        exec('from apis.trakt_api import %s as function' % mode.split('.')[1])
        function()
    else:
        if mode == 'trakt_sync_watched_to_fen':
            from ast import literal_eval
            from apis.trakt_api import sync_watched_trakt_to_fen
            sync_watched_trakt_to_fen(literal_eval(params['refresh']))
        elif mode == 'hide_unhide_trakt_items':
            from apis.trakt_api import hide_unhide_trakt_items
            hide_unhide_trakt_items(params['action'], params['media_type'], params['media_id'], params['section'])
        elif mode == 'trakt_authenticate':
            from apis.trakt_api import trakt_authenticate
            trakt_authenticate()
        elif mode == 'trakt_remove_authentication':
            from apis.trakt_api import trakt_remove_authentication
            trakt_remove_authentication()
elif 'build' in mode or '_next_episode' in mode:
    if mode == 'build_movie_list':
        from indexers.movies import Movies
        Movies(action=params.get('action')).fetch_list()
    elif mode == 'build_tvshow_list':
        from indexers.tvshows import TVShows
        TVShows(action=params.get('action')).fetch_list()
    elif mode == 'build_season_list':
        from indexers.tvshows import build_season_list
        build_season_list()
    elif mode == 'build_episode_list':
        from indexers.tvshows import build_episode_list
        build_episode_list()
    elif mode == 'build_next_episode':
        from modules.next_episode import build_next_episode
        build_next_episode()
    elif mode == 'build_in_progress_episode':
        from modules.in_progress import build_in_progress_episode
        build_in_progress_episode()
    elif mode == 'build_add_to_remove_from_list':
        from modules.utils import build_add_to_remove_from_list
        build_add_to_remove_from_list()
    elif mode == 'build_navigate_to_page':
        from modules.nav_utils import build_navigate_to_page
        build_navigate_to_page()
    elif mode == 'build_next_episode_manager':
        from modules.next_episode import build_next_episode_manager
        build_next_episode_manager()
    elif mode == 'build_kodi_library_recently_added':
        from modules.kodi_library import build_kodi_library_recently_added
        build_kodi_library_recently_added(params['db_type'])
    elif mode == 'add_next_episode_unwatched':
        from modules.next_episode import add_next_episode_unwatched
        add_next_episode_unwatched()
    elif mode == 'add_to_remove_from_next_episode_excludes':
        from modules.next_episode import add_to_remove_from_next_episode_excludes
        add_to_remove_from_next_episode_excludes()
elif '_play' in mode or 'play_' in mode and not 'autoplay' in mode:
    from ast import literal_eval
    if mode == 'play_media':
        from modules.sources import Sources
        Sources().playback_prep(params.get('vid_type'), params.get('tmdb_id'), params.get('query'), params.get('tvshowtitle'), params.get('season'),
                                params.get('episode'), params.get('ep_name'), params.get('plot'), params.get('meta'),
                                literal_eval(params.get('library', 'False')), params.get('background'), literal_eval(params.get('autoplay', 'None')))
    elif mode == 'play_display_results':
        from modules.sources import Sources
        Sources().display_results(params.get('page_no', None), params.get('previous_nav', None))
    elif mode == 'play_return_from_pagination':
        from modules.sources import Sources
        Sources().return_from_pagination(params['previous_nav'])
    elif mode == 'play_file':
        from modules.sources import Sources
        Sources().play_file(params['title'], params['source'])
    elif mode == 'play_auto':
        from modules.sources import Sources
        Sources().play_auto()
    elif mode == 'play_auto_nextep':
        from modules.sources import Sources
        Sources().play_auto_nextep()
    elif mode == 'media_play':
        from modules.player import FenPlayer
        FenPlayer().run()
    elif mode == 'play_trailer':
        from modules.nav_utils import play_trailer
        play_trailer(params.get('url'), params.get('all_trailers', []))
elif 'choice' in mode:
    if mode == 'scraper_color_choice':
        from modules.utils import scraper_color_choice
        scraper_color_choice()
    elif mode == 'external_color_choice':
        from modules.utils import external_color_choice
        external_color_choice()
    elif mode == 'next_episode_color_choice':
        from modules.next_episode import next_episode_color_choice
        next_episode_color_choice()
    elif mode == 'next_episode_options_choice':
        from modules.next_episode import next_episode_options_choice
        next_episode_options_choice()
    elif mode == 'next_episode_context_choice':
        from modules.next_episode import next_episode_context_choice
        next_episode_context_choice()
    elif mode == 'unaired_episode_color_choice':
        from modules.utils import unaired_episode_color_choice
        unaired_episode_color_choice()
    elif mode == 'scraper_dialog_color_choice':
        from modules.utils import scraper_dialog_color_choice
        scraper_dialog_color_choice()
    elif mode == 'scraper_quality_color_choice':
        from modules.utils import scraper_quality_color_choice
        scraper_quality_color_choice()
    elif mode == 'similar_recommendations_choice':
        from modules.nav_utils import similar_recommendations_choice
        similar_recommendations_choice()
    elif mode == 'folder_sources_choice':
        from modules.utils import folder_sources_choice
        folder_sources_choice()
    elif mode == 'internal_scrapers_order_choice':
        from modules.utils import internal_scrapers_order_choice
        internal_scrapers_order_choice()
elif 'favourites' in mode:
    if mode == 'my_furk_audio_favourites':
        from indexers.furk import my_furk_audio_favourites
        my_furk_audio_favourites()
    else:
        from modules.favourites import Favourites
        exec('Favourites().%s()' % mode)
elif 'subscriptions' in mode:
    from modules.subscriptions import Subscriptions
    if mode == 'subscriptions_add_remove':
        Subscriptions(params.get('db_type'), params.get('tmdb_id'), params.get('action'), params.get('orig_mode')).add_remove()
    elif mode == 'subscriptions_add_list':
        from modules.subscriptions import subscriptions_add_list
        subscriptions_add_list(params.get('db_type'))
    elif mode == 'subscriptions_update_interval':
        from modules.utils import subscriptions_update_interval
        subscriptions_update_interval()
    elif mode == 'update_subscriptions':
        from modules.settings import trakt_list_subscriptions
        if trakt_list_subscriptions():
            from modules.subscriptions import subscriptions_update_list
            subscriptions_update_list()
        else:
            exec('Subscriptions().%s()' % mode)
    else:
        exec('Subscriptions().%s()' % mode)
elif 'watched_unwatched' in mode:
    if mode == 'mark_as_watched_unwatched':
        from modules.indicators_bookmarks import mark_as_watched_unwatched
        mark_as_watched_unwatched()
    elif mode == 'mark_movie_as_watched_unwatched':
        from modules.indicators_bookmarks import mark_movie_as_watched_unwatched
        mark_movie_as_watched_unwatched()
    elif mode == 'mark_tv_show_as_watched_unwatched':
        from modules.indicators_bookmarks import mark_tv_show_as_watched_unwatched
        mark_tv_show_as_watched_unwatched()
    elif mode == 'mark_season_as_watched_unwatched':
        from modules.indicators_bookmarks import mark_season_as_watched_unwatched
        mark_season_as_watched_unwatched()
    elif mode == 'mark_episode_as_watched_unwatched':
        from modules.indicators_bookmarks import mark_episode_as_watched_unwatched
        mark_episode_as_watched_unwatched()
    elif mode == 'watched_unwatched_erase_bookmark':
        from modules.indicators_bookmarks import erase_bookmark
        erase_bookmark(params.get('db_type'), params.get('media_id'), params.get('season', ''), params.get('episode', ''), params.get('refresh', 'false'))
elif 'external_scrapers_' in mode:
    if mode == 'external_scrapers_disable':
        from modules.external_source_utils import external_scrapers_disable
        external_scrapers_disable()
    elif mode == 'external_scrapers_reset_stats':
        from modules.external_source_utils import external_scrapers_reset_stats
        external_scrapers_reset_stats()
    elif mode == 'external_scrapers_toggle_all':
        from modules.external_source_utils import toggle_all
        toggle_all(params.get('folder'), params.get('setting'))
    elif mode == 'external_scrapers_enable_disable_specific_all':
        from modules.external_source_utils import enable_disable_specific_all
        enable_disable_specific_all(params.get('folder'))
elif 'toggle' in mode:
    if mode == 'toggle_setting':
        from modules.nav_utils import toggle_setting
        toggle_setting()
    elif mode == 'toggle_jump_to':
        from modules.utils import toggle_jump_to
        toggle_jump_to()
    elif mode == 'toggle_provider':
        from modules.utils import toggle_provider
        toggle_provider()
elif 'history' in mode:
    if mode == 'search_history':
        from modules.history import search_history
        search_history()
    elif mode == 'clear_search_history':
        from modules.history import clear_search_history
        clear_search_history()
    elif mode == 'remove_from_history':
        from modules.history import remove_from_history
        remove_from_history()
elif 'real_debrid' in mode:
    if mode == 'real_debrid.rd_torrent_cloud':
        from indexers.real_debrid import rd_torrent_cloud
        rd_torrent_cloud()
    if mode == 'real_debrid.rd_downloads':
        from indexers.real_debrid import rd_downloads
        rd_downloads()
    elif mode == 'real_debrid.browse_rd_cloud':
        from indexers.real_debrid import browse_rd_cloud
        browse_rd_cloud(params['id'])
    elif mode == 'real_debrid.resolve_rd':
        from indexers.real_debrid import resolve_rd
        resolve_rd(params['url'])
    elif mode == 'real_debrid.rd_account_info':
        from indexers.real_debrid import rd_account_info
        rd_account_info()
    elif mode == 'real_debrid.authenticate':
        from apis.real_debrid_api import RealDebridAPI
        RealDebridAPI().auth()
    elif mode == 'real_debrid.authenticate_revoke':
        from apis.real_debrid_api import RealDebridAPI
        RealDebridAPI().revoke_auth()
    elif mode == 'real_debrid.delete_download_link':
        from indexers.real_debrid import delete_download_link
        delete_download_link(params['download_id'])
elif 'premiumize' in mode:
    if mode == 'premiumize.pm_torrent_cloud':
        from indexers.premiumize import pm_torrent_cloud
        pm_torrent_cloud(params.get('id', None), params.get('folder_name', None))
    elif mode == 'premiumize.pm_transfers':
        from indexers.premiumize import pm_transfers
        pm_transfers()
    elif mode == 'premiumize.pm_account_info':
        from indexers.premiumize import pm_account_info
        pm_account_info()
    elif mode == 'premiumize.rename':
        from indexers.premiumize import pm_rename
        pm_rename(params.get('file_type'), params.get('id'), params.get('name'))
    elif mode == 'premiumize.authenticate':
        from apis.premiumize_api import PremiumizeAPI
        PremiumizeAPI().auth()
    elif mode == 'premiumize.authenticate_revoke':
        from apis.premiumize_api import PremiumizeAPI
        PremiumizeAPI().revoke_auth()
elif 'alldebrid' in mode:
    if mode == 'alldebrid.ad_torrent_cloud':
        from indexers.alldebrid import ad_torrent_cloud
        ad_torrent_cloud(params.get('id', None))
    elif mode == 'alldebrid.browse_ad_cloud':
        from indexers.alldebrid import browse_ad_cloud
        browse_ad_cloud(params['folder'])
    elif mode == 'alldebrid.resolve_ad':
        from indexers.alldebrid import resolve_ad
        resolve_ad(params['url'])
    elif mode == 'alldebrid.ad_account_info':
        from indexers.alldebrid import ad_account_info
        ad_account_info()
    elif mode == 'alldebrid.authenticate':
        from apis.alldebrid_api import AllDebridAPI
        AllDebridAPI().auth()
    elif mode == 'alldebrid.authenticate_revoke':
        from apis.alldebrid_api import AllDebridAPI
        AllDebridAPI().revoke_auth()
elif 'people_search' in mode:
    from indexers.people import People
    actor_id = params.get('actor_id', 'None')
    actor_name = params.get('actor_name', 'None')
    actor_image = params.get('actor_image', 'None')
    if 'media_results' in mode:
        media_type = params.get('media_type')
        page_no = int(params.get('new_page', '1'))
        letter = params.get('new_letter', 'None')
        People((actor_id, actor_name, actor_image)).media_results(media_type, page_no, letter)
    else:
        action_code = 'People(%s).%s()' % ((actor_id, actor_name, actor_image), mode.split('.')[1])
        action_object = compile(action_code, 'people_search_string', 'exec')
        exec(action_object)
elif '_settings' in mode:
    if mode == 'open_settings':
        from modules.nav_utils import open_settings
        open_settings(params.get('query'))
    elif mode == 'backup_settings':
        from modules.nav_utils import backup_settings
        backup_settings()
    elif mode == 'restore_settings':
        from modules.nav_utils import restore_settings
        restore_settings()
    elif mode == 'open_ext_settings':
        from modules.utils import open_ext_settings
        open_ext_settings(params.get("addon"))
    elif mode == 'clean_settings':
        from modules.nav_utils import clean_settings
        clean_settings()
    elif mode == 'switch_settings':
        from modules.utils import switch_settings
        switch_settings()
    elif mode == 'resolveurl_settings':
        import resolveurl
        resolveurl.display_settings()
    elif mode == 'external_settings':
        from modules.utils import open_ext_settings
        open_ext_settings(params['ext_addon'])
elif 'container_' in mode:
    if mode == 'container_update':
        from modules.nav_utils import container_update
        container_update()
    elif mode == 'container_refresh':
        from modules.nav_utils import container_refresh
        container_refresh()
elif '_cache' in mode:
    if mode == 'refresh_cached_data':
        from modules.nav_utils import refresh_cached_data
        refresh_cached_data()
    elif mode == 'clear_cache':
        from modules.nav_utils import clear_cache
        clear_cache(params.get('cache'))
    elif mode == 'clear_all_cache':
        from modules.nav_utils import clear_all_cache
        clear_all_cache()
##EXTRA MODES##
elif mode == 'link_folders':
    from modules.nav_utils import link_folders
    link_folders(params['service'], params['folder_name'], params['action'])
elif mode == 'extended_info_open':
    from modules.nav_utils import extended_info_open
    extended_info_open(params.get('db_type'), params.get('tmdb_id'))
elif mode == 'show_image':
    from modules.nav_utils import show_image
    show_image()
elif mode == 'show_bio':
    from modules.nav_utils import show_bio
    show_bio()
elif mode == 'set_quality':
    from modules.utils import set_quality
    set_quality()
elif mode == 'playback_menu':
    from modules.utils import playback_menu
    playback_menu(params.get('from_results', None), params.get('suggestion', None), params.get('list_name', None), params.get('play_params', None))
elif mode == 'playback_kodi_library_menu':
    from modules.utils import playback_kodi_library_menu
    playback_kodi_library_menu()
elif mode == 'show_text':
    from modules.nav_utils import show_text
    show_text()
elif mode == 'movie_reviews':
    from modules.nav_utils import movie_reviews
    movie_reviews(params['tmdb_id'], params['rootname'], params['poster'])
elif mode == 'settings_layout':
    from modules.nav_utils import settings_layout
    settings_layout(params.get('settings_type', None))
elif mode == 'download_file':
    from modules.nav_utils import show_busy_dialog
    from modules import downloader
    show_busy_dialog()
    if params.get('db_type') in ('furk_file', 'easynews_file', 'realdebrid_direct_file', 'archive', 'audio'):
        downloader.download(params.get('url'))
    elif params.get('db_type') == 'realdebrid_file':
        from indexers.real_debrid import resolve_rd
        downloader.download(resolve_rd(params.get('url'), False))
    elif params.get('db_type') == 'premiumize_file':
        from apis.premiumize_api import PremiumizeAPI
        downloader.download(PremiumizeAPI().add_headers_to_url(params.get('url')))
    elif params.get('db_type') == 'alldebrid_file':
        from indexers.alldebrid import resolve_ad
        downloader.download(resolve_ad(params.get('url'), False))
    else:
        import json
        from modules import sources
        downloader.download(sources.Sources().resolve_sources(json.loads(params.get('source'))[0]))

