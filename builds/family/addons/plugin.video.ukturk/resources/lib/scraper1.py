import urllib,urllib2,re,os

def scrape(): 
    string=''
    link=open_url("http://www.sports-stream.net/schedule.html")
    events=re.compile('<p><span style=(.+?)</p>',re.DOTALL).findall(link)
    for event in events:
        time=re.compile('<span style="color:#FF0000;">(.+?)</span>').findall(event)[0]
        time='[COLOR blue]'+time+'[/COLOR]'
        naurl=re.compile('</span> (.+?) - <a href="(.+?)" target="_blank">.+?</a>').findall(event)
        for progname,url in naurl:
            url=url
            progname=progname
            progname=progname.replace('-','vs')
        string=string+'\n<item>\n<title>%s</title>\n<sportsdevil>%s</sportsdevil>\n'%(time+' - '+progname,url)
        string=string+'<thumbnail>ImageHere</thumbnail>\n<fanart>fanart</fanart>\n</item>\n'
    return string

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    return link
