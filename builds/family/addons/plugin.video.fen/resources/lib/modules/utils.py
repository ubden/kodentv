
import sys
import xbmc, xbmcaddon

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__url__ = sys.argv[0]

def pool_converter(items):
    """
    takes tuple, converts it to a list, and turns first item
    into the function and following items into the arguments
    """
    items = list(items)
    func = items.pop(0)
    return func(*items)

def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]

def natural_sort(list, key=lambda s:s):
    """
    Sort a list into natural alphanumeric order.
    """
    import re
    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text 
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]
    sort_key = get_alphanum_key_func(key)
    list.sort(key=sort_key)

def string_to_float(string, default_return):
    ''' Remove all alpha from string and return a float.
        Returns float of "default_return" upon ValueError. '''
    try:
        return float(''.join(c for c in string if (c.isdigit() or c =='.')))
    except ValueError:
        return float(default_return)

def jsondate_to_datetime(jsondate_object, resformat, remove_time=False):
    import _strptime  # fix bug in python import
    from datetime import datetime
    import time
    if remove_time:
        try: datetime_object = datetime.strptime(jsondate_object, resformat).date()
        except TypeError: datetime_object = datetime(*(time.strptime(jsondate_object, resformat)[0:6])).date()
    else:
        try: datetime_object = datetime.strptime(jsondate_object, resformat)
        except TypeError: datetime_object = datetime(*(time.strptime(jsondate_object, resformat)[0:6]))
    return datetime_object
    
def adjust_premiered_date(orig_date, adjust_hours):
    from datetime import timedelta
    orig_date += ' 23:59:59'
    datetime_object = jsondate_to_datetime(orig_date, "%Y-%m-%d %H:%M:%S")
    adjusted_datetime = datetime_object + timedelta(hours=adjust_hours)
    adjusted_string = adjusted_datetime.strftime('%Y-%m-%d')
    return adjusted_datetime, adjusted_string

def make_day(date, use_words=True):
    from datetime import timedelta
    import time
    from modules.settings import nextep_airdate_format
    from datetime import datetime
    today = datetime.utcnow()
    day_diff = (date - today).days
    date_format = nextep_airdate_format()
    try: day = date.strftime(date_format)
    except ValueError: day = date.strftime('%Y-%m-%d')
    if use_words:
        if day_diff == -1:
            day = 'YESTERDAY'
        elif day_diff == 0:
            day = 'TODAY'
        elif day_diff == 1:
            day = 'TOMORROW'
        elif 1 < day_diff < 7:
            day = date.strftime('%A').upper()
    return day

def calculate_age(born, str_format, died=None):
    ''' born and died are str objects e.g. "1972-05-28" '''
    from datetime import date, datetime
    import time
    try: born = datetime.strptime(born, str_format)
    except TypeError: born = datetime(*(time.strptime(born, str_format)[0:6]))
    if not died:
        today = date.today()
    else:
        try: died = datetime.strptime(died, str_format)
        except TypeError: died = datetime(*(time.strptime(died, str_format)[0:6]))
        today = died
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def batch_replace(s, replace_info):
    for r in replace_info:
        s = str(s).replace(r[0], r[1])
    return s

def clean_file_name(s, use_encoding=False, use_blanks=True):
    try:
        hex_entities = [['&#x26;', '&'], ['&#x27;', '\''], ['&#xC6;', 'AE'], ['&#xC7;', 'C'],
                    ['&#xF4;', 'o'], ['&#xE9;', 'e'], ['&#xEB;', 'e'], ['&#xED;', 'i'],
                    ['&#xEE;', 'i'], ['&#xA2;', 'c'], ['&#xE2;', 'a'], ['&#xEF;', 'i'],
                    ['&#xE1;', 'a'], ['&#xE8;', 'e'], ['%2E', '.'], ['&frac12;', '%BD'],
                    ['&#xBD;', '%BD'], ['&#xB3;', '%B3'], ['&#xB0;', '%B0'], ['&amp;', '&'],
                    ['&#xB7;', '.'], ['&#xE4;', 'A'], ['\xe2\x80\x99', '']]
        special_encoded = [['"', '%22'], ['*', '%2A'], ['/', '%2F'], [':', ','], ['<', '%3C'],
                            ['>', '%3E'], ['?', '%3F'], ['\\', '%5C'], ['|', '%7C']]
        
        special_blanks = [['"', ' '], ['*', ' '], ['/', ' '], [':', ''], ['<', ' '],
                            ['>', ' '], ['?', ' '], ['\\', ' '], ['|', ' '], ['%BD;', ' '],
                            ['%B3;', ' '], ['%B0;', ' '], ["'", ""], [' - ', ' '], ['.', ' '],
                            ['!', ''], [';', ''], [',', '']]
        s = batch_replace(s, hex_entities)
        if use_encoding:
            s = batch_replace(s, special_encoded)
        if use_blanks:
            s = batch_replace(s, special_blanks)
        s = s.strip()
    except: pass
    return s

def clean_title(title):
    import re
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub(r'\<[^>]*\>','', title)
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\(|\)|\[|\]|\{|\}|\s', '', title)
    title = re.sub('[^A-z0-9]', '', title)
    return title

def to_bytes(text):
    try:
        if isinstance(text, text_type):
            text = text.encode("utf-8")
    except:
        pass
    return text

