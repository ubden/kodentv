# -*- coding: utf-8 -*-

import os,sys,re,json,urllib,urlparse,base64,datetime,unicodedata
from resources.lib.modules import trakt,control,client,cache,metacache
from resources.lib.modules import playcount,workers,views
try:
    action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except:
    action = None


class movies:
    def __init__(self):
        self.list = []
        self.tmdb_link = 'https://api.themoviedb.org'
        self.trakt_link = 'https://api.trakt.tv'
        self.imdb_link = 'http://www.imdb.com'
        self.tmdb_key = control.setting('tm.user')
        if self.tmdb_key == '' or self.tmdb_key == None:
            self.tmdb_key = base64.b64decode('YzhiN2RiNzAxYmFjMGIyNmVkZmNjOTNiMzk4NTg5NzI=')
        self.omdb_key = control.setting('omdb.key')
        if self.omdb_key == '' or self.omdb_key == None:
            self.omdb_key = '74703860'
        self.trakt_user = re.sub('[^a-z0-9]', '-', control.setting('trakt.user').strip().lower())
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tmdb_lang = 'en'
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        self.year_date = (self.datetime - datetime.timedelta(days = 365)).strftime('%Y-%m-%d')
        self.tmdb_info_link = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=credits,releases,external_ids' % ('%s', self.tmdb_key, self.tmdb_lang)
        self.tmdb_by_query_imdb = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % ("%s", self.tmdb_key)
        self.imdb_by_query = 'http://www.omdbapi.com/?t=%s&y=%s&apikey=%s' % ("%s", "%s", self.omdb_key)
        self.imdbinfo = 'http://www.omdbapi.com/?i=%s&plot=full&r=json&apikey=%s' % ("%s", self.omdb_key)
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_poster = 'http://image.tmdb.org/t/p/w500'
        self.search_link = 'https://api.themoviedb.org/3/search/movie?&api_key=%s&query=%s'

        self.popular_link = 'https://api.themoviedb.org/3/movie/popular?api_key=%s&page=1' % self.tmdb_key
        self.toprated_link = 'https://api.themoviedb.org/3/movie/top_rated?api_key=%s&page=1' % self.tmdb_key
        self.featured_link = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&primary_release_date.gte=date[365]&primary_release_date.lte=date[60]&page=1' % self.tmdb_key
        self.theaters_link = 'https://api.themoviedb.org/3/movie/now_playing?api_key=%s&page=1' % self.tmdb_key
        self.premiere_link = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&first_air_date.gte=%s&first_air_date.lte=%s&page=1' % (self.tmdb_key, self.year_date, self.today_date)

        self.tmdbUserLists_link = 'https://api.themoviedb.org/4/list/%s?api_key=%s' % ("%s", self.tmdb_key)
        self.tmdbjewtestmovies_link = self.tmdbUserLists_link % ('97123')
        self.tmdbjewmovies_link = self.tmdbUserLists_link % ('86696')


    def get(self, url, idx=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass
            try:
                u = urlparse.urlparse(url).netloc.lower()
            except:
                pass
            if u in self.tmdb_link:
                self.list = cache.get(self.tmdb_list, 24, url)
                self.worker()
            elif u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakthistory_link:
                        raise Exception()
                    if not '/%s/' % self.trakt_user in url:
                        raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url):
                        raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url)
                except:
                    self.list = cache.get(self.trakt_list, 0, url)
                if '/%s/' % self.trakt_user in url:
                    self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a )', '', k['title'].lower()))
                if idx == True:
                    self.worker()
            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url)
                if idx == True:
                    self.worker()
            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True:
                    self.worker()
            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True:
                    self.worker()
            if idx == True:
                self.movieDirectory(self.list)
            return self.list
        except:
            pass


    def my_tmdbUserLists(self):
        movielist1 = control.setting('tmdb.movielist_name1')
        movielist1_link = control.setting('tmdb.movielist_id1')
        if movielist1:
            self.list.append({'name': movielist1, 'url': self.tmdbUserLists_link % movielist1_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist2 = control.setting('tmdb.movielist_name2')
        movielist2_link = control.setting('tmdb.movielist_id2')
        if movielist2:
            self.list.append({'name': movielist2, 'url': self.tmdbUserLists_link % movielist2_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist3 = control.setting('tmdb.movielist_name3')
        movielist3_link = control.setting('tmdb.movielist_id3')
        if movielist3:
            self.list.append({'name': movielist3, 'url': self.tmdbUserLists_link % movielist3_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist4 = control.setting('tmdb.movielist_name4')
        movielist4_link = control.setting('tmdb.movielist_id4')
        if movielist4:
            self.list.append({'name': movielist4, 'url': self.tmdbUserLists_link % movielist4_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist5 = control.setting('tmdb.movielist_name5')
        movielist5_link = control.setting('tmdb.movielist_id5')
        if movielist5:
            self.list.append({'name': movielist5, 'url': self.tmdbUserLists_link % movielist5_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist6 = control.setting('tmdb.movielist_name6')
        movielist6_link = control.setting('tmdb.movielist_id6')
        if movielist6:
            self.list.append({'name': movielist6, 'url': self.tmdbUserLists_link % movielist6_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist7 = control.setting('tmdb.movielist_name7')
        movielist7_link = control.setting('tmdb.movielist_id7')
        if movielist7:
            self.list.append({'name': movielist7, 'url': self.tmdbUserLists_link % movielist7_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist8 = control.setting('tmdb.movielist_name8')
        movielist8_link = control.setting('tmdb.movielist_id8')
        if movielist8:
            self.list.append({'name': movielist8, 'url': self.tmdbUserLists_link % movielist8_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist9 = control.setting('tmdb.movielist_name9')
        movielist9_link = control.setting('tmdb.movielist_id9')
        if movielist9:
            self.list.append({'name': movielist9, 'url': self.tmdbUserLists_link % movielist9_link, 'image': 'tmdb.png', 'action': 'movies2'})
        movielist10 = control.setting('tmdb.movielist_name10')
        movielist10_link = control.setting('tmdb.movielist_id10')
        if movielist10:
            self.list.append({'name': movielist10, 'url': self.tmdbUserLists_link % movielist10_link, 'image': 'tmdb.png', 'action': 'movies2'})
        self.addDirectory(self.list)
        return self.list


    def tmdbUserLists_ActorCollections(self):
        theUserLists = [
            ('Adam Sandler', '32777'),
            ('Al Pacino', '32815'),
            ('Alan Rickman', '32819'),
            ('Angelina Jolie', '32821'),
            ('Anthony Hopkins', '32820'),
            ('Arnold Schwarzenegger', '32825'),
            ('Bruce Lee', '13295'),
            ('Charlize Theron', '32826'),
            ('Clint Eastwood', '32827'),
            ('Demi Moore', '32828'),
            ('Denzel Washington', '32829'),
            ('Eddie Murphy', '32830'),
            ('Elvis Presley', '32831'),
            ('Gene Wilder', '32999'),
            ('Gerard Butler', '33000'),
            ('Goldie Hawn', '33023'),
            ('Jason Statham', '33001'),
            ('Jean-Claude Van Damme', '33002'),
            ('Jeffrey Dean Morgan', '33003'),
            ('John Travolta', '33004'),
            ('Johnny Depp', '33005'),
            ('Julia Roberts', '33006'),
            ('Kevin Costner', '33015'),
            ('Liam Neeson', '33016'),
            ('Mel Gibson', '33017'),
            ('Melissa McCarthy', '33020'),
            ('Meryl Streep', '33021'),
            ('Michelle Pfeiffer', '33022'),
            ('Nicolas Cage', '33024'),
            ('Nicole Kidman', '33025'),
            ('Paul Newman', '33026'),
            ('Reese Witherspoon', '33027'),
            ('Robert De Niro', '33028'),
            ('Samuel L Jackson', '33029'),
            ('Scarlett Johansson', '33031'),
            ('Sean Connery', '33030'),
            ('Sharon Stone', '33032'),
            ('Sigourney Weaver', '33033'),
            ('Steven Seagal', '33035'),
            ('Tom Hanks', '33036'),
            ('Vin Diesel', '33037'),
            ('Wesley Snipes', '33038'),
            ('Will Smith', '33039'),
            ('Winona Ryder', '33040')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.tmdbUserLists_link % i[1], 'image': 'tmdb.png', 'action': 'movies2'})
        self.addDirectory(self.list)
        return self.list


    def tmdbUserLists_DCvsMarvel(self):
        theUserLists = [
            ('The Marvel Universe', '1'),
            ('The DC Comics Universe', '3'),
            ('Marvel Movies', '11332'),
            ('DC Movies', '12725'),
            ('Marvel Collection', '32793'),
            ('DC Comics Collection', '32799'),
            ('DC-Animated Movies', '62764'),
            ('Marvel Animated Movies', '62905'),
            ('Super Heroes', '13584'),
            ('Super Heroes Section', '36121'),
            ('Marvel: The Infinity Saga', '122518')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.tmdbUserLists_link % i[1], 'image': 'tmdb.png', 'action': 'movies2'})
        self.addDirectory(self.list)
        return self.list


    def tmdbUserLists_Holidays(self):
        theUserLists = [
            ('4th of July', '13577'),
            ('Christmas Collection', '32770'),
            ('Christmas Movies', '12944'),
            ('Christmas', '13378'),
            ('Easter', '13381'),
            ('Halloween Time', '13383'),
            ('New Years', '13379'),
            ('Thanksgiving', '13578'),
            ('Valentines Day', '13576'),
            ('Xmas Movies', '35870')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.tmdbUserLists_link % i[1], 'image': 'tmdb.png', 'action': 'movies2'})
        self.addDirectory(self.list)
        return self.list


    def tmdbUserLists_Assortment(self):
        theUserLists = [
            ('420', '13376'),
            ('1980s', '36945'),
            ('1990s', '37061'),
            ('Addiction', '35709'),
            ('Anime', '33416'),
            ('Animes', '35678'),
            ('Based on a True Story', '13479'),
            ('Best Picture Winners - The Academy Awards', '28'),
            ('Best Picture Winners', '11334'),
            ('Biographies', '35681'),
            ('Bonecrushers Favs', '35679'),
            ('Boxsets Movies', '11549'),
            ('Canada Loves', '35688'),
            ('Car Movie Collection', '32790'),
            ('ChickFlicks', '47441'),
            ('Classic Action', '36478'),
            ('Classic Westerns', '36468'),
            ('Cold War', '36444'),
            ('Comedy Movies', '37193'),
            ('Comedy', '47393'),
            ('Cons', '36664'),
            ('Conspiracies', '36116'),
            ('Conspiracy', '36692'),
            ('Court', '48216'),
            ('Crusher sr', '36084'),
            ('Disney Collection', '32800'),
            ('Disney Movies', '11338'),
            ('Disney', '12711'),
            ('Dreamworks', '13475'),
            ('Drug-Related', '36409'),
            ('Enforcer Favs', '35873'),
            ('FBI', '48131'),
            ('FG The Cars the Star Movies', '38852'),
            ('Fighting', '47453'),
            ('Gangster', '36407'),
            ('Griffs True Stories', '40740'),
            ('Hackers', '43444'),
            ('Heist', '47388'),
            ('Horror Icons 2', '35693'),
            ('Kats Favs', '35871'),
            ('Kids Collection', '13368'),
            ('Kids Movie Collection', '32802'),
            ('Kids Zone', '35682'),
            ('Killers', '35700'),
            ('Krests', '35992'),
            ('Learning and Nature', '35687'),
            ('Lego Movie Collection', '13585'),
            ('Leons Creations', '35702'),
            ('Lockdown', '35881'),
            ('Mafia Hits', '12710'),
            ('Man and Machine', '48235'),
            ('Mental Health', '36491'),
            ('Morbidlyhorrorfying', '35698'),
            ('Myths', '36402'),
            ('Other Mysteries', '36400'),
            ('Paranormal', '35706'),
            ('Politics', '36970'),
            ('Princesses', '13583'),
            ('Scifi', '35701'),
            ('SciFi', '47454'),
            ('Scottish', '44884'),
            ('Skateboarding', '46382'),
            ('Spies', '36553'),
            ('Spotlight', '13375'),
            ('Stalker Favs', '35869'),
            ('Stand Up', '37533'),
            ('Star Trek', '38386'),
            ('Teen', '35680'),
            ('Toddlers', '35684'),
            ('Urban', '36401'),
            ('War', '47457'),
            ('Warhammer Movies', '35876')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.tmdbUserLists_link % i[1], 'image': 'tmdb.png', 'action': 'movies2'})
        self.addDirectory(self.list)
        return self.list


    def tmdbUserLists_Collections(self):
        theUserLists = [
            ('3 Ninjas', '13130'),
            ('12 Rounds', '13120'),
            ('28 Days Later', '13126'),
            ('48 Hrs', '33259'),
            ('101 Dalmations', '33182'),
            ('300', '13132'),
            ('A Goofy Movie', '16489'),
            ('A Haunted House', '13137'),
            ('Ace Ventura', '33260'),
            ('Agent Cody Banks', '16496'),
            ('Airplane', '33261'),
            ('Airport', '33262'),
            ('Aladdin', '33184'),
            ('Alice in Wonderland', '13158'),
            ('Alien', '13161'),
            ('All Dogs', '16473'),
            ('Alvin and the Chipmunks', '33185'),
            ('American Graffiti', '33263'),
            ('American Ninja', '13168'),
            ('American Pie', '13176'),
            ('Anaconda', '33264'),
            ('Analyze This', '33265'),
            ('Anchorman', '33266'),
            ('Atlantis', '33186'),
            ('Austin Powers', '33267'),
            ('AVP', '13199'),
            ('Babe', '33187'),
            ('Back to the Future', '33268'),
            ('Bad Ass', '13205'),
            ('Bad Boys', '33269'),
            ('Bad Santa', '33270'),
            ('Balto', '33188'),
            ('Bambi', '33189'),
            ('Barbershop', '13220'),
            ('Basic Instinct', '33271'),
            ('Batman', '33129'),
            ('Bean', '13225'),
            ('Beauty and the Beast', '33190'),
            ('Beethoven', '33191'),
            ('Best of the Best', '13269'),
            ('Beverly Hills Cop', '33272'),
            ('Big Mommas House', '33273'),
            ('Bloodsport', '13281'),
            ('Boondock Saints', '13287'),
            ('Bourne', '33275'),
            ('Bridget Jones', '13289'),
            ('Brother Bear', '33192'),
            ('Bruce Almighty', '33276'),
            ('Caddyshack', '33277'),
            ('Captain America', '33130'),
            ('Cars', '33193'),
            ('Casper', '16469'),
            ('Cats and Dogs', '16501'),
            ('Charlottes Web', '96168'),
            ('Cheaper by the Dozen', '33278'),
            ('Cheech and Chong', '33420'),
            ('Childs Play', '33279'),
            ('Cinderella', '33194'),
            ('City Slickers', '33280'),
            ('Clerks', '13255'),
            ('Cloudy with a Chance of Meatballs', '33195'),
            ('Cocoon', '13260'),
            ('Conan', '33281'),
            ('Crank', '33282'),
            ('Crocodile Dundee', '33419'),
            ('Crouching Tiger', '13291'),
            ('Cube', '13304'),
            ('Curious George', '16497'),
            ('Da Vinci Code', '33283'),
            ('Daddy Day Care', '33284'),
            ('Dark Knight', '33132'),
            ('Death Wish', '33285'),
            ('Delta Force', '33286'),
            ('Despicable Me', '33197'),
            ('Diary of a Wimpy Kid', '13300'),
            ('Die Hard', '33287'),
            ('Dirty Dancing', '33288'),
            ('Dirty Harry', '33289'),
            ('Divergent', '13311'),
            ('Dolphin Tale', '13312'),
            ('Dr. Dolittle', '16505'),
            ('Dragon Tattoo', '13313'),
            ('Dumb and Dumber', '33290'),
            ('Escape From New York', '33291'),
            ('Every Which Way But Loose', '33292'),
            ('Evil Dead', '13308'),
            ('Exorcist', '33293'),
            ('Fantasia', '16521'),
            ('Fantastic Four', '33133'),
            ('Fast and Furious', '13062'),
            ('Father of the Bride', '33295'),
            ('Ferngully', '16522'),
            ('Final Destination', '13306'),
            ('Finding Nemo', '33198'),
            ('Fletch', '33296'),
            ('Flinstones', '16474'),
            ('Fox and the Hound', '33199'),
            ('Free Willy', '33200'),
            ('Friday the 13th', '33298'),
            ('Friday', '33297'),
            ('Fugitive', '33299'),
            ('G.I. Joe', '33300'),
            ('Garfield', '16520'),
            ('Get Shorty', '33301'),
            ('Gettysburg', '33302'),
            ('Ghost Rider', '33303'),
            ('Ghostbusters', '33201'),
            ('Godfather', '33305'),
            ('Gods Not Dead', '33304'),
            ('Godzilla', '33306'),
            ('Green Street Holigans', '13282'),
            ('Gremlins', '33202'),
            ('Grown Ups', '33307'),
            ('Grumpy Old Men', '33308'),
            ('Guns of Navarone', '33309'),
            ('Halloween', '33310'),
            ('Hannibal Lector', '33312'),
            ('Happy Feet', '33204'),
            ('Harold and Kumar', '13264'),
            ('Harry Potter', '33205'),
            ('Hellraiser', '33313'),
            ('Herbie', '16524'),
            ('Highlander', '13256'),
            ('Hills Have Eyes', '13254'),
            ('Hollow Man', '13251'),
            ('Home Alone', '33206'),
            ('Homeward Bound', '33207'),
            ('Honey, I Shrunk', '33208'),
            ('Hoodwinked', '16523'),
            ('Horrible Bosses', '33314'),
            ('Hostel', '33315'),
            ('Hot Shots', '33316'),
            ('Hot Tub Time Machine', '13241'),
            ('Hotel Transylvania', '33209'),
            ('How to Train Your Dragon', '33210'),
            ('Hulk', '33134'),
            ('Human Centipede', '13238'),
            ('Hunchback of Notre Dame', '33211'),
            ('Ice Age', '33212'),
            ('Independence Day', '33317'),
            ('Indiana Jones', '33318'),
            ('Infernal Affairs', '13230'),
            ('Insidious', '33319'),
            ('Inspector Gadget', '16492'),
            ('IP Man', '13227'),
            ('Iron Eagle', '33320'),
            ('Iron Fists', '13226'),
            ('Iron Man', '33135'),
            ('Jack Reacher', '33321'),
            ('Jack Ryan', '33322'),
            ('Jackass', '33323'),
            ('James Bond', '33324'),
            ('Jaws', '33325'),
            ('Jeepers Creepers', '33326'),
            ('John Wick', '33327'),
            ('Johnny English', '13218'),
            ('Journey', '13216'),
            ('Judge Dredd', '13215'),
            ('Jumanji', '33328'),
            ('Jump Street', '13213'),
            ('Jurassic Park', '33217'),
            ('Justice League', '16491'),
            ('Kick-Ass', '33329'),
            ('Kickboxer', '13206'),
            ('Kill Bill', '33330'),
            ('King Kong', '33331'),
            ('Kung Fu Panda', '33218'),
            ('Lady and the Tramp', '33219'),
            ('Land Before Time', '16485'),
            ('Lara Croft', '33332'),
            ('Last Summer', '13198'),
            ('Legally Blonde', '33333'),
            ('Lego Star Wars', '16482'),
            ('Lethal Weapon', '33334'),
            ('Like Mike', '16486'),
            ('Lilo and Stitch', '33220'),
            ('Look Whos Talking', '33335'),
            ('Lord of The Rings', '13190'),
            ('Machete', '33336'),
            ('Mad Max', '13188'),
            ('Madagascar', '33221'),
            ('Magic Mike', '33337'),
            ('Major League', '33338'),
            ('Man From Snowy River', '33339'),
            ('Mask', '33340'),
            ('Maze Runner', '13182'),
            ('Meet the Parents', '33343'),
            ('Men in Black', '33344'),
            ('Miss Congeniality', '33346'),
            ('Missing in Action', '33347'),
            ('Mission: Impossible', '33348'),
            ('Monsters Inc', '33222'),
            ('Monty Python', '13173'),
            ('Mulan', '33223'),
            ('My Big Fat Greek Wedding', '13170'),
            ('National Lampoon', '33350'),
            ('National Lampoons Vacation', '33351'),
            ('National Treasure', '33352'),
            ('Neighbors', '33353'),
            ('Never Back Down', '13166'),
            ('New Groove', '33225'),
            ('Night at the Museum', '33354'),
            ('Nightmare on Elm Street', '33355'),
            ('Nims Island', '13162'),
            ('Ninja', '13160'),
            ('Now You See Me', '33356'),
            ('Nutty Professor', '33357'),
            ('Nymphomaniac', '13157'),
            ('Oceans Eleven', '33358'),
            ('Odd Couple', '33359'),
            ('Oh, God!', '33360'),
            ('Olympus Has Fallen', '33361'),
            ('Once Were Warriors', '13152'),
            ('Ong Bak', '13151'),
            ('Open Season', '33226'),
            ('Paranormal Activities', '13149'),
            ('Paul Blart: Mall Cop', '33363'),
            ('Percy Jackson', '13147'),
            ('Peter Pan', '16498'),
            ('Pink Panther', '13320'),
            ('Pirates of the Caribbean', '33364'),
            ('Pitch', '13144'),
            ('Planes', '33227'),
            ('Planet of the Apes', '33365'),
            ('Pocahontas', '33228'),
            ('Police Academy', '33366'),
            ('Poltergeist', '33367'),
            ('Porkys', '33368'),
            ('Power Rangers', '16493'),
            ('Predator', '33369'),
            ('Problem Child', '33229'),
            ('Psycho', '13133'),
            ('Punisher', '13131'),
            ('Quarantine', '13128'),
            ('Raid', '13127'),
            ('Rambo', '33371'),
            ('Red Cliff', '13123'),
            ('RED', '33372'),
            ('Resident Evil', '13122'),
            ('Revenge of the Nerds', '33373'),
            ('Riddick', '33374'),
            ('Ride Along', '33375'),
            ('Rio', '33230'),
            ('Rise of The Footsoldier', '13116'),
            ('Robocop', '33376'),
            ('Rocky', '33377'),
            ('Romancing the Stone', '33378'),
            ('Rush Hour', '33379'),
            ('Sammys Adventures', '33231'),
            ('Santa Clause', '33380'),
            ('Saw', '33381'),
            ('Scary Movie', '13108'),
            ('Scooby-Doo', '33232'),
            ('Scream', '13107'),
            ('Sex and the City', '33382'),
            ('Shaft', '33383'),
            ('Shanghai Noon', '33384'),
            ('Sherlock Holmes', '13105'),
            ('Short Circuit', '33233'),
            ('Shrek', '33234'),
            ('Sin City', '33385'),
            ('Sinister', '33386'),
            ('Sister Act', '33387'),
            ('Smokey and the Bandit', '33388'),
            ('Space Chimps', '16495'),
            ('Speed', '33389'),
            ('Spiderman', '33126'),
            ('SpongeBob SquarePants', '33235'),
            ('Spy Kids', '33236'),
            ('Stakeout', '33390'),
            ('Star Trek', '33391'),
            ('Star Wars', '33237'),
            ('Starship Troopers', '13097'),
            ('Step Up', '13096'),
            ('Stuart Little', '33238'),
            ('Superman', '33136'),
            ('Taken', '33393'),
            ('Tarzan', '33239'),
            ('Taxi', '33394'),
            ('Ted', '33395'),
            ('Teen Wolf', '33396'),
            ('Teenage Mutant Ninja Turtles', '33240'),
            ('Terminator', '33397'),
            ('Terms of Endearment', '33398'),
            ('Texas Chainsaw Massacre', '33399'),
            ('The Addams Family', '13148'),
            ('The Avengers', '13196'),
            ('The Before', '13267'),
            ('The Best Exotic Marigold Hotel', '13268'),
            ('The Blues Brothers', '13284'),
            ('The Butterfly Effect', '13297'),
            ('The Chronicals of Narnia', '13283'),
            ('The Conjuring', '13266'),
            ('The Crow', '13294'),
            ('The Expendables', '33294'),
            ('The Fly', '13303'),
            ('The Grudge', '13277'),
            ('The Hangover', '13271'),
            ('The Hobbit', '13252'),
            ('The Hunger Games', '13236'),
            ('The Huntsman', '13235'),
            ('The Inbetweeners', '13233'),
            ('The Jungle Book', '13212'),
            ('The Karate Kid', '33241'),
            ('The Lion King', '33242'),
            ('The Little Mermaid', '33243'),
            ('The Man With No Name', '13184'),
            ('The Matrix', '13183'),
            ('The Mechanic', '33342'),
            ('The Mighty Ducks', '13177'),
            ('The Mummy', '13171'),
            ('The Muppets', '16494'),
            ('The Naked Gun', '13169'),
            ('The Neverending Story', '33248'),
            ('The Omen', '13153'),
            ('The Protector', '13134'),
            ('The Purge', '33370'),
            ('The Reef', '16490'),
            ('The Ring', '33418'),
            ('The Sandlot', '16502'),
            ('The Smurfs', '33249'),
            ('The Sting', '33392'),
            ('The Thing', '33400'),
            ('The Woman In Black', '13070'),
            ('Think Like A Man', '13088'),
            ('Thomas and Friends', '16503'),
            ('Thomas Crown Affair', '33401'),
            ('Three Colors', '13087'),
            ('Tinkerbell', '33252'),
            ('Titans', '13085'),
            ('Tom and Jerry', '33253'),
            ('Tooth Fairy', '33251'),
            ('Toy Story', '33254'),
            ('Transformers', '13083'),
            ('Transporter', '33402'),
            ('Tremors', '13081'),
            ('Tron', '13080'),
            ('Twilight', '13079'),
            ('Under Siege', '33403'),
            ('Underworld', '13077'),
            ('Undisputed', '13076'),
            ('Universal Soldier', '33404'),
            ('VeggieTales', '33255'),
            ('VHS', '13074'),
            ('Wall Street', '33405'),
            ('Wallace and Grommit', '16504'),
            ('Waynes World', '33406'),
            ('Weekend at Bernies', '33407'),
            ('Whole Nine Yards', '33408'),
            ('Winnie the Pooh', '33257'),
            ('Wizard of Oz', '33258'),
            ('Wrong Turn', '13069'),
            ('X-Files', '33409'),
            ('X-Men', '33137'),
            ('xXx', '33410'),
            ('Young Guns', '33411'),
            ('Zoolander', '33412'),
            ('Zorro', '33413')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.tmdbUserLists_link % i[1], 'image': 'tmdb.png', 'action': 'movies2'})
        self.addDirectory(self.list)
        return self.list


    def tmdbUserLists_CollectionsDupes(self):
        theUserLists = [
            ('101 Dalmatians', '13113'),
            ('Ace Ventura', '13145'),
            ('Addams Family', '33183'),
            ('Aladdin', '13155'),
            ('Anchorman', '13180'),
            ('Austin Powers', '13193'),
            ('Avengers', '33128'),
            ('Babe', '13201'),
            ('Bad Boys', '13208'),
            ('Balto', '13214'),
            ('Bambi', '13217'),
            ('Batman', '13223'),
            ('Beauty and the Beast', '13229'),
            ('Beethoven', '13263'),
            ('Beverly Hills Cop', '13272'),
            ('Big Mommas House', '13274'),
            ('Blues Brothers', '33274'),
            ('Bourne', '13288'),
            ('Brother Bear', '13292'),
            ('Captain America', '13224'),
            ('Cars', '13244'),
            ('Childs Play', '13246'),
            ('Cinderella', '13249'),
            ('City Slickers', '13253'),
            ('Cloudy with a Chance of Meatballs', '13259'),
            ('Conan', '13262'),
            ('Crank', '13273'),
            ('Crocodile Dundee', '13278'),
            ('Daddy Daycare', '16487'),
            ('Despicable Me', '13299'),
            ('Die Hard', '13302'),
            ('Dirty Dancing', '13305'),
            ('Dirty Harry', '13307'),
            ('Dumb and Dumber', '13314'),
            ('Finding Nemo', '16499'),
            ('Fox and the Hound', '13301'),
            ('Free Willy', '13298'),
            ('Friday the 13th', '13296'),
            ('Friday', '13315'),
            ('G.I. Joe', '13293'),
            ('Godfather', '13285'),
            ('Gremlins', '13280'),
            ('Grown Ups', '13279'),
            ('Grumpy Old Men', '13275'),
            ('Halloween', '13316'),
            ('Hangover', '33311'),
            ('Hannibal Lector', '13270'),
            ('Happy Feet', '13265'),
            ('Harry Potter', '13261'),
            ('Hellraiser', '13257'),
            ('Home Alone', '13250'),
            ('Homeward', '13248'),
            ('Honey I Shrunk', '13247'),
            ('Horrible Bosses', '13245'),
            ('Hot Shots', '13242'),
            ('Hotel Transylvania', '13240'),
            ('How to Train Your Dragon', '13239'),
            ('Hunchback of Notre Dame', '13237'),
            ('Ice Age', '13234'),
            ('Independence Day', '13232'),
            ('Indiana Jones', '13231'),
            ('Insidious', '13228'),
            ('Jackass', '13222'),
            ('James Bond', '13221'),
            ('Jaws', '13219'),
            ('Jungle Book', '33216'),
            ('Jurassic Park', '13211'),
            ('Karate Kid', '13209'),
            ('Kick Ass', '13207'),
            ('Kill Bill', '13203'),
            ('Kung Fu Panda', '13202'),
            ('Lady and the Tramp', '13200'),
            ('Legally Blonde', '13197'),
            ('Lethal Weapon', '13195'),
            ('Lilo and Stitch', '16500'),
            ('Look Whos Talking', '13191'),
            ('Machete', '13189'),
            ('Madagascar', '13187'),
            ('Major League', '13185'),
            ('Matrix', '33341'),
            ('Meet the Parents', '13179'),
            ('Men in Black', '13178'),
            ('Mighty Ducks', '33345'),
            ('Mission Impossible', '13175'),
            ('Monsters Inc', '13174'),
            ('Mulan', '13172'),
            ('Naked Gun', '33349'),
            ('Narnia', '33224'),
            ('National Treasure', '13167'),
            ('Neighbors', '13210'),
            ('New Groove', '13164'),
            ('Night at the Museum', '16483'),
            ('Nightmare on Elm Street', '13163'),
            ('Now You See Me', '13159'),
            ('Oceans', '13156'),
            ('Olympus Has Fallen', '13154'),
            ('Omen', '33362'),
            ('Open Season', '13150'),
            ('Pirates of the Caribbean', '13146'),
            ('Planes', '13142'),
            ('Planet of the Apes', '13141'),
            ('Pocahontas', '13140'),
            ('Police Academy', '13139'),
            ('Poltergeist', '13138'),
            ('Predator', '13136'),
            ('Problem Child', '13135'),
            ('R.E.D.', '13124'),
            ('Rambo', '13125'),
            ('Riddick', '13121'),
            ('Ride Along', '13119'),
            ('Rio', '13117'),
            ('Robocop', '13115'),
            ('Rocky', '13114'),
            ('Romancing the Stone', '13112'),
            ('Rush Hour', '13111'),
            ('Sammys Adventure', '13110'),
            ('Saw', '13109'),
            ('Shanghai', '13106'),
            ('Short Circuit', '13104'),
            ('Shrek', '16470'),
            ('Sin City', '13103'),
            ('Sister Act', '13102'),
            ('Smokey and the Bandit', '13101'),
            ('Spongebob', '16508'),
            ('Spy Kids', '13099'),
            ('Star Trek', '13098'),
            ('Star Wars', '12741'),
            ('Stuart Little', '16488'),
            ('Taken', '13095'),
            ('Tarzan', '13094'),
            ('Ted', '13093'),
            ('Teen Wolf', '13091'),
            ('Teenage Mutant Ninja Turtles', '13092'),
            ('Terminator', '13090'),
            ('Texas Chainsaw', '13089'),
            ('The Lion King', '13194'),
            ('The Little Mermaid', '13192'),
            ('The Mechanic', '13181'),
            ('The Neverending Story', '13165'),
            ('The Purge', '13129'),
            ('The Ring', '13118'),
            ('The Smurfs', '13100'),
            ('The Tooth Fairy', '13084'),
            ('The Whole Nine Yards', '13071'),
            ('Tinker Bell', '13086'),
            ('Toy Story', '13060'),
            ('Transporter', '13082'),
            ('Under Siege', '13078'),
            ('Universal Soldier', '13075'),
            ('Waynes World', '13073'),
            ('Weekend At Bernies', '13072'),
            ('XXX', '13068'),
            ('Young Guns', '13067'),
            ('Zoolander', '13066'),
            ('Zorro', '13065')
        ]
        for i in theUserLists:
            self.list.append({'name': i[0], 'url': self.tmdbUserLists_link % i[1], 'image': 'tmdb.png', 'action': 'movies2'})
        self.addDirectory(self.list)
        return self.list


    def tmdb_list(self, url):
        next = url
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))
        except:
            pass
        try:
            result = client.request(url)
            result = json.loads(result)
            items = result['results']
        except:
            return
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            url2 = '%s&page=%s' % (url.split('&page=', 1)[0], str(page+1))
            result = client.request(url2)
            result = json.loads(result)
            items += result['results']
        except:
            pass
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total:
                raise Exception()
            if not 'page=' in url:
                raise Exception()
            next = '%s&page=%s' % (next.split('&page=', 1)[0], str(page+1))
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                title = item['title']
                #title = str(title)
                #title = re.sub(r'\ -',r'', title)
                #title =re.sub('+', ' ', title)
                #title =re.sub(':','', title)
                #title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                tmdb = item['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                poster = item['poster_path']
                if poster == '' or poster == None:
                    poster = '0'
                else:
                    poster = self.tmdb_poster + poster
                poster = poster.encode('utf-8')
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None:
                    fanart = '0'
                if not fanart == '0':
                    fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                premiered = item['release_date']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')
                rating = str(item['vote_average'])
                if rating == '' or rating == None:
                    rating = '0'
                rating = rating.encode('utf-8')
                votes = str(item['vote_count'])
                try:
                    votes = str(format(int(votes),',d'))
                except:
                    pass
                if votes == '' or votes == None:
                    votes = '0'
                votes = votes.encode('utf-8')
                plot = item['overview']
                if plot == '' or plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try:
                    tagline = tagline.encode('utf-8')
                except:
                    pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'code': '0', 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


    def trakt_list(self, url):
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            result = trakt.getTraktAsJson(u)
            items = []
            for i in result:
                try:
                    items.append(i['movie'])
                except:
                    pass
            if len(items) == 0:
                items = result
        except:
            return
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            p = str(int(q['page']) + 1)
            if p == '5':
                raise Exception()
            q.update({'page': p})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                tmdb = item['ids']['tmdb']
                if tmdb == None or tmdb == '':
                    tmdb = '0'
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    raise Exception()
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = imdb.encode('utf-8')
                poster = '0'
                try:
                    poster = item['images']['poster']['medium']
                except:
                    pass
                if poster == None or not '/posters/' in poster:
                    poster = '0'
                poster = poster.rsplit('?', 1)[0]
                poster = poster.encode('utf-8')
                banner = poster
                try:
                    banner = item['images']['banner']['full']
                except:
                    pass
                if banner == None or not '/banners/' in banner:
                    banner = '0'
                banner = banner.rsplit('?', 1)[0]
                banner = banner.encode('utf-8')
                fanart = '0'
                try:
                    fanart = item['images']['fanart']['full']
                except:
                    pass
                if fanart == None or not '/fanarts/' in fanart:
                    fanart = '0'
                fanart = fanart.rsplit('?', 1)[0]
                fanart = fanart.encode('utf-8')
                premiered = item['released']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')
                genre = item['genres']
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')
                try:
                    duration = str(item['runtime'])
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'
                duration = duration.encode('utf-8')
                try:
                    rating = str(item['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'
                rating = rating.encode('utf-8')
                try:
                    votes = str(item['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes),',d'))
                except:
                    pass
                if votes == None:
                    votes = '0'
                votes = votes.encode('utf-8')
                mpaa = item['certification']
                if mpaa == None:
                    mpaa = '0'
                mpaa = mpaa.encode('utf-8')
                plot = item['overview']
                if plot == None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                try:
                    tagline = item['tagline']
                except:
                    tagline = None
                if tagline == None and not plot == '0':
                    tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                elif tagline == None:
                    tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                try:
                    tagline = tagline.encode('utf-8')
                except:
                    pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'banner': banner, 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


    def imdb_list(self, url):
        try:
            if url == self.imdbwatchlist_link:
                def imdb_watchlist_id(url):
                    return re.findall('/export[?]list_id=(ls\d*)', client.request(url))[0]
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url
            result = client.request(url)
            result = result.replace('\n','')
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'tr', attrs = {'class': '.+?'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
        except:
            return
        try:
            next = client.parseDOM(result, 'span', attrs = {'class': 'pagination'})
            next += client.parseDOM(result, 'div', attrs = {'class': 'pagination'})
            name = client.parseDOM(next[-1], 'a')[-1]
            if 'laquo' in name:
                raise Exception()
            next = client.parseDOM(next, 'a', ret='href')[-1]
            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                try:
                    title = client.parseDOM(item, 'a')[1]
                except:
                    pass
                try:
                    title = client.parseDOM(item, 'a', attrs = {'onclick': '.+?'})[-1]
                except:
                    pass
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = client.parseDOM(item, 'span', attrs = {'class': 'year_type'})[0]
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()
                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = 'tt' + re.sub('[^0-9]', '', imdb.rsplit('tt', 1)[-1])
                imdb = imdb.encode('utf-8')
                poster = '0'
                try:
                    poster = client.parseDOM(item, 'img', ret='src')[0]
                except:
                    pass
                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    pass
                if not ('_SX' in poster or '_SY' in poster):
                    poster = '0'
                poster = re.sub('_SX\d*|_SY\d*|_CR\d+?,\d+?,\d+?,\d*','_SX500', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
                genre = client.parseDOM(item, 'span', attrs = {'class': 'genre'})
                genre = client.parseDOM(genre, 'a')
                genre = ' / '.join(genre)
                if genre == '':
                    genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                try:
                    duration = re.compile('(\d+?) mins').findall(item)[-1]
                except:
                    duration = '0'
                duration = client.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')
                try:
                    rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
                except:
                    rating = '0'
                try:
                    rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
                except:
                    rating = '0'
                if rating == '' or rating == '-':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')
                try:
                    votes = client.parseDOM(item, 'div', ret='title', attrs = {'class': 'rating rating-list'})[0]
                except:
                    votes = '0'
                try:
                    votes = re.compile('[(](.+?) votes[)]').findall(votes)[0]
                except:
                    votes = '0'
                if votes == '':
                    votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')
                try:
                    mpaa = client.parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
                except:
                    mpaa = '0'
                try:
                    mpaa = client.parseDOM(mpaa, 'span', ret='title')[0]
                except:
                    mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED':
                    mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')
                director = client.parseDOM(item, 'span', attrs = {'class': 'credit'})
                director += client.parseDOM(item, 'div', attrs = {'class': 'secondary'})
                try:
                    director = [i for i in director if 'Director:' in i or 'Dir:' in i][0]
                except:
                    director = '0'
                director = director.split('With:', 1)[0].strip()
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '':
                    director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')
                cast = client.parseDOM(item, 'span', attrs = {'class': 'credit'})
                cast += client.parseDOM(item, 'div', attrs = {'class': 'secondary'})
                try:
                    cast = [i for i in cast if 'With:' in i or 'Stars:' in i][0]
                except:
                    cast = '0'
                cast = cast.split('With:', 1)[-1].strip()
                cast = client.replaceHTMLCodes(cast)
                cast = cast.encode('utf-8')
                cast = client.parseDOM(cast, 'a')
                if cast == []:
                    cast = '0'
                plot = '0'
                try:
                    plot = client.parseDOM(item, 'span', attrs = {'class': 'outline'})[0]
                except:
                    pass
                try:
                    plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                except:
                    pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                if plot == '':
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try:
                    tagline = tagline.encode('utf-8')
                except:
                    pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': '0', 'studio': '0', 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': '0', 'cast': cast, 'plot': plot, 'tagline': tagline, 'code': imdb, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': '0', 'next': next})
            except:
                pass
        return self.list


    def worker(self):
        self.meta = []
        total = len(self.list)
        for i in range(0, total):
            self.list[i].update({'metacache': False})
        self.list = metacache.fetch(self.list, self.tmdb_lang)
        for r in range(0, total, 100):
            threads = []
            for i in range(r, r+100):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
        self.list = [i for i in self.list]
        if len(self.meta) > 0:
            metacache.insert(self.meta)


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True:
                raise Exception()
            try:
                tmdb = self.list[i]['tmdb']
            except:
                tmdb = '0'
            if not tmdb == '0':
                url = self.tmdb_info_link % tmdb
            else:
                raise Exception()
            item = client.request(url, timeout='10')
            item = json.loads(item)
            title = item['title']
            if not title == '0':
                self.list[i].update({'title': title})
            year = item['release_date']
            try:
                year = re.compile('(\d{4})').findall(year)[0]
            except:
                year = '0'
            if year == '' or year == None:
                year = '0'
            year = year.encode('utf-8')
            if not year == '0':
                self.list[i].update({'year': year})
            tmdb = item['id']
            if tmdb == '' or tmdb == None:
                tmdb = '0'
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            if not tmdb == '0':
                self.list[i].update({'tmdb': tmdb})
            imdb = item['imdb_id']
            if imdb == '' or imdb == None:
                imdb = '0'
            imdb = imdb.encode('utf-8')
            if not imdb == '0' and "tt" in imdb:
                self.list[i].update({'imdb': imdb, 'code': imdb})
            poster = item['poster_path']
            if poster == '' or poster == None:
                poster = '0'
            if not poster == '0':
                poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            if not poster == '0':
                self.list[i].update({'poster': poster})
            fanart = item['backdrop_path']
            if fanart == '' or fanart == None:
                fanart = '0'
            if not fanart == '0':
                fanart = '%s%s' % (self.tmdb_image, fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.list[i]['fanart'] == '0':
                self.list[i].update({'fanart': fanart})
            premiered = item['release_date']
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except:
                premiered = '0'
            if premiered == '' or premiered == None:
                premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0':
                self.list[i].update({'premiered': premiered})
            studio = item['production_companies']
            try:
                studio = [x['name'] for x in studio][0]
            except:
                studio = '0'
            if studio == '' or studio == None:
                studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0':
                self.list[i].update({'studio': studio})
            genre = item['genres']
            try:
                genre = [x['name'] for x in genre]
            except:
                genre = '0'
            if genre == '' or genre == None or genre == []:
                genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0':
                self.list[i].update({'genre': genre})
            try:
                duration = str(item['runtime'])
            except:
                duration = '0'
            if duration == '' or duration == None:
                duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0':
                self.list[i].update({'duration': duration})
            rating = str(item['vote_average'])
            if rating == '' or rating == None:
                rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0':
                self.list[i].update({'rating': rating})
            votes = str(item['vote_count'])
            try:
                votes = str(format(int(votes),',d'))
            except:
                pass
            if votes == '' or votes == None:
                votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0':
                self.list[i].update({'votes': votes})
            mpaa = item['releases']['countries']
            try:
                mpaa = [x for x in mpaa if not x['certification'] == '']
            except:
                mpaa = '0'
            try:
                mpaa = ([x for x in mpaa if x['iso_3166_1'].encode('utf-8') == 'US'] + [x for x in mpaa if not x['iso_3166_1'].encode('utf-8') == 'US'])[0]['certification']
            except:
                mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0':
                self.list[i].update({'mpaa': mpaa})
            director = item['credits']['crew']
            try:
                director = [x['name'] for x in director if x['job'].encode('utf-8') == 'Director']
            except:
                director = '0'
            if director == '' or director == None or director == []:
                director = '0'
            director = ' / '.join(director)
            director = director.encode('utf-8')
            if not director == '0':
                self.list[i].update({'director': director})
            writer = item['credits']['crew']
            try:
                writer = [x['name'] for x in writer if x['job'].encode('utf-8') in ['Writer', 'Screenplay']]
            except:
                writer = '0'
            try:
                writer = [x for n,x in enumerate(writer) if x not in writer[:n]]
            except:
                writer = '0'
            if writer == '' or writer == None or writer == []:
                writer = '0'
            writer = ' / '.join(writer)
            writer = writer.encode('utf-8')
            if not writer == '0':
                self.list[i].update({'writer': writer})
            cast = item['credits']['cast']
            try:
                cast = [(x['name'].encode('utf-8'), x['character'].encode('utf-8')) for x in cast]
            except:
                cast = []
            if len(cast) > 0:
                self.list[i].update({'cast': cast})
            plot = item['overview']
            if plot == '' or plot == None:
                plot = '0'
            plot = plot.encode('utf-8')
            if not plot == '0':
                self.list[i].update({'plot': plot})
            tagline = item['tagline']
            if (tagline == '' or tagline == None) and not plot == '0':
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            elif tagline == '' or tagline == None:
                tagline = '0'
            try:
                tagline = tagline.encode('utf-8')
            except:
                pass
            if not tagline == '0':
                self.list[i].update({'tagline': tagline})
            try:
                if not imdb == None or imdb == '0':
                    url = self.imdbinfo % imdb
                    item = client.request(url, timeout='10')
                    item = json.loads(item)
                    plot2 = item['Plot']
                    if plot2 == '' or plot2 == None:
                        plot = plot
                    plot = plot.encode('utf-8')
                    if not plot == '0':
                        self.list[i].update({'plot': plot})
                    rating2 = str(item['imdbRating'])
                    if rating2 == '' or rating2 == None:
                        rating = rating2
                    rating = rating.encode('utf-8')
                    if not rating == '0':
                        self.list[i].update({'rating': rating})
                    votes2 = str(item['imdbVotes'])
                    try:
                        votes2 = str(votes2)
                    except:
                        pass
                    if votes2 == '' or votes2 == None:
                        votes = votes2
                    votes = votes.encode('utf-8')
                    if not votes == '0':
                        self.list[i].update({'votes': votes2})
            except:
                pass
            self.meta.append({'tmdb': tmdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.tmdb_lang, 'item': {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}})
        except:
            pass


    def movieDirectory(self, items):
        if items == None or len(items) == 0:
            control.idle(); sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()
        try:
            isOld = False; control.item().getArt('type')
        except:
            isOld = True
        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'
        indicators = playcount.getMovieIndicators(refresh=True) if action == 'movies' else playcount.getMovieIndicators()
        playbackMenu = control.lang(32063).encode('utf-8') if control.setting('hosts.mode') == '2' else control.lang(32064).encode('utf-8')
        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')
        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')
        for i in items:
            try:
                label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                sysname = urllib.quote_plus('%s (%s)' % (title, year))
                systitle = urllib.quote_plus(title)
                meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})
                #meta.update({'trailer': 'plugin://script.extendedinfo/?info=playtrailer&&id=%s' % imdb})
                if not 'duration' in i:
                    meta.update({'duration': '120'})
                elif i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass
                poster = [i[x] for x in ['poster', 'poster2', 'poster3'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})
                sysmeta = urllib.quote_plus(json.dumps(meta))
                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)
                path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)
                cm = []
                cm.append(('Find similar', 'ActivateWindow(10025,%s?action=movies&url=https://api.trakt.tv/movies/%s/related,return)' % (sysaddon, imdb)))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' % (sysaddon, sysname, imdb)))
                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))
                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))
                cm.append((addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, sysname, systitle, year, imdb, tmdb)))
                item = control.item(label=label)
                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})
                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})
                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})
                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})
                if settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    item.setProperty('Fanart_Image', i['fanart2'])
                elif settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels = control.metadataClean(meta))
                #item.setInfo(type='Video', infoLabels=meta) # old code
                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass
        try:
            url = items[0]['next']
            if url == '':
                raise Exception()
            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))
            item = control.item(label=nextMenu)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None:
                item.setProperty('Fanart_Image', addonFanart)
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass
        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0:
            control.idle(); sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()
        queueMenu = control.lang(32065).encode('utf-8')
        playRandom = control.lang(32535).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')
        for i in items:
            try:
                name = i['name']
                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb
                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib.quote_plus(i['url'])
                except:
                    pass
                cm = []
                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=movie&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))
                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=moviesToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
                except:
                    pass
                item = control.item(label=name)
                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


