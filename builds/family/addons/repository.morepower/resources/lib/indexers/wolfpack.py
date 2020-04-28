import os as OO0O0O0OOO0000O00 ,re as O000O0O0O00OO000O ,sys as O0O000O0O0OOOO00O ,hashlib as OOOOOO0O00O0OO0O0 ,urllib as OO0OOOO0OOOOOOO00 ,urlparse as OO0O0OOO0O000OOO0 ,json as OOOOO0OOOOOOOOO00 ,base64 as OOO0O0OOOO0O0O0O0 ,random as O00O00O00OOO0OO0O ,datetime as O0O00O00O00O0O0OO #line:1
import xbmc as OO0000O00000OO00O #line:2
try :from sqlite3 import dbapi2 as OO000OOOOOO0OOO0O #line:4
except :from pysqlite2 import dbapi2 as OO000OOOOOO0OOO0O #line:5
from resources .lib .modules import cache as OOOOOOO0O0O00OOO0 #line:7
from resources .lib .modules import metacache as OOO0O0O0O0O0OOO00 #line:8
from resources .lib .modules import client as O0OOOO000O0O00O0O #line:9
from resources .lib .modules import control as O0OOOO0OOO00OO0OO #line:10
from resources .lib .modules import regex as OO0OO0O0000OOO0OO #line:11
from resources .lib .modules import trailer as O00O0OO0000O0OO0O #line:12
from resources .lib .modules import workers as O00O0O000O0O00000 #line:13
from resources .lib .modules import youtube as OO0OOOOO0O000O000 #line:14
from resources .lib .modules import views as OOO00O0OO0OOOO0OO #line:15
version =102 #line:18
class indexer :#line:20
    def __init__ (O0OO00O0OO0O0OOOO ):#line:21
        O0OO00O0OO0O0OOOO .list =[];O0OO00O0OO0O0OOOO .hash =[]#line:22
    def root (OO00O00O0O00000O0 ):#line:25
        try :#line:26
            OO0OO0O0000OOO0OO .clear ()#line:27
            O0000O00000O0OOO0 ='http://www.midian.appboxes.co/morepower/MorePower_Directory.xml'#line:28
            OO00O00O0O00000O0 .list =OO00O00O0O00000O0 .wolfpack_list (O0000O00000O0OOO0 )#line:29
            for O0000O0O0OO000000 in OO00O00O0O00000O0 .list :O0000O0O0OO000000 .update ({'content':'addons'})#line:30
            OO00O00O0O00000O0 .addDirectory (OO00O00O0O00000O0 .list )#line:31
            return OO00O00O0O00000O0 .list #line:32
        except :#line:33
            pass #line:34
    def get (OOO00O00O00OO0O0O ,OO0O00O0000000OO0 ):#line:37
        try :#line:38
            OOO00O00O00OO0O0O .list =OOO00O00O00OO0O0O .wolfpack_list (OO0O00O0000000OO0 )#line:39
            OOO00O00O00OO0O0O .worker ()#line:40
            OOO00O00O00OO0O0O .addDirectory (OOO00O00O00OO0O0O .list )#line:41
            return OOO00O00O00OO0O0O .list #line:42
        except :#line:43
            pass #line:44
    def getq (O0O0O0000OO0OOO0O ,O0O00OO0OOO00OO00 ):#line:47
        try :#line:48
            O0O0O0000OO0OOO0O .list =O0O0O0000OO0OOO0O .wolfpack_list (O0O00OO0OOO00OO00 )#line:49
            O0O0O0000OO0OOO0O .worker ()#line:50
            O0O0O0000OO0OOO0O .addDirectory (O0O0O0000OO0OOO0O .list ,queue =True )#line:51
            return O0O0O0000OO0OOO0O .list #line:52
        except :#line:53
            pass #line:54
    def getx (O0O00O0OO0O00O0OO ,OO00000000OOOOO00 ,worker =False ):#line:57
        try :#line:58
            O00O0O00O0O000000 ,OO0OO0OOO00O0OO00 =O000O0O0O00OO000O .findall ('(.+?)\|regex=(.+?)$',OO00000000OOOOO00 )[0 ]#line:59
            OO0OO0OOO00O0OO00 =OO0OO0O0000OOO0OO .fetch (OO0OO0OOO00O0OO00 )#line:60
            O00O0O00O0O000000 +=OO0OOOO0OOOOOOO00 .unquote_plus (OO0OO0OOO00O0OO00 )#line:61
            OO00000000OOOOO00 =OO0OO0O0000OOO0OO .resolve (O00O0O00O0O000000 )#line:62
            O0O00O0OO0O00O0OO .list =O0O00O0OO0O00O0OO .wolfpack_list ('',result =OO00000000OOOOO00 )#line:63
            O0O00O0OO0O00O0OO .addDirectory (O0O00O0OO0O00O0OO .list )#line:64
            return O0O00O0OO0O00O0OO .list #line:65
        except :#line:66
            pass #line:67
    def developer (O000OO0000OO0OO0O ):#line:70
        try :#line:71
            O00O0OOO000OO00O0 =OO0O0O0OOO0000O00 .path .join (O0OOOO0OOO00OO0OO .dataPath ,'testings.xml')#line:72
            O0O000O00000O0OOO =O0OOOO0OOO00OO0OO .openFile (O00O0OOO000OO00O0 );OOOO0OO00OOOOO0OO =O0O000O00000O0OOO .read ();O0O000O00000O0OOO .close ()#line:73
            O000OO0000OO0OO0O .list =O000OO0000OO0OO0O .wolfpack_list ('',result =OOOO0OO00OOOOO0OO )#line:74
            for OOO00O000OO00OOOO in O000OO0000OO0OO0O .list :OOO00O000OO00OOOO .update ({'content':'videos'})#line:75
            O000OO0000OO0OO0O .addDirectory (O000OO0000OO0OO0O .list )#line:76
            return O000OO0000OO0OO0O .list #line:77
        except :#line:78
            pass #line:79
    def youtube (O0O0OO0OOOOO0OO0O ,O00OO0O0O0OOO0O0O ,OOOOO0000OOO00OO0 ):#line:82
        try :#line:83
            O00OO0O0OO000OO0O =O00O0OO0000O0OO0O .trailer ().key_link .split ('=',1 )[-1 ]#line:84
            if 'PlaylistTuner'in OOOOO0000OOO00OO0 :#line:86
                O0O0OO0OOOOO0OO0O .list =OOOOOOO0O0O00OOO0 .get (OO0OOOOO0O000O000 .youtube (key =O00OO0O0OO000OO0O ).playlist ,1 ,O00OO0O0O0OOO0O0O )#line:87
            elif 'Playlist'in OOOOO0000OOO00OO0 :#line:88
                O0O0OO0OOOOO0OO0O .list =OOOOOOO0O0O00OOO0 .get (OO0OOOOO0O000O000 .youtube (key =O00OO0O0OO000OO0O ).playlist ,1 ,O00OO0O0O0OOO0O0O ,True )#line:89
            elif 'ChannelTuner'in OOOOO0000OOO00OO0 :#line:90
                O0O0OO0OOOOO0OO0O .list =OOOOOOO0O0O00OOO0 .get (OO0OOOOO0O000O000 .youtube (key =O00OO0O0OO000OO0O ).videos ,1 ,O00OO0O0O0OOO0O0O )#line:91
            elif 'Channel'in OOOOO0000OOO00OO0 :#line:92
                O0O0OO0OOOOO0OO0O .list =OOOOOOO0O0O00OOO0 .get (OO0OOOOO0O000O000 .youtube (key =O00OO0O0OO000OO0O ).videos ,1 ,O00OO0O0O0OOO0O0O ,True )#line:93
            if 'Tuner'in OOOOO0000OOO00OO0 :#line:95
                for OOO0O000OO0O00O00 in O0O0OO0OOOOO0OO0O .list :OOO0O000OO0O00O00 .update ({'name':OOO0O000OO0O00O00 ['title'],'poster':OOO0O000OO0O00O00 ['image'],'action':'plugin','folder':False })#line:96
                if 'Tuner2'in OOOOO0000OOO00OO0 :O0O0OO0OOOOO0OO0O .list =sorted (O0O0OO0OOOOO0OO0O .list ,key =lambda O0O00OO0OOO0OO00O :O00O00O00OOO0OO0O .random ())#line:97
                O0O0OO0OOOOO0OO0O .addDirectory (O0O0OO0OOOOO0OO0O .list ,queue =True )#line:98
            else :#line:99
                for OOO0O000OO0O00O00 in O0O0OO0OOOOO0OO0O .list :OOO0O000OO0O00O00 .update ({'name':OOO0O000OO0O00O00 ['title'],'poster':OOO0O000OO0O00O00 ['image'],'nextaction':OOOOO0000OOO00OO0 ,'action':'play','folder':False })#line:100
                O0O0OO0OOOOO0OO0O .addDirectory (O0O0OO0OOOOO0OO0O .list )#line:101
            return O0O0OO0OOOOO0OO0O .list #line:103
        except :#line:104
            pass #line:105
    def tvtuner (OOOOO0O000OOO0O0O ,O0OOO000OO0O00OOO ):#line:108
        try :#line:109
            OO0OO00OO00O00000 =O000O0O0O00OO000O .findall ('<preset>(.+?)</preset>',O0OOO000OO0O00OOO )[0 ]#line:110
            OOO00OOO000O0000O =((O0O00O00O00O0O0OO .datetime .utcnow ()-O0O00O00O00O0O0OO .timedelta (hours =5 ))).strftime ('%Y-%m-%d')#line:112
            OOO00OOO000O0000O =int (O000O0O0O00OO000O .sub ('[^0-9]','',str (OOO00OOO000O0000O )))#line:113
            O0OOO000OO0O00OOO ,OO00OOO0O0OO0OO0O ,O0OOO000OOO00OO00 ,OOOO000O0OO0O0OOO ,O00OO0OO0OO000OOO ,OOOOO0OOOO00OO00O ,O0O00OO000OOOOO0O =O000O0O0O00OO000O .findall ('<url>(.+?)</url>',O0OOO000OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<imdb>(.+?)</imdb>',O0OOO000OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<tvdb>(.+?)</tvdb>',O0OOO000OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<tvshowtitle>(.+?)</tvshowtitle>',O0OOO000OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<year>(.+?)</year>',O0OOO000OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<thumbnail>(.+?)</thumbnail>',O0OOO000OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<fanart>(.+?)</fanart>',O0OOO000OO0O00OOO )[0 ]#line:115
            OO0O00000O0OO0O00 =O0OOOO000O0O00O0O .request ('http://api.tvmaze.com/lookup/shows?thetvdb=%s'%O0OOO000OOO00OO00 )#line:117
            if OO0O00000O0OO0O00 ==None :OO0O00000O0OO0O00 =O0OOOO000O0O00O0O .request ('http://api.tvmaze.com/lookup/shows?imdb=%s'%OO00OOO0O0OO0OO0O )#line:118
            OO0O00000O0OO0O00 ='http://api.tvmaze.com/shows/%s/episodes'%str (OOOOO0OOOOOOOOO00 .loads (OO0O00000O0OO0O00 ).get ('id'))#line:119
            OOOOOO00O0OOOOO00 =OOOOO0OOOOOOOOO00 .loads (O0OOOO000O0O00O0O .request (OO0O00000O0OO0O00 ))#line:120
            OOOOOO00O0OOOOO00 =[(str (O0OO0O0OO0000O00O .get ('season')),str (O0OO0O0OO0000O00O .get ('number')),O0OO0O0OO0000O00O .get ('name').strip (),O0OO0O0OO0000O00O .get ('airdate'))for O0OO0O0OO0000O00O in OOOOOO00O0OOOOO00 ]#line:121
            if OO0OO00OO00O00000 =='tvtuner':#line:123
                OO0OOO0O0OOO0O00O =O00O00O00OOO0OO0O .choice (OOOOOO00O0OOOOO00 )#line:124
                OOOOOO00O0OOOOO00 =OOOOOO00O0OOOOO00 [OOOOOO00O0OOOOO00 .index (OO0OOO0O0OOO0O00O ):]+OOOOOO00O0OOOOO00 [:OOOOOO00O0OOOOO00 .index (OO0OOO0O0OOO0O00O )]#line:125
                OOOOOO00O0OOOOO00 =OOOOOO00O0OOOOO00 [:100 ]#line:126
            OOO0O0O0O0OO00OOO =''#line:128
            for OO0O0O00O00OOO00O in OOOOOO00O0OOOOO00 :#line:130
                try :#line:131
                    if int (O000O0O0O00OO000O .sub ('[^0-9]','',str (OO0O0O00O00OOO00O [3 ])))>OOO00OOO000O0000O :raise Exception ()#line:132
                    OOO0O0O0O0OO00OOO +='<item><title> %01dx%02d . %s</title><meta><content>episode</content><imdb>%s</imdb><tvdb>%s</tvdb><tvshowtitle>%s</tvshowtitle><year>%s</year><title>%s</title><premiered>%s</premiered><season>%01d</season><episode>%01d</episode></meta><link><sublink>search</sublink><sublink>searchsd</sublink></link><thumbnail>%s</thumbnail><fanart>%s</fanart></item>'%(int (OO0O0O00O00OOO00O [0 ]),int (OO0O0O00O00OOO00O [1 ]),OO0O0O00O00OOO00O [2 ],OO00OOO0O0OO0OO0O ,O0OOO000OOO00OO00 ,OOOO000O0OO0O0OOO ,O00OO0OO0OO000OOO ,OO0O0O00O00OOO00O [2 ],OO0O0O00O00OOO00O [3 ],int (OO0O0O00O00OOO00O [0 ]),int (OO0O0O00O00OOO00O [1 ]),OOOOO0OOOO00OO00O ,O0O00OO000OOOOO0O )#line:133
                except :#line:134
                    pass #line:135
            OOO0O0O0O0OO00OOO =O000O0O0O00OO000O .sub (r'[^\x00-\x7F]+',' ',OOO0O0O0O0OO00OOO )#line:137
            if OO0OO00OO00O00000 =='tvtuner':#line:139
                OOO0O0O0O0OO00OOO =OOO0O0O0O0OO00OOO .replace ('<sublink>searchsd</sublink>','')#line:140
            OOOOO0O000OOO0O0O .list =OOOOO0O000OOO0O0O .wolfpack_list ('',result =OOO0O0O0O0OO00OOO )#line:142
            if OO0OO00OO00O00000 =='tvtuner':#line:144
                OOOOO0O000OOO0O0O .addDirectory (OOOOO0O000OOO0O0O .list ,queue =True )#line:145
            else :#line:146
                OOOOO0O000OOO0O0O .worker ()#line:147
                OOOOO0O000OOO0O0O .addDirectory (OOOOO0O000OOO0O0O .list )#line:148
        except :#line:149
            pass #line:150
    def search (O0O0O00O00O0000O0 ):#line:153
        try :#line:154
            O0O0O00O00O0000O0 .list =[{'name':30702 ,'action':'addSearch'}]#line:155
            O0O0O00O00O0000O0 .list +=[{'name':30703 ,'action':'delSearch'}]#line:156
            try :#line:158
                def O00OO0O00000OO0OO ():return #line:159
                OOOOOO0000OO00000 =OOOOOOO0O0O00OOO0 .get (O00OO0O00000OO0OO ,600000000 ,table ='rel_srch')#line:160
                for OOO0O00000OO0OO0O in OOOOOO0000OO00000 :#line:162
                    try :O0O0O00O00O0000O0 .list +=[{'name':'%s...'%OOO0O00000OO0OO0O ,'url':OOO0O00000OO0OO0O ,'action':'addSearch'}]#line:163
                    except :pass #line:164
            except :#line:165
                pass #line:166
            O0O0O00O00O0000O0 .addDirectory (O0O0O00O00O0000O0 .list )#line:168
            return O0O0O00O00O0000O0 .list #line:169
        except :#line:170
            pass #line:171
    def delSearch (OO0OOOOO00OO000OO ):#line:174
        try :#line:175
            OOOOOOO0O0O00OOO0 .clear ('rel_srch')#line:176
            O0OOOO0OOO00OO0OO .refresh ()#line:177
        except :#line:178
            pass #line:179
    def addSearch (O000O0O0O0000O0OO ,url =None ):#line:182
        try :#line:183
            OO00O00O0000000OO ='http://www.midian.appboxes.co/wolfpackdata/wolfpack%20search.xml'#line:184
            if (url ==None or url ==''):#line:186
                OOO0O00O0OOO000OO =O0OOOO0OOO00OO0OO .keyboard ('',O0OOOO0OOO00OO0OO .lang (30702 ).encode ('utf-8'))#line:187
                OOO0O00O0OOO000OO .doModal ()#line:188
                if not (OOO0O00O0OOO000OO .isConfirmed ()):return #line:189
                url =OOO0O00O0OOO000OO .getText ()#line:190
            if (url ==None or url ==''):return #line:192
            def O0OOOOO0000OO0OOO ():return [url ]#line:194
            O0O00OO00O00OOOOO =OOOOOOO0O0O00OOO0 .get (O0OOOOO0000OO0OOO ,600000000 ,table ='rel_srch')#line:195
            def O0OOOOO0000OO0OOO ():return [O0O0OO0O0O0OO0OOO for O00OOO0O00O0000O0 ,O0O0OO0O0O0OO0OOO in enumerate ((O0O00OO00O00OOOOO +[url ]))if O0O0OO0O0O0OO0OOO not in (O0O00OO00O00OOOOO +[url ])[:O00OOO0O00O0000O0 ]]#line:196
            OOOOOOO0O0O00OOO0 .get (O0OOOOO0000OO0OOO ,0 ,table ='rel_srch')#line:197
            O00O0O0OOOOO0OO00 =O0OOOO000O0O00O0O .request (OO00O00O0000000OO )#line:199
            O00O0O0OOOOO0OO00 =O000O0O0O00OO000O .findall ('<link>(.+?)</link>',O00O0O0OOOOO0OO00 )#line:200
            O00O0O0OOOOO0OO00 =[OO0OOO0O0O0OO00O0 for OO0OOO0O0O0OO00O0 in O00O0O0OOOOO0OO00 if str (OO0OOO0O0O0OO00O0 ).startswith ('http')]#line:201
            O000O0O0O0000O0OO .list =[];OOO00000OOO00OO0O =[]#line:203
            for OO00O00O0000000OO in O00O0O0OOOOO0OO00 :OOO00000OOO00OO0O .append (O00O0O000O0O00000 .Thread (O000O0O0O0000O0OO .wolfpack_list ,OO00O00O0000000OO ))#line:204
            [OOOOO000O0OO00OOO .start ()for OOOOO000O0OO00OOO in OOO00000OOO00OO0O ];[O0OO0O00O0O00OO00 .join ()for O0OO0O00O0O00OO00 in OOO00000OOO00OO0O ]#line:205
            O000O0O0O0000O0OO .list =[O00OOO0O00000O00O for O00OOO0O00000O00O in O000O0O0O0000O0OO .list if url .lower ()in O00OOO0O00000O00O ['name'].lower ()]#line:207
            for OOO0OOOO0O0OOOO0O in O000O0O0O0000O0OO .list :#line:209
                try :#line:210
                    OOOOOOOOO0OOO00OO =''#line:211
                    if not OOO0OOOO0O0OOOO0O ['vip']in ['wolfpack TV']:OOOOOOOOO0OOO00OO +='[B]%s[/B] | '%OOO0OOOO0O0OOOO0O ['vip'].upper ()#line:212
                    OOOOOOOOO0OOO00OO +=OOO0OOOO0O0OOOO0O ['name']#line:213
                    OOO0OOOO0O0OOOO0O .update ({'name':OOOOOOOOO0OOO00OO })#line:214
                except :#line:215
                    pass #line:216
            for OOO0OOOO0O0OOOO0O in O000O0O0O0000O0OO .list :OOO0OOOO0O0OOOO0O .update ({'content':'videos'})#line:218
            O000O0O0O0000O0OO .addDirectory (O000O0O0O0000O0OO .list )#line:219
        except :#line:220
            pass #line:221
    def wolfpack_list (OO0OOO00000OO0O0O ,O0OOOO0OOOO0OO00O ,result =None ):#line:224
        try :#line:225
            if result ==None :result =OOOOOOO0O0O00OOO0 .get (O0OOOO000O0O00O0O .request ,0 ,O0OOOO0OOOO0OO00O )#line:226
            if result .strip ().startswith ('#EXTM3U')and '#EXTINF'in result :#line:228
                result =O000O0O0O00OO000O .compile ('#EXTINF:.+?\,(.+?)\n(.+?)\n',O000O0O0O00OO000O .MULTILINE |O000O0O0O00OO000O .DOTALL ).findall (result )#line:229
                result =['<item><title>%s</title><link>%s</link></item>'%(OO00000O0OOOO000O [0 ],OO00000O0OOOO000O [1 ])for OO00000O0OOOO000O in result ]#line:230
                result =''.join (result )#line:231
            try :O0O00OO000O0OOO00 =OOO0O0OOOO0O0O0O0 .b64decode (result )#line:233
            except :O0O00OO000O0OOO00 =''#line:234
            if '</link>'in O0O00OO000O0OOO00 :result =O0O00OO000O0OOO00 #line:235
            result =str (result )#line:237
            result =OO0OOO00000OO0O0O .account_filter (result )#line:239
            OO0O00OOO0OOO0OO0 =result .split ('<item>')[0 ].split ('<dir>')[0 ]#line:241
            try :O00OOO0OO0O0OO0O0 =O000O0O0O00OO000O .findall ('<poster>(.+?)</poster>',OO0O00OOO0OOO0OO0 )[0 ]#line:243
            except :O00OOO0OO0O0OO0O0 ='0'#line:244
            try :OO0000O00O00OO0OO =O000O0O0O00OO000O .findall ('<thumbnail>(.+?)</thumbnail>',OO0O00OOO0OOO0OO0 )[0 ]#line:246
            except :OO0000O00O00OO0OO ='0'#line:247
            try :OOO00O0O00O00O00O =O000O0O0O00OO000O .findall ('<fanart>(.+?)</fanart>',OO0O00OOO0OOO0OO0 )[0 ]#line:249
            except :OOO00O0O00O00O00O ='0'#line:250
            OO00OOOOO00O0O0OO =O000O0O0O00OO000O .compile ('((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>|<info>.+?</info>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><mode>[^<]+</mode>|<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail><date>[^<]+</date>))',O000O0O0O00OO000O .MULTILINE |O000O0O0O00OO000O .DOTALL ).findall (result )#line:252
        except :#line:253
            return #line:254
        for OOOOOO00OOOOOO000 in OO00OOOOO00O0O0OO :#line:256
            try :#line:257
                O0OOO000O00O00000 =O000O0O0O00OO000O .compile ('(<regex>.+?</regex>)',O000O0O0O00OO000O .MULTILINE |O000O0O0O00OO000O .DOTALL ).findall (OOOOOO00OOOOOO000 )#line:258
                O0OOO000O00O00000 =''.join (O0OOO000O00O00000 )#line:259
                O0O00OO0OO0OO0O00 =O000O0O0O00OO000O .compile ('(<listrepeat>.+?</listrepeat>)',O000O0O0O00OO000O .MULTILINE |O000O0O0O00OO000O .DOTALL ).findall (O0OOO000O00O00000 )#line:260
                O0OOO000O00O00000 =OO0OOOO0OOOOOOO00 .quote_plus (O0OOO000O00O00000 )#line:261
                OOOOOOOOOO00OOO00 =OOOOOO0O00O0OO0O0 .md5 ()#line:263
                for OO0OOO0O00O0O0000 in O0OOO000O00O00000 :OOOOOOOOOO00OOO00 .update (str (OO0OOO0O00O0O0000 ))#line:264
                OOOOOOOOOO00OOO00 =str (OOOOOOOOOO00OOO00 .hexdigest ())#line:265
                OOOOOO00OOOOOO000 =OOOOOO00OOOOOO000 .replace ('\r','').replace ('\n','').replace ('\t','').replace ('&nbsp;','')#line:267
                OOOOOO00OOOOOO000 =O000O0O0O00OO000O .sub ('<regex>.+?</regex>','',OOOOOO00OOOOOO000 )#line:268
                OOOOOO00OOOOOO000 =O000O0O0O00OO000O .sub ('<sublink></sublink>|<sublink\s+name=(?:\'|\").*?(?:\'|\")></sublink>','',OOOOOO00OOOOOO000 )#line:269
                OOOOOO00OOOOOO000 =O000O0O0O00OO000O .sub ('<link></link>','',OOOOOO00OOOOOO000 )#line:270
                OO0OO0OOO0OO0O000 =O000O0O0O00OO000O .sub ('<meta>.+?</meta>','',OOOOOO00OOOOOO000 )#line:272
                try :OO0OO0OOO0OO0O000 =O000O0O0O00OO000O .findall ('<title>(.+?)</title>',OO0OO0OOO0OO0O000 )[0 ]#line:273
                except :OO0OO0OOO0OO0O000 =O000O0O0O00OO000O .findall ('<name>(.+?)</name>',OO0OO0OOO0OO0O000 )[0 ]#line:274
                try :O0O00000O00O0OO00 =O000O0O0O00OO000O .findall ('<date>(.+?)</date>',OOOOOO00OOOOOO000 )[0 ]#line:276
                except :O0O00000O00O0OO00 =''#line:277
                if O000O0O0O00OO000O .search (r'\d+',O0O00000O00O0OO00 ):OO0OO0OOO0OO0O000 +=' [COLOR red] Updated %s[/COLOR]'%O0O00000O00O0OO00 #line:278
                try :OOO00O0OOO0OOOO00 =O000O0O0O00OO000O .findall ('<thumbnail>(.+?)</thumbnail>',OOOOOO00OOOOOO000 )[0 ]#line:280
                except :OOO00O0OOO0OOOO00 =OO0000O00O00OO0OO #line:281
                try :O0OO0O0O00O0OO0OO =O000O0O0O00OO000O .findall ('<fanart>(.+?)</fanart>',OOOOOO00OOOOOO000 )[0 ]#line:283
                except :O0OO0O0O00O0OO0OO =OOO00O0O00O00O00O #line:284
                try :OO0OOOOOOOO00O000 =O000O0O0O00OO000O .findall ('<meta>(.+?)</meta>',OOOOOO00OOOOOO000 )[0 ]#line:286
                except :OO0OOOOOOOO00O000 ='0'#line:287
                try :O0OOOO0OOOO0OO00O =O000O0O0O00OO000O .findall ('<link>(.+?)</link>',OOOOOO00OOOOOO000 )[0 ]#line:289
                except :O0OOOO0OOOO0OO00O ='0'#line:290
                O0OOOO0OOOO0OO00O =O0OOOO0OOOO0OO00O .replace ('>search<','><preset>search</preset>%s<'%OO0OOOOOOOO00O000 )#line:291
                O0OOOO0OOOO0OO00O ='<preset>search</preset>%s'%OO0OOOOOOOO00O000 if O0OOOO0OOOO0OO00O =='search'else O0OOOO0OOOO0OO00O #line:292
                O0OOOO0OOOO0OO00O =O0OOOO0OOOO0OO00O .replace ('>searchsd<','><preset>searchsd</preset>%s<'%OO0OOOOOOOO00O000 )#line:293
                O0OOOO0OOOO0OO00O ='<preset>searchsd</preset>%s'%OO0OOOOOOOO00O000 if O0OOOO0OOOO0OO00O =='searchsd'else O0OOOO0OOOO0OO00O #line:294
                O0OOOO0OOOO0OO00O =O000O0O0O00OO000O .sub ('<sublink></sublink>|<sublink\s+name=(?:\'|\").*?(?:\'|\")></sublink>','',O0OOOO0OOOO0OO00O )#line:295
                if OOOOOO00OOOOOO000 .startswith ('<item>'):O0OOOO0000000O00O ='play'#line:297
                elif OOOOOO00OOOOOO000 .startswith ('<plugin>'):O0OOOO0000000O00O ='plugin'#line:298
                elif OOOOOO00OOOOOO000 .startswith ('<info>')or O0OOOO0OOOO0OO00O =='0':O0OOOO0000000O00O ='0'#line:299
                else :O0OOOO0000000O00O ='directory'#line:300
                if O0OOOO0000000O00O =='play'and O0O00OO0OO0OO0O00 :O0OOOO0000000O00O ='xdirectory'#line:301
                if not O0OOO000O00O00000 =='':#line:303
                    OO0OOO00000OO0O0O .hash .append ({'regex':OOOOOOOOOO00OOO00 ,'response':O0OOO000O00O00000 })#line:304
                    O0OOOO0OOOO0OO00O +='|regex=%s'%OOOOOOOOOO00OOO00 #line:305
                if O0OOOO0000000O00O in ['directory','xdirectory','plugin']:#line:307
                    O00000OO000OO0O0O =True #line:308
                else :#line:309
                    O00000OO000OO0O0O =False #line:310
                try :OOO0O00O0OO000000 =O000O0O0O00OO000O .findall ('<content>(.+?)</content>',OO0OOOOOOOO00O000 )[0 ]#line:312
                except :OOO0O00O0OO000000 ='0'#line:313
                if OOO0O00O0OO000000 =='0':#line:314
                    try :OOO0O00O0OO000000 =O000O0O0O00OO000O .findall ('<content>(.+?)</content>',OOOOOO00OOOOOO000 )[0 ]#line:315
                    except :OOO0O00O0OO000000 ='0'#line:316
                if not OOO0O00O0OO000000 =='0':OOO0O00O0OO000000 +='s'#line:317
                if 'tvshow'in OOO0O00O0OO000000 and not O0OOOO0OOOO0OO00O .strip ().endswith ('.xml'):#line:319
                    O0OOOO0OOOO0OO00O ='<preset>tvindexer</preset><url>%s</url><thumbnail>%s</thumbnail><fanart>%s</fanart>%s'%(O0OOOO0OOOO0OO00O ,OOO00O0OOO0OOOO00 ,O0OO0O0O00O0OO0OO ,OO0OOOOOOOO00O000 )#line:320
                    O0OOOO0000000O00O ='tvtuner'#line:321
                if 'tvtuner'in OOO0O00O0OO000000 and not O0OOOO0OOOO0OO00O .strip ().endswith ('.xml'):#line:323
                    O0OOOO0OOOO0OO00O ='<preset>tvtuner</preset><url>%s</url><thumbnail>%s</thumbnail><fanart>%s</fanart>%s'%(O0OOOO0OOOO0OO00O ,OOO00O0OOO0OOOO00 ,O0OO0O0O00O0OO0OO ,OO0OOOOOOOO00O000 )#line:324
                    O0OOOO0000000O00O ='tvtuner'#line:325
                try :O0OO0O0O000O0O0OO =O000O0O0O00OO000O .findall ('<imdb>(.+?)</imdb>',OO0OOOOOOOO00O000 )[0 ]#line:327
                except :O0OO0O0O000O0O0OO ='0'#line:328
                try :OOOO0O00000OOO000 =O000O0O0O00OO000O .findall ('<tvdb>(.+?)</tvdb>',OO0OOOOOOOO00O000 )[0 ]#line:330
                except :OOOO0O00000OOO000 ='0'#line:331
                try :O00000OO0000O0OO0 =O000O0O0O00OO000O .findall ('<tvshowtitle>(.+?)</tvshowtitle>',OO0OOOOOOOO00O000 )[0 ]#line:333
                except :O00000OO0000O0OO0 ='0'#line:334
                try :O00OOO0OO000O0000 =O000O0O0O00OO000O .findall ('<title>(.+?)</title>',OO0OOOOOOOO00O000 )[0 ]#line:336
                except :O00OOO0OO000O0000 ='0'#line:337
                if O00OOO0OO000O0000 =='0'and not O00000OO0000O0OO0 =='0':O00OOO0OO000O0000 =O00000OO0000O0OO0 #line:339
                try :OO00000OO00O0O0OO =O000O0O0O00OO000O .findall ('<year>(.+?)</year>',OO0OOOOOOOO00O000 )[0 ]#line:341
                except :OO00000OO00O0O0OO ='0'#line:342
                try :O00OO0O0OO0O00000 =O000O0O0O00OO000O .findall ('<premiered>(.+?)</premiered>',OO0OOOOOOOO00O000 )[0 ]#line:344
                except :O00OO0O0OO0O00000 ='0'#line:345
                try :O0OOO0OO0OO0O0O00 =O000O0O0O00OO000O .findall ('<season>(.+?)</season>',OO0OOOOOOOO00O000 )[0 ]#line:347
                except :O0OOO0OO0OO0O0O00 ='0'#line:348
                try :O000OOOOOOO00O0O0 =O000O0O0O00OO000O .findall ('<episode>(.+?)</episode>',OO0OOOOOOOO00O000 )[0 ]#line:350
                except :O000OOOOOOO00O0O0 ='0'#line:351
                OO0OOO00000OO0O0O .list .append ({'name':OO0OO0OOO0OO0O000 ,'vip':O00OOO0OO0O0OO0O0 ,'url':O0OOOO0OOOO0OO00O ,'action':O0OOOO0000000O00O ,'folder':O00000OO000OO0O0O ,'poster':OOO00O0OOO0OOOO00 ,'banner':'0','fanart':O0OO0O0O00O0OO0OO ,'content':OOO0O00O0OO000000 ,'imdb':O0OO0O0O000O0O0OO ,'tvdb':OOOO0O00000OOO000 ,'tmdb':'0','title':O00OOO0OO000O0000 ,'originaltitle':O00OOO0OO000O0000 ,'tvshowtitle':O00000OO0000O0OO0 ,'year':OO00000OO00O0O0OO ,'premiered':O00OO0O0OO0O00000 ,'season':O0OOO0OO0OO0O0O00 ,'episode':O000OOOOOOO00O0O0 })#line:353
            except :#line:354
                pass #line:355
        OO0OO0O0000OOO0OO .insert (OO0OOO00000OO0O0O .hash )#line:357
        return OO0OOO00000OO0O0O .list #line:359
    def account_filter (OOO00O0OO00OO00O0 ,OOOO00O0OO0O00O00 ):#line:362
        if (O0OOOO0OOO00OO0OO .setting ('ustvnow_email')==''or O0OOOO0OOO00OO0OO .setting ('ustvnow_pass')==''):#line:363
            OOOO00O0OO0O00O00 =O000O0O0O00OO000O .sub ('http(?:s|)://(?:www\.|)ustvnow\.com/.+?<','<',OOOO00O0OO0O00O00 )#line:364
        if (O0OOOO0OOO00OO0OO .setting ('streamlive_user')==''or O0OOOO0OOO00OO0OO .setting ('streamlive_pass')==''):#line:366
            OOOO00O0OO0O00O00 =O000O0O0O00OO000O .sub ('http(?:s|)://(?:www\.|)streamlive\.to/.+?<','<',OOOO00O0OO0O00O00 )#line:367
        return OOOO00O0OO0O00O00 #line:369
    def worker (O0O0OOOOO0OOO0O00 ):#line:372
        if not O0OOOO0OOO00OO0OO .setting ('metadata')=='true':return #line:373
        O0O0OOOOO0OOO0O00 .imdb_info_link ='http://www.omdbapi.com/?i=%s&plot=full&r=json'#line:375
        O0O0OOOOO0OOO0O00 .tvmaze_info_link ='http://api.tvmaze.com/lookup/shows?thetvdb=%s'#line:376
        O0O0OOOOO0OOO0O00 .lang ='en'#line:377
        O0O0OOOOO0OOO0O00 .meta =[]#line:379
        OOOO00O0O000OO0O0 =len (O0O0OOOOO0OOO0O00 .list )#line:380
        if OOOO00O0O000OO0O0 ==0 :return #line:381
        for O0OOO00OOO00O00O0 in range (0 ,OOOO00O0O000OO0O0 ):O0O0OOOOO0OOO0O00 .list [O0OOO00OOO00O00O0 ].update ({'metacache':False })#line:383
        O0O0OOOOO0OOO0O00 .list =OOO0O0O0O0O0OOO00 .fetch (O0O0OOOOO0OOO0O00 .list ,O0O0OOOOO0OOO0O00 .lang )#line:384
        OOOO0OO0O000O00O0 =[O0O0O0O0O0OO00O0O ['imdb']for O0O0O0O0O0OO00O0O in O0O0OOOOO0OOO0O00 .list ]#line:386
        OOOO0OO0O000O00O0 =[O0OO00O0000OOOOOO for O00OO0000O0O0000O ,O0OO00O0000OOOOOO in enumerate (OOOO0OO0O000O00O0 )if O0OO00O0000OOOOOO not in OOOO0OO0O000O00O0 [:O00OO0000O0O0000O ]]#line:387
        if len (OOOO0OO0O000O00O0 )==1 :#line:388
                O0O0OOOOO0OOO0O00 .movie_info (0 );O0O0OOOOO0OOO0O00 .tv_info (0 )#line:389
                if O0O0OOOOO0OOO0O00 .meta :OOO0O0O0O0O0OOO00 .insert (O0O0OOOOO0OOO0O00 .meta )#line:390
        for O0OOO00OOO00O00O0 in range (0 ,OOOO00O0O000OO0O0 ):O0O0OOOOO0OOO0O00 .list [O0OOO00OOO00O00O0 ].update ({'metacache':False })#line:392
        O0O0OOOOO0OOO0O00 .list =OOO0O0O0O0O0OOO00 .fetch (O0O0OOOOO0OOO0O00 .list ,O0O0OOOOO0OOO0O00 .lang )#line:393
        for O0O0O00O00OOOO00O in range (0 ,OOOO00O0O000OO0O0 ,50 ):#line:395
            O00OO0OOO00O0OO0O =[]#line:396
            for O0OOO00OOO00O00O0 in range (O0O0O00O00OOOO00O ,O0O0O00O00OOOO00O +50 ):#line:397
                if O0OOO00OOO00O00O0 <=OOOO00O0O000OO0O0 :O00OO0OOO00O0OO0O .append (O00O0O000O0O00000 .Thread (O0O0OOOOO0OOO0O00 .movie_info ,O0OOO00OOO00O00O0 ))#line:398
                if O0OOO00OOO00O00O0 <=OOOO00O0O000OO0O0 :O00OO0OOO00O0OO0O .append (O00O0O000O0O00000 .Thread (O0O0OOOOO0OOO0O00 .tv_info ,O0OOO00OOO00O00O0 ))#line:399
            [OO0O0O0000O0OOO0O .start ()for OO0O0O0000O0OOO0O in O00OO0OOO00O0OO0O ]#line:400
            [O00OO00O00O0000OO .join ()for O00OO00O00O0000OO in O00OO0OOO00O0OO0O ]#line:401
        if O0O0OOOOO0OOO0O00 .meta :OOO0O0O0O0O0OOO00 .insert (O0O0OOOOO0OOO0O00 .meta )#line:403
    def movie_info (OOO00O000O000O0OO ,O0000O0OOO000O0OO ):#line:406
        try :#line:407
            if OOO00O000O000O0OO .list [O0000O0OOO000O0OO ]['metacache']==True :raise Exception ()#line:408
            if not OOO00O000O000O0OO .list [O0000O0OOO000O0OO ]['content']=='movies':raise Exception ()#line:410
            O0O0OOOO0OOO0OOO0 =OOO00O000O000O0OO .list [O0000O0OOO000O0OO ]['imdb']#line:412
            if O0O0OOOO0OOO0OOO0 =='0':raise Exception ()#line:413
            OO000O00OO000O0O0 =OOO00O000O000O0OO .imdb_info_link %O0O0OOOO0OOO0OOO0 #line:415
            O00O000O00000000O =O0OOOO000O0O00O0O .request (OO000O00OO000O0O0 ,timeout ='10')#line:417
            O00O000O00000000O =OOOOO0OOOOOOOOO00 .loads (O00O000O00000000O )#line:418
            if 'Error'in O00O000O00000000O and 'incorrect imdb'in O00O000O00000000O ['Error'].lower ():#line:420
                return OOO00O000O000O0OO .meta .append ({'imdb':O0O0OOOO0OOO0OOO0 ,'tmdb':'0','tvdb':'0','lang':OOO00O000O000O0OO .lang ,'item':{'code':'0'}})#line:421
            OOO00OO0OO0000OO0 =O00O000O00000000O ['Title']#line:423
            OOO00OO0OO0000OO0 =OOO00OO0OO0000OO0 .encode ('utf-8')#line:424
            if not OOO00OO0OO0000OO0 =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'title':OOO00OO0OO0000OO0 })#line:425
            O00OO00OOOOO00OOO =O00O000O00000000O ['Year']#line:427
            O00OO00OOOOO00OOO =O00OO00OOOOO00OOO .encode ('utf-8')#line:428
            if not O00OO00OOOOO00OOO =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'year':O00OO00OOOOO00OOO })#line:429
            O0O0OOOO0OOO0OOO0 =O00O000O00000000O ['imdbID']#line:431
            if O0O0OOOO0OOO0OOO0 ==None or O0O0OOOO0OOO0OOO0 ==''or O0O0OOOO0OOO0OOO0 =='N/A':O0O0OOOO0OOO0OOO0 ='0'#line:432
            O0O0OOOO0OOO0OOO0 =O0O0OOOO0OOO0OOO0 .encode ('utf-8')#line:433
            if not O0O0OOOO0OOO0OOO0 =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'imdb':O0O0OOOO0OOO0OOO0 ,'code':O0O0OOOO0OOO0OOO0 })#line:434
            O000OOOOOO00O00O0 =O00O000O00000000O ['Released']#line:436
            if O000OOOOOO00O00O0 ==None or O000OOOOOO00O00O0 ==''or O000OOOOOO00O00O0 =='N/A':O000OOOOOO00O00O0 ='0'#line:437
            O000OOOOOO00O00O0 =O000O0O0O00OO000O .findall ('(\d*) (.+?) (\d*)',O000OOOOOO00O00O0 )#line:438
            try :O000OOOOOO00O00O0 ='%s-%s-%s'%(O000OOOOOO00O00O0 [0 ][2 ],{'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}[O000OOOOOO00O00O0 [0 ][1 ]],O000OOOOOO00O00O0 [0 ][0 ])#line:439
            except :O000OOOOOO00O00O0 ='0'#line:440
            O000OOOOOO00O00O0 =O000OOOOOO00O00O0 .encode ('utf-8')#line:441
            if not O000OOOOOO00O00O0 =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'premiered':O000OOOOOO00O00O0 })#line:442
            O000O0OOOO0OOOO0O =O00O000O00000000O ['Genre']#line:444
            if O000O0OOOO0OOOO0O ==None or O000O0OOOO0OOOO0O ==''or O000O0OOOO0OOOO0O =='N/A':O000O0OOOO0OOOO0O ='0'#line:445
            O000O0OOOO0OOOO0O =O000O0OOOO0OOOO0O .replace (', ',' / ')#line:446
            O000O0OOOO0OOOO0O =O000O0OOOO0OOOO0O .encode ('utf-8')#line:447
            if not O000O0OOOO0OOOO0O =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'genre':O000O0OOOO0OOOO0O })#line:448
            O0000O0OOO0000O00 =O00O000O00000000O ['Runtime']#line:450
            if O0000O0OOO0000O00 ==None or O0000O0OOO0000O00 ==''or O0000O0OOO0000O00 =='N/A':O0000O0OOO0000O00 ='0'#line:451
            O0000O0OOO0000O00 =O000O0O0O00OO000O .sub ('[^0-9]','',str (O0000O0OOO0000O00 ))#line:452
            try :O0000O0OOO0000O00 =str (int (O0000O0OOO0000O00 )*60 )#line:453
            except :pass #line:454
            O0000O0OOO0000O00 =O0000O0OOO0000O00 .encode ('utf-8')#line:455
            if not O0000O0OOO0000O00 =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'duration':O0000O0OOO0000O00 })#line:456
            OO0O0OO00OOOOO0O0 =O00O000O00000000O ['imdbRating']#line:458
            if OO0O0OO00OOOOO0O0 ==None or OO0O0OO00OOOOO0O0 ==''or OO0O0OO00OOOOO0O0 =='N/A'or OO0O0OO00OOOOO0O0 =='0.0':OO0O0OO00OOOOO0O0 ='0'#line:459
            OO0O0OO00OOOOO0O0 =OO0O0OO00OOOOO0O0 .encode ('utf-8')#line:460
            if not OO0O0OO00OOOOO0O0 =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'rating':OO0O0OO00OOOOO0O0 })#line:461
            OO0OO00OO0000000O =O00O000O00000000O ['imdbVotes']#line:463
            try :OO0OO00OO0000000O =str (format (int (OO0OO00OO0000000O ),',d'))#line:464
            except :pass #line:465
            if OO0OO00OO0000000O ==None or OO0OO00OO0000000O ==''or OO0OO00OO0000000O =='N/A':OO0OO00OO0000000O ='0'#line:466
            OO0OO00OO0000000O =OO0OO00OO0000000O .encode ('utf-8')#line:467
            if not OO0OO00OO0000000O =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'votes':OO0OO00OO0000000O })#line:468
            OO0O0OOOOOOOOOOOO =O00O000O00000000O ['Rated']#line:470
            if OO0O0OOOOOOOOOOOO ==None or OO0O0OOOOOOOOOOOO ==''or OO0O0OOOOOOOOOOOO =='N/A':OO0O0OOOOOOOOOOOO ='0'#line:471
            OO0O0OOOOOOOOOOOO =OO0O0OOOOOOOOOOOO .encode ('utf-8')#line:472
            if not OO0O0OOOOOOOOOOOO =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'mpaa':OO0O0OOOOOOOOOOOO })#line:473
            OO00O00OO0OO0OOOO =O00O000O00000000O ['Director']#line:475
            if OO00O00OO0OO0OOOO ==None or OO00O00OO0OO0OOOO ==''or OO00O00OO0OO0OOOO =='N/A':OO00O00OO0OO0OOOO ='0'#line:476
            OO00O00OO0OO0OOOO =OO00O00OO0OO0OOOO .replace (', ',' / ')#line:477
            OO00O00OO0OO0OOOO =O000O0O0O00OO000O .sub (r'\(.*?\)','',OO00O00OO0OO0OOOO )#line:478
            OO00O00OO0OO0OOOO =' '.join (OO00O00OO0OO0OOOO .split ())#line:479
            OO00O00OO0OO0OOOO =OO00O00OO0OO0OOOO .encode ('utf-8')#line:480
            if not OO00O00OO0OO0OOOO =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'director':OO00O00OO0OO0OOOO })#line:481
            O0OO00O0OOOOOOOOO =O00O000O00000000O ['Writer']#line:483
            if O0OO00O0OOOOOOOOO ==None or O0OO00O0OOOOOOOOO ==''or O0OO00O0OOOOOOOOO =='N/A':O0OO00O0OOOOOOOOO ='0'#line:484
            O0OO00O0OOOOOOOOO =O0OO00O0OOOOOOOOO .replace (', ',' / ')#line:485
            O0OO00O0OOOOOOOOO =O000O0O0O00OO000O .sub (r'\(.*?\)','',O0OO00O0OOOOOOOOO )#line:486
            O0OO00O0OOOOOOOOO =' '.join (O0OO00O0OOOOOOOOO .split ())#line:487
            O0OO00O0OOOOOOOOO =O0OO00O0OOOOOOOOO .encode ('utf-8')#line:488
            if not O0OO00O0OOOOOOOOO =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'writer':O0OO00O0OOOOOOOOO })#line:489
            O00O0000000OO0OO0 =O00O000O00000000O ['Actors']#line:491
            if O00O0000000OO0OO0 ==None or O00O0000000OO0OO0 ==''or O00O0000000OO0OO0 =='N/A':O00O0000000OO0OO0 ='0'#line:492
            O00O0000000OO0OO0 =[O00OOO0OO00O00000 .strip ()for O00OOO0OO00O00000 in O00O0000000OO0OO0 .split (',')if not O00OOO0OO00O00000 =='']#line:493
            try :O00O0000000OO0OO0 =[(O0O000O00O0O00OOO .encode ('utf-8'),'')for O0O000O00O0O00OOO in O00O0000000OO0OO0 ]#line:494
            except :O00O0000000OO0OO0 =[]#line:495
            if O00O0000000OO0OO0 ==[]:O00O0000000OO0OO0 ='0'#line:496
            if not O00O0000000OO0OO0 =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'cast':O00O0000000OO0OO0 })#line:497
            OO0000OOOO00000O0 =O00O000O00000000O ['Plot']#line:499
            if OO0000OOOO00000O0 ==None or OO0000OOOO00000O0 ==''or OO0000OOOO00000O0 =='N/A':OO0000OOOO00000O0 ='0'#line:500
            OO0000OOOO00000O0 =O0OOOO000O0O00O0O .replaceHTMLCodes (OO0000OOOO00000O0 )#line:501
            OO0000OOOO00000O0 =OO0000OOOO00000O0 .encode ('utf-8')#line:502
            if not OO0000OOOO00000O0 =='0':OOO00O000O000O0OO .list [O0000O0OOO000O0OO ].update ({'plot':OO0000OOOO00000O0 })#line:503
            OOO00O000O000O0OO .meta .append ({'imdb':O0O0OOOO0OOO0OOO0 ,'tmdb':'0','tvdb':'0','lang':OOO00O000O000O0OO .lang ,'item':{'title':OOO00OO0OO0000OO0 ,'year':O00OO00OOOOO00OOO ,'code':O0O0OOOO0OOO0OOO0 ,'imdb':O0O0OOOO0OOO0OOO0 ,'premiered':O000OOOOOO00O00O0 ,'genre':O000O0OOOO0OOOO0O ,'duration':O0000O0OOO0000O00 ,'rating':OO0O0OO00OOOOO0O0 ,'votes':OO0OO00OO0000000O ,'mpaa':OO0O0OOOOOOOOOOOO ,'director':OO00O00OO0OO0OOOO ,'writer':O0OO00O0OOOOOOOOO ,'cast':O00O0000000OO0OO0 ,'plot':OO0000OOOO00000O0 }})#line:505
        except :#line:506
            pass #line:507
    def tv_info (OOOOO00OOOO0O0OOO ,O000O0OOOO00O0O0O ):#line:510
        try :#line:511
            if OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ]['metacache']==True :raise Exception ()#line:512
            if not OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ]['content']in ['tvshows','seasons','episodes']:raise Exception ()#line:514
            OOO000OOOO00OOOOO =OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ]['tvdb']#line:516
            if OOO000OOOO00OOOOO =='0':raise Exception ()#line:517
            OOO00000000OOOOO0 =OOOOO00OOOO0O0OOO .tvmaze_info_link %OOO000OOOO00OOOOO #line:519
            OOO0O0OO0O00OOOOO =O0OOOO000O0O00O0O .request (OOO00000000OOOOO0 ,output ='extended',error =True ,timeout ='10')#line:521
            if OOO0O0OO0O00OOOOO [1 ]=='404':#line:523
                return OOOOO00OOOO0O0OOO .meta .append ({'imdb':'0','tmdb':'0','tvdb':OOO000OOOO00OOOOO ,'lang':OOOOO00OOOO0O0OOO .lang ,'item':{'code':'0'}})#line:524
            OOO0O0OO0O00OOOOO =OOOOO0OOOOOOOOO00 .loads (OOO0O0OO0O00OOOOO [0 ])#line:526
            OO0O000OOOOO0O0OO =OOO0O0OO0O00OOOOO ['name']#line:528
            OO0O000OOOOO0O0OO =OO0O000OOOOO0O0OO .encode ('utf-8')#line:529
            if not OO0O000OOOOO0O0OO =='0':OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ].update ({'tvshowtitle':OO0O000OOOOO0O0OO })#line:530
            O000OOO0OO000000O =OOO0O0OO0O00OOOOO ['premiered']#line:532
            O000OOO0OO000000O =O000O0O0O00OO000O .findall ('(\d{4})',O000OOO0OO000000O )[0 ]#line:533
            O000OOO0OO000000O =O000OOO0OO000000O .encode ('utf-8')#line:534
            if not O000OOO0OO000000O =='0':OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ].update ({'year':O000OOO0OO000000O })#line:535
            try :O000OOOO0OOOO0O0O =OOO0O0OO0O00OOOOO ['externals']['imdb']#line:537
            except :O000OOOO0OOOO0O0O ='0'#line:538
            if O000OOOO0OOOO0O0O ==''or O000OOOO0OOOO0O0O ==None :O000OOOO0OOOO0O0O ='0'#line:539
            O000OOOO0OOOO0O0O =O000OOOO0OOOO0O0O .encode ('utf-8')#line:540
            if OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ]['imdb']=='0'and not O000OOOO0OOOO0O0O =='0':OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ].update ({'imdb':O000OOOO0OOOO0O0O })#line:541
            try :O00OO0O0OOO0OOO00 =OOO0O0OO0O00OOOOO ['network']['name']#line:543
            except :O00OO0O0OOO0OOO00 ='0'#line:544
            if O00OO0O0OOO0OOO00 ==''or O00OO0O0OOO0OOO00 ==None :O00OO0O0OOO0OOO00 ='0'#line:545
            O00OO0O0OOO0OOO00 =O00OO0O0OOO0OOO00 .encode ('utf-8')#line:546
            if not O00OO0O0OOO0OOO00 =='0':OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ].update ({'studio':O00OO0O0OOO0OOO00 })#line:547
            O0O000O00O000O0O0 =OOO0O0OO0O00OOOOO ['genres']#line:549
            if O0O000O00O000O0O0 ==''or O0O000O00O000O0O0 ==None or O0O000O00O000O0O0 ==[]:O0O000O00O000O0O0 ='0'#line:550
            O0O000O00O000O0O0 =' / '.join (O0O000O00O000O0O0 )#line:551
            O0O000O00O000O0O0 =O0O000O00O000O0O0 .encode ('utf-8')#line:552
            if not O0O000O00O000O0O0 =='0':OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ].update ({'genre':O0O000O00O000O0O0 })#line:553
            try :O000OO00O00OO0O0O =str (OOO0O0OO0O00OOOOO ['runtime'])#line:555
            except :O000OO00O00OO0O0O ='0'#line:556
            if O000OO00O00OO0O0O ==''or O000OO00O00OO0O0O ==None :O000OO00O00OO0O0O ='0'#line:557
            try :O000OO00O00OO0O0O =str (int (O000OO00O00OO0O0O )*60 )#line:558
            except :pass #line:559
            O000OO00O00OO0O0O =O000OO00O00OO0O0O .encode ('utf-8')#line:560
            if not O000OO00O00OO0O0O =='0':OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ].update ({'duration':O000OO00O00OO0O0O })#line:561
            OOOO0OOO0O0OOOO00 =str (OOO0O0OO0O00OOOOO ['rating']['average'])#line:563
            if OOOO0OOO0O0OOOO00 ==''or OOOO0OOO0O0OOOO00 ==None :OOOO0OOO0O0OOOO00 ='0'#line:564
            OOOO0OOO0O0OOOO00 =OOOO0OOO0O0OOOO00 .encode ('utf-8')#line:565
            if not OOOO0OOO0O0OOOO00 =='0':OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ].update ({'rating':OOOO0OOO0O0OOOO00 })#line:566
            O00OO00O00OO0OO00 =OOO0O0OO0O00OOOOO ['summary']#line:568
            if O00OO00O00OO0OO00 ==''or O00OO00O00OO0OO00 ==None :O00OO00O00OO0OO00 ='0'#line:569
            O00OO00O00OO0OO00 =O000O0O0O00OO000O .sub ('\n|<.+?>|</.+?>|.+?#\d*:','',O00OO00O00OO0OO00 )#line:570
            O00OO00O00OO0OO00 =O00OO00O00OO0OO00 .encode ('utf-8')#line:571
            if not O00OO00O00OO0OO00 =='0':OOOOO00OOOO0O0OOO .list [O000O0OOOO00O0O0O ].update ({'plot':O00OO00O00OO0OO00 })#line:572
            OOOOO00OOOO0O0OOO .meta .append ({'imdb':O000OOOO0OOOO0O0O ,'tmdb':'0','tvdb':OOO000OOOO00OOOOO ,'lang':OOOOO00OOOO0O0OOO .lang ,'item':{'tvshowtitle':OO0O000OOOOO0O0OO ,'year':O000OOO0OO000000O ,'code':O000OOOO0OOOO0O0O ,'imdb':O000OOOO0OOOO0O0O ,'tvdb':OOO000OOOO00OOOOO ,'studio':O00OO0O0OOO0OOO00 ,'genre':O0O000O00O000O0O0 ,'duration':O000OO00O00OO0O0O ,'rating':OOOO0OOO0O0OOOO00 ,'plot':O00OO00O00OO0OO00 }})#line:574
        except :#line:575
            pass #line:576
    def addDirectory (OOOOOOOOOO0OO0O00 ,O0OO000OO0O0O0OO0 ,queue =False ):#line:579
        if O0OO000OO0O0O0OO0 ==None or len (O0OO000OO0O0O0OO0 )==0 :return #line:580
        OO0O0OO00OOOOO0OO =O0O000O0O0OOOO00O .argv [0 ]#line:582
        O0O0OO0000OOO0OO0 =O0OO0O0OOO00OOO00 =O0OOOO0OOO00OO0OO .addonInfo ('icon')#line:583
        O0O0O0000OO00OOOO =O0OOOO0OOO00OO0OO .addonInfo ('fanart')#line:584
        O00O00O0000O000O0 =O0OOOO0OOO00OO0OO .playlist #line:586
        if not queue ==False :O00O00O0000O000O0 .clear ()#line:587
        try :OO0O0O00O000000OO =True if 'testings.xml'in O0OOOO0OOO00OO0OO .listDir (O0OOOO0OOO00OO0OO .dataPath )[1 ]else False #line:589
        except :OO0O0O00O000000OO =False #line:590
        OO0OO0O0OO0OO00O0 =[O0OO000000O0O000O ['content']for O0OO000000O0O000O in O0OO000OO0O0O0OO0 if 'content'in O0OO000000O0O000O ]#line:592
        if 'movies'in OO0OO0O0OO0OO00O0 :OO0OO0O0OO0OO00O0 ='movies'#line:593
        elif 'tvshows'in OO0OO0O0OO0OO00O0 :OO0OO0O0OO0OO00O0 ='tvshows'#line:594
        elif 'seasons'in OO0OO0O0OO0OO00O0 :OO0OO0O0OO0OO00O0 ='seasons'#line:595
        elif 'episodes'in OO0OO0O0OO0OO00O0 :OO0OO0O0OO0OO00O0 ='episodes'#line:596
        elif 'addons'in OO0OO0O0OO0OO00O0 :OO0OO0O0OO0OO00O0 ='addons'#line:597
        else :OO0OO0O0OO0OO00O0 ='videos'#line:598
        for OO000OO0O0O00O0OO in O0OO000OO0O0O0OO0 :#line:600
            try :#line:601
                try :O0000OO00O0OOO000 =O0OOOO0OOO00OO0OO .lang (int (OO000OO0O0O00O0OO ['name'])).encode ('utf-8')#line:602
                except :O0000OO00O0OOO000 =OO000OO0O0O00O0OO ['name']#line:603
                OO0O000O000O00O00 ='%s?action=%s'%(OO0O0OO00OOOOO0OO ,OO000OO0O0O00O0OO ['action'])#line:605
                try :OO0O000O000O00O00 +='&url=%s'%OO0OOOO0OOOOOOO00 .quote_plus (OO000OO0O0O00O0OO ['url'])#line:606
                except :pass #line:607
                try :OO0O000O000O00O00 +='&content=%s'%OO0OOOO0OOOOOOO00 .quote_plus (OO000OO0O0O00O0OO ['content'])#line:608
                except :pass #line:609
                if OO000OO0O0O00O0OO ['action']=='plugin'and 'url'in OO000OO0O0O00O0OO :OO0O000O000O00O00 =OO000OO0O0O00O0OO ['url']#line:611
                try :OOO00O0O0O0O00000 =dict (OO0O0OOO0O000OOO0 .parse_qsl (OO0O0OOO0O000OOO0 .urlparse (OO0O000O000O00O00 ).query ))['action']#line:613
                except :OOO00O0O0O0O00000 =None #line:614
                if OOO00O0O0O0O00000 =='developer'and not OO0O0O00O000000OO ==True :raise Exception ()#line:615
                OO00OO000O0OOO000 =OO000OO0O0O00O0OO ['poster']if 'poster'in OO000OO0O0O00O0OO else '0'#line:617
                O00O00O0OO0O00OO0 =OO000OO0O0O00O0OO ['banner']if 'banner'in OO000OO0O0O00O0OO else '0'#line:618
                OO0O00O000O0O0000 =OO000OO0O0O00O0OO ['fanart']if 'fanart'in OO000OO0O0O00O0OO else '0'#line:619
                if OO00OO000O0OOO000 =='0':OO00OO000O0OOO000 =O0O0OO0000OOO0OO0 #line:620
                if O00O00O0OO0O00OO0 =='0'and OO00OO000O0OOO000 =='0':O00O00O0OO0O00OO0 =O0OO0O0OOO00OOO00 #line:621
                elif O00O00O0OO0O00OO0 =='0':O00O00O0OO0O00OO0 =OO00OO000O0OOO000 #line:622
                O00O000000000OOOO =OO000OO0O0O00O0OO ['content']if 'content'in OO000OO0O0O00O0OO else '0'#line:624
                OOO00OO0O0000O0OO =OO000OO0O0O00O0OO ['folder']if 'folder'in OO000OO0O0O00O0OO else True #line:626
                OO0O0000O0OO000O0 =dict ((O000O0OO000OO0OO0 ,O0O0OO000000OO0OO )for O000O0OO000OO0OO0 ,O0O0OO000000OO0OO in OO000OO0O0O00O0OO .iteritems ()if not O0O0OO000000OO0OO =='0')#line:628
                O0OOO000O0OOOOOOO =[]#line:630
                if O00O000000000OOOO in ['movies','tvshows']:#line:632
                    OO0O0000O0OO000O0 .update ({'trailer':'%s?action=trailer&name=%s'%(OO0O0OO00OOOOO0OO ,OO0OOOO0OOOOOOO00 .quote_plus (O0000OO00O0OOO000 ))})#line:633
                    O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30707 ).encode ('utf-8'),'RunPlugin(%s?action=trailer&name=%s)'%(OO0O0OO00OOOOO0OO ,OO0OOOO0OOOOOOO00 .quote_plus (O0000OO00O0OOO000 ))))#line:634
                if O00O000000000OOOO in ['movies','tvshows','seasons','episodes']:#line:636
                    O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30708 ).encode ('utf-8'),'XBMC.Action(Info)'))#line:637
                if (OOO00OO0O0000O0OO ==False and not '|regex='in str (OO000OO0O0O00O0OO .get ('url')))or (OOO00OO0O0000O0OO ==True and O00O000000000OOOO in ['tvshows','seasons']):#line:639
                    O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30723 ).encode ('utf-8'),'RunPlugin(%s?action=queueItem)'%OO0O0OO00OOOOO0OO ))#line:640
                if O00O000000000OOOO =='movies':#line:642
                    try :O00000OOO0O00OOOO ='%s (%s)'%(OO000OO0O0O00O0OO ['title'],OO000OO0O0O00O0OO ['year'])#line:643
                    except :O00000OOO0O00OOOO =O0000OO00O0OOO000 #line:644
                    try :O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OO0O0OO00OOOOO0OO ,OO0OOOO0OOOOOOO00 .quote_plus (O00000OOO0O00OOOO ),OO0OOOO0OOOOOOO00 .quote_plus (OO000OO0O0O00O0OO ['url']),OO0OOOO0OOOOOOO00 .quote_plus (OO00OO000O0OOO000 ))))#line:645
                    except :pass #line:646
                elif O00O000000000OOOO =='episodes':#line:647
                    try :O00000OOO0O00OOOO ='%s S%02dE%02d'%(OO000OO0O0O00O0OO ['tvshowtitle'],int (OO000OO0O0O00O0OO ['season']),int (OO000OO0O0O00O0OO ['episode']))#line:648
                    except :O00000OOO0O00OOOO =O0000OO00O0OOO000 #line:649
                    try :O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OO0O0OO00OOOOO0OO ,OO0OOOO0OOOOOOO00 .quote_plus (O00000OOO0O00OOOO ),OO0OOOO0OOOOOOO00 .quote_plus (OO000OO0O0O00O0OO ['url']),OO0OOOO0OOOOOOO00 .quote_plus (OO00OO000O0OOO000 ))))#line:650
                    except :pass #line:651
                elif O00O000000000OOOO =='songs':#line:652
                    try :O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30722 ).encode ('utf-8'),'RunPlugin(%s?action=addDownload&name=%s&url=%s&image=%s)'%(OO0O0OO00OOOOO0OO ,OO0OOOO0OOOOOOO00 .quote_plus (O0000OO00O0OOO000 ),OO0OOOO0OOOOOOO00 .quote_plus (OO000OO0O0O00O0OO ['url']),OO0OOOO0OOOOOOO00 .quote_plus (OO00OO000O0OOO000 ))))#line:653
                    except :pass #line:654
                if OO0OO0O0OO0OO00O0 =='movies':#line:656
                    O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30711 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=movies)'%OO0O0OO00OOOOO0OO ))#line:657
                elif OO0OO0O0OO0OO00O0 =='tvshows':#line:658
                    O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30712 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=tvshows)'%OO0O0OO00OOOOO0OO ))#line:659
                elif OO0OO0O0OO0OO00O0 =='seasons':#line:660
                    O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30713 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=seasons)'%OO0O0OO00OOOOO0OO ))#line:661
                elif OO0OO0O0OO0OO00O0 =='episodes':#line:662
                    O0OOO000O0OOOOOOO .append ((O0OOOO0OOO00OO0OO .lang (30714 ).encode ('utf-8'),'RunPlugin(%s?action=addView&content=episodes)'%OO0O0OO00OOOOO0OO ))#line:663
                if OO0O0O00O000000OO ==True :#line:665
                    try :O0OOO000O0OOOOOOO .append (('Open in browser','RunPlugin(%s?action=browser&url=%s)'%(OO0O0OO00OOOOO0OO ,OO0OOOO0OOOOOOO00 .quote_plus (OO000OO0O0O00O0OO ['url']))))#line:666
                    except :pass #line:667
                O0000O0OOO0O00OO0 =O0OOOO0OOO00OO0OO .item (label =O0000OO00O0OOO000 ,iconImage =OO00OO000O0OOO000 ,thumbnailImage =OO00OO000O0OOO000 )#line:670
                try :O0000O0OOO0O00OO0 .setArt ({'poster':OO00OO000O0OOO000 ,'tvshow.poster':OO00OO000O0OOO000 ,'season.poster':OO00OO000O0OOO000 ,'banner':O00O00O0OO0O00OO0 ,'tvshow.banner':O00O00O0OO0O00OO0 ,'season.banner':O00O00O0OO0O00OO0 })#line:672
                except :pass #line:673
                if not OO0O00O000O0O0000 =='0':#line:675
                    O0000O0OOO0O00OO0 .setProperty ('Fanart_Image',OO0O00O000O0O0000 )#line:676
                elif not O0O0O0000OO00OOOO ==None :#line:677
                    O0000O0OOO0O00OO0 .setProperty ('Fanart_Image',O0O0O0000OO00OOOO )#line:678
                if queue ==False :#line:680
                    O0000O0OOO0O00OO0 .setInfo (type ='Video',infoLabels =OO0O0000O0OO000O0 )#line:681
                    O0000O0OOO0O00OO0 .addContextMenuItems (O0OOO000O0OOOOOOO )#line:682
                    O0OOOO0OOO00OO0OO .addItem (handle =int (O0O000O0O0OOOO00O .argv [1 ]),url =OO0O000O000O00O00 ,listitem =O0000O0OOO0O00OO0 ,isFolder =OOO00OO0O0000O0OO )#line:683
                else :#line:684
                    O0000O0OOO0O00OO0 .setInfo (type ='Video',infoLabels =OO0O0000O0OO000O0 )#line:685
                    O00O00O0000O000O0 .add (url =OO0O000O000O00O00 ,listitem =O0000O0OOO0O00OO0 )#line:686
            except :#line:687
                pass #line:688
        if not queue ==False :#line:690
            return O0OOOO0OOO00OO0OO .player .play (O00O00O0000O000O0 )#line:691
        try :#line:693
            OO000OO0O0O00O0OO =O0OO000OO0O0O0OO0 [0 ]#line:694
            if OO000OO0O0O00O0OO ['next']=='':raise Exception ()#line:695
            OO0O000O000O00O00 ='%s?action=%s&url=%s'%(OO0O0OO00OOOOO0OO ,OO000OO0O0O00O0OO ['nextaction'],OO0OOOO0OOOOOOO00 .quote_plus (OO000OO0O0O00O0OO ['next']))#line:696
            O0000O0OOO0O00OO0 =O0OOOO0OOO00OO0OO .item (label =O0OOOO0OOO00OO0OO .lang (30500 ).encode ('utf-8'))#line:697
            O0000O0OOO0O00OO0 .setArt ({'addonPoster':O0O0OO0000OOO0OO0 ,'thumb':O0O0OO0000OOO0OO0 ,'poster':O0O0OO0000OOO0OO0 ,'tvshow.poster':O0O0OO0000OOO0OO0 ,'season.poster':O0O0OO0000OOO0OO0 ,'banner':O0O0OO0000OOO0OO0 ,'tvshow.banner':O0O0OO0000OOO0OO0 ,'season.banner':O0O0OO0000OOO0OO0 })#line:698
            O0000O0OOO0O00OO0 .setProperty ('addonFanart_Image',O0O0O0000OO00OOOO )#line:699
            O0OOOO0OOO00OO0OO .addItem (handle =int (O0O000O0O0OOOO00O .argv [1 ]),url =OO0O000O000O00O00 ,listitem =O0000O0OOO0O00OO0 ,isFolder =True )#line:700
        except :#line:701
            pass #line:702
        if not OO0OO0O0OO0OO00O0 ==None :O0OOOO0OOO00OO0OO .content (int (O0O000O0O0OOOO00O .argv [1 ]),OO0OO0O0OO0OO00O0 )#line:704
        O0OOOO0OOO00OO0OO .directory (int (O0O000O0O0OOOO00O .argv [1 ]),cacheToDisc =True )#line:705
        if OO0OO0O0OO0OO00O0 in ['movies','tvshows','seasons','episodes']:#line:706
            OOO00O0OO0OOOO0OO .setView (OO0OO0O0OO0OO00O0 ,{'skin.estuary':55 })#line:707
