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

import os
import sys
import itertools as it
import math
from m3u8tool.io import EXTINF, EXT_X_BYTERANGE, EXT_X_TARGETDURATION, MEDIA, parse, format_line


def split(input_m3u8, output_m3u8_format, output_ts_format, split_duration, split_size, subcommand):
    m3u8_path = input_m3u8.name
    m3u8_dirname = os.path.dirname(m3u8_path)
    m3u8_basename = os.path.basename(m3u8_path)
    m3u8_filename = os.path.splitext(m3u8_basename)[0]

    if split_duration == 0.0:
        split_duration = sys.float_info.max

    if split_size == 0:
        split_size = sys.maxsize

    segments, header, footer = parse(input_m3u8)

    index = 1
    duration = 0.0
    size = 0
    total_duration = 0.0
    total_size = 0
    fragments = []

    def write(fragments, index):
        output_m3u8_path = output_m3u8_format.format(
            dirname=m3u8_dirname, basename=m3u8_basename, filename=m3u8_filename,
            index=index, offset_time=total_duration, offset_pos=total_size,
        )

        target_duration = int(math.floor(max(map(lambda e: e[EXTINF]['segment_duration'], fragments))))

        input_ts = None
        input_ts_path = None

        if output_ts_format is None:
            output_ts = None
        else:
            ts_path = fragments[0][MEDIA]['path']
            ts_dirname = os.path.dirname(ts_path)
            ts_basename = os.path.basename(ts_path)
            ts_filename = os.path.splitext(ts_basename)[0]

            output_ts_path = output_ts_format.format(
                dirname=ts_dirname, basename=ts_basename, filename=ts_filename,
                index=index, offset_time=total_duration, offset_pos=total_size,
            )

            output_ts = open(output_ts_path, mode='wb')
            print(output_ts_path + ' ', end='')

        def header_replace(e):
            nonlocal target_duration
            if e['kind'] == EXT_X_TARGETDURATION:
                e['target_duration'] = target_duration
            return e
        
        print(output_m3u8_path + ' ', end='')
        with open(output_m3u8_path, mode='w', encoding='UTF-8') as output_m3u8:
            for e in map(header_replace, header):
                print(format_line(e), file=output_m3u8)

            for f in fragments:
                if output_ts is not None:
                    ext_x_byterange = f[EXT_X_BYTERANGE]
                    input_ts_offset = ext_x_byterange['segment_offset']
                    segment_size = ext_x_byterange['segment_size']
                    ext_x_byterange['segment_offset'] = ext_x_byterange['output_segment_offset']
                    media = f[MEDIA]

                    if media['path'] != input_ts_path:
                        input_ts_path = media['path']
                        if input_ts is not None:
                            input_ts.close()
                        input_ts = open(input_ts_path, mode='rb')

                    media['path'] = output_ts_path

                    input_ts.seek(input_ts_offset)
                    output_ts.write(input_ts.read(segment_size))

                print(format_line(f), file=output_m3u8)

            for e in footer:
                print(format_line(e), file=output_m3u8)

        if output_ts is not None:
            output_ts.close()

        if input_ts is not None:
            input_ts.close()

        print(str(duration))

    for segment in segments:
        ext_x_byterange = segment[EXT_X_BYTERANGE]
        extinf = segment[EXTINF]

        ext_x_byterange['output_segment_offset'] = size
        fragments.append(segment)

        duration += extinf['segment_duration']
        size += ext_x_byterange['segment_size']

        if duration >= split_duration or size >= split_size:
            write(fragments, index)
            fragments = []
            index += 1
            duration = 0.0
            size = 0

    if len(fragments) > 0:
        write(fragments, index)
