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


def editthisgroup(self, *args, **kwargs):
    ewindow = tkinter.Toplevel()
    ewindow.title("Register")
    ewindow.geometry('600x820+200+200')
    ewindow.configure(background='powder blue')
    ewindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

    groupname = StringVar(value="Your Group Name")
    
    # CONFIGURATION METHOD (Paramiko, netmiko etc.)
    configmethodvar = StringVar()
    
    # Member Select Combobar
    global memseleccbxvar
    memseleccbxvar = []

    # IDs of Members in the group
    global memidchkbxvar
    memidchkbxvar=[]
    global fvmemselec #floating ID's
    fvmemselec=[]

    # MeTHOD Select Combobar
    global methseleccbxvar
    methseleccbxvar = StringVar()

    memvaluesdb = []
    
    global cmdenryvar
    cmdenryvar = []

    print(f"1) This is edit group page the current working directory is : {os.getcwd()}")
    # os.chdir(directorypathroot)
    #  groupdevicepath = os.path.join(str(directorypathroot) + "\\devicegroups")
    os.chdir(devicegroups)
    items = os.listdir(devicegroups)
    for item in items:
        if os.path.isdir(item):
            memseleccbxvar.append(item)
            # print(f"Directories = {item}")
    print(f"2) memseleccbxvar value = {memseleccbxvar}")
    print(f"3) This is edit group page the current working directory is : {os.getcwd()}")

    def onexitcleanup():
        # cleanup all values in vars for next group ?
        print("I am the exit routine onexitcleanup (editgroups)")
        ewindow.destroy()
    
    def callchangegroupfile(self, *args, **kwargs):
        if grpnamebtn.cget('state') == DISABLED and memselecbtn.cget('state') == DISABLED and confbtn.cget('state')==DISABLED and grpdesbtn.cget('state')==DISABLED:
            print(f"grpnamebtn.cget('state') =  {grpnamebtn.cget('state')}")
            print(f"memselecbtn.cget('state') =  {memselecbtn.cget('state')}")
            print(f"confbtn.cget('state') =  {confbtn.cget('state')}")
            print(f"grpdesbtn.cget('state') =  {grpdesbtn.cget('state')}")
            changegroupfile(self, *args, **kwargs)
        else:
            #print("something isnt right a button is not in disabled state")
            #ewindow.attributes('-topmost',True)
            #ewindow.lift()
            messagebox.showinfo("Please Set changes", "Please 'Set' changes to confirm details", parent=ewindow)
            #ewindow.lift()
            #ewindow.after(2000, ewindow.lift())


    def changegroupfile(self, *args, **kwargs):
        print(f"1a) called by ''callchangegroupfile'' (changegroupfile)")
        print(f"1b) The current working directory is (changegroupfile): {os.getcwd()}")
    

        # HERE WE GO 
        print(f"GO (Group name: {groupname.get()})")
        print(f"GO (Member Selection: {fvmemselec})")
        print(f"GO (Config Method: {configmethodvar.get()})")
        print(f"GO (Commands: {cmdenryvar})")

        # Get into the right folder
        groudevicepath = os.path.join(devicegroups, groupname.get())
        # load the file
        dest_path = os.path.join(groudevicepath, groupname.get() + ".json")
        filetoread = open(dest_path)
        inputjsondata = json.load(filetoread)
        print(f"Addbutton filetoread = {filetoread}")
        print(f"Addbutton inputjsondata = {inputjsondata}")

        # change members selection
        inputjsondata['members'] = fvmemselec
        print(f"8) Data in members: {inputjsondata['members']}")

        # change config method
        try:
            # So I think that a value already exist
            inputjsondata['method'][0] = confmethodselec.get() # confmethodselec.get()
            print(f"9) Value already exits so used the replace method 3: {inputjsondata['method']}")
        except:
            print("10) An error occured so trying a second method")
            try:
                print(f"9) Value doesn't exits method 3: {inputjsondata['method']}")
                inputjsondata['method'] = confmethodselec.get()
            except Exception as e:
                print(f"9a) (105) THIS ERROR NEEDS LOOKING AT : DIDNT WORK EITHER 3a: {inputjsondata['method']}")
                print(f"9a) (106) ERROR 3a: {str(e)}")

        else:
            print("9b) (109) So the 1st try = Looks like this works")
                



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

        btnadd.configure(state='disabled', fg_color='gray')

        editgrpstatuslbl.configure(text="Group Saved")

    def populatemembx(self, *args, **kwargs):
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
            print(result_list)
            memvaluesdb = result_list
            print(f"memvaluesdb = {memvaluesdb}")
            memselecchkbx.configure(values=memvaluesdb)

        
        except sqlite3.Error as error:
            print("The error (connecttodb.py(GETIDSFROMDB)) message is: ", error)
            print("Exception class is: ", error.__class__)
            print("Exception is", error.args)
        
    def grpcbxselc():
        global memselecchkbxvar
        global memseleccbxvar
        print("Set group profile name")
        groupname.set(grpnamecbx.get())
        print(f"1a) The current working directory is : {os.getcwd()}")
        print(f"2a) The groupname is : {groupname.get()}")
        groudevicepath = os.path.join(devicegroups, groupname.get())
        print(f"3a) The devicepath directory is : {str(groudevicepath)}")
        grpfilepath= os.path.join(groudevicepath, groupname.get() + ".json")
        print(f"4a) sourcepath = {grpfilepath}")
        grpfiletoread = open(grpfilepath)
        grpjsondata = json.load(grpfiletoread)
        print(f"1) I am 'inputjsondata' raw: {grpjsondata}")

        # # POPULATE THE MEMBERS IN THE GROUP SELECTION
        # THUS IS THE LIST OF ID's in the group
        print(f"7) Memberselection = {grpjsondata['members']}")
        memseleccbxvar = grpjsondata['members'] # Member Select Combobar
        print(f"8) Data in memseleccbxvar: {memseleccbxvar}")
        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, f"1) Current Group is : {groupname.get()}\n")
        cgouttxtbx.insert(INSERT, f"2) Current Members (memseleccbxvar) are: {memseleccbxvar}\n")
        
        # THIS LINE POPULATES THE 'Member Selection' Combobox with the saved group values from members
        memselecchkbx.set(memseleccbxvar)
        #memidchkbxvar = memselecchkbx.get()
        populatemembx(self, *args, **kwargs)
        print(f"8a) Data in memseleccbxvar: {memseleccbxvar}")
        
        # POPULATE THE METHOD SELECTION
        # method = netmiko, parimamiko etc
        methseleccbxvar = grpjsondata['method']
        print(f"9) Just want the first key in method 3: {grpjsondata['method']}")
        print(f"10) Just want the methseleccbxvar in method 3: {methseleccbxvar}")
        cgouttxtbx.insert(INSERT, f"3) Current Method is : {methseleccbxvar}\n")
        confmethodselec.configure(state='normal')
        confmethodselec.set(methseleccbxvar)
        confmethodselec.configure(state='readonly')



        # POPULATE THE COMMNDS SELECTION
        cmdenryvar = grpjsondata['commands']
        #cmdenryvar =  cmdenryvar.splitlines()
        print(f"11) The commands are cmdenryvar: {cmdenryvar}")
        # Command to populate the commans box here
        print ("\n".join(cmdenryvar))
        grpdesetry.config(state=NORMAL)
        cmdenryvar1 = "\n".join(cmdenryvar)
        grpdesetry.insert(INSERT, cmdenryvar1)
        cgouttxtbx.insert(INSERT, f"4) Notes : {cmdenryvar}\n")

        grpnamecbx.configure(state=DISABLED, fg_color='gray70', text_color_disabled='gray26')
        grpnamebtn.configure(text="Accepted", fg_color='gray', state=DISABLED)

        # Close the file
        grpfiletoread.close()

        # Now activate the rest of the buttons
        #grpnamebtn.configure(state=DISABLED)
        #grpname.configure(state=DISABLED)
        memselecbtn.configure(state=NORMAL, fg_color='green' )
        memselecchkbx.configure(state='readonly')
        memselectlbl.configure(state=NORMAL)
        conflbl.configure(state=NORMAL)
        confbtn.configure(state=NORMAL, fg_color='green')
        confmethodselec.configure(state='readonly', fg_color="pale green")
        grpdesbtn.configure(state=NORMAL, fg_color='green')
        grpdesetry.configure(state=NORMAL)
        grpdesclbl.configure(state=NORMAL)
        grpdesetry.configure(background="light yellow")
        
        btnadd.configure(state=NORMAL, fg_color='green')
        
    def memselectfun():
        global memidchkbxvar
        global fvmemselec
        memidchkbxvar = memselecchkbx.get()
        fvmemselec = []
        # Get the current combobox selected values
        if memselecchkbx.get() == '':
            print("memselecchkbx.get() is null")
            print(f"So use values: {memseleccbxvar}")
            cgouttxtbx.insert(INSERT, f"2) Remaines Unchanged Current Members: {memseleccbxvar}\n")
            fvmemselec = memseleccbxvar
        else:
            print("memselecchkbx.get() is not null")
            print(f"So use values: {memselecchkbx.get()}")
            cgouttxtbx.insert(INSERT, f"2) Changing Group Current Members to: {memselecchkbx.get()}\n")
            fvmemselec = memselecchkbx.get()
        
        # USE THIS VALUE TO SAVE TO THE FILE "fvmemselec"
        print(f"The floating variable for fvmemselec {fvmemselec}")
        
        #DISABLE THE MEMBER SECTION LINE
        memselectlbl.configure(state=DISABLED)
        memselecchkbx.configure(state=DISABLED) # Background Gray
        memselecbtn.configure(state=DISABLED, fg_color="gray", text="Accepted")
        #memselecbtn.configure()


    def confmethodselect():
        print("I am confmethodselect")
        cgouttxtbx.configure(state=NORMAL)
        cgouttxtbx.insert(INSERT, f"3) Config Method: {confmethodselec.get()}\n")
        cgouttxtbx.configure(state=DISABLED)
        configmethodvar.set(confmethodselec.get())
        print(f"configmethodvar value is : {configmethodvar.get()}")
        
        # USE configmethodvar AS VALUE
        # DESELECT LABEL, COMBOBOX , BUTTON
        conflbl.configure(state=DISABLED)
        confmethodselec.configure(state=DISABLED, fg_color='gray70', text_color_disabled='gray26')
        confbtn.configure(state=DISABLED, text="Accepted", fg_color="gray")


    def grpcmdstxtbx():
        global cmdenryvar
        print("I am grpcmdstxtbx")
        inp = grpdesetry.get(1.0, "end-1c")
        cgouttxtbx.config(state=NORMAL)
        cgouttxtbx.insert(INSERT, "4) Commands: " + "\n"+inp)
        cgouttxtbx.config(state=DISABLED)
        cmdenryvar =  inp.splitlines()
        print(f"inp={inp}")
        print(f"cmdenryvar={cmdenryvar}")
        #cgouttxtbx.insert(INSERT, cmdenryvar)

        # DESELECT LABEL, TEXTBOX , BUTTON
        grpdesetry.configure(bg="gray70")
        grpdesclbl.configure(state=DISABLED)
        grpdesetry.configure(state=DISABLED)
        grpdesbtn.configure(state=DISABLED, fg_color='gray', text="Accepted")

        #########################################################
        # IF BUTTON MEMBER AND BUTTON CONFIG AND NOTES BUTTON = DISABLED ACTIVATE SET CHANGES OPTION
        #########################################################

