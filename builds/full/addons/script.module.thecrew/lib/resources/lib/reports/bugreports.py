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
import re
import traceback

import xbmc
import xbmcgui
import xbmcaddon

from resources.lib.reports import themecontrol
from resources.lib.modules import control, log_utils, webform

br_file = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L1F4cE50V0NC'.decode('base64')

def BugReporter(open_bugs=None):
    class BugReporter_Window(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()
            self.report_text = themecontrol.getDialogText(br_file)
            self.open_bugs = open_bugs

            self.br_text = 102
            self.br_input = 103
            self.br_open = 104
            self.btn_submit = 201
            self.btn_close = 202

            self.showdialog()

        def showdialog(self):
            self.setProperty('dhtext', self.colors.dh_color)
            self.getControl(self.br_text).setText(self.report_text)
            self.getControl(self.br_open).setText(self.open_bugs)
            self.setFocusId(self.btn_close)

        def onClick(self, controlId):
            if controlId == self.btn_close:
                self.close()
            elif controlId == self.btn_submit:
                reportText = self.getControl(self.br_input).getText()
                if len(reportText) == 0:
                    xbmc.executebuiltin("XBMC.Notification(%s, %s, %s, %s)" % ('The Crew Bug Report', 'Bug Report Incomplete', 4000, control.addonIcon()))
                    return
                self.close()
                result = webform.webform().bug_report('The Crew', reportText)
                if result is None:
                    # Wait before submitting another report you fuckin spammer
                    xbmc.executebuiltin("XBMC.Notification(%s, %s, %s, %s)" % ('The Crew Bug Report', 'Wait Before Next Submission', 4000, control.addonIcon()))
                elif result is False:
                    # Failed to send. Site timed out or is down. Ya'll suck
                    xbmc.executebuiltin("XBMC.Notification(%s, %s, %s, %s)" % ('The Crew Bug Report', 'Submission Failed', 4000, control.addonIcon()))
                elif result is True:
                    # Bug Report worked, FUCK YEAH!
                    xbmc.executebuiltin("XBMC.Notification(%s, %s, %s, %s)" % ('The Crew Bug Report', 'Bug Report Completed', 4000, control.addonIcon()))

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()

    open_bugs=webform.webform().get_bugs()
    viewer = BugReporter_Window('BugReporter.xml', themecontrol.skinModule(), themecontrol.skinTheme(), '1080i', open_bugs=open_bugs)
    viewer.doModal()
    del viewer
