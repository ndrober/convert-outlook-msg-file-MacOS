# Convert Outlook .msg Files to .eml (MIME format)

This repository contains a Python 3.6 module for reading Microsoft Outlook .msg files and converting them to .eml format, which is the standard MIME format for email messages.

## Installation

1. Clone the repository:

git clone https://github.com/<your-username>/convert-msg-to-eml.git

2. Install the dependencies:

pip install -r requirements.txt

## Usage

To convert a single file on Mac, you can use the following command:

open -a ConvertMsgToEml message.msg

This command converts message.msg file, outputing the converted message in MIME format to the message.eml file, and finally opening it with Apple Mail.

To convert a set of files, you can provide the filenames as command-line arguments:

Open the ConvertMsgToEml Application and click the Convert Directory button.
This will convert each .msg file in the selected directory and create a corresponding .eml file with the converted message.

Building the .app
To build the application with PyInstaller, use the following command:
./build.sh

Using the module in your application
You can also import the outlookmsgfile module into your own application. Here's an example:

import outlookmsgfile

eml = outlookmsgfile.load('my_email_sample.msg')

# Process the `eml` object as needed

The load() function loads an .msg file and returns an EmailMessage instance representing the message in MIME format. You can then process the eml object according to your application's requirements.

Feel free to customize this README.md file further based on your project's specific details.

Please replace `<your-username>` in the clone command with your actual GitHub username.
