# -*- coding: utf-8 -*-

import xbmc, xbmcaddon
import os
import json
from tikimeta import tmdb
from tikimeta import tvdb
from tikimeta import trakt
from tikimeta import fanarttv
from tikimeta.kyradb import add as kiradb_add
from tikimeta.kyradb import KyraDBAPI as kyradb
from tikimeta.metacache import MetaCache
from tikimeta.utils import try_parse_int, safe_string, remove_accents, to_utf8
# from tikimeta.utils import logger

__addon__ = xbmcaddon.Addon("script.module.tikimeta")
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))

def getMovieMeta(id_type, media_id, user_info, hours=720):
    from datetime import timedelta
    metacache = MetaCache()
    meta = None
    tmdb_api = user_info['tmdb_api']
    image_resolution = user_info.get('image_resolution', {'poster': 'w780', 'fanart': 'w1280', 'still': 'w185', 'profile': 'w185'})
    language = user_info['language']
    extra_fanart_enabled = user_info['extra_fanart_enabled']
    def tmdb_meta(language):
        data = tmdb.tmdbMovies
        result = tmdb.tmdbMoviesExternalID
        return data(media_id, language, tmdb_api) if id_type == 'tmdb_id' else data(result(id_type, media_id, tmdb_api)['id'], language, tmdb_api)
    def fanarttv_meta(fanart_id):
        if extra_fanart_enabled: return fanarttv.get('movies', language, fanart_id, user_info['fanart_client_key'])
        else: return None
    # def kyradb_meta(kyradb_id):
    #     if user_info['gif_posters_enabled']: return kyradb(user_info['kyra_api_key'], user_info['kyra_user_key']).get_art(kyradb_id)
    #     else: return None
    def cached_meta():
        return metacache.get('movie', id_type, media_id)
    def set_cache_meta():
        metacache.set('movie', meta, timedelta(hours=hours))
    def delete_cache_meta():
        metacache.delete('movie', 'tmdb_id', meta['tmdb_id'])
    def check_tmdb_data(tmdb_data):
        if language != 'en' and tmdb_data['overview'] == '':
            overview = tmdb_meta('en')['overview']
            tmdb_data['overview'] = overview
        return tmdb_data
    meta = cached_meta()
    if meta and extra_fanart_enabled and not meta.get('fanart_added', False):
        try:
            meta = fanarttv.add('movies', language, meta['tmdb_id'], meta, user_info['fanart_client_key'])
            delete_cache_meta()
            set_cache_meta()
        except: pass
    # if meta and user_info['gif_posters_enabled'] and not meta.get('kyradb_added', False):
    #     try:
    #         meta = kiradb_add(meta['tmdb_id'], meta, user_info['kyra_api_key'], user_info['kyra_user_key'])
    #         delete_cache_meta()
    #         set_cache_meta()
    #     except: pass
    if not meta:
        try:
            fetch_fanart_art = False
            tmdb_data = check_tmdb_data(tmdb_meta(language))
            if not tmdb_data.get('poster_path', None):
                if extra_fanart_enabled: fetch_fanart_art = True
            fanarttv_data = fanarttv_meta(tmdb_data['id'])
            if fetch_fanart_art:
                tmdb_data['external_poster'] = fanarttv_data.get('fanarttv_poster', None)
                tmdb_data['external_fanart'] = fanarttv_data.get('fanarttv_fanart', None)
            tmdb_data['image_resolution'] = image_resolution
            # kyradb_data = kyradb_meta(tmdb_data['id'])
            kyradb_data = None # kyradb is currently offline.
            meta = buildMeta('movie', tmdb_data, fanarttv_data=fanarttv_data, kyradb_data=kyradb_data)
            set_cache_meta()
        except: pass
    return meta

