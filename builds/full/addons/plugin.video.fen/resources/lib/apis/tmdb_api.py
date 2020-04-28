# -*- coding: utf-8 -*-
import xbmcaddon
import requests, time
from modules.fen_cache import cache_object
from modules.settings import tmdb_api_check
# from modules.utils import logger

tmdb_api = tmdb_api_check()

def tmdb_keyword_id(query):
    string = "%s_%s" % ('tmdb_keyword_id', query)
    url = 'https://api.themoviedb.org/3/search/keyword?api_key=%s&query=%s' % (tmdb_api, query)
    return cache_object(get_tmdb, string, url, expiration=168)

def tmdb_company_id(query):
    string = "%s_%s" % ('tmdb_company_id', query)
    url = 'https://api.themoviedb.org/3/search/company?api_key=%s&query=%s' % (tmdb_api, query)
    return cache_object(get_tmdb, string, url, expiration=168)

def tmdb_movies_discover(query, page_no):
    string = query % page_no
    url = query % page_no
    return cache_object(get_tmdb, string, url)

def tmdb_movies_title_year(title, year=None):
    if year:
        string = "%s_%s_%s" % ('tmdb_movies_title_year', title, year)
        url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&year=%s' % (tmdb_api, title, year)
    else:
        string = "%s_%s" % ('tmdb_movies_title_year', title)
        url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s' % (tmdb_api, title)
    return cache_object(get_tmdb, string, url, expiration=672) # 1 month

