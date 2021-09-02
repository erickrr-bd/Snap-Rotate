from sys import exit
from dialog import Dialog

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
		#self.utils = Utils(self)
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