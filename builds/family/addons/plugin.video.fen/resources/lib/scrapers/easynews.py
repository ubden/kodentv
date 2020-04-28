import xbmcaddon, xbmcgui
import re
import json
from apis.easynews_api import EasyNewsAPI
from modules.utils import get_release_quality, get_file_info, clean_file_name, normalize
from scrapers import build_internal_scrapers_label, label_settings
from modules import settings
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
window = xbmcgui.Window(10000)
EasyNews = EasyNewsAPI()

class EasyNewsSource:
    def __init__(self):
        self.scrape_provider = 'easynews'
        self.sources = []
        self.max_results = int(__addon__.getSetting('easynews_limit'))
        self.max_gb = __addon__.getSetting('easynews_maxgb')
        self.max_bytes = int(self.max_gb) * 1024 * 1024 * 1024

    def results(self, info):
        try:
            self.info = info
            search_name = self._search_name()
            files = EasyNews.search(search_name)
            files = files[0:self.max_results]
            self.label_settings = label_settings(self.info['scraper_settings'], self.scrape_provider)
            for item in files:
                try:
                    if self.max_bytes:
                        match = re.search('([\d.]+)\s+(.*)', item['size'])
                        if match:
                            size_bytes = self.to_bytes(*match.groups())
                            if size_bytes > self.max_bytes:
                                continue
                    file_name = normalize(item['name'])
                    file_dl = item['url_dl']
                    size = float(int(item['rawSize']))/1073741824
                    details = get_file_info(file_name)
                    video_quality = get_release_quality(file_name, file_dl)
                    label, multiline_label = build_internal_scrapers_label(self.label_settings, file_name, details, size, video_quality)
                    self.sources.append({'name': file_name,
                                    'label': label,
                                    'multiline_label': multiline_label,
                                    'quality': video_quality,
                                    'size': size,
                                    'url_dl': file_dl,
                                    'id': file_dl,
                                    'local': False,
                                    'direct': True,
                                    'source': self.scrape_provider,
                                    'scrape_provider': self.scrape_provider})
                except: pass
            window.setProperty('easynews_source_results', json.dumps(self.sources))
        except Exception as e:
            from modules.utils import logger
            logger('FEN easynews scraper Exception', e)
        return self.sources

    def _search_name(self):
        search_title = clean_file_name(self.info.get("title"))
        db_type = self.info.get("db_type")
        year = self.info.get("year")
        years = '%s,%s,%s' % (str(int(year - 1)), year, str(int(year + 1)))
        season = self.info.get("season")
        episode = self.info.get("episode")
        if db_type == 'movie': search_name = '"%s" %s' % (search_title, years)
        else: search_name = '%s S%02dE%02d' % (search_title,  int(season), int(episode))
        return search_name

    def to_bytes(self, num, unit):
        unit = unit.upper()
        if unit.endswith('B'): unit = unit[:-1]
        units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
        try: mult = pow(1024, units.index(unit))
        except: mult = sys.maxint
        return int(float(num) * mult)

