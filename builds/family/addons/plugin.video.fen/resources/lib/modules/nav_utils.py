# -*- coding: utf-8 -*-
import xbmc, xbmcaddon
import sys, os
# from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')

def build_navigate_to_page():
    import xbmcgui
    import json
    import ast
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    from modules.settings import get_theme, nav_jump_use_alphabet
    use_alphabet = nav_jump_use_alphabet()
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    if use_alphabet:
        start_list = [chr(i) for i in range(97,123)]
        choice_list = [xbmcgui.ListItem(i.upper(), "[I]Jump to %s Starting with '%s'[/I]" % (params.get('db_type'), i.upper()), iconImage=os.path.join(get_theme(), 'item_jump.png')) for i in start_list]
    else:
        start_list = [str(i) for i in range(1, int(params.get('total_pages'))+1)]
        start_list.remove(params.get('current_page'))
        choice_list = [xbmcgui.ListItem('Page %s' % i, '[I]Jump to Page %s[/I]' % i, iconImage=os.path.join(get_theme(), 'item_jump.png')) for i in start_list]
    chosen_start = xbmcgui.Dialog().select('Fen', choice_list, useDetails=True)
    xbmc.sleep(500)
    if chosen_start < 0: return
    new_start = start_list[chosen_start]
    if use_alphabet:
        new_page = ''
        new_letter = new_start
    else:
        new_page = new_start
        new_letter = None
    final_params = {'mode': params.get('transfer_mode', ''),
                    'action': params.get('transfer_action', ''),
                    'new_page': new_page,
                    'new_letter': new_letter,
                    'media_type': params.get('media_type', ''),
                    'query': params.get('query', ''),
                    'actor_id': params.get('actor_id', ''),
                    'user': params.get('user', ''),
                    'slug': params.get('slug', ''),
                    'final_params': params.get('final_params', ''),
                    'refreshed': 'true'}
    url_params = {'mode': 'container_update', 'final_params': json.dumps(final_params)}
    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % build_url(url_params))

def paginate_list(item_list, page, letter, limit=20):
    from modules.utils import chunks
    def _get_start_index(letter):
        if letter == 't':
            try:
                beginswith_tuple = ('s', 'the s', 'a s', 'an s')
                indexes = [i for i,v in enumerate(title_list) if v.startswith(beginswith_tuple)]
                start_index = indexes[-1:][0] + 1
            except: start_index = None
        else:
            beginswith_tuple = (letter, 'the %s' % letter, 'a %s' % letter, 'an %s' % letter)
            try: start_index = next(i for i,v in enumerate(title_list) if v.startswith(beginswith_tuple))
            except: start_index = None
        return start_index
    if letter != 'None':
        import itertools
        title_list = [i['title'].lower() for i in item_list]
        start_list = [chr(i) for i in range(97,123)]
        letter_index = start_list.index(letter)
        base_list = [element for element in list(itertools.chain.from_iterable([val for val in itertools.izip_longest(start_list[letter_index:], start_list[:letter_index][::-1])])) if element != None]
        for i in base_list:
            start_index = _get_start_index(i)
            if start_index: break
        item_list = item_list[start_index:]
    pages = list(chunks(item_list, limit))
    total_pages = len(pages)
    return pages[page - 1], total_pages

def cached_page(action, page_no=None, silent=False):
    import datetime
    from modules.fen_cache import FenCache
    _cache = FenCache()
    string = 'fen_page_cache_%s' % action
    if page_no:
        _cache.set(string, page_no, expiration=datetime.timedelta(days=365))
        return
    cache = _cache.get(string)
    if cache:
        if not silent: notification('Auto [B]Page %d[/B] Selected' % cache, 4000)
        return cache
    else: return None

def cached_page_clear(action=None, silent=False):
    import xbmcvfs
    try: from sqlite3 import dbapi2 as database
    except ImportError: from pysqlite2 import dbapi2 as database
    profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
    if not xbmcvfs.exists(profile_dir): xbmcvfs.mkdirs(profile_dir)
    FEN_DB = os.path.join(profile_dir, "fen_cache.db")
    dbcon = database.connect(FEN_DB)
    dbcur = dbcon.cursor()
    if action: dbcur.execute("DELETE FROM fencache WHERE id=?", ('fen_page_cache_%s' % action,))
    else: dbcur.execute("DELETE FROM fencache WHERE id LIKE 'fen_page_cache_%'")
    dbcon.commit()
    dbcon.close()
    if not silent: notification('Page Cache Cleared')

def container_update(params=None):
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    import json
    params = params if params else dict(parse_qsl(sys.argv[2].replace('?','')))
    xbmc.sleep(500)
    try: xbmc.executebuiltin('Container.Update(%s)' % build_url(json.loads(params['final_params'])))
    except: xbmc.executebuiltin('Container.Update(%s)' % build_url(params['final_params']))

def container_refresh(params=None):
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    import json
    params = params if params else dict(parse_qsl(sys.argv[2].replace('?','')))
    xbmc.sleep(500)
    try: xbmc.executebuiltin('Container.Refresh(%s)' % build_url(json.loads(params['final_params'])))
    except: xbmc.executebuiltin('Container.Refresh(%s)' % build_url(params['final_params']))

def get_kodi_version():
    return int(xbmc.getInfoLabel("System.BuildVersion")[0:2])

def show_busy_dialog():
    if get_kodi_version() >= 18: return xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    else: return xbmc.executebuiltin('ActivateWindow(busydialog)')

def hide_busy_dialog():
    if get_kodi_version() >= 18: return xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    else: return xbmc.executebuiltin('Dialog.Close(busydialog)')

def close_all_dialog():
    xbmc.executebuiltin('Dialog.Close(all,true)')

def clear_all_window_properties():
    import xbmcgui
    window = xbmcgui.Window(10000)
    trakt_sync = window.getProperty('fen_trakt_sync_complete')
    refresh_trakt_info = window.getProperty('fen_refresh_trakt_info_complete')
    window.clearProperties()
    window.setProperty('fen_trakt_sync_complete', trakt_sync)
    window.setProperty('fen_refresh_trakt_info_complete', refresh_trakt_info)

def sleep(time):
    xbmc.sleep(time)

def focus_index(index):
    import xbmcgui
    import time
    time.sleep(1)
    current_window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    focus_id = current_window.getFocusId()
    try: current_window.getControl(focus_id).selectItem(index)
    except: pass

