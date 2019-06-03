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

import argparse
from m3u8tool import splitter, concatenator, converter

def main():
    parser = argparse.ArgumentParser(description='Process m3u8+ts files.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(dest='subcommand', help='sub-command help')
    parser_split = subparsers.add_parser('split', help='split m3u8+ts to splitted files', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_split.add_argument('-d', '--split_duration', type=float, default=60.0, help='duration [sec] if 0.0 then ignored')
    parser_split.add_argument('-s', '--split_size', type=int, default=0, help='size [byte] if 0 then ignored.')
    parser_split.add_argument('-m', '--output_m3u8_format', help='splitted m3u8 file name format', default='{filename}-{index:04}.m3u8')
    parser_split.add_argument('-t', '--output_ts_format', help='splitted ts file name format, if None then ignored.')
    parser_split.add_argument('input_m3u8', type=argparse.FileType('r'), help='input m3u8 file')

    parser_cat = subparsers.add_parser('cat', help='concatinate m3u8+ts to single file', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_cat.add_argument('-t', '--output_ts', type=argparse.FileType('wb'), help='output ts file, if None then ignored.')
    parser_cat.add_argument('input_m3u8', type=argparse.FileType('r'), nargs='+', help='input m3u8 files')
    parser_cat.add_argument('output_m3u8', type=argparse.FileType('w'), help='output m3u8 file')

    parser_convert = subparsers.add_parser('convert', help='convert file format', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_convert.add_argument('-t', '--output_ts', type=str, help='output ts file, if None then ignored.')
    parser_convert.add_argument('input_file', type=argparse.FileType('r'), help='input file')
    parser_convert.add_argument('output_file', type=str, help='output file')

    args = parser.parse_args()
    print(args)

    if args.subcommand == 'split':
        splitter.split(**vars(args))
    elif args.subcommand == 'cat':
        concatenator.cat(**vars(args))
    elif args.subcommand == 'convert':
        converter.convert(**vars(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
