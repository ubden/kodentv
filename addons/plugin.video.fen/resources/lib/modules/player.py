# -*- coding: utf-8 -*-
import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
import sys, os
try: from urllib import unquote
except ImportError: from urllib.parse import unquote
import json
import re
try: from urlparse import parse_qsl
except ImportError: from urllib.parse import parse_qsl
from apis.opensubtitles_api import OpenSubtitlesAPI
from modules.indicators_bookmarks import detect_bookmark, erase_bookmark
from modules.nav_utils import hide_busy_dialog, close_all_dialog, notification
from modules.utils import sec2time
from modules import settings
# from modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
window = xbmcgui.Window(10000)

class FenPlayer(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)
        self.set_resume = settings.set_resume()
        self.set_watched = settings.set_watched()
        self.autoplay_nextep = settings.autoplay_next_episode()
        self.nextep_threshold = settings.nextep_threshold()
        self.nextep_info = None
        self.delete_nextep_playcount = True
        self.media_marked = False
        self.subs_searched = False

    def run(self, url=None):
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        rootname = params.get('rootname', '')
        url = url if url else params.get("url") if 'url' in params else None
        url = unquote(url)
        if not url: return
        try:
            if rootname in ('video', 'music'):
                p_list = xbmc.PLAYLIST_VIDEO if rootname == 'video' else xbmc.PLAYLIST_MUSIC
                playlist = xbmc.PlayList(p_list)
                playlist.clear()
                listitem = xbmcgui.ListItem()
                listitem.setInfo(type=rootname, infoLabels={})
                playlist.add(url, listitem)
                return self.play(playlist)
            self.meta = json.loads(window.getProperty('fen_media_meta'))
            rootname = self.meta['rootname'] if 'rootname' in self.meta else ''
            bookmark = self.bookmarkChoice()
            if bookmark == -1: return
            self.meta.update({'url': url, 'bookmark': bookmark})
            listitem = xbmcgui.ListItem(path=url)
            try:
                if self.meta.get('use_animated_poster', False): poster = self.meta.get('gif_poster')
                else: poster = self.meta.get('poster')
                listitem.setProperty('StartPercent', str(self.meta.get('bookmark')))
                listitem.setArt({'poster': poster, 'fanart': self.meta.get('fanart'), 'banner': self.meta.get('banner'),
                                'clearart': self.meta.get('clearart'), 'clearlogo': self.meta.get('clearlogo'),
                                'landscape': self.meta.get('landscape'), 'discart': self.meta.get('discart')})
                listitem.setCast(self.meta['cast'])
                if self.meta['vid_type'] == 'movie':
                    listitem.setUniqueIDs({'imdb': str(self.meta['imdb_id']), 'tmdb': str(self.meta['tmdb_id'])})
                    listitem.setInfo(
                        'video', {'mediatype': 'movie', 'trailer': str(self.meta['trailer']),
                        'title': self.meta['title'], 'size': '0', 'duration': self.meta['duration'],
                        'plot': self.meta['plot'], 'rating': self.meta['rating'], 'premiered': self.meta['premiered'],
                        'studio': self.meta['studio'],'year': self.meta['year'], 'genre': self.meta['genre'],
                        'tagline': self.meta['tagline'], 'code': self.meta['imdb_id'], 'imdbnumber': self.meta['imdb_id'],
                        'director': self.meta['director'], 'writer': self.meta['writer'], 'votes': self.meta['votes']})
                elif self.meta['vid_type'] == 'episode':
                    listitem.setUniqueIDs({'imdb': str(self.meta['imdb_id']), 'tmdb': str(self.meta['tmdb_id']), 'tvdb': str(self.meta['tvdb_id'])})
                    listitem.setInfo(
                        'video', {'mediatype': 'episode', 'trailer': str(self.meta['trailer']), 'title': self.meta['ep_name'], 'imdbnumber': self.meta['imdb_id'],
                        'tvshowtitle': self.meta['title'], 'size': '0', 'plot': self.meta['plot'], 'year': self.meta['year'], 'votes': self.meta['votes'],
                        'premiered': self.meta['premiered'], 'studio': self.meta['studio'], 'genre': self.meta['genre'], 'season': int(self.meta['season']),
                        'episode': int(self.meta['episode']), 'duration': str(self.meta['duration']), 'rating': self.meta['rating']})
            except Exception as e:
                from modules.utils import logger
                logger('exception in meta set code', e)
                pass
            library_item = True if 'from_library' in self.meta else False
            if library_item: xbmcplugin.setResolvedUrl(__handle__, True, listitem)
            else: self.play(url, listitem)
            self.monitor()
        except Exception as e:
            from modules.utils import logger
            logger('exception in main code', e)
            return

    def bookmarkChoice(self):
        season = self.meta.get('season', '')
        episode = self.meta.get('episode', '')
        if season == 0: season = ''
        if episode == 0: episode = ''
        bookmark = 0
        try: resume_point, curr_time = detect_bookmark(self.meta['vid_type'], self.meta['media_id'], season, episode)
        except: resume_point = 0
        resume_check = float(resume_point)
        if resume_check > 0:
            percent = str(resume_point)
            raw_time = float(curr_time)
            _time = sec2time(raw_time, n_msec=0)
            bookmark = self.getResumeStatus(_time, percent, bookmark, self.meta.get('from_library', None))
            if bookmark == 0: erase_bookmark(self.meta['vid_type'], self.meta['media_id'], season, episode)
        return bookmark

    def getResumeStatus(self, _time, percent, bookmark, from_library):
        if settings.auto_resume(): return percent
        dialog = xbmcgui.Dialog()
        xbmc.sleep(600)
        choice = dialog.contextmenu(['Resume from [B]%s[/B]' % _time, 'Start from Beginning'])
        return percent if choice == 0 else bookmark if choice == 1 else -1

    def monitor(self):
        self.library_setting = 'library' if 'from_library' in self.meta else None
        self.autoplay_next_episode = True if self.meta['vid_type'] == 'episode' and self.autoplay_nextep else False
        while not self.isPlayingVideo():
            xbmc.sleep(100)
        close_all_dialog()
        while self.isPlayingVideo():
            try:
                xbmc.sleep(1000)
                self.total_time = self.getTotalTime()
                self.curr_time = self.getTime()
                self.current_point = round(float(self.curr_time/self.total_time*100),1)
                if self.current_point >= self.set_watched and not self.media_marked:
                    self.mediaWatchedMarker()
                if self.autoplay_next_episode:
                    if self.current_point >= self.nextep_threshold:
                        if not self.nextep_info:
                            self.nextEpPrep()
                        else: pass
            except: pass
            if not self.subs_searched: self.fetch_subtitles()
        if not self.media_marked: self.mediaWatchedMarker()
        self.refresh_container()

    def mediaWatchedMarker(self):
        try:
            if self.set_resume < self.current_point < self.set_watched:
                from modules.indicators_bookmarks import set_bookmark
                self.media_marked = True
                set_bookmark(self.meta['vid_type'], self.meta['media_id'], self.curr_time, self.total_time, self.meta.get('season', ''), self.meta.get('episode', ''))
            elif self.current_point > self.set_watched:
                self.media_marked = True
                if self.meta['vid_type'] == 'movie':
                    from modules.indicators_bookmarks import mark_movie_as_watched_unwatched, get_watched_info_movie
                    watched_function = mark_movie_as_watched_unwatched
                    watched_update = get_watched_info_movie
                    watched_params = {"mode": "mark_movie_as_watched_unwatched", "action": 'mark_as_watched',
                    "media_id": self.meta['media_id'], "title": self.meta['title'], "year": self.meta['year'],
                    "refresh": 'false', 'from_playback': 'true'}
                else:
                    from modules.indicators_bookmarks import mark_episode_as_watched_unwatched, get_watched_info_tv
                    watched_function = mark_episode_as_watched_unwatched
                    watched_update = get_watched_info_tv
                    watched_params = {"mode": "mark_episode_as_watched_unwatched", "action": "mark_as_watched",
                    "season": self.meta['season'], "episode": self.meta['episode'], "media_id": self.meta['media_id'],
                    "title": self.meta['title'], "year": self.meta['year'], "imdb_id": self.meta['imdb_id'],
                    "tvdb_id": self.meta["tvdb_id"], "refresh": 'false', 'from_playback': 'true'}
                watched_function(watched_params)
                xbmc.sleep(1000)
                watched_info = watched_update()[0]
        except: pass

    def nextEpPrep(self):
        auto_nextep_limit_reached = False
        autoplay_next_check_threshold = settings.autoplay_next_check_threshold()
        try: current_number = int(window.getProperty('current_autoplay_next_number'))
        except: current_number = 1
        if autoplay_next_check_threshold != 0:
            if current_number == autoplay_next_check_threshold:
                auto_nextep_limit_reached = True
                continue_playing = xbmcgui.Dialog().yesno('Fen Next Episode', '[B]Are you still watching %s?[/B]' % self.meta['title'], '', '', 'Not Watching', 'Still Watching', 10000)
                if not continue_playing == 1:
                    notification('Fen Next Episode Cancelled', 6000)
                    self.nextep_info = {'pass': True}
        if not self.nextep_info:
            from modules.next_episode import nextep_playback_info, nextep_play
            self.nextep_info = nextep_playback_info(self.meta['tmdb_id'], int(self.meta['season']), int(self.meta['episode']), self.library_setting)
            if not self.nextep_info.get('pass', False):
                if not auto_nextep_limit_reached: self.delete_nextep_playcount = False
                window.setProperty('current_autoplay_next_number', str(current_number+1))
                nextep_play(self.nextep_info)

    def fetch_subtitles(self):
        self.subs_searched = True
        season = int(self.meta['season']) if self.meta['vid_type'] == 'episode' else None
        episode = int(self.meta['episode']) if self.meta['vid_type'] == 'episode' else None
        try: Subtitles().get(self.meta['title'], self.meta['imdb_id'], season, episode)
        except: pass

    def refresh_container(self):
        if self.media_marked:
            xbmc.sleep(500)
            xbmc.executebuiltin("Container.Refresh")

    def onAVStarted(self):
        try: close_all_dialog()
        except: pass

    def onPlayBackStarted(self):
        try: close_all_dialog()
        except: pass

    # def onPlayBackEnded(self):
    #     try: self.playlist.clear()
    #     except: pass

    # def onPlayBackStopped(self):
    #     try: self.playlist.clear()
    #     except: pass

    def playAudioAlbum(self, t_files=None, name=None, from_seperate=False):
        import os
        import xbmcaddon
        from modules.utils import clean_file_name, batch_replace, to_utf8
        from modules.nav_utils import setView
        icon_directory = settings.get_theme()
        default_furk_icon = os.path.join(icon_directory, 'furk.png')
        formats = ('.3gp', ''), ('.aac', ''), ('.flac', ''), ('.m4a', ''), ('.mp3', ''), \
        ('.ogg', ''), ('.raw', ''), ('.wav', ''), ('.wma', ''), ('.webm', ''), ('.ra', ''), ('.rm', '')
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        furk_files_list = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        if from_seperate: t_files = [i for i in t_files if clean_file_name(i['path']) == params.get('item_path')]
        for item in t_files:
            try:
                name = item['path'] if not name else name
                if not 'audio' in item['ct']: continue
                url = item['url_dl']
                track_name = clean_file_name(batch_replace(to_utf8(item['name']), formats))
                listitem = xbmcgui.ListItem(track_name)
                listitem.setThumbnailImage(default_furk_icon)
                listitem.setInfo(type='music',infoLabels={'title': track_name, 'size': int(item['size']), 'album': clean_file_name(batch_replace(to_utf8(name), formats)),'duration': item['length']})
                listitem.setProperty('mimetype', 'audio/mpeg')
                playlist.add(url, listitem)
                if from_seperate: furk_files_list.append((url, listitem, False))
            except: pass
        self.play(playlist)
        if from_seperate:
            xbmcplugin.addDirectoryItems(__handle__, furk_files_list, len(furk_files_list))
            setView('view.furk_files')
            xbmcplugin.endOfDirectory(__handle__)

