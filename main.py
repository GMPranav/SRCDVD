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
		if google_status:
			for i in data.youtubeLinks:
				link = google.getVideoID(i)
			missed.append(google.checkVideo())
			
		if twitch_status:
			for i in data.twitchLinks:
				link = twitch.getVideoID(i)
			missed.append(twitch.checkVideo())

		# Unpack missed array
		for miss in [data for idx in range(len(missed)) for data in missed[idx]]:
			for run in data.runsArray:
				if miss in run['link']:
					data.dead_runs.append(
						f"https://speedrun.com/{data.gameAbbriveature}/run/{run['runID']}")
		
		file = open("missinglinks.txt", "w")
		for link in list(set(data.dead_runs)):
			file.write(link)
			file.write("\n")
		file.close()
