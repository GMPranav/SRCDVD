import requests
import re
import Config

class GoogleAPI:
	def __init__(self) -> None:
		self.apiKey = ""
		self.videoIDArray = []
		self.offset = 50
		self.notPrivate = []
		self.config = Config.Config()


	def auth(self):
		if self.config.isExists():
			googleAPI = self.config.load()['GoogleAPIKey']
			if googleAPI:
				self.apiKey = googleAPI
			else:
				self.apiKey = input("Enter your Google API Key: ")
		else:
			self.apiKey = input("Enter your Google API Key: ")
		url = "https://www.googleapis.com/youtube/v3/videos?id=0&part=status&key="+self.apiKey
		response = requests.get(url)
		if response.status_code == 400:
			print("[SKIP] API key not valid. Please pass a valid API key.")
			return False
		if response.ok:
			return True

	def getVideoID(self, videoLink):
		id = re.compile(r'([A-Za-z0-9_\-]{11}).*')
		videoID = re.findall(id, videoLink)
		if videoID:
			self.videoIDArray.append(videoID.pop())

	def checkVideo(self):
		for offset in range(0, len(self.videoIDArray)+self.offset, self.offset):
			ids = ','.join([str(x) for x in self.videoIDArray[offset:self.offset+offset]])
			url = "https://www.googleapis.com/youtube/v3/videos?id=" + ids + "&part=status&key="+self.apiKey
			response = requests.get(url)
			if response.ok:
				# List all video id's are not private and exist
				# Passing a group of ids returns only available videos
				for item in response.json()['items']:
					self.notPrivate.append(item['id'])
		return (set(self.videoIDArray)-set(self.notPrivate))

