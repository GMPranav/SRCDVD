import requests
import json
import re
import time

from requests.models import Response

class GoogleAPI:
	def __init__(self) -> None:
		self.api_key = ""

	def auth(self):
		self.api_key = input("Enter your Google API Key: ")

	def checkVideo(self, videoLink):
		id = re.compile(r'[A-Za-z0-9_\-]{11}')
		videoID = re.findall(id, videoLink)
		if videoID:
			response = requests.get(
				"https://www.googleapis.com/youtube/v3/videos?id="+videoID.pop()+"&part=status&key="+self.api_key)
			if response.status_code == 200:
				data = response.json()
				# Return link if it dead or private
				if data["pageInfo"]["totalResults"] == 0:
					return videoLink
