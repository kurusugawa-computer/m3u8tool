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
import subprocess

def convert(input_file, output_file, output_ts, disable_audio, subcommand):
    ffmpeg_path = os.environ.get('FFMPEG_PATH', 'ffmpeg')

    output_ext = os.path.splitext(output_file)[1].lower()

    exec_options = [
        ffmpeg_path,
        '-i', input_file.name,
        '-vcodec', 'copy',
    ]

    if disable_audio:
        exec_options += ['-an']
    else:
        exec_options += ['-acodec', 'copy']

    if output_ext == '.m3u8':
        exec_options += [
            '-hls_time', '1',
            '-hls_list_size', '0',
            '-hls_segment_type', 'mpegts',
            '-hls_flags', 'single_file',
        ]
        if output_ts is not None:
            exec_options += ['-hls_segment_filename', output_ts]

    exec_options.append(output_file)

    subprocess.run(exec_options)
