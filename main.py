import Twitch
import Google
import Data

if __name__ == '__main__':

	twitch = Twitch.TwitchAPI()
	google = Google.GoogleAPI()

	twitch_status = twitch.auth()
	google_status = google.auth()
	if twitch_status or google_status:
		missed = []
		data = Data.Data()
		data.getRuns()
		data.getNameID()
		data.getLinks()

		# TODO: If moderators will use this tool frequently,
		#  it may be worth caching old runs to a file to speed things up,
		#  so no reason to check over and over again every time they run it
		#

		for i in data.youtubeLinks:
			link = google.getVideoID(i)
		missed = google.checkVideo()

		for i in data.twitchLinks:
			link = twitch.checkVideo(i)
			if link:
				missed.append(link)

		for miss in missed:
			for run in data.runsArray:
				if miss in run['link']:
					data.dead_runs.append(
						f"https://speedrun.com/{data.gameAbbriveature}/run/{run['runID']}")

		file = open("missinglinks.txt", "w")
		for link in list(set(data.dead_runs)):
			file.write(link)
			file.write("\n")
		file.close()
