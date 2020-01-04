import sys
import logging
import os
from yandex_music.client import Client
from yandex_music.exceptions import BadRequest


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(message)s'
)
logger = logging.getLogger('yadow')


if __name__ == '__main__':
    client = Client()
    album_ids = sys.argv[1:]

    for album_id in album_ids:
        try:
            album = client.albums_with_tracks(album_id)
        except BadRequest:
            logger.error(f'invalid album id: {album_id}')
            continue

        logger.info(f'{album.title}: found {album.track_count} tracks')

        downloaded = 0
        path = album.title
        os.mkdir(path)
        for disk in album.volumes:
            for track in disk:
                logger.debug(f'downloading {track.title}')
                try:
                    track.download(
                        os.path.join(path, f'{track.title}.mp3'),
                    )
                    downloaded += 1
                except Exception:
                    logger.error(f'could not download {track.title}')
        logger.info(f'downloaded {downloaded} tracks')
