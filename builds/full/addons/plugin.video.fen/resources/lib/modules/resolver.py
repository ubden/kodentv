# -*- coding: utf-8 -*-
# from modules.utils import logger

def resolve_cached_torrents(debrid_provider, item_url, _hash):
    from modules.settings import store_resolved_torrent_to_cloud
    url = None
    if debrid_provider == 'Real-Debrid':
        from apis.real_debrid_api import RealDebridAPI as debrid_function
    elif debrid_provider == 'Premiumize.me':
        from apis.premiumize_api import PremiumizeAPI as debrid_function
    elif debrid_provider == 'AllDebrid':
        from apis.alldebrid_api import AllDebridAPI as debrid_function
    store_to_cloud = store_resolved_torrent_to_cloud(debrid_provider)
    args = (item_url, _hash, store_to_cloud) if debrid_provider in ('Real-Debrid', 'AllDebrid') else (item_url, store_to_cloud)
    try: url = debrid_function().resolve_magnet(*args)
    except: pass
    return url

def resolve_unchecked_torrents(debrid_provider, item_url, _hash):
    if debrid_provider == 'Real-Debrid':
        from apis.real_debrid_api import RealDebridAPI as debrid_function
    elif debrid_provider == 'Premiumize.me':
        from apis.premiumize_api import PremiumizeAPI as debrid_function
    elif debrid_provider == 'AllDebrid':
        from apis.alldebrid_api import AllDebridAPI as debrid_function
    try: cached = debrid_function().check_single_magnet(_hash)
    except: cached = False
    if cached: return resolve_cached_torrents(debrid_provider, item_url, _hash)
    else: return None

def resolve_uncached_torrents(debrid_provider, item_url, _hash):
    if debrid_provider == 'Real-Debrid':
        from apis.real_debrid_api import RealDebridAPI as debrid_function
    elif debrid_provider == 'Premiumize.me':
        from apis.premiumize_api import PremiumizeAPI as debrid_function
    elif debrid_provider == 'AllDebrid':
        from apis.alldebrid_api import AllDebridAPI as debrid_function
    success = debrid_function().add_uncached_torrent(item_url)
    if success: return resolve_cached_torrents(debrid_provider, item_url, _hash)
    else: return None

def resolve_debrid(debrid_provider, item_url):
    url = None
    if debrid_provider == 'Real-Debrid':
        from apis.real_debrid_api import RealDebridAPI as debrid_function
    elif debrid_provider == 'Premiumize.me':
        from apis.premiumize_api import PremiumizeAPI as debrid_function
    elif debrid_provider == 'AllDebrid':
        from apis.alldebrid_api import AllDebridAPI as debrid_function
    try: url = debrid_function().unrestrict_link(item_url)
    except: pass
    return url

def resolve_internal_sources(scrape_provider, item_id, url_dl, direct_debrid_link=False):
    url = None
    try:
        if scrape_provider == 'furk':
            import xbmcgui
            import json
            from indexers.furk import t_file_browser, seas_ep_query_list
            meta = json.loads(xbmcgui.Window(10000).getProperty('fen_media_meta'))
            filtering_list = seas_ep_query_list(meta['season'], meta['episode']) if meta['vid_type'] == 'episode' else ''
            t_files = t_file_browser(item_id, filtering_list)
            url = t_files[0]['url_dl']
        elif scrape_provider == 'rd-cloud':
            if direct_debrid_link: return url_dl
            from apis.real_debrid_api import RealDebridAPI
            url = RealDebridAPI().unrestrict_link(item_id)
        elif scrape_provider == 'pm-cloud':
            from apis.premiumize_api import PremiumizeAPI
            details = PremiumizeAPI().get_item_details(item_id)
            url = details['link']
            if url.startswith('/'): url = 'https' + url
        elif scrape_provider == 'ad-cloud':
            from apis.alldebrid_api import AllDebridAPI
            url = AllDebridAPI().unrestrict_link(item_id)
        elif scrape_provider in ('local', 'downloads', 'easynews'):
            url = url_dl
        elif scrape_provider in ('folder1', 'folder2', 'folder3', 'folder4', 'folder5'):
            if url_dl.endswith('.strm'):
                import xbmcvfs
                f = xbmcvfs.File(url_dl)
                url = f.read()
                f.close()
            else:
                url = url_dl
    except: pass
    return url

def resolve_free_links(url, provider, direct):
    try:
        try: from urlparse import parse_qsl
        except ImportError: from urllib.parse import parse_qsl
        from openscrapers.modules import client
        from openscrapers import sources
        try: import resolveurl
        except Exception: return
        sourceDict = sources()
        u = url
        call = [i[1] for i in sourceDict if i[0] == provider][0]
        u = url = call.resolve(url)
        if url is None or ('://' not in str(url) and 'magnet:' not in str(url)):
            raise Exception()
        url = url[8:] if url.startswith('stack:') else url
        urls = []
        for part in url.split(' , '):
            u = part
            if direct is not True:
                hmf = resolveurl.HostedMediaFile(url=u, include_disabled=True, include_universal=False)
                if hmf.valid_url() is True:
                    part = hmf.resolve()
            urls.append(part)
        url = 'stack://' + ' , '.join(urls) if len(urls) > 1 else urls[0]
        if url is False or url is None:
            return None
        ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
        if ext == 'rar':
            return None
        try:
            headers = url.rsplit('|', 1)[1]
        except Exception:
            headers = ''
        headers = quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
        headers = dict(parse_qsl(headers))
        if url.startswith('http') and '.m3u8' in url:
            result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout='20')
            if result is None:
                return None
        elif url.startswith('http'):
            result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='20')
            if result is None:
                return None
        return url
    except:
        return None