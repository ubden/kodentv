# -*- coding: utf-8 -*-
import xbmcaddon
from datetime import timedelta
from modules import fen_cache
# from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
_cache = fen_cache.FenCache()

def add_to_search_history(search_name, search_list):
    try:
        result = []
        cache = _cache.get(search_list)
        if cache: result = cache
        if search_name in result: result.remove(search_name)
        result.insert(0, search_name)
        result = result[:10]
        _cache.set(search_list, result, expiration=timedelta(days=365))
    except: return

def remove_from_history():
    import xbmc
    import sys
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    from modules.nav_utils import notification
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    try:
        result = _cache.get(params['setting_id'])
        result.remove(params.get('name'))
        _cache.set(params['setting_id'], result, expiration=timedelta(days=365))
        notification('[B]%s[/B] Removed from History' % params.get('name').upper(), 3500)
        xbmc.executebuiltin('Container.Refresh')
    except: return

def clear_search_history():
    import xbmcgui
    from modules.nav_utils import notification
    dialog = xbmcgui.Dialog()
    choice_list = [('Delete Movie Search History', 'movie_queries', 'Movie'),
                   ('Delete TV Show Search History', 'tvshow_queries', 'TV Show'), 
                   ('Delete People Search History', 'people_queries', 'People'),
                   ('Delete Furk Video Search History', 'furk_video_queries', 'Furk Video'), 
                   ('Delete Furk Audio Search History', 'furk_audio_queries', 'Furk Audio'), 
                   ('Delete Easynews Video Search History', 'easynews_video_queries', 'Easynews Video')]
    try:
        selection = dialog.select('Choose Search History to Delete', [i[0] for i in choice_list])
        if selection < 0: return
        setting = choice_list[selection][1]
        _cache.set(setting, '', expiration=timedelta(days=365))
        notification("%s Search History Removed" % choice_list[selection][2], 3500)
    except: return

def search_history():
    import xbmc, xbmcgui, xbmcplugin
    import sys, os
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    try: from urllib import unquote
    except ImportError: from urllib.parse import unquote
    from modules.nav_utils import build_url, setView
    from modules.settings import get_theme
    try:
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        (search_setting, display_title) = ('movie_queries', 'MOVIE') if params['action'] == 'movie' \
                                     else ('tvshow_queries', 'TVSHOW') if params['action'] == 'tvshow' \
                                     else ('people_queries', 'PEOPLE') if params['action'] == 'people' \
                                     else ('furk_video_queries', 'FURK VIDEO') if params['action'] == 'furk_video' \
                                     else ('furk_audio_queries', 'FURK AUDIO') if params['action'] == 'furk_audio' \
                                     else ('easynews_video_queries', 'EASYNEWS VIDEO') if params['action'] == 'easynews_video' \
                                     else ''
        history = _cache.get(search_setting)
        if not history: return
    except: return
    icon = os.path.join(get_theme(), 'search.png')
    fanart = os.path.join(xbmc.translatePath(__addon__.getAddonInfo('path')), 'fanart.png')
    for h in history:
        try:
            cm = []
            name = unquote(h)
            url_params = {'mode': 'build_movie_list', 'action': 'tmdb_movies_search', 'query': name} if params['action'] == 'movie' \
                    else {'mode': 'build_tvshow_list', 'action': 'tmdb_tv_search', 'query': name} if params['action'] == 'tvshow' \
                    else {'mode': 'people_search.search', 'actor_name': name} if params['action'] == 'people' \
                    else {'mode': 'furk.search_furk', 'db_type': 'video', 'query': name} if params['action'] == 'furk_video' \
                    else {'mode': 'furk.search_furk', 'db_type': 'audio', 'music': True, 'query': name} if params['action'] == 'furk_audio' \
                    else {'mode': 'easynews.search_easynews', 'query': name} if params['action'] == 'easynews_video' \
                    else ''
            display = '[B]%s SEARCH : [/B]' % display_title + name 
            url = build_url(url_params)
            cm.append(("[B]Remove from history[/B]",'XBMC.RunPlugin(%s?mode=%s&setting_id=%s&name=%s)' \
                % (sys.argv[0], 'remove_from_history', search_setting, name)))
            listitem = xbmcgui.ListItem(display)
            listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
            listitem.addContextMenuItems(cm)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(int(sys.argv[1]), 'addons')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    setView('view.main')
    