def to_utf8(obj):
    try:
        import copy
        if isinstance(obj, unicode):
            obj = obj.encode('utf-8', 'ignore')
        elif isinstance(obj, dict):
            obj = copy.deepcopy(obj)
            for key, val in obj.items():
                obj[key] = to_utf8(val)
        elif obj is not None and hasattr(obj, "__iter__"):
            obj = obj.__class__([to_utf8(x) for x in obj])
        else: pass
    except: pass
    return obj

def byteify(data, ignore_dicts=False):
    try:
        if isinstance(data, unicode):
            return data.encode('utf-8')
        if isinstance(data, list):
            return [byteify(item, ignore_dicts=True) for item in data]
        if isinstance(data, dict) and not ignore_dicts:
            return dict([(byteify(key, ignore_dicts=True), byteify(value, ignore_dicts=True)) for key, value in data.iteritems()])
    except:
        pass
    return data

def normalize(txt):
    import re
    txt = re.sub(r'[^\x00-\x7f]',r'', txt)
    return txt

def safe_string(obj):
    try:
        try:
            return str(obj)
        except UnicodeEncodeError:
            return obj.encode('utf-8', 'ignore').decode('ascii', 'ignore')
        except:
            return ""
    except:
        return obj

def remove_accents(obj):
    import unicodedata
    try:
        obj = u'%s' % obj
        obj = ''.join(c for c in unicodedata.normalize('NFD', obj) if unicodedata.category(c) != 'Mn')
    except:
        pass
    return obj

def read_from_file(path, silent=False):
    import xbmcvfs
    try:
        f = xbmcvfs.File(path)
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            pass
        return None

def regex_from_to(text, from_string, to_string, excluding=True):
    import re
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    import re
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

def remove_all(elements, list):
    return filter(lambda x: x not in elements, list)

def replace_html_codes(txt):
    try:
        from HTMLParser import HTMLParser
    except ImportError:
        from html.parser import HTMLParser
    import re
    txt = to_utf8(txt)
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    return txt

def logger(heading, function):
    xbmc.log('###%s###: %s' % (heading, function), 2)

def int_with_commas(number):
    '''helper to pretty format a number'''
    try:
        number = int(number)
        if number < 0:
            return '-' + int_with_commas(-number)
        result = ''
        while number >= 1000:
            number, number2 = divmod(number, 1000)
            result = ",%03d%s" % (number2, result)
        return "%d%s" % (number, result)
    except Exception:
        return ""

def try_parse_int(string):
    '''helper to parse int from string without erroring on empty or misformed string'''
    try:
        return int(string)
    except Exception:
        return 0

def writeDict(dict, filename, sep):
    with open(filename, "a") as f:
        for i in dict.keys():            
            f.write(i + " " + sep.join([str(x) for x in dict[i]]) + "\n")

