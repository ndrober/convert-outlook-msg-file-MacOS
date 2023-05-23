import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import outlookmsgfile
import plistlib

class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MSG to EML Converter")
        self.root.geometry("400x200")  # Set the window size to 400x200

        # Calculate the center coordinates of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2  # Center horizontally
        y = (screen_height - 200) // 2  # Center vertically
        self.root.geometry(f"400x200+{x}+{y}")  # Set the window position

        self.convert_button = tk.Button(self.root, text="Convert", command=self.select_directory)
        self.convert_button.pack()

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.convert(directory)

    def convert(self, directory):
        for file_name in os.listdir(directory):
            if file_name.endswith(".msg"):
                msg_file_path = os.path.join(directory, file_name)
                eml_file_path = os.path.join(directory, file_name[:-4] + ".eml")

                eml_message = outlookmsgfile.load(msg_file_path)

                with open(eml_file_path, "wb") as eml_file:
                    eml_file.write(eml_message.as_bytes())

                subprocess.run(['open', '-a', 'Mail', eml_file_path])

        # Modify Info.plist for file associations
        if hasattr(sys, "_MEIPASS"):
            plist_path = os.path.join(sys._MEIPASS, 'Info.plist')  # Path to Info.plist in the bundled app
        else:
            plist_path = 'Info.plist'  # Path to Info.plist when running in a regular Python environment

        plist = plistlib.load(open(plist_path, 'rb'))

        plist['CFBundleDocumentTypes'] = [
            {
                'CFBundleTypeName': 'Outlook Message File',
                'CFBundleTypeRole': 'Editor',
                'LSItemContentTypes': ['com.microsoft.outlook.msg'],
                'NSDocumentClass': 'Document',
                'CFBundleTypeExtensions': ['msg'],
                'CFBundleTypeIconFile': 'MSG2EML.icns'  # Replace with your icon file name
            }
        ]

        plistlib.dump(plist, open(plist_path, 'wb'))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MyApp()
    app.run()
