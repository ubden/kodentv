# -*- coding: utf-8 -*-
#########################################################
# SCRIPT  : script.py                                   #
#           Script handling commands for WebGrab++      #
#           I. Helwegen 2015                            #
#########################################################

####################### IMPORTS #########################
import sys, os
import xbmc, xbmcaddon, xbmcgui
from threading import Timer

#########################################################

####################### GLOBALS #########################
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('id')
__addonpath__ = __addon__.getAddonInfo('path')
#__LS__ = __addon__.getLocalizedString

### CONTROLS ###
BUTTON_UP    = 10
BUTTON_DOWN  = 20
BUTTON_LIVE  = 30
FIELD_TEXT   = 40
BUTTON_EXIT  = 50
LABEL_TITLE  = 60

CANCEL_DIALOG = (9, 10, 216, 247, 257, 275, 61448, 61467)
FIELD_LINES = 38
SCROLL_LINES = FIELD_LINES - 2
UPDATE_TIME = 0.1

LOGFILE = xbmc.translatePath(os.path.join('special://temp/', 'kodi.log'))

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
    
class GUI(xbmcgui.WindowXMLDialog):
	
    def __init__(self, *args, **kwargs):
        self.AutoMode = True
        self.Complete = None
        self.Line = 0
        self.LogFile = LOGFILE
        self.rt = None
      
    def onInit(self):
        self.getControl(LABEL_TITLE).setLabel("Kodi Log Viewer")

        if self.CheckService(False):
             self.rt = RepeatedTimer(UPDATE_TIME, self.CheckService, [self, True])

    def onClick(self, controlId):
        if (controlId == BUTTON_UP):
            if self.AutoMode == True:
                self.Complete = self.cat(self.LogFile)
                self.Line = len(self.Complete) - FIELD_LINES
                self.AutoMode = False
            self.UpdateTextBox(self.GetLines(True),Up=True)
        if (controlId == BUTTON_DOWN):
            if self.AutoMode == True:
                self.Complete = self.cat(self.LogFile)
                self.Line = len(self.Complete) - FIELD_LINES
                self.AutoMode = False
            self.UpdateTextBox(self.GetLines(False),Down=True)
        if (controlId == BUTTON_LIVE):
            self.Line = 0
            self.Complete = None
            self.AutoMode = True
        if (controlId == BUTTON_EXIT):
            self.ExitScript()

    def onAction(self, action):
        if (action.getButtonCode() in CANCEL_DIALOG):
            self.ExitScript()

    def ExitScript(self):
        if self.rt != None:
            self.rt.stop()
        self.Complete = None
        self.close()
        
    def CreateString(self, block, startgrey=False, endgrey=False):
        retstr = ""
        cnt = 0
        while cnt<len(block): 
            data=block[cnt].strip('\n')
            line=(data[:160] + '..') if len(data) > 160 else data
            if startgrey and cnt<2:
                retstr="%s[COLOR=FF999999]"%retstr
            elif endgrey and (cnt>FIELD_LINES-3):
                retstr="%s[COLOR=FF999999]"%retstr
            retstr=("%s%s"%(retstr,line))
            if startgrey and cnt<2:
                retstr="%s[/COLOR]"%retstr
            elif endgrey and (cnt>FIELD_LINES-3):
                retstr="%s[/COLOR]"%retstr
            if (cnt<len(block)-1):
                retstr=("%s[CR]"%retstr)
            cnt += 1
        return retstr
        
    def tail(self, filename, lines=1, _buffer=4098):
        lines_found = []
        block_counter = -1
    
        f = open(filename)
        while len(lines_found) < lines:
            try:
                f.seek(block_counter * _buffer, os.SEEK_END)
            except IOError:  # either file is too small, or too many lines requested
                f.seek(0)
                lines_found = f.readlines()
                break

            lines_found = f.readlines()

            if len(lines_found) > lines:
                break

            block_counter -= 1
        f.close()

        return lines_found[-lines:]
        
    def cat(self, filename, lines=10000, _buffer=4098):
        return self.tail(filename, 10000)
        
    def UpdateTextBox(self, Lines, Up=False, Down=False):
        self.getControl(FIELD_TEXT).setText(self.CreateString(Lines,Down,Up))
        
    def GetLines(self, Up):
        if Up == True:
            if (self.Line-SCROLL_LINES>0):
                self.Line -= SCROLL_LINES
            else:
                self.Line = 0
        else: # Down
            if (self.Line+SCROLL_LINES+FIELD_LINES<len(self.Complete)):
                self.Line += SCROLL_LINES
            else:
                self.Line = len(self.Complete) - FIELD_LINES
        return self.Complete[self.Line:self.Line+FIELD_LINES]

    def CheckService(self, Timed):
        if self.AutoMode == True:
            self.UpdateTextBox(self.tail(self.LogFile,FIELD_LINES))
        return True

#########################################################

#########################################################
######################## MAIN ###########################
#########################################################
__gui_type = "Classic" if __addon__.getSetting('gui_type').upper() == 'CLASSIC' else "Default"
ui = GUI("%s.xml" % __addonname__.replace(".","-") , __addonpath__, __gui_type)
ui.doModal()
del ui

