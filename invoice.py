#!/usr/bin/env python3
import os
import inspect
import sys
import time
import math
import jpype
import jpype.imports
from jpype.types import *

import customtkinter as tk
from customtkinter import filedialog
from pathlib import Path
from collections import defaultdict

######################################
#invoice type
mapInvoiceType = {
    "增值税电子普通发票_开具方": "inv_ord_issuer",
    "增值税电子普通发票_接收方": "inv_ord_receiver",
    "增值税电子专用发票_开具方": "inv_spcl_issuer",
    "增值税电子专用发票_接收方": "inv_spcl_receiver",
    "电子非税收入一般缴款书开_具方": "ntrev_gpm_issuer",
    "电子非税收入一般缴款书_接收方": "ntrev_gpm_receiver",
    "电子发票_铁路电子客票_开具方": "rai_issuer",
    "电子发票_铁路电子客票_接收方": "rai_receiver",
    "电子发票_航空运输电子客票行程单_开具方": "atr_issuer",
    "电子发票_航空运输电子客票行程单_接收方": "atr_receiver",
    "银行电子回单_开具方": "bker_issuer",
    "银行电子回单_接收方": "bker_receiver",
    "银行电子对账单": "bkrs",
    "全面数字化的电子发票-普通发票_接收方": "einv_ord_receiver",
    "全面数字化的电子发票-增值税专用发票_接收方": "einv_spcl_receiver",
    "财政电子票据": "efi",
    "国库集中支付电子凭证": "ctp",
}

strInvoiceType = '''
增值税电子普通发票_开具方
增值税电子普通发票_接收方
增值税电子专用发票_开具方
增值税电子专用发票_接收方
电子非税收入一般缴款书开_具方
电子非税收入一般缴款书_接收方
电子发票_铁路电子客票_开具方
电子发票_铁路电子客票_接收方
电子发票_航空运输电子客票行程单_开具方
电子发票_航空运输电子客票行程单_接收方
银行电子回单_开具方
银行电子回单_接收方
银行电子对账单
全面数字化的电子发票-普通发票_接收方
全面数字化的电子发票-增值税专用发票_接收方
财政电子票据
国库集中支付电子凭证
'''


######################################
#import jar
# Dynamically gathering JARs from a directory
baseDir = os.getcwd()
if hasattr(sys, '_MEIPASS'):
    baseDir = sys._MEIPASS
jars_dir = os.path.join(baseDir, "jars")
jar_files = [os.path.join(jars_dir, name) for name in os.listdir(jars_dir) if name.endswith(".jar")]
CLASSPATH = os.pathsep.join(jar_files)

# Start the JVM and specify the classpath to include your JAR
jpype.startJVM(jpype.getDefaultJVMPath(), '-ea', f'-Djava.class.path={CLASSPATH}')

# Import Java classes from your JAR
from api import *
#java_obj = VoucherFileUtil()


######################################
#Path tools
def get_files_in_dir_with_ext(directory, extension):
    base_path = Path(directory)
    return list(base_path.rglob(f'*.{extension.lstrip(".")}'))

def get_files_in_dir(directory):
    listFiles = []
    path_obj = Path(directory)
    for file_path in path_obj.rglob('*'):
        if file_path.is_file():
            listFiles.append(file_path)
    return listFiles


######################################
#GUI
def select_single_file(arrTypes):
    file_path = filedialog.askopenfilename(title="Select a File:", filetypes=arrTypes)
    return file_path


def select_multiple_files(arrTypes):
    file_paths = filedialog.askopenfilenames(title="Select Multiple Files:", filetypes=arrTypes)
    return file_paths


def save_as(arrTypes, strDefaultExt, strInitName=""):
    file_path = filedialog.asksaveasfilename(title="Save As:", filetypes=arrTypes, defaultextension=strDefaultExt, initialfile=strInitName)
    return file_path


def select_folder(strTitle):
    file_path = filedialog.askdirectory(title=strTitle)
    return file_path


#ret = select_folder(strTitle="Select a Folder to Save Output Files:")
#ret = save_as(arrTypes=[("jar", "*.jar"), ("zip", "*.zip")], strDefaultExt=".pdf", strInitName="aaa.txt") 
#print(ret)

