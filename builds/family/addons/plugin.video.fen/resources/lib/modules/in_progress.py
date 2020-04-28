import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, sys
from threading import Thread
from modules.nav_utils import setView
from indexers.tvshows import build_episode
from tikimeta import tvshow_meta, retrieve_user_info, check_meta_database
from modules import settings
try:
    from sqlite3 import dbapi2 as database
except ImportError:
    from pysqlite2 import dbapi2 as database
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
window = xbmcgui.Window(10000)

WATCHED_DB = os.path.join(__addon_profile__, 'watched_status.db')

def in_progress_movie(db_type, page_no, letter):
    from modules.nav_utils import paginate_list
    paginate = settings.paginate()
    limit = settings.page_limit()
    settings.check_database(WATCHED_DB)
    dbcon = database.connect(WATCHED_DB)
    dbcur = dbcon.cursor()
    dbcur.execute('''SELECT media_id FROM progress WHERE db_type=? ORDER BY rowid DESC''', ('movie',))
    rows = dbcur.fetchall()
    data = [i[0] for i in rows if not i[0] == '']
    original_list = [{'media_id': i} for i in data]
    if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    else: final_list, total_pages = original_list, 1
    return final_list, total_pages

def in_progress_tvshow(db_type, page_no, letter):
    from modules.utils import title_key
    from modules.nav_utils import paginate_list
    paginate = settings.paginate()
    limit = settings.page_limit()
    check_meta_database()
    if settings.watched_indicators() in (1, 2):
        from apis.trakt_api import trakt_indicators_tv
        items = trakt_indicators_tv()
        data = [(i[0], i[3]) for i in items if i[1] > len(i[2])]
    else:
        from modules.indicators_bookmarks import get_watched_status_tvshow, get_watched_info_tv
        def _process(item):
            meta = tvshow_meta('tmdb_id', item[0], meta_user_info)
            watched_status = get_watched_status_tvshow(watched_info, use_trakt, meta['tmdb_id'], meta.get('total_episodes'))
            if not watched_status[0] == 1: data.append(item)
        data = []
        threads = []
        settings.check_database(WATCHED_DB)
        dbcon = database.connect(WATCHED_DB)
        dbcur = dbcon.cursor()
        dbcur.execute('''SELECT media_id, title, last_played FROM watched_status WHERE db_type=? ORDER BY rowid DESC''', ('episode',))
        rows1 = dbcur.fetchall()
        in_progress_result = list(set([i for i in rows1]))
        watched_info, use_trakt = get_watched_info_tv()
        meta_user_info = retrieve_user_info()
        window.setProperty('fen_fanart_error', 'true')
        for item in in_progress_result: threads.append(Thread(target=_process, args=(item,)))
        [i.start() for i in threads]
        [i.join() for i in threads]
    data = sorted(data, key=lambda k: title_key(k[1]))
    original_list = [{'media_id': i[0]} for i in data]
    if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    else: final_list, total_pages = original_list, 1
    return final_list, total_pages

def build_in_progress_episode():
    from modules.indicators_bookmarks import get_watched_info_tv
    def process_eps(item):
    	episode_item = {"season": int(item[1]), "episode": int(item[2]), "meta": tvshow_meta('tmdb_id', item[0], meta_user_info),
                        "adjust_hours": adjust_hours, "current_adjusted_date": current_adjusted_date, 'watched_indicators': watched_indicators}
        listitem = build_episode(episode_item, watched_info, use_trakt, meta_user_info)['listitem']
        xbmcplugin.addDirectoryItem(__handle__, listitem[0], listitem[1], isFolder=listitem[2])
    check_meta_database()
    settings.check_database(WATCHED_DB)
    watched_info, use_trakt = get_watched_info_tv()
    meta_user_info = retrieve_user_info()
    adjust_hours = int(__addon__.getSetting('datetime.offset'))
    current_adjusted_date = settings.adjusted_datetime(dt=True)
    watched_indicators = settings.watched_indicators()
    window.clearProperty('fen_fanart_error')
    threads = []
    dbcon = database.connect(WATCHED_DB)
    dbcur = dbcon.cursor()
    dbcur.execute('''SELECT media_id, season, episode FROM progress WHERE db_type=? ORDER BY rowid DESC''', ('episode',))
    rows = dbcur.fetchall()
    for item in rows: threads.append(Thread(target=process_eps, args=(item,)))
    [i.start() for i in threads]
    [i.join() for i in threads]
    xbmcplugin.setContent(__handle__, 'episodes')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.episode_lists', 'episodes')

    