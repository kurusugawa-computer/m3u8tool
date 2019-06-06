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

import unittest
import sys
import os
import hashlib
from io import StringIO
import tempfile
from m3u8tool import app

def run_app(args):
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        app.main(args=args)
    finally:
        sys.stdout, sys.stderr = old_out, old_err

    return new_out.getvalue().strip()

class TestM3u8toolApp(unittest.TestCase):
    def setUp(self):
        self.tmpdir_obj = tempfile.TemporaryDirectory()
        self.tmpdir = self.tmpdir_obj.name

    def tearDown(self):
        self.tmpdir_obj.cleanup()

    def test_split(self):
        output_m3u8 = os.path.join(self.tmpdir, 'out-{index:04}.m3u8')
        self.assertEqual(
            output_m3u8.format(index=1)+' 60.064',
            run_app([
                'split',
                '-m', output_m3u8,
                'tests/data/Psalm16_ComeToTheWatersMovie.m3u8',
            ])
        )
        self.assertTempdirFileCount(1)
        with open('tests/data/Psalm16_ComeToTheWatersMovie.m3u8') as f:
            self.assertTempdirFileContent(f.read(), 'out-0001.m3u8')

    def test_split_m3u8(self):
        output_m3u8 = os.path.join(self.tmpdir, 'out-{index:04}.m3u8')
        self.assertEqual(
            '\n'.join([(output_m3u8+' 3.0032').format(index=i) for i in range(1,21)]),
            run_app(['split', '-d', '3.0', '-m', output_m3u8, 'tests/data/Psalm16_ComeToTheWatersMovie.m3u8'])
        )
        self.assertTempdirFileCount(20)
        self.assertTempdirFileContent(
            '#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-TARGETDURATION:3\n#EXT-X-MEDIA-SEQUENCE:0\n#EXTINF:3.003200,\n' +
            '#EXT-X-BYTERANGE:56212@0\nPsalm16_ComeToTheWatersMovie.ts\n#EXT-X-ENDLIST\n',
            'out-0001.m3u8'
        )

    def test_split_m3u8_e(self):
        output_m3u8 = os.path.join(self.tmpdir, 'out-{index:04}.m3u8')
        self.assertEqual(
            '\n'.join([(output_m3u8+' 3.0032').format(index=i) for i in range(1,21)]),
            run_app(['split', '-e', '-d', '3.0', '-m', output_m3u8, 'tests/data/Psalm16_ComeToTheWatersMovie.m3u8'])
        )
        self.assertTempdirFileCount(20)
        self.assertTempdirFileContent(
            '#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-TARGETDURATION:3\n#EXT-X-MEDIA-SEQUENCE:0\n#EXTINF:3.003200,\n' +
            '#EXT-X-BYTERANGE:56212@0\n'+os.path.abspath('tests/data/Psalm16_ComeToTheWatersMovie.ts')+'\n#EXT-X-ENDLIST\n',
            'out-0001.m3u8'
        )

    def _test_split_ts(self, output_m3u8, output_ts, append_options=[]):
        options = [
            'split',
            '-d', '3.0',
            '-m', output_m3u8,
            '-t', output_ts,
        ] + append_options
        self.assertEqual(
            '\n'.join([(output_ts+' '+output_m3u8+' 3.0032').format(index=i) for i in range(1,21)]),
            run_app(options + ['tests/data/Psalm16_ComeToTheWatersMovie.m3u8'])
        )
        self.assertTempdirFileCount(40)
        self.assertTempdirFileMD5('a0ead415b873efed81efaf1f11ab6ea6', 'out-0001.ts')
        self.assertTempdirFileMD5('779e321a9afe72adcdbb7556a7572dde', 'out-0002.ts')
        self.assertTempdirFileContent(
            '#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-TARGETDURATION:3\n#EXT-X-MEDIA-SEQUENCE:0\n#EXTINF:3.003200,\n' +
            '#EXT-X-BYTERANGE:56212@0\n'+output_ts.format(index=1)+'\n#EXT-X-ENDLIST\n',
            'out-0001.m3u8'
        )

    def test_split_ts_relative(self):
        self._test_split_ts(
            os.path.join(self.tmpdir, 'out-{index:04}.m3u8'),
            'out-{index:04}.ts'
        )

    def test_split_ts_relative_e(self):
        self._test_split_ts(
            os.path.join(self.tmpdir, 'out-{index:04}.m3u8'),
            'out-{index:04}.ts',
            append_options=['-e']
        )

    def test_split_ts_absolute(self):
        self._test_split_ts(
            os.path.join(self.tmpdir, 'out-{index:04}.m3u8'),
            os.path.join(self.tmpdir, 'out-{index:04}.ts')
        )

    def test_split_ts_absolute_e(self):
        self._test_split_ts(
            os.path.join(self.tmpdir, 'out-{index:04}.m3u8'),
            os.path.join(self.tmpdir, 'out-{index:04}.ts'),
            append_options=['-e']
        )

    def assertTempdirFileMD5(self, md5, filepath):
        hash_md5 = hashlib.md5()
        with open(os.path.join(self.tmpdir, filepath), 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        self.assertEqual(md5, hash_md5.hexdigest())

    def assertTempdirFileCount(self, count):
        self.assertEqual(
            count,
            len(os.listdir(self.tmpdir))
        )

    def assertTempdirFileContent(self, expected, filepath):
        with open(os.path.join(self.tmpdir, filepath), 'r') as f:
            self.assertEqual(expected, f.read())


if __name__ == '__main__':
    unittest.main()
