# coding: utf-8

import os
import subprocess

def convert(input_file, output_file, output_ts, subcommand):
    ffmpeg_path = os.environ.get('FFMPEG_PATH', 'ffmpeg')

    output_ext = os.path.splitext(output_file)[1].lower()

    exec_options = [
        ffmpeg_path,
        '-i', input_file.name,
        '-vcodec', 'copy',
        '-acodec', 'copy',
    ]

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
