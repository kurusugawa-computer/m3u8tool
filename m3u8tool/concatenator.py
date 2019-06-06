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

import math
import os
from m3u8tool.io import EXTINF, EXT_X_BYTERANGE, EXT_X_TARGETDURATION, MEDIA, parse, format_line

def cat(input_m3u8, output_m3u8, output_ts, subcommand):
    cat_segments = []
    cat_header = None
    cat_footer = None
    for segments, header, footer in map(parse, input_m3u8):
        cat_segments += segments
        cat_header = header
        cat_footer = footer

    target_duration = int(math.floor(max([e[EXTINF]['segment_duration'] for e in cat_segments])))

    def header_replace(e):
        nonlocal target_duration
        if e['kind'] == EXT_X_TARGETDURATION:
            e['target_duration'] = target_duration
        return e
    
    for e in map(header_replace, cat_header):
        print(format_line(e), file=output_m3u8)

    size = 0
    input_ts = None
    input_ts_path = None

    for f in cat_segments:
        m3u8_path = f['m3u8_path']
        m3u8_dirname = os.path.dirname(m3u8_path)

        if output_ts is not None:
            ext_x_byterange = f[EXT_X_BYTERANGE]
            input_ts_offset = ext_x_byterange['segment_offset']
            segment_size = ext_x_byterange['segment_size']
            ext_x_byterange['segment_offset'] = size
            size += segment_size
            media = f[MEDIA]

            if media['path'] != input_ts_path:
                input_ts_path = media['path']
                if input_ts is not None:
                    input_ts.close()

                if os.path.isabs(input_ts_path):
                    open_ts_path = input_ts_path
                else:
                    open_ts_path = os.path.join(m3u8_dirname, input_ts_path)

                input_ts = open(open_ts_path, mode='rb')

            media['path'] = output_ts.name

            input_ts.seek(input_ts_offset)
            output_ts.write(input_ts.read(segment_size))

        print(format_line(f), file=output_m3u8)

    for e in cat_footer:
        print(format_line(e), file=output_m3u8)
