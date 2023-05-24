# Convert Outlook .msg Files to .eml (MIME format)

This repository contains a Python 3.6 module for reading Microsoft Outlook .msg files and converting them to .eml format, which is the standard MIME format for email messages.

## Installation

1. Clone the repository:

git clone https://github.com/<your-username>/convert-msg-to-eml.git

2. Install the dependencies:

pip install -r requirements.txt

## Usage

To convert a single file, you can use the following command:

python convert_msg_to_eml.py < message.msg > message.eml

This command pipes the contents of the message.msg file to the convert_msg_to_eml.py script and outputs the converted message in MIME format to the message.eml file.

To convert a set of files, you can provide the filenames as command-line arguments:

python convert_msg_to_eml.py *.msg
This will convert each .msg file in the current directory and create a corresponding .eml file with the converted message.

Building the .app
To build the application with PyInstaller, use the following command:

pyinstaller --name=ConvertMsgToEml convert_msg_to_eml.py --target-arch universal2 --windowed --icon=MSG2EML.icns

This command packages your Python script into a standalone application named ConvertMsgToEml.app. The --target-arch universal2 option ensures compatibility with both Intel and Apple Silicon Macs. The --windowed option creates a windowed application without a console window. Finally, the --icon=MSG2EML.icns option sets the application icon to MSG2EML.icns. Make sure you have the MSG2EML.icns file in the same directory as your script.

Using the module in your application
You can also import the outlookmsgfile module into your own application. Here's an example:

import outlookmsgfile

eml = outlookmsgfile.load('my_email_sample.msg')

# Process the `eml` object as needed

The load() function loads an .msg file and returns an EmailMessage instance representing the message in MIME format. You can then process the eml object according to your application's requirements.

Feel free to customize this README.md file further based on your project's specific details.

Please replace `<your-username>` in the clone command with your actual GitHub username.