def play_trailer(url, all_trailers=[]):
    if all_trailers:
        import xbmcgui
        import json
        from modules.utils import clean_file_name, to_utf8
        all_trailers = to_utf8(json.loads(all_trailers))
        video_choice = xbmcgui.Dialog().select("Youtube Videos...", [clean_file_name(i['name']) for i in all_trailers])
        if video_choice < 0: return
        url = 'plugin://plugin.video.youtube/play/?video_id=%s' % all_trailers[video_choice].get('key')
    try: xbmc.executebuiltin('RunPlugin(%s)' % url)
    except: notification('Error Playing Trailer')

def show_text(heading=None, text_file=None, usemono=False):
    import xbmcgui
    from ast import literal_eval
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    heading = params.get('heading') if 'heading' in params else heading
    text_file = params.get('text_file') if 'text_file' in params else text_file
    usemono = literal_eval(params.get('usemono')) if 'usemono' in params else usemono
    text = open(text_file).read()
    try: xbmcgui.Dialog().textviewer(heading, text, usemono=usemono)
    except: xbmcgui.Dialog().textviewer(heading, text)
    finally: return

def show_image(image_url=None):
    if not image_url:
        try: from urlparse import parse_qsl
        except ImportError: from urllib.parse import parse_qsl
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        image_url = params['image_url']
    xbmc.executebuiltin('ShowPicture(%s)' % image_url)

def show_bio(actor_id=None):
    import xbmcgui
    from apis.tmdb_api import tmdb_people_biography
    from modules.utils import calculate_age
    def _make_biography():
        age = None
        heading = 'FEN Biography'
        name = bio_info.get('name')
        place_of_birth = bio_info.get('place_of_birth')
        biography = bio_info.get('biography')
        birthday = bio_info.get('birthday')
        deathday = bio_info.get('deathday')
        if deathday: age = calculate_age(birthday, '%Y-%m-%d', deathday)
        elif birthday: age = calculate_age(birthday, '%Y-%m-%d')
        text = '\n[COLOR dodgerblue][B]NAME:[/B][/COLOR] %s' % name
        if place_of_birth: text += '\n\n[COLOR dodgerblue][B]PLACE OF BIRTH[/B][/COLOR]: %s' % place_of_birth
        if birthday: text += '\n\n[COLOR dodgerblue][B]BIRTHDAY[/B][/COLOR]: %s' % birthday
        if deathday: text += '\n\n[COLOR dodgerblue][B]DIED:[/B][/COLOR] %s, aged %s' % (deathday, age)
        elif age: text += '\n\n[COLOR dodgerblue][B]AGE:[/B][/COLOR] %s' % age
        if biography: text += '\n\n[COLOR dodgerblue][B]BIOGRAPHY:[/B][/COLOR]\n%s' % biography
        return heading, text
    dialog = xbmcgui.Dialog()
    if not actor_id:
        try: from urlparse import parse_qsl
        except ImportError: from urllib.parse import parse_qsl
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        actor_id = params['actor_id']
    bio_info = tmdb_people_biography(actor_id)
    if bio_info.get('biography', None) in ('', None):
        bio_info = tmdb_people_biography(actor_id, 'en')
    if not bio_info: return notification('No Biography Found')
    heading, text = _make_biography()
    return dialog.textviewer(heading, text)

def movie_reviews(tmdb_id, rootname, poster):
    from apis.tmdb_api import tmdb_movies_reviews
    reviews_info = tmdb_movies_reviews(tmdb_id)
    total_results = reviews_info['total_results']
    if total_results == 0:
        return notification('No Reviews Found for Movie', 3500)
    import xbmcgui
    dialog = xbmcgui.Dialog()
    review_list = []
    all_reviews = reviews_info['results']
    for item in all_reviews:
        line1 = 'Review by: [B]%s[/B]' % item['author']
        line2 = '[I]%s...[/I]' % item['content'][:60]
        icon = poster
        listitem = xbmcgui.ListItem(line1, line2)
        listitem.setArt({'icon': icon})
        listitem.setProperty('review_id', str(item['id']))
        listitem.setProperty('reviewer_name', item['author'])
        listitem.setProperty('review_content', item['content'])
        review_list.append(listitem)
    selection = dialog.select('FEN - Choose Review...', review_list, useDetails=True)
    if selection >= 0:
        review_id = review_list[selection].getProperty('review_id')
        reviewer_name = review_list[selection].getProperty('reviewer_name')
        review_content = review_list[selection].getProperty('review_content')
    else: return
    heading = '%s Review by [B]%s[/B]' % (rootname, reviewer_name)
    dialog.textviewer(heading, review_content)
    if total_results > 1: return movie_reviews(tmdb_id, rootname, poster)

def open_settings(query):
    try:
        xbmc.sleep(500)
        kodi_version = get_kodi_version()
        button = (-100) if kodi_version <= 17 else (100)
        control = (-200) if kodi_version <= 17 else (80)
        hide_busy_dialog()
        menu, function = query.split('.')
        xbmc.executebuiltin('Addon.OpenSettings(plugin.video.fen)')
        xbmc.executebuiltin('SetFocus(%i)' % (int(menu) - button))
        xbmc.executebuiltin('SetFocus(%i)' % (int(function) - control))
    except: return

def extended_info_open(db_type, tmdb_id):
    if db_type == 'movie': function = 'extendedinfo'
    else: function = 'extendedtvinfo'
    return xbmc.executebuiltin('RunScript(script.extendedinfo,info=%s,id=%s)' % (function, tmdb_id))

def toggle_setting(setting_id=None, setting_value=None, refresh=False):
    if not setting_id:
        try: from urlparse import parse_qsl
        except ImportError: from urllib.parse import parse_qsl
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        setting_id = params.get('setting_id')
        setting_value = params.get('setting_value')
        refresh = params.get('refresh')
    __addon__.setSetting(setting_id, setting_value)
    if refresh:
        xbmc.executebuiltin('Container.Refresh')

def build_url(query):
    try: from urllib import urlencode
    except ImportError: from urllib.parse import urlencode
    from modules.utils import to_utf8
    return sys.argv[0] + '?' + urlencode(to_utf8(query))

