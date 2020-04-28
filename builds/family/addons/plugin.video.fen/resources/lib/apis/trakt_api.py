# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import os, sys
import requests
import json
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
import time
from modules import trakt_cache
from modules.fen_cache import cache_object
from modules.nav_utils import build_url, setView, add_dir, notification
from modules.utils import to_utf8
from modules import settings
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
dialog = xbmcgui.Dialog()
icon_directory = settings.get_theme()
fanart = xbmc.translatePath(__addon__.getAddonInfo('fanart'))
window = xbmcgui.Window(10000)

API_ENDPOINT = "https://api-v2launch.trakt.tv"
CLIENT_ID = "793c4e6772d7ccdd66e8f03aeb96a8a968bb9c71ad2b8ce721fd194935b9b1ef"
CLIENT_SECRET = "56bb84ffade5962bc981300cc417edd645283cd54eb97cea8964f26a98225c11"

def call_trakt(path, params={}, data=None, is_delete=False, with_auth=True, method=None, pagination=False, page=1, suppress_error_notification=False):
    def error_notification(line1, error):
        if suppress_error_notification: return
        from modules.nav_utils import notification
        return notification('%s: %s' % (line1, error), 3000, trakt_icon)
    def send_query():
        if with_auth:
            try:
                expires_at = __addon__.getSetting('trakt_expires_at')
                if time.time() > expires_at:
                    trakt_refresh_token()
            except:
                pass
            token = __addon__.getSetting('trakt_access_token')
            if token:
                headers['Authorization'] = 'Bearer ' + token
        try:
            if method:
                if method == 'post':
                    resp = requests.post("{0}/{1}".format(API_ENDPOINT, path), headers=headers, timeout=timeout)
                elif method == 'delete':
                    resp = requests.delete("{0}/{1}".format(API_ENDPOINT, path), headers=headers, timeout=timeout)
                elif method == 'sort_by_headers':
                    resp = requests.get("{0}/{1}".format(API_ENDPOINT, path), params, headers=headers, timeout=timeout)
            elif data is not None:
                assert not params
                resp = requests.post("{0}/{1}".format(API_ENDPOINT, path), json=data, headers=headers, timeout=timeout)
            elif is_delete:
                resp = requests.delete("{0}/{1}".format(API_ENDPOINT, path), headers=headers, timeout=timeout)
            else:
                resp = requests.get("{0}/{1}".format(API_ENDPOINT, path), params, headers=headers, timeout=timeout)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            error_notification('Trakt Error', e)
        except Exception as e:
            error_notification('', e)
        return resp
    trakt_icon = os.path.join(icon_directory, 'trakt.png')
    params = dict([(k, to_utf8(v)) for k, v in params.items() if v])
    timeout = 15.0
    resp = None
    numpages = 0
    headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': CLIENT_ID}
    if pagination: params['page'] = page
    response = send_query()
    if response.status_code == 401:
        if xbmc.Player().isPlaying() == False:
            if with_auth and dialog.yesno("Authenticate Trakt", "You must authenticate with Trakt. Do you want to authenticate now?") and trakt_authenticate():
                response = send_query()
            else: pass
        else: return
    response.raise_for_status()
    response.encoding = 'utf-8'
    try: result = response.json()
    except: result = None
    if method == 'sort_by_headers':
        headers = response.headers
        if 'X-Sort-By' in headers and 'X-Sort-How' in headers:
            from modules.utils import sort_list
            result = sort_list(headers['X-Sort-By'], headers['X-Sort-How'], result)
    if pagination: numpages = response.headers["X-Pagination-Page-Count"]
    return (result, numpages) if pagination else result

def trakt_get_device_code():
    data = { 'client_id': CLIENT_ID }
    return call_trakt("oauth/device/code", data=data, with_auth=False)

