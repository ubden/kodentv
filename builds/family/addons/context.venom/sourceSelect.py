import sys, xbmc, json

try:
	from urlparse import parse_qsl
	from urllib import quote_plus
except:
	from urllib.parse import parse_qsl, quote_plus


if __name__ == '__main__':
	item = sys.listitem
	message = item.getLabel()
	path = item.getPath()
	plugin = 'plugin://plugin.video.venom/'
	args = path.split(plugin, 1)
	xbmc.log('args = %s' % args, 2)

	params = dict(parse_qsl(args[1].replace('?', '')))


	xbmc.executebuiltin(path)
