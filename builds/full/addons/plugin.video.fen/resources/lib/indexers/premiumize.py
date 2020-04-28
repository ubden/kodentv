# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import sys, os
import re
import json
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
from apis.premiumize_api import PremiumizeAPI
from modules.settings import get_theme
from modules.nav_utils import build_url, setView
from modules.utils import clean_file_name, normalize, supported_video_extensions
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
icon_directory = get_theme()
default_pm_icon = os.path.join(icon_directory, 'premiumize.png')
fanart = os.path.join(addon_dir, 'fanart.png')
dialog = xbmcgui.Dialog()

Premiumize = PremiumizeAPI()

def pm_torrent_cloud(folder_id=None, folder_name=None):
    try:
        extensions = supported_video_extensions()
        cloud_files = Premiumize.user_cloud(folder_id)['content']
        cloud_files = [i for i in cloud_files if ('link' in i and i['link'].lower().endswith(tuple(extensions))) or i['type'] == 'folder']
        cloud_files = sorted(cloud_files, key=lambda k: k['name'])
        cloud_files = sorted(cloud_files, key=lambda k: k['type'], reverse=True)
    except: return
    for count, item in enumerate(cloud_files, 1):
        try:
            cm = []
            file_type = item['type']
            name = clean_file_name(item['name']).upper()
            rename_params = {'mode': 'premiumize.rename', 'file_type': file_type, 'id': item['id'], 'name': item['name']}
            if file_type == 'folder':
                size = 0
                display = '%02d | [B]%s[/B] | [I]%s [/I]' % (count, file_type.upper(), name)
                url_params = {'mode': 'premiumize.pm_torrent_cloud', 'id': item['id'], 'folder_name': normalize(item['name'])}
            else:
                url_link = item['link']
                if url_link.startswith('/'): url_link = 'https' + url_link
                size = item['size']
                display_size = float(int(size))/1073741824
                display = '%02d | [B]%s[/B] | %.2f GB | [I]%s [/I]' % (count, file_type.upper(), display_size, name)
                url_params = {'mode': 'media_play', 'url': url_link, 'rootname': 'video'}
                down_file_params = {'mode': 'download_file', 'name': item['name'], 'url': url_link,
                                    'db_type': 'premiumize_file', 'image': default_pm_icon}
                cm.append(("[B]Download File[/B]",'XBMC.RunPlugin(%s)' % build_url(down_file_params)))
            cm.append(("[B]Rename %s[/B]" % file_type.capitalize(),'XBMC.RunPlugin(%s)' % build_url(rename_params)))
            url = build_url(url_params)
            listitem = xbmcgui.ListItem(display)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'icon': default_pm_icon, 'poster': default_pm_icon, 'thumb': default_pm_icon, 'fanart': fanart, 'banner': default_pm_icon})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.premium')

def pm_transfers():
    extensions = supported_video_extensions()
    transfer_files = Premiumize.transfers_list()['transfers']
    for count, item in enumerate(transfer_files, 1):
        try:
            cm = []
            file_type = 'folder' if item['file_id'] is None else 'file'
            name = clean_file_name(item['name']).upper()
            status = item['status']
            progress = item['progress']
            if status == 'finished': progress = 100
            else:
                try:
                    progress = re.findall('\.(\d+)', str(progress))[0]
                    progress = progress[:2]
                except: progress = ''
            if file_type == 'folder':
                display = '%02d | %s%% | [B]%s[/B] | [I]%s [/I]' % (count, str(progress), file_type.upper(), name)
                url_params = {'mode': 'premiumize.pm_torrent_cloud', 'id': item['folder_id'], 'folder_name': normalize(item['name'])}
            else:
                details = Premiumize.get_item_details(item['file_id'])
                url_link = details['link']
                if url_link.startswith('/'): url_link = 'https' + url_link
                size = details['size']
                display_size = float(int(size))/1073741824
                display = '%02d | %s%% | [B]%s[/B] | %.2f GB | [I]%s [/I]' % (count, str(progress), file_type.upper(), display_size, name)
                url_params = {'mode': 'media_play', 'url': url_link, 'rootname': 'video'}
                down_file_params = {'mode': 'download_file', 'name': item['name'], 'url': url_link,
                                    'db_type': 'premiumize_file', 'image': default_pm_icon}
                cm.append(("[B]Download File[/B]",'XBMC.RunPlugin(%s)' % build_url(down_file_params)))
            url = build_url(url_params)
            listitem = xbmcgui.ListItem(display)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'icon': default_pm_icon, 'poster': default_pm_icon, 'thumb': default_pm_icon, 'fanart': fanart, 'banner': default_pm_icon})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.premium')

def pm_rename(file_type, file_id, current_name):
    new_name = dialog.input('Enter New Name for %s' % file_type.capitalize(), type=xbmcgui.INPUT_ALPHANUM, defaultt=current_name)
    if not new_name: return
    result = Premiumize.rename_cache_item(file_type, file_id, new_name)
    if result == 'success':
        Premiumize.clear_cache()
        xbmc.executebuiltin('XBMC.Container.Refresh()')
    else:
        return dialog.ok('Fen', 'Error Renaming Premiumize %s.' % file_type.capitalize())

def pm_account_info():
    from datetime import datetime
    import time
    import math
    try:
        account_info = Premiumize.account_info()
        customer_id = account_info['customer_id']
        expires = datetime.fromtimestamp(account_info['premium_until'])
        days_remaining = (expires - datetime.today()).days
        points_used = int(math.floor(float(account_info['space_used']) / 1073741824.0))
        space_used = float(int(account_info['space_used']))/1073741824
        percentage_used = str(round(float(account_info['limit_used']) * 100.0, 1))
        heading = 'PREMIUMIZE'
        body = []
        body.append('[B]Customer ID:[/B] %s' % customer_id)
        body.append('[B]Expires:[/B] %s' % expires)
        body.append('[B]Days Remaining:[/B] %s' % days_remaining)
        body.append('[B]Points Used:[/B] %.f' % points_used)
        body.append('[B]Space Used:[/B] %.2f' % space_used)
        body.append('[B]Fair Use (Percentage Used):[/B] %s' % (percentage_used + '%'))
        return dialog.select(heading, body)
    except Exception as e:
        return dialog.ok('Fen', 'Error Getting Premiumize Info..', e)
