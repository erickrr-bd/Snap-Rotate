from io import open as open_io
from os import system, path, remove
from modules.UtilsClass import Utils

"""
Class that manages everything related to the Snap-Rotate
service.
"""
class Service:
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores an object of type FormDialog.
	"""
	form_dialog = None

	"""
	Constructor for the Service class.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def __init__(self, form_dialog):
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)

	"""
	Method that starts the Snap-Rotate service.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def startService(self):
		result = system("systemctl start snap-rotate.service")
		if int(result) == 0:
			self.utils.createSnapRotateToolLog("Snap-Rotate service started", 1)
			self.form_dialog.d.msgbox("\nSnap-Rotate service started.", 7, 50, title = "Notification Message")
		if int(result) == 1280:
			self.utils.createSnapRotateToolLog("Failed to start snap-rotate.service. Service not found.", 3)
			self.form_dialog.d.msgbox("\nFailed to start snap-rotate.service. Service not found.", 7, 50, title = "Error Message")
		self.form_dialog.mainMenu()
			
	"""
	Method that restarts the Snap-Rotate service.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def restartService(self):
		result = system("systemctl restart snap-rotate.service")
		if int(result) == 0:
			self.utils.createSnapRotateToolLog("Snap-Rotate service restarted", 1)
			self.form_dialog.d.msgbox("\nSnap-Rotate service restarted.", 7, 50, title = "Notification Message")
		if int(result) == 1280:
			self.utils.createSnapRotateToolLog("Failed to restart snap-rotate.service. Service not found.", 3)
			self.form_dialog.d.msgbox("\nFailed to restart snap-rotate.service. Service not found", 7, 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that stops the Snap-Rotate service.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def stopService(self):
		result = system("systemctl stop snap-rotate.service")
		if int(result) == 0:
			self.utils.createSnapRotateToolLog("Snap-Rotate service stopped", 1)
			self.form_dialog.d.msgbox("\nSnap-Rotate service stopped.", 7, 50, title = "Notification Message")	
		if int(result) == 1280:
			self.utils.createSnapRotateToolLog("Failed to stop snap-rotate.service: Service not found", 3)
			self.form_dialog.d.msgbox("\nFailed to stop snap-rotate.service. Service not found.", 7, 50, title = "Error Message")
		self.form_dialog.mainMenu()

	"""
	Method that obtains the status of the Snap-Rotate service.

	Parameters:
	self -- An instantiated object of the Service class.
	"""
	def getStatusService(self):
		if path.exists('/tmp/snap_rotate.status'):
			remove('/tmp/snap_rotate.status')
		system('(systemctl is-active --quiet snap-rotate.service && echo "Snap-Rotate service is running!" || echo "Snap-Rotate service is not running!") >> /tmp/snap_rotate.status')
		system('echo "Detailed service status:" >> /tmp/snap_rotate.status')
		system('systemctl -l status snap-rotate.service >> /tmp/snap_rotate.status')
		with open_io('/tmp/snap_rotate.status', 'r', encoding = 'utf-8') as file_status:
			self.form_dialog.getScrollBox(file_status.read(), title = "Status Service")