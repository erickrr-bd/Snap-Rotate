from os import chmod
from datetime import date
from modules.UtilsClass import Utils
from modules.ElasticClass import Elastic

class Rotate:

	utils = None

	def __init__(self):
		self.utils = Utils()

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
				folder_repositories = "Snap_" + month + '_' + str(today.year)
				#print(folder_repositories)
				#chmod(folder_repositories, 755)
				elastic = Elastic(snap_rotate_conf)
				conn_es = elastic.getConnectionElastic()
				list_all_indices = elastic.getIndicesElastic(conn_es, "winlogbeat-*")
				list_indices_not_writeables = []
				for index in list_all_indices:
					is_writeable_index = elastic.getIsWriteableIndex(conn_es, index)
					if is_writeable_index == False:
						list_indices_not_writeables.append(index)
				if not len(list_indices_not_writeables) == 0:
					print("\nThe following indices will be stored in the snapshot:\n")
					print('\n'.join(list_indices_not_writeables))
				#	elastic.getInfoIndexElastic(conn_es, index)
				#	print('\n')
				#elastic.createRepositorySnapshot(conn_es, 'snap_winlogbeat_september', '/DATA-197/snap_winlog_september')
		else:
			print("\nElasticSearch version not supported by Snap-Rotate.")