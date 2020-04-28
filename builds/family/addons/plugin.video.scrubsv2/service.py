# -*- coding: utf-8 -*-

import threading
from resources.lib.modules import control,log_utils

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

try:
    AddonVersion = control.addon('plugin.video.scrubsv2').getAddonInfo('version')
    ModuleVersion = control.addon('script.module.scrubsv2').getAddonInfo('version')
    RepoVersion = control.addon('repository.jewrepo').getAddonInfo('version')
    log_utils.log('===-[AddonVersion: %s]-' % str(AddonVersion) + '-[ModuleVersion: %s]-' % str(ModuleVersion) + '-[RepoVersion: %s]-' % str(RepoVersion), log_utils.LOGNOTICE)
except:
    log_utils.log('===-[Error Oppps...', log_utils.LOGNOTICE)
    log_utils.log('===-[Had Trouble Getting Version Info. Make Sure You Have the JewRepo.', log_utils.LOGNOTICE)

def syncTraktLibrary():
    control.execute('RunPlugin(plugin://%s)' % 'plugin.video.scrubsv2/?action=tvshowsToLibrarySilent&url=traktcollection')
    control.execute('RunPlugin(plugin://%s)' % 'plugin.video.scrubsv2/?action=moviesToLibrarySilent&url=traktcollection')

if control.setting('autoTraktOnStart') == 'true':
    syncTraktLibrary()

if int(control.setting('schedTraktTime')) > 0:
    log_utils.log('===-[Starting Trakt Scheduling.', log_utils.LOGNOTICE)
    log_utils.log('===-[Scheduled Time Frame '+ control.setting('schedTraktTime')  + ' Hours.', log_utils.LOGNOTICE)
    timeout = 3600 * int(control.setting('schedTraktTime'))
    schedTrakt = threading.Timer(timeout, syncTraktLibrary)
    schedTrakt.start()

