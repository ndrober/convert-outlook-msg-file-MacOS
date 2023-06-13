#!/bin/bash
#
# Cleanup script for testing
# Removes Apple Mail configuration and any installed versions of ConvertMsgToEml

sudo rm -rf ${HOME}/Library/Group\ Containers/group.com.apple.mail \
	${HOME}/Library/Preferences/group.com.apple.mail.plist \
	${HOME}/Library/Preferences/com.apple.mail-shared.plist \
	${HOME}/Library/Application\ Scripts/com.apple.mail* \
	${HOME}/Library/Application\ Scripts/group.com.apple.mail \
	${HOME}/Library/Containers/com.apple.mail* \
	${HOME}/Library/Mail \
	${HOME}/Applications/ConvertMsgToEml.app \
	/Applications/ConvertMsgToEml.app
sudo pkgutil --forget ConvertMsgToEml
pkgutil --forget ConvertMsgToEml --volume=${HOME}
