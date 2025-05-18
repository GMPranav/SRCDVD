import requests
import re
import Config

class TwitchAPI:
	def __init__(self) -> None:
		self.body = {
			'client_id': None,
			'client_secret': None,
			"grant_type": 'client_credentials'
		}
		self.twitchAuthAPIKey = ""
		self.header = {}
		self.videoIDArray = []
		self.offset = 100
		self.notPrivate = []
		self.config = Config.Config()

	def auth(self):
		if self.config.isExists:
			TwitchClientID = self.config.load()['TwitchClientID']
			TwitchClientSecret = self.config.load()['TwitchClientSecret']
			if TwitchClientID and TwitchClientSecret:
				self.body['client_id'] = TwitchClientID
				self.body['client_secret'] = TwitchClientSecret
			else:
				self.body['client_id'] = input("Enter Client-ID: ")
				self.body['client_secret'] = input("Enter Client Secret: ")
		else:
			self.body['client_id'] = input("Enter Client-ID: ")
			self.body['client_secret'] = input("Enter Client Secret: ")
		response = requests.post(
			'https://id.twitch.tv/oauth2/token', self.body)
		if response.ok:
			self.twitchAuthAPIKey = response.json()['access_token']
			self.header = {'Client-ID': self.body['client_id'],
			'Authorization': "Bearer "+ self.twitchAuthAPIKey}
			return True
		if response.status_code == 400:
			print("[SKIP] Some of client keys not valid. Please pass a valid client key.")
			return False
	
	def getVideoID(self, videoLink):
		id = re.compile(r'(\d{8,11}).*')
		videoID = re.findall(id, videoLink)
		if videoID:
			self.videoIDArray.append(videoID.pop())

	def checkVideo(self):
		try:
			for offset in range(0, len(self.videoIDArray)+self.offset, self.offset):
				ids = '&id='.join([str(x) for x in self.videoIDArray[offset:self.offset+offset]])
				url = "https://api.twitch.tv/helix/videos?id=" + ids
				response = requests.get(url, headers=self.header)
				if response.ok:
					# List all video id's are not private and exist
					# Passing a group of ids returns only available video
					for data in response.json()['data']:
						self.notPrivate.append(data['id'])

			return (set(self.videoIDArray)-set(self.notPrivate))
			# KeyError occurs if a json object without a 'status' key
			# is received in response from the server 
			# In principle, if response code is 200, this should not happen
		except KeyError:
			pass
