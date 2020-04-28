# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcgui, xbmcvfs
import os
import sys
import re
import json
import datetime
import time
from threading import Thread
try:
    from sqlite3 import dbapi2 as database
except Exception:
    from pysqlite2 import dbapi2 as database
from modules.nav_utils import show_busy_dialog, hide_busy_dialog
from modules.utils import byteify, clean_file_name
from modules import debrid
from modules import external_source_utils
from openscrapers import sources
try:
    import resolveurl
except Exception:
    pass
# from modules.utils import logger

__fen__ = xbmcaddon.Addon(id='plugin.video.fen')
__external__ = xbmcaddon.Addon(id='script.module.openscrapers')
fen_icon = __fen__.getAddonInfo('icon')
dialog = xbmcgui.Dialog()
window = xbmcgui.Window(10000)

class ExternalSource:
    def __init__(self):
        self.scrape_provider = 'external'
        self.sources = []
        self.source_results = []
        self.duplicates = 0
        self.database_timeout = 60.0
        self.exportSettings()
        self.getConstants()

    def results(self, info):
        self.info = info
        self.scraper_settings = json.loads(info['scraper_settings'])
        results = self.getSources((info['title'] if info['db_type'] == 'movie' else info['ep_name']),
                            info['year'], info['imdb_id'], info['tvdb_id'], info['season'], info['episode'],
                            (info['title'] if info['db_type'] == 'episode' else None), info['premiered'], info['language'])
        return results

    def getSources(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, language):
        def _processLabels(background=False):
            if background:
                self.source_4k = len([e for e in self.sources if e['quality'] == '4K']) + self.internalSources4K
                self.source_1080 = len([e for e in self.sources if e['quality'] in ['1440p', '1080p']]) + self.internalSources1080p
                self.source_720 = len([e for e in self.sources if e['quality'] in ['720p', 'HD']]) + self.internalSources720p
                self.source_sd = len([e for e in self.sources if e['quality'] == 'SD']) + self.internalSourcesSD
                self.total = self.source_4k + self.source_1080 + self.source_720 + self.source_sd + self.internalSourcesTotal
            else:
                self.source_4k = len([e for e in self.sources if e['quality'] == '4K'])
                self.source_1080 = len([e for e in self.sources if e['quality'] in ['1440p', '1080p']])
                self.source_720 = len([e for e in self.sources if e['quality'] in ['720p', 'HD']])
                self.source_sd = len([e for e in self.sources if e['quality'] == 'SD'])
                self.total = self.source_4k + self.source_1080 + self.source_720 + self.source_sd
                self.internalSource_4k_label = total_format % (int_dialog_highlight, self.internalSources4K)
                self.internalSource_1080_label = total_format % (int_dialog_highlight, self.internalSources1080p)
                self.internalSource_720_label = total_format % (int_dialog_highlight, self.internalSources720p)
                self.internalSource_sd_label = total_format % (int_dialog_highlight, self.internalSourcesSD)
                self.internalSource_total_label = total_format % (int_dialog_highlight, self.internalSourcesTotal)
            self.source_4k_label = total_format % (ext_dialog_highlight, self.source_4k)
            self.source_1080_label = total_format % (ext_dialog_highlight, self.source_1080)
            self.source_720_label = total_format % (ext_dialog_highlight, self.source_720)
            self.source_sd_label = total_format % (ext_dialog_highlight, self.source_sd)
            self.source_total_label = total_format % (ext_dialog_highlight, self.total)
        def _scraperDialog():
            diag_format = ' 4K: %s | 1080p: %s | 720p: %s | SD: %s | %s: %s'.split('|')
            exonly_diag_format = '4K: %s | 1080p: %s | 720p: %s | SD: %s | %s: %s'
            for i in range(0, 4 * timeout):
                try:
                    if xbmc.abortRequested == True: return sys.exit()
                    try:
                        if progressDialog.iscanceled(): break
                    except Exception: pass
                    self.internalResults()
                    _processLabels()
                    current_time = time.time()
                    current_progress = current_time - start_time
                    if current_time < end_time:
                        try:
                            mainleft = [sourcelabelDict[x.getName()] for x in threads if x.is_alive() is True and x.getName() in mainsourceDict]
                            info = [sourcelabelDict[x.getName()] for x in threads if x.is_alive() is True]
                            if self.internal_activated:
                                line1 = ('%s:' + '|'.join(diag_format)) % (string6, self.internalSource_4k_label, self.internalSource_1080_label,
                                                          self.internalSource_720_label, self.internalSource_sd_label, str(string4), self.internalSource_total_label)
                                line2 = ('%s:' + '|'.join(diag_format)) % (string7, self.source_4k_label, self.source_1080_label, self.source_720_label, self.source_sd_label, str(string4), self.source_total_label)
                            else:
                                line1 = string7
                                line2 = exonly_diag_format % (self.source_4k_label, self.source_1080_label, self.source_720_label, self.source_sd_label, str(string4), self.source_total_label)
                            if len(info) > 6: line3 = string3 % (str(len(info)))
                            elif len(info) > 0: line3 = string3 % (', '.join(info))
                            else: break
                            percent = int((current_progress/float(timeout))*100)
                            progressDialog.update(percent, line1, line2, line3)
                            if pre_emp == 'true':
                                pre_emp_compare = self.source_4k if pre_emp_quality == '4k' else self.source_1080 if pre_emp_quality == '1080p' else self.source_720 if pre_emp_quality == '720p' else self.source_sd if pre_emp_quality == 'SD' else self.total
                                if pre_emp_compare >= int(pre_emp_limit): break
                            if finish_early == 'true' and percent >= 50:
                                if len(info) <= 5: break
                                if len(self.sources) >= 100 * len(info): break
                        except: pass
                    else:
                        try:
                            mainleft = [sourcelabelDict[x.getName()] for x in threads if x.is_alive() is True and x.getName() in mainsourceDict]
                            info = mainleft
                            if len(info) > 6: line3 = 'Waiting for: %s' % (str(len(info)))
                            elif len(info) > 0: line3 = 'Waiting for: %s' % (', '.join(info))
                            else: break
                            percent = int((current_progress/float(timeout))*100) % 100
                            progressDialog.update(percent, line1, line2, line3)
                        except Exception: break
                    time.sleep(0.5)
                except Exception: pass
            try: progressDialog.close()
            except Exception: pass
        def _scraperDialogBG():
            diag_format = '4K:%s|1080p:%s|720p:%s|SD:%s|T:%s'.split('|')
            for i in range(0, 4 * timeout):
                try:
                    if xbmc.abortRequested == True: return sys.exit()
                    try:
                        if progressDialog.iscanceled(): break
                    except Exception: pass
                    self.internalResults()
                    _processLabels(background=True)
                    current_time = time.time()
                    current_progress = current_time - start_time
                    if current_time < end_time:
                        try:
                            mainleft = [sourcelabelDict[x.getName()] for x in threads if x.is_alive() is True and x.getName() in mainsourceDict]
                            info = [sourcelabelDict[x.getName()] for x in threads if x.is_alive() is True]
                            line1 = '|'.join(diag_format) % (self.source_4k_label, self.source_1080_label, self.source_720_label, self.source_sd_label, self.source_total_label)
                            if len(info) > 0: line2 = string3 % (str(len(info)))
                            else: break
                            percent = int((current_progress/float(timeout))*100)
                            progressDialog.update(percent, line1, line2)
                            if pre_emp == 'true':
                                pre_emp_compare = self.source_4k if pre_emp_quality == '4k' else self.source_1080 if pre_emp_quality == '1080p' else self.source_720 if pre_emp_quality == '720p' else self.source_sd if pre_emp_quality == 'SD' else self.total
                                if pre_emp_compare >= int(pre_emp_limit): break
                            if finish_early == 'true' and percent >= 50:
                                if len(info) <= 5: break
                                if len(self.sources) >= 100 * len(info): break
                        except: pass
                    else: break
                    time.sleep(0.5)
                except Exception: pass
            try: progressDialog.close()
            except Exception: pass
        def _background():
            while time.time() < end_time:
                time.sleep(0.5)
                _processLabels(background=True)
                if pre_emp == 'true':
                    pre_emp_compare = self.source_4k if pre_emp_quality == '4k' else self.source_1080 if pre_emp_quality == '1080p' else self.source_720 if pre_emp_quality == '720p' else self.source_sd if pre_emp_quality == 'SD' else self.total
                    if pre_emp_compare >= int(pre_emp_limit): break
                info = [sourcelabelDict[x.getName()] for x in threads if x.is_alive() is True]
                if len(info) <= 5: break
                if len(self.sources) >= 100 * len(info): break
        if self.remove_failing_sources == 'true': self.sourcesRemoveFailing()
        content = 'movie' if tvshowtitle is None else 'episode'
        progressDialog = None
        if not self.background:
            if self.dialog_background: progressDialog = xbmcgui.DialogProgressBG()
            else: progressDialog = xbmcgui.DialogProgress()
            if content == 'movie': progressTitle = self.meta.get('rootname') if self.progressHeading == 1 else self.moduleProvider
            else: progressTitle = self.meta.get('rootname') if self.progressHeading == 1 else self.moduleProvider
            progressDialog.create(progressTitle, '')
            progressDialog.update(0)
            progressDialog.update(0, 'Preparing sources')
        sourceDict = self.sourceDict
        if content == 'movie': sourceDict = [(i[0], i[1], getattr(i[1], 'movie', None)) for i in sourceDict]
        else: sourceDict = [(i[0], i[1], getattr(i[1], 'tvshow', None)) for i in sourceDict]
        sourceDict = [(i[0], i[1]) for i in sourceDict if not i[2] is None]
        try: sourceDict = [(i[0], i[1], __external__.getSetting('provider.' + i[0])) for i in sourceDict]
        except Exception: sourceDict = [(i[0], i[1], 'true') for i in sourceDict]
        sourceDict = [(i[0], i[1]) for i in sourceDict if not i[2] == 'false']
        sourceDict = [(i[0], i[1], i[1].priority) for i in sourceDict]
        sourceDict = sorted(sourceDict, key=lambda i: i[2])
        threads = []
        if content == 'movie':
            title = external_source_utils.normalize(title)
            for i in sourceDict:
                threads.append(Thread(target=self.getMovieSource, args=(title, title, [], year, imdb, i[0], i[1])))
        else:
            tvshowtitle = external_source_utils.normalize(tvshowtitle)
            for i in sourceDict:
                threads.append(Thread(target=self.getEpisodeSource, args=(title, year, imdb, tvdb, season, episode, tvshowtitle, tvshowtitle, [], premiered, i[0], i[1])))
        [i.start() for i in threads]
        s = [i[0] + (i[1],) for i in zip(sourceDict, threads)]
        s = [(i[3].getName(), i[0], i[2]) for i in s]
        mainsourceDict = [i[0] for i in s if i[2] == 0]
        sourcelabelDict = dict([(i[0], i[1].upper()) for i in s])
        pre_emp = __fen__.getSetting('preemptive.termination')
        pre_emp_quality = __fen__.getSetting('preemptive.quality')
        pre_emp_limit = __fen__.getSetting('preemptive.limit')
        try: timeout = int(__fen__.getSetting('scrapers.timeout.1'))
        except: timeout = 45
        start_time = time.time()
        end_time = start_time + timeout
        int_dialog_highlight = __fen__.getSetting('int_dialog_highlight')
        if not int_dialog_highlight or int_dialog_highlight == '': int_dialog_highlight = 'darkgoldenrod'
        ext_dialog_highlight = __fen__.getSetting('ext_dialog_highlight')
        if not ext_dialog_highlight or ext_dialog_highlight == '': ext_dialog_highlight = 'dodgerblue'
        finish_early = __fen__.getSetting('search.finish.early')
        string1 = 'Time elapsed: %s seconds'
        string2 = '%s seconds'
        string3 = 'Remaining providers: %s'
        string4 = 'Total'
        if self.internal_activated:
            string6 = '[COLOR %s][B]Int[/B][/COLOR]' % int_dialog_highlight
            string7 = '[COLOR %s][B]Ext[/B][/COLOR]' % ext_dialog_highlight
        else:
            string7 = '[COLOR %s]External Scrapers[/COLOR]' % ext_dialog_highlight
        line1 = line2 = line3 = ""
        total_format = '[COLOR %s][B]%s[/B][/COLOR]'
        if self.background: _background()
        if self.dialog_background: _scraperDialogBG()
        else: _scraperDialog()
        if not self.suppress_notifications: show_busy_dialog()
        self.sourcesStats(sourceDict, self.sources)
        self.sourcesFilter()
        self.sourcesLabels()
        try:
            progressDialog.close()
        except Exception:
            pass
        return self.sources

    def getMovieSource(self, title, localtitle, aliases, year, imdb, source, call):
        try:
            dbcon = database.connect(self.providerDatabase, timeout=self.database_timeout)
            dbcur = dbcon.cursor()
            dbcur.execute('''PRAGMA synchronous = OFF''')
            dbcur.execute('''PRAGMA journal_mode = OFF''')
        except Exception:
            pass
        if imdb == '0':
            try:
                dbcur.execute("DELETE FROM rel_src WHERE source = ? AND imdb_id = ? AND season = ? AND episode = ?", (source, imdb, '', ''))
                dbcur.execute("DELETE FROM rel_url WHERE source = ? AND imdb_id = ? AND season = ? AND episode = ?", (source, imdb, '', ''))
                dbcon.commit()
            except Exception:
                pass
        try:
            sources = []
            dbcur.execute("SELECT * FROM rel_src WHERE source = ? AND imdb_id = ? AND season = ? AND episode = ?", (source, imdb, '', ''))
            match = dbcur.fetchone()
            t1 = int(re.sub('[^0-9]', '', str(match[5])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) > 120
            if update is False:
                sources = eval(match[4].encode('utf-8'))
                return self.sources.extend(sources)
        except Exception:
            pass
        try:
            url = None
            dbcur.execute("SELECT * FROM rel_url WHERE source = ? AND imdb_id = ? AND season = ? AND episode = ?", (source, imdb, '', ''))
            url = dbcur.fetchone()
            url = eval(url[4].encode('utf-8'))
        except Exception:
            pass
        try:
            if url is None:
                url = call.movie(imdb, title, localtitle, aliases, year)
            if url is None:
                return
            dbcur.execute("DELETE FROM rel_url WHERE source = ? AND imdb_id = ? AND season = ? AND episode = ?", (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, '', '', repr(url)))
            dbcon.commit()
        except Exception:
            pass
        try:
            sources = []
            sources = call.sources(url, self.hostDict, self.hostprDict)
            sources = [json.loads(t) for t in set(json.dumps(d, sort_keys=True) for d in sources)]
            sources = self.sourcesUpdate(source, sources)
            self.sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = ? AND imdb_id = ? AND season = ? AND episode = ?", (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, imdb, '', '', repr(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except Exception:
            pass

    def getEpisodeSource(self, title, year, imdb, tvdb, season, episode, tvshowtitle, localtvshowtitle, aliases, premiered, source, call):
        try:
            dbcon = database.connect(self.providerDatabase)
            dbcur = dbcon.cursor()
            dbcur.execute('''PRAGMA synchronous = OFF''')
            dbcur.execute('''PRAGMA journal_mode = OFF''')
        except Exception:
            pass
        try:
            sources = []
            dbcur.execute(
                "SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" %
                (source, imdb, season, episode))
            match = dbcur.fetchone()
            t1 = int(re.sub('[^0-9]', '', str(match[5])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) > 120
            if update is False:
                sources = eval(match[4].encode('utf-8'))
                return self.sources.extend(sources)
        except Exception:
            pass
        try:
            url = None
            dbcur.execute(
                "SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" %
                (source, imdb, '', ''))
            url = dbcur.fetchone()
            url = eval(url[4].encode('utf-8'))
        except Exception:
            pass
        try:
            if url is None:
                url = call.tvshow(imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year)
            if url is None:
                return
            dbcur.execute(
                "DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" %
                (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, '', '', repr(url)))
            dbcon.commit()
        except Exception:
            pass
        try:
            ep_url = None
            dbcur.execute(
                "SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" %
                (source, imdb, season, episode))
            ep_url = dbcur.fetchone()
            ep_url = eval(ep_url[4].encode('utf-8'))
        except Exception:
            pass
        try:
            if url is None:
                raise Exception()
            if ep_url is None:
                ep_url = call.episode(url, imdb, tvdb, title, premiered, season, episode)
            if ep_url is None:
                return
            dbcur.execute(
                "DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" %
                (source, imdb, season, episode))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, season, episode, repr(ep_url)))
            dbcon.commit()
        except Exception:
            pass
        try:
            sources = []
            sources = call.sources(ep_url, self.hostDict, self.hostprDict)
            sources = [json.loads(t) for t in set(json.dumps(d, sort_keys=True) for d in sources)]
            sources = self.sourcesUpdate(source, sources)
            self.sources.extend(sources)
            dbcur.execute(
                "DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" %
                (source, imdb, season, episode))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, imdb, season,
                                                                            episode, repr(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except Exception:
            pass

    def sourcesFilter(self):
        def _processFilters(d):
            for k, v in d.items():
                #TORRENTS...
                if self.torrentCheckCache == 'false':
                    self.filter += [dict(i.items() + [('debrid', k)]) for i in torrentSources if i.get('cache_provider') == 'Unchecked']
                else:
                    if k in ('Real-Debrid', 'Premiumize.me', 'AllDebrid'):
                        self.filter += [dict(i.items() + [('debrid', k)]) for i in torrentSources if k == i.get('cache_provider')]
                        if self.uncachedTorrents == 'true':
                            self.filter += [dict(i.items() + [('debrid', k)]) for i in torrentSources if 'Uncached' in i.get('cache_provider') and k in i.get('cache_provider')]
                    elif torrentSources:
                        if torrentSources[0].get('cache_provider') == 'Unchecked':
                            self.filter += [dict(i.items() + [('debrid', k)]) for i in torrentSources if i.get('cache_provider') == 'Unchecked']
                #HOSTERS
                valid_hosters = [i for i in result_hosters if i in v]
                self.filter += [dict(i.items() + [('debrid', k)]) for i in hoster_sources if i['source'].split('.')[0] in valid_hosters]
        self.torrentCheckCache = __fen__.getSetting('torrent.check.cache')
        if self.torrentCheckCache == '':  self.torrentCheckCache = 'false'
        self.uncachedTorrents = __fen__.getSetting('torrent.display.uncached')
        if self.uncachedTorrents == '': self.uncachedTorrents = 'false'
        removeDuplicates = __fen__.getSetting('remove.duplicates')
        if removeDuplicates == '': removeDuplicates = 'false'
        removeDuplicatesTorrents = __fen__.getSetting('remove.duplicates.torrents')
        if removeDuplicatesTorrents == '': removeDuplicatesTorrents = 'false'
        include_nondebrid = __fen__.getSetting('include_nondebrid_results')
        if include_nondebrid == '':  include_nondebrid = 'true'
        captcha = __fen__.getSetting('hosts.captcha')
        if captcha == '': captcha = 'true'
        if 'true' in (removeDuplicates, removeDuplicatesTorrents):
            if len(self.sources) > 0:
                self.sources = list(self.sourcesRemoveDuplicates(self.sources, removeDuplicates, removeDuplicatesTorrents))
                if not self.suppress_notifications: dialog.notification('Fen', '[B]%d[/B] Duplicate URL%s Removed' % (self.duplicates, ('' if self.duplicates == 1 else 's')) , fen_icon, 2500, sound=False)
        hoster_sources = [i for i in self.sources if not 'hash' in i]
        
        torrentSources = self.sourcesProcessTorrents([i for i in self.sources if 'hash' in i])
        self.filter = []
        result_hosters = list(set([i['source'].split('.')[0].lower() for i in self.sources]))
        debrid_hosters = debrid.debrid_valid_hosts(self.debrid_enabled)
        for d in debrid_hosters: _processFilters(d)
        if include_nondebrid == 'true' and self.hostDict:
            self.filter += [i for i in hoster_sources if not i['source'] in self.hostprDict and i['debridonly'] is False]
        self.sources = self.filter
        if not captcha == 'true':
            filter = [i for i in self.sources if i['source'].lower() in self.hostcapDict and 'debrid' not in i]
            self.sources = [i for i in self.sources if i not in filter]
        filter = [i for i in self.sources if i['source'].lower() in self.hostblockDict and 'debrid' not in i]
        self.sources = [i for i in self.sources if i not in filter]
        self.sources = self.sources[:2500]

    def sourcesLabels(self):
        def _processLabels(item):
            try:
                extraInfo = item.get('extraInfo', None)
                URLName = item.get('URLName', None)
                provider = item['provider']
                try: size = item['size_label']
                except: size = None
                quality = item['quality']
                source = item['source']
                source = source.rsplit('.', 1)[0]
                debrid = item.get('debrid', None)
                cache_provider = item.get('cache_provider', None)
                if debrid:
                    if debrid.lower() == 'real-debrid':
                        if cache_provider:
                            if cache_provider == 'Unchecked': debrid = 'RD UNCHECKED'
                            elif 'Uncached' in cache_provider and debrid in cache_provider: debrid = 'RD UNCACHED'
                            else: debrid = '[B]RD CACHED[/B]'
                        else: debrid = 'RD'
                    elif debrid.lower() == 'premiumize.me':
                        if cache_provider:
                            if cache_provider == 'Unchecked': debrid = 'PM UNCHECKED'
                            elif 'Uncached' in cache_provider and debrid in cache_provider: debrid = 'PM UNCACHED'
                            else: debrid = '[B]PM CACHED[/B]'
                        else: debrid = 'PM'
                    elif debrid.lower() == 'alldebrid':
                        if cache_provider:
                            if cache_provider == 'Unchecked': debrid = 'AD UNCHECKED'
                            elif 'Uncached' in cache_provider and debrid in cache_provider: debrid = 'AD UNCACHED'
                            else: debrid = '[B]AD CACHED[/B]'
                        else: debrid = 'AD'
                else:
                    item['debrid'] = ''
                label = ''
                multiline_label1 = ''
                multiline_label2 = '\n        '
                if debrid:
                    label += debrid
                    multiline_label1 += debrid
                else:
                    label += provider
                    multiline_label1 += provider
                if quality.upper() in ['4K', '1080P', '720P', 'TELE', 'SCR', 'CAM']:
                    label += ' | [I][B]%s[/B][/I]' % quality
                    multiline_label1 += ' | [I][B]%s[/B][/I]' % quality
                else:
                    label += ' | [I]SD[/I]'
                    multiline_label1 += ' | [I]SD[/I]'
                if size not in ('0', '0.0', '0 GB', '0.0 GB', '0.00 GB', '', 'None', None):
                    label += ' | %s' % size
                    multiline_label1 += ' | %s' % size
                if debrid:
                    label += ' | %s' % provider
                    multiline_label1 += ' | %s' % provider
                if source.lower() == 'torrent' and any(i in cache_provider for i in ('Unchecked', 'Uncached')) and 'seeders' in item:
                    label += ' | %s SEEDS' % item['seeders']
                    multiline_label1 += ' | %s SEEDS' % item['seeders']
                else:
                    label += ' | %s' % source
                    multiline_label1 += ' | %s' % source
                if enableExtraInfo:
                    if extraInfo: label += ' | %s' % extraInfo
                    if enableShowFilenames:
                        if URLName: label += ' | %s' % URLName
                        if extraInfo: multiline_label1 += ' | %s' % extraInfo
                        if URLName: multiline_label2 += URLName
                    else:
                        if extraInfo: multiline_label2 += extraInfo
                elif enableShowFilenames:
                    if URLName: label += ' | %s' % URLName
                    if URLName: multiline_label2 += URLName
                label = label.replace('| 0 |', '|').replace(' | [I]0 [/I]', '').replace('[I] [/I] | ', '')
                label = label.upper()
                multiline_label1 = multiline_label1.replace('| 0 |', '|').replace(' | [I]0 [/I]', '').replace('[I] [/I] | ', '')
                multiline_label1 = multiline_label1.upper()
                if multiline_label2 != '':
                    multiline_label2 = multiline_label2.replace('| 0 |', '|').replace(' | [I]0 [/I]', '').replace('[I] [/I] | ', '')
                    multiline_label2 = multiline_label2.upper()
                if highlightType == '1':
                    if quality.upper() == '4K': LeadingColor = highlight_4K
                    elif quality.upper()  == '1080P': LeadingColor = highlight_1080p
                    elif quality.upper() == '720P': LeadingColor = highlight_720p
                    else: LeadingColor = highlight_SD
                    if multiLineHighlight == '': multilineOpen = LeadingColor
                    else: multilineOpen = multiLineHighlight
                    item['label'] = '[COLOR=%s]' % LeadingColor + label + '[/COLOR]'
                    item['multiline_label'] = '[COLOR=%s]' % LeadingColor + multiline_label1 + '[/COLOR]' + '[COLOR=%s]' % multilineOpen + multiline_label2 + '[/COLOR]'
                else:
                    if debrid:
                        if 'torrent' in source.lower():
                            item['label'] = singleTorrentLeading + label + singleTorrentClosing
                            item['multiline_label'] = multi1TorrentLeading + multiline_label1 + multi1TorrentClosing + multi2TorrentLeading + multiline_label2 + multi2TorrentClosing
                        else:
                            item['label'] = singlePremiumLeading + label + singlePremiumClosing
                            item['multiline_label'] = multi1PremiumLeading + multiline_label1 + multi1PremiumClosing + multi2PremiumLeading + multiline_label2 + multi2PremiumClosing
                    else:
                        item['label'] = label
                        item['multiline_label'] = multiline_label1 + multi1RegularLeading + multiline_label2 + multi1RegularClosing
            except:
                pass
        enableExtraInfo = self.scraper_settings['extra_info']
        enableShowFilenames = self.scraper_settings['show_filenames']
        enableMultiline = self.scraper_settings['multiline']
        multiLineHighlight = self.scraper_settings['multiline_highlight']
        highlightType = self.scraper_settings['highlight_type']
        if highlightType == '1':
            highlight_4K = self.scraper_settings['highlight_4K']
            highlight_1080p = self.scraper_settings['highlight_1080p']
            highlight_720p = self.scraper_settings['highlight_720p']
            highlight_SD = self.scraper_settings['highlight_SD']
        else:
            premiumHighlight = self.scraper_settings['premium_highlight']
            torrentHighlight = self.scraper_settings['torrent_highlight']
            # Single Line...
            # Torrent...
            if torrentHighlight == '':
                singleTorrentLeading = ''
                singleTorrentClosing = ''
            else:
                singleTorrentLeading = '[COLOR=%s]' % torrentHighlight
                singleTorrentClosing = '[/COLOR]'
            # Premium...
            if premiumHighlight == '':
                singlePremiumLeading = ''
                singlePremiumClosing = ''
            else:
                singlePremiumLeading = '[COLOR=%s]' % premiumHighlight
                singlePremiumClosing = '[/COLOR]'
            # Multiline...
            # Torrent...
            if torrentHighlight == '':
                multi1TorrentLeading = ''
                multi1TorrentClosing = ''
            else:
                multi1TorrentLeading = '[COLOR=%s]' % torrentHighlight
                multi1TorrentClosing = '[/COLOR]'
            if multiLineHighlight == '':
                multi2TorrentLeading = multi1TorrentLeading
                multi2TorrentClosing = multi1TorrentClosing
            else:
                multi2TorrentLeading = '[COLOR=%s]' % multiLineHighlight
                multi2TorrentClosing = '[/COLOR]'
            # Premium...
            if premiumHighlight == '':
                multi1PremiumLeading = ''
                multi1PremiumClosing = ''
            else:
                multi1PremiumLeading = '[COLOR=%s]' % premiumHighlight
                multi1PremiumClosing = '[/COLOR]'
            if multiLineHighlight == '':
                multi2PremiumLeading = multi1PremiumLeading
                multi2PremiumClosing = multi1PremiumClosing
            else:
                multi2PremiumLeading = '[COLOR=%s]' % multiLineHighlight
                multi2PremiumClosing = '[/COLOR]'
            # Regular...
            if multiLineHighlight == '':
                multi1RegularLeading = ''
                multi1RegularClosing = ''
            else:
                multi1RegularLeading = '[COLOR=%s]' % multiLineHighlight
                multi1RegularClosing = '[/COLOR]'
        threads = []
        for i in self.sources: threads.append(Thread(target=_processLabels, args=(i,)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        self.sources = [i for i in self.sources if 'label' in i and 'multiline_label' in i]

    def sourcesUpdate(self, source, sources):
        def _addInfoandName(i):
            url = i['url']
            extraInfo = external_source_utils.getFileType(url)
            URLName = external_source_utils.getFileNameMatch(self.info['title'], url, i.get('name', None))
            return _updateSource(i, {'extraInfo': extraInfo, 'URLName': URLName})
        def _updateQuality(i):
            current_quality = i['quality']
            if 'name' in i: release_name = i['name']
            else: release_name = i['url']
            quality = external_source_utils.update_release_quality(release_name, current_quality)
            i.update({'quality': quality})
        def _getSize(i):
            size = 0
            size_label = None
            try:
                size = i['size']
                size_label = '%.2f GB' % size
            except:
                pass
            return _updateSource(i, {'external_size': size, 'size_label': size_label, 'size': 0})
        def _lowercase_hash(i):
            if 'hash' in i:
                _hash = i['hash'].lower()
                i['hash'] = _hash
        def _updateSource(i, update_dict):
            i.update(update_dict)
        source = byteify(source)
        for i in sources:
            update_dict = {'provider': source, 'external': True, 'scrape_provider': self.scrape_provider}
            _updateSource(i, update_dict)
            _getSize(i)
            _addInfoandName(i)
            _updateQuality(i)
            _lowercase_hash(i)
        return sources

    def sourcesRemoveDuplicates(self, sources, removeDuplicates, removeDuplicatesTorrents):
        uniqueURLs = set()
        uniqueHashes = set()
        for source in sources:
            try:
                if removeDuplicates == 'true':
                    if source['url'] not in uniqueURLs:
                        uniqueURLs.add(source['url'])
                        if removeDuplicatesTorrents == 'true':
                            if 'hash' in source:
                                if source['hash'] not in uniqueHashes:
                                    uniqueHashes.add(source['hash'])
                                    yield source
                                else: self.duplicates += 1
                            else: yield source
                        else: yield source
                    else: self.duplicates += 1
                elif removeDuplicatesTorrents == 'true':
                    if 'hash' in source:
                        if source['hash'] not in uniqueHashes:
                            uniqueHashes.add(source['hash'])
                            yield source
                        else:
                            self.duplicates += 1
                    else: yield source
                else: yield source
            except:
                yield source
    
    def sourcesProcessTorrents(self, torrentSources):
        def _return_unchecked_sources():
            for i in torrentSources: i.update({'cache_provider': 'Unchecked'})
            return torrentSources
        if len(torrentSources) == 0: return torrentSources
        hashList = []
        for i in torrentSources:
            try:
                infoHash = str(i['hash'])
                if len(infoHash) == 40: hashList.append(infoHash)
                else: torrentSources.remove(i)
            except: torrentSources.remove(i)
        if len(torrentSources) == 0: return torrentSources
        if self.torrentCheckCache == 'false': return _return_unchecked_sources()
        try:
            if len(self.debrid_enabled) == 0: return _return_unchecked_sources()
            xbmc.sleep(100)
            DBCheck = debrid.DebridCheck()
            cachedTorrents = []
            uncachedRDTorrents = []
            uncachedPMTorrents = []
            uncachedADTorrents = []
            hashList = list(set(hashList))
            xbmc.sleep(100)
            cachedRDHashes, cachedPMHashes, cachedADHashes = DBCheck.run(hashList, self.suppress_notifications, self.debrid_enabled)
            cachedRDSources = [dict(i.items() + [('cache_provider', 'Real-Debrid')]) for i in torrentSources if any(v in i['hash'] for v in cachedRDHashes)]
            cachedPMSources = [dict(i.items() + [('cache_provider', 'Premiumize.me')]) for i in torrentSources if any(v in i['hash'] for v in cachedPMHashes)]
            cachedADSources = [dict(i.items() + [('cache_provider', 'AllDebrid')]) for i in torrentSources if any(v in i['hash'] for v in cachedADHashes)]
            for i in [('Real-Debrid', cachedRDSources), ('Premiumize.me', cachedPMSources), ('AllDebrid', cachedADSources)]:
                if i[0] in self.debrid_enabled: cachedTorrents.extend(i[1])
            if self.uncachedTorrents == 'true':
                uncachedRDTorrents = [dict(i.items() + [('cache_provider', 'Uncached Real-Debrid')]) for i in torrentSources if not i['hash'] in cachedRDHashes]
                uncachedPMTorrents = [dict(i.items() + [('cache_provider', 'Uncached Premiumize.me')]) for i in torrentSources if not i['hash'] in cachedPMHashes]
                uncachedADTorrents = [dict(i.items() + [('cache_provider', 'Uncached AllDebrid')]) for i in torrentSources if not i['hash'] in cachedADHashes]
            return cachedTorrents + uncachedRDTorrents + uncachedPMTorrents + uncachedADTorrents
        except:
            from modules.nav_utils import notification
            notification('Error Processing Torrents', time=2500)
            return _return_unchecked_sources()

    def sourcesStats(self, sourceDict, sources):
        try:
            insert_list = []
            all_sources = [i[0] for i in sourceDict]
            working_scrapers = sorted(list(set([i['provider'] for i in sources])))
            non_working_scrapers = sorted([i for i in all_sources if not i in working_scrapers])
            dbcon = database.connect(self.providerDatabase, timeout=self.database_timeout)
            dbcur = dbcon.cursor()
            dbcur.execute('''PRAGMA synchronous = OFF''')
            dbcur.execute('''PRAGMA journal_mode = OFF''')
            dbcur.execute("SELECT * FROM scr_perf")
            scraper_stats = dbcur.fetchall()
            if scraper_stats != []:
                for i in scraper_stats:
                    try:
                        scraper, success, fail = str(i[0]), i[1], i[2]
                        if scraper in working_scrapers:
                            insert_list.append((scraper, success+1, fail))
                            working_scrapers.remove(scraper)
                        else:
                            insert_list.append((scraper, success, fail+1))
                            non_working_scrapers.remove(scraper)
                    except: pass
            if len(working_scrapers) > 0:
                for scraper in working_scrapers:
                    insert_list.append((scraper, 1, 0))
            if len(non_working_scrapers) > 0:
                for scraper in non_working_scrapers:
                    insert_list.append((scraper, 0, 1))
            dbcur.executemany("INSERT OR REPLACE INTO scr_perf VALUES (?, ?, ?)", insert_list)
            dbcon.commit()
            dbcon.close()
        except: pass

    def sourcesRemoveFailing(self):
        def _check_sources(item):
            if item[1] + item[2] >= threshold:
                if float(item[2])/2 >= float(item[1]):
                    remove_sources.append(item[0])
        try:
            threads = []
            remove_sources = []
            try: threshold = int(__fen__.getSetting('failing_scrapers.threshold'))
            except: threshold = 25
            activeSources = [i[0] for i in self.sourceDict]
            scrapers = external_source_utils.external_scrapers_fail_stats()
            scrapers = [i for i in scrapers if i[0] in activeSources]
            for i in scrapers: threads.append(Thread(target=_check_sources, args=(i,)))
            [i.start() for i in threads]
            [i.join() for i in threads]
            if len(remove_sources) > 0:
                for i in remove_sources: __external__.setSetting('provider.%s' % i, 'false')
                self.sourceDict = [i for i in self.sourceDict if not i[0] in remove_sources]
                if not self.suppress_notifications:
                    dialog.notification('Fen', '[B]%d[/B] Failing Scraper%s Disabled' % (len(remove_sources), ('' if len(remove_sources) == 1 else 's')) , fen_icon, 2500, sound=False)
        except: pass

    def internalResults(self):
        if self.furk_enabled == 'true' and not self.furk_sources:
            try: furk_sources = json.loads(window.getProperty('furk_source_results'))
            except: furk_sources = []
            if furk_sources:
                self.furk_sources = len(furk_sources)
                self.furk_sources_4K = len([i for i in furk_sources if i['quality'] == '4K'])
                self.furk_sources_1080p = len([i for i in furk_sources if i['quality'] == '1080p'])
                self.furk_sources_720p = len([i for i in furk_sources if i['quality'] == '720p'])
                self.furk_sources_SD = len([i for i in furk_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
        if self.easynews_enabled == 'true' and not self.easynews_sources:
            try: easynews_sources = json.loads(window.getProperty('easynews_source_results'))
            except: easynews_sources = []
            if easynews_sources:
                self.easynews_sources = len(easynews_sources)
                self.easynews_sources_4K = len([i for i in easynews_sources if i['quality'] == '4K'])
                self.easynews_sources_1080p = len([i for i in easynews_sources if i['quality'] == '1080p'])
                self.easynews_sources_720p = len([i for i in easynews_sources if i['quality'] == '720p'])
                self.easynews_sources_SD = len([i for i in easynews_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
        if self.pm_cloud_enabled == 'true' and not self.pm_cloud_sources:
            try: pm_cloud_sources = json.loads(window.getProperty('pm-cloud_source_results'))
            except: pm_cloud_sources = []
            if pm_cloud_sources:
                self.pm_cloud_sources = len(pm_cloud_sources)
                self.pm_cloud_sources_4K = len([i for i in pm_cloud_sources if i['quality'] == '4K'])
                self.pm_cloud_sources_1080p = len([i for i in pm_cloud_sources if i['quality'] == '1080p'])
                self.pm_cloud_sources_720p = len([i for i in pm_cloud_sources if i['quality'] == '720p'])
                self.pm_cloud_sources_SD = len([i for i in pm_cloud_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
        if self.rd_cloud_enabled == 'true' and not self.rd_cloud_sources:
            try: rd_cloud_sources = json.loads(window.getProperty('rd-cloud_source_results'))
            except: rd_cloud_sources = []
            if rd_cloud_sources:
                self.rd_cloud_sources = len(rd_cloud_sources)
                self.rd_cloud_sources_4K = len([i for i in rd_cloud_sources if i['quality'] == '4K'])
                self.rd_cloud_sources_1080p = len([i for i in rd_cloud_sources if i['quality'] == '1080p'])
                self.rd_cloud_sources_720p = len([i for i in rd_cloud_sources if i['quality'] == '720p'])
                self.rd_cloud_sources_SD = len([i for i in rd_cloud_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
        if self.ad_cloud_enabled == 'true' and not self.ad_cloud_sources:
            try: ad_cloud_sources = json.loads(window.getProperty('ad-cloud_source_results'))
            except: ad_cloud_sources = []
            if ad_cloud_sources:
                self.ad_cloud_sources = len(ad_cloud_sources)
                self.ad_cloud_sources_4K = len([i for i in ad_cloud_sources if i['quality'] == '4K'])
                self.ad_cloud_sources_1080p = len([i for i in ad_cloud_sources if i['quality'] == '1080p'])
                self.ad_cloud_sources_720p = len([i for i in ad_cloud_sources if i['quality'] == '720p'])
                self.ad_cloud_sources_SD = len([i for i in ad_cloud_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
        if self.local_enabled == 'true' and not self.local_sources:
            try: local_sources = json.loads(window.getProperty('local_source_results'))
            except: local_sources = []
            if local_sources:
                self.local_sources = len(local_sources)
                self.local_sources_4K = len([i for i in local_sources if i['quality'] == '4K'])
                self.local_sources_1080p = len([i for i in local_sources if i['quality'] == '1080p'])
                self.local_sources_720p = len([i for i in local_sources if i['quality'] == '720p'])
                self.local_sources_SD = len([i for i in local_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
        if self.downloads_enabled == 'true' and not self.downloads_sources:
            try: downloads_sources = json.loads(window.getProperty('downloads_source_results'))
            except: downloads_sources = []
            if downloads_sources:
                self.downloads_sources = len(downloads_sources)
                self.downloads_sources_4K = len([i for i in downloads_sources if i['quality'] == '4K'])
                self.downloads_sources_1080p = len([i for i in downloads_sources if i['quality'] == '1080p'])
                self.downloads_sources_720p = len([i for i in downloads_sources if i['quality'] == '720p'])
                self.downloads_sources_SD = len([i for i in downloads_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
        if self.folders_enabled == 'true':
            if not self.folder1_sources:
                try: folder1_sources = json.loads(window.getProperty('folder1_source_results'))
                except: folder1_sources = []
                if folder1_sources:
                    self.folder1_sources = len(folder1_sources)
                    self.folder1_sources_4K = len([i for i in folder1_sources if i['quality'] == '4K'])
                    self.folder1_sources_1080p = len([i for i in folder1_sources if i['quality'] == '1080p'])
                    self.folder1_sources_720p = len([i for i in folder1_sources if i['quality'] == '720p'])
                    self.folder1_sources_SD = len([i for i in folder1_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
            if not self.folder2_sources:
                try: folder2_sources = json.loads(window.getProperty('folder2_source_results'))
                except: folder2_sources = []
                if folder2_sources:
                    self.folder2_sources = len(folder2_sources)
                    self.folder2_sources_4K = len([i for i in folder2_sources if i['quality'] == '4K'])
                    self.folder2_sources_1080p = len([i for i in folder2_sources if i['quality'] == '1080p'])
                    self.folder2_sources_720p = len([i for i in folder2_sources if i['quality'] == '720p'])
                    self.folder2_sources_SD = len([i for i in folder2_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
            if not self.folder3_sources:
                try: folder3_sources = json.loads(window.getProperty('folder3_source_results'))
                except: folder3_sources = []
                if folder3_sources:
                    self.folder3_sources = len(folder3_sources)
                    self.folder3_sources_4K = len([i for i in folder3_sources if i['quality'] == '4K'])
                    self.folder3_sources_1080p = len([i for i in folder3_sources if i['quality'] == '1080p'])
                    self.folder3_sources_720p = len([i for i in folder3_sources if i['quality'] == '720p'])
                    self.folder3_sources_SD = len([i for i in folder3_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
            if not self.folder4_sources:
                try: folder4_sources = json.loads(window.getProperty('folder4_source_results'))
                except: folder4_sources = []
                if folder4_sources:
                    self.folder4_sources = len(folder4_sources)
                    self.folder4_sources_4K = len([i for i in folder4_sources if i['quality'] == '4K'])
                    self.folder4_sources_1080p = len([i for i in folder4_sources if i['quality'] == '1080p'])
                    self.folder4_sources_720p = len([i for i in folder4_sources if i['quality'] == '720p'])
                    self.folder4_sources_SD = len([i for i in folder4_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
            if not self.folder5_sources:
                try: folder5_sources = json.loads(window.getProperty('folder5_source_results'))
                except: folder5_sources = []
                if folder5_sources:
                    self.folder5_sources = len(folder5_sources)
                    self.folder5_sources_4K = len([i for i in folder5_sources if i['quality'] == '4K'])
                    self.folder5_sources_1080p = len([i for i in folder5_sources if i['quality'] == '1080p'])
                    self.folder5_sources_720p = len([i for i in folder5_sources if i['quality'] == '720p'])
                    self.folder5_sources_SD = len([i for i in folder5_sources if i['quality'] in ['SD', 'SCR', 'CAM', 'TELE']])
        self.internalSources4K = self.furk_sources_4K + self.easynews_sources_4K + self.pm_cloud_sources_4K + self.rd_cloud_sources_4K + self.ad_cloud_sources_4K + self.local_sources_4K + self.downloads_sources_4K + self.folder1_sources_4K + self.folder2_sources_4K + self.folder3_sources_4K + self.folder5_sources_4K + self.folder5_sources_4K
        self.internalSources1080p = self.furk_sources_1080p + self.easynews_sources_1080p + self.pm_cloud_sources_1080p + self.rd_cloud_sources_1080p + self.ad_cloud_sources_1080p + self.local_sources_1080p + self.downloads_sources_1080p + self.folder1_sources_1080p + self.folder2_sources_1080p + self.folder3_sources_1080p + self.folder4_sources_1080p + self.folder5_sources_1080p
        self.internalSources720p = self.furk_sources_720p + self.easynews_sources_720p + self.pm_cloud_sources_720p + self.rd_cloud_sources_720p + self.ad_cloud_sources_720p + self.local_sources_720p + self.downloads_sources_720p + self.folder1_sources_720p + self.folder2_sources_720p + self.folder3_sources_720p + self.folder4_sources_720p + self.folder5_sources_720p
        self.internalSourcesSD = self.furk_sources_SD + self.easynews_sources_SD + self.pm_cloud_sources_SD + self.rd_cloud_sources_SD + self.ad_cloud_sources_SD + self.local_sources_SD + self.downloads_sources_SD + self.folder1_sources_SD + self.folder2_sources_SD + self.folder3_sources_SD + self.folder4_sources_SD + self.folder5_sources_SD
        self.internalSourcesTotal = self.internalSources4K + self.internalSources1080p + self.internalSources720p + self.internalSourcesSD

    def getConstants(self):
        self.meta = json.loads(window.getProperty('fen_media_meta'))
        self.background = self.meta.get('background', False)
        self.dialog_background = True if (__fen__.getSetting('auto_play'), __fen__.getSetting('autoplay_minimal_notifications')) == ('true', 'true') else False
        self.suppress_notifications = True if self.background == True or self.dialog_background == True else False
        if not self.suppress_notifications: show_busy_dialog()
        external_source_utils.checkDatabase()
        self.debrid_enabled = debrid.debrid_enabled()
        sourceDict = sources()
        self.sourceDict = [i for i in sourceDict if not i[0] in ('furk', 'easynews', 'library')]
        if self.debrid_enabled == []:
            en_DebridOnly = external_source_utils.scraperNames('en_DebridOnly')
            en_Torrent = external_source_utils.scraperNames('en_Torrent')
            total_debrid = en_DebridOnly + en_Torrent
            self.sourceDict = [i for i in self.sourceDict if not i[0] in total_debrid]
        self.providerDatabase = os.path.join(xbmc.translatePath(__fen__.getAddonInfo('profile')), "ext_providers3.db")
        self.moduleProvider = __external__.getSetting('module.provider')
        try:
            self.hostDict = resolveurl.relevant_resolvers(order_matters=True)
            self.hostDict = [i.domains for i in self.hostDict if '*' not in i.domains]
            self.hostDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostDict)]
            self.hostDict = [x for y, x in enumerate(self.hostDict) if x not in self.hostDict[:y]]
        except Exception:
            self.hostDict = []
        self.hostprDict = ['1fichier.com', 'oboom.com', 'rapidgator.net', 'rg.to', 'uploaded.net', 'uploaded.to', 'uploadgig.com', 'ul.to',
                           'filefactory.com', 'nitroflare.com', 'turbobit.net', 'uploadrocket.net', 'multiup.org']
        self.hostcapDict = ['hugefiles.net', 'hugefiles.cc', 'vidup.me', 'vidup.tv', 'flashx.tv', 'flashx.to', 'flashx.sx', 'flashx.bz', 'flashx.cc', 'vshare.eu', 'vshare.io',
        					'thevideo.me', 'vev.io', 'uptobox.com', 'uptostream.com', 'jetload.net', 'jetload.tv', 'jetload.to']
        self.hosthqDict = ['gvideo', 'google.com', 'thevideo.me', 'raptu.com', 'filez.tv', 'uptobox.com', 'uptostream.com', 'xvidstage.com', 'xstreamcdn.com', 'idtbox.com']
        self.hostblockDict = ['waaw.tv', 'hqq.watch', 'netu.tv', 'hqq.tv', 'waaw1.tv', 'netu.tv', 'movdivx.com', 'divxme.com', 'streamflv.com', 'speedvid.net',
                              'powvideo.net', 'powvideo.cc', 'estream.to', 'estream.nu', 'estream.xyz', 'openload.io', 'openload.co', 'oload.tv', 'oload.stream',
                              'oload.win', 'oload.download', 'oload.info', 'oload.icu', 'oload.fun', 'oload.space', 'oload.life', 'openload.pw', 'streamango.com',
                              'streamcherry.com', 'fruitstreams.com', 'fruitadblock.net', 'fruithosted.net', 'fruithosts.net', 'streamin.to', 'torba.se', 'rapidvideo.com',
                              'rapidvideo.is', 'rapidvid.to''zippyshare.com', 'youtube.com', 'facebook.com', 'twitch.tv', ]
        self.furk_enabled = __fen__.getSetting('provider.furk')
        self.easynews_enabled = __fen__.getSetting('provider.easynews')
        self.pm_cloud_enabled = __fen__.getSetting('provider.pm-cloud')
        self.rd_cloud_enabled = __fen__.getSetting('provider.rd-cloud')
        self.ad_cloud_enabled = __fen__.getSetting('provider.ad-cloud')
        self.local_enabled = __fen__.getSetting('provider.local')
        self.downloads_enabled = __fen__.getSetting('provider.downloads')
        self.folders_enabled = __fen__.getSetting('provider.folders')
        self.progressHeading = int(__fen__.getSetting('progress.heading'))
        self.remove_failing_sources = __fen__.getSetting('remove.failing_scrapers')
        self.internal_activated = True if 'true' in (self.furk_enabled, self.easynews_enabled, self.pm_cloud_enabled, self.rd_cloud_enabled, self.ad_cloud_enabled, self.folders_enabled) \
                                else False
        self.furk_sources, self.furk_sources_4K, self.furk_sources_1080p, self.furk_sources_720p, self.furk_sources_SD = (0 for _ in range(5))
        self.easynews_sources, self.easynews_sources_4K, self.easynews_sources_1080p, self.easynews_sources_720p, self.easynews_sources_SD = (0 for _ in range(5))
        self.pm_cloud_sources, self.pm_cloud_sources_4K, self.pm_cloud_sources_1080p, self.pm_cloud_sources_720p, self.pm_cloud_sources_SD = (0 for _ in range(5))
        self.rd_cloud_sources, self.rd_cloud_sources_4K, self.rd_cloud_sources_1080p, self.rd_cloud_sources_720p, self.rd_cloud_sources_SD = (0 for _ in range(5))
        self.ad_cloud_sources, self.ad_cloud_sources_4K, self.ad_cloud_sources_1080p, self.ad_cloud_sources_720p, self.ad_cloud_sources_SD = (0 for _ in range(5))
        self.local_sources, self.local_sources_4K, self.local_sources_1080p, self.local_sources_720p, self.local_sources_SD = (0 for _ in range(5))
        self.downloads_sources, self.downloads_sources_4K, self.downloads_sources_1080p, self.downloads_sources_720p, self.downloads_sources_SD = (0 for _ in range(5))
        self.folder1_sources, self.folder1_sources_4K, self.folder1_sources_1080p, self.folder1_sources_720p, self.folder1_sources_SD = (0 for _ in range(5))
        self.folder2_sources, self.folder2_sources_4K, self.folder2_sources_1080p, self.folder2_sources_720p, self.folder2_sources_SD = (0 for _ in range(5))
        self.folder3_sources, self.folder3_sources_4K, self.folder3_sources_1080p, self.folder3_sources_720p, self.folder3_sources_SD = (0 for _ in range(5))
        self.folder4_sources, self.folder4_sources_4K, self.folder4_sources_1080p, self.folder4_sources_720p, self.folder4_sources_SD = (0 for _ in range(5))
        self.folder5_sources, self.folder5_sources_4K, self.folder5_sources_1080p, self.folder5_sources_720p, self.folder5_sources_SD = (0 for _ in range(5))
        self.internalSourcesTotal, self.internalSources4K, self.internalSources1080p, self.internalSources720p, self.internalSourcesSD = (0 for _ in range(5))
        hide_busy_dialog()

    def exportSettings(self):
        try:
            __external__.setSetting('torrent.enabled', 'true')
            __external__.setSetting('torrent.min.seeders', __fen__.getSetting('torrent.min.seeders'))
        except: pass





