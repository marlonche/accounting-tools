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
rowIndex = 0
tk.Label(root, text="Choose an operation:", width=20, fg="#BFB5A7", bg="#2D3639").grid(row=rowIndex, column=0, padx=10, pady=(10, 0))

#### Operations dropdown
options = [
    "从OFD中将XBRL文件提取到指定位置",
    "从PDF中将XBRL文件提取到指定位置",
    "从PDF中将附件提取到指定位置",
    "从PDF中提取XML",
    "JSON转XBRL",
    "XBRL转JSON",
    "XML转JSON",
    "从PDF中提取XML报文",
    "从OFD中提取出XBRL文件",
    "从PDF中提取出XBRL文件",
]

descriptions = [
    "",
    "",
    "",
    "适用于国库集中支付电子凭证",
    "",
    "",
    "",
    "仅适用于中央财政电子票据",
    "",
    "",
]

selectedIndex = 0
# Create a StringVar to hold the selected option
selectedOption = tk.StringVar(root)
selectedOption.set(options[selectedIndex])  # Set default value

# Response function on option selected
def on_option_selected(selectedValue):
    global selectedIndex
    selectedIndex = options.index(selectedValue)
    opDescription.config(text=descriptions[selectedIndex])

# Create the OptionMenu
dropdown = tk.OptionMenu(root, selectedOption, *options, command=on_option_selected)
dropdown.config(width=30)
rowIndex += 1
dropdown.grid(row=rowIndex, column=0, padx=10, pady=(10, 10))

#### Operation description:
opDescription = tk.Label(root, text=descriptions[0], width=20, fg="#BFB5A7", bg="#2D3639")
rowIndex += 1
opDescription.grid(row=rowIndex, column=0, padx=5, pady=(0, 50))

#### Input Output description:
rowIndex += 1
tk.Label(root, text="Input", width=20, fg="#BFB5A7", bg="#2D3639").grid(row=rowIndex, column=0, padx=5, pady=(0, 0))
tk.Label(root, text="Output", width=20, fg="#BFB5A7", bg="#2D3639").grid(row=rowIndex, column=2, padx=5, pady=(0, 0))

#### Input files
inputFiles = tk.Text(root, width=70, height=30, fg="black", bg="white")
rowIndex += 1
inputFiles.grid(row=rowIndex, column=0, padx=10, pady=10)

#### Start button
def on_start():
    print("button clicked")


btStart = tk.Button(root, text="Start", width=6, height=2, fg="yellow", bg= "gray", command=on_start)
btStart.grid(row=rowIndex, column=1, padx=10, pady=10)

#### Output files
outputFiles = tk.Text(root, width=70, height=30, fg="black", bg="white")
outputFiles.grid(row=rowIndex, column=2, padx=10, pady=10)

#### Select files button
def on_select_files():
    global inputFiles
    arrTypes = []
    match selectedIndex:
        case 0 | 8:
            arrTypes = [("ofd", "*.ofd")]
        case 1 | 2 | 3 | 7 | 9:
            arrTypes = [("pdf", "*.pdf")]
        case 4:
            arrTypes = [("json", "*.json")]
        case 5:
            arrTypes = [("xbrl", "*.xbrl")]
        case 6:
            arrTypes = [("xml", "*.xml")]
    files = select_multiple_files(arrTypes)
    for file in files:
        inputFiles.insert(tk.END, file+"\n")

btSelectFile = tk.Button(root, text="Select Files...", width=12, height=2, fg="yellow", bg= "gray", command=on_select_files)
rowIndex += 1
btSelectFile.grid(row=rowIndex, column=0, sticky="W", padx=(20, 10), pady=0)

#### Select folder button
def on_select_folder():
   print() 

btSelectFolder = tk.Button(root, text="Select Folder...", width=12, height=2, fg="yellow", bg= "gray", command=on_select_folder)
btSelectFolder.grid(row=rowIndex, column=0, sticky="E", padx=(10, 20), pady=0)

#### Clear Text button
def on_clear_text():
    inputFiles.delete("1.0", tk.END)

btClearText = tk.Button(root, text="Clear", width=12, height=2, fg="yellow", bg= "gray", command=on_clear_text)
btClearText.grid(row=rowIndex, column=0, padx=(10), pady=0)


# Start the main event loop
root.mainloop()

# Shutdown the JVM when done
jpype.shutdownJVM()
