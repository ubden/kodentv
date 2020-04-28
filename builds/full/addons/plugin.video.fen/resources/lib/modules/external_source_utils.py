# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcvfs, xbmcgui
import os
import re
import pkgutil
try:
    from HTMLParser import HTMLParser # Python 2
except ImportError:
    from html.parser import HTMLParser # Python 3
try:
    from sqlite3 import dbapi2 as database
except Exception:
    from pysqlite2 import dbapi2 as database
from modules.utils import to_utf8
from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
__external__ = xbmcaddon.Addon(id='script.module.openscrapers')
data_path = xbmc.translatePath(__addon__.getAddonInfo('profile'))
database_path = os.path.join(data_path, "ext_providers3.db")
scraper_module_base_folder = os.path.join(xbmc.translatePath(__external__.getAddonInfo('path')), 'lib', 'openscrapers')

def normalize(title):
    try:
        try: return title.decode('ascii').encode("utf-8")
        except: pass
        
        try: import unicodedata
        except ImportError: return
        title = u'%s' % obj
        title = ''.join(c for c in unicodedata.normalize('NFD', title) if unicodedata.category(c) != 'Mn')

        return str(title)
    except:
        return title

def deleteProviderCache(silent=False):
    try:
        if not xbmcvfs.exists(database_path): return 'failure'
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear all External Scraper Results.'): return 'cancelled'
        dbcon = database.connect(database_path)
        dbcur = dbcon.cursor()
        for i in ('rel_url', 'rel_src'): dbcur.execute("DELETE FROM %s" % i)
        dbcon.commit()
        dbcur.execute("VACUUM")
        dbcon.close()
        return 'success'
    except: return 'failure'

def checkDatabase():
    if not xbmcvfs.exists(data_path): xbmcvfs.mkdirs(data_path)
    dbcon = database.connect(database_path)
    dbcon.execute("""CREATE TABLE IF NOT EXISTS rel_url
                      (source text, imdb_id text, season text, episode text,
                      rel_url text, unique (source, imdb_id, season, episode)) 
                   """)
    dbcon.execute("""CREATE TABLE IF NOT EXISTS rel_src
                      (source text, imdb_id text, season text, episode text,
                      hosts text, added text, unique (source, imdb_id, season, episode)) 
                   """)
    dbcon.execute("""CREATE TABLE IF NOT EXISTS scr_perf
                      (source text, success integer, failure integer, unique (source)) 
                   """)
    dbcon.close()

def external_scrapers_fail_stats():
    checkDatabase()
    dbcon = database.connect(database_path)
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM scr_perf")
    results = dbcur.fetchall()
    results = sorted([(str(i[0]), i[1], i[2]) for i in results], key=lambda k: k[2] - k[1], reverse=True)
    return results

def external_scrapers_disable():
    from modules.utils import multiselect_dialog
    dialog = xbmcgui.Dialog()
    scrapers = external_scrapers_fail_stats()
    try: scrapers = [i for i in scrapers if __external__.getSetting('provider.%s' % i[0]) == 'true']
    except: scrapers = []
    if not scrapers: return dialog.ok('FEN', 'No Scraper Stats Available.', 'There may be no stats available at the moment.', 'Also, make sure you have some External Scrapers enabled.')
    scrapers_dialog = ['[B]%s[/B] | TOTAL: %s | [COLOR=green]SUCCESS: %d[/COLOR] | [COLOR=red]FAIL: %d[/COLOR]' % ( i[0].upper(), (i[1] + i[2]),i[1], i[2]) for i in scrapers]
    scraper_choice = multiselect_dialog('Choose Scrapers To Disable', scrapers_dialog, scrapers)
    if not scraper_choice: return
    if dialog.yesno('FEN', 'Do you wish to reset the Success/Fail results of these disabled scrapers?'): clear_database = True
    else: clear_database = False
    checkDatabase()
    dbcon = database.connect(database_path)
    dbcur = dbcon.cursor()
    for i in scraper_choice:
        if clear_database: dbcur.execute("DELETE FROM scr_perf WHERE source = ?", (i[0],))
        __external__.setSetting('provider.%s' % i[0], 'false')
    if clear_database:
        dbcon.commit()
        line1 = 'Scrapers Disabled and Results Reset.'
    else:
        line1 = 'Scrapers Disabled.'
    return dialog.ok('FEN', line1)