def readDict(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            values = line.split(sep)
            dict[values[0]] = {int(x) for x in values[1:len(values)]}
        return(dict)

def sec2time(sec, n_msec=3):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec,'__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)
    
def sort_list(sort_key, sort_direction, list_data):
    reverse = False if sort_direction == 'asc' else True
    if sort_key == 'rank':
        return sorted(list_data, key=lambda x: x['rank'], reverse=reverse)
    elif sort_key == 'added':
        return sorted(list_data, key=lambda x: x['listed_at'], reverse=reverse)
    elif sort_key == 'title':
        return sorted(list_data, key=lambda x: title_key(x[x['type']].get('title')), reverse=reverse)
    elif sort_key == 'released':
        return sorted(list_data, key=lambda x: released_key(x[x['type']]), reverse=reverse)
    elif sort_key == 'runtime':
        return sorted(list_data, key=lambda x: x[x['type']].get('runtime', 0), reverse=reverse)
    elif sort_key == 'popularity':
        return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
    elif sort_key == 'percentage':
        return sorted(list_data, key=lambda x: x[x['type']].get('rating', 0), reverse=reverse)
    elif sort_key == 'votes':
        return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
    elif sort_key == 'random':
        import random
        return sorted(list_data, key=lambda k: random.random())
    else:
        return list_data

def released_key(item):
    if 'released' in item:
        return item['released']
    elif 'first_aired' in item:
        return item['first_aired']
    else:
        return 0

def title_key(title):
    from modules.settings import ignore_articles
    if not ignore_articles(): return title
    import re
    try:
        if title is None: title = ''
        articles = ['the', 'a', 'an']
        match = re.match('^((\w+)\s+)', title.lower())
        if match and match.group(2) in articles: offset = len(match.group(1))
        else: offset = 0

        return title[offset:]
    except: return title

def supported_video_extensions():
    supported_video_extensions = xbmc.getSupportedMedia('video').split('|')
    return [i for i in supported_video_extensions if i != '' and i != '.zip']

def selection_dialog(dialog_list, function_list, string):
    import xbmcgui
    dialog = xbmcgui.Dialog()
    list_choice = dialog.select("%s" % string, dialog_list)
    if list_choice >= 0: return function_list[list_choice]
    else: return None

def multiselect_dialog(string, dialog_list, function_list=None, preselect= []):
    import xbmcgui
    dialog = xbmcgui.Dialog()
    if not function_list: function_list = dialog_list
    list_choice = dialog.multiselect(string, dialog_list, preselect=preselect)
    return [function_list[i] for i in list_choice] if list_choice is not None else list_choice

def set_quality(quality_setting=None):
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    quality_setting = quality_setting if quality_setting else params['quality_setting']
    string = 'Please Choose Autoplay Filters' if quality_setting == 'autoplay' else 'Please Choose Result Filters:'
    setting = 'autoplay_quality' if quality_setting == 'autoplay' else 'results_quality'
    dl = ['Include SD', 'Include 720p', 'Include 1080p', 'Include 4K']
    fl = ['SD', '720p', '1080p', '4K']
    try: preselect = [fl.index(i) for i in __addon__.getSetting(setting).split(', ')]
    except: preselect = []
    filters = multiselect_dialog(string, dl, fl, preselect)
    if filters is None: return
    if filters == []:
        import xbmcgui
        xbmcgui.Dialog().ok('FEN Filters', 'You must select at least 1 Filter Setting.', '', 'Please Retry.....')
        return set_quality(quality_setting)
    from modules.nav_utils import toggle_setting
    toggle_setting(setting, ', '.join(filters))

def open_ext_settings(addon):
    xbmc.sleep(500)
    xbmcaddon.Addon(id=addon).openSettings()

def enable_scrapers():
    from modules.settings import active_scrapers
    from modules.nav_utils import toggle_setting
    scrapers = ['external', 'furk', 'easynews', 'rd-cloud', 'pm-cloud', 'ad-cloud', 'local', 'downloads', 'folders']
    preselect = [scrapers.index(i) for i in active_scrapers(group_folders=True)]
    scrapers_dialog = [i.upper() for i in scrapers]
    scraper_choice = multiselect_dialog('Choose Fen Scrapers', scrapers_dialog, scrapers, preselect=preselect)
    if scraper_choice is None: return
    return [toggle_setting('provider.%s' % i, ('true' if i in scraper_choice else 'false')) for i in scrapers]

def set_active_cloud_store(current_active):
    debrid_clouds = [('real-debrid', 'RD', 'Real Debrid'), ('premiumize.me', 'PM', 'Premiumize'), ('alldebrid', 'AD', 'All Debrid')]
    dialog_list = [i[2] for i in debrid_clouds]
    function_list = [i[0] for i in debrid_clouds]
    preselect = [debrid_clouds.index(i) for i in current_active]
    store_torrents_choice = multiselect_dialog('Choose Debrid Clouds to Store Resolved Torrents', dialog_list, function_list, preselect=preselect)
    if store_torrents_choice is None: return
    for i in function_list:
        if i in store_torrents_choice: __addon__.setSetting('store_torrent.%s' % i, 'true')
        else: __addon__.setSetting('store_torrent.%s' % i, 'false')

def set_subtitle_action():
    from modules.nav_utils import toggle_setting
    choices = ('Auto', 'Select', 'Off')
    choice = selection_dialog(choices, choices, 'Fen - Choose Subtitles Action')
    if choice: return toggle_setting('subtitles.subs_action', choice)

def set_display_mode():
    test = "Directory|Very Simple Directory|Dialog"
    from modules.nav_utils import toggle_setting
    names = ('Directory', 'Very Simple Directory', 'Dialog')
    settings = ('0', '1', '2')
    choice = selection_dialog(names, settings, 'Fen - Choose Display Mode')
    if choice: return toggle_setting('display_mode', choice)

def subscriptions_update_interval():
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    from modules.nav_utils import toggle_setting
    import time
    from datetime import datetime, timedelta
    from modules.nav_utils import open_settings
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    subscription_timer = __addon__.getSetting('subscription_timer')
    if params['update_type'] == 'interval':
        subscriptions_update_label = 'subscriptions_update_label1'
        intervals = [('1 Hour', 1), ('2 Hours', 2), ('4 Hours', 4), ('8 Hours', 8), ('12 Hours', 12), ('16 Hours', 16), ('24 Hours', 24)]
        try: last_run_time = datetime.strptime(__addon__.getSetting('service_time'), "%Y-%m-%d %H:%M:%S") - timedelta(hours=int(subscription_timer))
        except TypeError: last_run_time = datetime(*(time.strptime(__addon__.getSetting('service_time'), "%Y-%m-%d %H:%M:%S")[0:6])) - timedelta(hours=int(subscription_timer))
        choice = selection_dialog([i[0] for i in intervals], intervals, 'Fen - Choose Subscription Update Interval')
        if not choice: choice = ('24 Hours', 24)
        interval = str(choice[1])
        interval_display = choice[0]
        new_run_time = last_run_time + timedelta(hours=int(interval))
        new_run_time = new_run_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        subscriptions_update_label = 'subscriptions_update_label2'
        intervals = []
        for i in range(24): intervals.append(('%02d:00' % i, i))
        choice = selection_dialog([i[0] for i in intervals], intervals, 'Fen - Choose Daily Subscription Update Time')
        if not choice: choice = ('06:00', 6)
        sub_hour = choice[1]
        interval_display = choice[0]
        interval = subscription_timer
        now = datetime.today()
        sub_day = now.day + 1 if sub_hour == 0 else now.day
        new_run_time = now.replace(day=sub_day, hour=sub_hour, minute=0, second=0, microsecond=0) + timedelta(days=1)
        difference = new_run_time - now
        if '1 day' in str(difference): new_run_time = now.replace(day=sub_day, hour=sub_hour, minute=0, second=0, microsecond=0)
        new_run_time = new_run_time.strftime("%Y-%m-%d %H:%M:%S")
    toggle_setting('subscription_timer', interval)
    toggle_setting(subscriptions_update_label, interval_display)
    toggle_setting('service_time', new_run_time)
    return open_settings('8.7')

def unaired_episode_color_choice():
    from modules.nav_utils import toggle_setting
    dialog = 'Please Choose Color for Unaired Episodes'
    chosen_color = color_chooser(dialog, no_color=True)
    if chosen_color: toggle_setting('unaired_episode_colour', chosen_color)

def scraper_dialog_color_choice():
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    from modules.nav_utils import toggle_setting
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    setting ='int_dialog_highlight' if params['setting'] == 'internal' else 'ext_dialog_highlight'
    dialog = 'Please Choose Color for Internal Scrapers Progress Dialog Highlight'
    chosen_color = color_chooser(dialog)
    if chosen_color: toggle_setting(setting, chosen_color)

def scraper_quality_color_choice():
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    from modules.nav_utils import toggle_setting
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    setting = params['setting']
    dialog = 'Please Choose Color for Scraper Quality Highlight'
    chosen_color = color_chooser(dialog)
    if chosen_color: toggle_setting(setting, chosen_color)

def external_scrapers_manager():
    import xbmcgui
    import json
    from modules.nav_utils import build_url
    dialog = xbmcgui.Dialog()
    icon = xbmcaddon.Addon(id='script.module.openscrapers').getAddonInfo('icon')
    fail_color = 'crimson'
    all_color = 'mediumvioletred'
    debrid_color = __addon__.getSetting('prem.identify')
    torrent_color = __addon__.getSetting('torrent.identify')
    tools_menu = \
        [('[COLOR %s][B]FAILURES[/B][/COLOR]', fail_color, '[B]- Disable Failing External Scrapers[/B]', {'mode': 'external_scrapers_disable'}),
        ('[COLOR %s][B]FAILURES[/B][/COLOR]', fail_color, '[B]- Reset Failing External Scraper Stats[/B]', {'mode': 'external_scrapers_reset_stats'}),
        ('[COLOR %s][B]ALL SCRAPERS[/B][/COLOR]', all_color , '[B]- Enable All Scrapers[/B]', {'mode': 'toggle_all', 'folder': 'all_eng', 'setting': 'true'}),
        ('[COLOR %s][B]ALL SCRAPERS[/B][/COLOR]', all_color , '[B]- Disable All Scrapers[/B]', {'mode': 'toggle_all', 'folder': 'all_eng', 'setting': 'false'}),
        ('[COLOR %s][B]ALL SCRAPERS[/B][/COLOR]', all_color , '[B]- Enable/Disable Specific Scrapers[/B]',{'mode': 'enable_disable_specific_all', 'folder': 'all_eng'}),
        ('[COLOR %s][B]DEBRID SCRAPERS[/B][/COLOR]', debrid_color , '[B]- Enable All Debrid Scrapers[/B]', {'mode': 'toggle_all', 'folder': 'en_DebridOnly', 'setting': 'true'}),
        ('[COLOR %s][B]DEBRID SCRAPERS[/B][/COLOR]', debrid_color , '[B]- Disable All Debrid Scrapers[/B]', {'mode': 'toggle_all', 'folder': 'en_DebridOnly', 'setting': 'false'}),
        ('[COLOR %s][B]DEBRID SCRAPERS[/B][/COLOR]', debrid_color , '[B]- Enable/Disable Specific Debrid Scrapers[/B]', {'mode': 'enable_disable_specific_all', 'folder': 'en_DebridOnly'}),
        ('[COLOR %s][B]TORRENT SCRAPERS[/B][/COLOR]', torrent_color , '[B]- Enable All Torrent Scrapers[/B]', {'mode': 'toggle_all', 'folder': 'en_Torrent', 'setting': 'true'}),
        ('[COLOR %s][B]TORRENT SCRAPERS[/B][/COLOR]', torrent_color , '[B]- Disable All Torrent Scrapers[/B]', {'mode': 'toggle_all', 'folder': 'en_Torrent', 'setting': 'false'}),
        ('[COLOR %s][B]TORRENT SCRAPERS[/B][/COLOR]', torrent_color , '[B]- Enable/Disable Specific Torrent Scrapers[/B]', {'mode': 'enable_disable_specific_all', 'folder': 'en_Torrent'})]
    choice_list = []
    for item in tools_menu:
        line1 = item[0] % item[1]
        line2 = item[2]
        listitem = xbmcgui.ListItem(line1, line2)
        listitem.setArt({'icon': icon})
        choice_list.append(listitem)
    chosen_tool = dialog.select("External Scrapers Manager", choice_list, useDetails=True)
    if chosen_tool < 0: return
    from modules import external_source_utils
    params = tools_menu[chosen_tool][3]
    mode = params['mode']
    if mode == 'external_scrapers_disable':
        external_source_utils.external_scrapers_disable()
    elif mode == 'external_scrapers_reset_stats':
        external_source_utils.external_scrapers_reset_stats()
    elif mode == 'toggle_all':
        external_source_utils.toggle_all(params['folder'], params['setting'])
    elif mode == 'enable_disable_specific_all':
        external_source_utils.enable_disable_specific_all(params['folder'])
    return external_scrapers_manager()

def switch_settings():
    from modules.nav_utils import toggle_setting, settings_layout
    choices = ('Basic', 'Advanced (Multiple Submenus)')
    choice = selection_dialog(choices, choices, 'Fen - Choose Settings Layout')
    if choice:
        toggle_setting('settings_layout', choice)
        settings_layout(choice)

def toggle_jump_to():
    from modules.nav_utils import toggle_setting, notification
    from modules.settings import nav_jump_use_alphabet
    use_alphabet = nav_jump_use_alphabet()
    (setting, new_action) = ('0', 'PAGE') if use_alphabet == True else ('1', 'ALPHABET')
    toggle_setting(setting_id='nav_jump', setting_value=setting, refresh=True)
    notification('Jump To Action Switched to [B]%s[/B]' % new_action)

def scraper_color_choice():
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    from modules.nav_utils import toggle_setting
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    choices = [('furk', 'provider.furk_colour'),
                ('easynews', 'provider.easynews_colour'),
                ('pm-cloud', 'provider.pm-cloud_colour'),
                ('rd-cloud', 'provider.rd-cloud_colour'),
                ('ad-cloud', 'provider.ad-cloud_colour'),
                ('local', 'provider.local_colour'),
                ('downloads', 'provider.downloads_colour'),
                ('folders', 'provider.folders_colour'),
                ('premium', 'prem.identify'),
                ('torrent', 'torrent.identify'),
                ('second_line', 'secondline.identify')]
    title, setting = [(i[0], i[1]) for i in choices if i[0] == params.get('setting')][0]
    dialog = 'Please Choose Color for %s Results Highlight' % title.upper()
    chosen_color = color_chooser(dialog, no_color=True)
    if chosen_color: toggle_setting(setting, chosen_color)

def folder_sources_choice():
    import xbmcgui
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    from modules.nav_utils import toggle_setting
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    setting = params['setting']
    folder = xbmcgui.Dialog().browse(0, 'FEN - Select Directory...', '')
    if not folder: folder = 'None'
    __addon__.setSetting(setting, folder)

def internal_scrapers_order_choice():
    import xbmcgui
    from modules.nav_utils import toggle_setting
    window = xbmcgui.Window(10000)
    try: current_ordering = window.getProperty('FEN_internal_scrapers_order').split(', ')
    except: current_ordering = ['']
    if len(current_ordering) != 4:
        from modules.settings import internal_scraper_order
        current_ordering = internal_scraper_order()
    default = [('FILES', current_ordering.index("FILES")),
               ('FURK', current_ordering.index("FURK")),
               ('EASYNEWS', current_ordering.index("EASYNEWS")),
               ('CLOUD', current_ordering.index("CLOUD"))]
    choices = sorted(default, key=lambda x: x[1])
    adjust_scraper = selection_dialog([i[0] for i in choices], [i[0] for i in choices], 'Fen - Choose Scraper to Change Order')
    if not adjust_scraper: return window.clearProperty('FEN_internal_scrapers_order')
    choices = [('Place [B]%s[/B] 1st' % adjust_scraper, (0, current_ordering.index(adjust_scraper))),
               ('Place [B]%s[/B] 2nd' % adjust_scraper, (1, current_ordering.index(adjust_scraper))),
               ('Place [B]%s[/B] 3rd' % adjust_scraper, (2, current_ordering.index(adjust_scraper))),
               ('Place [B]%s[/B] 4th' % adjust_scraper, (3, current_ordering.index(adjust_scraper)))]
    positioning_info = selection_dialog([i[0] for i in choices], [i[1] for i in choices], 'Fen - Choose %s Scraper Position' % adjust_scraper)
    if not positioning_info: return internal_scrapers_order_choice()
    new_position = positioning_info[0]
    current_position = positioning_info[1]
    current_ordering.insert(new_position, current_ordering.pop(current_position))
    new_order_setting = (', ').join(current_ordering)
    window.setProperty('FEN_internal_scrapers_order', new_order_setting)
    toggle_setting('internal_scrapers_order', new_order_setting)
    return internal_scrapers_order_choice()

def build_add_to_remove_from_list(meta='', media_type='', orig_mode='', from_search=''):
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    import json
    from modules.settings import trakt_list_subscriptions, watched_indicators
    from modules.nav_utils import build_url
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    media_type = params.get('media_type', '')
    orig_mode = params.get('orig_mode', '')
    from_search = params.get('from_search', '')
    meta = json.loads(params.get('meta', None))
    main_listing = [('Add to...', 'add'), ('Remove from...', 'remove')]
    mlc = selection_dialog([i[0] for i in main_listing], [i[1] for i in main_listing], 'Choose Add to or Remove from...')
    if mlc == None: return
    string = "Choose Selection to Add Item To" if mlc == 'add' else "Choose Selection to Remove Item From"
    heading = 'Add to ' if mlc == 'add' else 'Remove from '
    listing = [(heading + 'Trakt List', 'trakt'), (heading + 'Fen Favourites', 'favourites')]
    if not trakt_list_subscriptions(): listing.append((heading + 'Fen Subscriptions', 'subscriptions'))
    if media_type == 'tvshow' and watched_indicators() == 0: listing.append((heading + 'Fen Next Episode', 'unwatched_next_episode'))
    if mlc == 'remove': listing.append((heading + 'Cache (Re-cache %s Info)' % ('Movie' if media_type == 'movie' else 'TV Show'), 'refresh'))
    choice = selection_dialog([i[0] for i in listing], [i[1] for i in listing], string)
    if choice == None: return
    elif choice == 'trakt': url = {'mode': ('trakt.trakt_add_to_list' if mlc == 'add' else 'trakt.trakt_remove_from_list'), 'tmdb_id': meta["tmdb_id"], 'imdb_id': meta["imdb_id"], 'tvdb_id': meta["tvdb_id"], 'db_type': media_type}
    elif choice == 'favourites': url = {'mode': ('add_to_favourites' if mlc == 'add' else 'remove_from_favourites'), 'db_type': media_type, 'tmdb_id': meta["tmdb_id"], 'title': meta['title']}
    elif choice == 'subscriptions': url = {'mode': 'subscriptions_add_remove', 'action': mlc, 'db_type': media_type, 'tmdb_id': meta["tmdb_id"], 'orig_mode': orig_mode}
    elif choice == 'unwatched_next_episode': url = {'mode': 'add_next_episode_unwatched', 'action': mlc, 'title': meta["title"], 'tmdb_id': meta["tmdb_id"], 'imdb_id': meta["imdb_id"]}
    elif choice == 'refresh': url = {'mode': 'refresh_cached_data', 'db_type': media_type, 'id_type': 'tmdb_id', 'media_id': meta['tmdb_id']}
    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % build_url(url))

