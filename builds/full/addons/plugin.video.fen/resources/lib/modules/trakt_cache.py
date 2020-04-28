#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmcvfs, xbmcgui, xbmc, xbmcaddon
import datetime
import time
import sqlite3
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database
from functools import reduce
from modules.utils import to_utf8
from modules import settings
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
try: trakt_cache_file = xbmc.translatePath("%s/fen_trakt.db" % profile_dir).decode('utf-8')
except: trakt_cache_file = xbmc.translatePath("%s/fen_trakt.db" % profile_dir)

window = xbmcgui.Window(10000)


class TraktCache(object):
    _exit = False
    _auto_clean_interval = datetime.timedelta(hours=4)
    _win = None
    _busy_tasks = []
    _database = None

    def __init__(self):
        self._monitor = xbmc.Monitor()
        self.check_cleanup()

    def close(self):
        self._exit = True
        while self._busy_tasks:
            xbmc.sleep(25)
        del self._monitor
        self._log_msg("Closed")

    def __del__(self):
        if not self._exit:
            self.close()

    def get(self, endpoint):
        cur_time = self._get_timestamp(datetime.datetime.now())
        result = None
        result = self._get_mem_cache(endpoint, cur_time)
        if result is None:
            result = self._get_db_cache(endpoint, cur_time)

        return result

    def set(self, endpoint, data, expiration=datetime.timedelta(days=30)):
        task_name = "set.%s" % endpoint
        self._busy_tasks.append(task_name)
        expires = self._get_timestamp(datetime.datetime.now() + expiration)
        self._set_mem_cache(endpoint, expires, data)
        if not self._exit:
            self._set_db_cache(endpoint, expires, data)
        self._busy_tasks.remove(task_name)

    def check_cleanup(self):
        cur_time = datetime.datetime.now()
        lastexecuted = window.getProperty("fen_trakt.clean.lastexecuted")
        if not lastexecuted:
            window.setProperty("fen_trakt.clean.lastexecuted", repr(cur_time))
        elif (eval(lastexecuted) + self._auto_clean_interval) < cur_time:
            # cleanup needed...
            self._do_cleanup()

    def _get_mem_cache(self, endpoint, cur_time):
        result = None
        try: cachedata = window.getProperty(endpoint.encode("utf-8"))
        except: cachedata = window.getProperty(endpoint)
        if cachedata:
            cachedata = eval(cachedata)
            if cachedata[0] > cur_time:
                result = cachedata[1]
        return result

    def _set_mem_cache(self, endpoint, expires, data):
        cachedata = (expires, data)
        try:
            cachedata_str = repr(cachedata).encode("utf-8")
            window.setProperty(endpoint.encode("utf-8"), cachedata_str)
        except:
            cachedata_str = repr(cachedata)
            window.setProperty(endpoint, cachedata_str)

    def _get_db_cache(self, endpoint, cur_time):
        result = None
        query = "SELECT expires, data FROM fen_trakt WHERE id = ?"
        cache_data = self._execute_sql(query, (endpoint,))
        if cache_data:
            cache_data = cache_data.fetchone()
            if cache_data and cache_data[0] > cur_time:
                result = eval(cache_data[1])
                self._set_mem_cache(endpoint, cache_data[0], result)
        return result

    def _set_db_cache(self, endpoint, expires, data):
        query = "INSERT OR REPLACE INTO fen_trakt(id, expires, data) VALUES (?, ?, ?)"
        data = repr(data)
        self._execute_sql(query, (endpoint, expires, data))

    def _do_cleanup(self):
        if self._exit or self._monitor.abortRequested():
            return
        self._busy_tasks.append(__name__)
        cur_time = datetime.datetime.now()
        cur_timestamp = self._get_timestamp(cur_time)
        self._log_msg("Running cleanup...")
        if window.getProperty("fentraktcachecleanbusy"):
            return
        window.setProperty("fentraktcachecleanbusy", "busy")

        query = "SELECT id, expires FROM fen_trakt"
        for cache_data in self._execute_sql(query).fetchall():
            if self._exit or self._monitor.abortRequested():
                return
            try: window.clearProperty(cache_data[0].encode("utf-8"))
            except: window.clearProperty(cache_data[0])
            if cache_data[1] < cur_timestamp:
                query = 'DELETE FROM fen_trakt WHERE id = ?'
                self._execute_sql(query, (cache_data[0],))
                self._log_msg("delete from db %s" % cache_data[0])
        self._execute_sql("VACUUM")
        self._busy_tasks.remove(__name__)
        window.setProperty("fen_trakt.clean.lastexecuted", repr(cur_time))
        window.clearProperty("fentraktcachecleanbusy")
        self._log_msg("Auto cleanup done")

    def _get_database(self):
        if not xbmcvfs.exists(profile_dir):
            xbmcvfs.mkdirs(profile_dir)
        try:
            connection = sqlite3.connect(trakt_cache_file, timeout=30, isolation_level=None)
            connection.execute('SELECT * FROM fen_trakt LIMIT 1')
            return connection
        except Exception as error:
            if xbmcvfs.exists(trakt_cache_file):
                xbmcvfs.delete(trakt_cache_file)
            try:
                connection = sqlite3.connect(trakt_cache_file, timeout=30, isolation_level=None)
                connection.execute(
                    """CREATE TABLE IF NOT EXISTS fen_trakt(
                    id TEXT UNIQUE, expires INTEGER, data TEXT)""")
                return connection
            except Exception as error:
                self._log_msg("Exception while initializing _database: %s" % str(error), xbmc.LOGWARNING)
                self.close()
                return None

    def _execute_sql(self, query, data=None):
        retries = 0
        result = None
        error = None
        with self._get_database() as _database:
            while not retries == 10:
                if self._exit:
                    return None
                try:
                    if isinstance(data, list):
                        result = _database.executemany(query, data)
                    elif data:
                        result = _database.execute(query, data)
                    else:
                        result = _database.execute(query)
                    return result
                except sqlite3.OperationalError as error:
                    if "_database is locked" in error:
                        self._log_msg("retrying DB commit...")
                        retries += 1
                        self._monitor.waitForAbort(0.5)
                    else:
                        break
                except Exception as error:
                    break
            self._log_msg("_database ERROR ! -- %s" % str(error), xbmc.LOGWARNING)
        return None

    @staticmethod
    def _log_msg(msg, loglevel=xbmc.LOGDEBUG):
        try:
            if isinstance(msg, unicode):
                msg = msg.encode('utf-8')
        except: pass
        xbmc.log("Fen Trakt Cache --> %s" % msg, level=loglevel)

    @staticmethod
    def _get_timestamp(date_time):
        return int(time.mktime(date_time.timetuple()))

