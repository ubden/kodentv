"""
    TVAddons Log Uploader Script
    Copyright (C) 2016 tknorris

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
import urllib
import uploader
from uploader import UploaderError
from .. import log_utils

try:
    from urllib.request import urlopen, Request  # python 3.x
except ImportError:
    from urllib2 import urlopen, Request  # python 2.x

try:
    basestring
except NameError:
    basestring = str

try:
    import urlparse
except:
    from urllib import parse as urlparse

API_KEY = '66554d00fa20ba30f4f8a5da7c5bfb2f'
BASE_URL = 'http://pastebin.com'
EXPIRATION = '1W'

class PastebinUploader(uploader.Uploader):
    name = 'pastebin'

    def upload_log(self, log, name=None):
        url = '/api/api_post.php'
        data = {'api_dev_key': API_KEY, 'api_option': 'paste', 'api_paste_code': log, 'api_paste_name': 'Kodi Log',
                'api_paste_private': 1, 'api_paste_expire_date': EXPIRATION}
        url = urlparse.urljoin(BASE_URL, url)
        req = Request(url, data=urllib.urlencode(data))
        try:
            res = urlopen(req)
            html = res.read()
            if html.startswith('http'):
                return html
            elif html.upper().startswith('BAD API REQUEST'):
                raise UploaderError(html[len('Bad API request, '):])
            else:
                raise UploaderError(html)
        except Exception as e:
            raise UploaderError(e)
            
    def send_email(self, email, results):
        return None