def playback_menu(from_results=False, suggestion=None, list_name=None, play_params=None):
    try: from urlparse import parse_qsl
    except ImportError: from urllib.parse import parse_qsl
    from modules.nav_utils import toggle_setting, build_url, open_settings, clear_cache, cached_page_clear, clear_and_rescrape
    from modules import settings
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    content = xbmc.getInfoLabel('Container.Content')
    if not content: content = params.get('content', None)
    from_results = params.get('from_results', from_results)
    suggestion = params.get('suggestion', suggestion)
    list_name = params.get('list_name', list_name)
    play_params = params.get('play_params', play_params)
    autoplay_status, autoplay_toggle, filter_setting = ('On', 'false', 'autoplay_quality') if settings.auto_play() else ('Off', 'true', 'results_quality')
    quality_filter_setting = 'autoplay' if autoplay_status == 'On' else 'results'
    autoplay_next_status, autoplay_next_toggle = ('On', 'false') if settings.autoplay_next_episode() else ('Off', 'true')
    display_mode = settings.display_mode()
    display_mode_status = 'Directory' if display_mode == 0 else 'Very Simple Directory' if display_mode == 1 else 'Dialog'
    autoplay_hevc_status = settings.autoplay_hevc()
    current_subs_action_status = __addon__.getSetting('subtitles.subs_action')
    active_scrapers = [i.replace('-', '') for i in settings.active_scrapers(group_folders=True)]
    current_scrapers_status = ', '.join([i.upper()[:3] for i in active_scrapers]) if len(active_scrapers) > 0 else 'NONE'
    current_filter_status =  ', '.join(settings.quality_filter(filter_setting))
    indicators_status, indicators_toggle = ('Trakt', '0') if settings.watched_indicators() in (1, 2) else ('Fen', '1')
    cached_torrents_status, cached_torrents_toggle = ('On', 'false') if __addon__.getSetting('torrent.check.cache') =='true' else ('Off', 'true')
    uncached_torrents_status, uncached_torrents_toggle = ('On', 'false') if __addon__.getSetting('torrent.display.uncached') =='true' else ('Off', 'true')
    active_cloud_store = settings.active_store_torrent_to_cloud()
    active_cloud_store_status = ', '.join([i[1] for i in active_cloud_store]) if len(active_cloud_store) > 0 else 'NONE'
    furk_easy_suggestion = params.get('suggestion', '')
    listing = []  
    if play_params: listing += [('RESCRAPE & SELECT SOURCE', 'rescrape_select')]
    listing += [('AUTOPLAY: [I]Currently [B]%s[/B][/I]' % autoplay_status, 'toggle_autoplay')]
    if autoplay_status == 'On':
        listing += [('HEVC AUTOPLAY FILTER: [I]Currently [B]%s[/B][/I]' % autoplay_hevc_status, 'set_autoplay_hevc')]
        listing += [('AUTOPLAY NEXT EPISODE: [I]Currently [B]%s[/B][/I]' % autoplay_next_status, 'toggle_autoplay_next')]
    listing += [('ENABLE SCRAPERS: [I]Currently [B]%s[/B][/I]' % current_scrapers_status, 'enable_scrapers')]
    if autoplay_status == 'Off':
        listing += [('DISPLAY MODE: [I]Currently [B]%s[/B][/I]' % display_mode_status, 'set_display_mode')]
    listing += [('QUALITY FILTERS: [I]Currently [B]%s[/B][/I]' % current_filter_status, 'set_filters')]
    listing += [('DOWNLOAD SUBTITLES: [I]Currently [B]%s[/B][/I]' % current_subs_action_status, 'set_subs_action')]
    if settings.cache_page(): listing += [('CLEAR RESUME BROWSING PAGE', 'clear_cache_page')]
    listing += [('SWITCH INDICATOR PROVIDER: [I]Currently [B]%s[/B][/I]' % indicators_status, 'toggle_indicators')]
    if 'external' in active_scrapers:
        listing += [('CHECK FOR CACHED TORRENTS: [I]Currently [B]%s[/B][/I]' % cached_torrents_status, 'toggle_cached_torrents')]
        if cached_torrents_status == 'On':
            listing += [(' - SHOW UNCACHED TORRENTS: [I]Currently [B]%s[/B][/I]' % uncached_torrents_status, 'toggle_torrents_display_uncached')]
            listing += [(' - ADD TORRENTS TO CLOUD: [I]Currently [B]%s[/B][/I]' % active_cloud_store_status, 'set_active_cloud_store')]
    if content in ('movies', 'episodes', 'movie', 'episode'): listing += [('FURK/EASYNEWS SEARCH: [B][I]%s[/I][/B]' % furk_easy_suggestion, 'search_directly')]
    if settings.watched_indicators() in (1,2): listing += [('CLEAR TRAKT CACHE', 'clear_trakt_cache')]
    listing += [('EXTERNAL SCRAPERS MANAGER', 'open_external_scrapers_manager')]
    listing += [('OPEN TIKI META SETTINGS', 'open_meta_settings')]
    listing += [('OPEN OPENSCRAPERS SETTINGS', 'open_scraper_settings')]
    listing += [('OPEN FEN SETTINGS', 'open_fen_settings')]
    listing += [('[B]SAVE SETTINGS AND EXIT[/B]', 'save_and_exit')]
    xbmc.sleep(500)
    choice = selection_dialog([i[0] for i in listing], [i[1] for i in listing], 'Fen Options...')
    if choice == 'rescrape_select': return clear_and_rescrape(play_params)
    elif choice == 'toggle_autoplay': toggle_setting('auto_play', autoplay_toggle)
    elif choice == 'set_autoplay_hevc': set_autoplay_hevc()
    elif choice == 'toggle_autoplay_next': toggle_setting('autoplay_next_episode', autoplay_next_toggle)
    elif choice == 'enable_scrapers': enable_scrapers()
    elif choice == 'set_display_mode': set_display_mode()
    elif choice == 'set_filters': set_quality(quality_filter_setting)
    elif choice == 'set_subs_action': set_subtitle_action()
    elif choice == 'clear_cache_page': cached_page_clear(action=list_name)
    elif choice == 'toggle_indicators': toggle_setting('watched_indicators', indicators_toggle)
    elif choice == 'toggle_cached_torrents': toggle_setting('torrent.check.cache', cached_torrents_toggle)
    elif choice == 'toggle_torrents_display_uncached': toggle_setting('torrent.display.uncached', uncached_torrents_toggle)
    elif choice == 'set_active_cloud_store': set_active_cloud_store(active_cloud_store)
    elif choice == 'search_directly': furk_easynews_direct_search_choice(suggestion, from_results, list_name)
    elif choice == 'clear_trakt_cache': clear_cache('trakt')
    elif choice == 'open_external_scrapers_manager': external_scrapers_manager()
    elif choice == 'open_meta_settings': xbmc.executebuiltin('Addon.OpenSettings(script.module.tikimeta)')
    elif choice == 'open_scraper_settings': xbmc.executebuiltin('Addon.OpenSettings(script.module.openscrapers)')
    elif choice == 'open_fen_settings': open_settings('0.0')
    if choice in ('clear_cache_page', 'toggle_indicators', 'clear_trakt_cache') and content in ('movies', 'tvshows', 'seasons', 'episodes'): xbmc.executebuiltin('Container.Refresh')
    if choice in (None, 'rescrape_select', 'save_and_exit', 'clear_cache_page', 'toggle_indicators', 'clear_trakt_cache', 'search_directly', 'open_meta_settings', 'open_scraper_settings', 'open_fen_settings', 'open_external_scrapers_manager'): return
    xbmc.executebuiltin('RunPlugin(%s)' % build_url({'mode': 'playback_menu', 'from_results': from_results, 'suggestion': suggestion, 'list_name': list_name, 'play_params': play_params}))

