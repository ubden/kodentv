import sys, xbmc, json

try:
	from urlparse import parse_qsl
	# from urllib import quote_plus
except:
	from urllib.parse import parse_qsl
	# from urllib.parse import quote_plus

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
		year = meta.get('year', '')
		imdb = meta.get('imdb', '')
		tvdb = meta.get('tvdb', '')
		tvshowtitle = meta.get('tvshowtitle', '')

	else:
		year = params.get('year', '')
		imdb = params.get('imdb', '')
		tvdb = params.get('tvdb', '')
		tvshowtitle = params.get('tvshowtitle', '')

	path = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s,return)' % (
				plugin, tvshowtitle, year, imdb, tvdb)
	xbmc.executebuiltin('ActivateWindow(Videos,%s)' % path)