######################## none of this styling works
    style = ttk.Style()
    style.theme_use("clam")
    self.option_add("*TCombobox*Listbox*Background", 'pale green') # Background of dropdown selectbox
    self.option_add('*TCombobox*Listbox*Foreground', 'black') # Text colour of items in dropdown
    self.option_add('*TCombobox*Listbox*selectBackground', 'PaleGreen4') # Highlight selection
    self.option_add('*TCombobox*Listbox*selectForeground', 'white') # Test Highlight selection on dropdown
    self.option_add("*TCombobox*Listbox*Font", 'Helvetica 10 bold')

    style.map('TCombobox', fieldbackground=[('readonly','PaleGreen2')]) # field background empty
    style.map('TCombobox', selectbackground=[('readonly', 'PaleGreen2')]) # field background being filled bu numbers
    style.map('TCombobox', selectforeground=[('readonly', 'black')])
    style.map('TCombobox', selectbackground=[('disabled', 'gray20')])


    ewindow.grid_columnconfigure(0, weight=1)
    # device name
    createlabel = ctk.CTkLabel(ewindow, text="Edit a device group", font=('arial', 22, 'bold'))
    createlabel.grid(row=0, column=0,sticky=EW, columnspan=3, pady=(20,16))
    separator1 = ttk.Separator(ewindow, orient='horizontal')
    separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=10)
    
    # GROUP NAME (Group1, London Routers, WestCoastSwitches)
    grpname = ctk.CTkLabel(ewindow, text="Group name", font=('arial', 18, 'bold'))
    grpname.grid(row=2, column=0,sticky=W, padx=25, pady=10)
    grpnamecbx = ctk.CTkComboBox(ewindow, values=memseleccbxvar,  font=('arial', 14, 'bold'), fg_color="pale green")
    grpnamecbx.grid(row=2, column=1,sticky=EW, padx=10, pady=10)
    grpnamecbx.set("select Group to edit")
    grpnamebtn = ctk.CTkButton(ewindow, text="Set", command=grpcbxselc, width=100, fg_color="green", hover_color='green4')
    grpnamebtn.grid(row=2, column=2, padx=30, pady=10)


    # MEMBER SELECTION
    memselectlbl = Label(ewindow, text="Member Selection", font='arial 14 bold', bg="powder blue", fg='black', state=DISABLED)
    memselectlbl.grid(row=3, column=0 ,sticky=W, padx=25, pady=10)
    memselecchkbx = ChecklistCombobox(ewindow, values=memvaluesdb, font=('arial 12 bold'), state='disabled', checkbutton_height=3, height=12, style='TCombobox')
    memselecchkbx.grid(row=3, column=1,sticky=EW, padx=10, pady=10)
    memselecbtn = ctk.CTkButton(ewindow, text="Set", command=memselectfun, state=DISABLED, width=100, fg_color="gray", hover_color='green4')
    memselecbtn.grid(row=3, column=2, padx=30, pady=10)
    
    # CONFIGURATION COMBOBOX SELECTION
    conflbl = Label(ewindow, text="Config Method", font='arial 14 bold', bg='powder blue', fg='black', state=DISABLED)
    conflbl.grid(row=4, column=0,sticky=W, padx=25, pady=10)
    #confoptions = ['Paramiko', 'Netmiko', 'Netmiko_ch', 'Netmiko_ch_config', 'other-3']
    confmethodselec = ctk.CTkComboBox(ewindow, values=self.cmdcomboboxoptions, state='disabled', font=('arial', 14, 'bold'))
    confmethodselec.grid(row=4, column=1,sticky=EW, padx=10, pady=10)
    confbtn = ctk.CTkButton(ewindow, text="Set", command=confmethodselect, state=DISABLED, width=100, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'))
    confbtn.grid(row=4, column=2, padx=30, pady=10)   

    # device description
    grpdesclbl = Label(ewindow, text="Notes", font='arial 14 bold', bg='powder blue', fg='black', state=DISABLED)
    grpdesclbl.grid(row=5, column=0,sticky=NW, padx=25, pady=10)
    
    #grpdesetry = Text(ewindow, font='arial 14', height = 10, width = 25, bg="light yellow", wrap=WORD)
    grpdesetry = scrolledtext.ScrolledText(ewindow, font='arial 12', height = 10, width = 25, bg="gray70", wrap=WORD, state=DISABLED)
    grpdesetry.grid(row=6, column=0, sticky=EW, padx=(25, 10), pady=10, columnspan=2)
    grpdesbtn = ctk.CTkButton(ewindow, text="Set", command=grpcmdstxtbx, state=DISABLED, width=100, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'))
    grpdesbtn.grid(row=6, column=2, sticky=S, padx=30, pady=10) 


    separator2 = ttk.Separator(ewindow, orient='horizontal')
    separator2.grid(row=7, sticky=EW, columnspan=3, padx=20, pady=10)
    btnadd = ctk.CTkButton(ewindow, text="Set changes", state=DISABLED, width=100, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'), command=lambda:callchangegroupfile(self, *args, **kwargs))
    btnadd.grid(column=0, row=8, pady=10)
    btnexit = ctk.CTkButton(ewindow, text="EXIT", width=100, fg_color="red2", hover_color='red3', font=('arial', 12, 'bold'), command=onexitcleanup)
    btnexit.grid(column=1, row=8, pady=10, padx=25)
    cgouttxtbx = scrolledtext.ScrolledText(ewindow, font='arial 10', height = 10, width = 25, bg="PaleGreen2", wrap=WORD, state=DISABLED)
    cgouttxtbx.grid(row=9, column=0,sticky=EW, padx=(25, 25), pady=10, columnspan=3)

    editgrpstatuslbl = Label(ewindow, text="", font=('arial', 14, 'bold'), bg="powder blue", fg='OrangeRed2')
    editgrpstatuslbl.grid(row=10, column=0, sticky=W, padx=(30, 20), pady=10, columnspan=3)


    if grpnamebtn.cget("state") == DISABLED:
        print("grpnamebtn(state='disabled')")