def set_autoplay_hevc():
    from modules.settings import active_scrapers
    from modules.nav_utils import toggle_setting
    options = ['Include', 'Exclude', 'Prefer']
    options_choice = selection_dialog(options, options, 'Choose HEVC Autoplay Setting')
    if options_choice < 0: return
    return toggle_setting('autoplay_hevc', options_choice)

def furk_easynews_direct_search_choice(suggestion, from_results, list_name):
    from modules.nav_utils import build_url
    direct_search_furk_params = {'mode': 'furk.search_furk', 'db_type': 'video', 'suggestion': suggestion}
    direct_search_easynews_params = {'mode': 'easynews.search_easynews', 'suggestion': suggestion}
    choices = [('SEARCH FURK', direct_search_furk_params), ('SEARCH EASYNEWS', direct_search_easynews_params)]
    choice = selection_dialog([i[0] for i in choices], [i[1] for i in choices], 'Choose Direct Search Provider')
    if not choice: xbmc.executebuiltin('RunPlugin(%s)' % build_url({'mode': 'playback_menu', 'from_results': from_results, 'suggestion': suggestion, 'list_name': list_name}))
    else: xbmc.executebuiltin('XBMC.Container.Update(%s)' % build_url(choice))

def color_chooser(msg_dialog, no_color=False):
    color_chart = [
          'black', 'white', 'whitesmoke', 'gainsboro', 'lightgray', 'silver', 'darkgray', 'gray', 'dimgray',
          'snow', 'floralwhite', 'ivory', 'beige', 'cornsilk', 'antiquewhite', 'bisque', 'blanchedalmond',
          'burlywood', 'darkgoldenrod', 'ghostwhite', 'azure', 'lightsaltegray', 'lightsteelblue',
          'powderblue', 'lightblue', 'skyblue', 'lightskyblue', 'deepskyblue', 'dodgerblue', 'royalblue',
          'blue', 'mediumblue', 'midnightblue', 'navy', 'darkblue', 'cornflowerblue', 'slateblue', 'slategray',
          'yellowgreen', 'springgreen', 'seagreen', 'steelblue', 'teal', 'fuchsia', 'deeppink', 'darkmagenta',
          'blueviolet', 'darkviolet', 'darkorchid', 'darkslateblue', 'darkslategray', 'indigo', 'cadetblue',
          'darkcyan', 'darkturquoise', 'turquoise', 'cyan', 'paleturquoise', 'lightcyan', 'mintcream', 'honeydew',
          'aqua', 'aquamarine', 'chartreuse', 'greenyellow', 'palegreen', 'lawngreen', 'lightgreen', 'lime',
          'mediumspringgreen', 'mediumturquoise', 'lightseagreen', 'mediumaquamarine', 'mediumseagreen',
          'limegreen', 'darkseagreen', 'forestgreen', 'green', 'darkgreen', 'darkolivegreen', 'olive', 'olivedab',
          'darkkhaki', 'khaki', 'gold', 'goldenrod', 'lightyellow', 'lightgoldenrodyellow', 'lemonchiffon',
          'yellow', 'seashell', 'lavenderblush', 'lavender', 'lightcoral', 'indianred', 'darksalmon',
          'lightsalmon', 'pink', 'lightpink', 'hotpink', 'magenta', 'plum', 'violet', 'orchid', 'palevioletred',
          'mediumvioletred', 'purple', 'maroon', 'mediumorchid', 'mediumpurple', 'mediumslateblue', 'thistle',
          'linen', 'mistyrose', 'palegoldenrod', 'oldlace', 'papayawhip', 'moccasin', 'navajowhite', 'peachpuff',
          'sandybrown', 'peru', 'chocolate', 'orange', 'darkorange', 'tomato', 'orangered', 'red', 'crimson',
          'salmon', 'coral', 'firebrick', 'brown', 'darkred', 'tan', 'rosybrown', 'sienna', 'saddlebrown'
          ]
    color_display = ['[COLOR=%s]%s[/COLOR]' % (i, i.capitalize()) for i in color_chart]
    if no_color:
        color_chart.insert(0, 'No Color')
        color_display.insert(0, 'No Color')
    choice = selection_dialog(color_display, color_chart, msg_dialog)
    if not choice: return
    return choice

