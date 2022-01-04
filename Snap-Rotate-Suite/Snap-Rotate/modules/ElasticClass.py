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
	Property that saves the data of the Snap-Rotate configuration file.
	"""
	snap_rotate_configuration = None

	"""
	Constructor for the Elastic class.

	Parameters:
	self -- An instantiated object of the Elastic class.
	snap_rotate_configuration -- Object that has the information from the Snap-Rotate configuration file.
	"""
	def __init__(self, snap_rotate_configuration):
		self.utils = Utils()
		self.snap_rotate_configuration = snap_rotate_configuration
		
	"""
	Method that creates a connection object with ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.

	Return:
	conn_es -- Object that contains the connection to ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	exceptions.ConnectionError -- Error raised when there was an exception while talking to ES. 
	exceptions.AuthenticationException -- Exception representing a 401 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	InvalidURL -- The URL provided was somehow invalid.
	"""
	def getConnectionElastic(self):
		conn_es = None
		try:
			if(not self.snap_rotate_configuration['use_ssl_tls'] == True) and (not self.snap_rotate_configuration['use_http_authentication'] == True):
				conn_es = Elasticsearch(self.snap_rotate_configuration['es_host'],
										port = self.snap_rotate_configuration['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
			if(not self.snap_rotate_configuration['use_ssl_tls'] == True) and self.snap_rotate_configuration['use_http_authentication'] == True:
				conn_es = Elasticsearch(self.snap_rotate_configuration['es_host'],
										port = self.snap_rotate_configuration['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(self.snap_rotate_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(self.snap_rotate_configuration['password_http_authentication']).decode('utf-8')),
										use_ssl = False)
			if self.snap_rotate_configuration['use_ssl_tls'] == True and (not self.snap_rotate_configuration['use_http_authentication'] == True):
				if not self.snap_rotate_configuration['validate_certificate_ssl']:
					conn_es = Elasticsearch(self.snap_rotate_configuration['es_host'],
											port = self.snap_rotate_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = self.snap_rotate_configuration['path_certificate_file'])
					conn_es = Elasticsearch(self.snap_rotate_configuration['es_host'],
											port = self.snap_rotate_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if self.snap_rotate_configuration['use_ssl_tls'] == True and self.snap_rotate_configuration['use_http_authentication'] == True:
				if not self.snap_rotate_configuration['validate_certificate_ssl'] == True:
					conn_es = Elasticsearch(self.snap_rotate_configuration['es_host'],
											port = self.snap_rotate_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(self.snap_rotate_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(self.snap_rotate_configuration['password_http_authentication']).decode('utf-8')),
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = self.snap_rotate_configuration['path_certificate_file'])
					conn_es = Elasticsearch(self.snap_rotate_configuration['es_host'],
											port = self.snap_rotate_configuration['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(self.snap_rotate_configuration['user_http_authentication']).decode('utf-8'), self.utils.decryptAES(self.snap_rotate_configuration['password_http_authentication']).decode('utf-8')),
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if not conn_es == None:
				self.utils.createSnapRotateLog("Established connection with: " + self.snap_rotate_configuration['es_host'] + ':' + str(self.snap_rotate_configuration['es_port']), 1)
				self.utils.createSnapRotateLog("Cluster name: " + conn_es.info()['cluster_name'], 1)
				self.utils.createSnapRotateLog("Elasticsearch version: " + conn_es.info()['version']['number'], 1)
		except (KeyError, exceptions.ConnectionError, exceptions.AuthenticationException, exceptions.AuthorizationException, InvalidURL) as exception:
			self.utils.createSnapRotateLog("Failed to connect to ElasticSearch. For more information, see the logs.", 3)
			self.utils.createSnapRotateLog(exception, 3)
			exit(1)
		else:
			return conn_es

	"""
	Method that creates the repository for snapshots.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository.
	path_repository -- Repository path.

	Exceptions:
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES. 
	"""
	def createRepositoryFS(self, conn_es, repository_name, path_repository):
		try:
			conn_es.snapshot.create_repository(repository = repository_name, body = { "type": "fs", "settings": { "location": path_repository, "compress" : True }})
		except (exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.utils.createSnapRotateLog(exception, 3)
			print("\nError creating repository. For more information, see the logs.")
			exit(1)

	"""
	Method that creates a snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository.
	snapshot_name --  Name of the snapshot.
	indices -- List with the names of the indices that will be saved in the snapshot.

	Exceptions:
	exceptions.RequestError -- Exception representing a 400 status code.
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def createSnapshot(self, conn_es, repository_name, snapshot_name, indices):
		try:
			conn_es.snapshot.create(repository = repository_name, snapshot = snapshot_name, body = { "indices" : indices, "include_global_state" : False }, wait_for_completion = False)
		except (exceptions.RequestError, exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.utils.createSnapRotateLog("Failed to create snapshot. For more information, see the logs.", 3)
			self.utils.createSnapRotateLog(exception, 3)
			exit(1)

	"""
	Method that removes an index.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	index_name -- ElasticSearch index name.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError -- Error raised when there was an exception while talking to ES. 
	"""
	def deleteIndex(self, conn_es, index_name):
		try:
			conn_es.indices.delete(index = index_name)
		except (exceptions.AuthorizationException, exceptions.NotFoundError, exceptions.ConnectionError)  as exception:
			self.utils.createSnapRotateLog("Failed to delete index. For more information, see the logs.", 3)
			self.utils.createSnapRotateLog(exception, 3)
			exit(1)

	"""
	Method that gets all the names of the allowed indexes.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.

	Return:
	list_all_indices -- List with the names of the indices found.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError -- Error raised when there was an exception while talking to ES.
	"""
	def getIndicesElastic(self, conn_es):
		try:
			list_all_indices = []
			list_all_indices = conn_es.indices.get(index = '*')
			list_all_indices = sorted([index for index in list_all_indices if not index.startswith('.')])
		except (exceptions.AuthorizationException, exceptions.NotFoundError, exceptions.ConnectionError)  as exception:
			self.utils.createSnapRotateLog("Error getting the indices. For more information, see the logs.", 3)
			self.utils.createSnapRotateLog(exception, 3)
			exit(1)
		else:
			return list_all_indices
			
	"""
	Method that gets if an index is writeable or not.
	
	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	index_name -- ElasticSearch index name.

	Return:
	is_writeable_index -- Whether the index is writeable or not.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError -- Error raised when there was an exception while talking to ES.
	"""
	def getIsWriteableIndex(self, conn_es, index_name):
		try:
			info = conn_es.indices.get(index = index_name)
			aux_var = info[index_name]['aliases']
			for aux in aux_var:
				is_writeable_index = info[index_name]['aliases'][aux]['is_write_index']
		except (exceptions.AuthorizationException, exceptions.NotFoundError, exceptions.ConnectionError)  as exception:
			self.utils.createSnapRotateLog("Error getting index information. For more information, see the logs.", 3)
			self.utils.createSnapRotateLog(exception, 3)
			exit(1)
		else:
			return is_writeable_index

	"""
	Method that gets if the repository exists or not.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository to check whether it exists or not.

	Return:
	Whether or not the repository exists.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError -- Error raised when there was an exception while talking to ES.
	"""
	def getExistsRespositoryFS(self,conn_es, repository_name):
		try:
			conn_es.snapshot.verify_repository(repository = repository_name)
		except (exceptions.AuthorizationException, exceptions.NotFoundError, exceptions.ConnectionError) as exception:
			return False
		else:
			return True

	"""
	Method that obtains the current status of a snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository.
	snapshot_name --  Name of the snapshot.

	Return:
	status_snapshot -- Snapshot status.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def getStatusSnapshot(self, conn_es, repository_name, snapshot_name):
		try:
			info_snapshot = conn_es.snapshot.status(repository = repository_name, snapshot = snapshot_name)
			status_snapshot = info_snapshot['snapshots'][0]['state']
		except (exceptions.NotFoundError, exceptions.ConnectionError) as exception:
			self.utils.createSnapRotateLog("Failed to get snapshot status. For more information, see the logs.", 3)
			self.utils.createSnapRotateLog(exception, 3)
			exit(1)
		else:
			return status_snapshot

	"""
	Method that obtains information about a particular snapshot.

	Parameters:
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshot is saved.
	snapshot_name -- Name of the snapshot from which the information will be obtained.

	Return:
	snapshot_info -- Snapshot information.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def getSnapshotInfo(self, conn_es, repository_name, snapshot_name):
		try:
			snapshot_info = conn_es.snapshot.get(repository = repository_name, snapshot = snapshot_name)
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.utils.createSnapRotateLog("Failed to get snapshot status. For more information, see the logs.", 3)
			self.utils.createSnapRotateLog(exception, 3)
			exit(1)
		else:
			return snapshot_info