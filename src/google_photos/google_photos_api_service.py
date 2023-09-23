import json
import math
import requests

import src.google_photos.auth as auth


class GooglePhotosApiService:
    def __init__(self):
        self.creds = auth.get_credentials()
        self.endpoint = 'https://photoslibrary.googleapis.com/v1'
        self.headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.creds.token)
        }

    def check_creds(self):
        if not self.creds or not self.creds.valid:
            self.creds = auth.get_credentials()
            self.headers = {
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(self.creds.token)
            }

    def list_album_titles(self):
        self.check_creds()
        response = requests.get(self.endpoint + '/albums', headers=self.headers)
        response.raise_for_status()
        return [album.get('title') for album in response.json()['albums']]

    def get_album_id_from_name(self, album_name):
        self.check_creds()
        response = requests.get(self.endpoint + '/albums', headers=self.headers)
        response.raise_for_status()
        for album in response.json()['albums']:
            if album['title'].lower() == album_name.lower():
                return album['id']
        return None

    def get_album_contents(self, album_id):
        self.check_creds()
        payload = {
            'albumId': album_id
        }
        response = requests.post(self.endpoint + '/mediaItems:search', data=json.dumps(payload), headers=self.headers)
        response.raise_for_status()
        return response.json()['mediaItems']

    @staticmethod
    def download_photo(base_url, file_path):
        img_data = requests.get(base_url).content
        with open(file_path, 'wb') as handler:
            handler.write(img_data)

    def download_album_to_folder(self, album_id, path_to_folder, rename_to_order=False):
        album_contents = self.get_album_contents(album_id)
        digits = math.ceil(math.log(len(album_contents), 16))
        ordered_photos = []
        for i, photo in enumerate(album_contents):
            filename = photo['filename']
            if rename_to_order:
                filename = '{num:0{width}x}'.format(num=i, width=digits) + '_' + filename
            self.download_photo(photo['baseUrl'] + '=d', path_to_folder + '/' + filename)
            ordered_photos.append(filename)
        return ordered_photos
