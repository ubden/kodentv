#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui
import os
import datetime
import time
try: import sqlite3 as database
except ImportError: import pysqlite2 as database
# from tikimeta.utils import logger

window = xbmcgui.Window(10000)

class MetaCache():
    def __init__(self):
        self.datapath = xbmc.translatePath("special://userdata/addon_data/script.module.tikimeta")
        self.dbfile = os.path.join(self.datapath, "metacache4.db")
        self._auto_clean_interval = datetime.timedelta(hours=4)
        self.time = datetime.datetime.now()
        self.timeout = 240
        # self.check_database()
        # self.check_cleanup()

    def get(self, db_type, id_type, media_id):
        result = None
        try:
            current_time = self._get_timestamp(self.time)
            result = self.get_memory_cache(db_type, id_type, media_id, current_time)
            if result is None:
                dbcon = database.connect(self.dbfile, timeout=self.timeout)
                dbcur = self._set_PRAGMAS(dbcon)
                if db_type in ('movie', 'tvshow'):
                    dbcur.execute("SELECT meta, expires FROM metadata WHERE db_type = ? AND %s = ?" % id_type, (str(db_type), str(media_id)))
                else:
                    dbcur.execute("SELECT meta, expires FROM season_metadata WHERE tmdb_id = ?", (str(media_id),))
                cache_data = dbcur.fetchone()
                if cache_data:
                    if cache_data[1] > current_time:
                        result = eval(cache_data[0])
                        if db_type in ('movie', 'tvshow'): tmdb_id = result['tmdb_id']
                        else: tmdb_id = media_id
                        self.set_memory_cache(db_type, result, cache_data[1], tmdb_id)
                    else:
                        self.delete(db_type, id_type, media_id, dbcon)
        except Exception as e:
            from tikimeta.utils import logger
            logger('trouble with get', type(e))
        return result

    def set(self, db_type, meta, expiration=datetime.timedelta(days=30), tmdb_id=None):
        try:
            expires = self._get_timestamp(self.time + expiration)
            dbcon = database.connect(self.dbfile, timeout=self.timeout)
            dbcur = self._set_PRAGMAS(dbcon)
            if db_type in ('movie', 'tvshow'):
                dbcur.execute("INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?)", (str(db_type), str(meta['tmdb_id']), str(meta['imdb_id']), str(meta['tvdb_id']), repr(meta), int(expires)))
            else:
                dbcur.execute("INSERT INTO season_metadata VALUES (?, ?, ?)", (str(tmdb_id), repr(meta), int(expires)))
            dbcon.commit()
            self.set_memory_cache(db_type, meta, int(expires), tmdb_id)
        except Exception as e:
            from tikimeta.utils import logger
            logger('trouble with set', e)
            return None

    def get_memory_cache(self, db_type, id_type, media_id, current_time):
        result = None
        try:
            if db_type in ('movie', 'tvshow'):
                string = '%s_%s_%s' % (db_type, id_type, media_id)
            else:
                string = 'tikimeta_season_%s' % str(media_id)
            try: cachedata = window.getProperty(string.encode("utf-8"))
            except: cachedata = window.getProperty(string)
            if cachedata:
                cachedata = eval(cachedata)
                if cachedata[0] > current_time:
                    result = cachedata[1]
        except: pass
        return result

    def set_memory_cache(self, db_type, meta, expires, tmdb_id):
        if db_type in ('movie', 'tvshow'):
            string = '%s_%s_%s' % (str(db_type), 'tmdb_id', str(meta['tmdb_id']))
            cachedata = (expires, meta)
        else:
            string = 'tikimeta_season_%s' % str(tmdb_id)
            cachedata = (expires, meta)
        try: cachedata_repr = repr(cachedata).encode("utf-8")
        except: cachedata_repr = repr(cachedata)
        window.setProperty(string, cachedata_repr)

    def get_function(self, string):
        result = None
        try:
            current_time = self._get_timestamp(self.time)
            dbcon = database.connect(self.dbfile, timeout=self.timeout)
            dbcur = self._set_PRAGMAS(dbcon)
            dbcur.execute("SELECT string_id, data, expires FROM function_cache WHERE string_id = ?", (string,))
            cache_data = dbcur.fetchone()
            if cache_data:
                if cache_data[2] > current_time:
                    result = eval(cache_data[1])
                else:
                    dbcur.execute("DELETE FROM function_cache WHERE string_id = ?", (string,))
                    dbcon.commit()
        except: pass
        return result

    def set_function(self, string, result, expiration=datetime.timedelta(days=1)):
        try:
            expires = self._get_timestamp(self.time + expiration)
            dbcon = database.connect(self.dbfile, timeout=self.timeout)
            dbcur = self._set_PRAGMAS(dbcon)
            dbcur.execute("INSERT INTO function_cache VALUES (?, ?, ?)", (string, repr(result), int(expires)))
            dbcon.commit()
        except: return

    def delete(self, db_type, id_type, media_id, dbcon=None):
        try:
            if not dbcon: dbcon = database.connect(self.dbfile, timeout=self.timeout)
            dbcur = dbcon.cursor()
            if db_type in ('movie', 'tvshow'):
                dbcur.execute("DELETE FROM metadata WHERE db_type = ? AND %s = ?" % id_type, (str(db_type), str(media_id)))
                self.delete_memory_cache(db_type, id_type, media_id)
            if db_type in ('tvshow', 'season'):
                dbcur.execute("DELETE FROM season_metadata WHERE tmdb_id = ?", (str(media_id),))
                self.delete_memory_cache('season', id_type, media_id)
            dbcon.commit()
        except: return

    def delete_memory_cache(self, db_type, id_type, media_id):
        if db_type in ('movie', 'tvshow'): string = '%s_%s_%s' % (db_type, id_type, media_id)
        else: string = 'tikimeta_season_%s' % media_id
        window.clearProperty(string)

    def delete_function_cache(self, item):
        window.clearProperty(item)

    def delete_all(self):
        try:
            dbcon = database.connect(self.dbfile, timeout=self.timeout)
            dbcur = dbcon.cursor()
            for i in ('metadata', 'season_metadata', 'function_cache'): dbcur.execute("DELETE FROM %s" % i)
            dbcon.commit()
            dbcon.execute("VACUUM")
            dbcon.close()
        except: return

    def _set_PRAGMAS(self, dbcon):
        dbcur = dbcon.cursor()
        dbcur.execute('''PRAGMA synchronous = OFF''')
        dbcur.execute('''PRAGMA journal_mode = OFF''')
        return dbcur

    def check_database(self):
        import xbmcvfs
        if not xbmcvfs.exists(self.datapath):
            xbmcvfs.mkdirs(self.datapath)
        if not xbmcvfs.exists(self.dbfile):
            dbcon = database.connect(self.dbfile)
            self._check_metadata_cache_table(dbcon)
            self._check_season_metadata_cache_table(dbcon)
            self._check_function_cache_table(dbcon)

    def check_cleanup(self):
        while window.getProperty("tikimetacachecleanbusy") == 'busy':
            xbmc.sleep(25)
        cur_time = self.time
        lastexecuted = window.getProperty("tikimeta.clean.lastexecuted")
        if not lastexecuted:
            self._do_cleanup()
        elif (eval(lastexecuted) + self._auto_clean_interval) < cur_time:
            self._do_cleanup()

    def _do_cleanup(self):
        cur_time = self.time
        cur_timestamp = self._get_timestamp(cur_time)
        xbmc.log('[TIKIMETA]: Running Database Clean...', 2)
        if window.getProperty("tikimetacachecleanbusy"):
            return
        window.setProperty("tikimetacachecleanbusy", "busy")
        dbcon = database.connect(self.dbfile)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT db_type, tmdb_id, expires FROM metadata")
        cache_data = dbcur.fetchall()
        for data in cache_data:
            if data[2] < cur_timestamp:
                self.delete(data[0], 'tmdb_id', data[1], dbcon)
        dbcon.execute("VACUUM")
        dbcon.close()
        window.setProperty("tikimeta.clean.lastexecuted", repr(cur_time))
        window.clearProperty("tikimetacachecleanbusy")
        xbmc.log('[TIKIMETA]: Database Clean Finished', 2)

    def _check_metadata_cache_table(self, dbcon=None):
        if not dbcon: dbcon = database.connect(self.dbfile)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS metadata
                          (db_type text not null, tmdb_id text not null, imdb_id text, tvdb_id text,
                          meta text, expires integer, unique (db_type, tmdb_id))
                       """)

    def _check_season_metadata_cache_table(self, dbcon=None):
        if not dbcon: dbcon = database.connect(self.dbfile)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS season_metadata
                          (tmdb_id text not null, meta text,
                          expires integer, unique (tmdb_id))
                       """)

    def _check_function_cache_table(self, dbcon=None):
        if not dbcon: dbcon = database.connect(self.dbfile)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS function_cache
                         (string_id text not null, data text,
                         expires integer, unique (string_id))
                      """)

    def _get_timestamp(self, date_time):
        return int(time.mktime(date_time.timetuple()))

def cache_function(function, string, url, expiration=96, json=True):
    from tikimeta.utils import to_utf8
    from datetime import timedelta
    metacache = MetaCache()
    data = metacache.get_function(string)
    if data: return to_utf8(data)
    if json: result = function(url).json()
    else: result = function(url)
    metacache.set_function(string, result, expiration=timedelta(hours=expiration))
    return to_utf8(result)
