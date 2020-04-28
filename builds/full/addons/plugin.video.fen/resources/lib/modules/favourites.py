import xbmc, xbmcgui, xbmcaddon
import sys, os
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
from modules.nav_utils import notification
from modules.text import to_unicode
from modules.utils import to_utf8
from modules import settings
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database
# from modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))


class Favourites:
    def __init__(self):
        self.dialog = xbmcgui.Dialog()
        self.fav_database = os.path.join(__addon_profile__, 'favourites.db')
        settings.check_database(self.fav_database)
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        self.db_type = params.get('db_type')
        self.tmdb_id = params.get('tmdb_id')
        self.title = params.get('title')
        self.name = params.get('name')
        self.id = params.get('_id')
        self.url_dl = params.get('url_dl')
        self.size = params.get('size')

    def add_to_favourites(self):
        try:
            dbcon = database.connect(self.fav_database)
            dbcon.execute("INSERT INTO favourites VALUES (?, ?, ?)", (self.db_type, str(self.tmdb_id), to_unicode(self.title)))
            dbcon.commit()
            dbcon.close()
            notification('[B]%s[/B] added to Favourites' % self.title.upper(), 3500)
        except: notification('[B]%s[/B] already in Favourites' % self.title.upper(), 3500)

    def remove_from_favourites(self):
        dbcon = database.connect(self.fav_database)
        dbcon.execute("DELETE FROM favourites where db_type=? and tmdb_id=?", (self.db_type, str(self.tmdb_id)))
        dbcon.commit()
        dbcon.close()
        xbmc.executebuiltin("Container.Refresh")
        notification('[B]%s[/B] removed from Favourites' % self.title.upper(), 3500)

    def get_favourites(self, db_type):
        dbcon = database.connect(self.fav_database)
        dbcur = dbcon.cursor()
        dbcur.execute('''SELECT tmdb_id, title FROM favourites WHERE db_type=?''', (db_type,))
        result = dbcur.fetchall()
        dbcon.close()
        result = [{'tmdb_id': str(i[0]), 'title': str(to_utf8(i[1]))} for i in result]
        return result

    def clear_favourites(self):
        fl = [('Movie Favourites', 'movie'), ('TV Show Favourites', 'tvshow')]
        fl_choose = self.dialog.select("Choose Favourites to Erase", [i[0] for i in fl])
        if fl_choose < 0: return
        selection = fl[fl_choose]
        self.db_type = selection[1]
        confirm = self.dialog.yesno('Are you sure?', 'Continuing will erase all your [B]%s[/B]' % selection[0])
        if not confirm: return
        dbcon = database.connect(self.fav_database)
        dbcon.execute("DELETE FROM favourites WHERE db_type=?", (self.db_type,))
        dbcon.execute("VACUUM")
        dbcon.commit()
        dbcon.close()
        notification('[B]%s[/B] Erased' % selection[0], 3000)

def retrieve_favourites(db_type, page_no, letter):
    from modules.nav_utils import paginate_list
    from modules.utils import title_key
    from modules.settings import paginate, page_limit
    paginate = paginate()
    limit = page_limit()
    data = Favourites().get_favourites(db_type)
    data = sorted(data, key=lambda k: title_key(k['title']))
    original_list = [{'media_id': i['tmdb_id'], 'title': i['title']} for i in data]
    if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    else: final_list, total_pages = original_list, 1
    return final_list, total_pages


