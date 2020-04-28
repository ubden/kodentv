import urllib,urllib2,re,os

def scrape():
    string=''
    print 'xxxxxxxxxxxxxxxxxxx'
    link=open_url("https://mamahd.tv/").replace('\n','').replace('\t','')
    allgames=re.compile('<th class="home-streams">(.+?)widget-content style1">').findall(link)[0]
    #livegame=re.compile('<a href="(.+?)">.+?<img src="(.+?)".+?<div class="home cell">.+?<span>(.+?)</span>.+?<span>(.+?)</span>.+?</a>').findall(allgames)
    livegames=re.compile('<td class="home-time">(.+?)<td class="home-status">',re.DOTALL).findall(allgames)
    print livegames[0]
    for game in livegames:
            date=re.compile('<span class="date">(.+?)</span>',re.DOTALL).findall(game)[0]
            print date
            url=re.compile('<a href="(.+?)">').findall(game)[0]
            print url
            iconimage=re.compile('<img src="(.+?)">').findall(game)[0]
            print iconimage
            home=url.split('-')[0]
            print home


    #https://mamahd.tv/4657-OGC-Nice-vs-ES-Troyes-AC-live-stream.html
            


        



    #for url,iconimage,home,away in livegame:
    #    string=string+'<item>\n<title>%s vs %s</title>\n<sportsdevil>%s</sportsdevil>\n<thumbnail>%s</thumbnail>\n<fanart>fanart</fanart>\n</item>\n\n'%(home,away,url,iconimage)
    #return string

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    return link

