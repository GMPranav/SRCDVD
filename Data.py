import requests
import re
import json

class Data:
	def __init__(self) -> None:
		self.gameAbbriveature = ""
		self.gameInfo = "https://www.speedrun.com/api/v1/games/"
		self.runsCount = 0
		self.gameName = ""
		self.gameID = ""
		self.videoLinks = []
		self.youtubeLinks = []
		self.twitchLinks = []
		self.youtubeTemplate = ["youtube", "youtu"]
		self.twitchTemplate = ["twitch"]
		self.runsArray = []
		self.dead_runs = []
		self.offset = 200

	def getNameID(self):
		if self.gameAbbriveature == "":
				self.gameAbbriveature = input("Enter the game's abbreviation in speedrun.com (eg. \"smb1\" for Super Mario Bros.): ")

		response = requests.get(self.gameInfo + self.gameAbbriveature)
		if response.status_code == 200:
			response = response.json()
			self.gameName = response['data']['names']['international']
			self.gameID = response['data']['id']

	# TODO: Sometimes, array with dead runs includes normal runs, but which, for some reason, are not stored into api
	# (e.g. a link in the comments) and there is only a text link.
	# Most likely, we'll have to add some extra code to check if link to video exists in comments. (Weird)
	#
	def getLinks(self):
		offset = 0
		noMoreResults = False
		while not noMoreResults:
			url = "https://www.speedrun.com/api/v1/runs?max=200&offset=" + \
				str(offset) + "&status=verified&game=" + self.gameID
			response = requests.get(url)
			if response.status_code == 200:
				responseJson = response.json()
				data = responseJson['data']
				for runs in data:
					try:
						try:
							link = runs['videos']['links'][0]['uri']
							self.videoLinks.append(link)
							self.runsArray.append({"runID": runs['id'], "link": link})
						# The TypeError exception is used here to take a runID
						# from a run where 'links' key exists but is empty
						#
						except TypeError:
							self.dead_runs.append(f"https://speedrun.com/{self.gameAbbriveature}/run/{runs['id']}")
							continue
					# The KeyError exception is used here to take runID
					#  from a run where 'links' key not exists
					#
					except KeyError:
						self.dead_runs.append(f"https://speedrun.com/{self.gameAbbriveature}/run/{runs['id']}")
						continue
				if responseJson.get('pagination').get('links'):
					next_page = next((page['uri'] for page in responseJson['pagination']['links'] if page.get('rel') == 'next'), None)
					if next_page:
						offset += 200
					else:
						noMoreResults = True

			self.youtubeLinks = [link for link in self.videoLinks for template in self.youtubeTemplate if template in link]
			self.twitchLinks = [link for link in self.videoLinks for template in self.twitchTemplate if template in link]