def getTVShowMeta(id_type, media_id, user_info, hours=96):
    from datetime import timedelta
    metacache = MetaCache()
    meta = None
    tmdb_api = user_info['tmdb_api']
    tvdb_jwtoken = user_info['tvdb_jwtoken']
    tvdb_api = user_info['tvdb_api']
    image_resolution = user_info.get('image_resolution', {'poster': 'w780', 'fanart': 'w1280', 'still': 'w185', 'profile': 'w185'})
    language = user_info['language']
    extra_fanart_enabled = user_info['extra_fanart_enabled']
    def tmdb_meta():
        data = tmdb.tmdbTVShows
        result = tmdb.tmdbTVShowsExternalID
        return data(media_id, language, tmdb_api) if id_type == 'tmdb_id' else data(result(id_type, media_id, tmdb_api)['id'], language, tmdb_api)
    def tvdb_meta(tvdb_id):
        tvdb_summary = tvdb.TvdbAPI(tvdb_api, tvdb_jwtoken).get_series_episodes_summary(tvdb_id)
        return tvdb_summary
    def trakt_ids(id_type, _id):
        all_trakt_ids = trakt.traktGetIDs('show', id_type, str(_id))
        return all_trakt_ids
    def tvdb_overview(tvdb_id):
        tvdb_overview = tvdb.TvdbAPI(tvdb_api, tvdb_jwtoken).get_series_overview(tvdb_id, language)
        return tvdb_overview
    def fanarttv_meta(fanart_id):
        if extra_fanart_enabled: return fanarttv.get('tv', language, fanart_id, user_info['fanart_client_key'])
        else: return None
    def cached_meta():
        return metacache.get('tvshow', id_type, media_id)
    def set_cache_meta():
        metacache.set('tvshow', meta, timedelta(hours=hours))
    def delete_cache_meta():
        metacache.delete('tvshow', 'tmdb_id', meta['tmdb_id'])
    def check_tmdb_data(tvdb_id, tmdb_data):
        if language != 'en' and tmdb_data['overview'] == '':
            overview = tvdb_overview(tvdb_id)
            tmdb_data['overview'] = overview
        return tmdb_data
    meta = cached_meta()
    if meta and extra_fanart_enabled and not meta.get('fanart_added', False):
        try:
            meta = fanarttv.add('tv', language, meta['tvdb_id'], meta, user_info['fanart_client_key'])
            delete_cache_meta()
            set_cache_meta()
        except: pass
    if meta and not 'tvdb_summary' in meta:
        delete_cache_meta()
        meta = None
    if not meta:
        try:
            tvdb_summary = None
            tvdb_data = None
            fanarttv_data = None
            tmdb_data = tmdb_meta()
            tvdb_id = tmdb_data['external_ids']['tvdb_id']
            if not tvdb_id:
                imdb_id = tmdb_data['external_ids']['imdb_id']
                if imdb_id:
                    try:
                        tvdb_data = tvdb.TvdbAPI(tvdb_api, tvdb_jwtoken).get_series_by_imdb_id(imdb_id)
                        tvdb_id = tvdb_data.get('id', None)
                    except: pass
                if not tvdb_id:
                    try:
                        tvdb_data = tvdb.TvdbAPI(tvdb_api, tvdb_jwtoken).get_series_by_name(tmdb_data['name'])
                        tvdb_id = tvdb_data.get('id', None)
                    except: pass
                if tvdb_data:
                    tmdb_data['external_ids']['tvdb_id'] = tvdb_id
                    if not tmdb_data['poster_path']:
                        if tvdb_data.get('poster', None):
                            if 'banners' in tvdb_data['poster']: tmdb_data['external_poster'] = "http://thetvdb.com%s" % tvdb_data['poster']
                            else: tmdb_data['external_poster'] = "http://thetvdb.com/banners/%s" % tvdb_data['poster']
                        elif tvdb_data.get('image', None):
                            if 'banners' in tvdb_data['image']: tmdb_data['external_poster'] = "http://thetvdb.com%s" % tvdb_data['image']
                            else: tmdb_data['external_poster'] = "http://thetvdb.com/banners/%s" % tvdb_data['image']
                    if not tmdb_data['backdrop_path']:
                        if tvdb_data.get('fanart', None):
                            if 'banners' in tvdb_data['poster']: tmdb_data['external_fanart'] = "http://thetvdb.com%s" % tvdb_data['fanart']
                            else: tmdb_data['external_fanart'] = "http://thetvdb.com/banners/%s" % tvdb_data['fanart']
            if tvdb_id:
                tvdb_data = None
                tmdb_data = check_tmdb_data(tvdb_id, tmdb_data)
                tvdb_summary = tvdb_meta(tvdb_id)
                if not tmdb_data['poster_path'] and not tmdb_data.get('external_poster', None):
                    tvdb_data = tvdb.TvdbAPI(tvdb_api, tvdb_jwtoken).get_series(tvdb_id, language)
                    if tvdb_data.get('poster', None):
                        if 'banners' in tvdb_data['poster']: tmdb_data['external_poster'] = "http://thetvdb.com%s" % tvdb_data['poster']
                        else: tmdb_data['external_poster'] = "http://thetvdb.com/banners/%s" % tvdb_data['poster']
                    elif tvdb_data.get('image', None):
                        if 'banners' in tvdb_data['image']: tmdb_data['external_poster'] = "http://thetvdb.com%s" % tvdb_data['image']
                        else: tmdb_data['external_poster'] = "http://thetvdb.com/banners/%s" % tvdb_data['image']
                if not tmdb_data['backdrop_path'] and not tmdb_data.get('external_fanart', None):
                    if not tvdb_data: tvdb_data = tvdb.TvdbAPI(tvdb_api, tvdb_jwtoken).get_series(tvdb_id, language)
                    if tvdb_data.get('fanart', None):
                        if 'banners' in tvdb_data['poster']: tmdb_data['external_fanart'] = "http://thetvdb.com%s" % tvdb_data['fanart']
                        else: tmdb_data['external_fanart'] = "http://thetvdb.com/banners/%s" % tvdb_data['fanart']
                if tvdb_summary['airedSeasons'] == []:
                    tvdb_summary = None
                tmdb_data['image_resolution'] = image_resolution
                fanarttv_data = fanarttv_meta(tvdb_id)
            meta = buildMeta('tvshow', tmdb_data, fanarttv_data=fanarttv_data, tvdb_summary=tvdb_summary)
            set_cache_meta()
        except: pass
    return meta

