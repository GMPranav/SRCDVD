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
			print("[SKIP] Some of client key not valid. Please pass a valid client key.")
			return False

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
		# KeyError occurs if a json object without a 'status' key
		# is received in response from the server 
		# In principle, if response code is 200, this should not happen
		except KeyError:
			pass
