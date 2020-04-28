# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: The Crew
# Addon id: plugin.video.thecrew
# Addon Provider: The Crew
# Thanks Muad!

import os
import requests
import xml.etree.ElementTree as ET

import xbmcaddon

from resources.lib.modules import control

ACTION_PREVIOUS_MENU = 10  # ESC action
ACTION_NAV_BACK = 92  # Backspace action
ACTION_MOVE_LEFT = 1  # Left arrow key
ACTION_MOVE_RIGHT = 2  # Right arrow key
ACTION_MOVE_UP = 3  # Up arrow key
ACTION_MOVE_DOWN = 4  # Down arrow key
ACTION_MOUSE_WHEEL_UP = 104  # Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN = 105  # Mouse wheel down
ACTION_MOVE_MOUSE = 107  # Down arrow key
ACTION_SELECT_ITEM = 7  # Number Pad Enter
ACTION_BACKSPACE = 110  # ?
ACTION_MOUSE_LEFT_CLICK = 100
ACTION_MOUSE_LONG_CLICK = 108

MENU_ACTIONS = [ACTION_MOVE_UP, ACTION_MOVE_DOWN, ACTION_MOUSE_WHEEL_UP, ACTION_MOUSE_WHEEL_DOWN, ACTION_MOVE_MOUSE]

artPath = control.artPath()
_addon = xbmcaddon.Addon(id='plugin.video.thecrew')
addonname = _addon.getAddonInfo('name')

bg_news = os.path.join(artPath, 'newsbg.png')
bg_mid = os.path.join(artPath, 'bg_mid.png')
bg_ok = os.path.join(artPath, 'okbg.png')
bg_mdialog = os.path.join(artPath, 'mdialogbg.png')
btn_focus = os.path.join(artPath, 'onfocus.png')
btn_nofocus = os.path.join(artPath, 'onnofocus.png')
trakt_icon = os.path.join(artPath, 'trakticon.png')


class ThemeColors():
    def __init__(self):
        self.colors()

    def colors(self):
        tree = ET.parse(os.path.join(skinSubPath(), 'colors', 'colors.xml'))
        root = tree.getroot()
        for item in root.findall('color'):
            self.dh_color = item.find('dialogheader').text
            self.dt_color = item.find('dialogtext').text
            self.mh_color = item.find('menuheader').text
            self.mt_color = item.find('menutext').text
            self.link_color = item.find('link').text
            self.focus_textcolor = item.find('focustext').text
            self.btn_focus = item.find('focusbutton').text


class ThemeSounds():
    def __init__(self):
        self.sounds()

    def sounds(self):
        tree = ET.parse(os.path.join(skinAudioPath(), 'sounds.xml'))
        root = tree.getroot()
        if control.setting('notifyvoice') == 'true':
            sound_root = 'voice_'
        else:
            sound_root = 'system_'

        for item in root.findall(sound_root + 'actions'):
            self.select = os.path.join(skinAudioPath(), item.find('select').text)
            self.parentdir = os.path.join(skinAudioPath(), item.find('parentdir').text)
            self.previusmenu = os.path.join(skinAudioPath(), item.find('previusmenu').text)
            self.screenshot = os.path.join(skinAudioPath(), item.find('screenshot').text)
        for item in root.findall(sound_root + 'windows'):
            self.notifyerror = os.path.join(skinAudioPath(), item.find('notifyerror').text)
            self.notifyinfo = os.path.join(skinAudioPath(), item.find('notifyinfo').text)
            self.notifywarning = os.path.join(skinAudioPath(), item.find('notifywarning').text)


def getDialogText(url):
    try:
        message = requests.get(url).content

        if message is None:
            return 'Nothing today! Blame CNN'
        if '[link]' in message:
            tcolor = '[COLOR %s]' % (ThemeColors().link_color)
            message = message.replace('[link]', tcolor).replace('[/link]', '[/COLOR]')
        return message
    except Exception:
        return 'Nothing today! Blame CNN'


def skinTheme():
    theme = control.appearance()
    if theme in ['-', '']:
        return
    elif control.condVisibility('System.HasAddon(script.thecrew.artwork)'):
        return theme


def skinModule():
    theme = control.appearance()
    if theme in ['-', '']:
        return
    elif control.condVisibility('System.HasAddon(script.thecrew.artwork)'):
        aModule = xbmcaddon.Addon('script.thecrew.artwork').getSetting('artwork_module')
        return os.path.join(xbmcaddon.Addon(aModule).getAddonInfo('path'))


def skinSubPath():
    theme = control.appearance()
    if theme in ['-', '']:
        return
    elif control.condVisibility('System.HasAddon(script.thecrew.artwork)'):
        aModule = xbmcaddon.Addon('script.thecrew.artwork').getSetting('artwork_module')
        return os.path.join(xbmcaddon.Addon(aModule).getAddonInfo('path'), 'resources', 'skins', theme)


def skinAudioPath():
    theme = control.appearance()
    if theme in ['-', '']:
        return
    elif control.condVisibility('System.HasAddon(script.thecrew.artwork)'):
        aModule = xbmcaddon.Addon('script.thecrew.artwork').getSetting('artwork_module')
        return os.path.join(xbmcaddon.Addon(aModule).getAddonInfo('path'), 'resources', 'skins', theme, 'sounds')
