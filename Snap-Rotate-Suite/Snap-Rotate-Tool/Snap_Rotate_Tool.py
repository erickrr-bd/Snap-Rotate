#! /usr/bin/env python3

from modules.FormClass import FormDialog

"""
FormDialog type object.
"""
form = FormDialog()

"""
Main function of the application
"""
if __name__ == "__main__":
	while True:
		form.mainMenu()