from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from tkinter import scrolledtext
import customtkinter as ctk
import mysql.connector
from mysql.connector import Error
from passlib.context import CryptContext
import sqlite3
from settings import *
import os
from os.path import exists
import shutil
import json
from checklistcombobox import *
from PIL import ImageTk, Image


def createnewgroup(self, *args, **kwargs):
    rwindow = tkinter.Toplevel()
    rwindow.title("Register")
    rwindow.geometry('600x790+200+200')
    rwindow.resizable(False, False)
    rwindow.configure(background='powder blue')
    rwindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

    groupname = StringVar(value="Your Group Name")
    #members = StringVar(value="test_members")
    #devids = StringVar(value="test_devids")
    #groupcmdslist=[]
    configmethodvar = StringVar()
    
    # !
    # This is used to create the group selection dropdown selection
    # replace with self.groupcomboboxoptions
    #global memseleccbxvar
    # !

    global memselecchkbxvar
    self.memselecchkbxvar = []
    
    memvaluesdb = []
    
    global cmdenryvar
    cmdenryvar = []
    

    def changegroupfile(self, *args, **kwargs):
        # getinto current directory
        # print(f"The current working directory is : {os.getcwd()}")
        # print(f"The directory I want is: {directorypathroot}")
        # os.chdir(directorypathroot) # Obtained from settings file
        print(f"1) creategroupfile changegroupfile The cwd is : {os.getcwd()}")
        
        # Has the variables been captured
        print(f"2) Has the variables been captured {groupname.get()}")

        # change directory to project path
        # os.chdir(groudevicepath) # Obtained from settings file
        #print(f"The current working directory is : {os.getcwd()}")


        # HERE WE GO 
        print(f"3) GO (Group name: {groupname.get()})")
        print(f"4) GO (Member Selection: {self.memselecchkbxvar})")
        print(f"5) GO (Config Method: {configmethodvar.get()})")
        print(f"6) GO (Commands: {cmdenryvar})")

        # Get into the right folder
        groudevicepath = os.path.join(devicegroups, groupname.get())
        # load the file
        dest_path = os.path.join(groudevicepath, groupname.get() + ".json")
        filetoread = open(dest_path)
        inputjsondata = json.load(filetoread)
        print(f"7) Addbutton filetoread = {filetoread}")
        print(f"7b) Addbutton inputjsondata = {inputjsondata}")

        # change members selection
        inputjsondata['members'] = self.memselecchkbxvar
        print(f"8) Data in members: {inputjsondata['members']}")

        # change config method
        inputjsondata['method'].append(configmethodvar.get())
        print(f"9) Just want the first key in method 3: {inputjsondata['method']}")

        # change commands
        inputjsondata['commands'] = cmdenryvar
        #()
        print(f"10) Just want the first key commands: {inputjsondata['commands']}")

        # dump the file back
        print(f"11) I am 'inputjsondata' raw: {inputjsondata}")

        # OK Lets try try to change the data
        with open(dest_path, 'w', encoding='utf-8') as f:
            json.dump(inputjsondata, f, ensure_ascii=False, indent=4)

        # Close the file
        filetoread.close()

        # Make sure every button and combox is nulled
        # Member BUTTON and Input combobox
        memselecchkbx.configure(state='disabled') # Member Input combobox
        memselecbtn.configure(state='disabled', fg_color="gray")
        # ConfigMethod Button and Combobox
        confmethodselec.configure(state='disabled', fg_color="gray") # Method Combobox
        confbtn.configure(state='disabled', fg_color="gray")
        # Notes textbox and button
        grpdesetry.configure(state='disabled', bg="gray") # Notes textbox
        grpdesbtn.configure(state='disabled', fg_color="gray") # Button
        # Add Button
        btnadd.configure(state='disabled', fg_color="gray") # Button Add

        ########################### Status feedback
        creategrpstatuslbl.configure(text=f"New Group ({groupname.get()}) has been created")


    def populatemembx():
        print("Off to get the ID's to populate the checkbox selection")
        print("I'm going to fetch the list of IDs from the DB")
        try:
            sqliteConnection = sqlite3.connect(dbfile)
            cursor = sqliteConnection.cursor()
            query = (f"SELECT id FROM devices")
            cursor.execute(query)
            record = cursor.fetchall()
            result_list = [row[0] for row in record]
            result_list = list(map(str, result_list))
            print(f"creategroup/populatemembx = {result_list}")
            memvaluesdb = result_list
            #self.memseleccbxvar = result_list
            #print(f"memvaluesdb = {memvaluesdb}")
            memselecchkbx.config(values=memvaluesdb)
        
        except sqlite3.Error as error:
            print("The error (connecttodb.py(GETIDSFROMDB)) message is: ", error)
            print("Exception class is: ", error.__class__)
            print("Exception is", error.args)
    
    def grpprofilename():
        print("Set group profile name")
        # populate the members box with values
        populatemembx()
        #cgouttxtbx.insert(INSERT, f"1) Group name: {grpnameetry.get()}\n")
        grpnameetry.configure(state=DISABLED)
        grpnameetry.configure(fg_color="gray64")
        print(f"1)The current working directory is : {os.getcwd()}")
        print(f"2) The groupname is : {groupname.get()}")

        groudevicepath = os.path.join(devicegroups, groupname.get())

        if os.path.exists(groudevicepath):
            #print(f"Device already exists {groupname.get()}")
            grpnameetry.configure(state=NORMAL, fg_color="yellow2")
            messagebox.showinfo(title='Create Group', message=f'Group already exists: {groupname.get()}', icon='warning', parent=rwindow)


        else:
            print("Device doesn't exist")
            print(f"The devicepath directory is : {str(groudevicepath)}")
            # create file in project directory
            src_path = os.path.join(devicegroups, "jsonTemplate.json")
            dest_path = os.path.join(groudevicepath, groupname.get() + ".json")

        ####################################################################################
        # AT THIS POINT CREATE A Directory "C:\\Shared\\NetDevApp3\\cisco12ct\\devicegroups\\"
        # Also a blank template file .json is needed
        ####################################################################################

            if not os.path.exists(groudevicepath):
                os.mkdir(groudevicepath)
                print(f"New directory created : {groudevicepath}")

            print(f"sourcepath = {src_path}")
            print(f"desinationpath = {dest_path}")

            try:
                shutil.copy(src_path, dest_path)
                print("File copy was successfull")
            except:
                print("file copy failed")
        
        # read a file with parameters
        # Read file and load into memory
            filetoread = open(dest_path)
            inputjsondata = json.load(filetoread)
            inputjsondata['devicegroup']['groupname'] = groupname.get()
            print(f"1) I am 'inputjsondata' raw: {inputjsondata}")
            print(f"Try this see wahat happens: {inputjsondata}")
            print(f"Type of 'groupcomboboxoptions': {type(self.groupcomboboxoptions)}")
        #self.memseleccbxvar.append(groupname.get())
        #self.memseleccbxvar

        # OK Lets try try to change the data
            with open(dest_path, 'w', encoding='utf-8') as f:
                json.dump(inputjsondata, f, ensure_ascii=False, indent=4)
        
        # write to file with parameters
            print("json File altered(creategroup)")

        # Close the file
            filetoread.close()

        # Now activate the rest of the buttons
            cgouttxtbx.configure(state=NORMAL)
            cgouttxtbx.insert(INSERT, f"1) Group Created: {grpnameetry.get()}\n")
            cgouttxtbx.configure(state=DISABLED)
            grpnameetry.configure(state=DISABLED) #disabledbackground="green yellow"
            grpnamebtn.configure(state=DISABLED, fg_color="gray", text="Accepted")
            memselecbtn.configure(state=NORMAL, fg_color="green")
            memselecchkbx.configure(state='readonly')
            memselectlbl.configure(state=NORMAL)
            conflbl.configure(state=NORMAL)
            confbtn.configure(state=NORMAL, fg_color="green")
            confmethodselec.configure(state='readonly', fg_color="PaleGreen2", border_color='dark slate gray', button_color='dark slate gray')
            grpdesbtn.configure(state=NORMAL, fg_color="green")
            grpdesetry.configure(state=NORMAL)
            grpdesclbl.configure(state=NORMAL)
            grpdesetry.configure(background="light yellow")
        
            btnadd.configure(state=NORMAL, fg_color="green")
        


    def memselectfun():
        global memselecchkbxvar
        print("I am memselectfun")
        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, f"2) Members selected: {memselecchkbx.get()}\n")
        cgouttxtbx.configure(state=DISABLED)
        print(type(memselecchkbx.get()))
        self.memselecchkbxvar = memselecchkbx.get()
        print(f"memselecchkbxvar value is : {self.memselecchkbxvar}")

    def confmethodselect():
        print("I am confmethodselect")
        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, f"3) Config Method: {confmethodselec.get()}\n")
        cgouttxtbx.configure(state=DISABLED)
        configmethodvar.set(confmethodselec.get())
        print(f"configmethodvar value is : {configmethodvar.get()}")

    def grpcmdstxtbx():
        global cmdenryvar
        print("I am grpcmdstxtbx")
        inp = grpdesetry.get(1.0, "end-1c")
        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, "4) Notes/Commands: " + "\n"+inp)
        cgouttxtbx.configure(state=DISABLED)
        cmdenryvar =  inp.splitlines()
        print(f"inp={inp}")
        print(f"cmdenryvar={cmdenryvar}")
        #cgouttxtbx.insert(INSERT, cmdenryvar)



    #rwindow.grid_rowconfigure(0, weight=1)
    rwindow.grid_columnconfigure(0, weight=1)
    # device name
    createlabel = ctk.CTkLabel(rwindow, text="Create a new Device Group", font=('arial', 22, 'bold'))
    createlabel.grid(row=0, column=0,sticky=EW, columnspan=3, pady=(20,16))
    separator1 = ttk.Separator(rwindow, orient='horizontal')
    separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=10)
    
    # GROUP NAME
    grpname = ctk.CTkLabel(rwindow, text="Group name", font=('arial', 18, 'bold'))
    grpname.grid(row=2, column=0,sticky=W, padx=25, pady=10)
    grpnameetry = ctk.CTkEntry(rwindow, font=('arial', 14, 'bold'), fg_color="yellow2", justify='center', textvariable=groupname)
    grpnameetry.grid(row=2, column=1,sticky=EW, padx=10, pady=10)
    grpnamebtn = ctk.CTkButton(rwindow, text="Set", command=grpprofilename, width=100, fg_color="green", hover_color='green4', font=('arial', 12, 'bold'))
    grpnamebtn.grid(row=2, column=2, padx=30, pady=10) # the rest inherit padx=30
    grpnameetry.configure({"background": "PaleGreen2"})


    # MEMBER SELECTION
    memselectlbl = ctk.CTkLabel(rwindow, text="Member Selection", font=('arial', 18, 'bold'), state=DISABLED)
    memselectlbl.grid(row=3, column=0, sticky=W, padx=25, pady=10)
    memselecchkbx = ChecklistCombobox(rwindow, values=memvaluesdb, font=('arial 12 bold'), state='disabled', checkbutton_height=3, height=12, style='TCombobox')
    memselecchkbx.grid(row=3, column=1,sticky=EW, padx=10, pady=10)
    memselecbtn = ctk.CTkButton(rwindow, text="Set", command=memselectfun, state=DISABLED, width=100, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'))
    memselecbtn.grid(row=3, column=2)
    
    # CONFIGURATION COMBOBOX SELECTION
    conflbl = ctk.CTkLabel(rwindow, text="Config Method", font=('arial', 18, 'bold'), state=DISABLED)
    conflbl.grid(row=4, column=0,sticky=W, padx=25, pady=10)
    confmethodselec = ctk.CTkComboBox(rwindow, values=self.cmdcomboboxoptions, state='disabled', font=('arial', 14, 'bold'), dropdown_fg_color='PaleGreen2', dropdown_hover_color='PaleGreen3')
    confmethodselec.grid(row=4, column=1,sticky=EW, padx=10, pady=10)
    confbtn = ctk.CTkButton(rwindow, text="Set", command=confmethodselect, state=DISABLED, width=100, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'))
    confbtn.grid(row=4, column=2)

            

    # device description
    grpdesclbl = ctk.CTkLabel(rwindow, text="Notes", font=('arial', 18, 'bold'), state=DISABLED)
    grpdesclbl.grid(row=5, column=0,sticky=NW, padx=25, pady=10)
    
    #grpdesetry = Text(rwindow, font='arial 14', height = 10, width = 25, bg="light yellow", wrap=WORD)
    grpdesetry = scrolledtext.ScrolledText(rwindow, font='arial 12', height = 10, width = 25, bg="gray70", wrap=WORD, state=DISABLED)
    grpdesetry.grid(row=6, column=0,sticky=EW, padx=(25, 10), pady=10, columnspan=2)
    grpdesbtn = ctk.CTkButton(rwindow, text="Set", command=grpcmdstxtbx, state=DISABLED, width=100, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'))
    grpdesbtn.grid(row=6, column=2,sticky=S, padx=10, pady=10) 


    
    separator2 = ttk.Separator(rwindow, orient='horizontal')
    separator2.grid(row=7, sticky=EW, columnspan=3, padx=20, pady=10)
    btnadd = ctk.CTkButton(rwindow, text="Add", state=DISABLED, command=lambda:changegroupfile(self, *args, **kwargs), fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'))
    btnadd.grid(column=0, row=8, pady=10)
    btnexit = ctk.CTkButton(rwindow, text="EXIT", command=rwindow.destroy,  fg_color="red2", hover_color='red3', font=('arial', 12, 'bold'))
    btnexit.grid(column=1, row=8, pady=10, padx=25)
    cgouttxtbx = scrolledtext.ScrolledText(rwindow, font='arial 10', height = 10, width = 25, bg="PaleGreen2", wrap=WORD, state=DISABLED)
    cgouttxtbx.grid(row=9, column=0,sticky=EW, padx=(25, 25), pady=10, columnspan=3)

    creategrpstatuslbl = Label(rwindow, text="", font=('arial', 14, 'bold'), bg="powder blue", fg='OrangeRed2')
    creategrpstatuslbl.grid(row=10, column=0, sticky=W, padx=(30, 20), pady=10, columnspan=3)
    