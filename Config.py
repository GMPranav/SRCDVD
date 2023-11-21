import json
import os.path as fs

class Config:
	def __init__(self) -> None:
		self.configName = "config.json"

	def load(self):
		if self.isExists:
			with open(self.configName) as config:
				return json.load(config)

	def isExists(self):
		return fs.isfile(self.configName) and fs.getsize(self.configName) > 0
