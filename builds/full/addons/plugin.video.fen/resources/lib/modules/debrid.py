import xbmc, xbmcgui, xbmcvfs
import os
import time
import datetime
import sqlite3 as database
from apis.real_debrid_api import RealDebridAPI
from apis.premiumize_api import PremiumizeAPI
from apis.alldebrid_api import AllDebridAPI
from modules.utils import chunks
from threading import Thread
# from modules.utils import logger

progressDialog = xbmcgui.DialogProgress()

rd_api = RealDebridAPI()
pm_api = PremiumizeAPI()
ad_api = AllDebridAPI()

def debrid_enabled():
    debrid_enabled = []
    if rd_api.rd_enabled(): debrid_enabled.append('Real-Debrid')
    if pm_api.pm_enabled(): debrid_enabled.append('Premiumize.me')
    if ad_api.ad_enabled(): debrid_enabled.append('AllDebrid')
    return debrid_enabled

def debrid_valid_hosts(enabled_debrids):
    def _get_hosts(function):
        debrid_hosts.append(function.get_hosts())
    functions = []
    debrid_hosts = []
    threads = []
    for i in enabled_debrids:
        if i == 'Real-Debrid': functions.append(rd_api)
        elif i == 'Premiumize.me': functions.append(pm_api)
        else: functions.append(ad_api) # AllDebrid
    for i in functions: threads.append(Thread(target=_get_hosts, args=(i,)))
    [i.start() for i in threads]
    [i.join() for i in threads]
    return debrid_hosts


class DebridCheck:
    def __init__(self):
        self.db_cache = DebridCache()
        self.db_cache.check_database()
        self.cached_hashes = []
        self.main_threads = []
        self.rd_cached_hashes = []
        self.rd_hashes_unchecked = []
        self.rd_query_threads = []
        self.rd_process_results = []
        self.pm_cached_hashes = []
        self.pm_hashes_unchecked = []
        self.pm_process_results = []
        self.ad_cached_hashes = []
        self.ad_hashes_unchecked = []
        self.ad_query_threads = []
        self.ad_process_results = []
        self.starting_debrids = []
        self.starting_debrids_display = []

    def run(self, hash_list, background, debrid_enabled):
        xbmc.sleep(100)
        self.hash_list = hash_list
        self._query_local_cache(self.hash_list)
        if 'AllDebrid' in debrid_enabled:
            self.ad_cached_hashes = [str(i[0]) for i in self.cached_hashes if str(i[1]) == 'ad' and str(i[2]) == 'True']
            self.ad_hashes_unchecked = [i for i in self.hash_list if not any([h for h in self.cached_hashes if str(h[0]) == i and str(h[1]) =='ad'])]
            if self.ad_hashes_unchecked: self.starting_debrids.append(('AllDebrid', self.AD_cache_checker))
        if 'Premiumize.me' in debrid_enabled:
            self.pm_cached_hashes = [str(i[0]) for i in self.cached_hashes if str(i[1]) == 'pm' and str(i[2]) == 'True']
            self.pm_hashes_unchecked = [i for i in self.hash_list if not any([h for h in self.cached_hashes if str(h[0]) == i and str(h[1]) =='pm'])]
            if self.pm_hashes_unchecked: self.starting_debrids.append(('Premiumize.me', self.PM_cache_checker))
        if 'Real-Debrid' in debrid_enabled:
            self.rd_cached_hashes = [str(i[0]) for i in self.cached_hashes if str(i[1]) == 'rd' and str(i[2]) == 'True']
            self.rd_hashes_unchecked = [i for i in self.hash_list if not any([h for h in self.cached_hashes if str(h[0]) == i and str(h[1]) =='rd'])]
            if self.rd_hashes_unchecked: self.starting_debrids.append(('Real-Debrid', self.RD_cache_checker))
        if self.starting_debrids:
            for i in range(len(self.starting_debrids)):
                self.main_threads.append(Thread(target=self.starting_debrids[i][1]))
                self.starting_debrids_display.append((self.main_threads[i].getName(), self.starting_debrids[i][0]))
            [i.start() for i in self.main_threads]
            if background: [i.join() for i in self.main_threads]
            else: self.debrid_check_dialog()
        xbmc.sleep(100)
        return self.rd_cached_hashes, self.pm_cached_hashes, self.ad_cached_hashes

    def debrid_check_dialog(self):
        timeout = 25
        progressDialog.create('Fen Debrid', 'Please Wait..', '..', '..')
        progressDialog.update(0, 'Checking Debrid Services for Torrent Cache.', '..', '..')
        start_time = time.time()
        end_time = start_time + timeout
        for i in range(0, timeout*5):
            try:
                if xbmc.abortRequested == True: return sys.exit()
                try:
                    if progressDialog.iscanceled():
                        break
                except Exception:
                    pass
                alive_threads = [x.getName() for x in self.main_threads if x.is_alive() is True]
                remaining_debrids = [x[1] for x in self.starting_debrids_display if x[0] in alive_threads]
                current_time = time.time()
                current_progress = current_time - start_time
                try:
                    line2 = 'Checking Debrid Providers'
                    line3 = 'Remaining Debrid Checks: %s' % ', '.join(remaining_debrids).upper()
                    percent = int((current_progress/float(timeout))*100)
                    progressDialog.update(percent, '', line2, line3)
                except: pass
                time.sleep(0.2)
                if len(alive_threads) == 0: break
                if current_time > end_time: break
            except Exception:
                pass
        try:
            progressDialog.close()
        except Exception:
            pass
        xbmc.sleep(200)

    def RD_cache_checker(self):
        hash_chunk_list = list(chunks(self.rd_hashes_unchecked, 100))
        for item in hash_chunk_list: self.rd_query_threads.append(Thread(target=self._rd_lookup, args=(item,)))
        [i.start() for i in self.rd_query_threads]
        [i.join() for i in self.rd_query_threads]
        self._add_to_local_cache(self.rd_process_results, 'rd')

    def PM_cache_checker(self):
        self._pm_lookup(self.pm_hashes_unchecked)
        self._add_to_local_cache(self.pm_process_results, 'pm')

    def AD_cache_checker(self):
        self._ad_lookup(self.ad_hashes_unchecked)
        self._add_to_local_cache(self.ad_process_results, 'ad')

    def _rd_lookup(self, chunk):
        try:
            try: rd_cache = rd_api.check_cache(chunk)
            except: rd_cache = None
            if isinstance(rd_cache, dict):
                for h in chunk:
                    cached = 'False'
                    if h in rd_cache:
                        info = rd_cache[h]
                        if isinstance(info, dict) and len(info.get('rd')) > 0:
                            self.rd_cached_hashes.append(h)
                            cached = 'True'
                    self.rd_process_results.append((h, cached))
            else:
                for i in hash_list: self.rd_process_results.append((i, 'False'))
        except: pass

    def _pm_lookup(self, hash_list):
        try:
            try: pm_cache = pm_api.check_cache(hash_list)['response']
            except: pm_cache = None
            if isinstance(pm_cache, list):
                for c, h in enumerate(hash_list):
                    cached = 'False'
                    if pm_cache[c] is True:
                        self.pm_cached_hashes.append(h)
                        cached = 'True'
                    self.pm_process_results.append((h, cached))
            else:
                for i in hash_list: self.pm_process_results.append((i, 'False'))
        except: pass

    def _ad_lookup(self, hash_list):
        try:
            ad_cache = ad_api.check_cache(hash_list)['magnets']
            if isinstance(ad_cache, list):
                for i in ad_cache:
                    try:
                        cached = 'False'
                        if i['instant'] == True:
                            self.ad_cached_hashes.append(i['hash'])
                            cached = 'True'
                        self.ad_process_results.append((i['hash'], cached))
                    except: pass
            else:
                for i in hash_list: self.ad_process_results.append((i, 'False'))
        except: pass

    def _query_local_cache(self, _hash):
        cached = self.db_cache.get_many(_hash)
        if cached:
            self.cached_hashes = cached

    def _add_to_local_cache(self, _hash, debrid):
        self.db_cache.set_many(_hash, debrid)