def notification(line1, time=5000, icon=__addon__.getAddonInfo('icon'), sound=False):
    import xbmcgui
    xbmcgui.Dialog().notification('Fen', line1, icon, time, sound)

def add_dir(url_params, list_name, iconImage='DefaultFolder.png', fanartImage=__addon__.getAddonInfo('fanart'), isFolder=True):
    import xbmcgui, xbmcplugin
    from modules.settings import get_theme
    icon = os.path.join(get_theme(), iconImage)
    url = build_url(url_params)
    listitem = xbmcgui.ListItem(list_name)
    listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanartImage, 'banner': icon})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=listitem, isFolder=isFolder)

def setView(view_type, content='files'):
    if not 'fen' in xbmc.getInfoLabel('Container.PluginName'): return
    import time
    from modules.settings import check_database
    try: from sqlite3 import dbapi2 as database
    except: from pysqlite2 import dbapi2 as database
    profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
    views_db = os.path.join(profile_dir, "views.db")
    check_database(views_db)
    t = 0
    try:
        xbmc.sleep(500)
        dbcon = database.connect(views_db)
        dbcur = dbcon.cursor()
        while not xbmc.getInfoLabel('Container.Content') == content:
            if xbmc.abortRequested == True: break
            if not 'fen' in xbmc.getInfoLabel('Container.PluginName'): break
            t += 0.01
            if t >= 60.0: break
            time.sleep(0.01)
        dbcur.execute("SELECT view_id FROM views WHERE view_type = ?", (str(view_type),))
        view_id = dbcur.fetchone()[0]
        xbmc.executebuiltin("Container.SetViewMode(%s)" % str(view_id))
        dbcon.close()
    except: return

