from os import path
from sys import exit
from dialog import Dialog
from modules.UtilsClass import Utils
from modules.ConfigurationClass import Configuration

"""
Class that allows managing all the graphical interfaces
of the application.
"""
class FormDialog:
	"""
	Property that stores an object of type Dialog.
	"""
	d = None

	"""
	Constructor for the FormDialogs class.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def __init__(self):
		self.utils = Utils(self)
		self.d = Dialog(dialog = "dialog")
		self.d.set_background_title("SNAP-ROTATE-TOOL")

	"""
	Method that generates the menu interface.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	options -- List of options that make up the menu.
	title -- Title displayed on the interface.

	Return:
	tag_mm -- Chosen option.
	"""
	def getMenu(self, options, title):
		code_mm, tag_mm = self.d.menu("Choose an option:", choices = options, title = title)
		if code_mm == self.d.OK:
			return tag_mm
		if code_mm == self.d.CANCEL:
			exit(0)

	"""
	Method that generates an interface with several
	available options, and where only one of them can be
	chosen.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	options -- List of options that make up the interface.
	title -- Title displayed on the interface.

	Return:
	tag_rl -- Chosen option.
	"""
	def getDataRadioList(self, text, options, title):
		while True:
			code_rl, tag_rl = self.d.radiolist(
					  text,
					  width = 65,
					  choices = options,
					  title = title)
			if code_rl == self.d.OK:
				if len(tag_rl) == 0:
					self.d.msgbox("\nSelect at least one option.", 7, 50, title = "Error Message")
				else:
					return tag_rl
			if code_rl == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that launches an action based on the option
	chosen in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	option -- Chosen option.
	"""
	def switchMmenu(self, option):
		if option == 1:
			self.defineConfiguration()
		if option == 2:
			self.serviceMenu()
		if option == 3:
			self.getAbout()
		if option == 4:
			exit(0)

	"""
	Method that defines the action to be performed on the
	Snap-Rotate configuration file (creation or modification).

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def defineConfiguration(self):
		configuration = Configuration()

		options_conf_false = [("Create", "Create the configuration file", 0)]

		options_conf_true = [("Modify", "Modify the configuration file", 0)]
		
		try:
			if not path.exists(self.configuration.conf_file):
				opt_conf_false = self.getDataRadioList("Select a option:", options_conf_false, "Configuration Options")
				if opt_conf_false == "Create":
					self.configuration.createConfiguration()
			else:
				opt_conf_true = self.getDataRadioList("Select a option:", options_conf_true, "Configuration Options")
				if opt_conf_true == "Modify":
					self.configuration.updateConfiguration()
		except TypeError as exception:
			self.utils.createSnapToolLog(exception, 3)
			self.d.msgbox("\nAn error has occurred. For more information, see the logs.", 8, 50, title = "Error Message")
			self.mainMenu()

	"""
	Method that defines the menu on the actions to be
	carried out in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def mainMenu(self):
		options_mm = [("1", "Snap-Rotate Configuration"),
					  ("2", "Snap-Rotate Service"),
					  ("3", "About"),
					  ("4", "Exit")]

		option_mm = self.getMenu(options_mm, "Main Menu")
		self.switchMmenu(int(option_mm))