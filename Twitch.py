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
		self.token = ""

	def auth(self):
		self.body['client_id'] = input("Enter Client-ID: ")
		self.body['client_secret'] = input("Enter Client Secret: ")
		self.twitchAuthAPIKey = requests.post(
			'https://id.twitch.tv/oauth2/token', self.body).json()['access_token']
		self.header = {'Client-ID': self.body['client_id'],
                'Authorization': "Bearer "+self.twitchAuthAPIKey}

	def checkVideo(self, videoLink):
		try:
			id = re.compile(r'\d{8,11}')
			videoID = re.findall(id, videoLink)
			if videoID:
				url = "https://api.twitch.tv/helix/videos?id="+videoID.pop()
				response = requests.get(url, headers=self.header)
				if response.status_code == 200:
					# Return link if it dead
					if response.json()['status'] == 404:
						return videoLink
		# Else do nothing
		#
		except KeyError:
			pass
