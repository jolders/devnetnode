from settings import *
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import *
from PIL import ImageTk, Image
from devicecrud import fetchalldb, createdevice, changedbdevice, deletedbdevice
from connecttodb import getdevicefromid
from cmdframebox import showcmdframe
from filesdb import saveframeoutput
from sshservices import runcmdparamiko, runcmdnetmiko, runcmdnetmiko_ch, runcmdnetmiko_ch_config
from sshservicesgrp import runcmdparamikogrp, runcmdnetmikogrp, runcmdnetmikogrp_ch
from creategroup import createnewgroup
import os
from editgroups import editthisgroup
from deletegroup import delgroup
from backuptftp import tftpdevicebackup # tftpsaveconfig,
from backuptftpgrp import backupgrouptftp # tftpsaveconfiggrp
from uploadtftp import configuploadtftp
from uploadtftpgroup import configuploadtftpgroup

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        ## Setting up Initial Things
        self.title("DevNetNode")
        self.geometry("1400x750+50+50")
        self.resizable(True, True)
        self.minsize(1100,550)
        self.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))
        # self.iconbitmap('/Shared/NetDevApp3/cisco12ct/pythonicon.ico')

        # The selected device on the treeview
        self.iam_selecteddevice = tk.IntVar(self)
        # Used in Status bar with a value like Device ID or Group ID
        self.devicestatus = tk.StringVar(self, value=f"Device ID: ")
        # Status bar with a value like 5(selected index) or RTR1 (selected group)
        self.statusvargrp = tk.StringVar(self)
        # Group switch variable on self.topframea
        self.groupswitch_var = tk.StringVar(value="off")
        self.statusvarcmd = tk.StringVar(self, value="(Unselected)") # StatusLabel 'Paramiko', 'Netmiko', 'Netmiko_ch', 'Netmiko_ch_config', 'other-3'
        self.statusvarcmd2 = tk.StringVar(self, value="(Unselected)") # # StatusLabel 'sh ip int bri'

        self.groupcomboboxoptions = [] # 'Group1', 'Group2', 'Group3', 'Group4', 'Group5'
        self.groupoptionselected = tk.StringVar(self)

        self.cmdcomboboxoptions = ['Paramiko', 'Netmiko', 'Netmiko_ch', 'Netmiko_ch_config', 'Another ?']
        self.cmdmethodselected = tk.StringVar(self) # Netmiko

        self.cmdvarselected = tk.StringVar(self) # show interface gigabitEthernet 0/0

        self.returnedname = tk.StringVar(self) # Floating variable with hostname properties (RTR1)


        def createnewdevice(self): 
            self.cdwindow = ctk.CTkToplevel()
            # self.cdwindow.grab_set() # Problems on linux
            createdevice(self, self.cdwindow)

        def changethisdevice(self):
            print(f"Printing changethisdevice function={self.iam_selecteddevice.get()}")
            self.rdwindow = ctk.CTkToplevel()
            # self.rdwindow.grab_set() # Problems on linux
            changedbdevice(self, self.rdwindow, self.iam_selecteddevice.get())

        def deletethisdevice(self):
            print(f"Printing deletethisdevice function={self.iam_selecteddevice.get()}")
            deletedbdevice(self, self.iam_selecteddevice.get())

        def printstuff(self):
            print(f"1) printstuff self.iam_selecteddevice = {self.iam_selecteddevice.get()}")
            print(f"2) printstuff self.statusvargrp = {self.statusvargrp.get()}")
            print(f"3) printstuff self.groupoptionselected = {self.groupoptionselected.get()}")
            print(f"3) printstuff self.cmdmethodselected = {self.cmdmethodselected.get()}")

        def groupswitch_event(self):
            #print(f"Groupswitch_event value is :{self.groupswitch_var.get()}")
            #self.statusvargrp.set(self.groupswitch_var.get())
            self.groupcomboboxoptions = []
            listgroupnames(self)
            
            if self.groupswitch_var.get() == "on":
                self.devicestatus.set("Selected Group : ")
                self.statusvargrp.set(self.grpcombobox.get())
                self.iam_selecteddevice.set(0)
                # work needed to disable the frame showing the tree view database of devices
                self.grpcombobox.configure(state='readonly')
                self.grpcombobox.configure(fg_color='yellow2')
                self.grpcombobox.configure(values=self.groupcomboboxoptions)
                self.groupoptionselected.set(self.grpcombobox.get()) # put combobox value into var
                self.createa.configure(state='disabled')
                self.updatea.configure(state='disabled')
                self.deletea.configure(state='disabled')
                
                # Makes selection in tree view inactive and look inactive
                self.tree.bind('<Button-1>', 'break') 
                self.tree.bind('<MouseWheel>', 'break')
                self.vsb.config(command="")
                style = ttk.Style()
                style.configure("db.Treeview", background="gray64", relief="flat", rowheight="25")
                style.configure("db.Treeview.Heading", background="gray64", foreground="black", font=('Helvetica 10 bold'))
                style.map("Treeview", background=[('selected', "gray45")])
                self.tree.bind("<Button-3>", 'break')

            else:
                print("switch value is false")
                self.devicestatus.set(f"Device ID: ")
                self.grpcombobox.configure(state='disabled')
                self.grpcombobox.configure(fg_color='light goldenrod yellow')
                #self.grpcombobox.set('') #THIS NEEDS WORK ON
                self.iam_selecteddevice.set(self.tree.item(self.tree.selection())['values'][0])
                #self.cmdmethodselected.set('') self.groupoptionselected
                self.createa.configure(state='normal')
                self.updatea.configure(state='normal')
                self.deletea.configure(state='normal')
                
                # Makes selection in tree view active and look active
                self.tree.unbind('<Button-1>') 
                self.tree.unbind('<MouseWheel>')
                self.vsb.config(command=self.tree.yview)
                
                style = ttk.Style()
                style.theme_use("clam")
                style.configure("db.Treeview", background="pale green", relief="flat", rowheight="25")
                style.configure("db.Treeview.Heading", background="PaleGreen3", foreground="black", font=('Helvetica 10 bold'))
                style.map("Treeview", background=[('selected', "PaleGreen4")])
                
                self.option_add("*TCombobox*Listbox*Background", 'pale green') # Background of dropdown selectbox
                self.option_add('*TCombobox*Listbox*Foreground', 'black') # Text colour of items in dropdown
                self.option_add('*TCombobox*Listbox*selectBackground', 'PaleGreen4') # Highlight selection
                self.option_add('*TCombobox*Listbox*selectForeground', 'white') # Test Highlight selection on dropdown
                self.option_add("*TCombobox*Listbox*Font", 'Helvetica 10 bold')

                style.map('TCombobox', fieldbackground=[('readonly','PaleGreen2')]) # field background empty
                style.map('TCombobox', selectbackground=[('readonly', 'PaleGreen2')]) # field background being filled bu numbers
                style.map('TCombobox', selectforeground=[('readonly', 'black')]) # Text numbers 5,7,9
                #style.map('TCombobox', fieldbackground=[('disabled','gray20')]) # field background empty
                style.map('TCombobox', selectbackground=[('disabled', 'gray20')]) # field background being filled bu numbers
                #style.map('mcbx.TCombobox', selectbackground=[('disabled', 'gray20')])
        
        def runcmdselection(self):
            print(f"The value of varselected is: {self.iam_selecteddevice.get()}")
            #self.statuslblcmd.set("Connecting.......(runcmdselection)") # doesnt feedback in a timely manner
            #print(f"3) runcmdselection self.statusvargrp = {self.statusvargrp.get()}")
            
            if self.groupswitch_var.get() == 'off':
                print(f"1) runcmdselection self.groupswitch_var (OFF) = {self.groupswitch_var.get()}")
                print(f"2) runcmdselection self.iam_selecteddevice (#VALUE) = {self.iam_selecteddevice.get()}")
                print(f"3) runcmdselection self.cmdmethodselected = {self.cmdmethodselected.get()}")
                print(f"4) runcmdselection self.cmdvarselected = {self.cmdvarselected.get()}")
                print(f"Printing load device def iam_selecteddevice = {self.iam_selecteddevice.get()}'")
                # pass required vars to sshservices
                if self.cmdmethodselected.get() == "Paramiko":
                    print (f"Paramiko will be used to run '{self.iam_selecteddevice.get()}' ")
                    runcmdparamiko(self, self.iam_selecteddevice.get())
                if self.cmdmethodselected.get() == "Netmiko":
                    print (f"Netmiko will will be used to run '{self.iam_selecteddevice.get()}' ")
                    runcmdnetmiko(self, self.iam_selecteddevice.get())
                if self.cmdmethodselected.get() =="Netmiko_ch":
                    print (f"Netmiko.connectionHandler will will be used to run '{self.iam_selecteddevice.get()}' ")
                    runcmdnetmiko_ch(self, self.iam_selecteddevice.get())
                if self.cmdmethodselected.get() == "Netmiko_ch_config":
                    # set commands are not relevant so allow input into textbox
                    print (f"Netmiko_ch_config will will be used to run '{self.iam_selecteddevice.get()}' ")
                    runcmdnetmiko_ch_config(self, self.iam_selecteddevice.get())
                

            elif self.groupswitch_var.get() == 'on':
                print(f"1) runcmdselection self.groupswitch_var (ON) = {self.groupswitch_var.get()}")
                print(f"2) runcmdselection self.iam_selecteddevice (#VALUE=0) = {self.iam_selecteddevice.get()}")
                print(f"2) The Group value is  (self.groupoptionselected) = {self.groupoptionselected.get()}")
                print(f"3) runcmdselection self.cmdmethodselected = {self.cmdmethodselected.get()}")
                print(f"4) runcmdselection self.cmdvarselected = {self.cmdvarselected.get()}")
                #self.statustext.set(self.varselected.get())
                if self.cmdmethodselected.get() == "Paramiko":
                    print (f"Paramiko 'grp' will be used to run on group: '{self.groupoptionselected.get()}' ")
                    print (f"Paramiko 'grp' runcmdparamikogrp (self.groupoptionselected.get())= '{self.groupoptionselected.get()}' ")
                    print (f"Paramiko 'grp' runcmdparamikogrp (self.cmdvarselected.get())= '{self.cmdvarselected.get()}' ")
                    runcmdparamikogrp(self, self.groupoptionselected.get(), self.cmdvarselected.get()) # sshservicesgrp.py
                if self.cmdmethodselected.get() == "Netmiko":
                    print (f"Netmiko 'grp' will will be used to run '{self.groupoptionselected.get()}' ")
                    runcmdnetmikogrp(self, self.groupoptionselected.get(), self.cmdvarselected.get())
                if self.cmdmethodselected.get() == "Netmiko_ch": # Netmiko with 'Connection Handler'
                    print (f"Netmiko_ch 'grp' will will be used to run '{self.groupoptionselected.get()}' ")
                    runcmdnetmikogrp_ch(self, self.groupoptionselected.get(), self.cmdvarselected.get())
                if self.cmdmethodselected.get() == "Netmiko_ch_config": # Netmiko with 'Connection Handler'
                    print (f"Netmiko_ch_config 'grp' will will be used to run '{self.groupoptionselected.get()}' ")
                    runcmdnetmikogrp_ch(self, self.groupoptionselected.get()) # , self.cmdvarselected.get()

            else:
                print("runcmdselection self.groupswitch_var = UNDEFINED")
     
        def newgroup():
            print("You have accessed 'newgroup' function")
            createnewgroup(self, *args, **kwargs)
        def editgroup():
            print("You have accessed 'editgroup' function")
            editthisgroup(self, *args, **kwargs)
        def deletegroup():
            print("You have accessed 'deletegroup' function")
            delgroup(self)
      
        def listgroupnames(self):
            os.chdir(directorypathroot)
            print(f"2) (listgroupnames(self)) The current working directory is : {os.getcwd()}")
            # groupdevicepath = os.path.join(str(directorypathroot) + "\\devicegroups")
            os.chdir(devicegroups)
            print(f"3) (listgroupnames(self)) The current working directory is : {os.getcwd()}")
            
            items = os.listdir(devicegroups)
            for item in items:
                if os.path.isdir(item):
                    self.groupcomboboxoptions.append(item)
            print(f"4) Directories (groupcomboboxoptions) = {self.groupcomboboxoptions}")
            print(f"5) (listgroupnames(self)) The current working directory is : {devicegroups}")

        def groupcombobox_callback(choice):
            print("groupcombobox dropdown clicked:", choice)
            self.groupoptionselected.set(choice)
            self.statusvargrp.set(choice)
        def cmdcombobox_callback(choice):
            print("cmdcombobox dropdown clicked:", choice)
            print("This is being used intead of show_frame")
            self.cmdmethodselected.set(choice)
            self.statusvarcmd.set(choice)
            showcmdframe(self, choice, *args, **kwargs)

        def tftpconfig(): # self, *args, **kwargs ? > backuptftp.py
            # repeat main.py(231) devicecrud.py(111)
            print(f"tftpconfig {self.iam_selecteddevice.get()}") #backupftp.py
            #tftpsaveconfig(self, self.iam_selecteddevice.get())
            tftpdevicebackup(self)
        
        def tftpconfiggrp(): # self, *args, **kwargs
            # backupftpgrp.py
            print("This is the tftpconfiggrp function in main")
            backupgrouptftp(self)
            
            '''
            if self.groupswitch.get() == 'on' and self.groupoptionselected.get() != "Group Selection":
                #print("Looks like you're good to go")
                print(f"Group selection = {self.groupoptionselected.get()}")
                tftpsaveconfiggrp(self, self.groupoptionselected.get())
            else:
                print("Looks like you've not selected to checkbox and group")
            '''
            
        
        def tftupload(): #self, *args, **kwargs ?
            print("I am tftupload")
            configuploadtftp(self) #uploadtftp.py
        
        def tftprestoregroup():
            print("I am tftprestoregroup")
            configuploadtftpgroup(self)


        listgroupnames(self)

        # ------ Menu Start ------
        myMenu1 = Menu(self)
        self.config(menu=myMenu1)
        
        fileMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.quit)

        deviceMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="Devices", menu=deviceMenu)
        deviceMenu.add_command(label="Create a new Device", command=lambda:createnewdevice(self))
        deviceMenu.add_separator()
        deviceMenu.add_command(label="Edit an exsisting Device", command=lambda:changethisdevice(self))
        deviceMenu.add_command(label="Delete selected Device", command=lambda:deletethisdevice(self))
        
        grpMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="Device Groups", menu=grpMenu)
        grpMenu.add_command(label="Create a new Group", command=newgroup)
        grpMenu.add_separator()
        grpMenu.add_command(label="Edit an exsisting Group", command=editgroup)
        grpMenu.add_command(label="Delete a Group", command=deletegroup)

        tftpMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="TFTP Backup & Restore", menu=tftpMenu)
        tftpMenu.add_command(label="Backup Device (TFTP)", command=tftpconfig)
        tftpMenu.add_command(label="Restore Device (TFTP)", command=tftupload)
        tftpMenu.add_separator()
        tftpMenu.add_command(label="Backup Group (TFTP)", command=tftpconfiggrp)
        tftpMenu.add_command(label="Restore Group (TFTP)", command=tftprestoregroup)
        
        
        versionMenu = Menu(myMenu1, tearoff=0)
        myMenu1.add_cascade(label="                                                                                                                                         Version 0.03 (beta)", menu=versionMenu)
        # ------ Menu END ------

        def topFrame(self):
            self.topframemain = ctk.CTkFrame(self, height=40)
            self.topframemain.pack(fill='x', side='top') # expand=TRUE
            self.topframemain.pack_propagate(False)

            self.topframea = ctk.CTkFrame(self.topframemain, height=40, fg_color="PaleGreen3")
            self.topframea.pack(fill='x', expand=True, side='left')
            self.topframea.pack_propagate(False)

            self.topframeb = ctk.CTkFrame(self.topframemain, height=40, fg_color="lightblue")
            self.topframeb.pack(fill='x', expand=True, side='left')
            self.topframeb.pack_propagate(False)

            # Label Placeholders
            #self.lbltopframea = ctk.CTkLabel(self.topframea, text="topframea").pack(side='left')
            #self.btntopframea = ctk.CTkButton(self.topframea, text="btntopframea", command=lambda:printvalues()).pack(side='left')
            #self.lbltopframeb = ctk.CTkLabel(self.topframeb, text="topframeb").pack()
            self.createa = ctk.CTkButton(self.topframea, text='Create', width=75, command=lambda:createnewdevice(self), fg_color='dark slate gray', 
                                         font=('arial', 12, 'bold'), hover_color='Gray24', border_width=3, border_color='dark slate gray')
            self.createa.pack(side='left', padx=5)
            self.updatea= ctk.CTkButton(self.topframea, text='Update', width=75, command=lambda:changethisdevice(self), fg_color='dark slate gray', 
                                        font=('arial', 12, 'bold'), hover_color='Gray24', border_width=3, border_color='dark slate gray')
            self.updatea.pack(side='left', padx=5)
            self.deletea = ctk.CTkButton(self.topframea, text='Delete', width=75, command=lambda:deletethisdevice(self), fg_color='dark slate gray', 
                                         font=('arial', 12, 'bold'), hover_color='Gray24', border_width=3, border_color='dark slate gray')
            self.deletea.pack(side='left', padx=5)

            # PRINTVALUE
            # self.printvalues = ctk.CTkButton(self.topframea, text='PRINTVALUE', width=25, command=lambda:printstuff(self))
            # self.printvalues.pack(side='left', padx=5)

            self.grpcombobox = ctk.CTkComboBox(self.topframea , width=170, height=20, font=('arial', 14, 'bold'), command=groupcombobox_callback, dropdown_fg_color='khaki', 
                                               dropdown_hover_color='khaki3', border_color='dark slate gray', button_color='dark slate gray')
            self.grpcombobox.pack(side='right', pady=5, padx=10) # values=self.cmdcomboboxoptions,
            self.grpcombobox.set("Group Selection")
            self.grpcombobox.configure(state='disabled')

            # Group switch on/off
            self.groupswitch = ctk.CTkSwitch(self.topframea, text="Group Switch", command=lambda:groupswitch_event(self), variable=self.groupswitch_var, 
                                             onvalue="on", offvalue="off", switch_width=40, switch_height=20, fg_color='khaki2', 
                                             button_color='dark slate gray', border_width=2, border_color='dark slate gray', progress_color='yellow')
            self.groupswitch.pack(side='right', pady=10, padx=(10,10))

            self.lblcmd = ctk.CTkLabel(self.topframeb, text=" CMD select: ").pack(side='left', padx=10)

            self.cmdcombobox = ctk.CTkComboBox(self.topframeb, width=170, height=20, values=self.cmdcomboboxoptions, font=('arial', 14, 'bold'), fg_color='yellow2', command=cmdcombobox_callback, dropdown_fg_color='khaki', 
                                               dropdown_hover_color='khaki3', border_color='dark slate gray', button_color='dark slate gray', button_hover_color='dark green') #, command=cmdcombobox_callback
            self.cmdcombobox.pack(side='left', pady=5, padx=10)
            self.cmdcombobox.set("Method Selection")
            # self.cmdcombobox.configure(state='disabled')

            def copy_select(): # copy selected text to clipboard
                global cmddata
                if self.cmdtxtbox.selection_get():
                    cmddata=self.cmdtxtbox.selection_get() # copy selected text to clipboard
                    print(f"Copy ={cmddata}")
                    self.clipboard_clear()
                    self.clipboard_append(cmddata)
            
            def paste_select():
                global data
                self.cmdtxtbox.insert(tk.END,self.clipboard_get()) # Paste data from clipboard

            self.btncopy = ctk.CTkButton(self.topframeb,text='Paste', width=30, command=lambda:paste_select()) # ,command=lambda:copy_select()
            self.btncopy.pack(side='right', padx=5)
            self.btnpaste = ctk.CTkButton(self.topframeb,text='Copy', width=30, command=lambda:copy_select()) # ,command=lambda:paste_select()
            self.btnpaste.pack(side='right', padx=5)
            # On startup disable the buttons
            self.btncopy.configure(state='disabled')
            self.btnpaste.configure(state='disabled')

            self.btnrun = ctk.CTkButton(self.topframeb, text='Run', width=130, fg_color='green4', hover_color='green', text_color='white', font=('arial', 14, 'bold'), 
                                        border_width=2, border_color='dark green', command=lambda:runcmdselection(self))
            self.btnrun.pack(pady=7)

        def dataframe(self):
            self.dataframemain = ctk.CTkFrame(master=self, height=259, fg_color="gray64") # (#259,285) Removes white line at bottom of treeview devices
            self.dataframemain.pack(fill='x', side='top') # The background strip runs accross the frame treeview and cmd area
            self.dataframemain.pack_propagate(False)

            self.devtblframea = ctk.CTkFrame(self.dataframemain, fg_color="green4") # Draws a boder arround the Devices treeview
            self.devtblframea.pack(fill='both', expand=True, side='left')
            self.devtblframea.pack_propagate(False)

            # This is where the list of commands are shown
            self.cmdframea = ctk.CTkFrame(self.dataframemain, height=100, fg_color="gray64")
            self.cmdframea.pack(fill='both', expand=True, side='left')
            self.cmdframea.pack_propagate(False)


            # Small strip at bottom of cmd selection box removed from app.
            #self.cmdframeb = ctk.CTkFrame(self.cmdframea, height=60, fg_color="light steel blue")
            #self.cmdframeb.pack(fill='x', expand=False, side='bottom')
            #self.cmdframeb.pack_propagate(False)

            # Label Placeholders
            #self.lbldevtblframea = ctk.CTkLabel(self.devtblframea, text="devtblframea").pack()
            self.lblcmdframea = ctk.CTkLabel(self.cmdframea, text="cmdframea").pack()
            #self.lblcmdframeb = ctk.CTkLabel(self.cmdframeb, text="cmdframeb").pack()

        def dataoutput(self):
            self.dataoutputa = ctk.CTkFrame(master=self, height=565, fg_color="gray64") # OUTPUT DATA AREA
            self.dataoutputa.pack(fill='both', expand=True, side='bottom')
            self.dataoutputa.pack_propagate(False)

            self.dataoutputb = ctk.CTkFrame(self.dataoutputa, height=40, fg_color="gray64")
            self.dataoutputb.pack(fill='x', expand=False, side='bottom')
            self.dataoutputb.pack_propagate(False)
            
            # Label Placeholders
            #self.lbldataoutputa = ctk.CTkLabel(self.dataoutputa, text="dataoutputa").pack()
            #self.lbldataoutputb = ctk.CTkLabel(self.dataoutputb, text="dataoutputb").pack()

            # FRAME 2 (BOTTOM FRAME OF PANNED WINDOW)
            self.txtcontent = scrolledtext.ScrolledText(self.dataoutputa, wrap=WORD, background='light goldenrod yellow') #, height=23, width=83
            self.txtcontent.pack(expand=TRUE, fill='both', padx=2, pady=2) # shows orange arround output
            self.txtcontent.pack_propagate(0)
            
            self.btnsaveoutput = ctk.CTkButton(self.dataoutputb, text='Save output', width=135, fg_color='dark slate gray', command=lambda: saveframeoutput(self), 
                                               font=('arial', 12, 'bold'), hover_color='Gray24', border_width=3, border_color='dark slate gray')
            self.btnsaveoutput.pack(side='left', padx=5)
            self.btnclearoutput = ctk.CTkButton(self.dataoutputb, text='Clear', width=105, fg_color='dark slate gray', command=lambda: self.txtcontent.delete("1.0", END), 
                                                font=('arial', 12, 'bold'), hover_color='Gray24', border_width=3, border_color='dark slate gray') # self.txtcontent.delete("1.0", END) cleartext
            self.btnclearoutput.pack(side='left', padx=5)

            #self.lblstatusoutputa = ctk.CTkLabel(self.dataoutputb, text="statusoutput").pack(side='right')
            self.lbldevicestatus = ctk.CTkLabel(self.dataoutputb, textvariable=self.devicestatus).pack(side='left', padx=(20,5)) # Device ID:
            self.lblstatusoutputgrp = ctk.CTkLabel(self.dataoutputb, textvariable=self.statusvargrp).pack(side='left', padx=(5,5))
            self.lblstatuscmd = ctk.CTkLabel(self.dataoutputb, text=" | Run Method: ").pack(side='left', padx=(5,5))
            self.lblstatusoutputcmd = ctk.CTkLabel(self.dataoutputb, textvariable=self.statusvarcmd).pack(side='left', padx=(5,20))
            self.lblstatuscmd2 = ctk.CTkLabel(self.dataoutputb, text=" | Run Command: ").pack(side='left', padx=(5,20))
            self.lblstatusoutputcmd2 = ctk.CTkLabel(self.dataoutputb, textvariable=self.statusvarcmd2).pack(side='left')

            self.btnexit = ctk.CTkButton(self.dataoutputb, text='Exit', width=85, fg_color='red3', command=self.destroy, font=('arial', 12, 'bold'), hover_color='red4', border_width=2, border_color='red4') # self.txtcontent.delete("1.0", END) cleartext
            self.btnexit.pack(side='right', padx=5)


        topFrame(self)
        dataframe(self)
        #bottomframe(self)
        dataoutput(self)

        try:
            fetchalldb(self, self.devtblframea, self.iam_selecteddevice)
        except:
            print("Unable to load database of devices")
        
        groupswitch_event(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()

    


