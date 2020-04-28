# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import sys, os
import urllib
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
from apis.real_debrid_api import RealDebridAPI
from modules import fen_cache
from modules.settings import get_theme
from modules.nav_utils import build_url, setView
from modules.utils import clean_file_name, clean_title, normalize, supported_video_extensions
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
icon_directory = get_theme()
default_rd_icon = os.path.join(icon_directory, 'realdebrid.png')
fanart = os.path.join(addon_dir, 'fanart.png')

RealDebrid = RealDebridAPI()
_cache = fen_cache.FenCache()

def rd_torrent_cloud():
    try: my_cloud_files = RealDebrid.user_cloud()
    except: my_cloud_files = None
    if not my_cloud_files: return
    my_cloud_files = [i for i in my_cloud_files if i['status'] == 'downloaded']
    for count, item in enumerate(my_cloud_files, 1):
        try:
            cm = []
            folder_name = item['filename']
            normalized_folder_name = normalize(folder_name)
            string = 'FEN_RD_%s' % normalized_folder_name
            link_folders_add = {'mode': 'link_folders', 'service': 'RD', 'folder_name': normalized_folder_name, 'action': 'add'}
            link_folders_remove = {'mode': 'link_folders', 'service': 'RD', 'folder_name': normalized_folder_name, 'action': 'remove'}
            current_link = _cache.get(string)
            if current_link: ending = '[COLOR=limegreen][B][I]\n      (Linked to %s)[/I][/B][/COLOR]' % current_link
            else: ending = ''
            display = '%02d | [B]FOLDER[/B] | [I]%s [/I]%s' % (count, clean_file_name(normalized_folder_name).upper(), ending)
            url_params = {'mode': 'real_debrid.browse_rd_cloud', 'id': item['id']}
            url = build_url(url_params)
            cm.append(("[B]Link Movie/TV Show[/B]",'RunPlugin(%s)' % build_url(link_folders_add)))
            cm.append(("[B]Clear Movie/TV Show Link[/B]",'RunPlugin(%s)' % build_url(link_folders_remove)))
            listitem = xbmcgui.ListItem(display)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'icon': default_rd_icon, 'poster': default_rd_icon, 'thumb': default_rd_icon, 'fanart': fanart, 'banner': default_rd_icon})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.premium')

def rd_downloads():
    from modules.utils import jsondate_to_datetime
    try: my_downloads = RealDebrid.downloads()
    except: my_downloads = None
    if not my_downloads: return
    extensions = supported_video_extensions()
    my_downloads = [i for i in my_downloads if i['download'].lower().endswith(tuple(extensions))]
    for count, item in enumerate(my_downloads, 1):
        try:
            cm = []
            datetime_object = jsondate_to_datetime(item['generated'], "%Y-%m-%dT%H:%M:%S.%fZ", remove_time=True)
            filename = item['filename']
            name = clean_file_name(filename).upper()
            size = float(int(item['filesize']))/1073741824
            display = '%02d | %.2f GB | %s  | [I]%s [/I]' % (count, size, datetime_object, name)
            url_link = item['download']
            url_params = {'mode': 'media_play', 'url': url_link, 'rootname': 'video'}
            down_file_params = {'mode': 'download_file', 'name': name, 'url': url_link,
                                'db_type': 'realdebrid_direct_file', 'image': default_rd_icon}
            cm.append(("[B]Download File[/B]",'XBMC.RunPlugin(%s)' % build_url(down_file_params)))
            url = build_url(url_params)
            listitem = xbmcgui.ListItem(display)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'icon': default_rd_icon, 'poster': default_rd_icon, 'thumb': default_rd_icon, 'fanart': fanart, 'banner': default_rd_icon})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.premium')

