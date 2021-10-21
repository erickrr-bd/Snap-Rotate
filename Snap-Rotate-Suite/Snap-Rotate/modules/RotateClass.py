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
		months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
		snap_rotate_conf = self.utils.readYamlFile(self.utils.getPathSnapRotate("conf") + "/snap_rotate_conf.yaml", 'r')
		try:
			if float(snap_rotate_conf['es_version']) >= 7.0 and float(snap_rotate_conf['es_version']) <= 7.15:
				print("Snap-Rotate v3.0")
				print("@2021 Tekium. All rights reserved.")
				print("Author: Erick Rodriguez")
				print("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com")
				print("License: GPLv3")
				print("\nSnap-Rotate started...")
				time_execute = snap_rotate_conf['time_rotate'].split(':')
				while True:
					now = datetime.now()
					last_day_month = monthrange(now.year, now.month)[1]
					if now.day == last_day_month and (now.hour == int(time_execute[0]) and now.minute == int(time_execute[1])):
						telegram = Telegram()
						elastic = Elastic(snap_rotate_conf)
						month = months[now.month - 2]
						name_repository = "Snap_Rotate_" + month + '_' + str(now.year)
						conn_es = elastic.getConnectionElastic()
						list_all_indices = elastic.getIndicesElastic(conn_es)
						list_indices_not_writeables = []
						for index in list_all_indices:
							is_writeable_index = elastic.getIsWriteableIndex(conn_es, index)
							if is_writeable_index == False:
								list_indices_not_writeables.append(index)
						if not len(list_indices_not_writeables) == 0:
							print("\nRepository creation has started: " + name_repository)
							elastic.createRepositorySnapshot(conn_es, name_repository, snap_rotate_conf['repo_path'] + '/' + name_repository)
							self.utils.createSnapRotateLog("Repository created: " + name_repository, 1)
							print("\nRepository created: " + name_repository)
							message_end_repo = telegram.getMessageEndCreationRepository(name_repository, snap_rotate_conf['repo_path'] + '/' + name_repository)
							telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), message_end_repo)
							if snap_rotate_conf['type_snapshot'] == "Only":
								print("\nThe following indices will be stored in the snapshot:\n")
								print('\n'.join(list_indices_not_writeables))
								indices_to_snapshot = ','.join(list_indices_not_writeables)
								self.utils.createSnapRotateLog("Indices that are stored in the snapshot: " + indices_to_snapshot, 1)
								print("\nSnapshot creation has started: " + name_repository.lower())
								message_creation_start = telegram.getMessageStartCreationSnapshot(indices_to_snapshot, name_repository.lower(), name_repository)
								telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), message_creation_start)
								elastic.createSnapshot(conn_es, name_repository, name_repository.lower(), indices_to_snapshot)
								while True:
									status_snapshot = elastic.getStatusSnapshot(conn_es, name_repository, name_repository.lower())
									if status_snapshot == 'SUCCESS':
										break
									sleep(60)
								snapshot_info = elastic.getSnapshotInfo(conn_es, name_repository, name_repository.lower())
								self.utils.createSnapRotateLog("Snapshot created: " + name_repository.lower(), 1)
								print("\nSnapshot created: " + name_repository.lower())
								message_creation_end = telegram.getMessageEndSnapshot(name_repository.lower(), name_repository, snapshot_info['snapshots'][0]['start_time'], snapshot_info['snapshots'][0]['end_time'])
								telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), message_creation_end)
								if snap_rotate_conf['delete_index'] == True:
									elastic.deleteIndex(conn_es, indices_to_snapshot)
									if not conn_es.indices.exists(index = indices_to_snapshot):
										self.utils.createSnapRotateLog("Indices removed: " + indices_to_snapshot, 1)
										print("\nIndices removed: " + indices_to_snapshot)
										message_delete_index = telegram.getMessageDeleteIndex(indices_to_snapshot)
										telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), message_delete_index)
							elif snap_rotate_conf['type_snapshot'] == "Multiple":
								print("\nThe following indices will be stored in the snapshots:\n")
								print('\n'.join(list_indices_not_writeables))
								for index in list_indices_not_writeables:
									print("\nSnapshot creation has started: " + index)
									message_creation_start = telegram.getMessageStartCreationSnapshot(index, index, name_repository)
									telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), message_creation_start)
									elastic.createSnapshot(conn_es, name_repository, index, index)
									while True:
										status_snapshot = elastic.getStatusSnapshot(conn_es, name_repository, index)
										if status_snapshot == 'SUCCESS':
											break
										sleep(60)
									snapshot_info = elastic.getSnapshotInfo(conn_es, name_repository, index)
									self.utils.createSnapRotateLog("Snapshot created: " + index, 1)
									print("\nSnapshot created: " + index)
									message_creation_end = telegram.getMessageEndSnapshot(index, name_repository, snapshot_info['snapshots'][0]['start_time'], snapshot_info['snapshots'][0]['end_time'])
									telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), message_creation_end)
									if snap_rotate_conf['delete_index'] == True:
										elastic.deleteIndex(conn_es, index)
										if not conn_es.indices.exists(index = index):
											self.utils.createSnapRotateLog("Index removed: " + index, 1)
											print("\nIndex removed: " + index)
											message_delete_index = telegram.getMessageDeleteIndex(indices_to_snapshot)
											telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), message_delete_index)
							conn_es.transport.close()
							if snap_rotate_conf['compress_repo'] == True:
								print("\nCompression of the repository has started...")
								with open_tf(snap_rotate_conf['repo_path'] + '/' + name_repository + '.tar.gz', "w:gz") as tar_file:
									tar_file.add(snap_rotate_conf['repo_path'] + '/' + name_repository)
								self.utils.createSnapRotateLog("The repository has been compressed: " + name_repository, 1)
								print("\nThe repository has been compressed: " + name_repository)
								message_compress_repo = telegram.getMessageCompressFile(snap_rotate_conf['repo_path'] + '/' + name_repository + '.tar.gz')
								telegram.sendTelegramAlert(self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_rotate_conf['telegram_chat_id']).decode('utf-8'), message_compress_repo)
						else:
							self.utils.createSnapRotateLog("There are no indexes to back up", 2)
							print("\nThere are no indexes to back up.")
					sleep(60)
		except KeyError as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nError during the execution of the application. For more information, see the logs.")
			exit(1)