# Create the main window
root = tk.CTk()
# Set window properties
root.title("Invoice Tools")
# Set the window background color to light gray
root.configure(fg_color='#2D3639')
# Maximize the window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

# Add widgets here (e.g., labels, buttons)
rowIndex = 0
tk.CTkLabel(root, text="Choose an operation:", text_color="#BFB5A7", fg_color="#2D3639").grid(row=rowIndex, column=0, columnspan=3, pady=(10, 0))

#### Operations dropdown
options = [
    "从OFD或PDF中提取XBRL",
    "从PDF中提取附件",
    "从PDF中提取XML(国库集中支付电子凭证)",
    "从PDF中提取XML(中央财政电子票据)",
    "JSON转XBRL",
    "XBRL转JSON",
    "XML转JSON",
]

descriptions = [
    "Input包含多个PDF或OFD文件,或目录(目录包括子目录里面的所有PDF或OFD都将被处理)时, Output可指定输出目录(如不指定则输出到源文件所在目录); Input仅包含一个文件名时, Output输出XBRL文本",
    "Input可包含多个PDF文件,或目录(目录包括子目录里面的所有PDF都将被处理); Output可指定输出目录(如不指定则输出到源文件所在目录)",
    "适用于国库集中支付电子凭证; Input仅包含一个PDF文件名时, Output输出XML文本; Input包含多个PDF文件或目录(目录包括子目录里面的所有PDF都将被处理)时, Output可指定输出目录(如不指定则输出到源文件所在目录)",
    "仅适用于中央财政电子票据; Input仅包含一个PDF文件名时,Output输出XML文本; Input包含多个PDF文件或目录(目录包括子目录里面的所有PDF都将被处理)时, Output可指定输出目录(如不指定则输出到源文件所在目录)",
    "Input仅包含一个JSON文件名时,Output输出XBRL文本; Input包含多个JSON文件或目录(目录包括子目录里面的所有JSON文件都将被处理)时, Output可指定输出目录(如不指定则输出到源文件所在目录). JSON文件所在文件夹要用所属票据类型名称命名(程序启动时Output文本框列出了所有票据类型名称)",
    "Input仅包含一个XBRL文件名时,Output输出JSON文本; Input包含多个XBRL文件或目录(目录包括子目录里面的所有XBRL文件都将被处理)时, Output可指定输出目录(如不指定则输出到源文件所在目录). XBRL文件所在文件夹要用所属票据类型名称命名(程序启动时Output文本框列出了所有票据类型名称)",
    "Input包含XML文本或一个XML文件名时, Output输出JSON文本; Input包含多个XML文件或目录(目录包括子目录里面的所有XML文件都将被处理)时, Output可指定输出目录(如不指定则输出到源文件所在目录)",
]

selectedIndex = 0
# Create a StringVar to hold the selected option
selectedOption = tk.StringVar(root)
selectedOption.set(options[selectedIndex])  # Set default value

# Response function on option selected
def on_option_selected(selectedValue):
    global selectedIndex
    selectedIndex = options.index(selectedValue)
    descriptionBox.configure(state=tk.NORMAL)
    descriptionBox.delete("1.0", tk.END)
    descriptionBox.insert(tk.END, descriptions[selectedIndex])
    descriptionBox.configure(state=tk.DISABLED)

# Create the OptionMenu
dropdown = tk.CTkOptionMenu(root, variable=selectedOption, values=options, command=on_option_selected)
#dropdown.configure(width=35)
rowIndex += 1
dropdown.grid(row=rowIndex, column=0, columnspan=3, pady=(6, 6))

#### Operation description:
descriptionBox = tk.CTkTextbox(root, width=1200, height=50, text_color="#BFB5A7", fg_color="#2D3639")
rowIndex += 1
descriptionBox.grid(row=rowIndex, column=0, columnspan=3, padx=5, pady=(0, 20))
descriptionBox.insert(tk.END, descriptions[selectedIndex])
descriptionBox.configure(state=tk.DISABLED)

#### Input Output description:
rowIndex += 1
tk.CTkLabel(root, text="Input", text_color="#BFB5A7", fg_color="#2D3639").grid(row=rowIndex, column=0)
tk.CTkLabel(root, text="Output", text_color="#BFB5A7", fg_color="#2D3639").grid(row=rowIndex, column=2)