def tmdb_movies_popular(page_no):
    string = "%s_%s" % ('tmdb_movies_popular', page_no)
    url = 'https://api.themoviedb.org/3/movie/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_blockbusters(page_no):
    string = "%s_%s" % ('tmdb_movies_blockbusters', page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=revenue.desc&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_in_theaters(page_no):
    string = "%s_%s" % ('tmdb_movies_in_theaters', page_no)
    url = 'https://api.themoviedb.org/3/movie/now_playing?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_premieres(page_no):
    current_date, previous_date = get_dates(31, reverse=True)
    string = "%s_%s" % ('tmdb_movies_premieres', page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=1|2|3&page=%s' % (tmdb_api, previous_date, current_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_latest_releases(page_no):
    current_date, previous_date = get_dates(31, reverse=True)
    string = "%s_%s" % ('tmdb_movies_latest_releases', page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=4|5&page=%s' % (tmdb_api, previous_date, current_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_top_rated(page_no):
    string = "%s_%s" % ('tmdb_movies_top_rated', page_no)
    url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_upcoming(page_no):
    current_date, future_date = get_dates(31, reverse=False)
    string = "%s_%s" % ('tmdb_movies_upcoming', page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=3|2|1&page=%s' % (tmdb_api, current_date, future_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_genres(genre_id, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_genres', genre_id, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&with_genres=%s&sort_by=popularity.desc&page=%s' % (tmdb_api, genre_id, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_genres_by_year(genre_id, year, page_no):
    string = "%s_%s_%s_%s" % ('tmdb_movies_genres_by_year', genre_id, year, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&with_genres=%s&sort_by=popularity.desc&primary_release_year=%s&page=%s' % (tmdb_api, genre_id, year, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_languages(language, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_languages', language, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&with_original_language=%s&page=%s' % (tmdb_api, language, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_certifications(certification, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_certifications', certification, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&certification_country=US&certification=%s&page=%s' % (tmdb_api, certification, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_year(year, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_year', year, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&certification_country=US&primary_release_year=%s&page=%s' % (tmdb_api, year, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_similar(tmdb_id, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_similar', tmdb_id, page_no)
    url = 'https://api.themoviedb.org/3/movie/%s/similar?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_recommendations(tmdb_id, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_recommendations', tmdb_id, page_no)
    url = 'https://api.themoviedb.org/3/movie/%s/recommendations?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_search(term, page_no):
    from modules.history import add_to_search_history
    add_to_search_history(term, 'movie_queries')
    string = "%s_%s_%s" % ('tmdb_movies_search', term, page_no)
    url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=%s' % (tmdb_api, term, page_no)
    return cache_object(get_tmdb, string, url, expiration=4)

def tmdb_movies_reviews(tmdb_id):
    string = "%s_%s" % ('tmdb_movies_reviews', tmdb_id)
    url = 'https://api.themoviedb.org/3/movie/%s/reviews?api_key=%s' % (tmdb_id, tmdb_api)
    return cache_object(get_tmdb, string, url, expiration=4)

def tmdb_movies_actor_roles(actor_id):
    string = "%s_%s" % ('tmdb_movies_actor_roles', actor_id)
    url = 'https://api.themoviedb.org/3/person/%s/movie_credits?api_key=%s&language=en-US' % (int(actor_id), tmdb_api)
    return cache_object(get_tmdb, string, url, expiration=4)['cast']

def tmdb_people_info(query):
    string = "%s_%s" % ('tmdb_people_info', query)
    url = 'https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s&page=1' % (tmdb_api, query)
    return cache_object(get_tmdb, string, url, expiration=4)['results']

def tmdb_tv_discover(query, page_no):
    string = query % page_no
    url = query % page_no
    return cache_object(get_tmdb, string, url)

def tmdb_tv_title_year(title, year=None):
    if year:
        string = "%s_%s_%s" % ('tmdb_tv_title_year', title, year)
        url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&query=%s&first_air_date_year=%s&language=en-US' % (tmdb_api, title, year)
    else:
        string = "%s_%s" % ('tmdb_tv_title_year', title)
        url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&query=%s&language=en-US' % (tmdb_api, title)
    return cache_object(get_tmdb, string, url, expiration=672) # 1 month

def tmdb_tv_popular(page_no):
    string = "%s_%s" % ('tmdb_tv_popular', page_no)
    url = 'https://api.themoviedb.org/3/tv/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_premieres(page_no):
    current_date, previous_date = get_dates(31, reverse=True)
    string = "%s_%s" % ('tmdb_tv_premieres', page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' % (tmdb_api, previous_date, current_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_upcoming(page_no):
    current_date, future_date = get_dates(31, reverse=False)
    string = "%s_%s" % ('tmdb_tv_upcoming', page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' % (tmdb_api, current_date, future_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_top_rated(page_no):
    string = "%s_%s" % ('tmdb_tv_top_rated', page_no)
    url = 'https://api.themoviedb.org/3/tv/top_rated?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_airing_today(page_no):
    string = "%s_%s" % ('tmdb_tv_airing_today', page_no)
    url = 'https://api.themoviedb.org/3/tv/airing_today?api_key=%s&timezone=America/Edmonton&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url, expiration=24)

def tmdb_tv_on_the_air(page_no):
    string = "%s_%s" % ('tmdb_tv_on_the_air', page_no)
    url = 'https://api.themoviedb.org/3/tv/on_the_air?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_genres(genre_id, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_genres', genre_id, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&with_genres=%s&sort_by=popularity.desc&include_null_first_air_dates=false&page=%s' % (tmdb_api, genre_id, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_genres_by_year(genre_id, year, page_no):
    string = "%s_%s_%s_%s" % ('tmdb_tv_genres_by_year', genre_id, year, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&with_genres=%s&first_air_date_year=%s&sort_by=popularity.desc&include_null_first_air_dates=false&page=%s' % (tmdb_api, genre_id, year, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_languages(language, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_languages', language, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language=%s&page=%s' % (tmdb_api, language, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_year(year, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_year', year, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&first_air_date_year=%s&page=%s' % (tmdb_api, year, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_networks(network_id, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_networks', network_id, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&with_networks=%s&page=%s' % (tmdb_api, network_id, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_similar(tmdb_id, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_similar', tmdb_id, page_no)
    url = 'https://api.themoviedb.org/3/tv/%s/similar?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_recommendations(tmdb_id, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_recommendations', tmdb_id, page_no)
    url = 'https://api.themoviedb.org/3/tv/%s/recommendations?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_actor_roles(actor_id):
    string = "%s_%s" % ('tmdb_tv_actor_roles', actor_id)
    url = 'https://api.themoviedb.org/3/person/%s/tv_credits?api_key=%s&language=en-US' % (int(actor_id), tmdb_api)
    return cache_object(get_tmdb, string, url, expiration=4)['cast']

def tmdb_tv_search(term, page_no):
    from modules.history import add_to_search_history
    add_to_search_history(term, 'tvshow_queries')
    string = "%s_%s_%s" % ('tmdb_tv_search', term, page_no)
    url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&language=en-US&query=%s&page=%s' % (tmdb_api, term, page_no)
    return cache_object(get_tmdb, string, url, expiration=4)

def tmdb_popular_people(page_no):
    string = "%s_%s" % ('tmdb_popular_people', page_no)
    url = 'https://api.themoviedb.org/3/person/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_people_pictures(actor_id):
    string = "%s_%s" % ('tmdb_images_person', actor_id)
    url = 'https://api.themoviedb.org/3/person/%s/images?api_key=%s' % (actor_id, tmdb_api)
    return cache_object(get_tmdb, string, url)

def tmdb_people_biography(actor_id, language=None):
    if not language:
        from tikimeta.utils import get_language
        language = get_language()
    string = "%s_%s_%s" % ('tmdb_people_biography', actor_id, language)
    url = 'https://api.themoviedb.org/3/person/%s?api_key=%s&language=%s' % (actor_id, tmdb_api, language)
    return cache_object(get_tmdb, string, url)

def get_dates(days, reverse=True):
    import datetime
    current_date = datetime.date.today()
    if reverse: new_date = (current_date - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    else: new_date = (current_date + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    return str(current_date), new_date

def get_tmdb(url):
    try:
        try: response = requests.get(url)
        except requests.exceptions.SSLError: response = requests.get(url, verify=False)
    except requests.exceptions.ConnectionError: return
    if '200' in str(response): return response
    elif 'Retry-After' in response.headers:
        timeout = response.headers['Retry-After']
        time.sleep(int(timeout) + 1)
        return get_tmdb(url)
    else: return
