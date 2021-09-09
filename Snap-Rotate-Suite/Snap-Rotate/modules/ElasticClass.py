from sys import exit
from datetime import datetime
from modules.UtilsClass import Utils
from ssl import create_default_context
from requests.exceptions import InvalidURL
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions

"""
Class that manages everything related to ElasticSearch.
"""
class Elastic:
	"""
	Property that stores an object of the Utils class.
	"""
	utils = None

	"""
	Property that saves the data of the Snap-Rotate
	configuration file.
	"""
	snap_rotate_conf = None

	"""
	Constructor for the Elastic class.

	Parameters:
	self -- An instantiated object of the Elastic class.
	snap_rotate_conf -- Object that has the information
		 				from the Snap-Rotate configuration
		 				file.
	"""
	def __init__(self, snap_rotate_conf):
		self.utils = Utils()
		self.snap_rotate_conf = snap_rotate_conf
		
	"""
	Method that creates a connection object with ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.

	Return:
	conn_es -- Object that contains the connection to
			   ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is
				raised when you try to access a key that
				isn’t in a dictionary (dict). 
	exceptions.ConnectionError --  Error raised when there
								   was an exception while
								   talking to ES. 
	exceptions.AuthenticationException -- Exception representing
										  a 401 status code.
	exceptions.AuthorizationException -- Exception representing
										 a 403 status code.
	requests.exceptions.InvalidURL -- The URL provided was
									  somehow invalid.
	"""
	def getConnectionElastic(self):
		conn_es = None
		try:
			if(not self.snap_rotate_conf['use_ssl'] == True) and (not self.snap_rotate_conf['use_http_auth'] == True):
				conn_es = Elasticsearch(self.snap_rotate_conf['es_host'],
										port = self.snap_rotate_conf['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
			if(not self.snap_rotate_conf['use_ssl'] == True) and self.snap_rotate_conf['use_http_auth'] == True:
				conn_es = Elasticsearch(self.snap_rotate_conf['es_host'],
										port = self.snap_rotate_conf['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(self.snap_rotate_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(self.snap_rotate_conf['http_auth_pass']).decode('utf-8')),
										use_ssl = False)
			if self.snap_rotate_conf['use_ssl'] == True and (not self.snap_rotate_conf['use_http_auth'] == True):
				if not self.snap_rotate_conf['valid_certificate']:
					conn_es = Elasticsearch(self.snap_rotate_conf['es_host'],
											port = self.snap_rotate_conf['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = self.snap_rotate_conf['path_certificate'])
					conn_es = Elasticsearch(self.snap_rotate_conf['es_host'],
											port = self.snap_rotate_conf['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if self.snap_rotate_conf['use_ssl'] == True and self.snap_rotate_conf['use_http_auth'] == True:
				if not self.snap_rotate_conf['valid_certificate'] == True:
					conn_es = Elasticsearch(self.snap_rotate_conf['es_host'],
											port = self.snap_rotate_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(self.snap_rotate_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(self.snap_rotate_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = self.snap_rotate_conf['path_certificate'])
					conn_es = Elasticsearch(self.snap_rotate_conf['es_host'],
											port = self.snap_rotate_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(self.snap_rotate_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(self.snap_rotate_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if not conn_es == None:
				self.utils.createSnapRotateLog("Established connection with: " + self.snap_rotate_conf['es_host'] + ':' + str(self.snap_rotate_conf['es_port']), 1)
				print("\nCONNECTION DATA:\n")
				print("Cluster name: " + conn_es.info()['cluster_name'])
				print("Elasticsearch version: " + conn_es.info()['version']['number'])
		except (KeyError, exceptions.ConnectionError, exceptions.AuthenticationException, exceptions.AuthorizationException, InvalidURL) as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nFailed to connect to ElasticSearch. For more information, see the logs.")
			exit(1)
		else:
			return conn_es

	"""
	Method that obtains all the names of the indices that
	comply with an index pattern.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to
			   ElasticSearch.
	index_pattern -- ElasticSearch index pattern.

	Return:
	list_all_index -- List with the names of the indices
					  found.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404
								status code.
	exceptions.AuthorizationException -- Exception representing
										 a 403 status code.
	"""
	def getIndicesElastic(self, conn_es, index_pattern):
		try:
			list_all_index = []
			list_all_index = conn_es.indices.get(index_pattern)
		except (exceptions.AuthorizationException, exceptions.NotFoundError)  as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nError getting the indices. For more information, see the logs.")
		else:
			return list_all_index

	"""
	Method that gets if an index is writeable or not.
	
	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to
			   ElasticSearch.
	index_name -- ElasticSearch index name.

	Return:
	is_writeable_index -- Whether the index is writeable or
						  not.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404
								status code.
	exceptions.AuthorizationException -- Exception representing
										 a 403 status code.
	"""
	def getIsWriteableIndex(self, conn_es, index_name):
		try:
			info = conn_es.indices.get(index_name)
			aux_var = info[index_name]['aliases']
			for aux in aux_var:
				is_writeable_index = info[index_name]['aliases'][aux]['is_write_index']
		except (exceptions.AuthorizationException, exceptions.NotFoundError)  as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nError getting index information. For more information, see the logs.")
		else:
			return is_writeable_index

	"""
	Method that removes an index.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to
			   ElasticSearch.
	index_name -- ElasticSearch index name.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404
								status code.
	exceptions.AuthorizationException -- Exception representing
										 a 403 status code.
	"""
	def deleteIndex(self, conn_es, index_name):
		try:
			conn_es.indices.delete(index = index_name)
		except (exceptions.AuthorizationException, exceptions.NotFoundError)  as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nFailed to delete index. For more information, see the logs.")

	"""
	Method that creates the repository for snapshots.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to
			   ElasticSearch.
	repository_name -- Name of the repository.
	path_repository -- Repository path.

	Exceptions:
	exceptions.AuthorizationException -- Exception representing
										 a 403 status code.
	"""
	def createRepositorySnapshot(self, conn_es, repository_name, path_repository):
		try:
			conn_es.snapshot.create_repository(repository_name, body = { "type": "fs", "settings": { "location": path_repository, "compress" : True }})
		except (exceptions.AuthorizationException) as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nError creating repository. For more information, see the logs.")
			exit(1)

	"""
	Method that creates a snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to
			   ElasticSearch.
	repository_name -- Name of the repository.
	snapshot_name --  Name of the snapshot.
	indices -- List with the names of the indices that will}
	 		   be saved in the snapshot.

	Exceptions:
	exceptions.RequestError -- Exception representing a 400
							   status code.
	exceptions.NotFoundError -- Exception representing a 404
								status code.
	exceptions.AuthorizationException -- Exception representing
										 a 403 status code.
	"""
	def createSnapshot(self, conn_es, repository_name, snapshot_name, indices):
		try:
			conn_es.snapshot.create(repository = repository_name,
									snapshot = snapshot_name,
									body = { "indices" : indices, "include_global_state" : False },
									wait_for_completion = False)
		except (exceptions.RequestError, exceptions.NotFoundError, exceptions.AuthorizationException) as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nFailed to create snapshot. For more information, see the logs.")
			exit(1)

	"""
	Method that obtains the current status of a snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to
			   ElasticSearch.
	repository_name -- Name of the repository.
	snapshot_name --  Name of the snapshot.

	Return:
	status_snapshot -- Snapshot status.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404
								status code.
	"""
	def getStatusSnapshot(self, conn_es, repository_name, snapshot_name):
		try:
			info_snapshot = conn_es.snapshot.status(repository = repository_name,
													snapshot = snapshot_name)
			status_snapshot = info_snapshot['snapshots'][0]['state']
		except (exceptions.NotFoundError) as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nFailed to create snapshot. For more information, see the logs.")
		else:
			return status_snapshot