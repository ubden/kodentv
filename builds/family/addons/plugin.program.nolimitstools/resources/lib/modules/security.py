"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc,xbmcgui,os,shutil,base64,re
from resources.lib.modules import common as Common

def check():

	try:
		dp = xbmcgui.DialogProgress()
		dialog = xbmcgui.Dialog()
		ADDONTITLE="[COLOR aqua]No Limits[/COLOR] [COLOR white]Tools[/COLOR]"

		dp.create(ADDONTITLE, "[COLOR aqua]Running the No Limits Security check....[/COLOR]")
		dp.update(0)

		xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
		version=float(xbmc_version[:4])
		remove_from_db = 0

		if version >= 17.0 and version <= 17.9:		
			remove_from_db = 1
			Enabled = 0

			import sqlite3

			db_check = 50
			got_db = 0
			while got_db == 0:
				DB_File = xbmc.translatePath(os.path.join('special://home/userdata/', 'Database/Addons'+str(db_check)+'.db'))
				if os.path.exists(DB_File):
					got_db = 1
				else: db_check = db_check-1

		a = 0
		b = 0
		namelist      = []
		idlist        = []
		deslist       = []
		combinedlists = []

		link=Common.OPEN_URL(base64.b64decode(b'aHR0cDovL2VjaG9jb2Rlci5jb20vc2VjdXJpdHkvY2hlY2sueG1s'))
		link=link.replace('\n','').replace('\r','')
		match = re.compile('<item>(.+?)</item>').findall(link)
		number = len(match)
		number2 = number * 2
		for item in match:

			if b == 0: b = number
			a = a + 1

			name=re.compile('<name>(.+?)</name>').findall(item)[0]
			id=re.compile('<id>(.+?)</id>').findall(item)[0]
			description=re.compile('<description>(.+?)</description>').findall(item)[0]
			
			progress = 100 * a/int(number2)
			dp.update(progress, "","[COLOR dodgerblue]Adding data for " + str(name) + "[/COLOR]","[COLOR lime]" + str(b) + " entries left to scan.[/COLOR]")
			b = b - 1

			namelist.append(name)
			idlist.append(id)
			deslist.append(description)
			combinedlists = list(zip(namelist,idlist,deslist))

		the_list = sorted(combinedlists)
		i = 0
		j = 0
		b = 0
		k = 0
		addons_path = xbmc.translatePath('special://home/addons/')
		
		for get_name,get_id,get_desc in the_list:

			if b == 0: b = number

			a = a + 1
			progress = 100 * a/int(number2)
			dp.update(progress, "","[COLOR dodgerblue]Scanning for " + str(get_name) + "[/COLOR]","[COLOR lime]" + str(b) + " entries left to scan.[/COLOR]")
			b = b - 1

			for root, dirs, files in os.walk(addons_path):

				for d in dirs:
					k = k + 1
					if get_id in d:
						i = i + 1
						choice = dialog.yesno("[COLOR red][B]FOUND: " + get_name.upper() + '[/B][/COLOR]', '[COLOR white]We have found [COLOR red][B]' + get_name.upper() + '[/B][/COLOR] on your system. This addon has been flagged because: [COLOR red][B]' + get_desc.upper() + '[/B][/COLOR][/COLOR]', '[COLOR blue][B]Would you like to remove this from your system?[/B][/COLOR]',yeslabel='[B][COLOR lime]YES[/COLOR][/B]',nolabel='[B][COLOR red]NO[/COLOR][/B]')
						if choice == 1:
							try:
								shutil.rmtree(os.path.join(root, d))
								j = j + 1
								
								if remove_from_db == 1:
									try:
										DB_Path = DB_File 
										conn = sqlite3.connect(DB_Path)
										cursor = conn.cursor()
									 
										q = """ UPDATE installed SET enabled= ? WHERE addonID = ? """
										cursor.execute(q, (str(Enabled), str(get_id)))
										conn.commit()
									except: pass
							except: pass

		if remove_from_db == 1:
			xbmc.executebuiltin("UpdateLocalAddons")
			xbmc.executebuiltin("UpdateAddonRepos")

		dp.close()
		dialog.ok(ADDONTITLE, "[COLOR dodgerblue]We have finished scanning your system.[/COLOR]","[COLOR white]We found [B][COLOR yellowgreen]" + str(i) + " [/B][/COLOR]threats.[/COLOR][COLOR white] We removed [COLOR yellowgreen][B]" + str(j) + "[/B][/COLOR] threats.[/COLOR]","[COLOR white]Scanned folders [B][COLOR yellowgreen]" + str(k) + " [/B][/COLOR].[/COLOR][COLOR white] Checked for [COLOR yellowgreen][B]" + str(number) + "[/B][/COLOR] threats.[/COLOR]")
	except:
		dialog.ok(ADDONTITLE, "[COLOR yellowgreen]Sorry, there was an error running the security check at the moment. Please try again later.[/COLOR]")
		quit()