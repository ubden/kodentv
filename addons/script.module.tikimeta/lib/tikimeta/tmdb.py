# -*- coding: utf-8 -*-

import xbmcaddon
import requests
from time import sleep
from tikimeta.metacache import cache_function
# from tikimeta.utils import logger


def tmdbMovies(tmdb_id, language, tmdb_api=None):
    if not tmdb_api:
        from tikimeta.utils import tmdbApi
        tmdb_api = tmdbApi()
    url = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=external_ids,videos,credits,release_dates' % (tmdb_id, tmdb_api, language)
    return getTmdb(url).json()

def tmdbMoviesExternalID(external_source, external_id, tmdb_api=None):
    if not tmdb_api:
        from tikimeta.utils import tmdbApi
        tmdb_api = tmdbApi()
    string = "%s_%s_%s" % ('tmdbMoviesExternalID', external_source, external_id)
    url = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=%s' % (external_id, tmdb_api, external_source)
    return cache_function(getTmdb, string, url, 672)['movie_results'][0]

def tmdbMoviesTitleYear(title, year, tmdb_api=None):
    if not tmdb_api:
        from tikimeta.utils import tmdbApi
        tmdb_api = tmdbApi()
    string = "%s_%s_%s" % ('tmdbMoviesTitleYear', title, year)
    url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&query=%s&year=%s&page=%s' % (tmdb_api, title, year)
    result = cache_function(string, url, 672)
    return result['results'][0]

def tmdbTVShows(tmdb_id, language, tmdb_api=None):
    if not tmdb_api:
        from tikimeta.utils import tmdbApi
        tmdb_api = tmdbApi()
    url = 'https://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=external_ids,videos,credits,content_ratings' % (tmdb_id, tmdb_api, language)
    return getTmdb(url).json()

def tmdbTVShowsExternalID(external_source, external_id, tmdb_api=None):
    if not tmdb_api:
        from tikimeta.utils import tmdbApi
        tmdb_api = tmdbApi()
    string = "%s_%s_%s" % ('tmdbTVShowsExternalID', external_source, external_id)
    url = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=%s' % (external_id, tmdb_api, external_source)
    return cache_function(getTmdb, string, url, 672)['tv_results'][0]

def tmdbTVShowsTitleYear(title, year, tmdb_api=None):
    if not tmdb_api:
        from tikimeta.utils import tmdbApi
        tmdb_api = tmdbApi()
    string = "%s_%s_%s" % ('tmdbTVShowsTitleYear', title, year)
    url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&query=%s&first_air_date_year=%s' % (tmdb_api, title, year)
    return cache_function(getTmdb, string, url, 672)['results'][0]

def tmdbSeasonEpisodes(tmdb_id, season_no, language, tmdb_api=None):
    if not tmdb_api:
        from tikimeta.utils import tmdbApi
        tmdb_api = tmdbApi()
    string = "%s_%s_%s" % ('tmdbSeasonEpisodes', tmdb_id, season_no)
    url = 'https://api.themoviedb.org/3/tv/%s/season/%s?api_key=%s&language=%s&append_to_response=credits' % (tmdb_id, season_no, tmdb_api, language)
    return cache_function(getTmdb, string, url, 96)

def getTmdb(url):
    try:
        try: response = requests.get(url)
        except requests.exceptions.SSLError: response = requests.get(url, verify=False)
    except requests.exceptions.ConnectionError: return
    if '200' in str(response): return response
    elif 'Retry-After' in response.headers:
        timeout = response.headers['Retry-After']
        sleep(int(timeout) + 1)
        return getTmdb(url)
    else: return

