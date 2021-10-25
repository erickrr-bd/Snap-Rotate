from time import strftime
from datetime import datetime
from pycurl import Curl, HTTP_CODE
from urllib.parse import urlencode
from modules.UtilsClass import Utils

"""
Class that allows you to manage the sending of alerts through Telegram.
"""
class Telegram:
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Constructor for the Telegram class.

	Parameters:
	self -- An instantiated object of the Telegram class.
	"""
	def __init__(self):
		self.utils = Utils()

	"""
	Method that sends the alert to the telegram channel.

	Parameters:
	self -- Instance object.
	telegram_chat_id -- Telegram channel identifier to which the letter will be sent.
	telegram_bot_token -- Token of the Telegram bot that is the administrator of the Telegram channel to which the alerts will be sent.
	message -- Message to be sent to the Telegram channel.
	"""
	def sendTelegramAlert(self, telegram_chat_id, telegram_bot_token, message):
		if len(message) > 4096:
			message = "The size of the message in Telegram (4096) has been exceeded. Overall size: " + str(len(message))
		c = Curl()
		url = 'https://api.telegram.org/bot' + str(telegram_bot_token) + '/sendMessage'
		c.setopt(c.URL, url)
		data = { 'chat_id' : telegram_chat_id, 'text' : message }
		pf = urlencode(data)
		c.setopt(c.POSTFIELDS, pf)
		c.perform_rs()
		status_code = c.getinfo(HTTP_CODE)
		c.close()
		self.getStatusByTelegramCode(status_code)

	"""
	Method that creates the header of the message that will be sent to Telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.

	Return:
	header -- Header of the message.
	"""
	def getHeaderMessage(self):
		header = u'\u26A0\uFE0F' + " " + 'Snap-Rotate' +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		return header

	"""
	Method that generates the message in Telegram for when the creation of a snapshot has begun.

	Parameters:
	self -- An instantiated object of the Telegram class.
	index_name -- Name of the index that will be saved in the snapshot.
	repository_name -- Name of the repository where the snapshot will be saved.

	Return:
	message -- Message to send.
	"""
	def getMessageStartCreationSnapshot(self, index_name, snapshot_name, repository_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Snapshot creation has started\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + snapshot_name +"\n"
		message += u'\u2611\uFE0F' + " Index name: " + index_name + "\n"
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name
		return message

	"""
	Method that generates the message in Telegram for when the creation of a repository is finished.

	Parameters:
	self -- An instantiated object of the Telegram class.
	repository_name -- Name of the repository created.
	path_repository -- Path where the repository is hosted.

	Return:
	message -- Message to send.
	"""
	def getMessageEndCreationRepository(self, repository_name, path_repository):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Repository creation finished\n"
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name + '\n'
		message += u'\u2611\uFE0F' + " Repository path: " + path_repository
		return message

	"""
	Method that generates the message in Telegram for when the creation of a snapshot has finished.

	Parameters:
	self -- An instantiated object of the Telegram class.
	snapshot_name -- Name of the snapshot created.
	repository_name -- Name of the repository where the snapshot was saved.
	start_time -- Time when snapshot creation started.
	end_time -- Time when snapshot creation finished.

	Return:
	message -- Message to send.
	"""
	def getMessageEndSnapshot(self, snapshot_name, repository_name, start_time, end_time):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Snapshot creation completed\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + snapshot_name +"\n"
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name + "\n"
		message += u'\u2611\uFE0F' + " Start time: " + str(start_time) + "\n"
		message += u'\u2611\uFE0F' + " End time: " + str(end_time)
		return message

	"""
	Method that generates the message in Telegram for when an index is eliminated.

	Parameters:
	self -- An instantiated object of the Telegram class.
	index_name -- Index name removed.

	Return:
	message -- Message to send.
	"""
	def getMessageDeleteIndex(self, index_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Index removed\n"
		message += u'\u2611\uFE0F' + " Index name: " + index_name
		return message

	"""
	Method that generates the message in Telegram for when a repository is compressed.
	
	Parameters:
	self -- An instantiated object of the Telegram class.
	path_compress_file -- Path of the resulting compressed file.

	Return:
	message -- Message to send.
	"""
	def getMessageCompressFile(self, path_compress_file):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Repository compressed into a file\n"
		message += u'\u2611\uFE0F' + " Path of the compressed file: " + path_compress_file
		return message
	
	"""
	Method that prints the status of the alert delivery based on the response HTTP code.

	Parameters:
	self -- An instantiated object of the Telegram class.
	telegram_code -- HTTP code in response to the request made to Telegram.
	"""
	def getStatusByTelegramCode(self, telegram_code):
		if telegram_code == 200:
			self.utils.createSnapRotateLog("Telegram message sent.", 1)
			print("Telegram message sent.")
		elif telegram_code == 400:
			self.utils.createSnapRotateLog("Telegram message not sent. Status: Bad request.", 3)
			print("Telegram message not sent. Status: Bad request.")
		elif telegram_code == 401:
			self.utils.createSnapRotateLog("Telegram message not sent. Status: Unauthorized.", 3)
			print("Telegram message not sent. Status: Unauthorized.")
		elif telegram_code == 404:
			self.utils.createSnapRotateLog("Telegram message not sent. Status: Not found.", 3)
			print("Telegram message not sent. Status: Not found.")