def trakt_get_device_token(device_codes):
    data = {
        "code": device_codes["device_code"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    start = time.time()
    expires_in = device_codes["expires_in"]
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(("Authenticate Trakt"), ("Please go to [B]https://trakt.tv/activate[/B] and enter the code"), "[B]%s[/B]" % str(device_codes["user_code"]))
    try:
        time_passed = 0
        while not xbmc.abortRequested and not progress_dialog.iscanceled() and time_passed < expires_in:            
            try:
                response = call_trakt("oauth/device/token", data=data, with_auth=False, suppress_error_notification=True)
            except requests.HTTPError as e:
                if e.response.status_code != 400:
                    raise e
                progress = int(100 * time_passed / expires_in)
                progress_dialog.update(progress)
                xbmc.sleep(max(device_codes["interval"], 1)*1000)
            else:
                return response
                
            time_passed = time.time() - start
    finally:
        progress_dialog.close()
        del progress_dialog
    return None

def trakt_refresh_token():
    data = {        
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "refresh_token",
        "refresh_token": __addon__.getSetting('trakt_refresh_token')
    }
    response = call_trakt("oauth/token", data=data, with_auth=False)
    if response:
        __addon__.setSetting('trakt_access_token', response["access_token"])
        __addon__.setSetting('trakt_refresh_token', response["refresh_token"])

def trakt_authenticate():
    trakt_icon = os.path.join(icon_directory, 'trakt.png')
    code = trakt_get_device_code()
    token = trakt_get_device_token(code)
    if token:
        expires_at = time.time() + 60*60*24*30
        __addon__.setSetting('trakt_expires_at', str(expires_at))
        __addon__.setSetting('trakt_access_token', token["access_token"])
        __addon__.setSetting('trakt_refresh_token', token["refresh_token"])
        __addon__.setSetting('trakt_indicators_active', 'true')
        __addon__.setSetting('watched_indicators', '1')
        xbmc.sleep(1000)
        try:
            user = call_trakt("/users/me", with_auth=True)
            __addon__.setSetting('trakt_user', str(user['username']))
        except: pass
        notification('Trakt Account Authorized', 3000, trakt_icon)
        return True
    notification('Trakt Error Authorizing', 3000, trakt_icon)
    return False

def trakt_remove_authentication():
    data = {"token": __addon__.getSetting('trakt_access_token')}
    try: call_trakt("oauth/revoke", data=data, with_auth=False)
    except: pass
    __addon__.setSetting('trakt_user', '')
    __addon__.setSetting('trakt_expires_at', '')
    __addon__.setSetting('trakt_access_token', '')
    __addon__.setSetting('trakt_refresh_token', '')
    __addon__.setSetting('trakt_indicators_active', 'false')
    __addon__.setSetting('watched_indicators', '0')
    notification('Trakt Account Authorization Reset', 3000)

def trakt_movies_trending(page_no):
    string = "%s_%s" % ('trakt_movies_trending', page_no)
    url = {'path': "movies/trending/%s", "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_movies_anticipated(page_no):
    string = "%s_%s" % ('trakt_movies_anticipated', page_no)
    url = {'path': "movies/anticipated/%s", "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_movies_top10_boxoffice(page_no):
    string = "%s" % 'trakt_movies_top10_boxoffice'
    url = {'path': "movies/boxoffice/%s", 'pagination': False}
    return cache_object(get_trakt, string, url, False)

def trakt_movies_mosts(period, duration, page_no):
    string = "%s_%s_%s_%s" % ('trakt_movies_mosts', period, duration, page_no)
    url = {'path': "movies/%s/%s", "path_insert": (period, duration), "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_movies_related(imdb_id, page_no, letter='None'):
    from modules.nav_utils import paginate_list
    limit = 20
    string = "%s_%s" % ('trakt_movies_related', imdb_id)
    url = {'path': "movies/%s/related", "path_insert": imdb_id, "params": {'extended':'full', 'limit': 100}}
    original_list = cache_object(get_trakt, string, url, False)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, total_pages

def trakt_recommendations(db_type):
    limit = settings.page_limit() * 2
    return to_utf8(call_trakt("/recommendations/{0}".format(db_type), params={'limit': limit}))

def trakt_tv_trending(page_no):
    string = "%s_%s" % ('trakt_tv_trending', page_no)
    url = {'path': "shows/trending/%s", "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_tv_anticipated(page_no):
    string = "%s_%s" % ('trakt_tv_anticipated', page_no)
    url = {'path': "shows/anticipated/%s", "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_tv_certifications(certification, page_no):
    string = "%s_%s_%s" % ('trakt_tv_certifications', certification, page_no)
    url = {'path': "shows/collected/all?certifications=%s", "path_insert": certification, "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_tv_mosts(period, duration, page_no):
    string = "%s_%s_%s_%s" % ('trakt_tv_mosts', period, duration, page_no)
    url = {'path': "shows/%s/%s", "path_insert": (period, duration), "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_tv_related(imdb_id, page_no, letter='None'):
    from modules.nav_utils import paginate_list
    limit = 20
    string = "%s_%s" % ('trakt_tv_related', imdb_id)
    url = {'path': "shows/%s/related", "path_insert": imdb_id, "params": {'extended':'full', 'limit': 100}}
    from modules.nav_utils import paginate_list
    original_list = cache_object(get_trakt, string, url, False)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, total_pages

def trakt_get_hidden_items(list_type):
    string = 'trakt_hidden_items_%s' % list_type
    url = {'path': "users/hidden/%s", "path_insert": list_type, "params": {'limit': 1000, "type": "show"}, "with_auth": True, "pagination": False}
    return trakt_cache.cache_trakt_object(get_trakt, string, url)

def trakt_watched_unwatched(action, media, media_id, tvdb_id=0, season=None, episode=None, key=None):
    url = "sync/history" if action == 'mark_as_watched' else "sync/history/remove"
    if not key: key = "imdb"
    if media == 'movies': data = {"movies": [{"ids": {"tmdb": media_id}}]}
    elif media == 'episode': data = {"shows": [{"seasons": [{"episodes": [{"number": int(episode)}], "number": int(season)}], "ids": {key: media_id}}]}
    elif media =='shows': data = {"shows": [{"ids": {key: media_id}}]}
    elif media == 'season': data = {"shows": [{"ids": {key: media_id}, "seasons": [{"number": int(season)}]}]}
    result = call_trakt(url, data=data)
    if not media == 'movies':
        if tvdb_id == 0: return
        result_key = 'added' if action == 'mark_as_watched' else 'deleted'
        if not result[result_key]['episodes'] > 0:
            trakt_watched_unwatched(action, media, tvdb_id, tvdb_id, season, episode, key="tvdb")

def trakt_collection_widgets(db_type, param1, param2):
    # param1 = the type of list to be returned (from 'new_page' param), param2 is currently not used
    from modules.nav_utils import paginate_list
    try: limit = int(__addon__.getSetting('trakt_widget_limit'))
    except: limit = 20
    string_insert = 'movie' if db_type in ('movie', 'movies') else 'tvshow'
    window_property_name = 'fen_trakt_collection_%s' % string_insert
    try: data = json.loads(window.getProperty(window_property_name))
    except: data = trakt_fetch_collection_watchlist('collection', db_type)
    if param1 == 'recent':
        data = sorted(data, key=lambda k: k['collected_at'], reverse=True)[:limit]
    elif param1 == 'random':
        import random
        random.shuffle(data)
        data = data[:limit]
    for item in data:
        item['media_id'] = get_trakt_movie_id(item['media_ids']) if db_type == 'movies' else get_trakt_tvshow_id(item['media_ids'])
    return data, 1

def trakt_collection(db_type, page_no, letter):
    paginate = settings.paginate()
    limit = settings.page_limit()
    string_insert = 'movie' if db_type in ('movie', 'movies') else 'tvshow'
    window_property_name = 'fen_trakt_collection_%s' % string_insert
    try: original_list = json.loads(window.getProperty(window_property_name))
    except: original_list = trakt_fetch_collection_watchlist('collection', db_type)
    if paginate:
        from modules.nav_utils import paginate_list
        final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    else: final_list, total_pages = original_list, 1
    for item in final_list:
        item['media_id'] = get_trakt_movie_id(item['media_ids']) if db_type == 'movies' else get_trakt_tvshow_id(item['media_ids'])
    return final_list, total_pages

def trakt_watchlist(db_type, page_no, letter):
    from modules.nav_utils import paginate_list
    paginate = settings.paginate()
    limit = settings.page_limit()
    string_insert = 'movie' if db_type in ('movie', 'movies') else 'tvshow'
    window_property_name = 'fen_trakt_watchlist_%s' % string_insert
    try: original_list = json.loads(window.getProperty(window_property_name))
    except: original_list = trakt_fetch_collection_watchlist('watchlist', db_type)
    if paginate:
        from modules.nav_utils import paginate_list
        final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    else: final_list, total_pages = original_list, 1
    for item in final_list:
        item['media_id'] = get_trakt_movie_id(item['media_ids']) if db_type == 'movies' else get_trakt_tvshow_id(item['media_ids'])
    return final_list, total_pages

def trakt_fetch_collection_watchlist(list_type, db_type):
    from modules.utils import title_key
    key, string_insert = ('movie', 'movie') if db_type in ('movie', 'movies') else ('show', 'tvshow')
    collected_at = 'collected_at' if db_type in ('movie', 'movies') else 'last_collected_at'
    window_property_name = 'fen_trakt_%s_%s' % (list_type, string_insert)
    string = "trakt_%s_%s" % (list_type, string_insert)
    path = "sync/%s/" % list_type
    url = {"path": path + "%s", "path_insert": db_type, "params": {'extended':'full'}, "with_auth": True, "pagination": False, "method": "sort_by_headers"}
    data = trakt_cache.cache_trakt_object(get_trakt, string, url)
    if list_type == 'watchlist': data = [i for i in data if i['type'] == key]
    result = [{'media_ids': i[key]['ids'], 'title': i[key]['title'], 'collected_at': i.get(collected_at)} for i in data]
    result = sorted(result, key=lambda k: title_key(k['title']))
    window.setProperty(window_property_name, json.dumps(result))
    return result

def add_to_list(user, slug, data):
    result = call_trakt("/users/{0}/lists/{1}/items".format(user, slug), data = data)
    if result['added']['shows'] > 0 or result['added']['movies'] > 0:
        notification('Item added to Trakt List', 3000)
    else: notification('Error adding item to Trakt List', 3000)
    return result

def remove_from_list(user, slug, data):
    result = call_trakt("/users/{0}/lists/{1}/items/remove".format(user, slug), data=data)
    if result['deleted']['shows'] > 0 or result['deleted']['movies'] > 0:
        notification('Item removed from Trakt List', 3000)
        xbmc.executebuiltin("Container.Refresh")
    else: notification('Error removing item from Trakt List', 3000)
    return result

def add_to_watchlist(data):
    result = call_trakt("/sync/watchlist", data=data)
    if result['added']['movies'] > 0: db_type = 'movie'
    elif result['added']['shows'] > 0: db_type = 'tvshow'
    else: return notification('Error adding item to Trakt Watchlist', 3000)
    trakt_cache.clear_trakt_collection_watchlist_data('watchlist', db_type)
    notification('Item added to Trakt Watchlist', 6000)
    return result

def remove_from_watchlist(data):
    result = call_trakt("/sync/watchlist/remove", data=data)
    if result['deleted']['movies'] > 0: db_type = 'movie'
    elif result['deleted']['shows'] > 0: db_type = 'tvshow'
    else: return notification('Error removing item from Trakt Watchlist', 3000)
    trakt_cache.clear_trakt_collection_watchlist_data('watchlist', db_type)
    notification('Item removed from Trakt Watchlist', 3000)
    xbmc.executebuiltin("Container.Refresh")
    return result

def add_to_collection(data):
    result = call_trakt("/sync/collection", data=data)
    if result['added']['movies'] > 0: db_type = 'movie'
    elif result['added']['episodes'] > 0: db_type = 'tvshow'
    else: return notification('Error adding item to Trakt Collection', 3000)
    trakt_cache.clear_trakt_collection_watchlist_data('collection', db_type)
    notification('Item added to Trakt Collection', 6000)
    return result

def remove_from_collection(data):
    result = call_trakt("/sync/collection/remove", data=data)
    if result['deleted']['movies'] > 0: db_type = 'movie'
    elif result['deleted']['episodes'] > 0: db_type = 'tvshow'
    else: return notification('Error removing item from Trakt Collection', 3000)
    trakt_cache.clear_trakt_collection_watchlist_data('collection', db_type)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    notification('Item removed from Trakt Collection', 3000)
    xbmc.executebuiltin("Container.Refresh")
    return result
    
def trakt_get_next_episodes(include_hidden=False):
    ep_list = []
    result = trakt_tv_watched_raw()
    for item in result:
        season = item['seasons'][-1]['number']
        episodes = [x for x in item['seasons'][-1]['episodes'] if 'number' in x]
        episodes = sorted(episodes, key=lambda x: x['number'])
        episode = episodes[-1]['number']
        last_played = episodes[-1]['last_watched_at']
        tvdb_id = item['show']['ids']['tvdb']
        tmdb_id = get_trakt_tvshow_id(item['show']['ids'])
        ep_list.append({"tmdb_id": get_trakt_tvshow_id(item['show']['ids']), "tvdb_id": tvdb_id, "season": season, "episode": episode, "last_played": last_played})
    try: hidden_data = trakt_get_hidden_items("progress_watched")
    except: hidden_data = []
    if include_hidden:
        all_shows = [i['tmdb_id'] for i in ep_list]
        hidden_shows = [get_trakt_tvshow_id(i['show']['ids']) for i in hidden_data]
        return all_shows, hidden_shows
    hidden_shows = [i['show']['ids']['tvdb'] for i in hidden_data]
    items = [i for i in ep_list if not i['tvdb_id'] in hidden_shows]
    return items

def hide_unhide_trakt_items(action, db_type, media_id, list_type):
    db_type = 'movies' if db_type in ['movie', 'movies'] else 'shows'
    key = 'tmdb' if db_type == 'movies' else 'imdb'
    url = "users/hidden/{}".format(list_type) if action == 'hide' else "users/hidden/{}/remove".format(list_type)
    data = {db_type: [{'ids': {key: media_id}}]}
    call_trakt(url, data=data)
    trakt_cache.clear_trakt_hidden_data(list_type)

def hide_recommendations(db_type='', imdb_id=''):
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    db_type = params.get('db_type') if 'db_type' in params else db_type
    imdb_id = params.get('imdb_id') if 'imdb_id' in params else imdb_id
    result = call_trakt("/recommendations/{0}/{1}".format(db_type, imdb_id), method='delete')
    notification('Item hidden from Trakt Recommendations', 3000)
    xbmc.sleep(500)
    xbmc.executebuiltin("Container.Refresh")
    return result

def make_new_trakt_list():
    import urllib
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    mode = params.get('mode')
    list_title = dialog.input("Name New List", type=xbmcgui.INPUT_ALPHANUM)
    if not list_title: return
    list_name = urllib.unquote(list_title)
    data = {'name': list_name, 'privacy': 'private', 'allow_comments': False}
    call_trakt("users/me/lists", data=data)
    trakt_cache.clear_trakt_list_data('my_lists')
    notification('{}'.format('Trakt list Created', 3000))
    xbmc.executebuiltin("Container.Refresh")

def delete_trakt_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    user = params.get('user')
    list_slug = params.get('list_slug')
    confirm = dialog.yesno('Are you sure?', 'Continuing will delete this Trakt List')
    if confirm == True:
        url = "users/{0}/lists/{1}".format(user, list_slug)
        call_trakt(url, is_delete=True)
        trakt_cache.clear_trakt_list_data('my_lists')
        notification('List removed from Trakt', 3000)
        xbmc.executebuiltin("Container.Refresh")
    else: return

def search_trakt_lists():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    mode = params.get('mode')
    page = params.get('new_page') if 'new_page' in params else '1'
    search_title = params.get('search_title') if 'search_title' in params else dialog.input("Search Trakt Lists", type=xbmcgui.INPUT_ALPHANUM)
    if not search_title: return
    lists, pages = call_trakt("search", params={'type': 'list', 'fields': 'name, description', 'query': search_title, 'limit': 50}, pagination=True, page=page)
    icon = os.path.join(icon_directory, "search_trakt_lists.png")
    for item in lists:
        try:
            list_info = item["list"]
            name = list_info["name"]
            user = list_info["username"]
            slug = list_info["ids"]["slug"]
            item_count = list_info["item_count"]
            if list_info['privacy'] == 'private' or item_count == 0: continue
            cm = []
            url_params = {'mode': 'trakt.build_trakt_list', 'user': user, 'slug': slug}
            trakt_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
            trakt_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
            trakt_like_url = {'mode': 'trakt.trakt_like_a_list', 'user': user, 'list_slug': slug}
            trakt_subscriptions_url = {'mode': 'trakt.add_list_to_subscriptions', 'user': user, 'list_slug': slug}
            url = build_url(url_params)
            cm.append(("[B]Add to a Menu[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_selection_url)))
            cm.append(("[B]Add to a Shortcut Folder[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_folder_selection_url)))
            cm.append(("[B]Like this List[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_like_url)))
            cm.append(("[B]Add List to Subscriptions[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_subscriptions_url)))
            display = '[B]' + name + '[/B] - [I]by ' + user + ' - ' + str(item_count) + ' items[/I]'
            listitem = xbmcgui.ListItem(display)
            listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
            listitem.addContextMenuItems(cm)
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    if pages > page:
        new_page = int(page) + 1
        add_dir({'mode': mode, 'search_title': search_title, 'new_page': str(new_page),
            'foldername': mode}, 'Next Page >>', iconImage='item_next.png')
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.main')

def trakt_add_to_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    tmdb_id = params.get('tmdb_id')
    tvdb_id = params.get('tvdb_id')
    imdb_id = params.get('imdb_id')
    db_type = params.get('db_type')
    if db_type == 'movie':
        key, media_key, media_id = ('movies', 'tmdb', int(tmdb_id))
    else:
        key = 'shows'
        media_ids = [(imdb_id, 'imdb'), (tvdb_id, 'tvdb'), (tmdb_id, 'tmdb')]
        media_id, media_key = next(item for item in media_ids if item[0] != 'None')
        if media_id in (tmdb_id, tvdb_id):
            media_id = int(media_id)
    selected = get_trakt_list_selection()
    if selected is not None:
        data = {key: [{"ids": {media_key: media_id}}]}
        if selected['user'] == 'Watchlist':
            add_to_watchlist(data)
        elif selected['user'] == 'Collection':
            add_to_collection(data)
        else:
            user = selected['user']
            slug = selected['slug']
            add_to_list(user, slug, data)
            trakt_cache.clear_trakt_list_contents_data(user=user, list_slug=slug)

def trakt_remove_from_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    tmdb_id = params.get('tmdb_id')
    tvdb_id = params.get('tvdb_id')
    imdb_id = params.get('imdb_id')
    db_type = params.get('db_type')
    if db_type == 'movie':
        key, media_key, media_id = ('movies', 'tmdb', int(tmdb_id))
    else:
        key = 'shows'
        media_ids = [(imdb_id, 'imdb'), (tvdb_id, 'tvdb'), (tmdb_id, 'tmdb')]
        media_id, media_key = next(item for item in media_ids if item[0] != 'None')
        if media_id in (tmdb_id, tvdb_id):
            media_id = int(media_id)
    selected = get_trakt_list_selection()
    if selected is not None:
        data = {key: [{"ids": {media_key: media_id}}]}
        if selected['user'] == 'Watchlist':
            remove_from_watchlist(data)
        elif selected['user'] == 'Collection':
            remove_from_collection(data)
        else:
            user = selected['user']
            slug = selected['slug']
            remove_from_list(user, slug, data)
            trakt_cache.clear_trakt_list_contents_data(user=user, list_slug=slug)

def trakt_like_a_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    user = params.get('user')
    list_slug = params.get('list_slug')
    try:
        call_trakt("/users/{0}/lists/{1}/like".format(user, list_slug), method='post')
        trakt_cache.clear_trakt_list_data('liked_lists')
        notification('List Item Liked', 3000)
    except: notification('{}'.format('Trakt Error Liking List', 3000))

def trakt_unlike_a_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    user = params.get('user')
    list_slug = params.get('list_slug')
    try:
        call_trakt("/users/{0}/lists/{1}/like".format(user, list_slug), method='delete')
        trakt_cache.clear_trakt_list_data('liked_lists')
        notification('List Item Unliked', 3000)
        xbmc.executebuiltin("Container.Refresh")
    except: notification('{}'.format('Trakt Error Unliking List', 3000))

def get_trakt_list_selection(list_choice='none'):
    name = '%s[I]%s[/I]'
    my_lists = sorted([{'name': item["name"], 'display': name % (('[B]PERSONAL:[/B] ' if list_choice else ''), item["name"].upper()), 'user': item["user"]["ids"]["slug"], 'slug': item["ids"]["slug"]} for item in get_trakt_my_lists(build_list=False)], key=lambda k: k['name'])
    if list_choice in ('nav_edit', 'subscriptions'):
        liked_lists = sorted([{'name': item["list"]["name"], 'display': name % ('[B]LIKED:[/B] ', item["list"]["name"].upper()), 'user': item["list"]["user"]["ids"]["slug"], 'slug': item["list"]["ids"]["slug"]} for item in get_trakt_liked_lists(build_list=False)], key=lambda k: (k['display']))
        my_lists.extend(liked_lists)
    if not list_choice == 'nav_edit':
        my_lists.insert(0, {'name': 'Collection', 'display': '[B][I]COLLECTION [/I][/B]', 'user': 'Collection', 'slug': 'Collection'})
        my_lists.insert(0, {'name': 'Watchlist', 'display': '[B][I]WATCHLIST [/I][/B]',  'user': 'Watchlist', 'slug': 'Watchlist'})
    if list_choice == 'subscriptions':
        my_lists.insert(0, {'name': 'NONE', 'display': '[B]NONE[/B]', 'user': 'NONE', 'slug': 'NONE'})
    selection = dialog.select("Select list", [l["display"] for l in my_lists])
    if selection >= 0: return my_lists[selection]
    else: return None

def get_trakt_my_lists(build_list=True):
    from modules.trakt_cache import clear_all_trakt_cache_data
    clear_all_trakt_cache_data(confirm=False)
    my_list_icon = os.path.join(icon_directory, 'traktmylists.png')
    try:
        string = "trakt_my_lists"
        url = {"path": "users/me/lists%s", "with_auth": True, "pagination": False}
        lists = trakt_cache.cache_trakt_object(get_trakt, string, url)
        if not build_list: return lists
        for item in lists:
            cm = []
            name = item["name"]
            user = item["user"]["ids"]["slug"]
            slug = item["ids"]["slug"]
            item_count = item.get('item_count', None)
            if item_count: display_name = '%s (%s)' % (name, item_count)
            else: display_name = name
            url_params = {'mode': 'trakt.build_trakt_list', 'user': user, 'slug': slug}
            trakt_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
            trakt_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
            make_new_list_url = {'mode': 'trakt.make_new_trakt_list'}
            delete_list_url = {'mode': 'trakt.delete_trakt_list', 'user': user, 'list_slug': slug}
            trakt_subscriptions_url = {'mode': 'trakt.add_list_to_subscriptions', 'user': user, 'list_slug': slug}
            url = build_url(url_params)
            cm.append(("[B]Add to a Menu[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_selection_url)))
            cm.append(("[B]Add to a Shortcut Folder[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_folder_selection_url)))
            cm.append(("[B]Make a new Trakt list[/B]",'XBMC.RunPlugin(%s)' % build_url(make_new_list_url)))
            cm.append(("[B]Delete list[/B]",'XBMC.RunPlugin(%s)' % build_url(delete_list_url)))
            cm.append(("[B]Add List to Subscriptions[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_subscriptions_url)))
            listitem = xbmcgui.ListItem(display_name)
            listitem.setArt({'icon': my_list_icon, 'poster': my_list_icon, 'thumb': my_list_icon, 'fanart': fanart, 'banner': my_list_icon})
            listitem.addContextMenuItems(cm)
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.main')

def get_trakt_liked_lists(build_list=True):
    from modules.trakt_cache import clear_all_trakt_cache_data
    clear_all_trakt_cache_data(confirm=False)
    liked_list_icon = os.path.join(icon_directory, 'traktlikedlists.png')
    try:
        string = "trakt_liked_lists"
        url = {"path": "users/likes/lists%s", "params": {'limit': 1000}, "pagination": False, "with_auth": True}
        lists = trakt_cache.cache_trakt_object(get_trakt, string, url)
        if not build_list: return lists
        for item in lists:
            cm = []
            _item = item['list']
            name = _item["name"]
            user = _item["user"]["ids"]["slug"]
            slug = _item["ids"]["slug"]
            item_count = _item.get('item_count', None)
            if item_count: display_name = '%s (%s) - [I]by %s[/I]' % (name, item_count, user)
            else: display_name = '%s - [I]by %s[/I]' % (name, user)
            url_params = {'mode': 'trakt.build_trakt_list', 'user': user, 'slug': slug}
            trakt_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
            trakt_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
            unlike_list_url = {'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug}
            trakt_subscriptions_url = {'mode': 'trakt.add_list_to_subscriptions', 'user': user, 'list_slug': slug}
            url = build_url(url_params)
            listitem = xbmcgui.ListItem(display_name)
            listitem.setArt({'icon': liked_list_icon, 'poster': liked_list_icon, 'thumb': liked_list_icon, 'fanart': fanart, 'banner': liked_list_icon})
            cm.append(("[B]Add to a Menu[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_selection_url)))
            cm.append(("[B]Add to a Shortcut Folder[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_folder_selection_url)))
            cm.append(("[B]Unlike List[/B]",'XBMC.RunPlugin(%s)' % build_url(unlike_list_url)))
            cm.append(("[B]Add List to Subscriptions[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_subscriptions_url)))
            listitem.addContextMenuItems(cm, replaceItems=False)
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.main')

def get_trakt_trending_popular_lists():
    trending_popular_list_icon = os.path.join(icon_directory, 'trakt.png')
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    try:
        list_type = params['list_type']
        string = "trakt_%s_user_lists" % list_type
        path = "lists/%s/" % list_type
        url = {'path': path + "%s", "params": {'limit': 100}}
        lists = cache_object(get_trakt, string, url, False)
        for item in lists:
            cm = []
            _item = item['list']
            name = _item["name"]
            user = _item["user"]["ids"]["slug"]
            slug = _item["ids"]["slug"]
            item_count = _item.get('item_count', None)
            if item_count: display_name = '%s (%s) - [I]by %s[/I]' % (name, item_count, user)
            else: display_name = '%s - [I]by %s[/I]' % (name, user)
            url_params = {'mode': 'trakt.build_trakt_list', 'user': user, 'slug': slug}
            trakt_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
            trakt_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
            unlike_list_url = {'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug}
            trakt_subscriptions_url = {'mode': 'trakt.add_list_to_subscriptions', 'user': user, 'list_slug': slug}
            url = build_url(url_params)
            listitem = xbmcgui.ListItem(display_name)
            listitem.setArt({'icon': trending_popular_list_icon, 'poster': trending_popular_list_icon, 'thumb': trending_popular_list_icon, 'fanart': fanart, 'banner': trending_popular_list_icon})
            cm.append(("[B]Add to a Menu[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_selection_url)))
            cm.append(("[B]Add to a Shortcut Folder[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_folder_selection_url)))
            cm.append(("[B]Unlike List[/B]",'XBMC.RunPlugin(%s)' % build_url(unlike_list_url)))
            cm.append(("[B]Add List to Subscriptions[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_subscriptions_url)))
            listitem.addContextMenuItems(cm, replaceItems=False)
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
    except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.main')

def build_trakt_list():
    from indexers.movies import Movies
    from indexers.tvshows import TVShows
    from modules.nav_utils import paginate_list, cached_page
    from modules.trakt_cache import clear_all_trakt_cache_data
    from apis.trakt_api import sync_watched_trakt_to_fen
    def _add_misc_dir(url_params, list_name='Next Page >>', iconImage='item_next.png'):
        icon = os.path.join(icon_directory, iconImage)
        listitem = xbmcgui.ListItem(list_name)
        listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
        if url_params['mode'] == 'build_navigate_to_page': listitem.addContextMenuItems([("[B]Switch Jump To Action[/B]","XBMC.RunPlugin(%s)" % build_url({'mode': 'toggle_jump_to'}))])
        xbmcplugin.addDirectoryItem(handle=__handle__, url=build_url(url_params), listitem=listitem, isFolder=True)
    clear_all_trakt_cache_data(confirm=False)
    sync_watched_trakt_to_fen()
    paginate = settings.paginate()
    limit = settings.page_limit()
    is_widget = False if 'plugin' in xbmc.getInfoLabel('Container.PluginName') else True
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    user = params.get('user')
    slug = params.get('slug')
    cache_page_string = slug
    letter = params.get('new_letter', 'None')
    cache_page = settings.cache_page()
    page_no = int(params.get('new_page', '1'))
    if cache_page:
        if not 'new_page' in params:
            silent = True if is_widget else False
            retrieved_page = cached_page(cache_page_string, silent=silent)
            if retrieved_page: page_no = retrieved_page
    try:
        original_list = []
        result = get_trakt_list_contents(user, slug)
        for item in result:
            try:
                media_type = item['type']
                if not media_type in ('movie', 'show'): continue
                original_list.append({'media_type': media_type, 'title': item[media_type]['title'], 'media_ids': item[media_type]['ids']})
            except: pass
        if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
        else: final_list, total_pages = original_list, 1
        for item in final_list:
            item['media_id'] = get_trakt_movie_id(item['media_ids']) if item['media_type'] == 'movie' else get_trakt_tvshow_id(item['media_ids'])
        movie_list = [i['media_id'] for i in final_list if i['media_type'] == 'movie']
        show_list = [i['media_id'] for i in final_list if i['media_type'] == 'show']
        content = 'movies' if len(movie_list) > len(show_list) else 'tvshows'
        if total_pages > 2 and not is_widget: _add_misc_dir({'mode': 'build_navigate_to_page', 'db_type': 'Media', 'user': user, 'slug': slug, 'current_page': page_no, 'total_pages': total_pages, 'transfer_mode': 'trakt.build_trakt_list'}, 'Jump To...', 'item_jump.png')
        if len(movie_list) >= 1: Movies(movie_list, action=slug).worker()
        if len(show_list) >= 1: TVShows(show_list, action=slug).worker()
        if total_pages > page_no: _add_misc_dir({'mode': 'trakt.build_trakt_list', 'user': user, 'slug': slug, 'new_page': str(page_no + 1), 'new_letter': letter})
        if cache_page: cached_page(cache_page_string, page_no=page_no)
        xbmcplugin.setContent(__handle__, content)
        xbmcplugin.endOfDirectory(__handle__)
        if params.get('refreshed') == 'true': xbmc.sleep(1500)
        setView('view.trakt_list', content)
    except: notification('List Unavailable', 3000)

def get_trakt_list_contents(user, slug):
    string = "trakt_list_contents_%s_%s" % (user, slug)
    url = {"path": "users/%s/lists/%s/items", "path_insert": (user, slug), "params": {'extended':'full'}, "with_auth": True, "method": "sort_by_headers"}
    return trakt_cache.cache_trakt_object(get_trakt, string, url)

def get_trakt_my_calendar():
    from threading import Thread
    from tikimeta import tvshow_meta, retrieve_user_info
    from modules.indicators_bookmarks import get_watched_info_tv
    from indexers.tvshows import build_episode
    def _process(item, order):
        meta = tvshow_meta('tmdb_id', item['tmdb_id'], meta_user_info)
        episode_item = {"season": item['season'], "episode": item['episode'], "meta": meta, "action": "trakt_calendar",
                        "include_unaired": True, "first_aired": item['first_aired'], 'trakt_calendar': trakt_calendar,
                        "adjust_hours": adjust_hours, "current_adjusted_date": current_adjusted_date, "order": order,
                        "watched_indicators": watched_indicators}
        result.append(build_episode(episode_item, watched_info, use_trakt, meta_user_info))
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    recently_aired = params.get('recently_aired', None)
    if recently_aired:
        trakt_calendar = False
        import datetime
        current_date = settings.adjusted_datetime()
        start = (current_date - datetime.timedelta(days=14)).strftime('%Y-%m-%d')
        finish = 14
    else:
        trakt_calendar = True
        start, finish = settings.trakt_calendar_days()
    threads = []
    result = []
    string = "get_trakt_my_calendar_%s_%s" % (start, str(finish))
    url = {"path": "calendars/my/shows/%s/%s", "path_insert": (start, str(finish)), "with_auth": True, "pagination": False}
    data = trakt_cache.cache_trakt_object(get_trakt, string, url, expiration=3)
    data = [{'sort_title': '%s s%s e%s' % (i['show']['title'], str(i['episode']['season']).zfill(2), str(i['episode']['number']).zfill(2)), 'tmdb_id': get_trakt_tvshow_id(i['show']['ids']), 'season': i['episode']['season'], 'episode': i['episode']['number'], 'first_aired': i['first_aired']} for i in data if i['episode']['season'] > 0]
    data = [i for i in data if i['tmdb_id'] != None]
    data = [i for n, i in enumerate(data) if i not in data[n + 1:]] # remove duplicates
    if trakt_calendar:
        data = sorted(data, key=lambda k: k['sort_title'], reverse=False)
    else:
        try: limit = int(__addon__.getSetting('trakt_widget_limit'))
        except: limit = 20
        data = sorted(data, key=lambda k: k['first_aired'], reverse=True)
        data = data[:limit]
    data = sorted(data, key=lambda k: k['first_aired'], reverse=False)
    watched_info, use_trakt = get_watched_info_tv()
    meta_user_info = retrieve_user_info()
    adjust_hours = int(__addon__.getSetting('datetime.offset'))
    current_adjusted_date = settings.adjusted_datetime(dt=True)
    watched_indicators = settings.watched_indicators()
    window.setProperty('fen_fanart_error', 'true')
    for count, item in enumerate(data): threads.append(Thread(target=_process, args=(item, count)))
    [i.start() for i in threads]
    [i.join() for i in threads]
    r = [i for i in result if i is not None]
    r = sorted(r, key=lambda k: k['order'], reverse=True)
    item_list = [i['listitem'] for i in r]
    for i in item_list: xbmcplugin.addDirectoryItem(__handle__, i[0], i[1], i[2])
    xbmcplugin.setContent(__handle__, 'episodes')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.episode_lists', 'episodes')
    if settings.calendar_focus_today() and trakt_calendar:
        try: index = max([i for i, x in enumerate([i['label'] for i in r]) if '[TODAY]' in x])
        except: index = None
        if index:
            from modules.nav_utils import focus_index
            focus_index(index)

def get_trakt_movie_id(item):
    if item['tmdb']: return item['tmdb']
    from tikimeta import movie_meta_external_id
    tmdb_id = None
    if item['imdb']:
        try:
            meta = movie_meta_external_id('imdb_id', item['imdb'])
            tmdb_id = meta['id']
        except: pass
    return tmdb_id

def get_trakt_tvshow_id(item):
    if item['tmdb']: return item['tmdb']
    from tikimeta import tvshow_meta_external_id
    tmdb_id = None
    if item['imdb']:
        try: 
            meta = tvshow_meta_external_id('imdb_id', item['imdb'])
            tmdb_id = meta['id']
        except: tmdb_id = None
    if not tmdb_id:
        if item['tvdb']:
            try: 
                meta = tvshow_meta_external_id('tvdb_id', item['tvdb'])
                tmdb_id = meta['id']
            except: tmdb_id = None
    return tmdb_id

def trakt_indicators_movies():
    def _process(url):
        result = get_trakt(url)
        for i in result: i.update({'tmdb_id': get_trakt_movie_id(i['movie']['ids'])})
        result = [(i['tmdb_id'], i['movie']['title'], i['last_watched_at']) for i in result if i['tmdb_id'] != None]
        return result
    url = {'path': "sync/watched/movies%s", "with_auth": True, "pagination": False}
    result = trakt_cache.cache_trakt_object(_process, 'trakt_indicators_movies', url)
    return result

def trakt_indicators_tv():
    def _process(dummy_arg):
        result = trakt_tv_watched_raw()
        for i in result: i.update({'tmdb_id': get_trakt_tvshow_id(i['show']['ids'])})
        result = [(i['tmdb_id'], i['show']['aired_episodes'], sum([[(s['number'], e['number']) for e in s['episodes']] for s in i['seasons']], []), i['show']['title'], i['last_watched_at']) for i in result if i['tmdb_id'] != None]
        result = [(int(i[0]), int(i[1]), i[2], i[3], i[4]) for i in result]
        return result
    result = trakt_cache.cache_trakt_object(_process, 'trakt_indicators_tv', '')
    return result

def trakt_tv_watched_raw():
    url = {'path': "users/me/watched/shows?extended=full%s", "with_auth": True, "pagination": False}
    return trakt_cache.cache_trakt_object(get_trakt, 'trakt_tv_watched_raw', url)

def trakt_official_status(db_type):
    if not settings.addon_installed('script.trakt'): return True
    trakt_addon = xbmcaddon.Addon('script.trakt')
    try: authorization = trakt_addon.getSetting('authorization')
    except: authorization = ''
    if authorization == '': return True
    try: exclude_http = trakt_addon.getSetting('ExcludeHTTP')
    except: exclude_http = ''
    if exclude_http in ('true', ''): return True
    media_setting = 'scrobble_movie' if db_type in ('movie', 'movies') else 'scrobble_episode'
    try: scrobble = trakt_addon.getSetting(media_setting)
    except: scrobble = ''
    if scrobble in ('false', ''): return True
    return False

def get_trakt(url):
    result = call_trakt(url['path'] % url.get('path_insert', ''), params=url.get('params', {}), data=url.get('data'), is_delete=url.get('is_delete', False), with_auth=url.get('with_auth', False), method=url.get('method'), pagination=url.get('pagination', True), page=url.get('page'))
    return result[0] if url.get('pagination', True) else result

def make_trakt_slug(name):
    import re
    name = name.strip()
    name = name.lower()
    name = re.sub('[^a-z0-9_]', '-', name)
    name = re.sub('--+', '-', name)
    return name

def sync_watched_trakt_to_fen(refresh=False):
    if refresh: window.setProperty('fen_trakt_sync_complete', 'false')
    if window.getProperty('fen_trakt_sync_complete') == 'true': return
    if settings.watched_indicators() in (0, 2): return
    import os
    from datetime import datetime
    from modules.utils import clean_file_name
    try: from sqlite3 import dbapi2 as database
    except ImportError: from pysqlite2 import dbapi2 as database
    not_home_window = xbmc.getInfoLabel('Container.PluginName')
    profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
    processed_trakt_tv = []
    compare_trakt_tv = []
    try:
        if not_home_window:
            bg_dialog = xbmcgui.DialogProgressBG()
            bg_dialog.create('Trakt & Fen Watched Status', 'Please Wait')
        WATCHED_DB = os.path.join(profile_dir, "watched_status.db")
        settings.check_database(WATCHED_DB)
        dbcon = database.connect(WATCHED_DB)
        dbcur = dbcon.cursor()
        trakt_watched_movies = trakt_indicators_movies()
        trakt_watched_tv = trakt_indicators_tv()
        process_movies = False
        process_tvshows = False
        dbcur.execute("SELECT media_id FROM watched_status WHERE db_type = ?", ('movie',))
        fen_watched_movies = dbcur.fetchall()
        fen_watched_movies = [int(i[0]) for i in fen_watched_movies]
        compare_trakt_movies = [i[0] for i in trakt_watched_movies]
        process_trakt_movies = trakt_watched_movies
        if not sorted(fen_watched_movies) == sorted(compare_trakt_movies): process_movies = True
        if not_home_window: bg_dialog.update(50, 'Trakt & Fen Watched Status', 'Checking Movies Watched Status')
        xbmc.sleep(100)
        dbcur.execute("SELECT media_id, season, episode FROM watched_status WHERE db_type = ?", ('episode',))
        fen_watched_episodes = dbcur.fetchall()
        fen_watched_episodes = [(int(i[0]), i[1], i[2]) for i in fen_watched_episodes]
        for i in trakt_watched_tv:
            for x in i[2]:
                compare_trakt_tv.append((i[0], x[0], x[1]))
                processed_trakt_tv.append((i[0], x[0], x[1], i[3]))
        if not sorted(fen_watched_episodes) == sorted(compare_trakt_tv): process_tvshows = True
        if not_home_window: bg_dialog.update(100, 'Trakt & Fen Watched Status', 'Checking Episodes Watched Status')
        xbmc.sleep(100)
        if not process_movies and not process_tvshows and not_home_window:
            bg_dialog.close()
        if process_movies:
            dbcur.execute("DELETE FROM watched_status WHERE db_type=?", ('movie',))
            for count, i in enumerate(process_trakt_movies):
                try:
                    if not_home_window: bg_dialog.update(int(float(count) / float(len(trakt_watched_movies)) * 100), 'Trakt & Fen Watched Status', 'Syncing Movie Watched Status')
                    last_played = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dbcur.execute("INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", ('movie', str(i[0]), '', '', last_played, clean_file_name(to_utf8(i[1]))))
                except: pass
        if process_tvshows:
            dbcur.execute("DELETE FROM watched_status WHERE db_type=?", ('episode',))
            for count, i in enumerate(processed_trakt_tv):
                try:
                    if not_home_window: bg_dialog.update(int(float(count) / float(len(processed_trakt_tv)) * 100), 'Trakt & Fen Watched Status', 'Syncing Episode Watched Status')
                    last_played = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dbcur.execute("INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", ('episode', str(i[0]), i[1], i[2], last_played, clean_file_name(to_utf8(i[3]))))
                except: pass
        if process_movies or process_tvshows:
            dbcon.commit()
        if not_home_window:
            bg_dialog.close()
            from modules.nav_utils import notification
            notification('Trakt Watched to Fen Watched Sync Complete', time=4000)
        window.setProperty('fen_trakt_sync_complete', 'true')
        __addon__.setSetting('trakt_indicators_active', 'true')
        if refresh: xbmc.executebuiltin("Container.Refresh")
    except:
        if not_home_window:
            try: bg_dialog.close()
            except: pass
        from modules.nav_utils import notification
        notification('Error getting Trakt Watched Info', time=3500)
        pass

