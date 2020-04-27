# -*- coding: utf-8 -*-

'''
    BoxsetKings Add-on
    Copyright (C) 2017 BoxsetKings

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


import json

from resources.lib.modules import control
from resources.lib.modules import trakt


def getMovieIndicators(refresh=False):
    try:
        if trakt.getTraktIndicatorsInfo() == True: raise Exception()
        from metahandler import metahandlers
        indicators = metahandlers.MetaData(preparezip=False)
        return indicators
    except:
        pass
    try:
        if trakt.getTraktIndicatorsInfo() == False: raise Exception()
        if refresh == False: timeout = 720
        elif trakt.getWatchedActivity() < trakt.timeoutsyncMovies(): timeout = 720
        else: timeout = 0
        indicators = trakt.cachesyncMovies(timeout=timeout)
        return indicators
    except:
        pass


def getTVShowIndicators(refresh=False):
    try:
        if trakt.getTraktIndicatorsInfo() == True: raise Exception()
        from metahandler import metahandlers
        indicators = metahandlers.MetaData(preparezip=False)
        return indicators
    except:
        pass
    try:
        if trakt.getTraktIndicatorsInfo() == False: raise Exception()
        if refresh == False: timeout = 720
        elif trakt.getWatchedActivity() < trakt.timeoutsyncTVShows(): timeout = 720
        else: timeout = 0
        indicators = trakt.cachesyncTVShows(timeout=timeout)
        return indicators
    except:
        pass


def getSeasonIndicators(imdb):
    try:
        if trakt.getTraktIndicatorsInfo() == False: raise Exception()
        indicators = trakt.syncSeason(imdb)
        return indicators
    except:
        pass
    try:
        if trakt.getTraktIndicatorsInfo() == True: raise Exception()
        from metahandler import metahandlers
        indicators = metahandlers.MetaData(preparezip=False)
        return indicators
    except:
        pass

# ----------------------- LOCAL WATCHED MARKS		

def getShowLocalIndicator(imdb):
    try:
        import sys,xbmc
        from resources.lib.modules import control
        

        total = '6'
        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        try: from sqlite3 import dbapi2 as database
        except: from pysqlite2 import dbapi2 as database
        season_playcount = []
        season_file = control.seasons_meta
        id = imdb.encode('utf-8')	
        try:

            control.makeFile(control.dataPath)
            dbcon = database.connect(season_file)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT playcount FROM season_meta WHERE imdb = '%s'" % (id))
            match = dbcur.fetchall()
            for playcount in match:
				if '7' in str(playcount): play = '7'
				else: play = '6'
				season_playcount.append(play)
				
        except:
            pass			


        if "6" in season_playcount: 
			total = '6'
			return total
        elif int(len(season_playcount)) > 0:
			if not "6" in season_playcount:
				total = '7'
				metaget._update_watched(id, 'tvshow', int(total))

        total = metaget._get_watched('tvshow', id, '', '')  
        print ("ELYSIUM SEASON PLAYCOUNT", imdb, season_playcount, total)	       		
        total = str(total)
        return total
        
    except:
        return total

		
def getSeasonIndicators2(tvshowtitle, imdb, tvdb, season):
    try:
        import sys,xbmc
        from resources.lib.modules import control
        
        if not trakt.getTraktIndicatorsInfo() == False: raise Exception()
        total = '6'
        from metahandler import metahandlers
        from resources.lib.indexers import episodes
        if not int('%01d' % int(season)) > 0: raise Exception()
        metaget = metahandlers.MetaData(preparezip=False)

        name = control.addonInfo('name')


        imdb = imdb.encode('utf-8')
        tvdb = tvdb.encode('utf-8')
        season = season.encode('utf-8')
        # metaget.get_meta('tvshow', '', imdb_id=imdb)

        items = episodes.episodes().get(tvshowtitle, '0', imdb, tvdb, '0', idx=False)
        try: items = [i for i in items if int('%01d' % int(season)) == int('%01d' % int(i['season']))]
        except: pass
        season_playcount = []
        for i in range(len(items)):

            season, episode = items[i]['season'], items[i]['episode']
            playcount = metaget._get_watched_episode({'imdb_id' : imdb, 'season' : season, 'episode': episode, 'premiered' : ''})
            playcount = str(playcount)
			
            if playcount == '7': play = '1'
            else: play = '0'
            
            season_playcount.append(playcount)



        season_file = control.seasons_meta
        try: from sqlite3 import dbapi2 as database
        except: from pysqlite2 import dbapi2 as database
        
        try:
            
            control.makeFile(control.dataPath)
            dbcon = database.connect(season_file)
            dbcur = dbcon.cursor()
            dbcur.execute("CREATE TABLE IF NOT EXISTS season_meta (""imdb TEXT, ""tvdb TEXT, ""season TEXT, ""playcount TEXT, ""UNIQUE(imdb, tvdb, season, playcount)"");")
            dbcon.commit()
        except:
            pass
			
        if "6" in season_playcount: 
			total = '6'
			dbcon = database.connect(season_file)
			dbcur = dbcon.cursor()
			dbcur.execute("DELETE FROM season_meta WHERE imdb = '%s' AND season = '%s'" % (imdb, season))
			dbcur.execute("INSERT INTO season_meta Values (?, ?, ?, ?)", (imdb, tvdb, season, total))
			dbcon.commit()

        elif int(len(season_playcount)) > 0:
			if not "6" in season_playcount:
				total = '7'
				dbcon = database.connect(season_file)
				dbcur = dbcon.cursor()
				dbcur.execute("DELETE FROM season_meta WHERE imdb = '%s' AND season = '%s'" % (imdb, season))
				dbcur.execute("INSERT INTO season_meta Values (?, ?, ?, ?)", (imdb, tvdb, season, total))
				dbcon.commit()

			# metaget.change_watched('season', name='', imdb_id=imdb, season=season, watched=int(total))
        return total



    except:
        return total


# -----------------------------------------------


def getMovieOverlay(indicators, imdb):
    try:
        try:
            playcount = indicators._get_watched('movie', imdb, '', '')
            return str(playcount)
        except:
            playcount = [i for i in indicators if i == imdb]
            playcount = 7 if len(playcount) > 0 else 6
            return str(playcount)
    except:
        return '6'


def getTVShowOverlay(indicators, tvdb):
    try:
        playcount = [i[0] for i in indicators if i[0] == tvdb and len(i[2]) >= int(i[1])]
        playcount = 7 if len(playcount) > 0 else 6
        return str(playcount)
    except:
        return '6'


def getEpisodeOverlay(indicators, imdb, tvdb, season, episode):
    try:
        try:
            playcount = indicators._get_watched_episode({'imdb_id' : imdb, 'season' : season, 'episode': episode, 'premiered' : ''})
            return str(playcount)
        except:
            playcount = [i[2] for i in indicators if i[0] == tvdb]
            playcount = playcount[0] if len(playcount) > 0 else []
            playcount = [i for i in playcount if int(season) == int(i[0]) and int(episode) == int(i[1])]
            playcount = 7 if len(playcount) > 0 else 6
            return str(playcount)
    except:
        return '6'


def markMovieDuringPlayback(imdb, watched):
    try:
        if trakt.getTraktIndicatorsInfo() == False: raise Exception()

        if int(watched) == 7: trakt.markMovieAsWatched(imdb)
        else: trakt.markMovieAsNotWatched(imdb)
        trakt.cachesyncMovies()

        if trakt.getTraktAddonMovieInfo() == True:
            trakt.markMovieAsNotWatched(imdb)
    except:
        pass

    try:
        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        metaget.get_meta('movie', name='', imdb_id=imdb)
        metaget.change_watched('movie', name='', imdb_id=imdb, watched=int(watched))
    except:
        pass


def markEpisodeDuringPlayback(imdb, tvdb, season, episode, watched):
    try:
        if trakt.getTraktIndicatorsInfo() == False: raise Exception()

        if int(watched) == 7: trakt.markEpisodeAsWatched(tvdb, season, episode)
        else: trakt.markEpisodeAsNotWatched(tvdb, season, episode)
        trakt.cachesyncTVShows()

        if trakt.getTraktAddonEpisodeInfo() == True:
            trakt.markEpisodeAsNotWatched(tvdb, season, episode)
    except:
        pass

    try:
        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        metaget.get_meta('tvshow', name='', imdb_id=imdb)
        metaget.get_episode_meta('', imdb_id=imdb, season=season, episode=episode)
        metaget.change_watched('episode', '', imdb_id=imdb, season=season, episode=episode, watched=int(watched))
    except:
        pass


def movies(imdb, watched):
    try:
        if trakt.getTraktIndicatorsInfo() == False: raise Exception()
        if int(watched) == 7: trakt.markMovieAsWatched(imdb)
        else: trakt.markMovieAsNotWatched(imdb)
        trakt.cachesyncMovies()
        control.refresh()
    except:
        pass

    try:
        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        metaget.get_meta('movie', name='', imdb_id=imdb)
        metaget.change_watched('movie', name='', imdb_id=imdb, watched=int(watched))
        if trakt.getTraktIndicatorsInfo() == False: control.refresh()
    except:
        pass


def episodes(imdb, tvdb, season, episode, watched):
    try:
        if trakt.getTraktIndicatorsInfo() == False: raise Exception()
        if int(watched) == 7: trakt.markEpisodeAsWatched(tvdb, season, episode)
        else: trakt.markEpisodeAsNotWatched(tvdb, season, episode)
        trakt.cachesyncTVShows()
        control.refresh()
    except:
        pass

    try:
        from metahandler import metahandlers
        metaget = metahandlers.MetaData(preparezip=False)
        metaget.get_meta('tvshow', name='', imdb_id=imdb)
        metaget.get_episode_meta('', imdb_id=imdb, season=season, episode=episode)
        metaget.change_watched('episode', '', imdb_id=imdb, season=season, episode=episode, watched=int(watched))
        if trakt.getTraktIndicatorsInfo() == False: control.refresh()
    except:
        pass


def tvshows(tvshowtitle, imdb, tvdb, season, watched):
    try:
        import sys,xbmc

        if not trakt.getTraktIndicatorsInfo() == False: raise Exception()
        watched=int(watched)
        from metahandler import metahandlers
        from resources.lib.indexers import episodes
        imdb = imdb.encode('utf-8')
        metaget = metahandlers.MetaData(preparezip=False)

        name = control.addonInfo('name')

        dialog = control.progressDialogBG
        dialog.create(str(name), str(tvshowtitle))
        dialog.update(0, str(name), str(tvshowtitle))

        items = episodes.episodes().get(tvshowtitle, '0', imdb, tvdb, '0', idx=False)
        try: items = [i for i in items if int('%01d' % int(season)) == int('%01d' % int(i['season']))]
        except: pass
        items = [{'label': '%s S%02dE%02d' % (tvshowtitle, int(i['season']), int(i['episode'])), 'season': int('%01d' % int(i['season'])), 'episode': int('%01d' % int(i['episode']))} for i in items]

        for i in range(len(items)):
            if xbmc.abortRequested == True: return sys.exit()

            dialog.update(int((100 / float(len(items))) * i), str(name), str(items[i]['label']))

            season, episode = items[i]['season'], items[i]['episode']
            metaget.get_episode_meta('', imdb, season, episode)
            metaget.change_watched('episode', '', imdb, season=season, episode=episode, year='', watched=watched)

        try: dialog.close()
        except: pass
    except:
        try: dialog.close()
        except: pass


    control.refresh()

	
def marktvshows(tvshowtitle, imdb, tvdb, watched):
    try:
        import sys,xbmc

        if not trakt.getTraktIndicatorsInfo() == False: raise Exception()
        watched=int(watched)
        from metahandler import metahandlers
        from resources.lib.indexers import episodes
		
        imdb = imdb.encode('utf-8')

        metaget = metahandlers.MetaData(preparezip=False)

        name = control.addonInfo('name')

        dialog = control.progressDialogBG
        dialog.create(str(name), str(tvshowtitle))
        dialog.update(0, str(name), str(tvshowtitle))

        items = episodes.episodes().get(tvshowtitle, '0', imdb, tvdb, '0', idx=False)
        try: items = [i for i in items]
        except: pass
        items = [{'label': '%s S%02dE%02d' % (tvshowtitle, int(i['season']), int(i['episode'])), 'season': int('%01d' % int(i['season'])), 'episode': int('%01d' % int(i['episode']))} for i in items]

        season_file = control.seasons_meta
        try: from sqlite3 import dbapi2 as database
        except: from pysqlite2 import dbapi2 as database
        try:
            if watched == 6:
				total = '6'
				dbcon = database.connect(season_file)
				dbcur = dbcon.cursor()
				dbcur.execute("DELETE FROM season_meta WHERE imdb = '%s'" % (imdb))
				dbcon.commit()
        except:
            pass
			
		
        for i in range(len(items)):
            if xbmc.abortRequested == True: return sys.exit()
            dialog.update(int((100 / float(len(items))) * i), str(name), str(items[i]['label']))
            season, episode = items[i]['season'], items[i]['episode']
            metaget.get_episode_meta('', imdb, season, episode)
            metaget.change_watched('episode', '', imdb, season=season, episode=episode, year='', watched=watched)
            try:
				if watched == 7:
					total = '7'
					dbcon = database.connect(season_file)
					dbcur = dbcon.cursor()
					dbcur.execute("DELETE FROM season_meta WHERE imdb = '%s' AND season = '%s'" % (imdb, season))
					dbcur.execute("INSERT INTO season_meta Values (?, ?, ?, ?)", (imdb, tvdb, season, total))
					dbcon.commit()
            except:
				pass
				
        try: dialog.close()
        except: pass
    except:
        try: dialog.close()
        except: pass


    try:
        import sys,xbmc
        watched=int(watched)
        imdb = imdb.encode('utf-8')
        from metahandler import metahandlers
        from resources.lib.indexers import episodes

        metaget = metahandlers.MetaData(preparezip=False)
        metaget.get_meta('tvshow', name='', imdb_id=imdb)
        metaget._update_watched(imdb, 'tvshow', watched)
        metaget.change_watched('tvshow', '', imdb, watched=watched)

    except:
        pass
		

			
	



    control.refresh()

