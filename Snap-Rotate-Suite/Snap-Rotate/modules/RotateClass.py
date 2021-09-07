from modules.UtilsClass import Utils
from modules.ElasticClass import Elastic

class Rotate:

	utils = None

	def __init__(self):
		self.utils = Utils()

	def startSnapRotate(self):
		snap_rotate_conf = self.utils.readYamlFile(self.utils.getPathSnapRotate("conf") + "/snap_rotate_conf.yaml", 'r')
		if float(snap_rotate_conf['es_version']) >= 7.0 and float(snap_rotate_conf['es_version']) <= 7.14:
			print("Snap-Rotate v3.0")
			print("@2021 Tekium. All rights reserved.")
			print("Author: Erick Rodriguez")
			print("Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com")
			print("License: GPLv3\n")
			print("Snap-Rotate started...")
			elastic = Elastic(snap_rotate_conf)
			conn_es = elastic.getConnectionElastic()
			list_all_indices = elastic.getIndicesElastic(conn_es)
			for index in list_all_indices:
				elastic.getInfoIndexElastic(conn_es, index)
				print('\n')
			#elastic.createRepositorySnapshot(conn_es, 'snap_winlogbeat_september', '/DATA-197/snap_winlog_september')
		else:
			print("No soportada")