import requests
import re
import json

class CData:
	def __init__(self) -> None:
		self.gameAbriveature = ""
		self.gameInfo = "https://www.speedrun.com/api/v1/games/"
		self.runsCount = 0
		self.gameName = ""
		self.gameID = ""
		self.videoLinks = []
		self.youtubeLinks = []
		self.twitchLinks = []
		self.youtubeTemplate = ["youtube", "youtu"]
		self.twitchTemplate = ["twitch"]
		self.Links = []

	def getRuns(self):
		try:
			numRuns = re.compile('Number of runs.*?</div></div><div class=\"')
			if self.gameAbriveature == "":
				self.gameAbriveature = input(
					"Enter the game's abbreviation in speedrun.com (eg. \"smb1\" for Super Mario Bros.): ")

			stats = requests.get("https://www.speedrun.com/" + self.gameAbriveature + "/gamestats").text
			self.runsCount = int(re.findall(numRuns, stats.replace('\t', '').replace('\n', '')).pop()\
				.replace("Number of runs</div><div class=\"col-sm-6 row-list-text\">", "")\
					.replace("</div></div><div class=\"", "").replace(',', ""))
		except IndexError:
			print("No such abbreviation was found\n")

	def getNameID(self):
		try:
			if self.gameAbriveature == "":
				self.gameAbriveature = input(
				"Enter the game's abbreviation in speedrun.com (eg. \"smb1\" for Super Mario Bros.): ")
				response = requests.get(
				self.gameInfo + self.gameAbriveature).json()
				self.gameName = response['data']['names']['international']
				self.gameID = response['data']['game']
		except (IndexError, KeyError, TypeError):
			print("No such abbreviation was found\n")

	def getLinks(self):
		try:
			for offset in range(0, self.runsCount, 200):
				url = "https://www.speedrun.com/api/v1/runs?max=200&offset=" + \
					str(offset) + "&status=verified&game=" + self.gameID
				data = requests.get(url).json()['data']
				for runs in data:
					try:
						self.videoLinks.append(runs['videos']['links'][0]['uri'])
						self.Links.append({"runID": runs['id'], "link": runs['videos']['links'][0]['uri']})
						#for i in range(len(runs['videos']['links'])):
						#	self.videoLinks.append(runs['videos']['links'][i]['uri'])
						#	self.Links.append(
						#		{"runID": runs['id'], "link": runs['videos']['links'][i]['uri']})
					except TypeError:
						pass
		except KeyError:
			self.youtubeLinks = [
				link for link in self.videoLinks for template in self.youtubeTemplate if template in link]
			self.twitchLinks = [
				link for link in self.videoLinks for template in self.twitchTemplate if template in link]
			
