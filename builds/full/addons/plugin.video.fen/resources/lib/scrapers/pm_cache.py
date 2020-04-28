
import xbmcaddon, xbmcgui
import json
from apis.premiumize_api import PremiumizeAPI
from modules.utils import get_release_quality, get_file_info, clean_title, normalize, supported_video_extensions
from scrapers import build_internal_scrapers_label, label_settings
from modules import settings
# from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
window = xbmcgui.Window(10000)

Premiumize = PremiumizeAPI()

class PremiumizeSource:
    def __init__(self):
        self.scrape_provider = 'pm-cloud'
        self.sources = []
        self.threads  = []
        self.scrape_results = []

    def results(self, info):
        try:
            if not Premiumize.pm_enabled(): return self.scrape_results
            self.info = info
            self.db_type = self.info.get("db_type")
            self.title = self.info.get("title")
            self.year = self.info.get("year")
            if self.year: self.rootname = '%s (%s)' % (self.title, self.year)
            else: self.rootname = self.title
            self.season = self.info.get("season")
            self.episode = self.info.get("episode")
            self.query = clean_title(self.title)
            self.file_query = self._episode_query_list() if self.db_type == 'episode' else self._year_query_list()
            self.extensions = supported_video_extensions()
            self._scrape_cloud()
            if not self.scrape_results: return self.sources
            self.label_settings = label_settings(self.info['scraper_settings'], self.scrape_provider)
            for item in self.scrape_results:
                try:
                    file_name = normalize(item['name'])
                    path = item['path']
                    file_dl = item['id']
                    size = float(item['size'])/1073741824
                    video_quality = get_release_quality(file_name, path)
                    details = get_file_info(file_name)
                    if not details: details = get_file_info(path)
                    label, multiline_label = build_internal_scrapers_label(self.label_settings, file_name, details, size, video_quality)
                    self.sources.append({'name': file_name,
                                        'label': label,
                                        'multiline_label': multiline_label,
                                        'title': file_name,
                                        'quality': video_quality,
                                        'size': size,
                                        'url_dl': file_dl,
                                        'id': file_dl,
                                        'downloads': False,
                                        'direct': True,
                                        'source': self.scrape_provider,
                                        'scrape_provider': self.scrape_provider})
                except: pass
            window.setProperty('pm-cloud_source_results', json.dumps(self.sources))
        except Exception as e:
            from modules.utils import logger
            logger('FEN premiumize scraper Exception', e)
        return self.sources

    def _scrape_cloud(self):
        try:
            cloud_files = Premiumize.user_cloud_all()['files']
            cloud_files = [i for i in cloud_files if i['path'].lower().endswith(tuple(self.extensions))]
            cloud_files = sorted(cloud_files, key=lambda k: k['name'])
        except: return self.sources
        for item in cloud_files:
            item_name = clean_title(normalize(item['name']))
            if self.query in item_name:
                if self.db_type == 'movie':
                    if any(x in item['name'] for x in self.file_query):
                        self.scrape_results.append(item)
                else:
                    if any(x in item_name for x in self.file_query):
                        self.scrape_results.append(item)


    def _year_query_list(self):
        return [str(self.year), str(int(self.year)+1), str(int(self.year)-1)]

    def _episode_query_list(self):
        return ['s%02de%02d' % (int(self.season), int(self.episode)),
                '%dx%02d' % (int(self.season), int(self.episode)),
                '%02dx%02d' % (int(self.season), int(self.episode)),
                'season%02depisode%02d' % (int(self.season), int(self.episode)),
                'season%depisode%02d' % (int(self.season), int(self.episode)),
                'season%depisode%d' % (int(self.season), int(self.episode))]

