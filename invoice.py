import os
import inspect
import sys
import jpype
import jpype.imports
from jpype.types import *

import tkinter as tk
from tkinter import filedialog


######################################
#import jar
# Dynamically gathering JARs from a directory
jars_dir = os.getcwd() + '/jars'
jar_files = [os.path.join(jars_dir, name) for name in os.listdir(jars_dir) if name.endswith(".jar")]
CLASSPATH = os.pathsep.join(jar_files)

# Start the JVM and specify the classpath to include your JAR
jpype.startJVM(jpype.getDefaultJVMPath(), '-ea', f'-Djava.class.path={CLASSPATH}')

# Import Java classes from your JAR
from api import *
#java_obj = VoucherFileUtil()

######################################
#GUI
def select_single_file(arrTypes):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select a File:", filetypes=arrTypes)
    root.destroy()
    return file_path


def select_multiple_files(arrTypes):
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select Multiple Files:", filetypes=arrTypes)
    root.destroy()
    return file_paths


def save_as(arrTypes, strDefaultExt, strInitName=""):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(title="Save As:", filetypes=arrTypes, defaultextension=strDefaultExt, initialfile=strInitName)
    root.destroy()
    return file_path


def select_folder(strHint):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(title=strHint)
    root.destroy()
    return file_path


#ret = select_folder(strHint="Select a Folder to Save Output Files:")
#ret = save_as(arrTypes=[("jar", "*.jar"), ("zip", "*.zip")], strDefaultExt=".pdf", strInitName="aaa.txt") 
#print(ret)

# Create the main window
root = tk.Tk()
# Set window properties
root.title("Invoice Tools")
# Maximize the window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
# Add widgets here (e.g., labels, buttons)
# For example:
label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

# Start the main event loop
root.mainloop()

# Shutdown the JVM when done
jpype.shutdownJVM()
