from os import path
from modules.UtilsClass import Utils

"""
Class that manages everything related to the Snap-Rotate configuration.
"""
class Configuration:
	"""
	Property that stores an object of type FormDialog.
	"""
	form_dialog = None

	"""
	Property that stores the path of the configuration file.
	"""
	path_configuration_file = None

	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Constructor for the Configuration class.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		self.path_configuration_file = self.utils.getPathSnapRotate("conf") + "/snap_rotate_conf.yaml"

	"""
	Method that defines the information that will be stored in the configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def createConfiguration(self):
		data_configuration = []
		es_version = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", "7.16")
		data_configuration.append(es_version)
		es_host = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", "localhost")
		data_configuration.append(es_host)
		es_port = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", "9200")
		data_configuration.append(es_port)
		use_ssl_tls = self.form_dialog.getDataYesOrNo("\nDo you require Snap-Rotate to communicate with ElasticSearch using the SSL/TLS protocol?", "SSL/TLS Connection")
		if use_ssl_tls == "ok":
			data_configuration.append(True)
			validate_certificate_ssl = self.form_dialog.getDataYesOrNo("\nDo you require Snap-Rotate to validate the SSL certificate?", "Certificate Validation")
			if validate_certificate_ssl == "ok":
				data_configuration.append(True)
				path_certificate_file = self.form_dialog.getFile("/etc/Snap-Rotate-Suite/Snap-Rotate", "Select the CA certificate:", ".pem")
				data_configuration.append(path_certificate_file)
			else:
				data_configuration.append(False)
		else:
			data_configuration.append(False)
		use_http_authentication = self.form_dialog.getDataYesOrNo("\nIs it required to enable the use of HTTP authentication to connect to ElasticSearch?", "HTTP Authentication")
		if use_http_authentication == "ok":
			data_configuration.append(True)
			user_http_authentication = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
			data_configuration.append(user_http_authentication.decode('utf-8'))
			password_http_authentication = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
			data_configuration.append(password_http_authentication.decode('utf-8'))
		else:
			data_configuration.append(False)
		path_repositories = self.form_dialog.getDirectory("/etc/Snap-Rotate-Suite", "Repositories Path")
		path_repositories = path_repositories.rstrip('/')
		data_configuration.append(path_repositories)
		time_execution_rotate = self.form_dialog.getDataTime("Choose the time the snapshot will be created:", -1, -1)
		data_configuration.append(str(time_execution_rotate[0]) + ':' + str(time_execution_rotate[1]))
		is_delete_index = self.form_dialog.getDataYesOrNo("\nWill the indexes stored in the snapshot(s) be automatically deleted?", "Remove Indices")
		if is_delete_index == "ok":
			data_configuration.append(True)
		else:
			data_configuration.append(False)
		is_compress_repository = self.form_dialog.getDataYesOrNo("\nDo you require that the repository created be compressed into a file?", "Repository Compression")
		if is_compress_repository == "ok":
			data_configuration.append(True)
		else:
			data_configuration.append(False)
		telegram_bot_token = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
		data_configuration.append(telegram_bot_token.decode('utf-8'))
		telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
		data_configuration.append(telegram_chat_id.decode('utf-8'))
		self.createFileConfiguration(data_configuration)
		if path.exists(self.path_configuration_file):
			self.utils.createSnapRotateToolLog("Configuration file created", 1)
			self.form_dialog.d.msgbox(text = "\nConfiguration file created.", height = 7, width = 50, title = "Notification Message")
		else:
			self.form_dialog.d.msgbox(text = "\nError creating configuration file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that allows modifying one or more values assigned in the configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a  dictionary (dict). 
	"""
	def updateConfiguration(self):
		list_fields_update = [("Version", "ElasticSearch Version", 0),
							  ("Host", "ElasticSearch Host", 0),
							  ("Port", "ElasticSearch Port", 0),
							  ("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
						 	  ("HTTP Authentication", "Enable or disable HTTP authentication", 0),
							  ("Path", "Repositories path", 0),
							  ("Time", "Time at which it runs", 0),
							  ("Remove Index", "Delete indexes automatically", 0),
							  ("Compression", "Compress the repository", 0),
							  ("Bot Token", "Telegram bot token", 0),
							  ("Chat ID", "Telegram channel identifier", 0)]

		list_ssl_tls_true = [("Disable", "Disable SSL/TLS communication", 0),
							 ("Certificate Validation", "Modify certificate validation", 0)]

		list_ssl_tls_false = [("Enable", "Enable SSL/TLS communication", 0)]

		list_validate_certificate_true = [("Disable", "Disable certificate validation", 0),
									      ("Certificate File", "Change certificate file", 0)]

		list_validate_certificate_false = [("Enable", "Enable certificate validation", 0)]

		list_http_authentication_true = [("Disable", "Disable HTTP authentication", 0),
								   	     ("Data", "Modify HTTP authentication data", 0)]

		list_http_authentication_false = [("Enable", "Enable HTTP authentication", 0)]

		list_http_authentication_data = [("Username", "Username for HTTP authentication", 0),
								 		 ("Password", "User password", 0)]

		list_is_remove_index_true = [("Disable", "Disable automatic index removal", 0)]

		list_is_remove_index_false = [("Enable", "Enable automatic index removal", 0)]

		list_is_compress_repository_true = [("Disable", "Disable repository compression", 0)]

		list_is_compress_repository_false = [("Enable", "Enable repository compression", 0)]

		flag_es_version = 0
		flag_es_host = 0
		flag_es_port = 0
		flag_use_ssl_tls = 0
		flag_use_http_authentication = 0
		flag_path_repositories = 0
		flag_time_execution_rotate = 0
		flag_is_delete_index = 0
		flag_is_compress_repository = 0
		flag_telegram_bot_token = 0
		flag_telegram_chat_id = 0
		options_fields_update = self.form_dialog.getDataCheckList("Select one or more options:", list_fields_update, "Configuration File Fields")
		for option in options_fields_update:
			if option == "Version":
				flag_es_version = 1
			elif option == "Host":
				flag_es_host = 1
			elif option == "Port":
				flag_es_port = 1
			elif option == "SSL/TLS":
				flag_use_ssl_tls = 1
			elif option == "HTTP Authentication":
				flag_use_http_authentication = 1
			elif option == "Path":
				flag_path_repositories = 1
			elif option == "Time":
				flag_time_execution_rotate = 1
			elif option == "Remove Index":
				flag_is_delete_index = 1
			elif option == "Compression":
				flag_is_compress_repository = 1
			elif option == "Bot Token":
				flag_telegram_bot_token = 1
			elif option == "Chat ID":
				flag_telegram_chat_id = 1
		try:
			data_configuration = self.utils.readYamlFile(self.path_configuration_file, 'rU')
			hash_configuration_file_original = self.utils.getHashToFile(self.path_configuration_file)
			if flag_es_version == 1:
				es_version = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", data_configuration['es_version'])
				data_configuration['es_version'] = es_version
			if flag_es_host == 1:
				es_host = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", data_configuration['es_host'])
				data_configuration['es_host'] = es_host
			if flag_es_port == 1:
				port_es = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", str(data_configuration['es_port']))
				data_configuration['es_port'] = int(port_es)
			if flag_use_ssl_tls == 1:
				if data_configuration['use_ssl_tls'] == True:
					option_ssl_tls_true = self.form_dialog.getDataRadioList("Select a option:", list_ssl_tls_true, "SSL/TLS Connection")
					if option_ssl_tls_true == "Disable":
						data_configuration['use_ssl_tls'] = False
						del data_configuration['validate_certificate_ssl']
						if 'path_certificate_file' in data_configuration:
							del data_configuration['path_certificate_file']
					elif option_ssl_tls_true == "Certificate Validation":
						if data_configuration['validate_certificate_ssl'] == True:
							option_validate_certificate_true = self.form_dialog.getDataRadioList("Select a option:", list_validate_certificate_true, "Certificate Validation")
							if option_validate_certificate_true == "Disable":
								data_configuration['validate_certificate_ssl'] = False
								del data_configuration['path_certificate_file']
							elif option_validate_certificate_true == "Certificate File":
								path_certificate_file = self.form_dialog.getFile(data_configuration['path_certificate_file'], "Select the CA certificate:", ".pem")
								data_configuration['path_certificate_file'] = path_certificate_file
						else:
							option_validate_certificate_false = self.form_dialog.getDataRadioList("Select a option:", list_validate_certificate_false, "Certificate Validation")
							if option_validate_certificate_false == "Enable":
								data_configuration['validate_certificate_ssl'] = True
								path_certificate_file = self.form_dialog.getFile('/etc/Snap-Rotate-Suite/Snap-Rotate', "Select the CA certificate:", ".pem")
								validate_certificate_ssl_json = { 'path_certificate_file' : path_certificate_file }
								data_configuration.update(validate_certificate_ssl_json)
				else:
					option_ssl_tls_false = self.form_dialog.getDataRadioList("Select a option:", list_ssl_tls_false, "SSL/TLS Connection")
					if option_ssl_tls_false == "Enable":
						data_configuration['use_ssl_tls'] = True
						validate_certificate_ssl = self.form_dialog.getDataYesOrNo("\nDo you require Snap-Rotate to validate the SSL certificate?", "Certificate Validation")
						if validate_certificate_ssl == "ok":
							path_certificate_file = self.form_dialog.getFile('/etc/Snap-Rotate-Suite/Snap-Rotate', "Select the CA certificate:", ".pem")
							validate_certificate_ssl_json = { 'validate_certificate_ssl' : True, 'path_certificate_file' : path_certificate_file }
						else:
							validate_certificate_ssl_json = { 'validate_certificate_ssl' : False}
						data_configuration.update(validate_certificate_ssl_json)
			if flag_use_http_authentication == 1:
				if data_configuration['use_http_authentication'] == True:
					option_http_authentication_true = self.form_dialog.getDataRadioList("Select a option:", list_http_authentication_true, "HTTP Authentication")
					if option_http_authentication_true == "Disable":
						data_configuration['use_http_authentication'] = False
						del data_configuration['user_http_authentication']
						del data_configuration['password_http_authentication']
					elif option_http_authentication_true == "Data":
						flag_username_http_authentication = 0
						flag_password_http_authentication = 0
						options_http_authentication_data = self.form_dialog.getDataCheckList("Select one or more options:", list_http_authentication_data, "HTTP Authentication")
						for option in options_http_authentication_data:
							if option == "Username":
								flag_username_http_authentication = 1
							elif option == "Password":
								flag_password_http_authentication = 1
						if flag_username_http_authentication == 1:
							user_http_authentication = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
							data_configuration['user_http_authentication'] =  user_http_authentication.decode('utf-8')
						if flag_password_http_authentication == 1:
							password_http_authentication = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
							data_configuration['password_http_authentication'] = password_http_authentication.decode('utf-8')
				else:
					option_http_authentication_false = self.form_dialog.getDataRadioList("Select a option:", list_http_authentication_false, "HTTP Authentication")
					if option_http_authentication_false == "Enable":
						data_configuration['use_http_authentication'] = True
						user_http_authentication = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
						password_http_authentication = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
						http_authentication_json = { 'user_http_authentication' : user_http_authentication.decode('utf-8'), 'password_http_authentication' : password_http_authentication.decode('utf-8') }
						data_configuration.update(http_authentication_json)
			if flag_path_repositories == 1:
				path_repositories = self.form_dialog.getDirectory(data_configuration['path_repositories'], "Repositories Path")
				data_configuration['path_repositories'] = path_repositories
			if flag_time_execution_rotate == 1:
				time_execution_rotate_actual = data_configuration['time_execution_rotate'].split(':')
				time_execution_rotate = self.form_dialog.getDataTime("Choose the time the snapshot will be created:", int(time_execution_rotate_actual[0]), int(time_execution_rotate_actual[1]))
				data_configuration['time_execution_rotate'] = str(time_execution_rotate[0]) + ':' + str(time_execution_rotate[1])
			if flag_is_delete_index == 1:
				if data_configuration['is_delete_index'] == True:
					option_is_remove_index_true = self.form_dialog.getDataRadioList("Select a option:", list_is_remove_index_true, "Remove Indices")
					if option_is_remove_index_true == "Disable":
						data_configuration['is_delete_index'] = False
				else:
					option_is_remove_index_false = self.form_dialog.getDataRadioList("Select a option:", list_is_remove_index_false, "Remove Indices")
					if option_is_remove_index_false == "Enable":
						data_configuration['is_delete_index'] = True
			if flag_is_compress_repository == 1:
				if data_configuration['is_compress_repository'] == True:
					option_is_compress_repository_true = self.form_dialog.getDataRadioList("Select a option:", list_is_compress_repository_true, "Repository Compression")
					if option_is_compress_repository_true == "Disable":
						data_configuration['is_compress_repository'] = False
				else:
					option_is_compress_repository_false = self.form_dialog.getDataRadioList("Select a option:", list_is_compress_repository_false, "Repository Compression")
					if option_is_compress_repository_false == "Enable":
						data_configuration['is_compress_repository'] = True
			if flag_telegram_bot_token == 1:
				telegram_bot_token = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram bot token:", self.utils.decryptAES(data_configuration['telegram_bot_token']).decode('utf-8')))
				data_configuration['telegram_bot_token'] = telegram_bot_token.decode('utf-8')
			if flag_telegram_chat_id == 1:
				telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", self.utils.decryptAES(data_configuration['telegram_chat_id']).decode('utf-8')))
				data_configuration['telegram_chat_id'] = telegram_chat_id.decode('utf-8')
			self.utils.createYamlFile(data_configuration, self.path_configuration_file, 'w')
			hash_configuration_file_new = self.utils.getHashToFile(self.path_configuration_file)
			if hash_configuration_file_new == hash_configuration_file_original:
				self.form_dialog.d.msgbox(text = "\nThe configuration file was not modified.", height = 7, width = 50, title = "Notification Message")
			else:
				self.utils.createSnapRotateToolLog("The configuration file was modified", 1)
				self.form_dialog.d.msgbox(text = "\nThe configuration file was modified.", height = 7, width = 50, title = "Notification Message")
			self.form_dialog.mainMenu()
		except KeyError as exception:
			self.utils.createSnapRotateToolLog("Key Error: " + str(exception), 3)
			self.form_dialog.d.msgbox(text = "\nError modifying the configuration file. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that creates the YAML file with the data entered for the Snap-Rotate configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	data_configuration -- Object where the information to be stored in the configuration file is located.
	"""
	def createFileConfiguration(self, data_configuration):
		data_configuration_json = {'es_version' : data_configuration[0],
								   'es_host' : data_configuration[1],
								   'es_port' : int(data_configuration[2]),
								   'use_ssl_tls' : data_configuration[3]}
		
		if data_configuration[3] == True:
			if data_configuration[4] == True:
				validate_certificate_ssl_json = { 'validate_certificate_ssl' : data_configuration[4], 'path_certificate_file' : data_configuration[5] }
				last_index = 5
			else:
				validate_certificate_ssl_json = { 'validate_certificate_ssl' : data_configuration[4] }
				last_index = 4
			data_configuration_json.update(validate_certificate_ssl_json)
		else:
			last_index = 3

		if data_configuration[last_index + 1] == True:
			http_authentication_json = { 'use_http_authentication' : data_configuration[last_index + 1], 'user_http_authentication' : data_configuration[last_index + 2], 'password_http_authentication' : data_configuration[last_index + 3] }
			last_index += 3
		else:
			http_authentication_json = { 'use_http_authentication' : data_configuration[last_index + 1] }
			last_index += 1
		data_configuration_json.update(http_authentication_json)
		auxiliar_data_json = { 'path_repositories' : data_configuration[last_index + 1], 'time_execution_rotate' : data_configuration[last_index + 2], 'is_delete_index' : data_configuration[last_index + 3], 'is_compress_repository' : data_configuration[last_index + 4], 'telegram_bot_token' : data_configuration[last_index + 5], 'telegram_chat_id' : data_configuration[last_index + 6] } 
		data_configuration_json.update(auxiliar_data_json)

		self.utils.createYamlFile(data_configuration_json, self.path_configuration_file, 'w')