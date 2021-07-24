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
		url = "https://www.googleapis.com/youtube/v3/videos?id=0&part=status&key="+self.apiKey
		response = requests.get(url)
		if response.status_code == 400:
			print("[SKIP] API key not valid. Please pass a valid API key.")
			return False
		if response.status_code == 200:
			return True

	def getVideoID(self, videoLink):
		# FIXME: False positive arises because regex parses the channel names as well as the video id
		# which means that the video id for the race will not be valid in the list to check, e.g.
		# getVideoID(https://www.youtube.com/watch?v=<videoid>) -> <videoid>
		# getVideoID(https://www.youtube.com/watch?v=<videoid>&ab_channel=<channelName>) -> channelName
		# getVideoID(https://www.youtube.com/watch?v=<videoid>&list=<playlistid>&index=2) -> returns the last 11 characters of playlist id
		#
		# because the video id is associated with the run id, so if we pass on the channel name or part of the playlist, 
		# google api decides that the link is invalid and marks the run with a broken link
		id = re.compile(r'\/[A-Za-z0-9_\-]{11})',r'\=[A-Za-z0-9_\-]{11}')
		videoID = re.findall(id, videoLink)
		if videoID:
			self.videoIDArray.append(videoID.pop()[1:])

	def checkVideo(self):
		for offset in range(0, len(self.videoIDArray)+self.offset, self.offset):
			ids = ','.join([str(x) for x in self.videoIDArray[offset:self.offset+offset]])
			url = "https://www.googleapis.com/youtube/v3/videos?id=" + ids + "&part=status&key="+self.apiKey
			response = requests.get(url)
			if response.status_code == 200:
				for offset in response.json()['items']:
					self.notPrivate.append(offset['id'])
		return (set(self.videoIDArray)-set(self.notPrivate))