def getAllEpisodes(media_id, tvdb_id, seasons, tmdb_data, user_info, hours=96):
    def _reset_meta(tvdb_id):
        metacache = MetaCache()
        series_meta['tvdb_id'] = tvdb_id
        metacache.delete('tvshow', 'tmdb_id', media_id)
        metacache.set('tvshow', series_meta, timedelta(hours=hours), media_id)
        data = tvdb.TvdbAPI(user_info['tvdb_api'], user_info['tvdb_jwtoken']).get_all_episodes(tvdb_id, language)
        return _return_meta(data)
    def _get_tmdb_episodes(season):
        try:
            episodes = tmdb.tmdbSeasonEpisodes(media_id, season, language, user_info['tmdb_api'])['episodes']
            tmdb_data = {'season': season, 'episode_info': episodes}
            all_tmdb_episodes.append(tmdb_data)
        except: pass
    def _return_meta(data, use_tmdb=False):
        meta = buildSeasonsMeta(data, seasons, tmdb_data, image_resolution, use_tmdb=use_tmdb)
        metacache.set('season', meta, timedelta(hours=hours), media_id)
        return meta
    image_resolution = user_info.get('image_resolution', {'poster': 'w780', 'fanart': 'w1280', 'still': 'w185', 'profile': 'w185'})
    language = user_info['language']
    metacache = MetaCache()
    meta = None
    use_tmdb = False
    all_tmdb_episodes = []
    threads = []
    data = metacache.get('season', 'tmdb_id', media_id)
    if data: return data
    try:
        from datetime import timedelta
        if tvdb_id: data = tvdb.TvdbAPI(user_info['tvdb_api'], user_info['tvdb_jwtoken']).get_all_episodes(tvdb_id, language)
        if data: return _return_meta(data)
        from threading import Thread
        series_meta = getTVShowMeta('tmdb_id', media_id, user_info)
        imdb_id = series_meta['imdb_id']
        if imdb_id: data = tvdb.TvdbAPI(user_info['tvdb_api'], user_info['tvdb_jwtoken']).get_series_by_imdb_id(imdb_id)
        if data: _reset_meta(data['id'])
        for i in seasons: threads.append(Thread(target=_get_tmdb_episodes, args=(int(i),)))
        [i.start() for i in threads]
        [i.join() for i in threads]
        data = all_tmdb_episodes
        use_tmdb = True
    except: pass
    return _return_meta(data, use_tmdb)

