import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import sys, os
try: from urllib import unquote
except ImportError: from urllib.parse import unquote
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
from apis.easynews_api import EasyNewsAPI
from modules.settings import get_theme
from modules.nav_utils import build_url, setView
from modules.utils import clean_file_name, to_utf8
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
dialog = xbmcgui.Dialog()
icon_directory = get_theme()
default_easynews_icon = os.path.join(icon_directory, 'easynews.png')
fanart = os.path.join(addon_dir, 'fanart.png')

EasyNews = EasyNewsAPI()

def search_easynews():
    from modules.history import add_to_search_history
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    default = params.get('suggestion', '')
    search_title = clean_file_name(params.get('query')) if ('query' in params and params.get('query') != 'NA') else None
    if not search_title: search_title = dialog.input('Enter search Term', type=xbmcgui.INPUT_ALPHANUM, defaultt=default)
    if not search_title: return
    try:
        search_name = clean_file_name(unquote(search_title))
        add_to_search_history(search_name, 'easynews_video_queries')
        files = EasyNews.search(search_name)
        if not files: return dialog.ok('No results', 'No results')
        files = files[0:int(__addon__.getSetting('easynews_limit'))]
        easynews_file_browser(files)
    except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.premium')

def easynews_file_browser(files):
    for count, item in enumerate(files, 1):
        try:
            cm = []
            name = clean_file_name(item['name']).upper()
            url_dl = item['url_dl']
            size = str(round(float(int(item['rawSize']))/1048576000, 1))
            display = '%02d | [B]%s GB[/B] | [I]%s [/I]' % (count, size, name)
            url_params = {'mode': 'media_play', 'url': item['url_dl'], 'rootname': 'video'}
            url = build_url(url_params)
            down_file_params = {'mode': 'download_file', 'name': item['name'], 'url': item['url_dl'], 'db_type': 'easynews_file', 'image': default_easynews_icon}
            cm.append(("[B]Download File[/B]",'XBMC.RunPlugin(%s)' % build_url(down_file_params)))
            listitem = xbmcgui.ListItem(display)
            listitem.addContextMenuItems(cm)
            listitem.setArt({'icon': default_easynews_icon, 'poster': default_easynews_icon, 'thumb': default_easynews_icon, 'fanart': fanart, 'banner': default_easynews_icon})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass

def account_info():
    from datetime import datetime
    import time
    try:
        account_html, usage_html = EasyNews.account()
        if not account_html or not usage_html:
            return dialog.ok('Fen', 'Error Getting Easynews Info.', 'Account or Usage html not available.')
        account_info = {
                    'account_username': to_utf8(account_html[0].find_all('td', recursive = False)[1].getText()),
                    'account_type': to_utf8(account_html[1].find_all('td', recursive = False)[2].getText()),
                    'account_status': to_utf8(account_html[3].find_all('td', recursive = False)[2].getText()),
                    'account_expiration': to_utf8(account_html[2].find_all('td', recursive = False)[2].getText()),
                    'usage_total': to_utf8(usage_html[0].find_all('td', recursive = False)[1].getText()),
                    'usage_web': to_utf8(usage_html[1].find_all('td', recursive = False)[2].getText()),
                    'usage_NNTP': to_utf8(usage_html[2].find_all('td', recursive = False)[2].getText()),
                    'usage_remaining': to_utf8(usage_html[4].find_all('td', recursive = False)[2].getText()),
                    'usage_loyalty': to_utf8(usage_html[5].find_all('td', recursive = False)[2].getText())
                        }
        resformat = "%Y-%m-%d"
        try: expires = datetime.strptime(account_info['account_expiration'], resformat)
        except TypeError: expires = datetime(*(time.strptime(account_info['account_expiration'], resformat)[0:6]))
        days_remaining = (expires - datetime.today()).days
        heading = 'EASYNEWS'
        body = []
        body.append('[B]Account:[/B] %s' % account_info['account_type'])
        body.append('[B]Username:[/B] %s' % account_info['account_username'])
        body.append('[B]Status:[/B] %s' % account_info['account_status'])
        body.append('[B]Expires:[/B] %s' % expires)
        body.append('[B]Days Remaining:[/B] %s' % days_remaining)
        body.append('[B]Data Used:[/B] %s' % account_info['usage_total'].replace('Gigs', 'GB'))
        body.append('[B]Data Remaining:[/B] %s' % account_info['usage_remaining'].replace('Gigs', 'GB'))
        return dialog.select(heading, body)
    except Exception as e:
        return dialog.ok('Fen', 'Error Getting Easynews Info..', e)