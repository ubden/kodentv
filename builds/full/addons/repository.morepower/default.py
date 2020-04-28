import urlparse,sys,re
import urllib, urllib2
from urlparse import parse_qsl
import xml.etree.ElementTree as ET
import xbmcaddon, os



params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

content = params.get('content')

name = params.get('name')

url = params.get('url')

image = params.get('image')

fanart = params.get('fanart')

addonPath = xbmcaddon.Addon().getAddonInfo("path")


if action == None:
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().root()

elif action == 'directory':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().get(url)

elif action == 'qdirectory':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().getq(url)

elif action == 'xdirectory':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().getx(url)

elif action == 'developer':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().developer()

elif action == 'tvtuner':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().tvtuner(url)

elif 'youtube' in str(action):
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().youtube(url, action)

elif action == 'play':
	from resources.lib.indexers import wolfpack
	wolfpack.player().play(url, content)

elif action == 'browser':
	from resources.lib.indexers import wolfpack
	wolfpack.resolver().browser(url)

elif action == 'search':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().search()

elif action == 'addSearch':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().addSearch(url)

elif action == 'delSearch':
	from resources.lib.indexers import wolfpack
	wolfpack.indexer().delSearch()

elif action == 'queueItem':
	from resources.lib.modules import control
	control.queueItem()

elif action == 'openSettings':
	from resources.lib.modules import control
	control.openSettings()

elif action == 'urlresolverSettings':
	from resources.lib.modules import control
	control.openSettings(id='script.module.urlresolver')

elif action == 'addView':
	from resources.lib.modules import views
	views.addView(content)

elif action == 'downloader':
	from resources.lib.modules import downloader
	downloader.downloader()

elif action == 'addDownload':
	from resources.lib.modules import downloader
	downloader.addDownload(name,url,image)

elif action == 'removeDownload':
	from resources.lib.modules import downloader
	downloader.removeDownload(url)

elif action == 'startDownload':
	from resources.lib.modules import downloader
	downloader.startDownload()

elif action == 'startDownloadThread':
	from resources.lib.modules import downloader
	downloader.startDownloadThread()

elif action == 'stopDownload':
	from resources.lib.modules import downloader
	downloader.stopDownload()

elif action == 'statusDownload':
	from resources.lib.modules import downloader
	downloader.statusDownload()

elif action == 'trailer':
	from resources.lib.modules import trailer
	trailer.trailer().play(name)

elif action == 'clearCache':
	from resources.lib.modules import cache
	cache.clear()