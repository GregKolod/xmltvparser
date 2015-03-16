#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, os, xmltv

from collections import namedtuple
from operator import itemgetter
from optparse import OptionParser

Channel = namedtuple('Channel', [
    'id', 'name', 'icon'
])

def parse_args():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
        help="location of xml", metavar="FILE")

    return parser.parse_args()

def parse_channels():
    channels = {}
    for key in xmltv.read_channels(open(filename, 'r')):
        name = map(itemgetter(0), key['display-name'])
        id   = key['id']
        src  = key['icon'][0]['src']
        name = name[0]

        rec = dict(zip(Channel._fields, [id, name, src]))
        channel = Channel(**rec)
        channels[channel.id] = channel

    return channels

def retrieve_channel(id):
    return CHANNELS[id]

def parse_broadcasts():
    for key in xmltv.read_programmes(open(filename, 'r')):
        channel = retrieve_channel(key['channel'])
        titles = map(itemgetter(0), key['title'])

        print "%s - %s - %s - %s" % (titles[0], channel.name, format_time(key['start']), format_time(key['stop']))

def format_time(timestamp):
    return datetime.datetime.strptime(timestamp[:12], "%Y%m%d%H%M%S")

if __name__ == "__main__":
    (options, args) = parse_args()
    if os.path.exists(options.filename):
        filename = options.filename

    CHANNELS = parse_channels()
    parse_broadcasts()