def getSeasonEpisodes(media_id, tvdb_id, season, seasons, tmdb_data, user_info, all_episodes=False, hours=96):
    metacache = MetaCache()
    data = None
    episodes_data = None
    image_resolution = user_info.get('image_resolution', {'poster': 'w780', 'fanart': 'w1280', 'still': 'w185', 'profile': 'w185'})
    data = metacache.get('season', 'tmdb_id', media_id)
    if not data: data = getAllEpisodes(media_id, tvdb_id, seasons, tmdb_data, user_info)
    if data:
        use_tmdb = data[0].get('use_tmdb', False)
        if use_tmdb:
            episodes_data = tmdb.tmdbSeasonEpisodes(media_id, season, user_info['language'], user_info['tmdb_api'])['episodes']
        else:
            if all_episodes:
                episodes_data = []
                data = [i['episodes_data'] for i in data]
                for item in data:
                    for ep in item:
                        episodes_data.append(ep)
            else:
                episodes_data = [i['episodes_data'] for i in data if i['season_number'] == int(season)][0]
        episodes_data = buildEpisodesMeta(episodes_data, image_resolution, use_tmdb=use_tmdb)
    return episodes_data

def buildMeta(db_type, data, fanarttv_data=None, kyradb_data=None, tvdb_summary=None):
    meta = {}
    writer = []
    meta['cast'] = []
    meta['studio'] = []
    meta['all_trailers'] = []
    meta['mpaa'] = ''
    meta['director'] = ''
    meta['premiered'] = ''
    meta['writer'] = ''
    meta['trailer'] = ''
    meta['tmdb_id'] = data['id'] if 'id' in data else ''
    meta['imdb_id'] = data.get('imdb_id', '') if db_type == 'movie' else data['external_ids'].get('imdb_id', '')
    meta['imdbnumber'] = meta['imdb_id']
    meta['tvdb_id'] = data['external_ids'].get('tvdb_id', 'None')
    if data.get('poster_path'):
        meta['poster'] = "http://image.tmdb.org/t/p/%s%s" % (data['image_resolution']['poster'], data.get('poster_path'))
    elif data.get('external_poster'):
        meta['poster'] = data['external_poster']
    else:
        meta['poster'] = xbmc.translatePath(os.path.join(addon_dir, "resources", "default_images", "tikimeta_blank_poster.png"))
    if data.get('backdrop_path'):
        meta['fanart'] = "http://image.tmdb.org/t/p/%s%s" % (data['image_resolution']['fanart'], data.get('backdrop_path'))
    elif data.get('external_fanart'):
        meta['fanart'] = data['external_fanart']
    else:
        meta['fanart'] = xbmc.translatePath(os.path.join(addon_dir, "resources", "default_images", "tikimeta_blank_fanart.png"))
    if fanarttv_data:
        meta['banner'] = fanarttv_data['banner']
        meta['clearart'] = fanarttv_data['clearart']
        meta['clearlogo'] = fanarttv_data['clearlogo']
        meta['landscape'] = fanarttv_data['landscape']
        meta['discart'] = fanarttv_data['discart']
        meta['fanart_added'] = True
    else:
        meta['banner'] = xbmc.translatePath(os.path.join(addon_dir, "resources", "default_images", "tikimeta_blank_banner.png"))
        meta['clearart'] = ''
        meta['clearlogo'] = ''
        meta['landscape'] = ''
        meta['discart'] = ''
        meta['fanart_added'] = False
    if kyradb_data:
        meta['gif_poster'] = kyradb_data['gif_poster']
        meta['kyradb_added'] = True
    else:
        meta['gif_poster'] = ''
        meta['kyradb_added'] = False
    meta['rating'] = data['vote_average'] if 'vote_average' in data else ''
    try: meta['genre'] = ', '.join([item['name'] for item in data['genres']])
    except: meta['genre'] == []
    meta['plot'] = to_utf8(data['overview']) if 'overview' in data else ''
    meta['tagline'] = to_utf8(data['tagline']) if 'tagline' in data else ''
    meta['votes'] = data['vote_count'] if 'vote_count' in data else ''
    if db_type == 'movie':
        meta['mediatype'] = 'movie'
        meta['title'] = to_utf8(data['title'])
        try: meta['search_title'] = to_utf8(safe_string(remove_accents(data['title'])))
        except: meta['search_title'] = to_utf8(safe_string(data['title']))
        try: meta['original_title'] = to_utf8(safe_string(remove_accents(data['original_title'])))
        except: meta['original_title'] = to_utf8(safe_string(data['original_title']))
        try: meta['year'] = try_parse_int(data['release_date'].split('-')[0])
        except: meta['year'] = ''
        meta['duration'] = int(data['runtime'] * 60) if data.get('runtime') else ''
        if data.get('production_companies'): meta['studio'] = [item['name'] for item in data['production_companies']][0]
        if data.get('release_date'): meta['premiered'] = data['release_date']
    else:
        meta['mediatype'] = 'tvshow'
        meta['title'] = to_utf8(data['name'])
        try: meta['search_title'] = to_utf8(safe_string(remove_accents(data['name'])))
        except: meta['search_title'] = to_utf8(safe_string(data['name']))
        try: meta['original_title'] = to_utf8(safe_string(remove_accents(data['original_name'])))
        except: meta['original_title'] = to_utf8(safe_string(data['original_name']))
        meta['tvshowtitle'] = meta['title']
        try: meta['year'] = try_parse_int(data['first_air_date'].split('-')[0])
        except: meta['year'] = ''
        meta['premiered'] = data['first_air_date']
        meta['season_data'] = data['seasons']
        if tvdb_summary:
            meta['tvdb_summary'] = tvdb_summary
            meta['total_episodes'] = int(data['number_of_episodes'])
            meta['total_seasons'] = len([i for i in tvdb_summary['airedSeasons'] if not i == '0'])
        else:
            meta['tvdb_summary'] = {'airedEpisodes': data['number_of_episodes'], 'airedSeasons': [str(i['season_number']) for i in data['seasons']]}
            meta['total_episodes'] = data['number_of_episodes']
            meta['total_seasons'] = data['number_of_seasons']
        try: meta['duration'] = min(data['episode_run_time']) * 60 if 'episode_run_time' in data else ''
        except: meta['duration'] = 30
        if data.get('networks', None):
            try: meta['studio'] = [item['name'] for item in data['networks']][0]
            except: meta['studio'] = ''
    meta['rootname'] = '{0} ({1})'.format(meta['search_title'], meta['year'])
    if 'content_ratings' in data:
        for rat_info in data['content_ratings']['results']:
            if rat_info['iso_3166_1'] == 'US':
                meta['mpaa'] = rat_info['rating']
    if 'release_dates' in data:
        for rel_info in data['release_dates']['results']:
            if rel_info['iso_3166_1'] == 'US':
                meta['mpaa'] = rel_info['release_dates'][0]['certification']
    if 'credits' in data:
        if 'cast' in data['credits']:
            for cast_member in data['credits']['cast']:
                cast_thumb = ''
                if cast_member['profile_path']:
                    cast_thumb = 'http://image.tmdb.org/t/p/%s%s' % (data['image_resolution']['profile'], cast_member['profile_path'])
                meta['cast'].append({'name': cast_member['name'], 'role': cast_member['character'], 'thumbnail': cast_thumb})
        if 'crew' in data['credits']:
            for crew_member in data['credits']['crew']:
                cast_thumb = ''
                if crew_member['profile_path']:
                    cast_thumb = 'http://image.tmdb.org/t/p/%s%s' % (data['image_resolution']['profile'], crew_member['profile_path'])
                if crew_member['job'] in ['Author', 'Writer', 'Screenplay', 'Characters']:
                    writer.append(crew_member['name'])
                if crew_member['job'] == 'Director':
                    meta['director'] = crew_member['name']
            if writer: meta['writer'] = ', '.join(writer)
    if 'videos' in data:
        meta['all_trailers'] = data['videos']['results']
        for video in data['videos']['results']:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer' or video['type'] == 'Teaser':
                meta['trailer'] = 'plugin://plugin.video.youtube/play/?video_id=%s' % video['key']
                break
    return meta

