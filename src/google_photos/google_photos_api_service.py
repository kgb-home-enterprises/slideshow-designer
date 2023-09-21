import json

import src.google_photos.auth as auth
import requests


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
        response = requests.get(self.endpoint + '/mediaItems:search',
                                data=json.dumps(payload), headers=self.headers)
        response.raise_for_status()
        return response
