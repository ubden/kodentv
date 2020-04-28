import sys, xbmc, json
import datetime

try:
	from urlparse import parse_qsl
except:
	from urllib.parse import parse_qsl


if __name__ == '__main__':
	plugin = 'plugin://plugin.video.venom/'
	path = 'RunPlugin(%s?action=clearSources&opensettings=false)' % plugin
	xbmc.executebuiltin(path)