class Subtitles(xbmc.Player):
    def __init__(self):
        self.opensubtitles = OpenSubtitlesAPI()
        self.auto_enable = __addon__.getSetting('subtitles.auto_enable')
        self.subs_action = __addon__.getSetting('subtitles.subs_action')
        self.settings_language1 = __addon__.getSetting('subtitles.language')
        self.settings_language2 = __addon__.getSetting('subtitles.language2')
        self.manual_selection = True
        self.show_notification = __addon__.getSetting('subtitles.show_notification')
        self.quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webdl', 'webrip', 'webcap', 'web', 'hdtv', 'hdrip']
        self.language_dict = {'None': None,
            'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm',
            'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre',
            'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi',
            'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut',
            'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin',
            'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger',
            'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun',
            'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn',
            'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav',
            'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may',
            'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne',
            'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol',
            'Portuguese': 'por', 'Portuguese(Brazil)': 'pob', 'Romanian': 'rum',
            'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo',
            'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe',
            'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel',
            'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}
        self.language1 = self.language_dict[self.settings_language1]
        self.language2 = self.language_dict[self.settings_language2]

    def get(self, query, imdb_id, season, episode):
        def _notification(line, _time=3500):
            if self.show_notification: return notification(line, _time)
            else: return
        def _video_file_subs():
            try: available_sub_language = xbmc.Player().getSubtitles()
            except: available_sub_language = ''
            if available_sub_language in (self.language1, self.language2):
                if self.auto_enable == 'true': xbmc.Player().showSubtitles(True)
                _notification('Local Subtitles Found')
                return True
            return False
        def _downloaded_subs():
            files = xbmcvfs.listdir(subtitle_path)[1]
            if len(files) > 0:
                match_lang1 = None
                match_lang2 = None
                files = [i for i in files if i.endswith('.srt')]
                for item in files:
                    if item == search_filename:
                        match_lang1 = item
                        break
                    if search_filename2:
                        if item == search_filename2:
                            match_lang2 = item
                final_match = match_lang1 if match_lang1 else match_lang2 if match_lang2 else None
                if final_match:
                    subtitle = os.path.join(subtitle_path, final_match)
                    _notification('Downloaded Subtitles Found')
                    return subtitle
            return False
        def _searched_subs():
            chosen_sub = None
            search_language = self.language1
            result = self.opensubtitles.search(query, imdb_id, search_language, season, episode)
            if not result or len(result) == 0:
                search_language = self.language2
                if self.language2 == None:
                    _notification('No Subtitles Found')
                    return False
                _notification('Searching Secondary Language...', _time=1500)
                result = self.opensubtitles.search(query, imdb_id, self.language2, season, episode)
                if not result or len(result) == 0:
                    _notification('No Subtitles Found')
                    return False
            try: video_path = self.getPlayingFile()
            except: video_path = ''
            if '|' in video_path: video_path = video_path.split('|')[0]
            video_path = os.path.basename(video_path)
            if self.subs_action == 'Select':
                from modules.utils import selection_dialog
                xbmc.Player().pause()
                choices = [i for i in result if i['SubLanguageID'] == search_language and i['SubSumCD'] == '1']
                dialog_list = ['%02d | [B]%s[/B] |[I]%s[/I]' % (c, i['SubLanguageID'].upper(), i['MovieReleaseName']) for c, i in enumerate(choices, 1)]
                string = 'SUBTITLES - %s' % video_path
                chosen_sub = selection_dialog(dialog_list, choices, string)
                xbmc.Player().pause()
                if not chosen_sub:
                    _notification('No Subtitles Selected', _time=1500)
                    return False
            else:
                try: chosen_sub = [i for i in result if i['MovieReleaseName'].lower() in video_path.lower() and i['SubLanguageID'] == search_language and i['SubSumCD'] == '1'][0]
                except: pass
                if not chosen_sub:
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-', video_path)
                    fmt = [i.lower() for i in fmt]
                    fmt = [i for i in fmt if i in self.quality]
                    if season and fmt == '': fmt = 'hdtv'
                    result = [i for i in result if i['SubSumCD'] == '1']
                    filter = [i for i in result if i['SubLanguageID'] == search_language and any(x in i['MovieReleaseName'].lower() for x in fmt) and any(x in i['MovieReleaseName'].lower() for x in self.quality)]
                    filter += [i for i in result if any(x in i['MovieReleaseName'].lower() for x in self.quality)]
                    filter += [i for i in result if i['SubLanguageID'] == search_language]
                    if len(filter) > 0: chosen_sub = filter[0]
                    else: chosen_sub = result[0]; _notification('No Suitable Subtitles Found. Loading First Result')
            try: lang = xbmc.convertLanguage(chosen_sub['SubLanguageID'], xbmc.ISO_639_2)
            except: lang = chosen_sub['SubLanguageID']
            insert_name = sub_filename + '_%s.srt' % lang
            subtitle = os.path.join(subtitle_path, insert_name)
            download_url = chosen_sub['SubDownloadLink']
            content = self.opensubtitles.download(download_url)
            file = xbmcvfs.File(subtitle, 'w')
            file.write(str(content))
            file.close()
            xbmc.sleep(1000)
            return subtitle
        if self.subs_action == 'Off': return
        xbmc.sleep(2500)
        imdb_id = re.sub('[^0-9]', '', imdb_id)
        subtitle_path = xbmc.translatePath('special://temp/')
        sub_filename = 'FENSubs_%s_%s_%s' % (imdb_id, season, episode) if season else 'FENSubs_%s' % imdb_id
        search_filename = sub_filename + '_%s.srt' % self.language1
        if self.language2: search_filename2 = sub_filename + '_%s.srt' % self.language2
        else: search_filename2 = None
        subtitle = _video_file_subs()
        if subtitle: return
        subtitle = _downloaded_subs()
        if subtitle: return xbmc.Player().setSubtitles(subtitle)
        subtitle = _searched_subs()
        if subtitle: return xbmc.Player().setSubtitles(subtitle)