def browse_rd_cloud(folder_id):
    try:
        torrent_files = RealDebrid.user_cloud_info(folder_id)
    except: return
    extensions = supported_video_extensions()
    try:
        file_info = [i for i in torrent_files['files'] if i['path'].lower().endswith(tuple(extensions))]
        file_urls = torrent_files['links']
        for c, i in enumerate(file_info):
            try: i.update({'url_link': file_urls[c]})
            except: pass
        pack_info = sorted(file_info, key=lambda k: k['path'])
    except: return xbmcgui.Dialog().ok('Fen - Real Debrid', 'Cannot display Malformed Pack.')
    for count, item in enumerate(pack_info, 1):
        try:
            cm = []
            name = item['path']
            if name.startswith('/'): name = name.split('/')[-1]
            name = clean_file_name(name).upper()
            url_link = item['url_link']
            if url_link.startswith('/'): url_link = 'http' + url_link
            size = float(int(item['bytes']))/1073741824
            display = '%02d | [B]FILE[/B] | %.2f GB | [I]%s [/I]' % (count, size, name)
            url_params = {'mode': 'real_debrid.resolve_rd', 'url': url_link}
            url = build_url(url_params)
            down_file_params = {'mode': 'download_file', 'name': name, 'url': url_link,
                                'db_type': 'realdebrid_file', 'image': default_rd_icon}
            cm.append(("[B]Download File[/B]",'XBMC.RunPlugin(%s)' % build_url(down_file_params)))
            listitem = xbmcgui.ListItem(display)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'icon': default_rd_icon, 'poster': default_rd_icon, 'thumb': default_rd_icon, 'fanart': fanart, 'banner': default_rd_icon})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.premium')

def rd_external_browser(magnet, filtering_list):
    import re
    try:
        from HTMLParser import HTMLParser
    except ImportError:
        from html.parser import HTMLParser
    try:
        episode_match = False
        torrent_id = None
        torrent_keys = []
        extensions = supported_video_extensions()
        magnet_url = HTMLParser().unescape(magnet)
        r = re.search('''magnet:.+?urn:([a-zA-Z0-9]+):([a-zA-Z0-9]+)''', str(magnet), re.I)
        infoHash = r.group(2).lower()
        torrent_files = RealDebrid.check_hash(infoHash)
        torrent_files = torrent_files[infoHash]['rd'][0]
        try: files_tuple = sorted([(k, v['filename'].lower()) for k,v in torrent_files.items() if v['filename'].lower().endswith(tuple(extensions))])
        except: return None
        files_tuple = sorted(files_tuple)
        for i in files_tuple:
            if any(x in i[1] for x in filtering_list):
                episode_match = True
            torrent_keys.append(i[0])
        if not episode_match: return None
        if not torrent_keys: return None
        torrent_keys = ','.join(torrent_keys)
        torrent = RealDebrid.add_magnet(magnet_url)
        torrent_id = torrent['id']
        RealDebrid.add_torrent_select(torrent_id, torrent_keys)
        torrent_files = RealDebrid.user_cloud_info(torrent_id)
        file_info = [i for i in torrent_files['files'] if i['path'].lower().endswith(tuple(extensions))]
        file_urls = torrent_files['links']
        pack_info = [dict(i.items() + [('url_link', file_urls[c])]) for c, i in enumerate(file_info)]
        pack_info = sorted(pack_info, key=lambda k: k['path'])
        for item in pack_info:
            filename = clean_title(item['path'])
            if any(x in filename for x in filtering_list):
                correct_result = item
                break
        url_link = correct_result['url_link']
        RealDebrid.delete_torrent(torrent_id)
        return resolve_rd(url_link, play=False)
    except:
        if torrent_id: RealDebrid.delete_torrent(torrent_id)
        return None

def resolve_rd(url, play=True):
    resolved_link = RealDebrid.unrestrict_link(url)
    if not play: return resolved_link
    url_params = {'mode': 'media_play', 'url': resolved_link, 'rootname': 'video'}
    return xbmc.executebuiltin('XBMC.RunPlugin(%s)' % build_url(url_params))

def rd_account_info():
    from datetime import datetime
    import time
    dialog = xbmcgui.Dialog()
    try:
        account_info = RealDebrid.account_info()
        resformat = "%Y-%m-%dT%H:%M:%S.%fZ"
        try: expires = datetime.strptime(account_info['expiration'], resformat)
        except TypeError: expires = datetime(*(time.strptime(account_info['expiration'], resformat)[0:6]))
        days_remaining = (expires - datetime.today()).days
        heading = 'REAL DEBRID'
        body = []
        body.append('[B]Account:[/B] %s' % account_info['email'])
        body.append('[B]Username:[/B] %s' % account_info['username'])
        body.append('[B]Status:[/B] %s' % account_info['type'].capitalize())
        body.append('[B]Expires:[/B] %s' % expires)
        body.append('[B]Days Remaining:[/B] %s' % days_remaining)
        body.append('[B]Fidelity Points:[/B] %s' % account_info['points'])
        return dialog.select(heading, body)
    except Exception as e:
        return dialog.ok('Fen', 'Error Getting Real Debrid Info..', str(e))