def external_scrapers_reset_stats(silent=False):
    try:
        checkDatabase()
        if not silent:
            if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Reset all External Provider Stats.'): return
        dbcon = database.connect(database_path)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM scr_perf")
        dbcon.commit()
        dbcur.execute("VACUUM")
        dbcon.close()
        if silent: return
        return xbmcgui.Dialog().ok('FEN','External Provider Stats Reset.')
    except:
        if silent: return
        return xbmcgui.Dialog().ok('FEN','ERROR Resetting External Provider Stats.')

def _ext_scrapers_notice(status):
    from modules.nav_utils import notification
    notification('[B]External Scrapers Manager[/B] %s' % status, 2500)

def toggle_all(folder, setting, silent=False):
    try:
        sourcelist = scraperNames(folder)
        for i in sourcelist:
            source_setting = 'provider.' + i
            __external__.setSetting(source_setting, setting)
        if silent: return
        return _ext_scrapers_notice('Success')
    except:
        if silent: return
        return _ext_scrapers_notice('Failed')

def enable_disable_specific_all(folder):
    try:
        from modules.utils import multiselect_dialog
        enabled, disabled = scrapersStatus(folder)
        all_sources = sorted(enabled + disabled)
        preselect = [all_sources.index(i) for i in enabled]
        chosen = multiselect_dialog('Enable/Disable Scrapers', [i.upper() for i in all_sources], all_sources, preselect)
        if not chosen: return
        for i in all_sources:
            if i in chosen: __external__.setSetting('provider.' + i, 'true')
            else: __external__.setSetting('provider.' + i, 'false')
        return _ext_scrapers_notice('Success')
    except: return _ext_scrapers_notice('Failed')

def scrapersStatus(folder='all_eng'):
    providers = scraperNames(folder)
    enabled = [i for i in providers if __external__.getSetting('provider.' + i) == 'true']
    disabled = [i for i in providers if i not in enabled]
    return enabled, disabled

def scraperNames(folder):
    providerList = []
    provider = __external__.getSetting('module.provider')
    sourceFolder = getScraperFolder(provider)
    sourceFolderLocation = os.path.join(scraper_module_base_folder, sourceFolder)
    sourceSubFolders = [x[1] for x in os.walk(sourceFolderLocation)][0]
    if folder == 'all_eng':
        sourceSubFolders = [i for i in sourceSubFolders if i in ('en', 'en_DebridOnly', 'en_Torrent')]
    else:
        sourceSubFolders = [i for i in sourceSubFolders if i == folder]
    for i in sourceSubFolders:
        for loader, module_name, is_pkg in pkgutil.walk_packages([os.path.join(sourceFolderLocation, i)]):
            if is_pkg:
                continue
            providerList.append(module_name)
    return providerList

def getScraperFolder(scraper_source):
    sourceSubFolders = [x[1] for x in os.walk(scraper_module_base_folder)][0]
    try: sourceFolder = [i for i in sourceSubFolders if scraper_source.lower() in i.lower()][0]
    except: sourceFolder = setDefault()
    return sourceFolder

def setDefault():
    __external__.setSetting('module.provider', 'OpenScrapers')
    sourceFolder = 'sources_openscrapers'
    return sourceFolder

def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.strip()
    return txt

def getFileNameMatch(title, url, name=None):
    from modules.utils import clean_file_name
    if name: return clean_file_name(name)
    try: from urllib import unquote
    except ImportError: from urllib.parse import unquote
    from modules.utils import clean_title, normalize
    title_match = None
    try:
        title = clean_title(normalize(title))
        name_url = unquote(url)
        try: file_name = clean_title(name_url.split('/')[-1])
        except: return title_match
        test = name_url.split('/')
        for item in test:
            test_url = str(clean_title(normalize(item)))
            if title in test_url:
                title_match = clean_file_name(str(item)).replace('html', ' ').replace('+', ' ')
                break
    except:
        pass
    return title_match