def cache_trakt_object(function, string, url, expiration=None):
    expires = expiration if expiration else settings.trakt_cache_duration()
    _cache = TraktCache()
    cache = _cache.get(string)
    if cache: return to_utf8(cache)
    result = function(url)
    _cache.set(string, result, expiration=datetime.timedelta(hours=expires))
    return to_utf8(result)

def clear_trakt_watched_data(db_type):
    settings.check_database(trakt_cache_file)
    dbcon = database.connect(trakt_cache_file)
    dbcur = dbcon.cursor()
    if db_type == 'tvshow':
        dbcur.execute("DELETE FROM fen_trakt WHERE id=?", ('trakt_tv_watched_raw',))
        window.clearProperty('trakt_tv_watched_raw')
    action = 'trakt_indicators_movies' if db_type in ('movie', 'movies') else 'trakt_indicators_tv'
    dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
    dbcon.commit()
    window.clearProperty(action)

def clear_trakt_hidden_data(list_type):
    settings.check_database(trakt_cache_file)
    action = 'trakt_hidden_items_%s' % list_type
    try:
        dbcon = database.connect(trakt_cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
        dbcon.commit()
        dbcon.close()
        window.clearProperty(action)
    except: pass

def clear_trakt_collection_watchlist_data(list_type, db_type):
    settings.check_database(trakt_cache_file)
    if db_type == 'movies': db_type = 'movie' 
    if db_type in ('tvshows', 'shows'): db_type = 'tvshow' 
    action = 'trakt_%s_%s' % (list_type, db_type)
    try:
        dbcon = database.connect(trakt_cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
        dbcon.commit()
        dbcon.close()
        window.clearProperty(action)
        window.clearProperty('fen_trakt_%s_%s' % (list_type, db_type))
    except: pass

def clear_trakt_list_contents_data(clear_all=False, user=None, list_slug=None):
    from modules.nav_utils import clear_all_window_properties
    clear_all_window_properties()
    settings.check_database(trakt_cache_file)
    if clear_all:
        try:
            dbcon = database.connect(trakt_cache_file)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM fen_trakt WHERE id LIKE 'trakt_list_contents%'")
            dbcon.commit()
            dbcon.close()
        except: pass
    else:
        action = 'trakt_list_contents_%s_%s' % (user, list_slug)
        try:
            dbcon = database.connect(trakt_cache_file)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
            dbcon.commit()
            dbcon.close()
        except: pass

def clear_trakt_list_data(list_type):
    settings.check_database(trakt_cache_file)
    action = 'trakt_my_lists' if list_type == 'my_lists' else 'trakt_liked_lists'
    try:
        dbcon = database.connect(trakt_cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
        dbcon.commit()
        dbcon.close()
        window.clearProperty(action)
    except: pass

def clear_trakt_calendar():
    from modules.nav_utils import clear_all_window_properties
    clear_all_window_properties()
    settings.check_database(trakt_cache_file)
    try:
        dbcon = database.connect(trakt_cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fen_trakt WHERE id LIKE 'get_trakt_my_calendar%'")
        dbcon.commit()
        dbcon.close()
    except: return

def clear_all_trakt_cache_data(list_type='progress_watched', confirm=True, silent=False):
    from modules.nav_utils import notification
    def _process():
        window.setProperty('fen_refresh_trakt_info_complete', 'true')
        try:
            dbcon = database.connect(trakt_cache_file)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM fen_trakt")
            dbcon.commit()
            dbcon.execute("VACUUM")
            dbcon.close()
            return True
        except:
            return False
    if silent:
        return _process()
    if settings.refresh_trakt_on_startup() and not confirm:
        if window.getProperty('fen_refresh_trakt_info_complete') == 'true': return
        success = _process()
        if success:
            return
        else:
            return notification('Error Refreshing Trakt Cache')
    if confirm:
        if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear the Trakt Cache.'):
            return False
        result = _process()
        return result