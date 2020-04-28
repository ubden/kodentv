# -*- coding: utf-8 -*-

import xbmcgui, xbmcaddon
import requests
from tikimeta.metacache import cache_function
# from tikimeta.utils import logger

# Original Code belonged to nixgates. Thankyou.

base_url = "http://webservice.fanart.tv/v3/%s/%s"
api_key = "a7ad21743fd710fccb738232f2fbdcfc"
window = xbmcgui.Window(10000)

def get_query(art, language):
    if art is None: return ''
    try:
        result = [(x['url'], x['likes']) for x in art if x.get('lang') == language]
        if not result: result = [(x['url'], x['likes']) for x in art]
        result = [(x[0], x[1]) for x in result]
        result = sorted(result, key=lambda x: int(x[1]), reverse=True)
        result = [x[0] for x in result][0]
    except:
        result = ''
    if not 'http' in result: result = ''
    return result

def get(query, language, remote_id, client_key):
    def _get_fanart(info):
        def error_notification(line):
            if window.getProperty('fen_fanart_error') == 'true': return
            from tikimeta.utils import notification
            window.setProperty('fen_fanart_error', 'true')
            notification(line, 3000)
            notification('Consider disabling fanart until issue resolves.', 6000)
        language = info[1]
        art = base_url % (info[0], info[2])
        headers = {'client-key': info[3], 'api-key': api_key}
        try:
            art = requests.get(art, headers=headers, timeout=15.0)
        except requests.exceptions.Timeout as e:
            error_notification('Fanart.tv response timeout error')
            return None
        status = art.status_code
        if not status in (200, 404):
            error_notification('Fanart.tv response error: [B]%s[/B]' % str(status))
            return None
        art = art.json()
        if info[0] == 'movies':
            fanart_data = {'fanarttv_poster': get_query(art.get('movieposter'), language),
                            'fanarttv_fanart': get_query(art.get('moviebackground'), language),
                            'banner': get_query(art.get('moviebanner'), language),
                            'clearart': get_query(art.get('movieart', []) + art.get('hdmovieclearart', []), language),
                            'clearlogo': get_query(art.get('movielogo', []) + art.get('hdmovielogo', []), language),
                            'landscape': get_query(art.get('moviethumb'), language),
                            'discart': get_query(art.get('moviedisc'), language),
                            'fanart_added': True}
        else:
            fanart_data = {'fanarttv_poster': get_query(art.get('tvposter'), language),
                            'fanarttv_fanart': get_query(art.get('showbackground'), language),
                            'banner': get_query(art.get('tvbanner'), language),
                            'clearart': get_query(art.get('clearart', []) + art.get('hdclearart', []), language),
                            'clearlogo': get_query(art.get('hdtvlogo', []) + art.get('clearlogo', []), language),
                            'landscape': get_query(art.get('tvthumb'), language),
                            'discart': '',
                            'fanart_added': True}
        return fanart_data
    string = "%s_%s_%s_%s" % ('fanart', query, language, remote_id)
    return cache_function(_get_fanart, string, (query, language, remote_id, client_key), 720, json=False)

def add(query, language, remote_id, meta, client_key):
    try:
        fanart_data = get(query, language, remote_id, client_key)
        meta['fanarttv_poster'] = fanart_data['fanarttv_poster']
        meta['fanarttv_fanart'] = fanart_data['fanarttv_fanart']
        meta['banner'] = fanart_data['banner']
        meta['clearart'] = fanart_data['clearart']
        meta['clearlogo'] = fanart_data['clearlogo']
        meta['landscape'] = fanart_data['landscape']
        meta['discart'] = fanart_data['discart']
        meta['fanart_added'] = fanart_data['fanart_added']
    except: pass
    return meta

