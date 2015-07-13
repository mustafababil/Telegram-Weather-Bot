
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


	"""
		Return update's unique identifier

		@return integer
	"""
	def getUpdateID(self):
		return self.input['update_id']


	"""
		Return unique message identifier

		@return integer
	"""
	def getMessageID(self):
		return self.input['message'].get('message_id')


	"""
		Return date the message was sent in Unix time

		@return integer
	"""
	def getDate(self):
		return self.input['message'].get('date')


	"""
		Return UTF-8 text string if it is a text message

		@return string | None
	"""
	def getText(self):
		text = self.input['message'].get('text')
		if text:
			text = text.encode('utf-8','strict') # fix for every type of character input
		return text


	"""
		Return unique identifier for corressponding user or bot

		@return integer
	"""
	def getFromID(self):
		return self.input['message'].get('from')['id']


	"""
		Return first name of corressponding user or bot

		@return string
	"""
	def getFromName(self):
		return self.input['message'].get('from')['first_name']


	"""
		Return conversation ID for private or group chat

		@return integer
	"""
	def getChatID(self):
		return self.input['message'].get('chat')['id']


	"""
		Return location type if entered

		@return Location | None
	"""
	def getLocation(self):
		return self.input['message'].get('location')


	"""
		Return latitude

		@return float | None
	"""
	def getLat(self):
		if self.getLocation():
			return self.getLocation().get('latitude')
		return None


	"""
		Return longitude

		@return float | None
	"""
	def getLng(self):
		if self.getLocation():
			return self.getLocation().get('longitude')
		return None
