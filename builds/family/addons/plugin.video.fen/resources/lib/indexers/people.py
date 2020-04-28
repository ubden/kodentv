
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import sys, os
try: from urllib import unquote
except ImportError: from urllib.parse import unquote
from apis import tmdb_api as TMDb
from modules.nav_utils import build_url, add_dir, setView, notification, paginate_list
from modules import settings
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
dialog = xbmcgui.Dialog()
fanart = __addon__.getAddonInfo('fanart')
icon_directory = settings.get_theme()

class People():
    def __init__(self, actor_info=None):
        self.image_base = 'http://image.tmdb.org/t/p/%s%s'
        self.actor_id = actor_info[0]
        self.choose_id = True if self.actor_id == 'None' else False
        self.actor_name = actor_info[1]
        self.actor_image = actor_info[2]

    def search(self):
        if self.choose_id:
            self.query = self._get_query()
            if not self.query: return
            self.actor_id, self.actor_name, self.actor_image = self._get_actor_details()
            if not self.actor_id: return
        self.main()

    def main(self):
        params = {'actor_id': self.actor_id, 'actor_name': self.actor_name, 'actor_image': self.actor_image}
        for menu_item in [('Movies', 'people_search.media_results'), ('TV Shows', 'people_search.media_results'), ('Biography', 'people_search.biography_results'), ('Images', 'people_search.image_results')]:
            if menu_item[0] == 'Movies': params['media_type'] = 'movies'
            elif menu_item[0] == 'TV Shows': params['media_type'] = 'tvshows'
            self._add_dir(menu_item[0], menu_item[1], params, isFolder=True)
        xbmcplugin.setContent(__handle__, 'files')
        xbmcplugin.endOfDirectory(__handle__)
        setView('view.main')

    def biography_results(self):
        from modules.utils import calculate_age
        def _make_biography():
            age = None
            heading = 'FEN Biography'
            name = bio_info.get('name')
            place_of_birth = bio_info.get('place_of_birth')
            biography = bio_info.get('biography')
            birthday = bio_info.get('birthday')
            deathday = bio_info.get('deathday')
            if deathday: age = calculate_age(birthday, '%Y-%m-%d', deathday)
            elif birthday: age = calculate_age(birthday, '%Y-%m-%d')
            text = '\n[COLOR dodgerblue][B]NAME:[/B][/COLOR] %s' % name
            if place_of_birth: text += '\n\n[COLOR dodgerblue][B]PLACE OF BIRTH[/B][/COLOR]: %s' % place_of_birth
            if birthday: text += '\n\n[COLOR dodgerblue][B]BIRTHDAY[/B][/COLOR]: %s' % birthday
            if deathday: text += '\n\n[COLOR dodgerblue][B]DIED:[/B][/COLOR] %s, aged %s' % (deathday, age)
            elif age: text += '\n\n[COLOR dodgerblue][B]AGE:[/B][/COLOR] %s' % age
            if biography: text += '\n\n[COLOR dodgerblue][B]BIOGRAPHY:[/B][/COLOR]\n%s' % biography
            return heading, text
        dialog = xbmcgui.Dialog()
        bio_info = TMDb.tmdb_people_biography(self.actor_id)
        if bio_info.get('biography', None) in ('', None):
            bio_info = TMDb.tmdb_people_biography(self.actor_id, 'en')
        if not bio_info: return notification('No Biography Found')
        heading, text = _make_biography()
        return dialog.textviewer(heading, text)

    def image_results(self):
        results = TMDb.tmdb_people_pictures(self.actor_id)
        for item in results['profiles']:
            thumb_url = self.image_base % ('h632', item['file_path'])
            image_url = self.image_base % ('original', item['file_path'])
            name = '%sx%s' % (item['height'], item['width'])
            url_params = {'mode': 'show_image', 'image_url': image_url}
            url = build_url(url_params)
            listitem = xbmcgui.ListItem(name)
            listitem.setArt({'icon': thumb_url, 'poster': thumb_url, 'thumb': thumb_url, 'fanart': fanart, 'banner': thumb_url})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        xbmcplugin.setContent(__handle__, 'files')
        xbmcplugin.endOfDirectory(__handle__)
        setView('view.main')

    def media_results(self, media_type, page_no, letter):
        from indexers.movies import Movies
        from indexers.tvshows import TVShows
        from modules.nav_utils import paginate_list, cached_page
        from modules.utils import title_key
        def _add_misc_dir(url_params, list_name='Next Page >>', info='Navigate to Next Page...', iconImage='item_next.png'):
            listitem = xbmcgui.ListItem(list_name, iconImage=os.path.join(icon_directory, iconImage))
            listitem.setArt({'fanart': __addon__.getAddonInfo('fanart')})
            listitem.setInfo('video', {'title': list_name, 'plot': info})
            if url_params['mode'] == 'build_navigate_to_page': listitem.addContextMenuItems([("[B]Switch Jump To Action[/B]","XBMC.RunPlugin(%s)" % build_url({'mode': 'toggle_jump_to'}))])
            xbmcplugin.addDirectoryItem(handle=__handle__, url=build_url(url_params), listitem=listitem, isFolder=True)
        not_widget = xbmc.getInfoLabel('Container.PluginName')
        cache_page = settings.cache_page()
        cache_page_string = 'people_search_%s_%s' % (media_type, self.actor_id)
        limit = 20
        if cache_page:
            if not 'new_page' in params:
                silent = False if not_widget else True
                retrieved_page = cached_page(cache_page_string, silent=silent)
                if retrieved_page: page_no = retrieved_page
        try:
            builder = Movies if media_type == 'movies' else TVShows
            function = TMDb.tmdb_movies_actor_roles if media_type == 'movies' else TMDb.tmdb_tv_actor_roles
            content = 'movies' if media_type == 'movies' else 'tvshows'
            key = 'title' if media_type == 'movies' else 'name'
            result = function(self.actor_id)
            data = sorted(result, key=lambda k: title_key(k[key]))
            original_list = [{'media_id': i['id'], 'title': i[key]} for i in data]
            paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
            media_list = [i['media_id'] for i in paginated_list]
            if total_pages > 2 and not_widget: _add_misc_dir({'mode': 'build_navigate_to_page', 'db_type': 'Media', 'media_type': media_type, 'actor_id': self.actor_id, 'actor_name': self.actor_name, 'actor_image': self.actor_image, 'current_page': page_no, 'total_pages': total_pages, 'transfer_mode': 'people_search.media_results'}, 'Jump To...', 'Jump To a Certain Page/Letter...', 'item_jump.png')
            builder(media_list, action='people_search_%s' % media_type).worker()
            if total_pages > page_no: _add_misc_dir({'mode': 'people_search.media_results', 'media_type': media_type, 'actor_id': self.actor_id, 'actor_name': self.actor_name, 'actor_image': self.actor_image, 'new_page': str(page_no + 1), 'new_letter': letter})
            if cache_page: cached_page(cache_page_string, page_no=page_no)
            xbmcplugin.setContent(__handle__, content)
            xbmcplugin.endOfDirectory(__handle__)
            setView('view.%s' % content, content)
        except: notification('No Results', 3000)

    def _get_query(self):
        if self.actor_name in ('None', '', None): actor_name = dialog.input("Search Fen", type=xbmcgui.INPUT_ALPHANUM)
        else: actor_name = self.actor_name
        return unquote(actor_name)

    def _get_actor_details(self):
        from modules.history import add_to_search_history
        actors = TMDb.tmdb_people_info(self.query)
        actor_list = []
        if len(actors) > 1:
            for item in actors:
                known_for_list = [i.get('title', 'NA') for i in item['known_for']]
                known_for_list = [i for i in known_for_list if not i == 'NA']
                known_for = '[I]%s[/I]' % ', '.join(known_for_list) if known_for_list else '[I]Movie Actor[/I]'
                listitem = xbmcgui.ListItem(item['name'], known_for)
                image = 'http://image.tmdb.org/t/p/w185/%s' % item['profile_path'] if item['profile_path'] else os.path.join(icon_directory, 'genre_family.png')
                listitem.setArt({'icon': image})
                listitem.setProperty('id', str(item['id']))
                listitem.setProperty('name', str(item['name']))
                listitem.setProperty('image', str(image.replace('w185', 'h632')))
                actor_list.append(listitem)
            selection = dialog.select("Select Person", actor_list, useDetails=True)
            if selection >= 0:
                actor_id = int(actor_list[selection].getProperty('id'))
                actor_name = actor_list[selection].getProperty('name')
                actor_image = actor_list[selection].getProperty('image')
            else: return None, None, None
        else:
            actors = actors[0]
            actor_id = actors['id']
            actor_name = actors['name']
            try: image_id = actors['profile_path']
            except: image_id = None
            if not image_id: actor_image = os.path.join(icon_directory, 'genre_family.png')
            else: actor_image = 'http://image.tmdb.org/t/p/h632/%s' % image_id
        add_to_search_history(actor_name, 'people_queries')
        return actor_id, actor_name, actor_image

    def _add_dir(self, list_name, mode, url_params, isFolder=True):
        url_params['mode'] = mode
        actor_id = url_params['actor_id']
        actor_name = url_params['actor_name']
        actor_image = url_params['actor_image']
        list_name = '[B]%s :[/B] %s' % (actor_name.upper(), list_name)
        info = url_params.get('info', '')
        url = build_url(url_params)
        listitem = xbmcgui.ListItem(list_name, iconImage=actor_image)
        listitem.setArt({'fanart': fanart})
        listitem.setInfo('video', {'title': list_name, 'plot': info})
        xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=isFolder)
