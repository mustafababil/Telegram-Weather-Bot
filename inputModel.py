
"""
	Represents user input type
	https://core.telegram.org/bots/api#available-types
"""

import json

class inputModel(object):

	"""
		Initialiaze with direct user input without modification.
	"""
	def __init__(self, input):
		self.input = input


	def getUpdateID(self):
		return self.input['update_id']


	def getMessageID(self):
		return self.input['message'].get('message_id')


	def getDate(self):
		return self.input['message'].get('date')


	def getText(self):
		text = self.input['message'].get('text')
		if text:
			text = text.encode('utf-8','strict') # fix for every type of character input
		return text

	def getFromID(self):
		return self.input['message'].get('from')['id']


	def getFromName(self):
		return self.input['message'].get('from')['first_name']


	def getChatID(self):
		return self.input['message'].get('chat')['id']


	def getLocation(self):
		return self.input['message'].get('location')

	
	def getLat(self):
		if self.getLocation():
			return self.getLocation().get('latitude')


	def getLng(self):
		if self.getLocation():
			return self.getLocation().get('longitude')