def get_release_quality(release_name, release_link=None):
    import re
    try:
        if release_name is None: return
        quality = None
        release_name = replace_html_codes(release_name)
        fmt = re.sub('[^A-Za-z0-9]+', ' ', release_name)
        fmt = fmt.encode('utf-8')
        fmt = str(fmt.lower())
        fmt = fmt.lower()
        fmtl = list(fmt.split(' '))
        if any(i in ['dvdscr', 'r5', 'r6'] for i in fmtl): quality = 'SCR'
        elif any(i in ['camrip', 'hdcam', 'dvdcam', 'cam'] for i in fmtl): quality = 'CAM'
        elif any(i in ['tc', 'tsrip', 'hdts', 'dvdts', 'hdtc', 'telecine', 'tc720p', 'tc720', 'hd-tc', 'telesync', 'ts'] for i in fmtl): quality = 'TELE'
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
        if not quality:
            if release_link:
                release_link = replace_html_codes(release_link)
                fmt = re.sub('[^A-Za-z0-9]+', ' ', release_link)
                fmt = fmt.encode('utf-8')
                fmt = str(fmt.lower())
                fmt = fmt.lower()
                fmtl = list(fmt.split(' '))
                if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
                elif any(i in ['camrip', 'hdcam', 'dvdcam', 'cam'] for i in fmt): quality = 'CAM'
                elif any(i in ['tc', 'tsrip', 'hdts', 'dvdts', 'hdtc', 'telecine', 'tc720p', 'tc720', 'hd-tc', 'telesync', 'ts'] for i in fmt): quality = 'TELE'
                elif ' 4k ' in fmt: quality = '4K'
                elif ' 2160 ' in fmt: quality = '4K'
                elif ' 2160p ' in fmt: quality = '4K'
                elif ' uhd ' in fmt: quality = '4K'
                elif ' 1080 ' in fmt: quality = '1080p'
                elif ' 1080p ' in fmt: quality = '1080p'
                elif ' fullhd ' in fmt: quality = '1080p'
                elif ' 720p ' in fmt: quality = '720p'
                elif ' hd ' in fmt: quality = '720p'
                else: quality = 'SD'
            else: quality = 'SD'
        return quality
    except:
        return 'SD'

def get_file_info(url):
    import re
    try:
        url = replace_html_codes(url)
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
    if ' 3d ' in url:
        info += ' 3D |'
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



