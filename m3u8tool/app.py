# coding: utf-8

import argparse
import m3u8tool.splitter
import m3u8tool.concatenater

def main():
    parser = argparse.ArgumentParser(description='Process m3u8+ts files.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(dest='subcommand', help='sub-command help')
    parser_split = subparsers.add_parser('split', help='split m3u8+ts to splitted files', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_split.add_argument('-d', '--split_duration', type=float, default=60.0, help='duration [sec] if 0.0 then ignored')
    parser_split.add_argument('-s', '--split_size', type=int, default=0, help='size [byte] if 0 then ignored.')
    parser_split.add_argument('-m', '--output_m3u8_format', help='splitted m3u8 file name format', default='{filename}-{index:04}.m3u8')
    parser_split.add_argument('-t', '--output_ts_format', help='splitted ts file name format, if None then ignored.')
    parser_split.add_argument('input_m3u8', type=argparse.FileType('r'), help='input m3u8 file')

    parser_cat = subparsers.add_parser('cat', help='cat m3u8+ts to catted file', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_cat.add_argument('-t', '--output_ts', type=argparse.FileType('wb'), help='output ts file, if None then ignored.')
    parser_cat.add_argument('input_m3u8', type=argparse.FileType('r'), nargs='+', help='input m3u8 files')
    parser_cat.add_argument('output_m3u8', type=argparse.FileType('w'), help='output m3u8 file')

    args = parser.parse_args()
    print(args)

    if args.subcommand == 'split':
        m3u8tool.splitter.split(**vars(args))
    elif args.subcommand == 'cat':
        m3u8tool.concatenater.cat(**vars(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
