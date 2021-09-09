from os import chmod
from time import sleep
from datetime import date
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
		if float(snap_rotate_conf['es_version']) >= 7.0 and float(snap_rotate_conf['es_version']) <= 7.14:
			print("Snap-Rotate v3.0")
			print("@2021 Tekium. All rights reserved.")
			print("Author: Erick Rodriguez")
			print("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com")
			print("License: GPLv3")
			print("\nSnap-Rotate started...")
			today = date.today()
			if today.day == snap_rotate_conf['date_rotate']:
				month = months[today.month - 1]
				name_repository = "Snap_" + month + '_' + str(today.year)
				#print(folder_repositories)
				#chmod(folder_repositories, 755)
				elastic = Elastic(snap_rotate_conf)
				conn_es = elastic.getConnectionElastic()
				print("\nCreating the repository ...")
				elastic.createRepositorySnapshot(conn_es, name_repository, "/DATA-197/" + name_repository)
				self.utils.createSnapRotateLog("\nRepository created: " + name_repository, 1)
				print("\nRepository created: " + name_repository)
				list_all_indices = elastic.getIndicesElastic(conn_es, "winlogbeat-*")
				list_indices_not_writeables = []
				for index in list_all_indices:
					is_writeable_index = elastic.getIsWriteableIndex(conn_es, index)
					if is_writeable_index == False:
						list_indices_not_writeables.append(index)
				if not len(list_indices_not_writeables) == 0:
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
				else:
					self.utils.createSnapRotateLog("There are no indexes to back up", 2)
					print("\nThere are no indexes to back up.")
				
		else:
			self.utils.createSnapRotateLog("ElasticSearch version not supported by Snap-Rotate", 2)
			print("\nElasticSearch version not supported by Snap-Rotate.")