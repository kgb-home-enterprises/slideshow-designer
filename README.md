# slideshow-designer

Before running any scripts, contact the application owner to obtain a `credentials.json` file for connecting to the API. Alternatively, you can configure your own [OAuth Credentials](https://developers.google.com/identity/protocols/oauth2). Copy your `credentials.json` file to `src/google_photos/creds`. 

## `slideshow_album.py`
Use this script to download an album from Google Photos in JPG format. By default it will prefix the filenames to preserve the order set in Google Photos, as well as maintain any editing done in Google Photos. Before running the script, update line 12 with the name of the album you want to download from Google Photos

```ALBUM_NAME = ''  # TODO: Enter your album name here```

The first time you run a script that accesses Google Photos you will be asked to login in your browser. After the first run your credentials will be cached for future use. When you run the script, you will be prompted with a file dialog box. Navigate to the folder where you would like to save the files and select "OK". The album will be download into it's own folder within the folder you select.

NOTE: If you receive the following error while attempting to login to Google, please reach out to your OAuth app owner to grant access to your Google account.
![image](https://github.com/kgb-home-enterprises/slideshow-designer/assets/64853910/2e0539d1-6205-4e83-a109-82cf54e8ff35)

