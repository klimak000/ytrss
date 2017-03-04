#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
#                                                                         #
#  Copyright (C) 2017  Rafal Kobel <rafalkobel@rafyco.pl>                 #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################

from ytrss.core.sys.debug import Debug
from sets import Set
import abc, os, json

class UrlRememberer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_data = ""
        self.database = Set()
        try:
            plik = open(self.file_name)
            try:
                self.file_data = plik.read()
            finally:
                plik.close()
            for elem in self.file_data.split('\n'):
                self.database.add(elem)
        except:
            pass
    def add_element(self, address):
        """ Dodaj dane do bazydanych. """
        self.database.add(address)
        if (self.file_name == ""):
            return
        plik = open(self.file_name, 'a')
        plik.writelines(address+'\n')
        plik.close()
        self.file_data = "%s\n%s\n" % (self.file_data, address)
    def is_new(self, address):
        """ Czy dane znajduja sie w pliku. """
        if address in self.database:
            print("isnieje %s" % address)
            return False
        else:
            print("nieisnieje %s" % address)
            return True
    def get_elements(self):
        return self.database

class Download_Queue:
    def __init__(self, settings):
        self.url_rss = settings.get_url_rss() 
        self.download_file = settings.get_download_file()
        self.rememberer = UrlRememberer(self.url_rss)
    def _queue_mp3(self, address):
        """ Dodaj do pliku z danymi do pobrania. """
        if Debug.get_instance().is_debug():
            return
        plik = open(self.download_file, 'a')
        plik.writelines(address+'\n')
        plik.close()
    def queue_mp3(self, address):
        Debug.get_instance().debug_log("DOWNLOAD: %s" % address)
        if self.rememberer.is_new(address):
            self._queue_mp3(address)
            if not(Debug.get_instance().is_debug()):
                self.rememberer.add_element(address)
