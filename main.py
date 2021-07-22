import Twitch
import Google
import Data
from collections import Counter


if __name__ == '__main__':
	missed = []
	dead_runs = []

	twitch = Twitch.TwitchAPI()
	google = Google.GoogleAPI()
	twitch.auth()
	google.auth()

	data = Data.CData()
	data.getRuns()
	data.getNameID()
	data.getLinks()

	# TODO: It may be worth paralleling the checks, at least for 4-8 threads
	# And it is desirable to get rid of these "for"
	for i in data.twitchLinks:
		link = twitch.checkVideo(i)
		if link:
			missed.append(link)

	for i in data.youtubeLinks:
		link = google.checkVideo(i)
		if link:
			missed.append(link)

	for miss in missed:
		for info in data.Links:
			if miss == info['link']:
				dead_runs.append(
					f"https://speedrun.com/{data.gameAbriveature}/run/{info['runID']}")
	# Print unique links
	print(*Counter(dead_runs))

