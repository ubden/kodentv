import sys, xbmc, json

try:
	from urlparse import parse_qsl
except:
	from urllib.parse import parse_qsl


if __name__ == '__main__':
	item = sys.listitem
	message = item.getLabel()
	path = item.getPath()
	plugin = 'plugin://plugin.video.venom/'
	args = path.split(plugin, 1)
	# xbmc.log('args = %s' % args, 2)
	params = dict(parse_qsl(args[1].replace('?', '')))

	if 'meta' in params:
		meta = json.loads(params['meta'])
		imdb = meta.get('imdb', '')
		action = 'tvshows' if 'tvshowtitle' in meta else 'movies'

	else:
		imdb = params.get('imdb', '')
		action = 'tvshows' if 'tvshowtitle' in params else 'movies'

	path = '%s?action=%s&url=https://api.trakt.tv/%s/%s/related,return)' % (plugin, action, 'shows' if 'tvshows' in action else 'movies', imdb)
	xbmc.executebuiltin('ActivateWindow(Videos,%s)' % path)