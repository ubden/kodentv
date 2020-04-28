import xbmc, xbmcaddon, xbmcgui
import sys
import json
from modules.utils import clean_file_name, to_utf8
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
dialog = xbmcgui.Dialog()
window = xbmcgui.Window(10000)

def retrieve_kodi_library(db_type, page_no, letter):
    from modules.utils import title_key, to_utf8
    from modules.nav_utils import paginate_list
    from settings import paginate, page_limit
    paginate = paginate()
    limit = page_limit()
    if db_type in ('movie', 'movies'):
        db_type = 'movies'
        JSON_req = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", \
        "params": {"properties": ["title", "imdbnumber"]},"id": "1"}'
    elif db_type in ('tvshow', 'tvshows'):
        db_type = 'tvshows'
        JSON_req = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTvShows", \
        "params": {"properties": ["title","imdbnumber","uniqueid"]}, "id": "1"}'
    r = xbmc.executeJSONRPC(JSON_req)
    r = to_utf8(json.loads(r)['result'][db_type])
    r = sorted(r, key=lambda k: title_key(k['title']))
    original_list = [{'title': i.get('title', None), 'media_id': i.get('imdbnumber', None)} for i in r] if db_type == 'movies' else [{'title': i.get('title', None), 'media_id': i['uniqueid']['tvdb'] if 'uniqueid' in i and 'tvdb' in i['uniqueid'] else i['imdbnumber'] if i['imdbnumber'].startswith("tt") else None} for i in r]
    if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    else: final_list, total_pages = original_list, 1
    return final_list, total_pages

def get_library_video(db_type, title, year, season=None, episode=None):
    import xbmcvfs
    try:
        years = (year, str(int(year)+1), str(int(year)-1))
        if db_type == 'movie':
            r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["imdbnumber", "title", "originaltitle", "file"]}, "id": 1}' % years)
            r = to_utf8(r)
            r = json.loads(r)['result']['movies']
            try:
                r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()]
            except:
                return None
            r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["streamdetails", "file"], "movieid": %s }, "id": 1}' % str(r['movieid']))
            r = to_utf8(r)
            r = json.loads(r)['result']['moviedetails']
        elif db_type  == 'tvshow':
            r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title", "year"]}, "id": 1}' % years)
            r = to_utf8(r)
            r = json.loads(r)['result']['tvshows']
            try:
                r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])][0]
                return r
            except:
                return None
    except: pass

def set_bookmark_kodi_library(db_type, tmdb_id, curr_time, season='', episode=''):
    from tikimeta import movie_meta, tvshow_meta, retrieve_user_info
    meta_user_info = retrieve_user_info()
    window.setProperty('fen_fanart_error', 'true')
    try:
        info = movie_meta('tmdb_id', tmdb_id, meta_user_info) if db_type == 'movie' else tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
        title = info['title']
        year = info['year']
        years = (str(year), str(int(year)+1), str(int(year)-1))
        if db_type == 'movie': r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
        else: r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
        r = to_utf8(r)
        r = json.loads(r)['result']['movies'] if db_type == 'movie' else json.loads(r)['result']['tvshows']
        if db_type == 'movie': r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()]
        else: r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])]
        if db_type == 'episode':
            r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(r['tvshowid'])))
            r = to_utf8(r)
            r = json.loads(r)['result']['episodes'][0]
        (method, id_name, library_id) = ('SetMovieDetails', 'movieid', r['movieid']) if db_type == 'movie' else ('SetEpisodeDetails', 'episodeid', r['episodeid'])
        query = {"jsonrpc": "2.0", "id": "setResumePoint", "method": "VideoLibrary."+method, "params": {id_name: library_id, "resume": {"position": curr_time,}}}
        xbmc.executeJSONRPC(json.dumps(query))
    except: pass

def mark_as_watched_unwatched_kodi_library(db_type, action, title, year, season=None, episode=None):
    try:
        playcount = 1 if action == 'mark_as_watched' else 0
        years = (str(year), str(int(year)+1), str(int(year)-1))
        if db_type == 'movie': r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
        else: r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
        r = to_utf8(r)
        r = json.loads(r)['result']['movies'] if db_type == 'movie' else json.loads(r)['result']['tvshows']
        if db_type == 'movie': r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()][0]
        else: r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])][0]
        if db_type == 'episode':
            r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(r['tvshowid'])))
            r = to_utf8(r)
            r = json.loads(r)['result']['episodes'][0]
        (method, id_name, library_id) = ('SetMovieDetails', 'movieid', r['movieid']) if db_type == 'movie' else ('SetEpisodeDetails', 'episodeid', r['episodeid'])
        query = {"jsonrpc": "2.0", "method": "VideoLibrary."+method, "params": {id_name : library_id, "playcount" : playcount }, "id": 1 }
        xbmc.executeJSONRPC(json.dumps(query))
        query = {"jsonrpc": "2.0", "id": "setResumePoint", "method": "VideoLibrary."+method, "params": {id_name: library_id, "resume": {"position": 0,}}}
        xbmc.executeJSONRPC(json.dumps(query))
    except: pass

