from os import path
from sys import exit
from pathlib import Path
from dialog import Dialog
from re import compile as re_compile
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
	Method that generates the interface for entering decimal
	or floating type data.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_nd -- Decimal or float value entered.
	"""
	def getDataNumberDecimal(self, text, initial_value):
		decimal_reg_exp = re_compile(r'^[1-9](\.[0-9]+)?$')
		while True:
			code_nd, tag_nd = self.d.inputbox(text, 10, 50, initial_value)
			if code_nd == self.d.OK:
				if(not self.utils.validateRegularExpression(decimal_reg_exp, tag_nd)):
					self.d.msgbox("\nInvalid data entered. Required value (decimal or float).", 8, 50, title = "Error Message")
				else:
					return tag_nd
			if code_nd == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter an IP
	address.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_ip -- IP address entered.
	"""
	def getDataIP(self, text, initial_value):
		ip_reg_exp = re_compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
		while True:
			code_ip, tag_ip = self.d.inputbox(text, 10, 50, initial_value)
			if code_ip == self.d.OK:
				if(not self.utils.validateRegularExpression(ip_reg_exp, tag_ip)):
					self.d.msgbox("\nInvalid data entered. Required value (IP address).", 8, 50, title = "Error Message")
				else:
					return tag_ip
			if code_ip == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter a port.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_port -- Port entered.
	"""
	def getDataPort(self, text, initial_value):
		port_reg_exp = re_compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_port, tag_port = self.d.inputbox(text, 10, 50, initial_value)
			if code_port == self.d.OK:
				if(not self.utils.validateRegularExpression(port_reg_exp, tag_port)):
					self.d.msgbox("\nInvalid data entered. Required value (0 - 65535).", 8, 50, title = "Error Message")
				else:
					return tag_port
			if code_port == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter text.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_input -- Text entered.
	"""
	def getDataInputText(self, text, initial_value):
		while True:
			code_input, tag_input = self.d.inputbox(text, 10, 50, initial_value)
			if code_input == self.d.OK:
				if tag_input == "":
					self.d.msgbox("\nInvalid data entered. Required value (not empty).", 8, 50, title = "Error Message")
				else:
					return tag_input
			if code_input == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter a password.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_pass -- Password entered.
	"""
	def getDataPassword(self, text, initial_value):
		while True:
			code_pass, tag_pass = self.d.passwordbox(text, 10, 50, initial_value, insecure = True)
			if code_pass == self.d.OK:
				if tag_pass == "":
					self.d.msgbox("\nInvalid data entered. Required value (not empty).", 8, 50, title = "Error Message")
				else:
					return tag_pass
			if code_pass == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates a decision-making interface
	(yes / no).

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	title -- Title displayed on the interface.

	Return:
	tag_yesorno -- Chosen option (yes or no).
	"""
	def getDataYesOrNo(self, text, title):
		tag_yesorno = self.d.yesno(text, 10, 50, title = title)
		return tag_yesorno

	"""
	Method that generates an interface to select a file.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	initial_path -- Directory or initial path.
	title -- Title displayed on the interface.

	Return:
	tag_df -- Path of the selected file.
	"""
	def getFile(self, initial_path, title):
		while True:
			code_fd, tag_df = self.d.fselect(initial_path, 8, 50, title = title)
			if code_fd == self.d.OK:
				if tag_df == "":
					self.d.msgbox("\nSelect a file. Required value (PEM file).", 7, 50, title = "Error Message")
				else:
					ext = Path(tag_df).suffix
					if not ext == ".pem":
						self.d.msgbox("\nSelect a file. Required value (PEM file).", 7, 50, title = "Error Message")
					else:
						return tag_df
			if code_fd == self.d.CANCEL:
				self.mainMenu()

	"""

	"""
	def getDirectory(self, initial_path, title):
		while True:
			code_dd, tag_dd = self.d.dselect(initial_path, 8, 50, title = title)
			if code_dd == self.d.OK:
				if tag_dd == "":
					self.d.msgbox("\nSelect a directory. Required value (not empty).", 7, 50, title = "Error Message")
				else:
					return tag_dd
			if code_dd == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface where it is allowed
	to select a time.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	hour -- Hour.
	minutes -- Minutes.

	Return:
	tag_time -- Chosen time.
	"""
	def getDataTime(self, text, hour, minutes):
		code_time, tag_time = self.d.timebox(text,
											hour = hour,
											minute = minutes,
											second = 00)
		if code_time == self.d.OK:
			return tag_time
		if code_time == self.d.CANCEL:
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
		configuration = Configuration(self)

		options_conf_false = [("Create", "Create the configuration file", 0)]

		options_conf_true = [("Modify", "Modify the configuration file", 0)]
		
		try:
			if not path.exists(configuration.conf_file):
				opt_conf_false = self.getDataRadioList("Select a option:", options_conf_false, "Configuration Options")
				if opt_conf_false == "Create":
					configuration.createConfiguration()
			else:
				opt_conf_true = self.getDataRadioList("Select a option:", options_conf_true, "Configuration Options")
				if opt_conf_true == "Modify":
					configuration.updateConfiguration()
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