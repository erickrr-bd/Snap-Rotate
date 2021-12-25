from os import path
from sys import exit
from time import sleep
from datetime import datetime
from calendar import monthrange
from tarfile import open as open_tf
from modules.UtilsClass import Utils
from modules.ElasticClass import Elastic
from modules.TelegramClass import Telegram

"""
Class that manages everything related to Snap-Rotate.
"""
class Rotate:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Constructor for the Rotate class.

	Parameters:
	self -- An instantiated object of the Rotate class.
	"""
	def __init__(self):
		self.utils = Utils()

	"""
	Method that starts Snap-Rotate.

	Parameters:
	self -- An instantiated object of the Rotate class.
	"""
	def startSnapRotate(self):
		path_configuration_file = self.utils.getPathSnapRotate("conf") + "/snap_rotate_configuration.yaml"
		try:
			if path.exists(path_configuration_file):
				snap_rotate_configurationiguration = self.utils.readYamlFile(path_configuration_file, 'r')
				if float(snap_rotate_configurationiguration['es_version']) >= 7.0 and float(snap_rotate_configurationiguration['es_version']) <= 7.16:
					print("Snap-Rotate v3.1")
					print("@2021 Tekium. All rights reserved.")
					print("Author: Erick Rodriguez")
					print("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com")
					print("License: GPLv3")
					print("\nSnap-Rotate started...")
					time_execution_rotate = snap_rotate_configurationiguration['time_execution_rotate'].split(':')
					while True:
						now = datetime.now()
						if now.hour == int(time_execution_rotate[0]) and now.minute == int(time_execution_rotate[1]):
							elastic = Elastic(snap_rotate_configurationiguration)
							telegram = Telegram()
							months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
							month = months[now.month - 1]
							name_repository = "Snap_Rotate_" + month + '_' + str(now.year)
							conn_es = elastic.getConnectionElastic()
							list_all_indices = elastic.getIndicesElastic(conn_es)
							list_indices_not_writeables = []
							for index in list_all_indices:
								is_writeable_index = elastic.getIsWriteableIndex(conn_es, index)
								if is_writeable_index == False:
									list_indices_not_writeables.append(index)
							if not len(list_indices_not_writeables) == 0:
								elastic.createRepositoryFS(conn_es, name_repository, snap_rotate_configuration['path_repositories'] + '/' + name_repository)
								self.utils.createSnapRotateLog("\nRepository created: " + name_repository, 1)
								print("\nRepository created: " + name_repository)
								message_creation_end_repository = telegram.getMessageEndCreationRepository(name_repository, snap_rotate_configuration['path_repositories'] + '/' + name_repository)
								telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_configuration['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_configuration['telegram_bot_token']).decode('utf-8'), message_creation_end_repository)
								for index in list_indices_not_writeables:
									print("\nSnapshot creation has started: " + index)
									message_creation_start_snapshot = telegram.getMessageStartCreationSnapshot(index, index, name_repository)
									telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_configuration['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_configuration['telegram_bot_token']).decode('utf-8'), message_creation_start_snapshot)
									elastic.createSnapshot(conn_es, name_repository, index, index)
									while True:
										status_snapshot = elastic.getStatusSnapshot(conn_es, name_repository, index)
										if status_snapshot == 'SUCCESS':
											break
										sleep(60)
									snapshot_info = elastic.getSnapshotInfo(conn_es, name_repository, index)
									self.utils.createSnapRotateLog("Snapshot created: " + index, 1)
									print("\nSnapshot created: " + index)
									message_creation_end_snapshot = telegram.getMessageEndSnapshot(index, name_repository, snapshot_info['snapshots'][0]['start_time'], snapshot_info['snapshots'][0]['end_time'])
									telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_configuration['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_configuration['telegram_bot_token']).decode('utf-8'), message_creation_end_snapshot)
									if snap_rotate_configuration['is_delete_index'] == True:
										elastic.deleteIndex(conn_es, index)
										if not conn_es.indices.exists(index = index):
											self.utils.createSnapRotateLog("Index removed: " + index, 1)
											print("\nIndex removed: " + index)
											message_delete_index = telegram.getMessageDeleteIndex(index)
											telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_configuration['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_configuration['telegram_bot_token']).decode('utf-8'), message_delete_index)
								last_day_month = monthrange(now.year, now.month)[1]
								if now.day == last_day_month:
									if snap_rotate_configuration['is_compress_repository'] == True:
										print("\nCompression of the repository has started...")
										path_repository = snap_rotate_configuration['path_repositories'] + '/' + name_repository + '.tar.gz'
										with open_tf(path_repository, "w:gz") as tar_file:
											tar_file.add(snap_rotate_configuration['path_repositories'] + '/' + name_repository)
										if path.exists(path_repository):
											self.utils.createSnapRotateLog("The repository has been compressed: " + name_repository, 1)
											print("\nThe repository has been compressed: " + name_repository)
											message_compress_repository = telegram.getMessageCompressFile(name_repository, path_repository)
											telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_configuration['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_configuration['telegram_bot_token']).decode('utf-8'), message_compress_repository)
							else:
								print("\nThere are no indexes to store in the repository.")
							conn_es.transport.close()
						sleep(60)
				else:
					print("\nElasticSearch version not supported.")
			else:
				print("\nConfiguration file not found.")
		except KeyError as exception:
			self.utils.createSnapRotateLog("Key Error: " + str(exception), 3)
			print("\nError during the execution of the application. For more information, see the logs.")
			exit(1)