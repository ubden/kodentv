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
import abc

abstractstaticmethod = abc.abstractmethod
class abstractclassmethod(classmethod):

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)

class UploaderError(Exception):
    pass

class Uploader(object):
    __metaclass__ = abc.ABCMeta
    name = ''

    @abc.abstractmethod
    def upload_log(self, log, name=None):
        '''
        Return the url of the log, or raise a UploaderError on failure
        The name of the log is optional and may or may not be used by the uploader
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def send_email(self, email, results):
        '''
        Return True if email succeeds, False if it fails, or None if email isn't supported
        '''
        raise NotImplementedError
