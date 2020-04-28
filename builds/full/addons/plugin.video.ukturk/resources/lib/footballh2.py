import urllib,urllib2,re,os,sys,requests

def FHContent(name,url,iconiamge):
	stringlist=''
	source = requests.get(url).content
	match = re.findall('p-1">(.*?)</a>',source,flags=re.DOTALL)
	webbase = 'https://www.ngolos.com/'
	for games in match:
		try:
			url2 = re.findall('href="(.*?)"',games,re.DOTALL)[0]
			if webbase not in url2: url2 = webbase + url2
			teamhome = re.findall('<div\s+class="match_title.+?>(.*?)<',games,re.DOTALL)[0]
			teamaway = re.findall('px-2">.+?>(.*?)</div>',games,re.DOTALL)[0]
			date = re.findall('<div\s+class="match_date.+?>(.*?)<',games,re.DOTALL)[0]
			finalscore = re.findall('px-2">(.*?)</div>',games,re.DOTALL)[0]
			name = date + ' | ' + teamhome + ' VS ' + teamaway + ' | ' + finalscore
			string='<start>'+name+'<sep>'+url2+'<end>'
			stringlist=stringlist+string
		except: pass
	return stringlist

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    return link