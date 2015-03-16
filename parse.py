#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.models import Channel, BroadCast

import datetime, json, os, xmltv

from operator import itemgetter
from optparse import OptionParser

def parse_args():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
        help="location of xml", metavar="FILE")

    parser.add_option("-d", "--destination", dest="destination",
        help="location of output files", metavar="FILE")

    return parser.parse_args()

def parse_channels():
    channels = {}
    for key in xmltv.read_channels(open(filename, 'r')):
        c = Channel(id = key['id'], icon = key['icon'][0]['src'], \
                name = map(itemgetter(0), key['display-name'])[0])
        channels[c.id] = c

    return channels

def retrieve_channel(id):
    return CHANNELS[id]

def parse_broadcasts():
    broadcasts = {}
    ctr = 0
    for element in xmltv.read_programmes(open(filename, 'r')):
        ctr += 1
        channel = retrieve_channel(element['channel'])
        start_time =  format_time(element['start'])
        end_time =  format_time(element['stop'])
        key = '%s:%s' % (channel.id,start_time.strftime("%Y%m%d%R"))

        b = BroadCast(id = key, channel = channel.id, \
            blurb = retrieve_blurb(element), \
            title = retrieve_title(element), \
            start_time = start_time.strftime("%Y-%m-%d %R"),
            end_time = end_time.strftime("%Y-%m-%d %R"))

        broadcasts[key] = b

    return broadcasts

def retrieve_title(element):
    titles = map(itemgetter(0), element['title'])
    return titles[0]

def retrieve_blurb(element):
    if 'desc' in element:
        desc = map(itemgetter(0), element['desc'])
        return desc[0]
    return ''

def format_time(timestamp):
    return datetime.datetime.strptime(timestamp[:12], "%Y%m%d%H%M")

def output_json():
    channels_output = [{'id': CHANNELS[id].id, 'name': CHANNELS[id].name, \
        'icon': CHANNELS[id].icon} for id in CHANNELS]

    with open(os.path.join(options.destination, 'channels.json'), 'w') as f:
        f.write(json.dumps(channels_output, sort_keys=True, indent=2))

    for key in sorted(BROADCASTS):
        print "%s %s %s" % (BROADCASTS[key].channel, BROADCASTS[key].title, BROADCASTS[key].start_time)

if __name__ == "__main__":
    (options, args) = parse_args()
    if os.path.exists(options.filename):
        filename = options.filename

    if not os.path.exists(options.destination):
        os.makedirs(options.destination)

    CHANNELS = parse_channels()
    BROADCASTS = parse_broadcasts()

    output_json()
