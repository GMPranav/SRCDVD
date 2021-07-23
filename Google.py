import requests
import json
import re

class GoogleAPI:
	def __init__(self) -> None:
		self.apiKey = ""

	def auth(self):
		self.apiKey = input("Enter your Google API Key: ")

	def checkVideo(self, videoLink):
		id = re.compile(r'[A-Za-z0-9_\-]{11}')
		videoID = re.findall(id, videoLink)
		if videoID:
			response = requests.get(
				"https://www.googleapis.com/youtube/v3/videos?id="+videoID.pop()+"&part=status&key="+self.apiKey)
			if response.status_code == 200:
				data = response.json()
				# Return link if it dead or private
				#
				if data["pageInfo"]["totalResults"] == 0:
					return videoLink
