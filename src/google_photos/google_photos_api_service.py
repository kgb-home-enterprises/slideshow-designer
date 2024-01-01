import json
import math
import requests

import src.google_photos.auth as auth
import src.utils.logging as logging


class GooglePhotosApiService:
    def __init__(self):
        self.logger = logging.Logger('GooglePhotosService')
        self.creds = auth.get_credentials()
        self.endpoint = 'https://photoslibrary.googleapis.com/v1'
        self.headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.creds.token)
        }

    def check_creds(self):
        if not self.creds or not self.creds.valid:
            self.logger.info('credentials not found or expired')
            self.creds = auth.get_credentials()
            self.logger.info('new credentials created')
            self.headers = {
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.creds.token)
            }

    def set_logging_level(self, level):
        self.logger.set_level(level)

    def list_album_titles(self):
        self.logger.info('request to list album titles')
        self.check_creds()
        response = requests.get(self.endpoint + '/albums', headers=self.headers)
        response.raise_for_status()
        self.logger.info('returning album titles')
        return [album.get('title') for album in response.json()['albums']]

    def get_album_id_from_name(self, album_name):
        self.logger.info(f'request for albumId of "{album_name}"')
        self.check_creds()
        response = requests.get(self.endpoint + '/albums', headers=self.headers)
        response.raise_for_status()
        for album in response.json()['albums']:
            if album['title'].lower() == album_name.lower():
                self.logger.info('returning albumId')
                return album['id']

        while 'nextPageToken' in response.json():
            page_token = response.json()['nextPageToken']
            response = requests.get(self.endpoint + f'/albums?pageToken={page_token}', headers=self.headers)
            response.raise_for_status()
            for album in response.json()['albums']:
                if album['title'].lower() == album_name.lower():
                    self.logger.info('returning albumId')
                    return album['id']
        self.logger.warn(f'No albumId found for {album_name}')
        return None

    def get_album_contents(self, album_id):
        self.logger.info(f'request for contents of album {album_id}')
        self.check_creds()
        payload = {
            'albumId': album_id,
            'pageSize': 100
        }
        more_content = True
        media_items = []
        while more_content:
            response = requests.post(self.endpoint + '/mediaItems:search', data=json.dumps(payload), headers=self.headers)
            response.raise_for_status()
            media_items += response.json()['mediaItems']
            if 'nextPageToken' in response.json():
                payload['pageToken'] = response.json()['nextPageToken']
            else:
                more_content = False
        self.logger.info(f'returning album contents')
        return media_items

    @staticmethod
    def download_photo(base_url, file_path):
        img_data = requests.get(base_url).content
        with open(file_path, 'wb') as handler:
            handler.write(img_data)

    def download_album_to_folder(self, album_id, path_to_folder, rename_to_order=False):
        self.logger.info(f'request to download album {album_id} to {path_to_folder}')
        album_contents = self.get_album_contents(album_id)
        digits = math.ceil(math.log(len(album_contents), 10))
        ordered_photos = []
        for i, photo in enumerate(album_contents):
            filename = photo['filename']
            if rename_to_order:
                filename = '{num:0{width}}'.format(num=i, width=digits) + '_' + filename
            self.logger.info(f'downloading {photo["filename"]} to {path_to_folder}/{filename}...')
            self.download_photo(photo['baseUrl'] + '=d', path_to_folder + '/' + filename)
            ordered_photos.append(filename)
        self.logger.info('album download complete!')
        return ordered_photos
