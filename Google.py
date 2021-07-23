import requests
import json
import re

class GoogleAPI:
	def __init__(self) -> None:
		self.apiKey = ""
		self.videoIDArray = []
		self.offset = 50
		self.notPrivate = []

	def auth(self):
		self.apiKey = input("Enter your Google API Key: ")

	def getVideoID(self, videoLink):
		id = re.compile(r'[A-Za-z0-9_\-]{11}')
		videoID = re.findall(id, videoLink)
		if videoID:
			self.videoIDArray.append(videoID.pop())

	def checkVideo(self):
		for offset in range(0, len(self.videoIDArray)+self.offset, self.offset):
			ids = ','.join([str(x) for x in self.videoIDArray[offset:self.offset+offset]])
			url = "https://www.googleapis.com/youtube/v3/videos?id=" + ids + "&part=status&key="+self.apiKey
			response = requests.get(url)
			if response.status_code == 200:
				for offset in response.json()['items']:
					self.notPrivate.append(offset['id'])
		return (set(self.videoIDArray)-set(self.notPrivate))

