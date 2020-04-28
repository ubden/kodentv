import sys, xbmc, json
import datetime

try:
	from urlparse import parse_qsl
	from urllib import quote_plus
except:
	from urllib.parse import parse_qsl, quote_plus


if __name__ == '__main__':
	item = sys.listitem
	message = item.getLabel()
	path = item.getPath()
	dt = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
	systime = (dt).strftime('%Y%m%d%H%M%S%f')
	plugin = 'plugin://plugin.video.venom/'
	args = path.split(plugin, 1)
	params = dict(parse_qsl(args[1].replace('?', '')))
	title = params['title']

	if 'meta' in params:
		meta = json.loads(params['meta'])
		year = meta.get('year', '')
		imdb = meta.get('imdb', '')
		tvdb = meta.get('tvdb', '')
		season = meta.get('season', '')
		episode = meta.get('episode', '')
		tvshowtitle = meta.get('tvshowtitle', '')
		premiered = meta.get('premiered', '')

	else:
		year = params.get('year', '')
		imdb = params.get('imdb', '')
		tvdb = params.get('tvdb', '')
		season = params.get('season', '')
		episode = params.get('episode', '')
		tvshowtitle = params.get('tvshowtitle', '')
		premiered = params.get('premiered', '')

	sysmeta = quote_plus(json.dumps(meta))
	path = 'PlayMedia(%s?action=reScrape&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=%s&meta=%s&t=%s)' % (
									plugin, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, sysmeta, systime)
	xbmc.executebuiltin(path)