class DebridCache:
    def __init__(self):
        self.datapath = xbmc.translatePath("special://profile/addon_data/plugin.video.fen")
        self.dbfile = os.path.join(self.datapath, "debridcache.db")

    def get_many(self, hash_list):
        result = None
        try:
            current_time = self._get_timestamp(datetime.datetime.now())
            dbcon = database.connect(self.dbfile, timeout=40.0)
            dbcur = dbcon.cursor()
            dbcur.execute('SELECT * FROM debrid_data WHERE hash in ({0})'.format(', '.join('?' for _ in hash_list)), hash_list)
            cache_data = dbcur.fetchall()
            if cache_data:
                if cache_data[0][3] > current_time:
                    result = cache_data
                else:
                    self.remove_many(cache_data)
        except: pass
        return result

    def remove_many(self, old_cached_data):
        try:
            old_cached_data = [(str(i[0]),) for i in old_cached_data]
            dbcon = database.connect(self.dbfile, timeout=40.0)
            dbcur = dbcon.cursor()
            dbcur.executemany("DELETE FROM debrid_data WHERE hash=?", old_cached_data)
            dbcon.commit()
        except: pass

    def set_many(self, hash_list, debrid, expiration=datetime.timedelta(hours=2)):
        try:
            expires = self._get_timestamp(datetime.datetime.now() + expiration)
            insert_list = [(i[0], debrid, i[1], expires) for i in hash_list]
            dbcon = database.connect(self.dbfile, timeout=40.0)
            dbcur = dbcon.cursor()
            dbcur.executemany("INSERT INTO debrid_data VALUES (?, ?, ?, ?)", insert_list)
            dbcon.commit()
        except: pass

    def check_database(self):
        if not xbmcvfs.exists(self.datapath):
            xbmcvfs.mkdirs(self.datapath)
        dbcon = database.connect(self.dbfile)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS debrid_data
                      (hash text not null, debrid text not null, cached text, expires integer, unique (hash, debrid))
                        """)
        dbcon.close()

    def clear_database(self):
        try:
            dbcon = database.connect(self.dbfile)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM debrid_data")
            dbcur.execute("VACUUM")
            dbcon.commit()
            dbcon.close()
            return 'success'
        except: return 'failure'

    def _get_timestamp(self, date_time):
        return int(time.mktime(date_time.timetuple()))






