# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import sys, os
import json
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
from apis.alldebrid_api import AllDebridAPI
from modules import fen_cache
from modules.settings import get_theme
from modules.nav_utils import build_url, setView
from modules.utils import clean_file_name, normalize, supported_video_extensions
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
icon_directory = get_theme()
default_ad_icon = os.path.join(icon_directory, 'alldebrid.png')
fanart = os.path.join(addon_dir, 'fanart.png')
dialog = xbmcgui.Dialog()

AllDebrid = AllDebridAPI()
_cache = fen_cache.FenCache()

def ad_torrent_cloud(folder_id=None):
    cloud_dict = AllDebrid.user_cloud()['magnets']
    cloud_dict = [i for i in cloud_dict if i['statusCode'] == 4]
    for count, item in enumerate(cloud_dict, 1):
        try:
            cm = []
            folder_name = item['filename']
            normalized_folder_name = normalize(folder_name)
            string = 'FEN_AD_%s' % normalized_folder_name
            link_folders_add = {'mode': 'link_folders', 'service': 'AD', 'folder_name': normalized_folder_name, 'action': 'add'}
            link_folders_remove = {'mode': 'link_folders', 'service': 'AD', 'folder_name': normalized_folder_name, 'action': 'remove'}
            current_link = _cache.get(string)
            if current_link: ending = '[COLOR=limegreen][B][I]\n      (Linked to %s)[/I][/B][/COLOR]' % current_link
            else: ending = ''
            display = '%02d | [B]FOLDER[/B] | [I]%s [/I]%s' % (count, clean_file_name(normalized_folder_name).upper(), ending)
            url_params = {'mode': 'alldebrid.browse_ad_cloud', 'folder': json.dumps(item)}
            url = build_url(url_params)
            cm.append(("[B]Link Movie/TV Show[/B]",'RunPlugin(%s)' % build_url(link_folders_add)))
            cm.append(("[B]Clear Movie/TV Show Link[/B]",'RunPlugin(%s)' % build_url(link_folders_remove)))
            listitem = xbmcgui.ListItem(display)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'icon': default_ad_icon, 'poster': default_ad_icon, 'thumb': default_ad_icon, 'fanart': fanart, 'banner': default_ad_icon})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.premium')

def browse_ad_cloud(folder):
    final_files = []
    extensions = supported_video_extensions()
    torrent_folder = json.loads(folder)
    links = torrent_folder['links']
    links = [i for i in links if i['filename'].lower().endswith(tuple(extensions))]
    for count, item in enumerate(links, 1):
        try:
            cm = []
            url_link = item['link']
            name = clean_file_name(item['filename']).upper()
            size = item['size']
            display_size = float(int(size))/1073741824
            display = '%02d | %.2f GB | [I]%s [/I]' % (count, display_size, name)
            url_params = {'mode': 'alldebrid.resolve_ad', 'url': url_link}
            url = build_url(url_params)
            down_file_params = {'mode': 'download_file', 'name': name, 'url': url_link,
                                'db_type': 'alldebrid_file', 'image': default_ad_icon}
            cm.append(("[B]Download File[/B]",'XBMC.RunPlugin(%s)' % build_url(down_file_params)))
            listitem = xbmcgui.ListItem(display)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'icon': default_ad_icon, 'poster': default_ad_icon, 'thumb': default_ad_icon, 'fanart': fanart, 'banner': default_ad_icon})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.premium')

def resolve_ad(url, play=True):
    resolved_link = AllDebrid.unrestrict_link(url)
    if not play: return resolved_link
    url_params = {'mode': 'media_play', 'url': resolved_link, 'rootname': 'video'}
    return xbmc.executebuiltin('XBMC.RunPlugin(%s)' % build_url(url_params))

def ad_account_info():
    from datetime import datetime
    try:
        account_info = AllDebrid.account_info()['user']
        username = account_info['username']
        email = account_info['email']
        status = 'Premium' if account_info['isPremium'] else 'Not Active'
        expires = datetime.fromtimestamp(account_info['premiumUntil'])
        days_remaining = (expires - datetime.today()).days
        heading = 'ALLDEBRID'
        body = []
        body.append('[B]Username:[/B] %s' % username)
        body.append('[B]Email:[/B] %s' % email)
        body.append('[B]Status:[/B] %s' % status)
        body.append('[B]Expires:[/B] %s' % expires)
        body.append('[B]Days Remaining:[/B] %s' % days_remaining)
        return dialog.select(heading, body)
    except Exception as e:
        return dialog.ok('Fen', 'Error Getting AllDebrid Info..', e)