def link_folders(service, folder_name, action):
    import xbmcgui
    from modules import fen_cache
    def _get_media_type():
        from modules.settings import get_theme
        for item in [('movie', 'Movie', 'movies.png'), ('tvshow', 'TV Show', 'tv.png')]:
            line1 = '[B]%s[/B]' % item[1]
            line2 = '[I]Link this Folder to a %s[/I]' % item[1]
            icon = os.path.join(get_theme(), item[2])
            listitem = xbmcgui.ListItem(line1, line2)
            listitem.setArt({'icon': icon})
            listitem.setProperty('media_type', item[0])
            media_type_list.append(listitem)
        chosen_media_type = dialog.select("FEN Folder Link: Select Media Type", media_type_list, useDetails=True)
        return chosen_media_type
    dialog = xbmcgui.Dialog()
    _cache = fen_cache.FenCache()
    string = 'FEN_%s_%s' % (service, folder_name)
    current_link = _cache.get(string)
    profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
    media_type_list = []
    if action == 'remove':
        if not current_link: return dialog.ok('FEN Folder Link', 'No Movie/TV Show Linked to this Folder.')
        if not dialog.yesno('FEN Folder Link', 'Clear Link to [B]%s[/B]?' % current_link): return
        from modules.settings import check_database
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        window = xbmcgui.Window(10000)
        cache_file = os.path.join(profile_dir, "fen_cache.db")
        check_database(cache_file)
        dbcon = database.connect(cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fencache WHERE id=?", (string,))
        dbcon.commit()
        dbcon.close()
        window.clearProperty(string)
        if service == 'FOLDER':
            clear_cache('folder_scraper', silent=True)
        xbmc.executebuiltin("Container.Refresh")
        return dialog.ok('FEN Folder Link', 'Link Removed.')
    if current_link:
        if not dialog.yesno('FEN Folder Link', 'This Folder is Already Linked to Movie/TV Show:', '[B]%s[/B]' % current_link, 'Do you wish to Link this Folder to Different Movie/TV Show?'): return
    media_type = _get_media_type()
    if media_type < 0: return
    media_type = media_type_list[media_type].getProperty('media_type')
    title = dialog.input("Enter %s" % media_type).lower()
    if not title: return
    from apis.tmdb_api import tmdb_movies_title_year, tmdb_tv_title_year
    year = dialog.input("Enter Year (Optional)", type=xbmcgui.INPUT_NUMERIC)
    function = tmdb_movies_title_year if media_type == 'movie' else tmdb_tv_title_year
    results = function(title, year)['results']
    if len(results) == 0: return dialog.ok('FEN Folder Link', 'No Matching Titles to Select.', 'Please Try a Different Search Term.')
    name_key = 'title' if media_type == 'movie' else 'name'
    released_key = 'release_date' if media_type == 'movie' else 'first_air_date'
    choice_list = []
    for item in results:
        title = item[name_key]
        try: year = item[released_key].split('-')[0]
        except: year = ''
        if year: rootname = '%s (%s)' % (title, year)
        else: rootname = title
        line1 = rootname
        line2 = '[I]%s[/I]' % item['overview']
        icon = 'http://image.tmdb.org/t/p/w92%s' % item['poster_path'] if item.get('poster_path') else xbmc.translatePath(__addon__.getAddonInfo('icon'))
        listitem = xbmcgui.ListItem(line1, line2)
        listitem.setArt({'icon': icon})
        listitem.setProperty('rootname', rootname)
        choice_list.append(listitem)
    chosen_title = dialog.select("FEN Folder Link: Select Correct Title", choice_list, useDetails=True)
    if chosen_title < 0: return
    from datetime import timedelta
    rootname = choice_list[chosen_title].getProperty('rootname')
    _cache.set(string, rootname, expiration=timedelta(days=365))
    if service == 'FOLDER':
        clear_cache('folder_scraper', silent=True)
    xbmc.executebuiltin("Container.Refresh")
    return dialog.ok('FEN Folder Link (%s)' % media_type.upper(), '[B]%s[/B]' % rootname, 'Linked to this Folder.')

def clean_settings():
    import xbmcgui, xbmcvfs
    import xml.etree.ElementTree as ET
    def _make_content(dict_object):
        if kodi_version >= 18:
            content = '<settings version="2">'
            for item in dict_object:
                if item['id'] in active_settings:
                    if 'default' in item and 'value' in item: content += '\n    <setting id="%s" default="%s">%s</setting>' % (item['id'], item['default'], item['value'])
                    elif 'default' in item: content += '\n    <setting id="%s" default="%s"></setting>' % (item['id'], item['default'])
                    elif 'value' in item: content += '\n    <setting id="%s">%s</setting>' % (item['id'], item['value'])
                    else: content += '\n    <setting id="%s"></setting>'
                else: removed_settings.append(item)
        else:
            content = '<settings>'
            for item in dict_object:
                if item['id'] in active_settings:
                    if 'value' in item: content += '\n    <setting id="%s" value="%s" />' % (item['id'], item['value'])
                    else: content += '\n    <setting id="%s" value="" />' % item['id']
                else: removed_settings.append(item)
        content += '\n</settings>'
        return content
    close_all_dialog()
    xbmc.sleep(500)
    progressDialog = xbmcgui.DialogProgress()
    progressDialog.create('Please Wait...', '', '', '')
    progressDialog.update(0, '  ', '', '')
    kodi_version = get_kodi_version()
    addon_ids = ['plugin.video.fen', 'script.module.tikimeta', 'script.module.openscrapers']
    addon_names = [xbmcaddon.Addon(id=i).getAddonInfo('name') for i in addon_ids]
    addon_dirs = [xbmc.translatePath(xbmcaddon.Addon(id=i).getAddonInfo('path')) for i in addon_ids]
    profile_dirs = [xbmc.translatePath(xbmcaddon.Addon(id=i).getAddonInfo('profile')) for i in addon_ids]
    active_settings_xmls = [os.path.join(xbmc.translatePath(xbmcaddon.Addon(id=i).getAddonInfo('path')), 'resources', 'settings.xml') for i in addon_ids]
    try: params = zip(addon_names, profile_dirs, active_settings_xmls) # Python 2
    except: params = list(zip(addon_names, profile_dirs, active_settings_xmls)) # Python 3
    for addon in params:
        try:
            if xbmc.abortRequested == True: return sys.exit()
            try:
                if progressDialog.iscanceled():
                    break
            except Exception:
                pass
            current_progress = params.index(addon)+1
            removed_settings = []
            active_settings = []
            current_user_settings = []
            root = ET.parse(addon[2]).getroot()
            for item in root.findall('./category/setting'):
                setting_id = item.get('id')
                if setting_id:
                    active_settings.append(setting_id)
            settings_xml = os.path.join(addon[1], 'settings.xml')
            root = ET.parse(settings_xml).getroot()
            for item in root:
                dict_item = {}
                setting_id = item.get('id')
                setting_default = item.get('default')
                if kodi_version >= 18: setting_value = item.text
                else: setting_value = item.get('value')
                dict_item['id'] = setting_id
                if setting_value: dict_item['value'] = setting_value
                if setting_default: dict_item['default'] = setting_default
                current_user_settings.append(dict_item)
            new_content = _make_content(current_user_settings)
            nfo_file = xbmcvfs.File(settings_xml, 'w')
            nfo_file.write(new_content)
            nfo_file.close()
            percent = int((current_progress/float(len(params)))*100)
            line2 = 'Cleaned Addon: [B]%s[/B]' % addon[0]
            line3 = 'Removed Settings: [B]%s[/B]' % len(removed_settings)
            progressDialog.update(percent, '', line2, line3)
        except:
            notification('Error Cleaning [B]%s[/B] Settings.' % addon[0], 2000)
        xbmc.sleep(1200)
    try:
        progressDialog.close()
    except Exception:
        pass
    xbmcgui.Dialog().ok('Fen', 'All Settings Cleared.')

def backup_settings():
    import xbmcgui, xbmcvfs
    import os
    from modules.zfile import ZipFile
    from modules.utils import multiselect_dialog
    from modules.utils import logger
    try:
        user_data = [('Settings File', '.xml'), ('Database Files', '.db')]
        preselect = [0,1]
        subs_folders = (__addon__.getSetting('movies_directory'), __addon__.getSetting('tv_shows_directory'))
        default_subs_folders = (xbmc.translatePath('special://profile/addon_data/plugin.video.fen/Movie Subscriptions/'),
                                xbmc.translatePath('special://profile/addon_data/plugin.video.fen/TVShow Subscriptions/'))
        any_subs = list(set(subs_folders) & set(default_subs_folders))
        if any_subs:
            user_data.append(('Subscriptions Files', '.strm'))
            preselect.append(2)
        dialog_list = [i[0] for i in user_data]
        function_list = [i[1] for i in user_data]
        backup_exts = multiselect_dialog('Choose Which Data to Backup', dialog_list, function_list, preselect=preselect)
        if not backup_exts: return
        dialog = xbmcgui.Dialog()
        profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
        backup_path = xbmc.translatePath(__addon__.getSetting('backup_directory'))
        if backup_path in ('', None): return dialog.ok('FEN','', 'Please enter a backup path in settings.', '')
        temp_zip = xbmc.translatePath(os.path.join(profile_dir, 'fen_settings.zip'))
        backup_zip = xbmc.translatePath(os.path.join(backup_path, 'fen_settings.zip'))
        root_len = len(profile_dir)
        line1 = 'User Data Successfully Backed Up.'
        try:
            with ZipFile(temp_zip, 'w') as zippy:
                for folder_name, subfolders, filenames in os.walk(profile_dir):
                    for item in filenames:
                        if any(item.endswith(i) for i in backup_exts):
                            file_path = os.path.join(folder_name, item)
                            zippy.write(file_path, file_path[root_len:])
            xbmcvfs.copy(temp_zip, backup_zip)
            xbmcvfs.delete(temp_zip)
        except Exception as e:
            logger('ERROR backing up Fen User Data OPENING ZIP.', e)
            line1 = 'ERROR backing up Fen User Data.'
    except Exception as e:
        logger('ERROR backing up Fen User Data MAIN.', e)
        line1 = 'ERROR backing up Fen User Data.'
    dialog.ok('FEN','', line1, '')

def restore_settings():
    import xbmcgui, xbmcvfs
    import os
    from modules.zfile import ZipFile
    dialog = xbmcgui.Dialog()
    profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
    backup_path = xbmc.translatePath(__addon__.getSetting('backup_directory'))
    if backup_path in ('', None): return dialog.ok('FEN','', 'There is no backup path in settings.', '')
    temp_zip = xbmc.translatePath(os.path.join(profile_dir, 'fen_settings.zip'))
    backup_zip = xbmc.translatePath(os.path.join(backup_path, 'fen_settings.zip'))
    if not xbmcvfs.exists(backup_zip): return dialog.ok('FEN','', 'There is no backup zip in the backup filepath set.', '')
    line1 = 'User Data Successfully Restored.'
    try:
        xbmcvfs.copy(backup_zip, temp_zip)
        with ZipFile(temp_zip, "r") as zip_file:
            zip_file.extractall(profile_dir)
        xbmcvfs.delete(temp_zip)
    except:
        from modules.utils import logger
        logger('error', e)
        line1 = 'ERROR restoring Fen User Data.'
    dialog.ok('FEN','', line1, '')

def settings_layout(settings_type=None):
    import xbmcvfs
    if not settings_type: settings_type = __addon__.getSetting('settings_layout')
    addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
    content_source = 'settings_basic.xml' if settings_type == 'Basic' else 'settings_advanced.xml'
    active_settings_xml = os.path.join(addon_dir, 'resources', 'settings.xml')
    template_settings_xml = os.path.join(addon_dir, 'resources', 'settings_files', content_source)
    f = xbmcvfs.File(template_settings_xml)
    new_content = f.read()
    f.close()
    f = xbmcvfs.File(active_settings_xml, 'w')
    f.write(str(new_content))
    f.close()
    return

def similar_recommendations_choice():
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    import json
    from modules.utils import selection_dialog
    import tikimeta
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    db_type = params.get('db_type')
    try: meta_user_info = json.loads(params.get('meta_user_info'))
    except: meta_user_info= tikimeta.retrieve_user_info()
    meta_type = 'movie' if db_type == 'movies' else 'tvshow'
    dl = ['Similar', 'Recommended']
    fl = ['trakt_%s_related' % db_type, 'tmdb_%s_recommendations' % db_type]
    string = 'Please Choose Movie Search Option:' if db_type == 'movies' else 'Please Choose TV Show Search Option:'
    mode = 'build_%s_list' % meta_type
    choice = selection_dialog(dl, fl, string)
    if not choice: return
    try:
        sim_recom_params = {'mode': mode, 'action': choice, 'sim_recom_tmdb': params.get('sim_recom_tmdb'), 'sim_recom_imdb': params.get('sim_recom_imdb'), 'sim_recom_name': params.get('sim_recom_name'), 'from_search': params.get('from_search')}
        xbmc.executebuiltin('XBMC.Container.Update(%s)' % build_url(sim_recom_params))
    except: return

def clear_and_rescrape(play_params):
    import json
    for item in ('internal_scrapers', 'external_scrapers'): clear_cache(item, silent=True)
    play_params = json.loads(play_params)
    play_params['autoplay'] = False
    return xbmc.executebuiltin('RunPlugin(%s)' % build_url(play_params))

def refresh_cached_data(db_type=None, id_type=None, media_id=None, from_list=False):
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    import tikimeta
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    try:
        tikimeta.delete_cache_item(params.get('db_type', db_type), params.get('id_type', id_type), params.get('media_id', media_id))
        if params.get('from_list', from_list): return True
        notification('Cache refreshed for item')
        xbmc.executebuiltin('Container.Refresh')
    except:
        if params.get('from_list', from_list): return False
        notification('Refreshing of Cache failed for item', 4500)

def remove_unwanted_info_keys(dict_item):
    remove = ('fanart_added', 'art', 'cast', 'item_no', 'poster', 'rootname', 'imdb_id', 'tmdb_id', 'tvdb_id',
        'all_trailers', 'total_episodes', 'total_seasons', 'total_watched', 'total_unwatched', 'airedSeasons',
        'poster', 'fanart', 'banner', 'clearlogo', 'clearart', 'landscape', 'discart', 'last_episode_to_air',
        'status', 'season_data', 'tvdb_data', 'tvdb_summary', 'in_production', 'next_episode_to_air',
        'guest_stars', 'thumb', 'gif_poster', 'kyradb_added', 'background', 'bookmark', 'ep_name', 'media_id',
        'query', 'url', 'vid_type', 'use_animated_poster', 'original_title', 'search_title', 'fanarttv_poster',
        'fanarttv_fanart')
    for k in remove: dict_item.pop(k, None)
    return dict_item

def clear_cache(cache_type, silent=False):
    import xbmcgui
    profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
    clear_all_window_properties()
    if cache_type == 'meta':
        from tikimeta import delete_meta_cache
        if not delete_meta_cache(silent=silent): return
        description = 'Meta Data'
    elif cache_type == 'internal_scrapers':
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear all Internal Scraper Results.'): return
        from apis import furk_api
        from apis import easynews_api
        furk_api.clear_media_results_database()
        easynews_api.clear_media_results_database()
        for item in ('pm_cloud', 'rd_cloud', 'ad_cloud', 'folder_scraper'): clear_cache(item, silent=True)
        description = 'Internal Scraper Results'
    elif cache_type == 'external_scrapers':
        from modules.external_source_utils import deleteProviderCache
        from modules.debrid import DebridCache
        data = deleteProviderCache(silent=silent)
        debrid_cache = DebridCache().clear_database()
        if not (data, debrid_cache) == ('success', 'success'): return
        description = 'External Scraper Results'
    elif cache_type == 'trakt':
        from modules.trakt_cache import clear_all_trakt_cache_data
        if not clear_all_trakt_cache_data(silent=silent): return
        description = 'Trakt Cache'
    elif cache_type == 'pages':
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear all Browsed Pages History.'): return
        if not cached_page_clear(silent=silent): return
        description = 'Browsed Pages Cache'
    elif cache_type == 'pm_cloud':
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear the Premiumize Cloud Cache.'): return
        from apis.premiumize_api import PremiumizeAPI
        if not PremiumizeAPI().clear_cache(): return
        description = 'Premiumize Cloud Cache'
    elif cache_type == 'rd_cloud':
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear the Real Debrid Cloud Cache.'): return
        from apis.real_debrid_api import RealDebridAPI
        if not RealDebridAPI().clear_cache(): return
        description = 'Real Debrid Cloud Cache'
    elif cache_type == 'ad_cloud':
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear the All Debrid Cloud Cache.'): return
        from apis.alldebrid_api import AllDebridAPI
        if not AllDebridAPI().clear_cache(): return
        description = 'All Debrid Cloud Cache'
    elif cache_type == 'folder_scraper':
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear the Folder Scrpaers Cache.'): return
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        fen_cache_file = os.path.join(profile_dir, 'fen_cache.db')
        dbcon = database.connect(fen_cache_file)
        dbcur = dbcon.cursor()
        try:
            dbcur.execute("DELETE FROM fencache WHERE id LIKE 'fen_FOLDERSCRAPER_%'")
            dbcon.commit()
            dbcon.close()
        except: pass
    else: # 'list'
        import xbmcvfs
        LIST_DATABASE = os.path.join(profile_dir, 'fen_cache.db')
        if not xbmcvfs.exists(LIST_DATABASE): return
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear all List Data.'): return
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        from modules.settings import media_lists
        media_lists = media_lists()
        dbcon = database.connect(LIST_DATABASE)
        dbcur = dbcon.cursor()
        sql = """SELECT id from fencache where id LIKE """
        for item in media_lists: sql = sql + "'" + item + "'" + ' OR id LIKE '
        sql = sql[:-12]
        dbcur.execute(sql)
        results = dbcur.fetchall()
        remove_list = [str(i[0]) for i in results]
        for item in remove_list:
            dbcur.execute("""DELETE FROM fencache WHERE id=?""", (item,))
        dbcon.commit()
        dbcon.execute("VACUUM")
        dbcon.close()
        description = 'List Data'
    if not silent: notification('%s Cleared' % description)

def clear_all_cache():
    import xbmcgui
    dialog = xbmcgui.Dialog()
    if not dialog.yesno('Are you sure?','Fen will Clear All Caches.'): return
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create('Please Wait', '')
    caches = [('meta', 'Meta Cache'), ('internal_scrapers', 'Internal Scrapers Cache'), ('external_scrapers', 'External Scrapers Cache'), ('trakt', 'Trakt Cache'), ('pages', 'Browsed Pages Cache'), ('pm_cloud', 'PM Cloud Cache'), ('rd_cloud', 'RD Cloud Cache'), ('list', 'List Data Cache')]
    for count, cache_type in enumerate(caches, 1):
        progress_dialog.update(int(float(count) / float(len(caches)) * 100), 'Clearing....', cache_type[1])
        clear_cache(cache_type[0], silent=True)
        xbmc.sleep(400)
    progress_dialog.close()
    xbmc.sleep(500)
    dialog.ok('Fen', 'All Caches Cleared')

def refresh_icon():
    import xbmcvfs, xbmcgui
    try: from sqlite3 import dbapi2 as database
    except ImportError: from pysqlite2 import dbapi2 as database
    try:
        icon_path = xbmc.translatePath(os.path.join(ADDON_PATH, 'icon.png'))
        thumbs_folder = xbmc.translatePath('special://thumbnails')
        TEXTURE_DB = xbmc.translatePath(os.path.join('special://database', 'Textures13.db'))
        dbcon = database.connect(TEXTURE_DB)
        dbcur = dbcon.cursor()
        dbcur.execute("""SELECT cachedurl FROM texture WHERE url = ?""", (icon_path,))
        image = dbcur.fetchone()[0]
        dbcon.close()
        removal_path = os.path.join(thumbs_folder, image)
        if xbmcgui.Dialog().yesno("Fen", 'Add-on Icon about to be refreshed.', 'Continue?', '', 'No', 'Yes'):
            xbmcvfs.delete(removal_path)
            xbmc.sleep(200)
            xbmc.executebuiltin('ReloadSkin()')
            xbmc.sleep(500)
            notice = '[B]Success!![/B] Icon refreshed.'
        else: return
    except:
        notice = '[B]Error!![/B] deleting icon from database'
    notification(notice)

def years():
    from datetime import datetime
    year = datetime.today().year
    return range(year, 1899, -1)

oscar_winners_tmdb_ids = [496243, 490132, 399055, 376867, 314365, 194662, 76203, 68734, 74643, 45269, 12162, 12405, 6977, 1422, 1640, 70, 122, 1574, 453, 98,
                        14, 1934, 597, 409, 197, 13, 424, 33, 274, 581, 403, 380, 746, 792, 606, 279, 11050, 783, 9443, 16619,
                        12102, 11778, 703, 1366, 510, 240, 9277, 238, 1051, 11202, 3116, 17917, 10633, 874, 15121, 11113, 5769, 947, 1725, 284,
                        665, 17281, 826, 2897, 15919, 654, 11426, 27191, 2769, 705, 25430, 23383, 33667, 887, 28580, 17661, 27367, 289, 43266, 223,
                        770, 34106, 43278, 43277, 12311, 3078, 56164, 33680, 42861, 143, 65203, 28966, 631]

movie_certifications = ('G','PG','PG-13','R','NC-17', 'NR')

tvshow_certifications = ('tv-y','tv-y7','tv-g','tv-pg','tv-14','tv-ma')

languages = [('Arabic', 'ar'),         ('Bosnian', 'bs'),
             ('Bulgarian', 'bg'),      ('Chinese', 'zh'),
             ('Croatian', 'hr'),       ('Dutch', 'nl'),
             ('English', 'en'),        ('Finnish', 'fi'),
             ('French', 'fr'),         ('German', 'de'),
             ('Greek', 'el'),          ('Hebrew', 'he'),
             ('Hindi ', 'hi'),         ('Hungarian', 'hu'),
             ('Icelandic', 'is'),      ('Italian', 'it'),
             ('Japanese', 'ja'),       ('Korean', 'ko'),
             ('Macedonian', 'mk'),     ('Norwegian', 'no'),
             ('Persian', 'fa'),        ('Polish', 'pl'),
             ('Portuguese', 'pt'),     ('Punjabi', 'pa'),
             ('Romanian', 'ro'),       ('Russian', 'ru'),
             ('Serbian', 'sr'),        ('Slovenian', 'sl'),
             ('Spanish', 'es'),        ('Swedish', 'sv'),
             ('Turkish', 'tr'),        ('Ukrainian', 'uk')]

regions = [{'code': 'AF', 'name': 'Afghanistan'},         {'code': 'AL', 'name': 'Albania'},
           {'code': 'DZ', 'name': 'Algeria'},             {'code': 'AQ', 'name': 'Antarctica'},
           {'code': 'AR', 'name': 'Argentina'},           {'code': 'AM', 'name': 'Armenia'},
           {'code': 'AU', 'name': 'Australia'},           {'code': 'AT', 'name': 'Austria'},
           {'code': 'BD', 'name': 'Bangladesh'},          {'code': 'BY', 'name': 'Belarus'},
           {'code': 'BE', 'name': 'Belgium'},             {'code': 'BR', 'name': 'Brazil'},
           {'code': 'BG', 'name': 'Bulgaria'},            {'code': 'KH', 'name': 'Cambodia'},
           {'code': 'CA', 'name': 'Canada'},              {'code': 'CL', 'name': 'Chile'},
           {'code': 'CN', 'name': 'China'},               {'code': 'HR', 'name': 'Croatia'},
           {'code': 'CZ', 'name': 'Czech Republic'},      {'code': 'DK', 'name': 'Denmark'},
           {'code': 'EG', 'name': 'Egypt'},               {'code': 'FI', 'name': 'Finland'},
           {'code': 'FR', 'name': 'France'},              {'code': 'DE', 'name': 'Germany'},
           {'code': 'GR', 'name': 'Greece'},              {'code': 'HK', 'name': 'Hong Kong'},
           {'code': 'HU', 'name': 'Hungary'},             {'code': 'IS', 'name': 'Iceland'},
           {'code': 'IN', 'name': 'India'},               {'code': 'ID', 'name': 'Indonesia'},
           {'code': 'IR', 'name': 'Iran'},                {'code': 'IQ', 'name': 'Iraq'},
           {'code': 'IE', 'name': 'Ireland'},             {'code': 'IL', 'name': 'Israel'},
           {'code': 'IT', 'name': 'Italy'},               {'code': 'JP', 'name': 'Japan'},
           {'code': 'MY', 'name': 'Malaysia'},            {'code': 'NP', 'name': 'Nepal'},
           {'code': 'NL', 'name': 'Netherlands'},         {'code': 'NZ', 'name': 'New Zealand'},
           {'code': 'NO', 'name': 'Norway'},              {'code': 'PK', 'name': 'Pakistan'},
           {'code': 'PY', 'name': 'Paraguay'},            {'code': 'PE', 'name': 'Peru'},
           {'code': 'PH', 'name': 'Philippines'},         {'code': 'PL', 'name': 'Poland'},
           {'code': 'PT', 'name': 'Portugal'},            {'code': 'PR', 'name': 'Puerto Rico'},
           {'code': 'RO', 'name': 'Romania'},             {'code': 'RU', 'name': 'Russian Federation'},
           {'code': 'SA', 'name': 'Saudi Arabia'},        {'code': 'RS', 'name': 'Serbia'},
           {'code': 'SG', 'name': 'Singapore'},           {'code': 'SK', 'name': 'Slovakia'},
           {'code': 'SI', 'name': 'Slovenia'},            {'code': 'ZA', 'name': 'South Africa'},
           {'code': 'ES', 'name': 'Spain'},               {'code': 'LK', 'name': 'Sri Lanka'},
           {'code': 'SE', 'name': 'Sweden'},              {'code': 'CH', 'name': 'Switzerland'},
           {'code': 'TH', 'name': 'Thailand'},            {'code': 'TR', 'name': 'Turkey'},
           {'code': 'UA', 'name': 'Ukraine'},             {'code': 'AE', 'name': 'United Arab Emirates'},
           {'code': 'GB', 'name': 'United Kingdom'},      {'code': 'US', 'name': 'United States'},
           {'code': 'UY', 'name': 'Uruguay'},             {'code': 'VE', 'name': 'Venezuela'},
           {'code': 'VN', 'name': 'Viet Nam'},            {'code': 'YE', 'name': 'Yemen'},
           {'code': 'ZW', 'name': 'Zimbabwe'}]

movie_genres = {'Action': ['28', 'genre_action.png'],              'Adventure': ['12', 'genre_adventure.png'],
                'Animation': ['16', 'genre_animation.png'],        'Comedy': ['35', 'genre_comedy.png'],
                'Crime': ['80', 'genre_crime.png'],                'Documentary': ['99', 'genre_documentary.png'],
                'Drama': ['18', 'genre_drama.png'],                'Family': ['10751', 'genre_family.png'],
                'Fantasy': ['14', 'genre_fantasy.png'],            'History': ['36', 'genre_history.png'],
                'Horror': ['27', 'genre_horror.png'],              'Music': ['10402', 'genre_music.png'],
                'Mystery': ['9648', 'genre_mystery.png'],          'Romance': ['10749', 'genre_romance.png'],
                'Science Fiction': ['878', 'genre_scifi.png'],     'TV Movie': ['10770', 'genre_soap.png'],
                'Thriller': ['53', 'genre_thriller.png'],          'War': ['10752', 'genre_war.png'], 
                'Western': ['37', 'genre_western.png']}

tvshow_genres = {'Action & Adventure': ['10759', 'genre_action.png'],     'Animation': ['16', 'genre_animation.png'],
                'Comedy': ['35', 'genre_comedy.png'],                     'Crime': ['80', 'genre_crime.png'],
                'Documentary': ['99', 'genre_documentary.png'],           'Drama': ['18', 'genre_drama.png'],
                'Family': ['10751', 'genre_family.png'],                  'Kids': ['10762', 'genre_kids.png'],
                'Mystery': ['9648', 'genre_mystery.png'],                 'News':['10763', 'genre_news.png'],
                'Reality': ['10764', 'genre_reality.png'],                'Sci-Fi & Fantasy': ['10765', 'genre_scifi.png'],
                'Soap': ['10766', 'genre_soap.png'],                      'Talk': ['10767', 'genre_talk.png'],
                'War & Politics': ['10768', 'genre_war.png'],             'Western': ['37', 'genre_western.png']}

networks = [{"id":54,"name":"Disney Channel","logo": "https://i.imgur.com/ZCgEkp6.png"},          {"id":44,"name":"Disney XD","logo": "https://i.imgur.com/PAJJoqQ.png"},
            {"id":2,"name":"ABC","logo": "https://i.imgur.com/qePLxos.png"},                      {"id":493,"name":"BBC America","logo": "https://i.imgur.com/TUHDjfl.png"},
            {"id":6,"name":"NBC","logo": "https://i.imgur.com/yPRirQZ.png"},                      {"id":13,"name":"Nickelodeon","logo": "https://i.imgur.com/OUVoqYc.png"},
            {"id":14,"name":"PBS","logo": "https://i.imgur.com/r9qeDJY.png"},                     {"id":16,"name":"CBS","logo": "https://i.imgur.com/8OT8igR.png"},
            {"id":19,"name":"FOX","logo": "https://i.imgur.com/6vc0Iov.png"},                     {"id":21,"name":"The WB","logo": "https://i.imgur.com/rzfVME6.png"},
            {"id":24,"name":"BET","logo": "https://i.imgur.com/ZpGJ5UQ.png"},                     {"id":30,"name":"USA Network","logo": "https://i.imgur.com/Doccw9E.png"},
            {"id":32,"name":"CBC","logo": "https://i.imgur.com/unQ7WCZ.png"},                     {"id":173,"name":"AT-X","logo": "https://i.imgur.com/JshJYGN.png"},
            {"id":33,"name":"MTV","logo": "https://i.imgur.com/QM6DpNW.png"},                     {"id":34,"name":"Lifetime","logo": "https://i.imgur.com/tvYbhen.png"},
            {"id":35,"name":"Nick Junior","logo": "https://i.imgur.com/leuCWYt.png"},             {"id":41,"name":"TNT","logo": "https://i.imgur.com/WnzpAGj.png"},
            {"id":43,"name":"National Geographic","logo": "https://i.imgur.com/XCGNKVQ.png"},     {"id":47,"name":"Comedy Central","logo": "https://i.imgur.com/ko6XN77.png"},
            {"id":49,"name":"HBO","logo": "https://i.imgur.com/Hyu8ZGq.png"},                     {"id":55,"name":"Spike","logo": "https://i.imgur.com/BhXYytR.png"},
            {"id":67,"name":"Showtime","logo": "https://i.imgur.com/SawAYkO.png"},                {"id":56,"name":"Cartoon Network","logo": "https://i.imgur.com/zmOLbbI.png"},
            {"id":65,"name":"History Channel","logo": "https://i.imgur.com/LEMgy6n.png"},         {"id":84,"name":"TLC","logo": "https://i.imgur.com/c24MxaB.png"},
            {"id":68,"name":"TBS","logo": "https://i.imgur.com/RVCtt4Z.png"},                     {"id":71,"name":"The CW","logo": "https://i.imgur.com/Q8tooeM.png"},
            {"id":74,"name":"Bravo","logo": "https://i.imgur.com/TmEO3Tn.png"},                   {"id":76,"name":"E!","logo": "https://i.imgur.com/3Delf9f.png"},
            {"id":77,"name":"Syfy","logo": "https://i.imgur.com/9yCq37i.png"},                    {"id":80,"name":"Adult Swim","logo": "https://i.imgur.com/jCqbRcS.png"},
            {"id":91,"name":"Animal Planet","logo": "https://i.imgur.com/olKc4RP.png"},           {"id":110,"name":"CTV","logo": "https://i.imgur.com/qUlyVHz.png"},
            {"id":129,"name":"A&E","logo": "https://i.imgur.com/xLDfHjH.png"},                    {"id":158,"name":"VH1","logo": "https://i.imgur.com/IUtHYzA.png"},
            {"id":174,"name":"AMC","logo": "https://i.imgur.com/ndorJxi.png"},                    {"id":928,"name":"Crackle","logo": "https://i.imgur.com/53kqZSY.png"},
            {"id":202,"name":"WGN America","logo": "https://i.imgur.com/TL6MzgO.png"},            {"id":209,"name":"Travel Channel","logo": "https://i.imgur.com/mWXv7SF.png"},
            {"id":213, "name":"Netflix","logo": "https://i.imgur.com/jI5c3bw.png"},               {"id":251,"name":"Audience","logo": "https://i.imgur.com/5Q3mo5A.png"},
            {"id":270,"name":"SundanceTV","logo": "https://i.imgur.com/qldG5p2.png"},             {"id":318,"name":"Starz","logo": "https://i.imgur.com/Z0ep2Ru.png"},
            {"id":359,"name":"Cinemax","logo": "https://i.imgur.com/zWypFNI.png"},                {"id":364,"name":"truTV","logo": "https://i.imgur.com/HnB3zfc.png"},
            {"id":384,"name":"Hallmark Channel","logo": "https://i.imgur.com/zXS64I8.png"},       {"id":397,"name":"TV Land","logo": "https://i.imgur.com/1nIeDA5.png"},
            {"id":1024,"name":"Amazon","logo": "https://i.imgur.com/ru9DDlL.png"},                {"id":1267,"name":"Freeform","logo": "https://i.imgur.com/f9AqoHE.png"},
            {"id":4,"name":"BBC One","logo": "https://i.imgur.com/u8x26te.png"},                  {"id":332,"name":"BBC Two","logo": "https://i.imgur.com/SKeGH1a.png"},
            {"id":3,"name":"BBC Three","logo": "https://i.imgur.com/SDLeLcn.png"},                {"id":100,"name":"BBC Four","logo": "https://i.imgur.com/PNDalgw.png"},
            {"id":214,"name":"Sky One","logo": "https://i.imgur.com/xbgzhPU.png"},                {"id":9,"name":"ITV","logo": "https://i.imgur.com/5Hxp5eA.png"},
            {"id":26,"name":"Channel 4","logo": "https://i.imgur.com/6ZA9UHR.png"},               {"id":99,"name":"Channel 5","logo": "https://i.imgur.com/5ubnvOh.png"},
            {"id":136,"name":"E4","logo": "https://i.imgur.com/frpunK8.png"},                     {"id":210,"name":"HGTV","logo": "https://i.imgur.com/INnmgLT.png"},
            {"id":453,"name":"Hulu","logo": "https://i.imgur.com/uSD2Cdw.png"},                   {"id":1436,"name":"YouTube Red","logo": "https://i.imgur.com/ZfewP1Y.png"},
            {"id":64,"name":"Discovery Channel","logo": "https://i.imgur.com/8UrXnAB.png"},       {"id":2739,"name":"Disney +","logo": "https://i.imgur.com/DVrPgbM.png"},
            {"id":2552,"name":"Apple TV +","logo": "https://i.imgur.com/fAQMVNp.png"},            {"id":2697,"name":"Acorn TV","logo": "https://i.imgur.com/fSWB5gB.png"}]

