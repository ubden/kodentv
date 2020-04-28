import xbmcaddon, xbmcgui
import re
import json
from datetime import timedelta
from apis.furk_api import FurkAPI
from modules import fen_cache
from modules.utils import get_release_quality, get_file_info, clean_file_name, to_utf8, normalize
from scrapers import build_internal_scrapers_label, label_settings
from modules import settings
# from modules.utils import logger

Furk = FurkAPI()
__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
window = xbmcgui.Window(10000)

class FurkSource:
    def __init__(self):
        self.scrape_provider = 'furk'
        self.sources = []
        self.furk_limit = int(__addon__.getSetting('furk.limit'))
        self.max_gb = int(__addon__.getSetting('furk_maxgb'))

    def results(self, info):
        try:
            self.info = info
            search_name = self._search_name()
            files = Furk.search(search_name)
            if not files: return self.sources
            active_downloads = self.get_active_downloads()
            cached_files = [i for i in files if i.get('type') not in ('default', 'audio', '') and i.get('is_ready') == '1'][0:self.furk_limit]
            uncached_files = [i for i in files if i.get('type') not in ('default', 'audio', '') and i not in cached_files]
            self.label_settings = label_settings(self.info['scraper_settings'], self.scrape_provider)
            for i in cached_files:
                try:
                    file_name = normalize(i['name'])
                    file_id = i['id']
                    files_num_video = i['files_num_video']
                    size = float(int(i['size']))/1073741824
                    if not int(files_num_video) > 3:
                        if size > self.max_gb:
                            continue
                    file_dl = i['url_dl']
                    details = get_file_info(file_name)
                    video_quality = get_release_quality(file_name, file_dl)
                    furk_settings = {'files_num_video': files_num_video, 'uncached': False, 'active_download': False}
                    label, multiline_label = build_internal_scrapers_label(self.label_settings, file_name, details, size, video_quality, **furk_settings)
                    self.sources.append({'name': file_name,
                                    'label': label,
                                    'multiline_label': multiline_label,
                                    'title': file_name,
                                    'quality': video_quality,
                                    'size': size,
                                    'url_dl': file_dl,
                                    'id': file_id,
                                    'local': False,
                                    'direct': True,
                                    'source': self.scrape_provider,
                                    'scrape_provider': self.scrape_provider})
                except Exception as e:
                    from modules.utils import logger
                    logger('FURK ERROR - 65', e)
                    pass
            for i in uncached_files:
                try:
                    file_name = i['name']
                    info_hash = i['info_hash']
                    try: files_num_video = i['files_num_video']
                    except: files_num_video = 1
                    try: size = float(int(i['size']))/1073741824
                    except: size = 0
                    active_download = True if info_hash in active_downloads else False
                    details = get_file_info(file_name)
                    video_quality = get_release_quality(file_name)
                    furk_settings = {'files_num_video': files_num_video, 'uncached': True, 'active_download': active_download}
                    label, multiline_label = build_internal_scrapers_label(self.label_settings, file_name, details, size, video_quality, **furk_settings)
                    self.sources.append({'name': file_name,
                                    'label': label,
                                    'multiline_label': multiline_label,
                                    'title': file_name,
                                    'quality': video_quality,
                                    'size': size,
                                    'url_dl': info_hash,
                                    'id': info_hash,
                                    'local': False,
                                    'direct': True,
                                    'uncached': True,
                                    'source': self.scrape_provider,
                                    'scrape_provider': self.scrape_provider})
                except Exception as e:
                    from modules.utils import logger
                    logger('FURK ERROR - 96', e)
                    pass
            window.setProperty('furk_source_results', json.dumps([i for i in self.sources if not 'uncached' in i]))
        except Exception as e:
            from modules.utils import logger
            logger('FEN furk scraper Exception', e)
            pass

        return self.sources

    def get_active_downloads(self):
        _cache = fen_cache.FenCache()
        cache = _cache.get('furk_active_downloads')
        if cache != None: result = cache
        else:
            active_downloads = Furk.file_get_active()
            result = [i['info_hash'] for i in active_downloads]
            _cache.set('furk_active_downloads', result, expiration=timedelta(hours=1))
        return result

    def _search_name(self):
        search_title = clean_file_name(to_utf8(self.info.get("title")))
        search_title = search_title.replace(' ', '+')
        db_type = self.info.get("db_type")
        if db_type == 'movie':
            year = self.info.get("year")
            years = '%s+|+%s+|+%s' % (str(int(year - 1)), year, str(int(year + 1)))
            search_name = '@name+%s+%s' % (search_title, years)
        else:
            season = self.info.get("season")
            episode = self.info.get("episode")
            queries = self._seas_ep_query_list(season, episode)
            search_name = '@name+%s+@files+%s+|+%s+|+%s+|+%s+|+%s' % (search_title, queries[0], queries[1], queries[2], queries[3], queries[4])
        return search_name

    def _seas_ep_query_list(self, season, episode):
        return ['s%02de%02d' % (int(season), int(episode)),
                '%dx%02d' % (int(season), int(episode)),
                '%02dx%02d' % (int(season), int(episode)),
                '"season %d episode %d"' % (int(season), int(episode)),
                '"season %02d episode %02d"' % (int(season), int(episode))]