def batch_mark_episodes_as_watched_unwatched_kodi_library(show_info, list_object):
    action = list_object['action']
    episode_list = list_object['season_ep_list']
    tvshowid = list_object['tvshowid']
    playcount = 1 if action == 'mark_as_watched' else 0
    tvshowid = str(show_info['tvshowid'])
    ep_ids = []
    action_list = []
    bg_dialog = xbmcgui.DialogProgressBG()
    bg_dialog.create('Please Wait', '')
    try:
        for item in episode_list:
            try:
                season = item.split('<>')[0]
                episode = item.split('<>')[1]
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file", "playcount"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(tvshowid)))
                r = to_utf8(r)
                r = json.loads(r)['result']['episodes'][0]
                ep_ids.append('%s<>%s' % (r['episodeid'], r['playcount']))
            except: pass
        for count, item in enumerate(ep_ids, 1):
            try:
                ep_id = item.split('<>')[0]
                current_playcount = item.split('<>')[1]
                if int(current_playcount) != playcount:
                    xbmc.sleep(50)
                    display = 'Syncing Kodi Library Watched Status'
                    bg_dialog.update(int(float(count) / float(len(ep_ids)) * 100), 'Please Wait', '%s' % display)
                    t = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %d, "playcount" : %d }, "id": 1 }' % (int(ep_id) ,playcount)
                    t = json.loads(t)
                    action_list.append(t)
                else: pass
            except: pass
        bg_dialog.update(100, 'Please Wait', 'Finalizing Sync with Kodi Library')
        r = xbmc.executeJSONRPC(json.dumps(action_list))
        bg_dialog.close()
        return r
    except: pass

def build_kodi_library_recently_added(db_type):
    import xbmcplugin
    from modules.nav_utils import setView
    limit = int(__addon__.getSetting('recent_added_limit'))
    recent_added = []
    results = []
    if db_type in ('movie', 'movies'):
        from indexers.movies import Movies
        db_type = 'movies'
        view_type = 'view.movies'
        try:
            JSON_req = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetRecentlyAddedMovies", \
            "params": {"properties": ["title", "imdbnumber"]},"id": "1"}'
            r = xbmc.executeJSONRPC(JSON_req)
            r = to_utf8(json.loads(r)['result'][db_type])[:limit]
            results = [i.get('imdbnumber') for i in r]
            Movies(results, 'imdb_id').worker()
        except: pass
    else:
        from indexers.tvshows import build_episode
        from modules.indicators_bookmarks import get_watched_info_tv
        from tikimeta import tvshow_meta, retrieve_user_info
        from threading import Thread
        def process_eps(item):
            results.append(build_episode({"season": int(item['season']), "episode": int(item['episode']), 'order': item['order'], "meta": tvshow_meta('tvdb_id',
                                          item['media_id'], meta_user_info)}, watched_info, use_trakt, meta_user_info))
        try:
            db_type = 'episodes'
            view_type = 'view.episodes'
            ALL_JSON_req = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTvShows", \
            "params": {"properties": ["imdbnumber","uniqueid"]}, "id": "1"}'
            r = xbmc.executeJSONRPC(ALL_JSON_req)
            r = to_utf8(json.loads(r)['result']['tvshows'])
            tvshow_list = [{'tvshow_id': i["tvshowid"], 'media_id': i['uniqueid']['tvdb'] if 'uniqueid' in i and 'tvdb' in i['uniqueid'] else i['imdbnumber'] if not i['imdbnumber'].startswith("tt") else None} for i in r]
            tvshow_list = [i for i in tvshow_list if i['media_id'] != None]
            JSON_req = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetRecentlyAddedEpisodes", \
            "params": {"properties": ["tvshowid", "season", "episode"]}, "id": "1"}'
            r = xbmc.executeJSONRPC(JSON_req)
            r = to_utf8(json.loads(r)['result'][db_type])[:limit]
            episodes_list = [{'tvshow_id': i['tvshowid'], 'season': i['season'], 'episode': i['episode'], 'order': r.index(i)} for i in r]
            watched_info, use_trakt = get_watched_info_tv()
            meta_user_info = retrieve_user_info()
            window.setProperty('fen_fanart_error', 'true')
            for i in episodes_list:
                for t in tvshow_list:
                    if i['tvshow_id'] == t['tvshow_id']:
                        recent_added.append({'media_id': t['media_id'], 'season': i['season'], 'episode': i['episode'], 'order': episodes_list.index(i)})
            threads = []
            for item in recent_added: threads.append(Thread(target=process_eps, args=(item,)))
            [i.start() for i in threads]
            [i.join() for i in threads]
            r = [i for i in results if i is not None]
            r = sorted(r, key=lambda k: k['order'])
            listitems = [i['listitem'] for i in r]
            xbmcplugin.addDirectoryItems(__handle__, listitems, len(listitems))
        except: pass
    xbmcplugin.setContent(__handle__, db_type)
    xbmcplugin.endOfDirectory(__handle__)
    setView(view_type, db_type)
        