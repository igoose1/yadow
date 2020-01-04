# Copyright 2020 Oskar Sharipov
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

"""
yadow

downloads tracks from Yandex Music by their albums' ids
"""

import sys
import logging
import os
from yandex_music.client import Client
from yandex_music.exceptions import BadRequest


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(message)s'
)


if __name__ == '__main__':
    logger = logging.getLogger('yadow')
    client = Client()
    album_ids = sys.argv[1:]

    if album_ids in ([], ['--help'], ['-?']):
        print('''Usage yadow.py [OPTIONS] ALBUM_ID [ALBUM_ID...]

yadow downloads tracks from Yandex Music by their albums' ids

Options:
    --help, -?        Print this help text and exit''')
        sys.exit()

    for album_id in album_ids:
        try:
            album = client.albums_with_tracks(album_id)
        except BadRequest:
            logger.error(f'invalid album id: {album_id}')
            continue

        logger.info(f'"{album.title}": found {album.track_count} tracks')

        downloaded = 0
        path = album.title
        try:
            os.mkdir(path)
        except FileExistsError:
            logger.info(f'directory {path} exists')
        for disk in album.volumes:
            for track in disk:
                logger.debug(f'downloading "{track.title}"')
                try:
                    name = '{num}.{title}.mp3'.format(
                        num=str(album.track_count - downloaded).rjust(
                            len(str(album.track_count)), '0'
                        ),
                        title=track.title
                    )
                    track.download(
                        os.path.join(path, name),
                    )
                    downloaded += 1
                except Exception:
                    logger.error(f'could not download "{track.title}"')
        logger.info(f'downloaded {downloaded} tracks into {path}')
