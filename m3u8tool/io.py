# coding: utf-8
#
# Copyright 2019, Kurusugawa Computer Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import itertools as it

EXTINF = '#EXTINF'
EXT_X_BYTERANGE = '#EXT-X-BYTERANGE'
EXT_X_ENDLIST = '#EXT-X-ENDLIST'
EXT_X_TARGETDURATION = '#EXT-X-TARGETDURATION'
MEDIA = 'MEDIA'
SEGMENT = 'SEGMENT'
UNKNOWN = 'UNKNOWN'


def format_line(element):
    formatter = {
        EXTINF: lambda t: t['kind'] + ':' + '{0:.6f}'.format(t['segment_duration']) + ',' + t['title'],
        EXT_X_BYTERANGE: lambda t: t['kind'] + ':' + str(t['segment_size']) + '@' + str(t['segment_offset']),
        EXT_X_ENDLIST: lambda t: t['kind'],
        EXT_X_TARGETDURATION: lambda t: t['kind'] + ':' + str(t['target_duration']),
        MEDIA: lambda t: t['path'],
        UNKNOWN: lambda t: t['line'],
        SEGMENT: lambda t: '\n'.join(map(format_line, t['elements'])),
    }
    return formatter[element['kind']](element)


def parse_line(line):
    if line.startswith(EXTINF):
        tokens = line.replace(',', ':').split(':')
        return {'kind': EXTINF, 'segment_duration': float(tokens[1]), 'title': tokens[2]}
    elif line.startswith(EXT_X_BYTERANGE):
        tokens = line.replace('@', ':').split(':')
        return {'kind': EXT_X_BYTERANGE, 'segment_size': int(tokens[1]), 'segment_offset': int(tokens[2])}
    elif line.startswith(EXT_X_TARGETDURATION):
        tokens = line.split(':')
        return {'kind': EXT_X_TARGETDURATION, 'target_duration': int(tokens[1])}
    elif line.startswith(EXT_X_ENDLIST):
        return {'kind': EXT_X_ENDLIST}
    elif line.lower().endswith('.ts'):
        return {'kind': MEDIA, 'path': line}
    else:
        return {'kind': UNKNOWN, 'line': line}


def parse(input_m3u8):
    lines = input_m3u8.read().splitlines()
    elements = list(map(parse_line, lines))

    def header_filter(t): return not t['kind'] in [EXTINF, EXT_X_BYTERANGE, MEDIA]

    header = list(it.takewhile(header_filter, elements))

    segments = []

    def new_segment(): return {'kind': SEGMENT, 'm3u8_path': input_m3u8.name, 'elements': []}

    segment = new_segment()

    for element in it.dropwhile(header_filter, elements):
        segment['elements'].append(element)
        if element['kind'] == EXTINF:
            segment[EXTINF] = element
        elif element['kind'] == EXT_X_BYTERANGE:
            segment[EXT_X_BYTERANGE] = element
        elif element['kind'] == MEDIA:
            segment[MEDIA] = element
            segments.append(segment)
            segment = new_segment()

    footer = segment['elements']

    return (segments, header, footer)
