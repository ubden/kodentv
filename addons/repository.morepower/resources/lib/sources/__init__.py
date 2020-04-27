# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import sys,pkgutil,re,json,urllib,urlparse,random,datetime,time

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import workers

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

try: import urlresolver
except: pass

try: import xbmc
except: pass


class sources:
    def __init__(self):
        self.getConstants()
        self.sources = []


    def getSources(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, quality='HD', timeout=20):
        u = None

        sourceDict = []
        for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
        sourceDict = [i[0] for i in sourceDict if i[1] == False]

        content = 'movie' if tvshowtitle == None else 'episode'

        if content == 'movie':
            sourceDict = [i for i in sourceDict if i.endswith(('_mv', '_mv_tv'))]
        else:
            sourceDict = [i for i in sourceDict if i.endswith(('_tv', '_mv_tv'))]

        if quality == 'SD':
            quality = ['movie4k_mv', 'movie25_mv', 'onseries_tv', 'primewire_mv_tv', 'watchfree_mv_tv', 'watchseries_tv', 'wmo_mv']
            sourceDict = [i for i in sourceDict if i in quality]

        threads = []

        control.makeFile(control.dataPath)
        self.sourceFile = control.providercacheFile

        if content == 'movie':
            title = cleantitle.normalize(title)
            for source in sourceDict: threads.append(workers.Thread(self.getMovieSource, title, year, imdb, re.sub('_mv_tv$|_mv$|_tv$', '', source), __import__(source, globals(), locals(), [], -1).source()))
        else:
            tvshowtitle = cleantitle.normalize(tvshowtitle)
            for source in sourceDict: threads.append(workers.Thread(self.getEpisodeSource, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, re.sub('_mv_tv$|_mv$|_tv$', '', source), __import__(source, globals(), locals(), [], -1).source()))

        [i.start() for i in threads]

        progressDialog = control.progressDialog
        progressDialog.create(control.addonInfo('name'), control.lang(30726).encode('utf-8'))
        progressDialog.update(0)

        progressDialog.update(0, control.lang(30726).encode('utf-8'), control.lang(30731).encode('utf-8'))

        for i in range(0, timeout * 2):
            try:
                if progressDialog.iscanceled(): break
                if xbmc.abortRequested == True: return sys.exit()
                is_alive = [x.is_alive() for x in threads]
                if all(x == False for x in is_alive): break
                time.sleep(0.5)
            except:
                pass

        for i in range(0, 20 * 2):
            try:
                if progressDialog.iscanceled(): break
                if xbmc.abortRequested == True: return sys.exit()
                is_alive = [x.is_alive() for x in threads]
                if all(x == False for x in is_alive): break
                if self.sources: break
                time.sleep(0.5)
            except:
                pass

        progressDialog.update(50, control.lang(30726).encode('utf-8'), control.lang(30731).encode('utf-8'))

        items = self.sourcesFilter()

        filter = [i for i in items if i['source'].lower() in self.hostcapDict and i['debrid'] == '']
        items = [i for i in items if not i in filter]

        filter = [i for i in items if i['source'].lower() in self.hostblockDict and i['debrid'] == '']
        items = [i for i in items if not i in filter]

        items = [i for i in items if ('autoplay' in i and i['autoplay'] == True) or not 'autoplay' in i]

        for i in range(len(items)):
            try:
                if progressDialog.iscanceled(): break
                if xbmc.abortRequested == True: return sys.exit()
                url = self.sourcesResolve(items[i])
                if u == None: u = url
                if not url == None: break
            except:
                pass

        try: progressDialog.close()
        except: pass

        return u


    def getURISource(self, url):
        u = None

        sourceDict = []
        for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
        sourceDict = [i[0] for i in sourceDict if i[1] == False]
        sourceDict = [(i, __import__(i, globals(), locals(), [], -1).source()) for i in sourceDict]

        domain = re.sub('^www\.|^www\d+\.', '', urlparse.urlparse(url.strip().lower()).netloc)

        domains = [(i[0], i[1].domains) for i in sourceDict]
        domains = [i[0] for i in domains if any(x in domain for x in i[1])]

        if not domains: return False

        call = [i[1] for i in sourceDict if i[0] == domains[0]][0]

        progressDialog = control.progressDialog
        progressDialog.create(control.addonInfo('name'), control.lang(30726).encode('utf-8'))
        progressDialog.update(0)

        progressDialog.update(0, control.lang(30726).encode('utf-8'), control.lang(30731).encode('utf-8'))

        self.sources = call.sources(url, self.hostDict, self.hostprDict)

        progressDialog.update(50, control.lang(30726).encode('utf-8'), control.lang(30731).encode('utf-8'))

        items = self.sourcesFilter()

        filter = [i for i in items if i['source'].lower() in self.hostcapDict and i['debrid'] == '']
        items = [i for i in items if not i in filter]

        filter = [i for i in items if i['source'].lower() in self.hostblockDict and i['debrid'] == '']
        items = [i for i in items if not i in filter]

        items = [i for i in items if ('autoplay' in i and i['autoplay'] == True) or not 'autoplay' in i]

        for i in range(len(items)):
            try:
                if progressDialog.iscanceled(): break
                if xbmc.abortRequested == True: return sys.exit()
                url = self.sourcesResolve(items[i])
                if u == None: u = url
                if not url == None: break
            except:
                pass

        try: progressDialog.close()
        except: pass

        return u


    def getMovieSource(self, title, year, imdb, source, call):
        try:
            dbcon = database.connect(self.sourceFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_url (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""rel_url TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_src (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""hosts TEXT, ""added TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
        except:
            pass

        try:
            sources = []
            dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            match = dbcur.fetchone()
            t1 = int(re.sub('[^0-9]', '', str(match[5])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) > 60
            if update == False:
                sources = json.loads(match[4])
                return self.sources.extend(sources)
        except:
            pass

        try:
            url = None
            dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            url = dbcur.fetchone()
            url = url[4]
        except:
            pass

        try:
            if url == None: url = call.movie(imdb, title, year)
            if url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, '', '', url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = call.sources(url, self.hostDict, self.hostprDict)
            if sources == None or sources == []: raise Exception()
            self.sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, imdb, '', '', json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except:
            pass


    def getEpisodeSource(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, source, call):
        try:
            dbcon = database.connect(self.sourceFile)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_url (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""rel_url TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
            dbcur.execute("CREATE TABLE IF NOT EXISTS rel_src (""source TEXT, ""imdb_id TEXT, ""season TEXT, ""episode TEXT, ""hosts TEXT, ""added TEXT, ""UNIQUE(source, imdb_id, season, episode)"");")
        except:
            pass

        try:
            sources = []
            dbcur.execute("SELECT * FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
            match = dbcur.fetchone()
            t1 = int(re.sub('[^0-9]', '', str(match[5])))
            t2 = int(datetime.datetime.now().strftime("%Y%m%d%H%M"))
            update = abs(t2 - t1) > 60
            if update == False:
                sources = json.loads(match[4])
                return self.sources.extend(sources)
        except:
            pass

        try:
            url = None
            dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            url = dbcur.fetchone()
            url = url[4]
        except:
            pass

        try:
            if url == None: url = call.tvshow(imdb, tvdb, tvshowtitle, year)
            if url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, '', ''))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, '', '', url))
            dbcon.commit()
        except:
            pass

        try:
            ep_url = None
            dbcur.execute("SELECT * FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
            ep_url = dbcur.fetchone()
            ep_url = ep_url[4]
        except:
            pass

        try:
            if url == None: raise Exception()
            if ep_url == None: ep_url = call.episode(url, imdb, tvdb, title, premiered, season, episode)
            if ep_url == None: raise Exception()
            dbcur.execute("DELETE FROM rel_url WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
            dbcur.execute("INSERT INTO rel_url Values (?, ?, ?, ?, ?)", (source, imdb, season, episode, ep_url))
            dbcon.commit()
        except:
            pass

        try:
            sources = []
            sources = call.sources(ep_url, self.hostDict, self.hostprDict)
            if sources == None or sources == []: raise Exception()
            self.sources.extend(sources)
            dbcur.execute("DELETE FROM rel_src WHERE source = '%s' AND imdb_id = '%s' AND season = '%s' AND episode = '%s'" % (source, imdb, season, episode))
            dbcur.execute("INSERT INTO rel_src Values (?, ?, ?, ?, ?, ?)", (source, imdb, season, episode, json.dumps(sources), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
            dbcon.commit()
        except:
            pass


    def sourcesFilter(self):
        provider = control.setting('hosts.sort.provider')

        quality = control.setting('hosts.quality')
        if quality == '': quality = '0'

        captcha = control.setting('hosts.captcha')


        random.shuffle(self.sources)

        if provider == 'true':
            self.sources = sorted(self.sources, key=lambda k: k['provider'])

        local = [i for i in self.sources if 'local' in i and i['local'] == True]
        self.sources = [i for i in self.sources if not i in local]

        filter = []
        filter += [i for i in self.sources if i['direct'] == True]
        filter += [i for i in self.sources if i['direct'] == False]
        self.sources = filter

        filter = []
        for d in self.debridDict: filter += [dict(i.items() + [('debrid', d)]) for i in self.sources if i['source'].lower() in self.debridDict[d]]
        filter += [i for i in self.sources if not i['source'].lower() in self.hostprDict and i['debridonly'] == False]
        self.sources = filter

        filter = []
        filter += local
        if quality == '0': filter += [i for i in self.sources if i['quality'] == '1080p' and 'debrid' in i]
        if quality == '0' or quality == '1': filter += [i for i in self.sources if i['quality'] == 'HD' and 'debrid' in i]
        if quality == '0': filter += [i for i in self.sources if i['quality'] == '1080p' and not 'debrid' in i and 'memberonly' in i]
        if quality == '0' or quality == '1': filter += [i for i in self.sources if i['quality'] == 'HD' and not 'debrid' in i and 'memberonly' in i]
        if quality == '0': filter += [i for i in self.sources if i['quality'] == '1080p' and not 'debrid' in i and not 'memberonly' in i]
        if quality == '0' or quality == '1': filter += [i for i in self.sources if i['quality'] == 'HD' and not 'debrid' in i and not 'memberonly' in i]
        filter += [i for i in self.sources if i['quality'] == 'SD']
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'SCR']
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'CAM']
        self.sources = filter

        if not captcha == 'true':
            filter = [i for i in self.sources if i['source'].lower() in self.hostcapDict and not 'debrid' in i]
            self.sources = [i for i in self.sources if not i in filter]

        filter = [i for i in self.sources if i['source'].lower() in self.hostblockDict and not 'debrid' in i]
        self.sources = [i for i in self.sources if not i in filter]

        self.sources = self.sources[:2000]

        for i in range(len(self.sources)):
            u = self.sources[i]['url']
            s = self.sources[i]['source'].lower()
            p = self.sources[i]['provider']
            p = re.sub('v\d*$', '', p)

            q = self.sources[i]['quality']

            try: f = (' | '.join(['[I]%s [/I]' % info.strip() for info in self.sources[i]['info'].split('|')]))
            except: f = ''

            try: d = self.sources[i]['debrid']
            except: d = self.sources[i]['debrid'] = ''

            if not d == '': label = '%02d | [B]%s[/B] | ' % (int(i+1), d)
            #if not d == '': label = '%02d | [B]%s[/B] | [B]%s[/B] | ' % (int(i+1), p, d)
            else: label = '%02d | [B]%s[/B] | ' % (int(i+1), p)

            if q in ['1080p', 'HD']: label += '%s | %s | [B][I]%s [/I][/B]' % (s.rsplit('.', 1)[0], f, q)
            elif q == 'SD': label += '%s | %s' % (s.rsplit('.', 1)[0], f)
            else: label += '%s | %s | [I]%s [/I]' % (s.rsplit('.', 1)[0], f, q)
            label = label.replace('| 0 |', '|').replace(' | [I]0 [/I]', '')
            label = label.replace('[I]HEVC [/I]', 'HEVC')
            label = re.sub('\[I\]\s+\[/I\]', ' ', label)
            label = re.sub('\|\s+\|', '|', label)
            label = re.sub('\|(?:\s+|)$', '', label)

            self.sources[i]['label'] = label.upper()

        return self.sources


    def sourcesResolve(self, item, info=False):
        try:
            self.url = None

            u = url = item['url']

            d = item['debrid'] ; direct = item['direct']

            provider = item['provider'].lower()

            if not provider.endswith(('_mv', '_tv', '_mv_tv')):
                sourceDict = []
                for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
                provider = [i[0] for i in sourceDict if i[1] == False and i[0].startswith(provider + '_')][0]

            source = __import__(provider, globals(), locals(), [], -1).source()
            u = url = source.resolve(url)

            if url == None or not '://' in str(url): raise Exception()

            if not d == '':
                url = debrid.resolver(url, d)

            elif not direct == True:
                hmf = urlresolver.HostedMediaFile(url=u, include_disabled=True, include_universal=False)
                if hmf.valid_url() == True: url = hmf.resolve()


            if url == False or url == None: raise Exception()

            ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
            if ext == 'rar': raise Exception()

            try: headers = url.rsplit('|', 1)[1]
            except: headers = ''
            headers = urllib.quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
            headers = dict(urlparse.parse_qsl(headers))


            if url.startswith('http') and '.m3u8' in url:
                result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout='20')
                if result == None: raise Exception()

            elif url.startswith('http'):
                result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='20')
                if result == None: raise Exception()


            self.url = url
            return url
        except:
            if info == True: self.errorForSources()
            return


    def errorForSources(self):
        return


    def getConstants(self):
        try:
            self.hostDict = urlresolver.relevant_resolvers(order_matters=True)
            self.hostDict = [i.domains for i in self.hostDict if not '*' in i.domains]
            self.hostDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostDict)]
            self.hostDict = [x for y,x in enumerate(self.hostDict) if x not in self.hostDict[:y]]
        except:
            self.hostDict = []

        self.hostprDict = ['1fichier.com', 'oboom.com', 'rapidgator.net', 'rg.to', 'uploaded.net', 'uploaded.to', 'ul.to', 'filefactory.com', 'nitroflare.com', 'turbobit.net', 'uploadrocket.net']

        self.hostcapDict = ['hugefiles.net', 'kingfiles.net', 'openload.io', 'openload.co', 'thevideo.me', 'torba.se']

        self.hostblockDict = []

        self.debridDict = debrid.debridDict()


