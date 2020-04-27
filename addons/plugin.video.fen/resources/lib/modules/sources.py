# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
try: from urllib import unquote, quote_plus
except ImportError: from urllib.parse import unquote, quote_plus
import sys, os
import json
import time
from datetime import datetime, timedelta
from threading import Thread
from modules.external_source_utils import toggle_all, external_scrapers_reset_stats
from modules.utils import clean_file_name, selection_dialog
from indexers.furk import t_file_browser, seas_ep_query_list, add_uncached_file
from modules.nav_utils import build_url, setView, notification, close_all_dialog, show_busy_dialog, hide_busy_dialog
from modules.utils import string_to_float, to_utf8, safe_string, remove_accents
from modules import settings
from modules.utils import logger

try: __resolveURL__ = xbmcaddon.Addon(id='script.module.resolveurl')
except: pass
__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
__handle__ = int(sys.argv[1])
window = xbmcgui.Window(10000)
dialog = xbmcgui.Dialog()
default_furk_icon = os.path.join(settings.get_theme(), 'furk.png')

class Sources:
    def __init__(self):
        self.play_physical = False
        self.suppress_notifications = False
        self.providers = []
        self.sources = []
        self.prescrape_sources = []
        self.starting_providers = []
        self.prescrape_starting_providers = []
        self.uncached_results = []
        self.threads = []
        self.prescrape_threads = []
        self.display_mode = settings.display_mode()
        self.folder_scrapers = ('folder1', 'folder2', 'folder3', 'folder4', 'folder5')
        self.file_scrapers = ('local', 'downloads', 'folder1', 'folder2', 'folder3', 'folder4', 'folder5')
        self.internal_scrapers = ('furk', 'rd-cloud', 'ad-cloud', 'local', 'downloads', 'easynews', 'pm-cloud', 'folder1', 'folder2', 'folder3', 'folder4', 'folder5')

    def playback_prep(self, vid_type, tmdb_id, query, tvshowtitle=None, season=None, episode=None, ep_name=None, plot=None, meta=None, from_library=False, background='false', autoplay=None):
        self._clear_sources()
        self.background = True if background == 'true' else False
        self.dialog_background = True if (__addon__.getSetting('auto_play'), __addon__.getSetting('autoplay_minimal_notifications')) == ('true', 'true') else False
        self.suppress_notifications = True if self.background == True or self.dialog_background == True else False
        self.from_library = from_library
        self.widget = False if 'plugin' in xbmc.getInfoLabel('Container.PluginName') else True
        self.action = 'Container.Update(%s)' if not self.widget else 'RunPlugin(%s)'
        self.autoplay = autoplay if autoplay != None else settings.auto_play()
        self.autoplay_hevc = settings.autoplay_hevc()
        self.check_library = settings.check_prescrape_sources('local')
        self.check_downloads = settings.check_prescrape_sources('downloads')
        self.check_folders = settings.check_prescrape_sources('folders')
        self.include_prerelease_results = settings.include_prerelease_results()
        self.include_uncached_results = settings.include_uncached_results()
        self.internal_scraper_order = settings.internal_scraper_order()
        self.language = xbmcaddon.Addon(id='script.module.tikimeta').getSetting('meta_language')
        self.vid_type = vid_type
        self.tmdb_id = tmdb_id
        self.season = int(season) if season else ''
        self.episode = int(episode) if episode else ''
        if meta: self.meta = json.loads(meta)
        else: self._grab_meta()
        display_name = clean_file_name(unquote(query)) if vid_type == 'movie' else '%s - %dx%.2d' % (self.meta['title'], self.season, self.episode)
        if from_library: self.meta.update({'plot': plot, 'from_library': from_library, 'ep_name': ep_name})
        self.meta.update({'query': query, 'vid_type': self.vid_type, 'media_id': self.tmdb_id, 'rootname': display_name,
                          'tvshowtitle': self.meta['title'], 'season': self.season, 'episode': self.episode, 'background': self.background})
        self.search_info = self._search_info()
        window.setProperty('fen_media_meta', json.dumps(self.meta))
        self.get_sources()

    def get_sources(self):
        self.active_scrapers = settings.active_scrapers()
        if 'external' in self.active_scrapers:
            self._activate_resolveURL()
            self._check_reset_external_scrapers()
        self.play_physical = self.pre_scrape_check()
        if self.play_physical: results = self.sources
        if not self.play_physical:
            results = self.collect_results()
            results = self.filter_results(results)
            results = self.sort_results(results)
        if 'external' in self.active_scrapers:
            self._activate_resolveURL(setting='false')
        if not results:
            return self._no_results()
        if self.autoplay:
            results = self._sort_hevc(results)
        elif self.include_uncached_results:
            results += self.uncached_results
        results = self.enumerate_labels(results)
        window.setProperty('fen_search_results', json.dumps(results))
        hide_busy_dialog()
        self.play_source()

    def collect_results(self):
        if 'folder' in '.'.join(self.active_scrapers):
            self.check_folder_scrapers(self.active_scrapers, self.providers, False)
        if 'local' in self.active_scrapers:
            from scrapers.local_library import LocalLibrarySource
            self.providers.append(('local', LocalLibrarySource()))
        if 'downloads' in self.active_scrapers:
            from scrapers.downloads import DownloadsSource
            self.providers.append(('downloads', DownloadsSource()))
        if 'furk' in self.active_scrapers:
            from scrapers.furk import FurkSource
            self.providers.append(('furk', FurkSource()))
        if 'easynews' in self.active_scrapers:
            from scrapers.easynews import EasyNewsSource
            self.providers.append(('easynews', EasyNewsSource()))
        if 'pm-cloud' in self.active_scrapers:
            from scrapers.pm_cache import PremiumizeSource
            self.providers.append(('pm-cloud', PremiumizeSource()))
        if 'rd-cloud' in self.active_scrapers:
            from scrapers.rd_cache import RealDebridSource
            self.providers.append(('rd-cloud', RealDebridSource()))
        if 'ad-cloud' in self.active_scrapers:
            from scrapers.ad_cache import AllDebridSource
            self.providers.append(('ad-cloud', AllDebridSource()))
        if 'external' in self.active_scrapers:
            from scrapers.external import ExternalSource
            self.providers.append(('external', ExternalSource()))
        for i in range(len(self.providers)):
            self.threads.append(Thread(target=self.activate_providers, args=(self.providers[i][1],)))
            self.starting_providers.append((self.threads[i].getName(), self.providers[i][0]))
        [i.start() for i in self.threads]
        if 'external' in self.active_scrapers or self.background:
            [i.join() for i in self.threads]
        else:
            self.scrapers_dialog('internal')
        return self.sources

    def filter_results(self, results):
        cached_results = [i for i in results if not 'uncached' in i]
        self.uncached_results = [i for i in results if 'uncached' in i]
        quality_filter = self._quality_filter()
        include_local_in_filter = settings.include_sources_in_filter('include_local')
        include_downloads_in_filter = settings.include_sources_in_filter('include_downloads')
        include_folders_in_filter = settings.include_sources_in_filter('include_folders')
        filter_torrent_size = __addon__.getSetting('torrent.filter.size')
        include_3D_results = __addon__.getSetting('include_3d_results')
        if filter_torrent_size:
            torrent_min_size = string_to_float(__addon__.getSetting('torrent.size.minimum.movies' if self.vid_type == 'movie' else 'torrent.size.minimum.episodes'), 0)
            torrent_max_size = string_to_float(__addon__.getSetting('torrent.size.maximum.movies' if self.vid_type == 'movie' else 'torrent.size.maximum.episodes'), 200)
        results = []
        for item in cached_results:
            append_item = False
            if any(x in item for x in self.folder_scrapers) and not include_folders_in_filter: append_item = True
            elif item.get("local") and not include_local_in_filter: append_item = True
            elif item.get("downloads") and not include_downloads_in_filter: append_item = True
            elif item.get("quality") in quality_filter: append_item = True
            if item['source'].lower() == 'torrent' and filter_torrent_size == 'true':
                if not torrent_min_size < item['external_size'] < torrent_max_size: append_item = False
            if not include_3D_results:
                info = item['info'] if 'info' in item else item['label']
                if '3D' in info: append_item = False
            if append_item: results.append(item)
        return results

    def sort_results(self, results):
        def _add_keys(item):
            provider = item['scrape_provider']
            if provider in ('local', 'downloads') or 'folder' in provider: provider = 'files'
            item['quality_rank'] = self._get_quality_rank(item.get("quality", "SD"))
            if provider == 'external':
                item['debrid_rank'] = self._get_debrid_rank(item.get('debrid', 'internal'))
                item['name_rank'] = item['provider']
                if sort_torrent_top == 'true': item['torrent_rank'] = self._get_torrent_rank(item)
            else:
                item['debrid_rank'] = 1
                item['torrent_rank'] = 1
                item['name_rank'] = self._get_name_rank(provider.upper())
                item['external_size'] = 600.0 * 1024
        sort_keys = list(settings.results_sort_order())
        sort_torrent_top = __addon__.getSetting('torrent.sort.them.up')
        sort_torrent_size = __addon__.getSetting('torrent.sort.size')
        if 'external' in self.active_scrapers:
            insert = 0 if sort_keys[0] == 'name_rank' else 1
            sort_keys.insert(insert, 'debrid_rank')
            if sort_torrent_top == 'true':
                sort_keys.insert(insert, 'torrent_rank')
            if sort_torrent_size == 'true':
                insert2 = 3 if sort_keys[1] == 'torrent_rank' else -1
                sort_keys.insert(insert2, 'external_size')
        threads = []
        for item in results: threads.append(Thread(target=_add_keys, args=(item,)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        for item in reversed(sort_keys):
            if item in ('size', 'external_size'): reverse = True
            else: reverse = False
            results = sorted(results, key=lambda k: k[item], reverse=reverse)
        providers = []
        if settings.sorted_first('sort_rd-cloud_first'): providers.append('rd-cloud')
        if settings.sorted_first('sort_pm-cloud_first'): providers.append('pm-cloud')
        if settings.sorted_first('sort_ad-cloud_first'): providers.append('ad-cloud')
        if settings.sorted_first('sort_folders_first'): providers.extend(self.folder_scrapers)
        if settings.sorted_first('sort_downloads_first'): providers.append('downloads')
        if settings.sorted_first('sort_local_first'): providers.append('local')
        for provider in providers: self._sort_first(provider, results)
        return results

    def activate_providers(self, function):
        sources = function.results(self.search_info)
        self.sources.extend(sources)

    def activate_prescrape_providers(self, function):
        sources = function.results(self.search_info)
        self.prescrape_sources.extend(sources)

    def enumerate_labels(self, results):
        for n, i in enumerate(results, 1):
            i['label'] = '%s | %s' % (str(n).zfill(2), i['label'])
            i['multiline_label'] = '%s | %s' % (str(n).zfill(2), i['multiline_label'])
        return results

    def play_source(self):
        if self.background:
            return xbmc.executebuiltin(self.action % build_url({'mode': 'play_auto_nextep'}))
        if self.play_physical or self.autoplay:
            return self.play_auto()
        if self.display_mode == 2 or self.from_library or self.widget:
            return self.dialog_results()
        return xbmc.executebuiltin(self.action % build_url({'mode': 'play_display_results'}))

    def pre_scrape_check(self):
        prescrape_scrapers = []
        if not any(x in self.active_scrapers for x in self.file_scrapers): return False
        if self.autoplay:
            if 'local' in self.active_scrapers:
                from scrapers.local_library import LocalLibrarySource
                prescrape_scrapers.append(('local', LocalLibrarySource()))
            if 'downloads' in self.active_scrapers:
                from scrapers.downloads import DownloadsSource
                prescrape_scrapers.append(('downloads', DownloadsSource()))
            if 'folder' in '.'.join(self.active_scrapers):
                self.check_folder_scrapers(self.active_scrapers, prescrape_scrapers, False)
        else:
            if 'local' in self.active_scrapers and self.check_library:
                from scrapers.local_library import LocalLibrarySource
                prescrape_scrapers.append(('local', LocalLibrarySource()))
            if 'downloads' in self.active_scrapers and self.check_downloads:
                from scrapers.downloads import DownloadsSource
                prescrape_scrapers.append(('downloads', DownloadsSource()))
            if 'folder' in '.'.join(self.active_scrapers):
                self.check_folder_scrapers(self.active_scrapers, prescrape_scrapers)
        self.total_active_scrapers = len(prescrape_scrapers)
        if self.total_active_scrapers == 0: return False
        for i in range(len(prescrape_scrapers)):
            self.prescrape_threads.append(Thread(target=self.activate_prescrape_providers, args=(prescrape_scrapers[i][1],)))
            self.prescrape_starting_providers.append((self.prescrape_threads[i].getName(), prescrape_scrapers[i][0]))
        [i.start() for i in self.prescrape_threads]
        if self.background:
            [i.join() for i in self.prescrape_threads]
        else:
            self.scrapers_dialog('pre_scrape')
        if not self.prescrape_sources: return False
        prescrape_results = self.filter_results(self.prescrape_sources)
        if not prescrape_results: return False
        if self.autoplay:
            self.sources.extend(prescrape_results)
            return True
        result = selection_dialog([i.get('multiline_label') for i in prescrape_results], prescrape_results, 'Pre-Scrape Results:')
        if not result: return False
        self.sources.append(result)
        return True

    def check_folder_scrapers(self, active_scrapers, append_list, prescrape=True):
        from scrapers.folder_scraper import FolderScraper
        for i in active_scrapers:
            if i.startswith('folder'):
                scraper_name = __addon__.getSetting('%s.display_name' % i)
                if prescrape:
                    if self.check_folders: append_list.append((scraper_name, FolderScraper(i, scraper_name)))
                else: append_list.append((scraper_name, FolderScraper(i, scraper_name)))

    def scrapers_dialog(self, scrape_type):
        def _scraperDialog():
            for i in range(0, 100):
                try:
                    if xbmc.abortRequested == True: return sys.exit()
                    try:
                        if progress_dialog.iscanceled():
                            break
                    except Exception:
                        pass
                    alive_threads = [x.getName() for x in _threads if x.is_alive() is True]
                    remaining_providers = [x[1] for x in _starting_providers if x[0] in alive_threads]
                    source_4k_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality'] == '4K' and  not 'uncached' in e]))
                    source_1080_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality']  == '1080p' and  not 'uncached' in e]))
                    source_720_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality'] == '720p' and  not 'uncached' in e]))
                    source_sd_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality'] in ['SD', 'SCR', 'CAM', 'TELE'] and not 'uncached' in e]))
                    source_total_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality'] in ['4K', '1080p', '720p', 'SD', 'SCR', 'CAM', 'TELE'] and not 'uncached' in e]))
                    try:
                        line1 = '[COLOR %s]%s[/COLOR]' % (int_dialog_highlight, _line1_insert)
                        line2 = ('[COLOR %s][B]%s[/B][/COLOR] 4K: %s | 1080p: %s | 720p: %s | SD: %s | Total: %s') % (int_dialog_highlight, _line2_insert, source_4k_label, source_1080_label, source_720_label, source_sd_label, source_total_label)
                        if len(remaining_providers) > 3: line3_insert = str(len(remaining_providers))
                        else: line3_insert = ', '.join(remaining_providers).upper()
                        line3 = 'Remaining providers: %s' % line3_insert
                        current_time = time.time()
                        current_progress = current_time - start_time
                        percent = int((current_progress/float(timeout))*100)
                        progress_dialog.update(max(1, percent), line1, line2, line3)
                    except: pass
                    time.sleep(0.2)
                    if len(alive_threads) == 0: break
                    if end_time < current_time: break
                except Exception:
                    pass
        def _scraperDialogBG():
            for i in range(0, 100):
                try:
                    if xbmc.abortRequested == True: return sys.exit()
                    try:
                        if progress_dialog.iscanceled():
                            break
                    except Exception:
                        pass
                    alive_threads = [x.getName() for x in _threads if x.is_alive() is True]
                    remaining_providers = [x[1] for x in _starting_providers if x[0] in alive_threads]
                    source_4k_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality'] == '4K' and  not 'uncached' in e]))
                    source_1080_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality']  == '1080p' and  not 'uncached' in e]))
                    source_720_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality'] == '720p' and  not 'uncached' in e]))
                    source_sd_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality'] in ['SD', 'SCR', 'CAM', 'TELE'] and not 'uncached' in e]))
                    source_total_label = total_format % (int_dialog_highlight, len([e for e in _sources if e['quality'] in ['4K', '1080p', '720p', 'SD', 'SCR', 'CAM', 'TELE'] and not 'uncached' in e]))
                    try:
                        line1 = '4K:%s|1080p:%s|720p:%s|SD:%s|T:%s' % (source_4k_label, source_1080_label, source_720_label, source_sd_label, source_total_label)
                        line2 = 'Remaining providers: %s' % str(len(remaining_providers))
                        current_time = time.time()
                        current_progress = current_time - start_time
                        percent = int((current_progress/float(timeout))*100)
                        progress_dialog.update(max(1, percent), line1, line2)
                    except: pass
                    time.sleep(0.2)
                    if len(alive_threads) == 0: break
                    if end_time < current_time: break
                except Exception:
                    pass
        hide_busy_dialog()
        timeout = 25
        int_dialog_highlight = __addon__.getSetting('int_dialog_highlight')
        if not int_dialog_highlight or int_dialog_highlight == '': int_dialog_highlight = 'dodgerblue'
        total_format = '[COLOR %s][B]%s[/B][/COLOR]'
        _progress_heading = int(__addon__.getSetting('progress.heading'))
        _progress_title = self.meta.get('rootname') if _progress_heading == 1 else 'Internal Scrapers' if scrape_type == 'internal' else 'Pre-Scrape'
        _threads = self.threads if scrape_type == 'internal' else self.prescrape_threads
        _starting_providers = self.starting_providers if scrape_type == 'internal' else self.prescrape_starting_providers
        _sources = self.sources if scrape_type == 'internal' else self.prescrape_sources
        _line1_insert = 'Internal Scrapers' if scrape_type == 'internal' else 'Pre-Scrape Sources'
        _line2_insert = 'Int:' if scrape_type == 'internal' else 'Pre:'
        if self.suppress_notifications:
            progress_dialog = xbmcgui.DialogProgressBG()
            function = _scraperDialogBG
        else:
            progress_dialog = xbmcgui.DialogProgress()
            function = _scraperDialog
        start_time = time.time()
        end_time = start_time + timeout
        progress_dialog.create(_progress_title, '')
        progress_dialog.update(0)
        function()
        try: progress_dialog.close()
        except Exception: pass
        xbmc.sleep(500)

    def display_results(self, page_no=None, previous_nav=None):
        def _build_simple_directory(item, position=None):
            try:
                cm = []
                title = item.get('title')
                item_id = item.get('id', None)
                uncached = item.get('uncached', False)
                mode = 'furk.add_uncached_file' if uncached else 'play_file'
                source = json.dumps([item])
                url = build_url({'mode': mode, 'name': title, 'title': title, 'id': item_id, 'source': source})
                listitem = xbmcgui.ListItem(item.get("label"))
                listitem.setArt({'poster': poster})
                if paginate_results:
                    return_from_pagination_params = {'mode': 'play_return_from_pagination', 'previous_nav': previous_nav}
                    cm.append(("[B]Exit Results[/B]",'XBMC.RunPlugin(%s)' % build_url(return_from_pagination_params)))
                listitem.addContextMenuItems(cm)
                item_list.append({'list_item': (url, listitem, False), 'position': position})
            except: pass
        def _build_directory(item, position=None):
            try:
                title = item.get('title')
                item_id = item.get('id', None)
                scrape_provider = item['scrape_provider']
                uncached_furk = True if scrape_provider == 'furk' and 'uncached' in item else False
                uncached_torrent = True if 'Uncached' in item.get('cache_provider', '') else False
                uncached = True if True in (uncached_furk, uncached_torrent) else False
                mode = 'furk.add_uncached_file' if uncached_furk else 'play_file'
                source = json.dumps([item])
                url = build_url({'mode': mode, 'name': title, 'title': title, 'id': item_id, 'source': source})
                name = item.get('name')
                url_dl = item.get('url_dl')
                cm = []
                if multiline_label:
                    display = item.get("multiline_label")
                else:
                    display = item.get("label")
                listitem = xbmcgui.ListItem(display)
                listitem.setInfo('video', {'plot': meta['plot']})
                listitem.setArt({'poster': poster, 'fanart': meta['fanart'], 'thumb': poster, 'clearlogo': meta['clearlogo']})
                if paginate_results:
                    return_from_pagination_params = {'mode': 'play_return_from_pagination', 'previous_nav': previous_nav}
                    cm.append(("[B]Exit Results[/B]",'XBMC.RunPlugin(%s)' % build_url(return_from_pagination_params)))
                if not uncached:
                    if scrape_provider not in self.file_scrapers:
                        down_file_params = {'mode': 'download_file', 'name': meta.get('rootname'), 'url': url_dl, 'source': source, 'meta': meta_json}
                        if scrape_provider == 'furk': down_file_params['archive'] = True
                        cm.append(("[B]Download File[/B]",'XBMC.RunPlugin(%s)' % build_url(down_file_params)))
                    if scrape_provider == 'furk':
                        if 'PACK' in display:
                            down_archive_params = {'mode': 'download_file', 'name': name, 'url': url_dl, 'db_type': 'archive', 'image': default_furk_icon}
                            cm.append(("[B]Download Archive[/B]",'XBMC.RunPlugin(%s)' % build_url(down_archive_params)))
                        browse_pack_params = {'mode': 'furk.browse_packs', 'file_name': name, 'file_id': item_id}
                        add_files_params = {'mode': 'furk.add_to_files', 'name': name, 'item_id': item_id}
                        cm.append(("[B]Browse Furk Folder[/B]",'XBMC.RunPlugin(%s)'  % build_url(browse_pack_params)))
                        cm.append(("[B]Add to My Files[/B]",'XBMC.RunPlugin(%s)'  % build_url(add_files_params)))
                listitem.addContextMenuItems(cm)
                item_list.append({'list_item': (url, listitem, False), 'position': position})
            except: pass
        try: results = json.loads(window.getProperty('fen_search_results'))
        except: return
        paginate_results = True if __addon__.getSetting('results.paginate') == 'true' else False
        if paginate_results:
            from modules.nav_utils import paginate_list
            if not previous_nav: previous_nav = xbmc.getInfoLabel('Container.FolderPath')
            try: limit = int(__addon__.getSetting('results.page_limit'))
            except: limit = 300
            if not page_no: page_no = 1
            page_no = int(page_no)
            next_page = page_no + 1
            results, total_pages = paginate_list(results, page_no, 'None', limit)
        meta_json = window.getProperty('fen_media_meta')
        meta = json.loads(meta_json)
        if meta.get('use_animated_poster', False): poster = meta.get('gif_poster')
        else: poster = meta.get('poster')
        multiline_label = settings.multiline_results()
        build_results = _build_simple_directory if self.display_mode == 1 else _build_directory
        item_list = []
        threads = []
        for position, item in enumerate(results): threads.append(Thread(target=build_results, args=(item, position)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        item_list.sort(key=lambda k: k['position'])
        xbmcplugin.addDirectoryItems(__handle__, [i['list_item'] for i in item_list])
        if paginate_results:
            if limit == len(results):
                icon = os.path.join(settings.get_theme(), 'item_next.png')
                next_page_url = build_url({'mode': 'play_display_results', 'page_no': str(next_page), 'previous_nav': previous_nav})
                listitem = xbmcgui.ListItem('Continue to [B]Page %s[/B] >>' % str(next_page))
                listitem.setArt({'icon': icon, 'fanart': __addon__.getAddonInfo('fanart')})
                listitem.setInfo('video', {'plot': 'Continue to [B]Page %s[/B]...' % str(next_page)})
                xbmcplugin.addDirectoryItem(handle=__handle__, url=next_page_url, listitem=listitem, isFolder=True)
        sleep = 1500 if len(results) <= 250 else 3000
        xbmcplugin.setContent(__handle__, 'files')
        xbmcplugin.endOfDirectory(__handle__)
        xbmc.sleep(sleep)
        setView('view.search_results')

    def return_from_pagination(self, previous_nav):
        return xbmc.executebuiltin('Container.Update(%s,replace)' % previous_nav)

    def dialog_results(self):
        hide_busy_dialog()
        close_all_dialog()
        multiline_label = settings.multiline_results()
        links_list = []
        results = json.loads(window.getProperty('fen_search_results'))
        for item in results:
            if multiline_label: listitem = xbmcgui.ListItem(item.get("multiline_label"))
            else: listitem = xbmcgui.ListItem(item.get("label"))
            listitem.setProperty('IsPlayable', 'false')
            links_list.append(listitem)
        chosen = dialog.select("Fen Results", links_list)
        if chosen < 0: return
        chosen_result = results[chosen]
        if chosen_result.get('uncached', False):
            return add_uncached_file(chosen_result.get('name'), chosen_result.get('id'))
        return self.play_file(chosen_result.get('title'), json.dumps([chosen_result]))

    def play_auto_nextep(self):
        try: results = json.loads(window.getProperty('fen_search_results'))
        except: return
        from modules.player import FenPlayer
        meta = json.loads(window.getProperty('fen_media_meta'))
        url = self.play_auto(background=True)
        notification('%s %s S%02dE%02d' % ('[B]Next Up:[/B]', meta['title'], meta['season'], meta['episode']), 10000, meta['poster'])
        player = xbmc.Player()
        while player.isPlaying():
            xbmc.sleep(100)
        xbmc.sleep(500)
        if 'plugin://' in url:
            return xbmc.executebuiltin("RunPlugin({0})".format(url))
        FenPlayer().run(url)

    def _no_results(self):
        hide_busy_dialog()
        xbmc.sleep(500)
        if self.background:
            return notification('%s %s' % ('[B]Next Up:[/B]', '[I]No results found.[/I]'), 10000)
        return dialog.ok('Fen', 'No Results')

    def _search_info(self):
        search_title = self._get_search_title()
        ep_name = self._get_ep_name()
        return {'db_type': self.vid_type, 'title': search_title, 'year': self.meta.get('year'),
        'tmdb_id': self.tmdb_id, 'imdb_id': self.meta.get('imdb_id'), 'season': self.season,
        'episode': self.episode, 'premiered': self.meta.get('premiered'), 'tvdb_id': self.meta.get('tvdb_id'),
        'ep_name': ep_name, 'language': self.language, 'scraper_settings': json.dumps(settings.scraping_settings())}

    def _get_search_title(self):
        if 'search_title' in self.meta:
            if self.language != 'en': search_title = self.meta['original_title']
            else: search_title = self.meta['search_title']
        else: search_title = self.meta['title']
        if '(' in search_title: search_title = search_title.split('(')[0]
        return search_title

    def _get_ep_name(self):
        try: ep_name = to_utf8(safe_string(remove_accents(self.meta.get('ep_name'))))
        except: ep_name = to_utf8(safe_string(self.meta.get('ep_name')))
        return ep_name

    def _quality_filter(self):
        setting = 'results_quality' if not self.autoplay else 'autoplay_quality'
        quality_filter = settings.quality_filter(setting)
        if self.include_prerelease_results: quality_filter += ['SCR', 'CAM', 'TELE']
        return quality_filter

    def _get_quality_rank(self, quality):
        if quality == '4K': return 1
        if quality == '1080p': return 2
        if quality == '720p': return 3
        if quality == 'SD': return 4
        if quality in ['SCR', 'CAM', 'TELE']: return 5
        return 6

    def _get_debrid_rank(self, debrid):
        if debrid != '': return 2
        else: return 3

    def _get_torrent_rank(self, item):
        source = item['source'].lower()
        if source == 'torrent':
            cache_provider = item['cache_provider']
            if 'Uncached' in cache_provider: return 3
            if cache_provider == 'Unchecked': return 4
            return 2
        else: return 5

    def _get_name_rank(self, provider):
        if self.internal_scraper_order[0] in provider: return ['1'] * 10
        if self.internal_scraper_order[1] in provider: return ['1'] * 11
        if self.internal_scraper_order[2] in provider: return ['1'] * 12
        if self.internal_scraper_order[3] in provider: return ['1'] * 13

    def _sort_hevc(self, results):
        if self.autoplay_hevc == '': self.autoplay_hevc == 'Include'
        if self.autoplay_hevc == 'Exclude':
            results = [i for i in results if not 'HEVC' in i['label']]
        elif self.autoplay_hevc == 'Prefer':
            hevc_list = [i for i in results if 'HEVC' in i['label']]
            non_hevc_list = [i for i in results if not i in hevc_list]
            results = hevc_list + non_hevc_list
        return results

    def _sort_first(self, provider, results):
        try:
            inserts = []
            result = [i for i in results if i['scrape_provider'] == provider]
            for i in result:
                inserts.append(i)
                results.remove(i)
            inserts = sorted(inserts, key=lambda k: k['quality_rank'], reverse=True)
            for i in inserts: results.insert(0, i)
        except: pass
        return results

    def _grab_meta(self):
        import tikimeta
        meta_user_info = tikimeta.retrieve_user_info()
        window.setProperty('fen_fanart_error', 'true')
        if self.vid_type == "movie":
            self.meta = tikimeta.movie_meta('tmdb_id', self.tmdb_id, meta_user_info)
            if not 'rootname' in self.meta: self.meta['rootname'] = '{0} ({1})'.format(self.meta['title'], self.meta['year'])
        else:
            self.meta = tikimeta.tvshow_meta('tmdb_id', self.tmdb_id, meta_user_info)
            episodes_data = tikimeta.season_episodes_meta(self.meta['tmdb_id'], self.meta['tvdb_id'], self.season, self.meta['tvdb_summary']['airedSeasons'], self.meta['season_data'], meta_user_info)
            try:
                display_name = '%s - %dx%.2d' % (self.meta['title'], self.season, self.episode)
                episode_data = [i for i in episodes_data if i['episode'] == int(self.episode)][0]
                self.meta.update({'vid_type': 'episode', 'rootname': display_name, 'season': episode_data['season'],
                            'episode': episode_data['episode'], 'premiered': episode_data['premiered'], 'ep_name': episode_data['title'],
                            'plot': episode_data['plot']})
            except: pass

    def _check_reset_external_scrapers(self):
        def _reset_scrapers():
            try:
                toggle_all('all_eng', 'true', silent=True)
                external_scrapers_reset_stats(silent=True)
                notification('All Scrapers Reset', 3000)
                xbmc.sleep(500)
            except:
                notification('ERROR Resetting Scrapers', 3000)
        def _get_timestamp(date_time):
            return int(time.mktime(date_time.timetuple()))
        try:
            reset = int(__addon__.getSetting('failing_scrapers.reset'))
            if reset == 0: return
            if reset in (1,2):
                current_time = _get_timestamp(datetime.now())
                hours = 24 if reset == 1 else 168
                expiration = timedelta(hours=hours)
                try:
                    expires_time = int(__addon__.getSetting('failing_scrapers.reset_time'))
                except:
                    expires_time = _get_timestamp(datetime.now() + expiration)
                    return __addon__.setSetting('failing_scrapers.reset_time', str(expires_time))
                if current_time < expires_time: return
                expires_time = _get_timestamp(datetime.now() + expiration)
                __addon__.setSetting('failing_scrapers.reset_time', str(expires_time))
            else:
                current_os_version = xbmcaddon.Addon(id='script.module.openscrapers').getAddonInfo('version')
                saved_os_version = __addon__.getSetting('openscrapers.version')
                if saved_os_version in (None, ''): return __addon__.setSetting('openscrapers.version', str(current_os_version))
                if current_os_version == saved_os_version: return
                __addon__.setSetting('openscrapers.version', str(current_os_version))
            _reset_scrapers()
        except: pass

    def _activate_resolveURL(self, setting='true'):
        try:
            __resolveURL__.setSetting('RapidgatorResolver_enabled', setting)
            xbmc.sleep(100)
            for item in ('login', 'premium'):
                __resolveURL__.setSetting('RapidgatorResolver_%s' % item, setting)
                xbmc.sleep(100)
            xbmc.sleep(500)
        except: pass

    def _clear_sources(self):
        for item in ('local_source_results', 'downloads_source_results', 'furk_source_results', 'folder1_source_results', 'folder2_source_results',
                    'folder3_source_results', 'folder4_source_results', 'folder5_source_results', 'easynews_source_results', 'pm-cloud_source_results',
                    'rd-cloud_source_results', 'ad-cloud_source_results', 'fen_media_meta', 'fen_search_results'):
            window.clearProperty(item)

    def play_file(self, title, source):
        from modules.player import FenPlayer
        def _uncached_confirm(item):
            if not dialog.yesno('FEN - Uncached Torrent', 'Download this Torrent to your [B]%s[/B] Cloud?' % item['debrid'].upper()):
                return None
            else:
                self.caching_confirmed = True
                return item
        try:
            next = []
            prev = []
            total = []
            results = json.loads(window.getProperty('fen_search_results'))
            results = [i for i in results if not i.get('uncached', False)]
            results = [i for i in results if not 'Uncached' in i.get('cache_provider', '') or i == json.loads(source)[0]]
            source_index = results.index(json.loads(source)[0])
            for i in range(1, 25):
                try:
                    u = results[i+source_index]
                    if u in total:
                        raise Exception()
                    total.append(u)
                    next.append(u)
                except Exception:
                    break
            for i in range(-25, 0)[::-1]:
                try:
                    u = results[i+source_index]
                    if u in total:
                        raise Exception()
                    total.append(u)
                    prev.append(u)
                except Exception:
                    break
            items = json.loads(source)
            items = [i for i in items+next+prev][:40]
            header = "Fen"
            header2 = header.upper()
            progressDialog = xbmcgui.DialogProgress()
            progressDialog.create(header, '')
            progressDialog.update(0)
            block = None
            for i in range(len(items)):
                try:
                    self.url = None
                    self.caching_confirmed = False
                    try:
                        if progressDialog.iscanceled():
                            break
                        progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
                    except Exception:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))
                    if items[i]['source'] == block:
                        raise Exception()
                    w = Thread(target=self.resolve_sources, args=(items[i],))
                    w.start()
                    offset = 60 * 2 if items[i].get('source') in ['hugefiles.net', 'kingfiles.net', 'openload.io', 'openload.co', 'oload.tv', 'thevideo.me', 'vidup.me', 'streamin.to', 'torba.se'] else 0
                    m = ''
                    for x in range(3600):
                        try:
                            if xbmc.abortRequested is True:
                                return sys.exit()
                            if progressDialog.iscanceled():
                                return progressDialog.close()
                        except Exception:
                            pass
                        k = xbmc.getCondVisibility('Window.IsActive(virtualkeyboard)')
                        if k:
                            m += '1'
                            m = m[-1]
                        if (w.is_alive() is False or x > 30 + offset) and not k:
                            break
                        k = xbmc.getCondVisibility('Window.IsActive(yesnoDialog)')
                        if k:
                            m += '1'
                            m = m[-1]
                        if (w.is_alive() is False or x > 30 + offset) and not k:
                            break
                        time.sleep(0.5)
                    for x in range(30):
                        try:
                            if xbmc.abortRequested is True:
                                return sys.exit()
                            if progressDialog.iscanceled():
                                return progressDialog.close()
                        except Exception:
                            pass
                        if m == '':
                            break
                        if w.is_alive() is False:
                            break
                        time.sleep(0.5)
                    if w.is_alive() is True:
                        block = items[i]['source']
                    if self.url == 'uncached':
                        self.url = _uncached_confirm(items[i])
                    if self.url is None:
                        raise Exception()
                    try:
                        progressDialog.close()
                    except Exception:
                        pass
                    xbmc.sleep(200)
                    if self.url: break
                except Exception: pass
            try: progressDialog.close()
            except Exception: pass
            if self.caching_confirmed:
                return self.resolve_sources(self.url, cache_item=True)
            return FenPlayer().run(self.url)
        except Exception:
            pass

    def play_auto(self, background=False):
        meta = json.loads(window.getProperty('fen_media_meta'))
        items = json.loads(window.getProperty('fen_search_results'))
        items = [i for i in items if not i.get('uncached', False)]
        items = [i for i in items if not 'Uncached' in i.get('cache_provider', '')]
        filter = [i for i in items if i['source'].lower() in ['hugefiles.net', 'kingfiles.net', 'openload.io', 'openload.co', 'oload.tv', 'thevideo.me', 'vidup.me', 'streamin.to', 'torba.se'] and i['debrid'] == '']
        items = [i for i in items if i not in filter]
        u = None
        if background:
            for i in range(len(items)):
                try:
                    if xbmc.abortRequested is True:
                        return sys.exit()
                    url = self.resolve_sources(items[i])
                    if u is None:
                        u = url
                    if url is not None:
                        break
                except Exception:
                    pass
            return self.url
        if not self.suppress_notifications:
            self.suppress_notifications = True if (__addon__.getSetting('auto_play'), __addon__.getSetting('autoplay_minimal_notifications')) == ('true', 'true') else False
        if self.suppress_notifications:
            show_busy_dialog()
            for i in range(len(items)):
                try:
                    if xbmc.abortRequested is True:
                        return sys.exit()
                    url = self.resolve_sources(items[i])
                    if 'plugin://' in url:
                        hide_busy_dialog()
                        return xbmc.executebuiltin("RunPlugin({0})".format(url))
                    if u is None:
                        u = url
                    if url is not None:
                        break
                except Exception:
                    pass
        else:
            header = "Fen"
            header2 = header.upper()
            try:
                progressDialog = xbmcgui.DialogProgress()
                progressDialog.create(header, '')
                progressDialog.update(0)
            except Exception:
                pass
            for i in range(len(items)):
                try:
                    if progressDialog.iscanceled():
                        break
                    progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
                except Exception:
                    progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))
                try:
                    if xbmc.abortRequested is True:
                        return sys.exit()
                    url = self.resolve_sources(items[i])
                    if 'plugin://' in url:
                        try: progressDialog.close()
                        except Exception: pass
                        hide_busy_dialog()
                        return xbmc.executebuiltin("RunPlugin({0})".format(url))
                    if u is None:
                        u = url
                    if url is not None:
                        break
                except Exception:
                    pass
            try: progressDialog.close()
            except Exception: pass
        hide_busy_dialog()
        from modules.player import FenPlayer
        FenPlayer().run(self.url)
        return u

    def furkTFile(self, file_name, file_id):
        from apis.furk_api import FurkAPI
        from indexers.furk import get_release_quality
        hide_busy_dialog()
        close_all_dialog()
        t_files = FurkAPI().t_files(file_id)
        t_files = [i for i in t_files if 'video' in i['ct'] and 'bitrate' in i]
        display_list = []
        display_list = ['%02d | [B]%s[/B] | [B]%.2f GB[/B] | [I]%s[/I]' % \
                        (count, get_release_quality(i['name'], i['url_dl'], t_file='yep')[0],
                        float(i['size'])/1073741824,
                        clean_file_name(i['name']).upper()) for count, i in enumerate(t_files, 1)]
        chosen = dialog.select(file_name, display_list)
        if chosen < 0: return None
        chosen_result = t_files[chosen]
        url_dl = chosen_result['url_dl']
        from modules.player import FenPlayer
        return FenPlayer().run(url_dl)

    def resolve_sources(self, item, cache_item=False):
        from modules import resolver
        try:
            if 'cache_provider' in item:
                if item['cache_provider'] in ('Real-Debrid', 'Premiumize.me', 'AllDebrid'):
                    url = resolver.resolve_cached_torrents(item['cache_provider'], item['url'], item['hash'])
                    self.url = url
                    return url
                if item['cache_provider'] == 'Unchecked':
                    url = resolver.resolve_unchecked_torrents(item['debrid'], item['url'], item['hash'])
                    self.url = url
                    return url
                if 'Uncached' in item['cache_provider']:
                    if cache_item:
                        url = resolver.resolve_uncached_torrents(item['debrid'], item['url'], item['hash'])
                        if not url: return None
                        from modules.player import FenPlayer
                        return FenPlayer().run(url)
                    else:
                        url = 'uncached'
                        self.url = url
                        return url
                    return None
            if item.get('scrape_provider', None) in self.internal_scrapers:
                url = resolver.resolve_internal_sources(item['scrape_provider'], item['id'], item['url_dl'], item.get('direct_debrid_link', False))
                self.url = url
                return url
            if item['debrid'] in ('Real-Debrid', 'Premiumize.me', 'AllDebrid') and not item['source'].lower() == 'torrent':
                from openscrapers import sources
                self.sourceDict = sources()
                call = [i[1] for i in self.sourceDict if i[0] == item['provider']][0]
                url = call.resolve(item['url'])
                url = resolver.resolve_debrid(item['debrid'], url)
                if url is not None:
                    self.url = url
                    return url
                else:
                    return None
            else:
                url = resolver.resolve_free_links(item['url'], item['provider'], item['direct'])
                self.url = url
                return url
        except Exception:
            return