class resolver :#line:711
    def browser (O00000O0OO0OO0O00 ,OOOOO0O00O000OOO0 ):#line:712
        try :#line:713
            OOOOO0O00O000OOO0 =O00000O0OO0OO0O00 .get (OOOOO0O00O000OOO0 )#line:714
            if OOOOO0O00O000OOO0 ==False :return #line:715
            O0OOOO0OOO00OO0OO .execute ('RunPlugin(plugin://plugin.program.chrome.launcher/?url=%s&mode=showSite&stopPlayback=no)'%OO0OOOO0OOOOOOO00 .quote_plus (OOOOO0O00O000OOO0 ))#line:716
        except :#line:717
            pass #line:718
    def link (OOOOOO00OOOO0000O ,O00OOOO000O0O00O0 ):#line:721
        try :#line:722
            O00OOOO000O0O00O0 =OOOOOO00OOOO0000O .get (O00OOOO000O0O00O0 )#line:723
            if O00OOOO000O0O00O0 ==False :return #line:724
            O0OOOO0OOO00OO0OO .execute ('ActivateWindow(busydialog)')#line:726
            O00OOOO000O0O00O0 =OOOOOO00OOOO0000O .process (O00OOOO000O0O00O0 )#line:727
            O0OOOO0OOO00OO0OO .execute ('Dialog.Close(busydialog)')#line:728
            if O00OOOO000O0O00O0 ==None :return O0OOOO0OOO00OO0OO .infoDialog (O0OOOO0OOO00OO0OO .lang (30705 ).encode ('utf-8'))#line:730
            return O00OOOO000O0O00O0 #line:731
        except :#line:732
            pass #line:733
    def get (OOO0OO0O0O0O0O00O ,O000O00O0OO0OO000 ):#line:736
        try :#line:737
            OO0O0O0O0OO0O0OO0 =O000O0O0O00OO000O .compile ('<sublink(?:\s+name=|)(?:\'|\"|)(.*?)(?:\'|\"|)>(.+?)</sublink>').findall (O000O00O0OO0OO000 )#line:738
            if len (OO0O0O0O0OO0O0OO0 )==0 :return O000O00O0OO0OO000 #line:740
            if len (OO0O0O0O0OO0O0OO0 )==1 :return OO0O0O0O0OO0O0OO0 [0 ][1 ]#line:741
            OO0O0O0O0OO0O0OO0 =[('Link %s'%(int (OO0O0O0O0OO0O0OO0 .index (OO0O000OO0000OOOO ))+1 )if OO0O000OO0000OOOO [0 ]==''else OO0O000OO0000OOOO [0 ],OO0O000OO0000OOOO [1 ])for OO0O000OO0000OOOO in OO0O0O0O0OO0O0OO0 ]#line:743
            O0O0000OOO000O00O =O0OOOO0OOO00OO0OO .selectDialog ([OO0O0O0OO0OOOO000 [0 ]for OO0O0O0OO0OOOO000 in OO0O0O0O0OO0O0OO0 ],O0OOOO0OOO00OO0OO .infoLabel ('listitem.label'))#line:745
            if O0O0000OOO000O00O ==-1 :return False #line:747
            else :return OO0O0O0O0OO0O0OO0 [O0O0000OOO000O00O ][1 ]#line:748
        except :#line:749
            pass #line:750
    def f4m (O00OOOOO0O0O0OOOO ,O00O000OO0000OO0O ,OO000O0OO00OO0O00 ):#line:753
            try :#line:754
                if not any (OO00OO0O0O000O0OO in O00O000OO0000OO0O for OO00OO0O0O000O0OO in ['.f4m','.ts']):raise Exception ()#line:755
                O000OO0OOOOOO0OOO =O00O000OO0000OO0O .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:756
                if not O000OO0OOOOOO0OOO in ['f4m','ts']:raise Exception ()#line:757
                OOOO00000000O000O =OO0O0OOO0O000OOO0 .parse_qs (O00O000OO0000OO0O )#line:759
                try :O0O000O00OOOOO00O =OOOO00000000O000O ['proxy'][0 ]#line:761
                except :O0O000O00OOOOO00O =None #line:762
                try :OOO00OOOO0O0O00O0 =OOOOO0OOOOOOOOO00 .loads (OOOO00000000O000O ['proxy_for_chunks'][0 ])#line:764
                except :OOO00OOOO0O0O00O0 =True #line:765
                try :OO0OOOOO0OO00OO0O =int (OOOO00000000O000O ['maxbitrate'][0 ])#line:767
                except :OO0OOOOO0OO00OO0O =0 #line:768
                try :OO0O0OOOOO000OO00 =OOOOO0OOOOOOOOO00 .loads (OOOO00000000O000O ['simpledownloader'][0 ])#line:770
                except :OO0O0OOOOO000OO00 =False #line:771
                try :OOOO000O0O0OO000O =OOOO00000000O000O ['auth'][0 ]#line:773
                except :OOOO000O0O0OO000O =''#line:774
                try :OO00OO0OO0O0O000O =OOOO00000000O000O ['streamtype'][0 ]#line:776
                except :OO00OO0OO0O0O000O ='TSDOWNLOADER'if O000OO0OOOOOO0OOO =='ts'else 'HDS'#line:777
                try :O0000O00000O000O0 =OOOO00000000O000O ['swf'][0 ]#line:779
                except :O0000O00000O000O0 =None #line:780
                from F4mProxy import f4mProxyHelper as O0000OOO0O0OOOOO0 #line:782
                return O0000OOO0O0OOOOO0 ().playF4mLink (O00O000OO0000OO0O ,OO000O0OO00OO0O00 ,O0O000O00OOOOO00O ,OOO00OOOO0O0O00O0 ,OO0OOOOO0OO00OO0O ,OO0O0OOOOO000OO00 ,OOOO000O0O0OO000O ,OO00OO0OO0O0O000O ,False ,O0000O00000O000O0 )#line:783
            except :#line:784
                pass #line:785
    def process (O0OO0OOO000OO0OO0 ,O00000O0OO0O00OOO ,direct =True ):#line:788
        try :#line:789
            if not any (O00O00OO00000O0O0 in O00000O0OO0O00OOO for O00O00OO00000O0O0 in ['.jpg','.png','.gif']):raise Exception ()#line:790
            OOO0O00O0O0O0O000 =O00000O0OO0O00OOO .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:791
            if not OOO0O00O0O0O0O000 in ['jpg','png','gif']:raise Exception ()#line:792
            try :#line:793
                O000OO000000O0000 =OO0O0O0OOO0000O00 .path .join (O0OOOO0OOO00OO0OO .dataPath ,'img')#line:794
                O0OOOO0OOO00OO0OO .deleteFile (O000OO000000O0000 )#line:795
                O0O0OO0O000OOOO0O =O0OOOO0OOO00OO0OO .openFile (O000OO000000O0000 ,'w')#line:796
                O0O0OO0O000OOOO0O .write (O0OOOO000O0O00O0O .request (O00000O0OO0O00OOO ))#line:797
                O0O0OO0O000OOOO0O .close ()#line:798
                O0OOOO0OOO00OO0OO .execute ('ShowPicture("%s")'%O000OO000000O0000 )#line:799
                return False #line:800
            except :#line:801
                return #line:802
        except :#line:803
            pass #line:804
        try :#line:806
            OOO0OOOOO00000OOO ,OOOOOO0000OOO0OO0 =O000O0O0O00OO000O .findall ('(.+?)\|regex=(.+?)$',O00000O0OO0O00OOO )[0 ]#line:807
            OOOOOO0000OOO0OO0 =OO0OO0O0000OOO0OO .fetch (OOOOOO0000OOO0OO0 )#line:808
            OOO0OOOOO00000OOO +=OO0OOOO0OOOOOOO00 .unquote_plus (OOOOOO0000OOO0OO0 )#line:809
            if not '</regex>'in OOO0OOOOO00000OOO :raise Exception ()#line:810
            O0O000O00O0OOO00O =OO0OO0O0000OOO0OO .resolve (OOO0OOOOO00000OOO )#line:811
            if not O0O000O00O0OOO00O ==None :O00000O0OO0O00OOO =O0O000O00O0OOO00O #line:812
        except :#line:813
            pass #line:814
        try :#line:816
            if not O00000O0OO0O00OOO .startswith ('rtmp'):raise Exception ()#line:817
            if len (O000O0O0O00OO000O .compile ('\s*timeout=(\d*)').findall (O00000O0OO0O00OOO ))==0 :O00000O0OO0O00OOO +=' timeout=10'#line:818
            return O00000O0OO0O00OOO #line:819
        except :#line:820
            pass #line:821
        try :#line:823
            if not any (O0OO0O0O0OO0OOOO0 in O00000O0OO0O00OOO for O0OO0O0O0OO0OOOO0 in ['.m3u8','.f4m','.ts']):raise Exception ()#line:824
            OOO0O00O0O0O0O000 =O00000O0OO0O00OOO .split ('?')[0 ].split ('&')[0 ].split ('|')[0 ].rsplit ('.')[-1 ].replace ('/','').lower ()#line:825
            if not OOO0O00O0O0O0O000 in ['m3u8','f4m','ts']:raise Exception ()#line:826
            return O00000O0OO0O00OOO #line:827
        except :#line:828
            pass #line:829
        try :#line:831
            OO00O000OOOOO00O0 =O000O0O0O00OO000O .findall ('<preset>(.+?)</preset>',O00000O0OO0O00OOO )[0 ]#line:832
            if not 'search'in OO00O000OOOOO00O0 :raise Exception ()#line:834
            OOO00OO0O0O0O0000 ,OO00OO00OOO00O000 ,O0O0OO000OOO0O000 =O000O0O0O00OO000O .findall ('<title>(.+?)</title>',O00000O0OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<year>(.+?)</year>',O00000O0OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<imdb>(.+?)</imdb>',O00000O0OO0O00OOO )[0 ]#line:836
            try :OO00O000O0000O000 ,OOO00O0O00OOO0OO0 ,OOO00000O0OOOOO00 ,OOO000OO0O0O0O000 ,O000OO0OO0OOO00OO =O000O0O0O00OO000O .findall ('<tvdb>(.+?)</tvdb>',O00000O0OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<tvshowtitle>(.+?)</tvshowtitle>',O00000O0OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<premiered>(.+?)</premiered>',O00000O0OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<season>(.+?)</season>',O00000O0OO0O00OOO )[0 ],O000O0O0O00OO000O .findall ('<episode>(.+?)</episode>',O00000O0OO0O00OOO )[0 ]#line:838
            except :OO00O000O0000O000 =OOO00O0O00OOO0OO0 =OOO00000O0OOOOO00 =OOO000OO0O0O0O000 =O000OO0OO0OOO00OO =None #line:839
            direct =False #line:841
            O000OOOO0O0OO000O ='HD'if not OO00O000OOOOO00O0 =='searchsd'else 'SD'#line:843
            from resources .lib .sources import sources as O00O0OO000OOO00O0 #line:845
            O0O000O00O0OOO00O =O00O0OO000OOO00O0 ().getSources (OOO00OO0O0O0O0000 ,OO00OO00OOO00O000 ,O0O0OO000OOO0O000 ,OO00O000O0000O000 ,OOO000OO0O0O0O000 ,O000OO0OO0OOO00OO ,OOO00O0O00OOO0OO0 ,OOO00000O0OOOOO00 ,O000OOOO0O0OO000O )#line:847
            if not O0O000O00O0OOO00O ==None :return O0O000O00O0OOO00O #line:849
        except :#line:850
            pass #line:851
        try :#line:853
            from resources .lib .sources import sources as O00O0OO000OOO00O0 #line:854
            O0O000O00O0OOO00O =O00O0OO000OOO00O0 ().getURISource (O00000O0OO0O00OOO )#line:856
            if not O0O000O00O0OOO00O ==False :direct =False #line:858
            if O0O000O00O0OOO00O ==None or O0O000O00O0OOO00O ==False :raise Exception ()#line:859
            return O0O000O00O0OOO00O #line:861
        except :#line:862
            pass #line:863
        try :#line:865
            if not '.google.com'in O00000O0OO0O00OOO :raise Exception ()#line:866
            from resources .lib .modules import directstream as O0OO0OO00000000O0 #line:867
            O0O000O00O0OOO00O =O0OO0OO00000000O0 .google (O00000O0OO0O00OOO )[0 ]['url']#line:868
            return O0O000O00O0OOO00O #line:869
        except :#line:870
            pass #line:871
        try :#line:873
            if not 'filmon.com/'in O00000O0OO0O00OOO :raise Exception ()#line:874
            from resources .lib .modules import filmon as O00O000OO000OO0O0 #line:875
            O0O000O00O0OOO00O =O00O000OO000OO0O0 .resolve (O00000O0OO0O00OOO )#line:876
            return O0O000O00O0OOO00O #line:877
        except :#line:878
            pass #line:879
        try :#line:881
            import urlresolver as OO0OO0OOO000O0OO0 #line:882
            O00O0O000000O00OO =OO0OO0OOO000O0OO0 .HostedMediaFile (url =O00000O0OO0O00OOO )#line:884
            if O00O0O000000O00OO .valid_url ()==False :raise Exception ()#line:886
            direct =False ;O0O000O00O0OOO00O =O00O0O000000O00OO .resolve ()#line:888
            if not O0O000O00O0OOO00O ==False :return O0O000O00O0OOO00O #line:890
        except :#line:891
            pass #line:892
        if direct ==True :return O00000O0OO0O00OOO #line:894
class player (OO0000O00000OO00O .Player ):#line:897
    def __init__ (OO0O0O0000OOO0000 ):#line:898
        OO0000O00000OO00O .Player .__init__ (OO0O0O0000OOO0000 )#line:899
    def play (OOO0000O00O00O0O0 ,OOO0O0OOOOOO0OO0O ,content =None ):#line:902
        try :#line:903
            OO00O000O0O000O00 =OOO0O0OOOOOO0OO0O #line:904
            OOO0O0OOOOOO0OO0O =resolver ().get (OOO0O0OOOOOO0OO0O )#line:906
            if OOO0O0OOOOOO0OO0O ==False :return #line:907
            O0OOOO0OOO00OO0OO .execute ('ActivateWindow(busydialog)')#line:909
            OOO0O0OOOOOO0OO0O =resolver ().process (OOO0O0OOOOOO0OO0O )#line:910
            O0OOOO0OOO00OO0OO .execute ('Dialog.Close(busydialog)')#line:911
            if OOO0O0OOOOOO0OO0O ==None :return O0OOOO0OOO00OO0OO .infoDialog (O0OOOO0OOO00OO0OO .lang (30705 ).encode ('utf-8'))#line:913
            if OOO0O0OOOOOO0OO0O ==False :return #line:914
            O0O0O0000OOOO00OO ={}#line:916
            for O00O0O00000O00O00 in ['title','originaltitle','tvshowtitle','year','season','episode','genre','rating','votes','director','writer','plot','tagline']:#line:917
                try :O0O0O0000OOOO00OO [O00O0O00000O00O00 ]=O0OOOO0OOO00OO0OO .infoLabel ('listitem.%s'%O00O0O00000O00O00 )#line:918
                except :pass #line:919
            O0O0O0000OOOO00OO =dict ((O0000OO0O000O0OOO ,OOO0O00OO0000O0O0 )for O0000OO0O000O0OOO ,OOO0O00OO0000O0O0 in O0O0O0000OOOO00OO .iteritems ()if not OOO0O00OO0000O0O0 =='')#line:920
            if not 'title'in O0O0O0000OOOO00OO :O0O0O0000OOOO00OO ['title']=O0OOOO0OOO00OO0OO .infoLabel ('listitem.label')#line:921
            O0O0O0O000000OO00 =O0OOOO0OOO00OO0OO .infoLabel ('listitem.icon')#line:922
            OOO0000O00O00O0O0 .name =O0O0O0000OOOO00OO ['title'];OOO0000O00O00O0O0 .year =O0O0O0000OOOO00OO ['year']if 'year'in O0O0O0000OOOO00OO else '0'#line:925
            OOO0000O00O00O0O0 .getbookmark =True if (content =='movies'or content =='episodes')else False #line:927
            OOO0000O00O00O0O0 .offset =bookmarks ().get (OOO0000O00O00O0O0 .name ,OOO0000O00O00O0O0 .year )#line:929
            O0OOOOOOO00O0O0OO =resolver ().f4m (OOO0O0OOOOOO0OO0O ,OOO0000O00O00O0O0 .name )#line:931
            if not O0OOOOOOO00O0O0OO ==None :return #line:932
            O0OOO00O0OOO000O0 =O0OOOO0OOO00OO0OO .item (path =OOO0O0OOOOOO0OO0O ,iconImage =O0O0O0O000000OO00 ,thumbnailImage =O0O0O0O000000OO00 )#line:935
            try :O0OOO00O0OOO000O0 .setArt ({'icon':O0O0O0O000000OO00 })#line:936
            except :pass #line:937
            O0OOO00O0OOO000O0 .setInfo (type ='Video',infoLabels =O0O0O0000OOOO00OO )#line:938
            O0OOOO0OOO00OO0OO .player .play (OOO0O0OOOOOO0OO0O ,O0OOO00O0OOO000O0 )#line:939
            O0OOOO0OOO00OO0OO .resolve (int (O0O000O0O0OOOO00O .argv [1 ]),True ,O0OOO00O0OOO000O0 )#line:940
            OOO0000O00O00O0O0 .totalTime =0 ;OOO0000O00O00O0O0 .currentTime =0 #line:942
            for O00O0O00000O00O00 in range (0 ,240 ):#line:944
                if OOO0000O00O00O0O0 .isPlayingVideo ():break #line:945
                O0OOOO0OOO00OO0OO .sleep (1000 )#line:946
            while OOO0000O00O00O0O0 .isPlayingVideo ():#line:947
                try :#line:948
                    OOO0000O00O00O0O0 .totalTime =OOO0000O00O00O0O0 .getTotalTime ()#line:949
                    OOO0000O00O00O0O0 .currentTime =OOO0000O00O00O0O0 .getTime ()#line:950
                except :#line:951
                    pass #line:952
                O0OOOO0OOO00OO0OO .sleep (2000 )#line:953
            O0OOOO0OOO00OO0OO .sleep (5000 )#line:954
        except :#line:955
            pass #line:956
    def onPlayBackStarted (OOO0O0OO000O0O0O0 ):#line:959
        O0OOOO0OOO00OO0OO .execute ('Dialog.Close(all,true)')#line:960
        if OOO0O0OO000O0O0O0 .getbookmark ==True and not OOO0O0OO000O0O0O0 .offset =='0':#line:961
            OOO0O0OO000O0O0O0 .seekTime (float (OOO0O0OO000O0O0O0 .offset ))#line:962
    def onPlayBackStopped (O00O0OOO0OOO00O0O ):#line:965
        if O00O0OOO0OOO00O0O .getbookmark ==True :#line:966
            bookmarks ().reset (O00O0OOO0OOO00O0O .currentTime ,O00O0OOO0OOO00O0O .totalTime ,O00O0OOO0OOO00O0O .name ,O00O0OOO0OOO00O0O .year )#line:967
    def onPlayBackEnded (O0000O00O0OO00OO0 ):#line:970
        O0000O00O0OO00OO0 .onPlayBackStopped ()#line:971
class bookmarks :#line:975
    def get (O0O00OO0O000OOO00 ,OO0O000O0OO000O00 ,year ='0'):#line:976
        try :#line:977
            O0OO00OO0OO000O00 ='0'#line:978
            O0000O000000O000O =OOOOOO0O00O0OO0O0 .md5 ()#line:982
            for O0O0O00O0O0000000 in OO0O000O0OO000O00 :O0000O000000O000O .update (str (O0O0O00O0O0000000 ))#line:983
            for O0O0O00O0O0000000 in year :O0000O000000O000O .update (str (O0O0O00O0O0000000 ))#line:984
            O0000O000000O000O =str (O0000O000000O000O .hexdigest ())#line:985
            O0OO0O0000O000O0O =OO000OOOOOO0OOO0O .connect (O0OOOO0OOO00OO0OO .bookmarksFile )#line:987
            OO0OO000000O0OO00 =O0OO0O0000O000O0O .cursor ()#line:988
            OO0OO000000O0OO00 .execute ("SELECT * FROM bookmark WHERE idFile = '%s'"%O0000O000000O000O )#line:989
            O00O000000OOO0OO0 =OO0OO000000O0OO00 .fetchone ()#line:990
            O0O00OO0O000OOO00 .offset =str (O00O000000OOO0OO0 [1 ])#line:991
            O0OO0O0000O000O0O .commit ()#line:992
            if O0O00OO0O000OOO00 .offset =='0':raise Exception ()#line:994
            OO00OOO0OOOOOOO00 ,OOO0000O00OOOO0OO =divmod (float (O0O00OO0O000OOO00 .offset ),60 );O000OOOO00OOO0OO0 ,OO00OOO0OOOOOOO00 =divmod (OO00OOO0OOOOOOO00 ,60 )#line:996
            O0O0O0O0OO0OO0000 ='%02d:%02d:%02d'%(O000OOOO00OOO0OO0 ,OO00OOO0OOOOOOO00 ,OOO0000O00OOOO0OO )#line:997
            O0O0O0O0OO0OO0000 =(O0OOOO0OOO00OO0OO .lang (32502 )%O0O0O0O0OO0OO0000 ).encode ('utf-8')#line:998
            try :OOO00O0000O00O000 =O0OOOO0OOO00OO0OO .dialog .contextmenu ([O0O0O0O0OO0OO0000 ,O0OOOO0OOO00OO0OO .lang (32501 ).encode ('utf-8'),])#line:1000
            except :OOO00O0000O00O000 =O0OOOO0OOO00OO0OO .yesnoDialog (O0O0O0O0OO0OO0000 ,'','',str (OO0O000O0OO000O00 ),O0OOOO0OOO00OO0OO .lang (32503 ).encode ('utf-8'),O0OOOO0OOO00OO0OO .lang (32501 ).encode ('utf-8'))#line:1001
            if OOO00O0000O00O000 :O0O00OO0O000OOO00 .offset ='0'#line:1003
            return O0O00OO0O000OOO00 .offset #line:1005
        except :#line:1006
            return O0OO00OO0OO000O00 #line:1007
    def reset (O0OOO0O000O0O0000 ,OO000O000OOO0OOOO ,OO000O0O000OO0O0O ,O00OO0O0000000OO0 ,year ='0'):#line:1010
        try :#line:1011
            OO00OO00OO00O000O =str (OO000O000OOO0OOOO )#line:1014
            OOOO00OO0000OO000 =int (OO000O000OOO0OOOO )>180 and (OO000O000OOO0OOOO /OO000O0O000OO0O0O )<=.92 #line:1015
            O00OOOOOO0O0OO0OO =OOOOOO0O00O0OO0O0 .md5 ()#line:1017
            for O00O00O0000OO00O0 in O00OO0O0000000OO0 :O00OOOOOO0O0OO0OO .update (str (O00O00O0000OO00O0 ))#line:1018
            for O00O00O0000OO00O0 in year :O00OOOOOO0O0OO0OO .update (str (O00O00O0000OO00O0 ))#line:1019
            O00OOOOOO0O0OO0OO =str (O00OOOOOO0O0OO0OO .hexdigest ())#line:1020
            O0OOOO0OOO00OO0OO .makeFile (O0OOOO0OOO00OO0OO .dataPath )#line:1022
            O000O00OO0OOO0OO0 =OO000OOOOOO0OOO0O .connect (O0OOOO0OOO00OO0OO .bookmarksFile )#line:1023
            O0OO0OOO00O0O0OOO =O000O00OO0OOO0OO0 .cursor ()#line:1024
            O0OO0OOO00O0O0OOO .execute ("CREATE TABLE IF NOT EXISTS bookmark (" "idFile TEXT, " "timeInSeconds TEXT, " "UNIQUE(idFile)" ");")#line:1025
            O0OO0OOO00O0O0OOO .execute ("DELETE FROM bookmark WHERE idFile = '%s'"%O00OOOOOO0O0OO0OO )#line:1026
            if OOOO00OO0000OO000 :O0OO0OOO00O0O0OOO .execute ("INSERT INTO bookmark Values (?, ?)",(O00OOOOOO0O0OO0OO ,OO00OO00OO00O000O ))#line:1027
            O000O00OO0OOO0OO0 .commit ()#line:1028
        except :#line:1029
            pass 
#e9015584e6a44b14988f13e2298bcbf9

