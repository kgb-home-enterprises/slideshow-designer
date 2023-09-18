import unittest

from unittest.mock import patch
from src.google_photos.google_photos_api_service import GooglePhotosApiService


class TestGooglePhotosApiService(unittest.TestCase):
    @patch("src.google_photos.auth.get_credentials", return_value=True)
    def setUp(self, mock_get_credentials) -> None:
        pass

    def test_list_album_titles(self) -> None:
        self.assertTrue(True)
