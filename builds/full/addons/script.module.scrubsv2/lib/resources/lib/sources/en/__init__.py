# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 03-21-2019 by JewBMX in Scrubs.

import os.path

files = os.listdir(os.path.dirname(__file__))
__all__ = [filename[:-3] for filename in files if not filename.startswith('__') and filename.endswith('.py')]


###Dev Shit.
# TIP = '(this is fake and just a lazy way to force a scraper to not run lol.)'
# if test.status() is False: raise Exception()
# if source_utils.limit_hosts() is True and host in str(sources): continue

# if debrid.status() is False: raise Exception()
# if debrid.tor_enabled() is False: raise Exception()

# if not url: return
# if url == None: return sources
#if url == None or url == False: raise Exception()

# if url in str(sources): continue
# if host in str(sources): continue

# results_limit = 30
# if results_limit < 1: continue
# else: results_limit -= 1

# from resources.lib.modules import cfscrape
# self.scraper = cfscrape.create_scraper()
# r = self.scraper.get(url).content

# from resources.lib.modules import client
# url = client.request(url, timeout='10', output='geturl')
# r = client.request(url)

#import traceback
#from resources.lib.modules import log_utils
#except Exception:
    #failure = traceback.format_exc()
    #log_utils.log('---Scraper Testing - Exception: \n' + str(failure))
    #return

# import xbmcgui
# TIP = '(name as in you name it.)'
# xbmcgui.Dialog ().textviewer ("data",str (name))
# xbmcgui.Dialog ().textviewer ("data",str (info))

# from resources.lib.modules import log_utils
# log_utils.log('---Scraper Testing - Sources - host: ' + str(host))
# log_utils.log('---Scraper Testing - Sources - quality: ' + str(quality))
# log_utils.log('---Scraper Testing - Sources - info: ' + str(info))
# log_utils.log('---Scraper Testing - Sources - url: \n' + str(url))

# from resources.lib.modules import source_tools
# valid, host = source_tools.checkHost(link, hostDict)
# quality = source_tools.get_quality(link)
# info = source_tools.get_info(link)

# from resources.lib.modules import more_sources
# for source in more_sources.getMore(url, hostDict): sources.append(source)
# for source in more_sources.more_gomo(url, hostDict): sources.append(source)
# for source in more_sources.more_vidnode(url, hostDict): sources.append(source)
# for source in more_sources.more_vidlink(url, hostDict): sources.append(source)


