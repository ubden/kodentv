# -*- coding: utf-8 -*-
import xbmcaddon, xbmcvfs, xbmcgui
import re
import json
import os
from threading import Thread
try: from urlparse import urlparse
except ImportError: from urllib.parse import urlparse
from modules.utils import get_release_quality, get_file_info, supported_video_extensions, clean_title, normalize
from scrapers import build_internal_scrapers_label, label_settings
from modules import settings
# from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
window = xbmcgui.Window(10000)

class DownloadsSource:
    def __init__(self):
        self.scrape_provider = 'downloads'
        self.threads  = []
        self.sources = []
        self.scrape_results = []
        self.extensions = supported_video_extensions()
        self.extensions.remove('.strm')

    def results(self, info):
        try:
            self.info = info
            self.db_type = self.info.get("db_type")
            self.folder_path = settings.download_directory(self.db_type)
            self.title = self.info.get("title")
            self.year = self.info.get("year")
            self.season = self.info.get("season")
            self.episode = self.info.get("episode")
            self.title_query = clean_title(self.title)
            self.folder_query = self._season_query_list() if self.db_type == 'episode' else self._year_query_list()
            self.file_query = self._episode_query_list() if self.db_type == 'episode' else self._year_query_list()
            self._scrape_directory(self.folder_path)
            if not self.scrape_results: return self.sources
            self.label_settings = label_settings(self.info['scraper_settings'], self.scrape_provider)
            for item in self.scrape_results:
                try:
                    file_name = item[0]
                    file_dl = item[1]
                    size = self._get_size(file_dl)
                    details = get_file_info(file_name)
                    video_quality = get_release_quality(file_name, file_dl)
                    label, multiline_label = build_internal_scrapers_label(self.label_settings, file_name, details, size, video_quality)
                    self.sources.append({'name': file_name,
                                        'label': label,
                                        'multiline_label': multiline_label,
                                        'title': file_name,
                                        'quality': video_quality,
                                        'size': size,
                                        'url_dl': file_dl,
                                        'id': file_dl,
                                        'downloads': True,
                                        'direct': True,
                                        'source': self.scrape_provider,
                                        'scrape_provider': self.scrape_provider})
                except: pass
            window.setProperty('downloads_source_results', json.dumps(self.sources))
        except Exception as e:
            from modules.utils import logger
            logger('FEN downloads scraper Exception', e)
        return self.sources

    def _scrape_directory(self, folder_name):
        folder_files = []
        folder_results = []
        dirs, files = xbmcvfs.listdir(folder_name)
        for i in dirs: folder_files.append((i, 'folder'))
        for i in files: folder_files.append((i, 'file'))
        for item in folder_files:
            file_type = item[1]
            item_name = clean_title(normalize(item[0]))
            if file_type == 'file':
                ext = os.path.splitext(urlparse(item[0]).path)[-1]
                if ext in self.extensions:
                    if self.db_type == 'movie':
                        if self.title_query in item_name:
                            url_path = self.url_path(folder_name, item[0])
                            self.scrape_results.append((item[0], url_path))
                    elif any(x in item_name for x in self.file_query):
                        if not folder_name in self.folder_path:
                            url_path = self.url_path(folder_name, item[0])
                            self.scrape_results.append((item[0], url_path))
                        elif self.title_query in item_name:
                            url_path = self.url_path(folder_name, item[0])
                            self.scrape_results.append((item[0], url_path))  
            elif file_type == 'folder':
                if self.title_query in item_name or any(x in item_name for x in self.folder_query):
                    new_folder = os.path.join(folder_name, item[0])
                    folder_results.append(new_folder)
        if not folder_results: return
        return self._scraper_worker(folder_results)

    def _scraper_worker(self, folder_results):
        threads = []
        for i in folder_results: threads.append(Thread(target=self._scrape_directory, args=(i,)))
        [i.start() for i in threads]
        [i.join() for i in threads]

    def url_path(self, folder, file):
        url_path = os.path.join(folder, file)
        return url_path

    def _get_size(self, file):
        f = xbmcvfs.File(file)
        s = f.size()
        f.close()
        size = float(s)/1073741824
        return size

    def _year_query_list(self):
        return (str(self.year), str(int(self.year)+1), str(int(self.year)-1))

    def _season_query_list(self):
        return ['season%02d' % int(self.season), 'season%s' % self.season]

    def _episode_query_list(self):
        return ['s%02de%02d' % (int(self.season), int(self.episode)),
                '%dx%02d' % (int(self.season), int(self.episode)),
                '%02dx%02d' % (int(self.season), int(self.episode)),
                'season%02depisode%02d' % (int(self.season), int(self.episode)),
                'season%depisode%02d' % (int(self.season), int(self.episode)),
                'season%depisode%d' % (int(self.season), int(self.episode))]
