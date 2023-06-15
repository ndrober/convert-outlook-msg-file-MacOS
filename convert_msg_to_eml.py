import os
import sys
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
import outlookmsgfile
from email import generator
from AppKit import NSURL, UTType, NSWorkspace, NSFileManager
import datetime
import plistlib

class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.createcommand("::tk::mac::OpenDocument", self.open_file_event)
        self.root.title("MSG to EML Converter")
        self.root.geometry("400x200")  # Set the window size to 400x200

        # Initialize AppKit.NSWorkspace
        self.NSWorkspace = NSWorkspace.new()
        self.mailapps = self.get_mail_apps()
        self.read_preferences()

        # Bring to front
        self.root.lift()
        self.root.attributes('-topmost',True)
        self.root.after_idle(self.root.attributes,'-topmost',False)

        # Calculate the center coordinates of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2  # Center horizontally
        y = (screen_height - 200) // 2  # Center vertically
        self.root.geometry(f"400x200+{x}+{y}")  # Set the window position

        self.root.frame1 = tk.Frame(self.root)
        self.root.frame1.pack(side='top', fill='both', expand=True)
        self.convert_file_button = tk.Button(self.root, text="Convert File", command=self.select_file)
        self.convert_file_button.pack()

        self.root.frame2 = tk.Frame(self.root)
        self.root.frame2.pack(side='bottom', fill='both', expand=True)
        self.convert_dir_button = tk.Button(self.root, text="Convert Directory", command=self.select_directory)
        self.convert_dir_button.pack()

        # Setup File Bar menus
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, name="file")
        menubar.add_cascade(menu=filemenu, label="File")
        filemenu.add_command(label='Convert File...', command=self.select_file)
        filemenu.add_command(label='Convert Directory...', command=self.select_directory)
        filemenu.add_separator()
        prefmenu = tk.Menu(menubar)
        filemenu.add_cascade(menu=prefmenu, label="Preferences")
        mailmenu = tk.Menu(menubar)
        prefmenu.add_cascade(menu=mailmenu, label="Use Mail App")
        for app in self.mailapps:
            system_def = ''
            if app['isdefault']:
                system_def = ' (System Default)'
            mailmenu.add_radiobutton(label=app['app_displayname'] + system_def, value=app['app_url'], variable=self.preferences['use_mail_app'], command=self.write_preferences)
        prefmenu.add_checkbutton(label='File Event Converts', onvalue=True, offvalue=False, variable=self.preferences['file_event_converts'], command=self.write_preferences)
        prefmenu.add_checkbutton(label='Open on Convert', onvalue=True, offvalue=False, variable=self.preferences['open_on_convert'], command=self.write_preferences)
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=self.root.destroy)
        windowmenu = tk.Menu(menubar, name="window")
        menubar.add_cascade(menu=windowmenu, label="Window")
        self.root['menu'] = menubar

    def get_mail_apps(self):
        apps = []
        mailtype = UTType.typeWithMIMEType_("message/rfc822")
        mailappurls = self.NSWorkspace.URLsForApplicationsToOpenContentType_(mailtype)
        defaultmailappurl = self.NSWorkspace.URLForApplicationToOpenContentType_(mailtype)

        fm = NSFileManager.new()

        for url in mailappurls:
            displayName = fm.displayNameAtPath_(url.path())
            isdefault = False
            if str(url) == str(defaultmailappurl):
                isdefault = True
            apps.append({'app_url':str(url), 'app_displayname':displayName, 'isdefault':isdefault})

        return apps


    def read_preferences(self):
        pref_path = os.path.expanduser('~/Library/Application Support/ConvertMsgToEml')
        self.pref_file = os.path.join(pref_path, 'Preferences.plist')
        if not os.path.isdir(pref_path):
            os.makedirs(pref_path, exist_ok=True)

        if os.path.isfile(self.pref_file):
            with open(self.pref_file, 'rb') as f:
                self.preferences = plistlib.load(f)
        else:
            self.preferences = {}

        if not 'use_mail_app' in self.preferences:
            self.preferences['use_mail_app'] = tk.StringVar()
            self.preferences['use_mail_app'].set('file:///System/Applications/Mail.app/')
        else:
            tmp_use_mail_app = self.preferences['use_mail_app']
            self.preferences['use_mail_app'] = tk.StringVar()
            self.preferences['use_mail_app'].set(tmp_use_mail_app)

        if not 'file_event_converts' in self.preferences:
            self.preferences['file_event_converts'] = tk.BooleanVar()
            self.preferences['file_event_converts'].set(False)
        else:
            tmp_file_event_converts = self.preferences['file_event_converts']
            self.preferences['file_event_converts'] = tk.BooleanVar()
            self.preferences['file_event_converts'].set(tmp_file_event_converts)

        if not 'open_on_convert' in self.preferences:
            self.preferences['open_on_convert'] = tk.BooleanVar()
            self.preferences['open_on_convert'].set(True)
        else:
            tmp_open_on_convert = self.preferences['open_on_convert']
            self.preferences['open_on_convert'] = tk.BooleanVar()
            self.preferences['open_on_convert'].set(tmp_open_on_convert)

        if not os.path.isfile(self.pref_file):
            self.write_preferences()

    def write_preferences(self):
        tmp_preferences = {}
        tmp_preferences['use_mail_app'] = self.preferences['use_mail_app'].get()
        tmp_preferences['file_event_converts'] = self.preferences['file_event_converts'].get()
        tmp_preferences['open_on_convert'] = self.preferences['open_on_convert'].get()
        tmp_preferences['last_updated'] = datetime.datetime.now()
        with open(self.pref_file, 'wb') as f:
            plistlib.dump(tmp_preferences, f)


    def open_file_event(self, *args):
        for arg in args:
            #outfile = infile = str(arg)
            infile = str(arg)

            if not infile.lower().endswith(".msginit"):
                if self.preferences['file_event_converts'].get():
                    self._do_convert(infile)
                else:
                    self._do_convert(infile, tempfile.gettempdir())
        self.root.destroy()

    def select_file(self):
        file = filedialog.askopenfilename(title="Convert file", filetypes=(("MSG files","*.msg"), ("EML files","*.eml")))
        if os.path.isfile(file):
            self.convert(file)

    def select_directory(self):
        directory = filedialog.askdirectory(title="Convert directory")
        if os.path.isdir(directory):
            self.convert(directory)

    def convert(self, item):
        if os.path.isdir(item):
            for file_name in os.listdir(item):
                if file_name.lower().endswith(".msg"):
                    self._do_convert(os.path.join(item, file_name))
        else:
            self._do_convert(item)

    def _do_convert(self, item, targetdir=None):
        if targetdir is None:
            targetdir = os.path.dirname(item)
        if item.endswith(".msg") or item.endswith(".eml"):
            msg_file_path = item
            eml_file_path = os.path.join(targetdir, os.path.basename(item)[:-4] + ".eml")
            if item.lower().endswith(".msg"):
                eml_message = outlookmsgfile.load(msg_file_path)
                with open(eml_file_path, "wb") as eml_file:
                    eml_file.write(eml_message.as_bytes())

            if self.preferences['open_on_convert'].get():
                for app in self.mailapps:
                    if app['app_url'] == self.preferences['use_mail_app'].get():
                        self.NSWorkspace.openFile_withApplication_(eml_file_path, app['app_displayname'])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MyApp()
    app.run()
