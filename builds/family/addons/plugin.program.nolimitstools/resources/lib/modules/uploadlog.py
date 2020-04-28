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
import re
import os
import sys
import xbmcgui
from resources.lib.log import log_utils
from resources.lib.log import kodi
from resources.lib.log.kodi import i18n
from resources.lib.log.uploaders import *
from resources.lib.log.uploaders.uploader import UploaderError

REPLACES = [
    ('''://[^'"/]+:[^'"/]+@''', '''//USER:PASSWORD@'''),
    ('<(user|username)>.+?</\\1>', '<\\1>USER</\\1>'),
    ('<(pass|password)>.+?</\\1>', '<\\1>PASSWORD</\\1>'),
    ('''&(pass|password|pwd|pin)=[^'"&]+''', '&\\1=PASSWORD')
]

FILES = [
    ('kodi.log', 'kodi.log'),
    ('kodi.old.log', 'kodi.old.log'),
    ('spmc.log', 'spmc.log'),
    ('spmc.old.log', 'spmc.old.log'),
    ('freetelly.log', 'freetelly.log'),
    ('freetelly.old.log', 'freetelly.old.log')
]

EMAIL_SENT = {True: i18n('email_successful'), False: i18n('email_failed'), None: i18n('email_unsupported'), '': i18n('email_not_configured')}
SERVER_ORDER = {'tvaddons': 1, 'pastebin': 3, 'dropbox': 2, 'ubuntu': 4}

def __get_logs():
    logs = []
    log_path = kodi.translate_path('special://logpath')
    for file_name, name in FILES:
        full_path = os.path.join(log_path, file_name)
        if os.path.exists(full_path):
            logs.append((full_path, name))
    return logs

def upload_logs():
    logs = __get_logs()
    results = {}
    last_error = ''
    uploaders = uploader.Uploader.__class__.__subclasses__(uploader.Uploader)
    uploaders = [klass for klass in uploaders if
                 SERVER_ORDER.get(klass.name, 100) and kodi.get_setting('enable_%s' % (klass.name)) == 'true']
    uploaders.sort(key=lambda x: SERVER_ORDER.get(x.name, 100))
    if not uploaders: last_error = 'No Uploaders Enabled'
    for log in logs:
        full_path, name = log
        if '.old.' not in name or kodi.get_setting('include_old') == 'true':
            with open(full_path, 'r') as f:
                log = f.read()
                
            for pattern, replace in REPLACES:
                log = re.sub(pattern, replace, log)
            
            for klass in uploaders:
                try:
                    log_service = klass()
                    result = log_service.upload_log(log, name)
                    results[log_service.name] = results.get(log_service.name, {'service': log_service, 'results': {}})
                    results[log_service.name]['results'][name] = result
                    break
                except UploaderError as e:
                    log_utils.log('Uploader Error: (%s) %s: %s' % (log_service.__class__.__name__, name, e), log_utils.LOGWARNING)
                    last_error = str(e)
            else:
                log_utils.log('No successful upload for: %s Last Error: %s' % (name, last_error), log_utils.LOGWARNING)
            
    if results:
        email = kodi.get_setting('email')
        if email:
            for service in results:
                try:
                    success = results[service]['service'].send_email(email, results[service]['results'])
                    results[service]['email'] = success
                except UploaderError as e:
                    log_utils.log('Email Error: (%s): %s' % (service, e), log_utils.LOGWARNING)
                    results[service]['email'] = False

        args = [i18n('logs_uploaded')]
        for _, name in FILES:
            for service in results:
                if name in results[service]['results']:
                    line = '%s: %s [I](%s)[/I]' % (name, results[service]['results'][name], EMAIL_SENT[results[service].get('email', '')])
                    args.append(line)
                    log_utils.log('Log Uploaded: %s: %s' % (name, results[service]['results'][name]), log_utils.LOGNOTICE)
                    
        xbmcgui.Dialog().ok(*args)
    else:
        kodi.notify(i18n('logs_failed') % (last_error), duration=5000)

def __confirm_upload():
    return xbmcgui.Dialog().yesno(kodi.get_name(), i18n('upload_question'), '', i18n('warning'))
    
def main(argv=None):
    try:
        if kodi.get_setting('email_prompt') != 'true' and not kodi.get_setting('email'):
            kodi.set_setting('email_prompt', 'true')
            kodi.show_settings()
            
        if __confirm_upload():
            upload_logs()
    except Exception as e:
        log_utils.log('Uploader Error: %s' % (e), log_utils.LOGWARNING)
        kodi.notify(msg=str(e))
        raise

if __name__ == '__main__':
    sys.exit(main())
