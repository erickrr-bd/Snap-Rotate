from os import path
from sys import exit
from pathlib import Path
from dialog import Dialog
from re import compile as re_compile
from modules.UtilsClass import Utils
from modules.ServiceClass import Service
from modules.ConfigurationClass import Configuration

"""
Class that allows managing all the graphical interfaces of the application.
"""
class FormDialog:
	"""
	Property that stores an object of type Dialog.
	"""
	d = None

	"""
	Constructor for the FormDialog class.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def __init__(self):
		self.d = Dialog(dialog = "dialog")
		self.utils = Utils(self)
		self.d.set_background_title("SNAP-ROTATE-TOOL")

	"""
	Method that generates the menu interface.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	options -- List of options that make up the menu.
	title -- Title displayed on the interface.

	Return:
	tag_menu -- Chosen option.
	"""
	def getMenu(self, text, options, title):
		code_menu, tag_menu = self.d.menu(text = text,
										  choices = options,
										  title = title)
		if code_menu == self.d.OK:
			return tag_menu
		if code_menu == self.d.CANCEL:
			exit(0)

	"""
	Method that generates an interface with several available options, and where only one of them can be chosen.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	options -- List of options that make up the interface.
	title -- Title displayed on the interface.

	Return:
	tag_radiolist -- Chosen option.
	"""
	def getDataRadioList(self, text, options, title):
		while True:
			code_radiolist, tag_radiolist = self.d.radiolist(text = text,
					  										 width = 65,
					  										 choices = options,
					  										 title = title)
			if code_radiolist == self.d.OK:
				if len(tag_radiolist) == 0:
					self.d.msgbox("\nSelect at least one option.", 7, 50, title = "Error Message")
				else:
					return tag_radiolist
			elif code_radiolist == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface with several available options, and where you can choose one or more of them.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	options -- List of options that make up the interface.
	title -- Title displayed on the interface.

	Return:
	tag_checklist -- List with the chosen options.
	"""
	def getDataCheckList(self, text, options, title):
		while True:
			code_checklist, tag_checklist = self.d.checklist(text = text,
					 										 width = 75,
					 										 choices = options,
					 										 title = title)
			if code_checklist == self.d.OK:
				if len(tag_checklist) == 0:
					self.d.msgbox("\nSelect at least one option.", 7, 50, title = "Error Message")
				else:
					return tag_checklist
			elif code_checklist == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for entering decimal or floating type data.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Decimal or float value entered.
	"""
	def getDataNumberDecimal(self, text, initial_value):
		decimal_reg_exp = re_compile(r'^[1-9](\.[0-9]+)?$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text,
											  			  height = 10,
											  			  width = 50,
											  			  init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(decimal_reg_exp, tag_inputbox)):
					self.d.msgbox("\nInvalid data entered. Required value (decimal or float).", 8, 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter an IP address.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- IP address entered.
	"""
	def getDataIP(self, text, initial_value):
		ip_reg_exp = re_compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text,
														  height = 10,
														  width = 50,
														  init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(ip_reg_exp, tag_inputbox)):
					self.d.msgbox("\nInvalid data entered. Required value (IP address).", 8, 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter a port.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Port entered.
	"""
	def getDataPort(self, text, initial_value):
		port_reg_exp = re_compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text,
														  height = 10,
														  width = 50,
														  init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(port_reg_exp, tag_inputbox)):
					self.d.msgbox("\nInvalid data entered. Required value (0 - 65535).", 8, 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter text.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Text entered.
	"""
	def getDataInputText(self, text, initial_value):
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text,
														  height = 10,
														  width = 50,
														  init = initial_value)
			if code_inputbox == self.d.OK:
				if tag_inputbox == "":
					self.d.msgbox("\nInvalid data entered. Required value (not empty).", 8, 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter a password.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_passwordbox -- Password entered.
	"""
	def getDataPassword(self, text, initial_value):
		while True:
			code_passwordbox, tag_passwordbox = self.d.passwordbox(text = text,
																   height = 10,
																   width = 50,
																   init = initial_value,
																   insecure = True)
			if code_passwordbox == self.d.OK:
				if tag_passwordbox == "":
					self.d.msgbox("\nInvalid data entered. Required value (not empty).", 8, 50, title = "Error Message")
				else:
					return tag_passwordbox
			elif code_passwordbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates a decision-making interface (yes/no).

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	title -- Title displayed on the interface.

	Return:
	tag_yesno -- Chosen option (yes or no).
	"""
	def getDataYesOrNo(self, text, title):
		tag_yesno = self.d.yesno(text = text,
								 height = 10,
								 width = 50,
								 title = title)
		return tag_yesno

	"""
	Method that generates an interface to select a file.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	initial_path -- Initial path in the interface.
	title -- Title displayed on the interface.
	extension_file -- Extension valid for the file.

	Return:
	tag_fselect -- Path of the selected file.
	"""
	def getFile(self, initial_path, title, extension_file):
		while True:
			code_fselect, tag_fselect = self.d.fselect(filepath = initial_path,
													   height = 8,
													   width = 50,
													   title = title)
			if code_fselect == self.d.OK:
				if tag_fselect == "":
					self.d.msgbox("\nSelect a file. Required value: " + extension_file + " file.", 7, 50, title = "Error Message")
				else:
					ext_file = Path(tag_fselect).suffix
					if not ext_file == extension_file:
						self.d.msgbox("\nSelect a file. Required value: " + extension_file + " file.", 7, 50, title = "Error Message")
					else:
						return tag_fselect
			elif code_fselect == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to select a directory.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	initial_path -- Initial path in the interface.
	title -- Title displayed on the interface.

	Return:
	tag_dselect -- Selected directory.
	"""
	def getDirectory(self, initial_path, title):
		while True:
			code_dselect, tag_dselect = self.d.dselect(filepath = initial_path,
													   height = 8,
													   width = 50,
													   title = title)
			if code_dselect == self.d.OK:
				if tag_dselect == "":
					self.d.msgbox("\nSelect a directory. Required value (not empty).", 7, 50, title = "Error Message")
				else:
					return tag_dselect
			elif code_dselect == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface where it is allowed to select a time.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	hour -- Time displayed on the interface.
	minutes -- Minutes displayed on the interface.

	Return:
	tag_timebox -- Chosen time.
	"""
	def getDataTime(self, text, hour, minutes):
		code_timebox, tag_timebox = self.d.timebox(text = text,
												   hour = hour,
												   minute = minutes,
												   second = 00)
		if code_timebox == self.d.OK:
			return tag_timebox
		elif code_timebox == self.d.CANCEL:
			self.mainMenu()

	"""
	Method that generates an interface with scroll box.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	text -- Text displayed on the interface.
	title -- Title displayed on the interface.
	"""
	def getScrollBox(self, text, title):
		code_scrollbox = self.d.scrollbox(text = text,
										  height = 15,
										  width = 70,
										  title = title)
		if code_scrollbox == self.d.OK:
			self.mainMenu()

	"""
	Method that defines the action to be performed on the Snap-Rotate configuration file (creation or modification).

	Parameters:
	self -- An instantiated object of the FormDialog class.
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
			self.utils.createSnapRotateToolLog(exception, 3)
			self.d.msgbox("\nAn error has occurred. For more information, see the logs.", 8, 50, title = "Error Message")
			self.mainMenu()

	"""
	Method that displays a message on the screen with information about the application.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def getAbout(self):
		message = "\nCopyright@2021 Tekium. All rights reserved.\nSnap-Rotate v3.0\nAuthor: Erick Rodriguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\n" + "License: GPLv3\n\nSnap-Rotate is an application that creates a repository every last\nday of the month, and it stores snapshots of certain indexes."
		self.getScrollBox(message, "About")

	"""
	Method that launches an action based on the option chosen in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
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
	Method that launches an action based on the option chosen in the service menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchSmenu(self, option):
		service = Service(self)
		if option == 1:
			service.startService()
		if option == 2:
			service.restartService()
		if option == 3:
			service.stopService()
		if option == 4:
			service.getStatusService()

	"""
	Method that defines the menu of options related to the Snap-Rotate service.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def serviceMenu(self):
		options_sm = [("1", "Start Service"),
					  ("2", "Restart Service"),
					  ("3", "Stop Service"),
					  ("4", "Service Status")]

		option_sm = self.getMenu("Choose an option:", options_sm, "Service Menu")
		self.switchSmenu(int(option_sm))

	"""
	Method that defines the menu on the actions to be carried out in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def mainMenu(self):
		options_mm = [("1", "Snap-Rotate Configuration"),
					  ("2", "Snap-Rotate Service"),
					  ("3", "About"),
					  ("4", "Exit")]

		option_mm = self.getMenu("Choose an option:", options_mm, "Main Menu")
		self.switchMmenu(int(option_mm))