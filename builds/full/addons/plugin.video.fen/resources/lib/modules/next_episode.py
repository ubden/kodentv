import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import sys, os
import json
from datetime import date
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
import _strptime  # fix bug in python import
from threading import Thread
from modules.nav_utils import build_url, setView, remove_unwanted_info_keys, notification
from modules.utils import jsondate_to_datetime
from apis.trakt_api import sync_watched_trakt_to_fen, get_trakt_tvshow_id
from modules.trakt_cache import clear_all_trakt_cache_data
from indexers.tvshows import build_episode
from modules import settings
from tikimeta import tvshow_meta, all_episodes_meta, retrieve_user_info, check_meta_database
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__handle__ = int(sys.argv[1])
window = xbmcgui.Window(10000)

WATCHED_DB = os.path.join(__addon_profile__, "watched_status.db")

result = []

def build_next_episode():
    from modules.indicators_bookmarks import get_watched_info_tv
    def _process_eps(item):
        try:
            meta = tvshow_meta('tmdb_id', item['tmdb_id'], meta_user_info)
            include_unaired = nextep_settings['include_unaired']
            season = item['season']
            episode = item['episode']
            unwatched = item.get('unwatched', False)
            seasons_data = all_episodes_meta(meta['tmdb_id'], meta['tvdb_id'], meta['tvdb_summary']['airedSeasons'], meta['season_data'], meta_user_info)
            curr_season_data = [i for i in seasons_data if i['season_number'] == season][0]
            season = season if episode < curr_season_data['episode_count'] else season + 1
            episode = episode + 1 if episode < curr_season_data['episode_count'] else 1
            if settings.watched_indicators() in (1, 2):
                resformat = "%Y-%m-%dT%H:%M:%S.%fZ"
                curr_last_played = item.get('last_played', '2000-01-01T00:00:00.000Z')
            else:
                resformat = "%Y-%m-%d %H:%M:%S"
                curr_last_played = item.get('last_played', '2000-01-01 00:00:00')
            datetime_object = jsondate_to_datetime(curr_last_played, resformat)
            episode_item = {"season": season, "episode": episode, "meta": meta, "curr_last_played_parsed": datetime_object, "action": "next_episode",
                            "unwatched": unwatched, "nextep_display_settings": nextep_display_settings, 'include_unaired': include_unaired,
                            "adjust_hours": adjust_hours, "current_adjusted_date": current_adjusted_date, 'watched_indicators': watched_indicators}
            result.append(build_episode(episode_item, watched_info, use_trakt, meta_user_info))
        except: pass
    check_meta_database()
    clear_all_trakt_cache_data(confirm=False)
    sync_watched_trakt_to_fen()
    try:
        threads = []
        seen = set()
        ep_list = []
        nextep_settings = settings.nextep_content_settings()
        nextep_display_settings = settings.nextep_display_settings()
        watched_info, use_trakt = get_watched_info_tv()
        adjust_hours = int(__addon__.getSetting('datetime.offset'))
        current_adjusted_date = settings.adjusted_datetime(dt=True)
        meta_user_info = retrieve_user_info()
        watched_indicators = settings.watched_indicators()
        cache_to_disk = nextep_settings['cache_to_disk']
        nextep_display_settings['cache_to_disk'] = cache_to_disk
        window.setProperty('fen_fanart_error', 'true')
        if nextep_settings['include_unwatched']:
            for i in get_unwatched_next_episodes(): ep_list.append(i)
        if watched_indicators in (1, 2):
            from apis.trakt_api import trakt_get_next_episodes
            ep_list += trakt_get_next_episodes()
        else:
            settings.check_database(WATCHED_DB)
            dbcon = database.connect(WATCHED_DB)
            dbcur = dbcon.cursor()
            dbcur.execute('''SELECT media_id, season, episode, last_played FROM watched_status WHERE db_type=?''', ('episode',))
            rows = dbcur.fetchall()
            rows = sorted(rows, key = lambda x: (x[0], x[1], x[2]), reverse=True)
            [ep_list.append({"tmdb_id": a, "season": int(b), "episode": int(c), "last_played": d}) for a, b, c, d in rows if not (a in seen or seen.add(a))]
            ep_list = [x for x in ep_list if x['tmdb_id'] not in check_for_next_episode_excludes()]
        ep_list = [i for i in ep_list if not i['tmdb_id'] == None]
        for item in ep_list: threads.append(Thread(target=_process_eps, args=(item,)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        r = [i for i in result if i is not None]
        r = sort_next_eps(r, nextep_settings)
        item_list = [i['listitem'] for i in r]
        for i in item_list: xbmcplugin.addDirectoryItem(__handle__, i[0], i[1], i[2])
        xbmcplugin.setContent(__handle__, 'episodes')
        xbmcplugin.endOfDirectory(__handle__, cacheToDisc=cache_to_disk)
        setView('view.episode_lists', 'episodes')
    except:
        notification('Error getting Next Episode Info', time=3500)
        pass

def sort_next_eps(result, nextep_settings):
    from modules.utils import title_key
    def func(function):
        if nextep_settings['sort_key'] == 'name': return title_key(function)
        else: return function
    return sorted(result, key=lambda i:func(i[nextep_settings['sort_key']]), reverse=nextep_settings['sort_direction'])

def get_unwatched_next_episodes():
    try:
        if settings.watched_indicators() in (1, 2):
            from apis.trakt_api import trakt_fetch_collection_watchlist, get_trakt_tvshow_id
            data = trakt_fetch_collection_watchlist('watchlist', 'tvshow')
            return [{"tmdb_id": get_trakt_tvshow_id(i['media_ids']), "season": 1, "episode": 0, "unwatched": True} for i in data]
        else:
            settings.check_database(WATCHED_DB)
            dbcon = database.connect(WATCHED_DB)
            dbcur = dbcon.cursor()
            dbcur.execute('''SELECT media_id FROM unwatched_next_episode''')
            unwatched = dbcur.fetchall()
            return [{"tmdb_id": i[0], "season": 1, "episode": 0, "unwatched": True} for i in unwatched]
    except: return []

def add_next_episode_unwatched(action=None, media_id=None, silent=False):
    from modules.indicators_bookmarks import mark_as_watched_unwatched
    settings.check_database(WATCHED_DB)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    media_id = params['tmdb_id'] if not media_id else media_id
    action = params['action'] if not action else action
    if action == 'add': command, line1 = "INSERT OR IGNORE INTO unwatched_next_episode VALUES (?)", '%s Added to Fen Next Episode' % params.get('title')
    else: command, line1 = "DELETE FROM unwatched_next_episode WHERE media_id=?", '%s Removed from Fen Next Episode' % params.get('title')
    dbcon = database.connect(WATCHED_DB)
    dbcon.execute(command, (media_id,))
    dbcon.commit()
    dbcon.close()
    if not silent: notification(line1, time=3500)

def add_to_remove_from_next_episode_excludes():
    settings.check_database(WATCHED_DB)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    action = params.get('action')
    media_id = str(params.get('media_id'))
    title = str(params.get('title'))
    dbcon = database.connect(WATCHED_DB)
    if action == 'add':
        dbcon.execute("INSERT INTO exclude_from_next_episode VALUES (?, ?)", (media_id, title))
        line1 = '[B]{}[/B] excluded from Fen Next Episode'.format(title.upper())
    elif action == 'remove':
        dbcon.execute("DELETE FROM exclude_from_next_episode WHERE media_id=?", (media_id,))
        line1 = '[B]{}[/B] included in Fen Next Episode'.format(title.upper())
    dbcon.commit()
    dbcon.close()
    notification('{}'.format(line1), time=5000)
    xbmc.sleep(500)
    xbmc.executebuiltin("Container.Refresh")

def check_for_next_episode_excludes():
    settings.check_database(WATCHED_DB)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    dbcon = database.connect(WATCHED_DB)
    dbcur = dbcon.cursor()
    dbcur.execute('''SELECT media_id FROM exclude_from_next_episode''')
    row = dbcur.fetchall()
    dbcon.close()
    return [str(i[0]) for i in row]

def build_next_episode_manager():
    from modules.nav_utils import add_dir
    from modules.indicators_bookmarks import get_watched_status_tvshow, get_watched_info_tv
    def _process(tmdb_id, action):
        try:
            meta = tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
            title = meta['title']
            if action == 'manage_unwatched':
                action, display = 'remove', '[COLOR=%s][UNWATCHED][/COLOR] %s' % (NEXT_EP_UNWATCHED, title)
                url_params = {'mode': 'add_next_episode_unwatched', 'action': 'remove', 'tmdb_id': tmdb_id, 'title': title}
            elif action == 'trakt_and_fen':
                action, display = 'unhide' if tmdb_id in exclude_list else 'hide', '[COLOR=red][EXCLUDED][/COLOR] %s' % title if tmdb_id in exclude_list else '[COLOR=green][INCLUDED][/COLOR] %s' % title
                url_params = {"mode": "hide_unhide_trakt_items", "action": action, "media_type": "shows", "media_id": meta['imdb_id'], "section": "progress_watched"}
            else:
                action, display = 'remove' if tmdb_id in exclude_list else 'add', '[COLOR=red][EXCLUDED][/COLOR] %s' % title if tmdb_id in exclude_list else '[COLOR=green][INCLUDED][/COLOR] %s' % title
                url_params = {'mode': 'add_to_remove_from_next_episode_excludes', 'action': action, 'title': title, 'media_id': tmdb_id}
            sorted_list.append({'tmdb_id': tmdb_id, 'display': display, 'url_params': url_params, 'meta': json.dumps(meta)})
        except: pass
    check_meta_database()
    clear_all_trakt_cache_data(confirm=False)
    sync_watched_trakt_to_fen()
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    NEXT_EP_UNWATCHED = __addon__.getSetting('nextep.unwatched_colour')
    if not NEXT_EP_UNWATCHED or NEXT_EP_UNWATCHED == '': NEXT_EP_UNWATCHED = 'red'
    threads = []
    sorted_list = []
    action = params['action']
    if action == 'manage_unwatched':
        tmdb_list = [i['tmdb_id'] for i in get_unwatched_next_episodes()]
        heading = 'Select Show to remove from Fen Next Episode:'
    elif settings.watched_indicators() in (1, 2):
        from apis.trakt_api import trakt_get_next_episodes
        tmdb_list, exclude_list = trakt_get_next_episodes(include_hidden=True)
        heading = 'Select Show to Hide/Unhide from Trakt Progress:'
        action = 'trakt_and_fen'
    else:
        settings.check_database(WATCHED_DB)
        dbcon = database.connect(WATCHED_DB)
        dbcur = dbcon.cursor()
        dbcur.execute('''SELECT media_id FROM watched_status WHERE db_type=? GROUP BY media_id''', ('episode',))
        rows = dbcur.fetchall()
        tmdb_list = [row[0] for row in rows]
        exclude_list = check_for_next_episode_excludes()
        heading = 'Select Show to Include/Exclude in Fen Next Episode:'
    add_dir({'mode': 'nill'}, '[I][COLOR=grey][B]INFO:[/B][/COLOR] [COLOR=grey2]%s[/COLOR][/I]' % heading, iconImage='settings.png')
    if not tmdb_list:
        return notification('No Shows Present', time=5000)
    meta_user_info = retrieve_user_info()
    window.setProperty('fen_fanart_error', 'true')
    for tmdb_id in tmdb_list: threads.append(Thread(target=_process, args=(tmdb_id, action)))
    [i.start() for i in threads]
    [i.join() for i in threads]
    sorted_items = sorted(sorted_list, key=lambda k: k['display'])
    watched_info, use_trakt = get_watched_info_tv()
    for i in sorted_items:
        try:
            cm = []
            meta = json.loads(i['meta'])
            playcount, overlay, total_watched, total_unwatched = get_watched_status_tvshow(watched_info, use_trakt, meta['tmdb_id'], meta.get('total_episodes'))
            meta.update({'playcount': playcount, 'overlay': overlay,
                         'total_watched': str(total_watched), 'total_unwatched': str(total_unwatched)})
            url = build_url(i['url_params'])
            browse_url = build_url({'mode': 'build_season_list', 'meta': i['meta']})
            cm.append(("[B]Browse...[/B]",'XBMC.Container.Update(%s)' % browse_url))
            listitem = xbmcgui.ListItem(i['display'])
            listitem.setProperty('watchedepisodes', str(total_watched))
            listitem.setProperty('unwatchedepisodes', str(total_unwatched))
            listitem.setProperty('totalepisodes', str(meta['total_episodes']))
            listitem.setProperty('totalseasons', str(meta['total_seasons']))
            listitem.addContextMenuItems(cm)
            listitem.setArt({'poster': meta['poster'],
                            'fanart': meta['fanart'],
                            'banner': meta['banner'],
                            'clearart': meta['clearart'],
                            'clearlogo': meta['clearlogo'],
                            'landscape': meta['landscape']})
            listitem.setCast(meta['cast'])
            listitem.setInfo('video', remove_unwanted_info_keys(meta))
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'tvshows')
    xbmcplugin.endOfDirectory(__handle__, cacheToDisc=False)
    setView('view.main', 'tvshows')

def next_episode_color_choice(setting=None):
    from modules.utils import color_chooser
    from modules.nav_utils import open_settings
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    choices = [('Airdate', 'nextep.airdate_colour'),
                ('Unaired', 'nextep.unaired_colour'),
                ('Unwatched', 'nextep.unwatched_colour')]
    prelim_setting = params.get('setting', None) if not setting else setting
    title, setting = [(i[0], i[1]) for i in choices if i[0] == prelim_setting][0]
    dialog = 'Please Choose Color for %s Highlight' % title
    chosen_color = color_chooser(dialog, no_color=True)
    if chosen_color: __addon__.setSetting(setting, chosen_color)

def next_episode_options_choice(setting=None):
    from modules.utils import selection_dialog
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    choices = [
            ('Sort Type', 'nextep.sort_type', [('RECENTLY WATCHED', '0'), ('AIRDATE', '1'), ('TITLE', '2')]),
            ('Sort Order', 'nextep.sort_order', [('DESCENDING', '0'), ('ASCENDING', '1')]),
            ('Include Unaired', 'nextep.include_unaired', [('OFF', 'false'), ('ON', 'true')]),
            ('Include Trakt or Fen Unwatched', 'nextep.include_unwatched', [('OFF', 'false'), ('ON', 'true')]),
            ('Cache To Disk', 'nextep.cache_to_disk', [('OFF', 'false'), ('ON', 'true')]),
            ('Include Airdate in Title', 'nextep.include_airdate', [('OFF', 'false'), ('ON', 'true')]),
            ('Airdate Format', 'nextep.airdate_format', [('DAY-MONTH-YEAR', '0'), ('YEAR-MONTH-DAY', '1'), ('MONTH-DAY-YEAR', '2')])
                ]
    prelim_setting = params.get('setting') if not setting else setting
    title, setting = [(i[0], i[1]) for i in choices if i[0] == prelim_setting][0]
    string = 'Please Choose Setting for %s' % title
    full_list = [i[2] for i in choices if i[0] == prelim_setting][0]
    dialog_list = [i[0] for i in full_list]
    function_list = [i[1] for i in full_list]
    selection = selection_dialog(dialog_list, function_list, string)
    if not selection: return
    setting_name = [i[0] for i in full_list if i[1] == selection][0]
    __addon__.setSetting(setting, selection)
    notification('%s set to %s' % (title, setting_name), 6000)

def next_episode_context_choice():
    from modules.utils import selection_dialog
    from modules.nav_utils import toggle_setting, build_url
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    content_settings = settings.nextep_content_settings()
    display_settings = settings.nextep_display_settings()
    airdate_replacement = [('%d-%m-%Y', 'Day-Month-Year'), ('%Y-%m-%d', 'Year-Month-Day'), ('%m-%d-%Y', 'Month-Day-Year')]
    sort_type_status = ('Recently Watched', 'Airdate', 'Title')[content_settings['sort_type']]
    sort_order_status = ('Descending', 'Ascending')[content_settings['sort_order']]
    toggle_sort_order_SETTING = ('nextep.sort_order', ('0' if sort_order_status == 'Ascending' else '1'))
    cache_to_disk_status = str(content_settings['cache_to_disk'])
    toggle_cache_to_disk_SETTING = ('nextep.cache_to_disk', ('true' if cache_to_disk_status == 'False' else 'false'))
    unaired_status = str(content_settings['include_unaired'])
    toggle_unaired_SETTING = ('nextep.include_unaired', ('true' if unaired_status == 'False' else 'false'))
    unwatched_status = str(content_settings['include_unwatched'])
    toggle_unwatched_SETTING = ('nextep.include_unwatched', ('true' if unwatched_status == 'False' else 'false'))
    airdate_status = str(display_settings['include_airdate'])
    toggle_airdate_SETTING = ('nextep.include_airdate', ('true' if airdate_status == 'False' else 'false'))
    airdate_format = settings.nextep_airdate_format()
    airdate_format_status = [airdate_format.replace(i[0], i[1]) for i in airdate_replacement if i[0] == airdate_format][0]
    airdate_highlight = display_settings['airdate_colour'].capitalize()
    unaired_highlight = display_settings['unaired_colour'].capitalize()
    unwatched_highlight = display_settings['unwatched_colour'].capitalize()
    choices = [
            ('MANAGE IN PROGRESS SHOWS', 'manage_in_progress'),
            ('SORT TYPE: [I]Currently [B]%s[/B][/I]' % sort_type_status, 'Sort Type'),
            ('SORT ORDER: [I]Currently [B]%s[/B][/I]' % sort_order_status, 'toggle_cache_to_disk'),
            ('CACHE TO DISK: [I]Currently [B]%s[/B][/I]' % cache_to_disk_status, 'toggle_cache_to_disk'),
            ('INCLUDE UNAIRED EPISODES: [I]Currently [B]%s[/B][/I]' % unaired_status, 'toggle_unaired'),
            ('INCLUDE WATCHLIST/UNWATCHED TV: [I]Currently [B]%s[/B][/I]' % unwatched_status, 'toggle_unwatched'),
            ('INCLUDE AIRDATE: [I]Currently [B]%s[/B][/I]' % airdate_status, 'toggle_airdate'),
            ('AIRDATE FORMAT: [I]Currently [B]%s[/B][/I]' % airdate_format_status, 'Airdate Format'),
            ('AIRDATE HIGHLIGHT: [I]Currently [B]%s[/B][/I]' % airdate_highlight, 'Airdate'),
            ('UNAIRED HIGHLIGHT: [I]Currently [B]%s[/B][/I]' % unaired_highlight, 'Unaired'),
            ('UNWATCHED HIGHLIGHT: [I]Currently [B]%s[/B][/I]' % unwatched_highlight, 'Unwatched')]
    if settings.watched_indicators() == 0: choices.append(('MANAGE UNWATCHED TV SHOWS', 'manage_unwatched'))
    if settings.watched_indicators() in (1,2): choices.append(('CLEAR TRAKT CACHE', 'clear_cache'))
    string = 'Next Episode Manager'
    dialog_list = [i[0] for i in choices]
    function_list = [i[1] for i in choices]
    choice = selection_dialog(dialog_list, function_list, string)
    if not choice: return
    if choice in ('toggle_sort_order', 'toggle_cache_to_disk', 'toggle_unaired', 'toggle_unwatched', 'toggle_airdate'):
        setting = eval(choice + '_SETTING')
        toggle_setting(setting[0], setting[1])
    elif choice == 'clear_cache':
        from modules.nav_utils import clear_cache
        clear_cache('trakt')
    else:
        if choice in ('manage_in_progress', 'manage_unwatched'):
            xbmc.executebuiltin('Container.Update(%s)' % build_url({'mode': 'build_next_episode_manager', 'action': choice})); return
        elif choice in ('Airdate','Unaired', 'Unwatched'): function = next_episode_color_choice
        else: function = next_episode_options_choice
        function(choice)
    xbmc.executebuiltin("Container.Refresh")
    xbmc.executebuiltin('RunPlugin(%s)' % build_url({'mode': 'next_episode_context_choice'}))

def nextep_playback_info(tmdb_id, current_season, current_episode, from_library=None):
    def build_next_episode_play():
        ep_data = [i['episodes_data'] for i in seasons_data if i['season_number'] == season][0]
        ep_data = [i for i in ep_data if i['airedEpisodeNumber'] == episode][0]
        airdate = ep_data['firstAired']
        d = airdate.split('-')
        episode_date = date(int(d[0]), int(d[1]), int(d[2]))
        if current_adjusted_date < episode_date: return {'pass': True}
        query = meta['title'] + ' S%.2dE%.2d' % (int(season), int(episode))
        display_name = '%s - %dx%.2d' % (meta['title'], int(season), int(episode))
        meta.update({'vid_type': 'episode', 'rootname': display_name, "season": season, 'ep_name': ep_data['episodeName'],
                    "episode": episode, 'premiered': airdate, 'plot': ep_data['overview']})
        meta_json = json.dumps(meta)
        url_params = {'mode': 'play_media', 'background': 'true', 'vid_type': 'episode', 'tmdb_id': meta['tmdb_id'],
                    'query': query, 'tvshowtitle': meta['rootname'], 'season': season,
                    'episode': episode, 'meta': meta_json, 'ep_name': ep_data['episodeName']}
        if from_library: url_params.update({'library': 'True', 'plot': ep_data['overview']})
        return build_url(url_params)
    check_meta_database()
    meta_user_info = retrieve_user_info()
    meta = tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
    nextep_info = {'pass': True}
    try:
        current_adjusted_date = settings.adjusted_datetime()
        seasons_data = all_episodes_meta(tmdb_id, meta['tvdb_id'], meta['tvdb_summary']['airedSeasons'], meta['season_data'], meta_user_info)
        curr_season_data = [i for i in seasons_data if i['season_number'] == current_season][0]
        season = current_season if current_episode < curr_season_data['episode_count'] else current_season + 1
        episode = current_episode + 1 if current_episode < curr_season_data['episode_count'] else 1
        nextep_info = {'season': season, 'episode': episode, 'url': build_next_episode_play()}
    except: pass
    return nextep_info

def nextep_play(next_ep_info):
    xbmc.executebuiltin("RunPlugin(%s)" % next_ep_info['url'])





