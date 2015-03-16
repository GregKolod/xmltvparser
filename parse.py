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
    broadcasts = {}
    ctr = 0
    for element in xmltv.read_programmes(open(filename, 'r')):
        ctr += 1
        broadcasts[ctr] = retrieve_broadcast(element)

    return broadcasts

def retrieve_broadcast(element):
        #titles = map(itemgetter(0), element['title'])

        return {
            'channel': retrieve_channel(element['channel']),
            #'blurb': _retrieve_blurb(element),
            'title': retrieve_title(element),
            'start_time': format_time(element['start']),
            'end_time': format_time(element['stop']),
        }
        #print "%s - %s - %s - %s" % (titles[0], channel.name, format_time(key['start']), format_time(key['stop']))

def retrieve_title(element):
    titles = map(itemgetter(0), element['title'])
    return titles[0]

def format_time(timestamp):
    return datetime.datetime.strptime(timestamp[:12], "%Y%m%d%H%M%S")

if __name__ == "__main__":
    (options, args) = parse_args()
    if os.path.exists(options.filename):
        filename = options.filename

    CHANNELS = parse_channels()
    BROADCASTS = parse_broadcasts()
    print BROADCASTS