def buildSeasonsMeta(data, seasons, tmdb_data, image_resolution, use_tmdb=False):
    seasons = sorted([int(i) for i in seasons])
    meta = []
    for i in seasons:
        season_info = {}
        season_info['poster_path'] = None
        season_info['overview'] = ''
        season_info['name'] = ''
        season_info['season_number'] = i
        if use_tmdb:
            tmdb_info = [d['episode_info'] for d in data if d['season'] == i][0]
            season_info['use_tmdb'] = True
            season_info['episodes_data'] = tmdb_info
            season_info['episode_count'] = len(tmdb_info)
        else:
            episodes = [d for d in data if d['airedSeason'] == i]
            season_info['episodes_data'] = episodes
            season_info['episode_count'] = len(episodes)
        try: season_info['poster_path'] = ["http://image.tmdb.org/t/p/%s%s" % (image_resolution['poster'], p['poster_path']) for p in tmdb_data if p['season_number'] == i and p['poster_path'] is not None][0]
        except: pass
        try: season_info['overview'] = [p['overview'] for p in tmdb_data if p['season_number'] == i][0]
        except: pass
        try: season_info['name'] = [p['name'] for p in tmdb_data if p['season_number'] == i][0]
        except: pass
        meta.append(season_info)
    return meta

def buildEpisodesMeta(data, image_resolution, use_tmdb=False):
    meta = []
    if use_tmdb:
        for i in data:
            episode_info = {}
            writer = []
            episode_info['writer'] = ''
            episode_info['director'] = ''
            if 'crew' in data:
                for crew_member in data['crew']:
                    if crew_member['job'] in ['Author', 'Writer', 'Screenplay', 'Characters']:
                        writer.append(crew_member['name'])
                    if crew_member['job'] == 'Director':
                        episode_info['director'] = crew_member['name']
                if writer: episode_info['writer'] = ', '.join(writer)
            episode_info['mediatype'] = 'episode'
            episode_info['title'] = i['name']
            episode_info['plot'] = i['overview']
            episode_info['premiered'] = i['air_date']
            episode_info['season'] = i['season_number']
            episode_info['episode'] = i['episode_number']
            if i.get('still_path', None) is not None:
                episode_info['thumb'] = 'http://image.tmdb.org/t/p/%s%s' % (image_resolution['still'], i['still_path'])
            else: episode_info['thumb'] = None
            episode_info['rating'] = i['vote_average']
            episode_info['votes'] = i['vote_count']
            episode_info['guest_stars'] = []
            meta.append(episode_info)
    else:
        for i in data:
            episode_info = {}
            episode_info['writer'] = ''
            episode_info['director'] = ''
            episode_info['mediatype'] = 'episode'
            episode_info['title'] = i['episodeName']
            episode_info['plot'] = i['overview']
            episode_info['premiered'] = i['firstAired']
            episode_info['season'] = i['airedSeason']
            episode_info['episode'] = i['airedEpisodeNumber']
            episode_info['thumb'] = 'https://www.thetvdb.com/banners/%s' % i['filename'] if 'episodes' in i['filename'] else None
            episode_info['rating'] = i['siteRating']
            episode_info['votes'] = i['siteRatingCount']
            episode_info['writer'] = ', '.join(i['writers'])
            episode_info['director'] = ', '.join(i['directors'])
            episode_info['guest_stars'] = i['guestStars']
            meta.append(episode_info)
    return meta

