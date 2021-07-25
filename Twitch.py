import requests
import json
import re

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

	def auth(self):
		self.body['client_id'] = input("Enter Client-ID: ")
		self.body['client_secret'] = input("Enter Client Secret: ")
		response = requests.post(
			'https://id.twitch.tv/oauth2/token', self.body)
		if response.status_code == 200:
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
				ids = ','.join([str(x) for x in self.videoIDArray[offset:self.offset+offset]])
				url = "https://api.twitch.tv/helix/videos?id=" + ids
				response = requests.get(url, headers=self.header)
				if response.status_code == 200:
					# Return link if it dead
					for i in response.json()['data']:
						self.notPrivate.append(i['id'])

			return (set(self.videoIDArray)-set(self.notPrivate))
			# KeyError occurs if a json object without a 'status' key
			# is received in response from the server 
			# In principle, if response code is 200, this should not happen
		except KeyError:
			pass