#### Input box
inputBox = tk.CTkTextbox(root, width=600, height=400, text_color="black", font=tk.CTkFont(family="IBM Plex Mono", size=14, weight="bold"))
rowIndex += 1
inputBox.grid(row=rowIndex, column=0, padx=3, pady=3)
inputBox.configure(state=tk.DISABLED)

#### Output box
outputBox = tk.CTkTextbox(root, width=600, height=400, text_color="black", font=tk.CTkFont(family="IBM Plex Mono", size=14, weight="bold"))
outputBox.grid(row=rowIndex, column=2, padx=3, pady=3)
outputBox.insert(tk.END, strInvoiceType)
outputBox.configure(state=tk.DISABLED)

#### Start button
mapInputFiles = defaultdict(lambda: set())

#progress bar
rootBar = tk.CTkToplevel(root)
rootBar.transient(root)
rootBar.lift()
rootBar.title("Processing...")
width = math.floor(rootBar.winfo_screenwidth() * 0.8)
height = math.floor(rootBar.winfo_screenheight() * 0.1)
x = (rootBar.winfo_screenwidth() // 2) - (width // 2)
y = (rootBar.winfo_screenheight() // 2) - (height // 2)
rootBar.geometry(f'{width}x{height}+{x}+{y}')
progress = tk.CTkProgressBar(rootBar, orientation=tk.HORIZONTAL, mode='determinate')
progress.pack(fill=tk.X, expand=True)
rootBar.withdraw()  # Hide the progress bar initially

def on_start():
    global mapInputFiles
    btStart.configure(state=tk.DISABLED)
    #progress bar
    rootBar.deiconify()
    rootBar.grab_set()
    progress.pack(fill=tk.X, expand=True)
    progress.set(0)
    progressMax = 1
    progressVal = 0
    def updateProgress():
        nonlocal progressVal
        progressVal += 1
        progress.set(progressVal / progressMax)
        rootBar.update_idletasks()

    lines = inputBox.get("1.0", tk.END).splitlines()
    lines = [line for line in lines if line.strip()]
    for line in lines:
        path = Path(line)
        if path.is_dir():
            listFiles = get_files_in_dir(line)
            for file in listFiles:
                ext = Path(file).suffix.removeprefix(".")
                if ext not in mapInputFiles:
                    mapInputFiles[ext] = set()
                mapInputFiles[ext].add(file)
        elif path.is_file():
            ext = path.suffix.removeprefix(".")
            if ext not in mapInputFiles:
                mapInputFiles[ext] = set()
            mapInputFiles[ext].add(line)
    strDestDir = ""
    lines = outputBox.get("1.0", tk.END).splitlines()
    lines = [line for line in lines if line.strip()]
    if len(lines) == 1:
        path = Path(lines[0])
        if path.exists() and path.is_dir():
            strDestDir = lines[0]
    match selectedIndex:
        #"从OFD或PDF中提取XBRL"
        case 0:
            setOfd = mapInputFiles["ofd"]
            setPdf = mapInputFiles["pdf"]
            progressMax = len(setOfd) + len(setPdf)
            for file in setOfd:
                updateProgress()
                path = Path(file)
                strDestFile = str(path.with_suffix(".xbrl"))
                if strDestDir:
                    strDestFile = str((Path(strDestDir) / path.name).with_suffix(".xbrl"))
                VoucherFileUtil.extractXBRLFromOFD(file, strDestFile)
                if len(setOfd) == 1:
                    strXbrl = ""
                    with open(strDestFile, 'r', encoding='utf-8') as f:
                        strXbrl = f.read()
                    outputBox.configure(state=tk.NORMAL)
                    outputBox.delete("1.0", tk.END)
                    outputBox.insert(tk.END, strXbrl)
                    outputBox.configure(state=tk.DISABLED)
            for file in setPdf:
                updateProgress()
                path = Path(file)
                strDestFile = str(path.with_suffix(".xbrl"))
                if strDestDir:
                    strDestFile = str((Path(strDestDir) / path.name).with_suffix(".xbrl"))
                VoucherFileUtil.extractXBRLFromPDF(file, strDestFile)
                if len(setPdf) == 1:
                    strXbrl = ""
                    with open(strDestFile, 'r', encoding='utf-8') as f:
                        strXbrl = f.read()
                    outputBox.configure(state=tk.NORMAL)
                    outputBox.delete("1.0", tk.END)
                    outputBox.insert(tk.END, strXbrl)
                    outputBox.configure(state=tk.DISABLED)
        #"从PDF中提取附件"
        case 1:
            setPdf = mapInputFiles["pdf"]
            progressMax = len(setPdf) 
            for file in setPdf:
                updateProgress()
                path = Path(file)
                if not strDestDir:
                    strDestDir = str(path.parent)
                VoucherFileUtil.extractAttachFromPDF(file, strDestDir) 
        #"从PDF中提取XML(国库集中支付电子凭证)"
        case 2:
            setPdf = mapInputFiles["pdf"]
            progressMax = len(setPdf) 
            for file in setPdf:
                updateProgress()
                path = Path(file)
                strDestFile = str(path.with_suffix(".xml"))
                if strDestDir:
                    strDestFile = str((Path(strDestDir) / path.name).with_suffix(".xml"))
                strXml = str(VoucherFileUtil.extractXMLFromPDF(file))
                if len(setPdf) == 1:
                    outputBox.configure(state=tk.NORMAL)
                    outputBox.delete("1.0", tk.END)
                    outputBox.insert(tk.END, strXml)
                    outputBox.configure(state=tk.DISABLED)
                with open(strDestFile, "w") as f:
                    f.write(strXml)
        #"从PDF中提取XML(中央财政电子票据)"
        case 3:
            setPdf = mapInputFiles["pdf"]
            progressMax = len(setPdf) 
            for file in setPdf:
                updateProgress()
                path = Path(file)
                strDestFile = str(path.with_suffix(".xml"))
                if strDestDir:
                    strDestFile = str((Path(strDestDir) / path.name).with_suffix(".xml"))
                strXml = str(VoucherFileUtil.extractXMLFromCEBPDF(file))
                if len(setPdf) == 1:
                    outputBox.configure(state=tk.NORMAL)
                    outputBox.delete("1.0", tk.END)
                    outputBox.insert(tk.END, strXml)
                    outputBox.configure(state=tk.DISABLED)
                with open(strDestFile, "w") as f:
                    f.write(strXml)
        #"JSON转XBRL"
        case 4:
            setJson = mapInputFiles["json"]
            progressMax = len(setJson) 
            for file in setJson:
                updateProgress()
                path = Path(file)
                strDestFile = str(path.with_suffix(".xbrl"))
                if strDestDir:
                    strDestFile = str((Path(strDestDir) / path.name).with_suffix(".xbrl"))
                strJson = ""
                configID = mapInvoiceType[path.parent.name]
                with open(file, 'r', encoding='utf-8') as f:
                    strJson = f.read()
                strXbrl = str(VoucherFileUtil.json2Xbrl(strJson, configID))
                if len(setJson) == 1:
                    outputBox.configure(state=tk.NORMAL)
                    outputBox.delete("1.0", tk.END)
                    outputBox.insert(tk.END, strXbrl)
                    outputBox.configure(state=tk.DISABLED)
                with open(strDestFile, "w") as f:
                    f.write(strXbrl)
            
        #"XBRL转JSON"
        case 5:
            setXbrl = mapInputFiles["xbrl"]
            progressMax = len(setXbrl) 
            for file in setXbrl:
                updateProgress()
                path = Path(file)
                strDestFile = str(path.with_suffix(".json"))
                if strDestDir:
                    strDestFile = str((Path(strDestDir) / path.name).with_suffix(".json"))
                strXbrl = ""
                configID = mapInvoiceType[path.parent.name]
                with open(file, 'r', encoding='utf-8') as f:
                    strXbrl = f.read()
                strJson = str(VoucherFileUtil.xbrl2Json(strXbrl, configID).toJSONString())
                if len(setXbrl) == 1:
                    outputBox.configure(state=tk.NORMAL)
                    outputBox.delete("1.0", tk.END)
                    outputBox.insert(tk.END, strJson)
                    outputBox.configure(state=tk.DISABLED)
                with open(strDestFile, "w") as f:
                    f.write(strJson)
         
        #"XML转JSON"
        case 6:
            setXml = mapInputFiles["xml"]
            progressMax = len(setXml) 
            for file in setXml:
                updateProgress()
                path = Path(file)
                strDestFile = str(path.with_suffix(".json"))
                if strDestDir:
                    strDestFile = str((Path(strDestDir) / path.name).with_suffix(".json"))
                strXml = ""
                with open(file, 'r', encoding='utf-8') as f:
                    strXml = f.read()
                strJson = str(VoucherFileUtil.xml2Json(strXml).toJSONString())
                if len(setXml) == 1:
                    outputBox.configure(state=tk.NORMAL)
                    outputBox.delete("1.0", tk.END)
                    outputBox.insert(tk.END, strJson)
                    outputBox.configure(state=tk.DISABLED)
                with open(strDestFile, "w") as f:
                    f.write(strJson)
    btStart.configure(state=tk.NORMAL)
    rootBar.grab_release()
    rootBar.withdraw()


btStart = tk.CTkButton(root, text="Start", width=50, command=on_start)
btStart.grid(row=rowIndex, column=1, padx=0)

#### Select files button
def on_select_files():
    arrTypes = []
    match selectedIndex:
        case 0:
            arrTypes = [("ofd,pdf", "*.ofd *.pdf")]
        case 1 | 2 | 3:
            arrTypes = [("pdf", "*.pdf")]
        case 4:
            arrTypes = [("json", "*.json")]
        case 5:
            arrTypes = [("xbrl", "*.xbrl")]
        case 6:
            arrTypes = [("xml", "*.xml")]
    files = select_multiple_files(arrTypes)
    inputBox.configure(state=tk.NORMAL)
    for file in files:
        inputBox.insert(tk.END, file+"\n")
    inputBox.configure(state=tk.DISABLED)

#btSelectFile = tk.Button(root, text="Select Files...", width=12, height=2, fg="yellow", bg= "#535151", command=on_select_files)
btSelectFile = tk.CTkButton(root, text="Select Files...", command=on_select_files)
rowIndex += 1
btSelectFile.grid(row=rowIndex, column=0, sticky="W", padx=(20, 10), pady=0)

#### Select input folder button
def on_select_input_folder():
    ret = select_folder(strTitle="Select a folder containing input files:")
    if not ret:
        return
    inputBox.configure(state=tk.NORMAL)
    inputBox.insert(tk.END, ret+"/\n")
    inputBox.configure(state=tk.DISABLED)

#btSelectInputFolder = tk.Button(root, text="Select Folder...", width=12, height=2, fg="yellow", bg= "#535151", command=on_select_input_folder)
btSelectInputFolder = tk.CTkButton(root, text="Select Folder...", command=on_select_input_folder)
btSelectInputFolder.grid(row=rowIndex, column=0, padx=(10), pady=0)

#### Clear text box button
def on_clear_text():
    inputBox.configure(state=tk.NORMAL)
    inputBox.delete("1.0", tk.END)
    inputBox.configure(state=tk.DISABLED)

#btClearText = tk.Button(root, text="Clear", width=12, height=2, fg="yellow", bg= "#535151", command=on_clear_text)
btClearText = tk.CTkButton(root, text="Clear", command=on_clear_text)
btClearText.grid(row=rowIndex, column=0, sticky="E", padx=(10, 20), pady=0)

#### Select output folder button
def on_select_output_folder():
    ret = select_folder(strTitle="Select a folder to store output files:")
    if not ret:
        return
    outputBox.configure(state=tk.NORMAL)
    outputBox.delete("1.0", tk.END)
    outputBox.insert(tk.END, ret+"/\n")
    outputBox.configure(state=tk.DISABLED)

#btSelectOutputFolder = ttk.Button(root, text="Select Folder...", width=12, height=2, fg="#613302", bg="#535151", activebackground="#050505", command=on_select_output_folder)
btSelectOutputFolder = tk.CTkButton(root, text="Select Folder...", command=on_select_output_folder)
btSelectOutputFolder.grid(row=rowIndex, column=2, sticky="W", padx=(20, 10), pady=0)


# Start the main event loop
root.mainloop()

# Shutdown the JVM when done
jpype.shutdownJVM()
