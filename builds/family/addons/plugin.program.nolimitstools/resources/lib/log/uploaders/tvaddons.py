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
import urllib2
import urlparse
import urllib
import StringIO
import gzip
import json
import uploader
from uploader import UploaderError
from .. import log_utils

BASE_URL = 'https://logs.tvaddons.ag/'
EXPIRATION = 2592000
USE_GZIP = False

class TvaddonsUploader(uploader.Uploader):
    name = 'tvaddons'
    
    def upload_log(self, log, name=None):
        url = '/api/json/create'
        url = urlparse.urljoin(BASE_URL, url)
        headers = {'Content-Type': 'application/json'}
        data = {'data': log, 'language': 'kodilog', 'expire': EXPIRATION}
        data = json.dumps(data)
        if USE_GZIP:
            s = StringIO.StringIO()
            g = gzip.GzipFile(fileobj=s, mode='w')
            g.write(data)
            g.close()
            data = s.getvalue()
            headers['Content-Encoding'] = 'gzip'
        req = urllib2.Request(url, data=data, headers=headers)
        try:
            res = urllib2.urlopen(req)
            html = res.read()
            try:
                js_data = json.loads(html)
                if 'result' in js_data:
                    result = js_data['result']
                    if 'id' in result:
                        return urlparse.urljoin(BASE_URL, result['id'])
                    elif 'error' in result:
                        raise UploaderError('tvaddons error: %s' % (result['error']))
                    else:
                        raise UploaderError('Unexcepted Response: %s' % (result))
                else:
                        raise UploaderError('Unexcepted Response: %s' % (js_data))
            except ValueError as e:
                raise UploaderError('Unparseable Resonse from tvaddons: %s' % (html))
        except Exception as e:
            raise UploaderError(e)
            
    def send_email(self, email, results):
        url = '/mail_logs.php'
        data = {'email': email, 'results': results}
        headers = {'Content-Type': 'application/json'}
        url = urlparse.urljoin(BASE_URL, url)
        req = urllib2.Request(url, data=json.dumps(data), headers=headers)
        try:
            res = urllib2.urlopen(req)
            html = res.read()
            js_data = json.loads(html)
            if 'result' in js_data:
                if js_data['result'] == 'success':
                    return True
                else:
                    raise UploaderError(js_data.get('msg', 'Unknown Error'))
        except Exception as e:
            raise UploaderError(e)
        
        return False
