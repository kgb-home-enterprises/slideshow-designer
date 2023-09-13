import auth

from googleapiclient.discovery import build


class GooglePhotosApiService:
    def __init__(self):
        self.creds = auth.get_credentials()
        self.service = build('photoslibrary', 'v1', credentials=self.creds, static_discovery=False)

    def check_creds(self):
        if not self.creds or not self.creds.valid:
            self.creds = auth.get_credentials()
            self.service = build('photoslibrary', 'v1', credentials=self.creds, static_discovery=False)

    def list_album_titles(self):
        self.check_creds()
        response = self.service.albums().list().execute()
        return [album.get('title') for album in response['albums']]


print(GooglePhotosApiService().list_album_titles())
