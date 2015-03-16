#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, json, os, xmltv

from operator import itemgetter
from optparse import OptionParser

class Channel():

    def __init__(self, id, name, icon):
        self.id = id
        self.name = name
        self.icon = icon

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

        c = Channel(id=id, name=name, icon=src)
        channels[c.id] = c

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
    channel = retrieve_channel(element['channel'])
    return {
        'channel': channel.id,
        'blurb': retrieve_blurb(element),
        'title': retrieve_title(element),
        'start_time': format_time(element['start']),
        'end_time': format_time(element['stop']),
    }

def retrieve_title(element):
    titles = map(itemgetter(0), element['title'])
    return titles[0]

def retrieve_blurb(element):
    if 'desc' in element:
        desc = map(itemgetter(0), element['desc'])
        return desc[0]
    return ''

def format_time(timestamp):
    return datetime.datetime.strptime(timestamp[:12], "%Y%m%d%H%M%S")

def output_json():
    channels_output = [{'id': CHANNELS[id].id, 'name': CHANNELS[id].name, \
        'icon': CHANNELS[id].icon} for id in CHANNELS]

    print json.dumps(channels_output)

if __name__ == "__main__":
    (options, args) = parse_args()
    if os.path.exists(options.filename):
        filename = options.filename

    CHANNELS = parse_channels()
    BROADCASTS = parse_broadcasts()

    output_json()
