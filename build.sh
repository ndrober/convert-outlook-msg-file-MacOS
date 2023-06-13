#!/bin/bash


# Options:
# ./build.sh [ASK] <- Builds install package which asks which destination 
# ./build.sh SYSTEM <- Builds install package for system destination
# ./build.sh USER <- Builds install package for user home destination
#
# Populate CODESIGNAPP and CODESIGNDEV environment variables to sign packages
# Format:
#   Developer ID Installer: Name (Team ID)
#   Developer ID Application: Name (Team ID)


export BUILDVERSION=$(cat version.txt)

mkdir -p dist build
rm -rf build/ConvertMsgToEml dist/ConvertMsgToEml dist/resources dist/Distribution.xml

pyinstaller --noconfirm ConvertMsgToEml.spec
RET=$?

if [ "${RET}" -eq 0 ]; then
	pkgbuild --root dist/ConvertMsgToEml.app --identifier ConvertMsgToEml --scripts scripts --install-location /Applications/ConvertMsgToEml.app dist/ConvertMsgToEml.pkg
	RET=$?
else
	echo "Unknown error occured: ${RET}"
	exit 1
fi

if [ "${RET}" -eq 0 ]; then
	productbuild --synthesize --package dist/ConvertMsgToEml.pkg dist/Distribution.xml
	RET=$?
else
	echo "Unknown error occured: ${RET}"
	exit 2
fi

if [ "${RET}" -eq 0 ]; then
	mkdir -p dist/resources
	cp welcome.html dist/resources
	sed -i '' '3i\'$'\n''<title>ConvertMsgToEml</title>\'$'\n' dist/Distribution.xml
	sed -i '' '4i\'$'\n''<welcome file="welcome.html"/>\'$'\n' dist/Distribution.xml
	RET=$?
	if [ "$1" = "SYSTEM" ]; then
		sed -i '' '15i\'$'\n''<domains enable_anywhere="false" enable_currentUserHome="false" enable_localSystem="true"/>\'$'\n' dist/Distribution.xml
		RET=$?
	elif [ "$1" = "USER" ]; then
		sed -i '' '15i\'$'\n''<domains enable_anywhere="false" enable_currentUserHome="true" enable_localSystem="false"/>\'$'\n' dist/Distribution.xml
		RET=$?
	else
		sed -i '' '15i\'$'\n''<domains enable_anywhere="false" enable_currentUserHome="true" enable_localSystem="true"/>\'$'\n' dist/Distribution.xml
		RET=$?
	fi
else
	echo "Unknown error occured: ${RET}"
	exit 3
fi

if [ "${RET}" -eq 0 ]; then
	if [ "${CODESIGNINST}" != "" ]; then
		productbuild --sign "${CODESIGNINST}" --distribution dist/Distribution.xml --resources dist/resources --package-path dist --scripts scripts --version ${BUILDVERSION} dist/ConvertMsgToEml-dist.pkg
	else
		productbuild --distribution dist/Distribution.xml --resources dist/resources --package-path dist --scripts scripts --version ${BUILDVERSION} dist/ConvertMsgToEml-dist.pkg
	fi
	RET=$?
else
	echo "Unknown error occured: ${RET}"
	exit 4
fi

if [ "${RET}" -eq 0 ]; then
	rm -f dist/ConvertMsgToEml.pkg
	mv dist/ConvertMsgToEml-dist.pkg dist/ConvertMsgToEml-${BUILDVERSION}.pkg
	echo "Package location: dist/ConvertMsgToEml-${BUILDVERSION}.pkg"
	RET=$?
else
	echo "Unknown error occured: ${RET}"
	exit 5
fi

if [ "${RET}" -ne 0 ]; then
	echo "Unknown error occured: ${RET}"
	exit 6
fi
