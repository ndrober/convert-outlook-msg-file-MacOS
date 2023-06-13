import os
import sys
import subprocess
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
import outlookmsgfile
from email import generator

class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.createcommand("::tk::mac::OpenDocument", self.open_file_event)
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

    def open_file_event(self, *args):
        for arg in args:
            outfile = infile = str(arg)

            if not infile.lower().endswith(".msginit"):
                if infile.lower().endswith(".msg"):
                    eml_message = outlookmsgfile.load(infile)
                    outfile = "{}/{}.eml".format(tempfile.gettempdir(), os.path.basename(infile)[:-4])
                    with open(outfile, "wb") as eml_file:
                        eml_file.write(eml_message.as_bytes())

                elif not infile.lower().endswith(".eml"):
                    messagebox.showinfo("Open File Error", "Could not open file: {}".format(str(arg)))

                subprocess.run(['open', '-a', 'Mail', outfile])
        self.root.destroy()

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.convert(directory)

    def convert(self, directory):
        for file_name in os.listdir(directory):
            if file_name.lower().endswith(".msg"):
                msg_file_path = os.path.join(directory, file_name)
                eml_file_path = os.path.join(directory, file_name[:-4] + ".eml")

                eml_message = outlookmsgfile.load(msg_file_path)

                with open(eml_file_path, "wb") as eml_file:
                    eml_file.write(eml_message.as_bytes())

                subprocess.run(['open', '-a', 'Mail', eml_file_path])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MyApp()
    app.run()
