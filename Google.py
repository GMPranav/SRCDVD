import re
import Config
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleAPI:
    def __init__(self) -> None:
        self.credentials = None
        self.token_file = "google_token.pickle"
        self.videoIDArray = []
        self.offset = 50
        self.notPrivate = []
        self.config = Config.Config()

    def auth(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.credentials = pickle.load(token)
                status, _ = self.youtubeRequest('0')

        if not self.credentials or not status:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_oauth.json',
                scopes=["https://www.googleapis.com/auth/youtube.readonly"]
            )
            self.credentials = flow.run_local_server(port=0)
            status, _ = self.youtubeRequest('0')

            with open(self.token_file, 'wb') as token:
                pickle.dump(self.credentials, token)

        return status

    def youtubeRequest(self, ids):
        try:
            youtube = build('youtube', 'v3', credentials=self.credentials)
            request = youtube.videos().list(part='status', id=ids)
            response = request.execute()
            return True, response
        except HttpError as e:
            print(f"[ERROR] API request failed: {e}")
            return False, None

    def getVideoID(self, videoLink):
        id = re.compile(r'([A-Za-z0-9_\-]{11}).*')
        videoID = re.findall(id, videoLink)
        if videoID:
            self.videoIDArray.append(videoID.pop())

    def checkVideo(self):
        for offset in range(0, len(self.videoIDArray)+self.offset, self.offset):
            ids = ','.join([str(x) for x in self.videoIDArray[offset:self.offset+offset]])
            status, response = self.youtubeRequest(ids)
            if status:
                # List all video id's are not private and exist
                # Passing a group of ids returns only available videos
                for item in response['items']:
                    self.notPrivate.append(item['id'])
        return (set(self.videoIDArray)-set(self.notPrivate))
