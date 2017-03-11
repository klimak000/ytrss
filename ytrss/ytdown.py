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

from __future__ import unicode_literals
from ytrss import get_version
import logging
from ytrss.core.settings import SettingException
from ytrss.core import Download_Queue
from ytrss.core.settings import YTSettings
from argparse import ArgumentParser
import os
try:
    import argcomplete
except ImportError:
    pass

def __option_args(argv=None):
    parser = ArgumentParser(description="Save one or more urls from Youtube to file.",
                            prog='ytdown',
                            version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-c", "--conf", dest="configuration", 
                        help="configuration file", default="", metavar="FILE")
    parser.add_argument("-l", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help="Set the logging level")
    parser.add_argument("urls", nargs='*', default=[], type=unicode,
                        help="Url to download.")
    try:
        argcomplete.autocomplete(parser)
    except NameError:
        pass
    return parser.parse_args(argv)

def main(argv=None):
    options = __option_args(argv)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=options.logLevel)
    try:
        settings = YTSettings(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)
        
    if len(options.urls) < 1:
        print("Require url to download")
        exit(1)
        
    queue = Download_Queue(settings)
    for url in options.urls:
        if queue.queue_mp3(url):
            print("Filmik zostanie pobrany: {}".format(url))
        else:
            print("Filmik nie zostanie pobrany: {}".format(url))
            
if __name__ == "__main__":
    main()