def update_release_quality(release_name, current_quality):
    quality = current_quality
    try:
        if release_name is None: return current_quality
        release_name = replaceHTMLCodes(release_name)
        fmt = re.sub('[^A-Za-z0-9]+', ' ', release_name)
        fmt = fmt.encode('utf-8')
        fmt = str(fmt.lower())
        fmt = fmt.lower()
        fmtl = list(fmt.split(' '))
        if any(i in ['dvdscr', 'r5', 'r6'] for i in fmtl): quality = 'SCR'
        elif any(i in ['camrip', 'hdcam', 'dvdcam', 'cam'] for i in fmtl): quality = 'CAM'
        elif any(i in ['tc', 'tsrip', 'hdts', 'dvdts', 'hdtc', 'telecine', 'tc720p', 'tc720', 'hd-tc', 'hd-ts', 'telesync', 'ts'] for i in fmtl): quality = 'TELE'
        elif ' 2160p ' in fmt: quality = '4K'
        elif ' 2160 ' in fmt: quality = '4K'
        elif ' uhd ' in fmt: quality = '4K'
        elif ' 4k ' in fmt: quality = '4K'
        elif ' 1080p ' in fmt: quality = '1080p'
        elif ' 1080 ' in fmt: quality = '1080p'
        elif ' fullhd ' in fmt: quality = '1080p'
        elif ' 720p ' in fmt: quality = '720p'
        elif ' hd ' in fmt: quality = '720p'
        elif ' 480p ' in fmt: quality = 'SD'
        elif ' 480 ' in fmt: quality = 'SD'
        elif ' 576p ' in fmt: quality = 'SD'
        elif ' 576 ' in fmt: quality = 'SD'
    except: pass
    return quality

def getFileType(url):
    try:
        url = replaceHTMLCodes(url)
        url = re.sub('[^A-Za-z0-9]+', ' ', url)
        url = url.encode('utf-8')
        url = str(url.lower())
    except:
        url = str(url)
    info = ''
    if any(i in url for i in [' h 265 ', ' h265 ', ' x265 ', ' hevc ']):
        info += '[B]HEVC[/B] |'
    if ' hi10p ' in url:
        info += ' HI10P |'
    if ' 10bit ' in url:
        info += ' 10BIT |'
    if any(i in url for i in [' bluray ', ' blu ray ']):
        info += ' BLURAY |'
    if any(i in url for i in [' bd r ', ' bdr ', ' bd rip ', ' bdrip ', ' br rip ', ' brrip ']):
        info += ' BD-RIP |'
    if ' remux ' in url:
        info += ' REMUX |'
    if any(i in url for i in [' dvdrip ', ' dvd rip ']):
        info += ' DVD-RIP |'
    if any(i in url for i in [' dvd ', ' dvdr ', ' dvd r ']):
        info += ' DVD |'
    if any(i in url for i in [' webdl ', ' web dl ', ' web ', ' web rip ', ' webrip ']):
        info += ' WEB |'
    if ' hdtv ' in url:
        info += ' HDTV |'
    if ' sdtv ' in url:
        info += ' SDTV |'
    if any(i in url for i in [' hdrip ', ' hd rip ']):
        info += ' HDRIP |'
    if any(i in url for i in [' uhdrip ', ' uhd rip ']):
        info += ' UHDRIP |'
    if ' xvid ' in url:
        info += ' XVID |'
    if ' avi ' in url:
        info += ' AVI |'
    if ' hdr ' in url:
        info += ' HDR |'
    if ' imax ' in url:
        info += ' IMAX |'
    if ' ac3 ' in url:
        info += ' AC3 |'
    if ' eac3 ' in url:
        info += ' EAC3 |'
    if ' aac ' in url:
        info += ' AAC |'
    if any(i in url for i in [' dd ', ' dolby ', ' dolbydigital ', ' dolby digital ']):
        info += ' DD |'
    if any(i in url for i in [' truehd ', ' true hd ']):
        info += ' TRUEHD |'
    if ' atmos ' in url:
        info += ' ATMOS |'
    if any(i in url for i in [' ddplus ', ' dd plus ', ' ddp ']):
        info += ' DD+ |'
    if ' dts ' in url:
        info += ' DTS |'
    if any(i in url for i in [' hdma ', ' hd ma ']):
        info += ' HD.MA |'
    if any(i in url for i in [' hdhra ', ' hd hra ']):
        info += ' HD.HRA |'
    if any(i in url for i in [' dtsx ', ' dts x ']):
        info += ' DTS:X |'
    if ' dd5 1 ' in url:
        info += ' DD | 5.1 |'
    if any(i in url for i in [' 5 1 ', ' 6ch ']):
        info += ' 5.1 |'
    if any(i in url for i in [' 7 1 ', ' 8ch ']):
        info += ' 7.1 |'
    if any (i in url for i in [' subs ', ' subbed ', ' sub ']):
        info += ' SUBS |'
    if any (i in url for i in [' dub ', ' dubbed ', ' dublado ']):
        info += ' DUB |'
    info = info.rstrip('|')
    return info



