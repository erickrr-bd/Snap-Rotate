from sys import exit
from time import sleep
from datetime import datetime
from tarfile import open as open_tf
from modules.UtilsClass import Utils
from modules.ElasticClass import Elastic

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
			if float(snap_rotate_conf['es_version']) >= 7.0 and float(snap_rotate_conf['es_version']) <= 7.14:
				print("Snap-Rotate v3.0")
				print("@2021 Tekium. All rights reserved.")
				print("Author: Erick Rodriguez")
				print("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com")
				print("License: GPLv3")
				print("\nSnap-Rotate started...")
				time_execute = snap_rotate_conf['time_rotate'].split(':')
				while True:
					now = datetime.now()
					if now.day == snap_rotate_conf['day_rotate']:
						month = months[now.month - 1]
						name_repository = "Snap_" + month + '_' + str(now.year)
						print(name_repository)
						elastic = Elastic(snap_rotate_conf)
						conn_es = elastic.getConnectionElastic()
						list_all_indices = elastic.getIndicesElastic(conn_es)
						list_indices_not_writeables = []
						for index in list_all_indices:
							is_writeable_index = elastic.getIsWriteableIndex(conn_es, index)
							if is_writeable_index == False:
								list_indices_not_writeables.append(index)
						if not len(list_indices_not_writeables) == 0:
							print("\nCreating the repository ...")
							elastic.createRepositorySnapshot(conn_es, name_repository, snap_rotate_conf['repo_path'] + '/' + name_repository)
							self.utils.createSnapRotateLog("Repository created: " + name_repository, 1)
							print("\nRepository created: " + name_repository)
							if snap_rotate_conf['type_snapshot'] == "Only":
								print("\nThe following indices will be stored in the snapshot:\n")
								print('\n'.join(list_indices_not_writeables))
								indices_to_snapshot = ','.join(list_indices_not_writeables)
								self.utils.createSnapRotateLog("Indices that are stored in the snapshot: " + indices_to_snapshot, 1)
								elastic.createSnapshot(conn_es, name_repository, name_repository.lower(), indices_to_snapshot)
								while True:
									status_snapshot = elastic.getStatusSnapshot(conn_es, name_repository, name_repository.lower())
									if status_snapshot == 'SUCCESS':
										break
									sleep(60)
								self.utils.createSnapRotateLog("Snapshot created: " + name_repository.lower(), 1)
								print("\nSnapshot created: " + name_repository.lower())
								elastic.deleteIndex(conn_es, indices_to_snapshot)
								if not conn_es.indices.exists(index = indices_to_snapshot):
									self.utils.createSnapRotateLog("Indices removed: " + indices_to_snapshot, 1)
									print("\nIndices removed: " + indices_to_snapshot)
							elif snap_rotate_conf['type_snapshot'] == "Multiple":
								print("\nThe following indices will be stored in the snapshots:\n")
								print('\n'.join(list_indices_not_writeables))
								for index in list_indices_not_writeables:
									elastic.createSnapshot(conn_es, name_repository, index, index)
									while True:
										status_snapshot = elastic.getStatusSnapshot(conn_es, name_repository, index)
										if status_snapshot == 'SUCCESS':
											break
										sleep(60)
									self.utils.createSnapRotateLog("Snapshot created: " + index, 1)
									print("\nSnapshot created: " + index)
									elastic.deleteIndex(conn_es, index)
									if not conn_es.indices.exists(index = index):
										self.utils.createSnapRotateLog("Index removed: " + index, 1)
										print("\nIndex removed: " + index)
							with open_tf(snap_rotate_conf['repo_path'] + '/' + name_repository + '.tar.gz', "w:gz") as tar_file:
								tar_file.add(snap_rotate_conf['repo_path'] + '/' + name_repository)
							self.utils.createSnapRotateLog("The repository has been compressed: " + name_repository, 1)
							print("\nThe repository has been compressed: " + name_repository)
						else:
							self.utils.createSnapRotateLog("There are no indexes to back up", 2)
							print("\nThere are no indexes to back up.")
					sleep(60)
		except KeyError as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nError during the execution of the application. For more information, see the logs.")
			exit(1)