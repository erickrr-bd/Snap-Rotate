from datetime import datetime
from modules.UtilsClass import Utils

"""
Class that manages everything related to the Inv-Alert
configuration.
"""
class Configuration:
	"""
	Property that stores an object of type FormDialogs.
	"""
	form_dialog = None

	"""
	Property that stores the path of the configuration file.
	"""
	conf_file = None

	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores the options for how often the
	inventory will be fetched.
	"""
	options_frequency_rotation = [["Weekly", "Weekly rotation", 0],
								  ["Monthly", "Monthly rotation", 0]]

	"""
	Constructor for the Configuration class.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		self.conf_file = self.utils.getPathSnapRotate("conf") + "/snap_rotate_conf.yaml"

	"""
	Method where all the necessary information for the
	configuration of Snap-Rotate is defined.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def createConfiguration(self):
		data_conf = []
		now = datetime.now()
		version_es = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", "7.14")
		host_es = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", "localhost")
		port_es = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", "9200")
		data_conf.append(version_es)
		data_conf.append(host_es)
		data_conf.append(port_es)
		use_ssl = self.form_dialog.getDataYesOrNo("\nDo you want Inv-Alert to connect to ElasticSearch using the SSL/TLS protocol?", "Connection Via SSL/TLS")
		if use_ssl == "ok":
			data_conf.append(True)
			valid_certificate = self.form_dialog.getDataYesOrNo("\nDo you want the certificate for SSL/TLS communication to be validated?", "Certificate Validation")
			if valid_certificate == "ok":
				data_conf.append(True)
				cert_file = self.form_dialog.getFile('/etc/Inv-Alert-Suite/Inv-Alert', "Select the CA certificate:")
				data_conf.append(cert_file)
			else:
				data_conf.append(False)
		else:
			data_conf.append(False)
		http_auth = self.form_dialog.getDataYesOrNo("\nIs it required to enable the use of HTTP authentication to connect to ElasticSearch?", "HTTP Authentication")
		if http_auth == "ok":
			data_conf.append(True)
			user_http_auth = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
			pass_http_auth = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
			data_conf.append(user_http_auth.decode('utf-8'))
			data_conf.append(pass_http_auth.decode('utf-8'))
		else:
			data_conf.append(False)
		repo_path = self.form_dialog.getDirectory("/etc/Snap-Rotate-Suite", "Repositories Path")
		frequency_rotation = self.form_dialog.getDataRadioList("Select a option:", self.options_frequency_rotation, "Repository Rotation Frequency")
		time_daily_execution = self.form_dialog.getDataTime("Choose the daily time to validate:", now.hour, now.minute)
		data_conf.append(repo_path)
		data_conf.append(frequency_rotation)
		data_conf.append(str(time_daily_execution[0]) + ':' + str(time_daily_execution[1]))
		print(data_conf)


	"""
	Method that creates the YAML file where the configuration
	is stored.

	Parameters:
	self -- An instantiated object of the Configuration class.
	data_conf -- Variable where all the information related to
				 the configuration is stored.
	"""
	def createFileConfiguration(self, data_conf):
		data_json = {'es_version' : data_conf[0],
					'es_host' : data_conf[1],
					'es_port' : int(data_conf[2]),
					'use_ssl' : data_conf[3]}
		
		if data_conf[3] == True:
			if data_conf[4] == True:
				valid_cert_json = { 'valid_certificate' : data_conf[4], 'path_certificate' : data_conf[5] }
				last_index = 5
			else:
				valid_cert_json = { 'valid_certificate' : data_conf[4] }
				last_index = 4
			data_json.update(valid_cert_json)
		else:
			last_index = 3

		if data_conf[last_index + 1] == True:
			http_auth_json = { 'use_http_auth' : data_conf[last_index + 1], 'http_auth_user' : data_conf[last_index + 2], 'http_auth_pass' : data_conf[last_index + 3] }
			last_index += 3
		else:
			http_auth_json = { 'use_http_auth' : data_conf[last_index + 1] }
			last_index += 1
		data_json.update(http_auth_json)
		aux_json = { 'repo_path' : data_conf[last_index + 1], 'frequency_rotation' : data_conf[last_index + 2], 'time_execution' : data_conf[last_index + 3] } 
		data_json.update(aux_json)

		self.utils.createYamlFile(data_json, self.conf_file, 'w')