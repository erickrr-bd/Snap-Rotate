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
	Constructor for the Configuration class.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		self.conf_file = self.utils.getPathSnapRotate("conf") + "/snap_rotate_conf.yaml"

	def createConfiguration(self):
		print("Hola")