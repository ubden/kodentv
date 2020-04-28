
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import re
import datetime
from modules.fen_cache import cache_object
from modules.utils import regex_from_to
# from modules.utils import logger

base_url = 'http://www.imdb.com/'
# watchlist = 'user/ur%s/watchlist?sort=%s' % (self.imdb_user, sort)

# def imdb_movies_new(page_no):
#     string = "%s_%s" % ('imdb_movies_new', page_no)
#     start = get_start(page_no)
#     url = base_url % 'feature,tv_movie&num_votes=1000,&production_status=released&release_date=date[365],date[90]&sort=moviemeter,asc&count=20&start=%s&ref_=adv_nxt' % start
#     return cache_object(get_imdb, string, url, False)

# def imdb_movies_languages(lang, page_no):
#     string = "%s_%s_%s" % ('imdb_movies_languages', lang, page_no)
#     start = get_start(page_no)
#     url = base_url % 'feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=20&start=%s&ref_=adv_nxt' % (lang, start)
#     return cache_object(get_imdb, string, url, False)

def imdb_movies_oscar_winners(page_no):
    string = "%s_%s" % ('imdb_movies_oscar_winners', page_no)
    start = get_start(page_no)
    url = base_url + 'search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=20&start=%s&ref_=adv_nxt' % start
    return cache_object(get_imdb, string, url, False)

# def imdb_tv_new(page_no):
#     string = "%s_%s" % ('imdb_tv_new', page_no)
#     start = get_start(page_no)
#     url = base_url % 'tv_series,mini_series&languages=en&num_votes=100,&release_date=date[60],date[0]&sort=release_date,desc&count=20&start=%s&ref_=adv_nxt' % start
#     return cache_object(get_imdb, string, url, False)

# def imdb_tv_languages(lang, page_no):
#     string = "%s_%s_%s" % ('imdb_tv_languages', lang, page_no)
#     start = get_start(page_no)
#     url = base_url % 'tv_series,mini_series&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=20&start=%s&ref_=adv_nxt' % (lang, start)
#     return cache_object(get_imdb, string, url, False)

def get_start(page_no):
    return (str(((int(page_no)-1)*20)+1) if page_no > 1 else '1')

def get_imdb(url):
    try:
        date_time = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        for i in re.findall('date\[(\d+)\]', url):
            url = url.replace('date[%s]' % i, (date_time - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        result = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
        return [regex_from_to(str(item.h3.a), 'title/', '/') for item in result]
    except: return


