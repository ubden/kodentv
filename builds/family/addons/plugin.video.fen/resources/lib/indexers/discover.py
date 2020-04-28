import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, sys
try: from urllib import urlencode
except ImportError: from urllib.parse import urlencode
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
import json
from modules.nav_utils import build_url, setView
from modules.utils import to_utf8
from modules import settings
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])

tmdb_api = settings.tmdb_api_check()
icon_directory = settings.get_theme()
dialog = xbmcgui.Dialog()
window = xbmcgui.Window(10000)

class Discover:
    def __init__(self, db_type=None):
        self.view = 'view.main'
        self.icon = os.path.join(icon_directory, 'discover.png')
        self.fanart = os.path.join(addon_dir, 'fanart.png')
        self.db_type = db_type
        if self.db_type: self.window_id = 'FEN_%s_discover_params' % self.db_type.upper()
        else: self.window_id = ''
        try: self.discover_params = json.loads(window.getProperty(self.window_id))
        except: self.discover_params = {}

    def movie(self):
        self._set_default_params('movie')
        names = self.discover_params['search_name']
        self._add_dir({'mode': 'discover._clear_property', 'db_type': 'movie', 'list_name': '[B]CLEAR ALL FILTERS[/B]'})
        if not 'recommended' in names: self._add_dir({'mode': 'discover.similar_recommended', 'db_type': 'movie', 'key': 'similar', 'list_name': '[B]Discover Similar:[/B]  [I]%s[/I]' % names.get('similar', '')})
        if not 'similar' in names: self._add_dir({'mode': 'discover.similar_recommended', 'db_type': 'movie', 'key': 'recommended', 'list_name': '[B]Discover Recommended:[/B]  [I]%s[/I]' % names.get('recommended', '')})
        if not any(i in names for i in ['similar', 'recommended']):
            self._add_dir({'mode': 'discover.year_start', 'db_type': 'movie', 'list_name': '[B]Year Start:[/B]  [I]%s[/I]' % names.get('year_start', '')})
            self._add_dir({'mode': 'discover.year_end', 'db_type': 'movie', 'list_name': '[B]Year End:[/B]  [I]%s[/I]' % names.get('year_end', '')})
            self._add_dir({'mode': 'discover.include_genres', 'db_type': 'movie', 'list_name': '[B]Include Genres:[/B]  [I]%s[/I]' % names.get('include_genres', '')})
            self._add_dir({'mode': 'discover.exclude_genres', 'db_type': 'movie', 'list_name': '[B]Exclude Genres:[/B]  [I]%s[/I]' % names.get('exclude_genres', '')})
            self._add_dir({'mode': 'discover.include_keywords', 'db_type': 'movie', 'list_name': '[B]Include Keywords:[/B]  [I]%s[/I]' % names.get('include_keywords', '')})
            self._add_dir({'mode': 'discover.exclude_keywords', 'db_type': 'movie', 'list_name': '[B]Exclude Keywords:[/B]  [I]%s[/I]' % names.get('exclude_keywords', '')})
            self._add_dir({'mode': 'discover.language', 'db_type': 'movie', 'list_name': '[B]Language:[/B]  [I]%s[/I]' % names.get('language', '')})
            self._add_dir({'mode': 'discover.region', 'db_type': 'movie', 'list_name': '[B]Region:[/B]  [I]%s[/I]' % names.get('region', '')})
            self._add_dir({'mode': 'discover.companies', 'db_type': 'movie', 'list_name': '[B]Companies:[/B]  [I]%s[/I]' % names.get('companies', '')})
            self._add_dir({'mode': 'discover.certification', 'db_type': 'movie', 'list_name': '[B]Certification:[/B]  [I]%s[/I]' % names.get('certification', '')})
            self._add_dir({'mode': 'discover.rating', 'db_type': 'movie', 'list_name': '[B]Minimum Rating:[/B]  [I]%s[/I]' % names.get('rating', '')})
            self._add_dir({'mode': 'discover.rating_votes', 'db_type': 'movie', 'list_name': '[B]Minimum Number of Votes:[/B]  [I]%s[/I]' % names.get('rating_votes', '')})
            self._add_dir({'mode': 'discover.cast', 'db_type': 'movie', 'list_name': '[B]Includes Cast Member:[/B]  [I]%s[/I]' % names.get('cast', '')})
            self._add_dir({'mode': 'discover.sort_by', 'db_type': 'movie', 'list_name': '[B]Sort By:[/B]  [I]%s[/I]' % names.get('sort_by', '')})
            self._add_dir({'mode': 'discover.adult', 'db_type': 'movie', 'list_name': '[B]Includes Adult:[/B]  [I]%s[/I]' % names.get('adult', 'False')})
        self._add_defaults()
        self._end_directory()

    def tvshow(self):
        self._set_default_params('tvshow')
        names = self.discover_params['search_name']
        self._add_dir({'mode': 'discover._clear_property', 'db_type': 'tvshow', 'list_name': '[B]CLEAR ALL FILTERS[/B]'})
        if not 'recommended' in names: self._add_dir({'mode': 'discover.similar_recommended', 'db_type': 'tvshow', 'key': 'similar', 'list_name': '[B]Discover Similar:[/B]  [I]%s[/I]' % names.get('similar', '')})
        if not 'similar' in names: self._add_dir({'mode': 'discover.similar_recommended', 'db_type': 'tvshow', 'key': 'recommended', 'list_name': '[B]Discover Recommended:[/B]  [I]%s[/I]' % names.get('recommended', '')})
        if not any(i in names for i in ['similar', 'recommended']):
            self._add_dir({'mode': 'discover.year_start', 'db_type': 'tvshow', 'list_name': '[B]Year Start:[/B]  %s' % names.get('year_start', '')})
            self._add_dir({'mode': 'discover.year_end', 'db_type': 'tvshow', 'list_name': '[B]Year End:[/B]  %s' % names.get('year_end', '')})
            self._add_dir({'mode': 'discover.include_genres', 'db_type': 'tvshow', 'list_name': '[B]Include Genres:[/B]  %s' % names.get('include_genres', '')})
            self._add_dir({'mode': 'discover.exclude_genres', 'db_type': 'tvshow', 'list_name': '[B]Exclude Genres:[/B]  %s' % names.get('exclude_genres', '')})
            self._add_dir({'mode': 'discover.include_keywords', 'db_type': 'tvshow', 'list_name': '[B]Include Keywords:[/B]  [I]%s[/I]' % names.get('include_keywords', '')})
            self._add_dir({'mode': 'discover.exclude_keywords', 'db_type': 'tvshow', 'list_name': '[B]Exclude Keywords:[/B]  [I]%s[/I]' % names.get('exclude_keywords', '')})
            self._add_dir({'mode': 'discover.language', 'db_type': 'tvshow', 'list_name': '[B]Language:[/B]  %s' % names.get('language', '')})
            self._add_dir({'mode': 'discover.network', 'db_type': 'tvshow', 'list_name': '[B]Network:[/B]  %s' % names.get('network', '')})
            self._add_dir({'mode': 'discover.rating', 'db_type': 'tvshow', 'list_name': '[B]Minimum Rating:[/B]  %s' % names.get('rating', '')})
            self._add_dir({'mode': 'discover.rating_votes', 'db_type': 'tvshow', 'list_name': '[B]Minimum Number of Votes:[/B]  %s' % names.get('rating_votes', '')})
            self._add_dir({'mode': 'discover.sort_by', 'db_type': 'tvshow', 'list_name': '[B]Sort By:[/B]  [I]%s[/I]' % names.get('sort_by', '')})
        self._add_defaults()
        self._end_directory()

    def similar_recommended(self, key):
        if self._action(key) in ('clear', None): return
        title = dialog.input("FEN DISCOVER: Enter Title").lower()
        if not title: return
        if self.db_type == 'movie':
            from apis.tmdb_api import tmdb_movies_title_year as function
        else:
            from apis.tmdb_api import tmdb_tv_title_year as function
        year = dialog.input("Enter Year (Optional)", type=xbmcgui.INPUT_NUMERIC)
        results = function(title, year)['results']
        if len(results) == 0: return dialog.ok('FEN DISCOVER', 'No Matching Titles to Select.', 'Please Try a Different Search Term.')
        choice_list = []
        for item in results:
            title = item['title'] if self.db_type == 'movie' else item['name']
            try: year = item['release_date'].split('-')[0] if self.db_type == 'movie' else item['first_air_date'].split('-')[0]
            except: year = ''
            if year: rootname = '%s (%s)' % (title, year)
            else: rootname = title
            line1 = rootname
            line2 = '[I]%s[/I]' % item['overview']
            icon = 'http://image.tmdb.org/t/p/w92%s' % item['poster_path'] if item.get('poster_path') else xbmc.translatePath(__addon__.getAddonInfo('icon'))
            listitem = xbmcgui.ListItem(line1, line2)
            listitem.setArt({'icon': icon})
            listitem.setProperty('rootname', rootname)
            listitem.setProperty('tmdb_id', str(item['id']))
            choice_list.append(listitem)
        chosen_title = dialog.select("FEN DISCOVER: Select Correct Title", choice_list, useDetails=True)
        if chosen_title < 0: return
        rootname = choice_list[chosen_title].getProperty('rootname')
        tmdb_id = choice_list[chosen_title].getProperty('tmdb_id')
        values = (tmdb_id, rootname)
        self._process(key, values)

    def include_keywords(self):
        key = 'include_keywords'
        if self._action(key) in ('clear', None): return
        current_key_ids = self.discover_params['search_string'].get(key, [])
        current_keywords = self.discover_params['search_name'].get(key, [])
        if not isinstance(current_key_ids, list):
            current_key_ids = current_key_ids.replace('&with_keywords=', '').split(', ')
        if not isinstance(current_keywords, list):
            current_keywords = current_keywords.split(', ')
        keyword = dialog.input("Enter Keyword to Search")
        if keyword:
            from apis.tmdb_api import tmdb_keyword_id
            try:
                result = tmdb_keyword_id(keyword)['results']
                keywords_choice = self._multiselect_dialog('FEN DISCOVER: Choose Included Keywords', [i['name'].upper() for i in result], result)
                if keywords_choice:
                    for i in keywords_choice:
                        current_key_ids.append(str(i['id']))
                        current_keywords.append(i['name'].upper())
            except: pass
            values = ('&with_keywords=%s' % ','.join([i for i in current_key_ids]), ', '.join([i for i in current_keywords]))
            self._process(key, values)

    def exclude_keywords(self):
        key = 'exclude_keywords'
        if self._action(key) in ('clear', None): return
        current_key_ids = self.discover_params['search_string'].get(key, [])
        current_keywords = self.discover_params['search_name'].get(key, [])
        if not isinstance(current_key_ids, list):
            current_key_ids = current_key_ids.split(', ')
        if not isinstance(current_keywords, list):
            current_keywords = current_keywords.split(', ')
        keyword = dialog.input("Enter Keyword to Search")
        if keyword:
            from apis.tmdb_api import tmdb_keyword_id
            try:
                result = tmdb_keyword_id(keyword)['results']
                keywords_choice = self._multiselect_dialog('FEN DISCOVER: Choose Excluded Keywords', [i['name'].upper() for i in result], result)
                if keywords_choice:
                    for i in keywords_choice:
                        current_key_ids.append(str(i['id']))
                        current_keywords.append(i['name'].upper())
            except: pass
            values = ('&without_keywords=%s' % ','.join([i for i in current_key_ids]), ', '.join([i for i in current_keywords]))
            self._process(key, values)

    def year_start(self):
        key = 'year_start'
        if self._action(key) in ('clear', None): return
        from modules.nav_utils import years
        years = years()
        years_list = [str(i) for i in years]
        year_start = self._selection_dialog(years_list, years, 'FEN DISCOVER: Choose Start Year')
        if year_start:
            if self.discover_params['db_type'] == 'movie':
                value = 'primary_release_date.gte'
            else:
                value = 'first_air_date.gte'
            values = ('&%s=%s-01-01' % (value, str(year_start)), str(year_start))
            self._process(key, values)

    def year_end(self):
        key = 'year_end'
        if self._action(key) in ('clear', None): return
        from modules.nav_utils import years
        years = years()
        years_list = [str(i) for i in years]
        year_end = self._selection_dialog(years_list, years, 'FEN DISCOVER: Choose End Year')
        if year_end:
            if self.discover_params['db_type'] == 'movie':
                value = 'primary_release_date.lte'
            else:
                value = 'first_air_date.lte'
            values = ('&%s=%s-12-31' % (value, str(year_end)), str(year_end))
            self._process(key, values)

    def include_genres(self):
        key = 'include_genres'
        if self._action(key) in ('clear', None): return
        if self.discover_params['db_type'] == 'movie':
            from modules.nav_utils import movie_genres as genres
        else:
            from modules.nav_utils import tvshow_genres as genres
        genre_list = [(k, v[0]) for k,v in sorted(genres.items())]
        genres_choice = self._multiselect_dialog('FEN DISCOVER: Choose Included Genres', [i[0] for i in genre_list], genre_list)
        if genres_choice:
            genre_ids = ','.join([i[1] for i in genres_choice])
            genre_names = ', '.join([i[0] for i in genres_choice])
            values = ('&with_genres=%s' % genre_ids, genre_names)
            self._process(key, values)

    def exclude_genres(self):
        key = 'exclude_genres'
        if self._action(key) in ('clear', None): return
        if self.discover_params['db_type'] == 'movie':
            from modules.nav_utils import movie_genres as genres
        else:
            from modules.nav_utils import tvshow_genres as genres
        genre_list = [(k, v[0]) for k,v in sorted(genres.items())]
        genres_choice = self._multiselect_dialog('FEN DISCOVER: Choose Excluded Genres', [i[0] for i in genre_list], genre_list)
        if genres_choice:
            genre_ids = ','.join([i[1] for i in genres_choice])
            genre_names = ', '.join([i[0] for i in genres_choice])
            values = ('&without_genres=%s' % genre_ids, '/'.join(genre_names.split(', ')))
            self._process(key, values)

    def language(self):
        key = 'language'
        if self._action(key) in ('clear', None): return
        from modules.nav_utils import languages
        languages_list = [i[0] for i in languages]
        language = self._selection_dialog(languages_list, languages, 'FEN DISCOVER: Choose Language')
        if language:
            values = ('&with_original_language=%s' % str(language[1]), str(language[1]).upper())
            self._process(key, values)

    def region(self):
        key = 'region'
        if self._action(key) in ('clear', None): return
        from modules.nav_utils import regions
        region_names = [i['name'] for i in regions]
        region_codes = [i['code'] for i in regions]
        region = self._selection_dialog(region_names, region_codes, 'FEN DISCOVER: Choose Region')
        if region:
            region_name = [i['name'] for i in regions if i['code'] == region][0]
            values = ('&region=%s' % region, region_name)
            self._process(key, values)

    def rating(self):
        key = 'rating'
        if self._action(key) in ('clear', None): return
        ratings = [i for i in range(1,11)]
        ratings_list = [str(float(i)) for i in ratings]
        rating = self._selection_dialog(ratings_list, ratings, 'FEN DISCOVER: Choose Minimum Rating')
        if rating:
            values = ('&vote_average.gte=%s' % str(rating), str(float(rating)))
            self._process(key, values)

    def rating_votes(self):
        key = 'rating_votes'
        if self._action(key) in ('clear', None): return
        rating_votes = [i for i in range(0,1001,50)]
        rating_votes.pop(0)
        rating_votes.insert(0, 1)
        rating_votes_list = [str(i) for i in rating_votes]
        rating_votes = self._selection_dialog(rating_votes_list, rating_votes, 'FEN DISCOVER: Choose Minimum Number of Votes')
        if rating_votes:
            values = ('&vote_count.gte=%s' % str(rating_votes), str(rating_votes))
            self._process(key, values)

    def certification(self):
        key = 'certification'
        if self._action(key) in ('clear', None): return
        from modules.nav_utils import movie_certifications as certifications
        certifications_list = [i.upper() for i in certifications]
        certification = self._selection_dialog(certifications_list, certifications, 'FEN DISCOVER: Choose Certification')
        if certification:
            values = ('&certification_country=US&certification=%s' % certification, certification.upper())
            self._process(key, values)

    def cast(self):
        key = 'cast'
        if self._action(key) in ('clear', None): return
        from apis.tmdb_api import get_tmdb
        from modules.fen_cache import cache_object
        result = None
        actor_id = None
        search_name = None
        search_name = dialog.input('FEN DISCOVER: Enter Actor/Actress Name', type=xbmcgui.INPUT_ALPHANUM)
        if not search_name: return
        string = "%s_%s" % ('tmdb_movies_people_search_actor_data', search_name)
        url = 'https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s' % (tmdb_api, search_name)
        result = cache_object(get_tmdb, string, url, 4)
        result = result['results']
        if not result: return
        actor_list = []
        if len(result) > 1:
            for item in result:
                name = item['name']
                known_for_list = [i.get('title', 'NA') for i in item['known_for']]
                known_for_list = [i for i in known_for_list if not i == 'NA']
                known_for = '[I]%s[/I]' % ', '.join(known_for_list) if known_for_list else '[I]Movie Actor[/I]'
                listitem = xbmcgui.ListItem(name, known_for)
                listitem.setArt({'icon': 'http://image.tmdb.org/t/p/w185/%s' % item['profile_path']})
                listitem.setProperty('id', str(item['id']))
                listitem.setProperty('name', name)
                actor_list.append(listitem)
            selection = dialog.select("FEN DISCOVER: Select Correct Actor/Actress", actor_list, useDetails=True)
            if selection >= 0:
                actor_id = int(actor_list[selection].getProperty('id'))
                actor_name = actor_list[selection].getProperty('name')
            else:
                self._set_property()
        else:
            actor_id = [item['id'] for item in result][0]
            actor_name = [item['name'] for item in result][0]
        if actor_id:
            try: values = ('&with_cast=%s' % str(actor_id), actor_name.decode('ascii', 'ignore'))
            except: values = ('&with_cast=%s' % str(actor_id), actor_name)
            self._process(key, values)

    def network(self):
        key = 'network'
        if self._action(key) in ('clear', None): return
        from modules.nav_utils import networks
        network_list = []
        networks = sorted(networks, key=lambda k: k['name'])
        for item in networks:
            name = item['name']
            listitem = xbmcgui.ListItem(name, iconImage=item['logo'])
            listitem.setProperty('id', str(item['id']))
            listitem.setProperty('name', name)
            network_list.append(listitem)
        selection = dialog.select("FEN DISCOVER: Select Network", network_list, useDetails=True)
        if selection >= 0:
            network_id = int(network_list[selection].getProperty('id'))
            network_name = network_list[selection].getProperty('name')
            values = ('&with_networks=%s' % network_id, network_name)
            self._process(key, values)

    def companies(self):
        key = 'companies'
        if self._action(key) in ('clear', None): return
        current_company_ids = self.discover_params['search_string'].get(key, [])
        current_companies = self.discover_params['search_name'].get(key, [])
        if not isinstance(current_company_ids, list):
            current_company_ids = current_company_ids.replace('&with_companies=', '').split('|')
        if not isinstance(current_companies, list):
            current_companies = current_companies.split(', ')
        company = dialog.input("Enter Company to Search")
        if company:
            from apis.tmdb_api import tmdb_company_id
            try:
                result = tmdb_company_id(company)['results']
                company_choice = self._multiselect_dialog('FEN DISCOVER: Choose Included Companies', [i['name'].upper() for i in result], result)
                if company_choice:
                    for i in company_choice:
                        current_company_ids.append(str(i['id']))
                        current_companies.append(i['name'].upper())
            except: pass
            values = ('&with_companies=%s' % '|'.join([i for i in current_company_ids]), ', '.join([i for i in current_companies]))
            self._process(key, values)

    def sort_by(self):
        key = 'sort_by'
        if self._action(key) in ('clear', None): return
        if self.discover_params['db_type'] == 'movie':
            sort_by_list = self._movies_sort()
        else:
            sort_by_list = self._tvshows_sort()
        sort_by_value = self._selection_dialog([i[0] for i in sort_by_list], [i[1] for i in sort_by_list], 'FEN DISCOVER: Choose Sort By')
        if sort_by_value:
            sort_by_name = [i[0] for i in sort_by_list if i[1] == sort_by_value][0]
            values = (sort_by_value, sort_by_name)
            self._process(key, values)

    def adult(self):
        key = 'adult'
        include_adult = self._selection_dialog(('True', 'False'), ('true', 'false'), 'FEN DISCOVER: Choose Adult Titles Inclusion')
        if include_adult:
            values = ('&include_adult=%s' % include_adult, include_adult.capitalize())
            self._process(key, values)

    def export(self):
        try:
            db_type = self.discover_params['db_type']
            query = self.discover_params['final_string']
            name = self.discover_params['name']
            set_history(db_type, name, query)
            if db_type == 'movie':
                mode = 'build_movie_list'
                action = 'tmdb_movies_discover'
            else:
                mode = 'build_tvshow_list'
                action = 'tmdb_tv_discover'
            final_params = {'name': name, 'mode': mode, 'action': action, 'query': query, 'iconImage': self.icon}
            url_params = {'mode': 'navigator.adjust_main_lists', 'method': 'add_external',
                        'list_name': name, 'menu_item': json.dumps(final_params)}
            xbmc.executebuiltin('XBMC.RunPlugin(%s)' % self._build_url(url_params))
        except:
            from modules.nav_utils import notification
            notification('Please set some filters before exporting')

    def history(self, db_type=None, display=True):
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        cache_file = os.path.join(__addon_profile__, "fen_cache.db")
        db_type = db_type if db_type else self.db_type
        string = 'fen_discover_%s_%%' % self.db_type
        settings.check_database(cache_file)
        dbcon = database.connect(cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT id, data FROM fencache WHERE id LIKE ? ORDER BY rowid DESC", (string,))
        history = dbcur.fetchall()
        if not display: return [i[0] for i in history]
        data = [eval(i[1]) for i in history]
        for count, item in enumerate(data):
            try:
                cm = []
                data_id = history[count][0]
                name = item['name']
                url_params = {'mode': item['mode'], 'action': item['action'], 'query': item['query'],
                              'name': name, 'iconImage': self.icon}
                display = '%s | %s' % (count+1, name)
                url = build_url(url_params)
                remove_single_params = {'mode': 'discover.remove_from_history', 'data_id': data_id}
                remove_all_params = {'mode': 'discover.remove_all_history', 'db_type': db_type}
                export_params = {'mode': 'navigator.adjust_main_lists', 'method': 'add_external',
                                'list_name': name, 'menu_item': json.dumps(url_params)}
                listitem = xbmcgui.ListItem(display)
                listitem.setArt({'icon': self.icon, 'poster': self.icon, 'thumb': self.icon, 'fanart': self.fanart, 'banner': self.icon})
                cm.append(("[B]Export List[/B]",'XBMC.RunPlugin(%s)'% self._build_url(export_params)))
                cm.append(("[B]Remove From History[/B]",'XBMC.RunPlugin(%s)'% self._build_url(remove_single_params)))
                cm.append(("[B]Clear All %s History[/B]" % db_type.capitalize(),'XBMC.RunPlugin(%s)'% self._build_url(remove_all_params)))
                listitem.addContextMenuItems(cm)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder=True)
            except: pass
        self._end_directory()

    def remove_from_history(self, data_id=None):
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        from modules.nav_utils import notification
        display_notification = False
        if not data_id:
            params = dict(parse_qsl(sys.argv[2].replace('?','')))
            data_id = params['data_id']
            display_notification = True
        cache_file = os.path.join(__addon_profile__, "fen_cache.db")
        settings.check_database(cache_file)
        dbcon = database.connect(cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fencache WHERE id=?", (data_id,))
        dbcon.commit()
        window.clearProperty(data_id)
        xbmc.executebuiltin("Container.Refresh")
        if display_notification: notification('Result Removed from Discover History')

    def remove_all_history(self):
        from modules.nav_utils import notification
        if not dialog.yesno('Are you sure?','Fen will Clear Discover\'s %s History.' % self.db_type.upper()): return
        all_history = self.history(self.db_type, display=False)
        for item in all_history:
            self.remove_from_history(data_id=item)
        notification('Discover History Cleared')

    def help(self):
        heading = 'FEN DISCOVER: Help Dialog'
        text = self._help_text()
        read = dialog.textviewer(heading, text)

    def _set_default_params(self, db_type):
        if not 'db_type' in self.discover_params:
            self._clear_property()
            url_db_type = 'movie' if db_type == 'movie' else 'tv'
            param_db_type = 'Movies' if db_type == 'movie' else 'TV Shows'
            self.discover_params['db_type'] = db_type
            self.discover_params['search_string'] = {}
            self.discover_params['search_string']['base'] = 'https://api.themoviedb.org/3/discover/%s?api_key=%s&language=en-US&page=%s' % (url_db_type, tmdb_api, '%s')
            self.discover_params['search_string']['base_similar'] = 'https://api.themoviedb.org/3/%s/%s/similar?api_key=%s&language=en-US&page=%s' % (url_db_type, '%s', tmdb_api, '%s')
            self.discover_params['search_string']['base_recommended'] = 'https://api.themoviedb.org/3/%s/%s/recommendations?api_key=%s&language=en-US&page=%s' % (url_db_type, '%s', tmdb_api, '%s')
            self.discover_params['search_name'] = {'db_type': param_db_type}
            self._set_property()

    def _add_defaults(self):
        if self.discover_params['db_type'] == 'movie':
            mode = 'build_movie_list'
            action = 'tmdb_movies_discover'
        else:
            mode = 'build_tvshow_list'
            action = 'tmdb_tv_discover'
        name = self.discover_params.get('name', '...')
        query = self.discover_params.get('final_string', '')
        self._add_dir({'mode': mode, 'action': action, 'query': query, 'name': name, 'list_name': '[B]SAVE & BROWSE RESULTS FOR:[/B]  [I]%s[/I]' % name}, os.path.join(icon_directory, 'search.png'))
        self._add_dir({'mode': 'discover.export', 'db_type': self.db_type, 'list_name': '[B]EXPORT SEARCH:[/B]  [I]%s[/I]' % name}, os.path.join(icon_directory, 'nextpage.png'))

    def _action(self, key):
        dict_item = self.discover_params
        add_to_list = ('keyword', 'companies')
        action = 'Add to' if any(word in key for word in add_to_list) else 'Change'
        if key in dict_item['search_name']:
            action = self._selection_dialog(['%s Filter' % action.capitalize(),'Clear Filter'], (action, 'clear'), 'FEN DISCOVER: Filter Action')
        if action is None: return
        if action == 'clear':
            for k in ('search_string', 'search_name'): dict_item[k].pop(key, None)
            self._process()
        return action

    def _process(self, key=None, values=None):
        if key:
            self.discover_params['search_string'][key] = values[0]
            self.discover_params['search_name'][key] = values[1]
        self._build_string()
        self._build_name()
        self._set_property()

    def _clear_property(self):
        window.clearProperty(self.window_id)
        self.discover_params = {}

    def _set_property(self):
        return window.setProperty(self.window_id, json.dumps(self.discover_params))

    def _add_dir(self, params, icon=None):
        icon = self.icon if not icon else icon
        list_name = params.get('list_name', '')
        url = self._build_url(params)
        listitem = xbmcgui.ListItem(list_name)
        listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': self.fanart, 'banner': icon})
        xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=True)

    def _end_directory(self):
        xbmcplugin.setContent(__handle__, 'addons')
        xbmcplugin.endOfDirectory(__handle__)
        setView(self.view, 'addons')

    def _build_url(self, query):
        return __url__ + '?' + urlencode(to_utf8(query))

    def _selection_dialog(self, dialog_list, function_list, string):
        list_choose = dialog.select("%s" % string, dialog_list)
        if list_choose >= 0: return function_list[list_choose]
        else: return None

    def _multiselect_dialog(self, string, dialog_list, function_list=None, preselect= []):
        if not function_list: function_list = dialog_list
        list_choose = dialog.multiselect(string, dialog_list, preselect=preselect)
        if list_choose:
            return [function_list[i] for i in list_choose]
        else:
            return

    def _build_string(self):
        string_params = self.discover_params['search_string']
        if 'similar' in string_params:
            string = string_params['base_similar'] % (string_params['similar'], '%s')
            self.discover_params['final_string'] = string
            return
        if 'recommended' in string_params:
            string = string_params['base_recommended'] % (string_params['recommended'], '%s')
            self.discover_params['final_string'] = string
            return
        string = string_params['base']
        if 'year_start' in string_params:
            string += string_params['year_start']
        if 'year_end' in string_params:
            string += string_params['year_end']
        if 'include_genres' in string_params:
            string += string_params['include_genres']
        if 'exclude_genres' in string_params:
            string += string_params['exclude_genres']
        if 'include_keywords' in string_params:
            string += string_params['include_keywords']
        if 'exclude_keywords' in string_params:
            string += string_params['exclude_keywords']
        if 'companies' in string_params:
            string += string_params['companies']
        if 'language' in string_params:
            string += string_params['language']
        if 'region' in string_params:
            string += string_params['region']
        if 'rating' in string_params:
            string += string_params['rating']
        if 'rating_votes' in string_params:
            string += string_params['rating_votes']
        if 'certification' in string_params:
            string += string_params['certification']
        if 'cast' in string_params:
            string += string_params['cast']
        if 'network' in string_params:
            string += string_params['network']
        if 'adult' in string_params:
            string += string_params['adult']
        if 'sort_by' in string_params:
            string += string_params['sort_by']
        self.discover_params['final_string'] = string

    def _build_name(self):
        values = self.discover_params['search_name']
        name = '[B]%s[/B] ' % values['db_type']
        if 'similar' in values:
            name += '| Similar to %s' % values['similar']
            self.discover_params['name'] = name
            return
        if 'recommended' in values:
            name += '| Recommended based on %s' % values['recommended']
            self.discover_params['name'] = name
            return
        if 'year_start' in values:
            if 'year_end' in values and not values['year_start'] == values['year_end']:
                name += '| %s' % values['year_start']
            else:
                name += '| %s ' % values['year_start']
        if 'year_end' in values:
            if 'year_start' in values:
                if not values['year_start'] == values['year_end']:
                    name += '-%s ' % values['year_end']
            else:
                name += '| %s ' % values['year_end']
        if 'language' in values:
            name += '| %s ' % values['language']
        if 'region' in values:
            name += '| %s ' % values['region']
        if 'network' in values:
            name += '| %s ' % values['network']
        if 'include_genres' in values:
            name += '| %s ' % values['include_genres']
            if 'exclude_genres' in values:
                name += '(not %s) ' % values['exclude_genres']
        elif 'exclude_genres' in values:
            name += '| not %s ' % values['exclude_genres']
        if 'companies' in values:
            name += '| %s ' % values['companies']
        if 'certification' in values:
            name += '| %s ' % values['certification']
        if 'rating' in values:
            name += '| %s+ ' % values['rating']
            if 'rating_votes' in values:
                name += '(%s) ' % values['rating_votes']
        elif 'rating_votes' in values:
            name += '| %s+ votes ' % values['rating_votes']
        if 'cast' in values:
            name += '| with %s ' % values['cast']
        if 'include_keywords' in values:
            name += '| incl.words: %s ' % values['include_keywords']
        if 'exclude_keywords' in values:
            name += '| excl.words: %s ' % values['exclude_keywords']
        if 'sort_by' in values:
            name += '| %s ' % values['sort_by']
        if 'adult' in values:
            if values['adult'] == 'True': name += '| incl. Adult '
        self.discover_params['name'] = name

    def _movies_sort(self):
        return [
            ('Popularity (asc)', '&sort_by=popularity.asc'),
            ('Popularity (desc)', '&sort_by=popularity.desc'),
            ('Release Date (asc)', '&sort_by=primary_release_date.asc'),
            ('Release Date (desc)', '&sort_by=primary_release_date.desc'),
            ('Revenue (asc)', '&sort_by=revenue.asc'),
            ('Revenue (desc)', '&sort_by=revenue.desc'),
            ('Title (asc)', '&sort_by=original_title.asc'),
            ('Title (desc)', '&sort_by=original_title.desc'),
            ('Rating (asc)', '&sort_by=vote_average.asc'),
            ('Rating (desc)', '&sort_by=vote_average.desc')
                ]

    def _tvshows_sort(self):
        return [
            ('Popularity (asc)', '&sort_by=popularity.asc'),
            ('Popularity (desc)', '&sort_by=popularity.desc'),
            ('First Aired (asc)', '&sort_by=first_air_date.asc'),
            ('First Aired (desc)', '&sort_by=first_air_date.desc'),
            ('Rating (asc)', '&sort_by=vote_average.asc'),
            ('Rating (desc)', '&sort_by=vote_average.desc')
            ]

    def _help_text(self):
        text = '' \
        '*Select a category and assign a filter value. You only need to assign the values you wish ' \
        'to include in the search. e.g. If you don\'t need a certain actor included, then leave "Includes Cast Member" blank etc. ' \
        ' \n\n*Once you have filled in all the categories you need, hit "Save & Browse Results" to immediately browse the results. ' \
        '\n\n*Alternately, you can select "Export Search", give the search a name, and choose which of the main Fen lists you wish to save it to ' \
        'e.g. Root Menu or Movies or TV Shows. You can then browse that list whenever you want, without having to re-enter the ' \
        'different filters continuously.' \
        '\n\n*Fen will keep a history of the last 7 days of filtered lists you have made. Select "Discover: History" to re-browse these lists.' \
        '\n\n[B]EXAMPLE 1:[/B]' \
        '\n[I]You want to search for Comedy Action Movies made in the 1980\'s that are PG Rated.[/I]' \
        '\n    - Assign a "[B]Year Start[/B]" filter of "1980"' \
        '\n    - Assign a "[B]Year End[/B]" filter of "1989"' \
        '\n    - Assign a "[B]Include Genres[/B]" filter of "Action, Comedy"' \
        '\n    - Assign a "[B]Certification[/B]" filter of "PG"' \
        '\n    - Select "[B]Browse Results[/B]" to immediately see the results or "[B]Export List[/B]" to export the list to Fen Root Menu or Fen Movies Menu etc"' \
        '\n[B]Enjoy your 1980\'s Action/Comedy Family Movie Night!!![/B]' \
        '\n\n[B]You can also search for Similar or Recommended Titles![/B]' \
        '\n[B]EXAMPLE 2:[/B]' \
        '\n[I]You want to search for Movies Similar to Avengers Endgame.[/I]' \
        '\n    - Assign a "[B]Discover Similar[/B]" [B]Title[/B] of "Avengers Endgame"' \
        '\n    - Assign a "[B]Discover Similar[/B]" [B]Year[/B] of "2019" (leave blank if you don\'t know the year)' \
        '\n    - Choose from the titles presented for the correct Movie/TV Show' \
        '\n    - You will notice the other filters have disappeared. Once a "Discover Similar" value has been set, the other filters are not available.' \
        '\n    - Select "[B]Browse Results[/B]" to immediately see the results or "[B]Export List[/B]" to export the list to Fen Root Menu or Fen Movies Menu etc"' \
        '\n[B]You will see a list of Movies Similar to Avengers Endgame!!![/B]'
        return text

def set_history(db_type, name, query):
    from modules import fen_cache
    from datetime import timedelta
    _cache = fen_cache.FenCache()
    string = 'fen_discover_%s_%s' % (db_type, query)
    cache = _cache.get(string)
    if cache: return
    if db_type == 'movie':
        mode = 'build_movie_list'
        action = 'tmdb_movies_discover'
    else:
        mode = 'build_tvshow_list'
        action = 'tmdb_tv_discover'
    data = {'mode': mode, 'action': action, 'name': name, 'query': query}
    _cache.set(string, data, expiration=timedelta(days=7))
    return
