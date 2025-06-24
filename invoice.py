#!/usr/bin/env python3
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
# Set the window background color to light gray
root.configure(bg='#2D3639')
# Maximize the window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

# Add widgets here (e.g., labels, buttons)
# Operation description:
opDescript = tk.Label(root, text="Hello, Tkinter!", width=20, fg="#BFB5A7", bg="#2D3639")
opDescript.grid(row=1, column=0, padx=5, pady=10)

#Input files
inputFiles = tk.Text(root, width=40, height=20, fg="black", bg="white")
inputFiles.grid(row=2, column=0, padx=10, pady=10)

#Start button
def on_start():
    print("button clicked")


btStart = tk.Button(root, text="Start", width=6, height=2, fg="white", bg= "gray", command=on_start)
btStart.grid(row=2, column=1, padx=10, pady=10)

#Output files
outputFiles = tk.Text(root, width=40, height=20, fg="black", bg="white")
outputFiles.grid(row=2, column=2, padx=10, pady=10)


# Start the main event loop
root.mainloop()

# Shutdown the JVM when done
jpype.shutdownJVM()
