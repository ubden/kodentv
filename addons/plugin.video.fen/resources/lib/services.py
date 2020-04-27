import xbmc, xbmcgui, xbmcaddon
import sys
import time
from datetime import datetime, timedelta
import _strptime  # fix bug in python import
from modules import settings
# from modules.utils import logger



__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
window = xbmcgui.Window(10000)

class VersionCheck:
    def run(self):
        xbmc.log("[FEN] VersionCheck Service Starting...", 2)
        fen_version = __addon__.getAddonInfo('version')
        tikimeta_version = xbmcaddon.Addon(id='script.module.tikimeta').getAddonInfo('version')
        tikiart_version = xbmcaddon.Addon(id='script.tiki.artwork').getAddonInfo('version')
        openscrapers_version = xbmcaddon.Addon(id='script.module.openscrapers').getAddonInfo('version')
        xbmc.log("[FEN] Current FEN Version: %s" % fen_version, 2)
        xbmc.log("[FEN] Current TIKIMETA Version: %s" % tikimeta_version, 2)
        xbmc.log("[FEN] Current TIKIART Version: %s" % tikiart_version, 2)
        xbmc.log("[FEN] Current OPENSCRAPERS Version: %s" % openscrapers_version, 2)
        xbmc.log("[FEN] Killing VersionCheck Service", 2)

class CheckSettings:
    def run(self):
        from modules.nav_utils import settings_layout
        xbmc.log("[FEN] Check Settings Service Starting...", 2)
        settings_layout()
        xbmc.log("[FEN] Killing Check Settings Service", 2)

class AutoRun:
    def run(self):
        xbmc.log("[FEN] Autostart Service Starting...", 2)
        if settings.auto_start_fen():
            xbmc.log("[FEN] Killing Autostart Service", 2)
            return xbmc.executebuiltin('RunAddon(plugin.video.fen)')
        else: 
            xbmc.log("[FEN] Killing Autostart Service", 2)
            return

class SubscriptionsUpdater:             
    def run(self):
        xbmc.log("[FEN] Subscription service starting...")
        hours = settings.subscription_timer()
        while not xbmc.abortRequested:
            if settings.subscription_update():
                try:
                    next_run  = datetime.fromtimestamp(time.mktime(time.strptime(__addon__.getSetting('service_time'), "%Y-%m-%d %H:%M:%S")))
                    now = datetime.now()
                    if now > next_run:
                        if xbmc.Player().isPlaying() == False:
                            if xbmc.getCondVisibility('Library.IsScanningVideo') == False:
                                xbmc.sleep(3000)
                                xbmc.log("[FEN] Updating video subscriptions")
                                xbmc.executebuiltin('RunPlugin(plugin://plugin.video.fen/?&mode=update_subscriptions)')
                                xbmc.sleep(500)
                                if __addon__.getSetting('subsciptions.update_type') == '1':
                                    next_update = datetime.now() + timedelta(hours=24)
                                    next_update = next_update.strftime('%Y-%m-%d') + ' %s:00' % __addon__.getSetting('subscriptions_update_label2')
                                else:
                                    next_update = str(now + timedelta(hours=hours)).split('.')[0]
                                __addon__.setSetting('service_time', next_update)
                                xbmc.sleep(500)
                                xbmc.log("[FEN] Subscriptions updated. Next run at " + __addon__.getSetting('service_time'), 2)
                                xbmc.sleep(3000)
                        else:
                            xbmc.log("[FEN] Player is running, waiting until finished")
                except: pass
            xbmc.sleep(3000)

VersionCheck().run()
CheckSettings().run()
AutoRun().run()
SubscriptionsUpdater().run()
