import sqlite3
from tkinter import *
import tkinter as tk
from tkinter.ttk import Treeview
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
import customtkinter as ctk
from settings import *
from PIL import ImageTk, Image
#from backuptftpgrp import tftpsaveconfiggrp
# from uploadtftp import configuploadtftp
import os


# Collect and display the devices database
def fetchalldb(self, devtblframea, iam_selecteddevice):
    devtblframea = self.devtblframea
    # print("I am fetchalldb.py")
    # Treeview styling
    style = ttk.Style()
    style.theme_use("clam") #'aqua', 'step', 'clam', 'alt', 'default', 'classic'
    style.configure("db.Treeview", background="pale green", relief="flat", rowheight="25")
    style.configure("db.Treeview.Heading", background="PaleGreen3", foreground="black", font=('Helvetica 10 bold'))
    style.configure("dbgray.Treeview", background="gray60", relief="flat", rowheight="25")
    style.configure("dbgray.Treeview.Heading", background="gray50", foreground="black", font=('Helvetica 10 bold'))
    ttk.Style().map("dbgray.Treeview.Heading", background = [('active', "gray40")])
    ttk.Style().map("Treeview.Heading", background = [('pressed', '!focus', "SlateGray3"),('active', "chartreuse3"),('disabled', '#ffffff')])
    style.map("Treeview", background=[('selected', "PaleGreen4")])

    self.my_canvas = Canvas(self.devtblframea)
    self.my_canvas.pack(side="left", fill=BOTH, expand=1, padx=2, pady=2) # shows a border arround the treeview devices "yellow"
    self.tree = ttk.Treeview(self.my_canvas, selectmode='browse', style="db.Treeview") 
    self.tree.pack(side="bottom", fill=BOTH, expand=1) #side='left', expand=TRUE, fill=BOTH, anchor=NW
    #tree.pack_propagate(0)
    self.vsb = ttk.Scrollbar(self.devtblframea, orient="vertical", command=self.tree.yview) #width=20
    self.vsb.pack(side='right', expand=FALSE, fill=BOTH, anchor=NW)
    #vsb.pack_propagate(0)
    self.tree.configure(yscrollcommand=self.vsb.set)

    con = sqlite3.connect(dbfile)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM devices")
    rows = cursor.fetchall()
    self.tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8")
    self.tree['show'] = 'headings'
    self.tree.column("1", width=5, anchor='c')
    self.tree.column("2", width=10, anchor='c')
    self.tree.column("3", width=10, anchor='c')
    self.tree.column("4", width=10, anchor='c')
    self.tree.column("5", width=10, anchor='c')
    self.tree.column("6", width=20, anchor='c')
    self.tree.column("7", width=20, anchor='c')
    self.tree.column("8", width=20, anchor='c')
    self.tree.heading("1", text="id")
    self.tree.heading("2", text="name")
    self.tree.heading("3", text="ip")
    self.tree.heading("4", text="username")
    self.tree.heading("5", text="password")
    self.tree.heading("6", text="description")
    self.tree.heading("7", text="type")
    self.tree.heading("8", text="golden")

    for item in self.tree.get_children():
        self.tree.delete(item)
        print("db table display deleted")

    #print(row)
    for record in rows:
        self.tree.insert("",'end', iid=record[0], values=(record[0],record[1],record[2],record[3],record[4],record[5][:22],record[6],record[7]))
    
    firstselec = self.tree.get_children()[0]
    print (f"1) fetchdb.py -The firstselect item is : {firstselec}")
    self.tree.selection_set(firstselec)
    cursor.close()
    con.close()
    
    def selectItem(a):
        #global iam_selecteddevice
        try:
            selected_item = self.tree.selection()
            treeview_id = self.tree.item(selected_item)['values'][0]
            #print(f"I am DEF selectItem {treeview_id}")
            self.iam_selecteddevice.set(value=treeview_id)
            #floatingiam.set(value=treeview_id)
            # statusvargrp is the status value on the statusoutput frame
            self.statusvargrp.set(str(self.iam_selecteddevice.get()))

        except:
            print("No selectItem error in fetchdb.py line 75")

    
    def rightClickMenu(event):
        print("1) devicecrud.py (rightClickMenu) Right click menu")

        def helloedit():
            print(f"hello! edit: {iam_selecteddevice.get()}")
            #changedbdevice(iam_selecteddevice)
            #print(f"Printing changethisdevice function={self.iam_selecteddevice.get()}")
            self.rdwindow = ctk.CTkToplevel()
            self.rdwindow.grab_set()
            changedbdevice(self, self.rdwindow, self.iam_selecteddevice.get())

        def hellodelete():
            print(f"hello! delete: {iam_selecteddevice.get()}")
            deletedbdevice(self, self.iam_selecteddevice.get())

        def hellocreate():
            print(f"hello! greate new device")
            self.cdwindow = ctk.CTkToplevel()
            self.cdwindow.grab_set()
            createdevice(self, self.cdwindow)

        def hellocreatedir():
            print(f"hello! delete: {iam_selecteddevice.get()}")
            getdevicename = []
            thisdevicename = ""
            getdevicename = self.tree.item(self.tree.focus())
            thisdevicename = getdevicename['values'][1]
            print(f"thisdevicename = {thisdevicename}")
            print(type(thisdevicename))


            devicepath = os.path.join(devicesaveddata, thisdevicename)
            print(f"2) The devicepath directory is (filesdb.py): {devicepath}")
            
            if not os.path.exists(devicepath):
                os.mkdir(devicepath)
                print(f"4) New directory created (filesdb.py): {devicepath}")
                messagebox.showinfo(parent=self.my_canvas, title='Directory creation', message=f'A directory was created.\n{devicepath}')
                return

            if os.path.exists(devicepath):
                messagebox.showinfo(parent=self.my_canvas, title='Directory creation', message=f'Directory already exists.\n(no creation necessary)\n{devicepath}')
                return

        
    # create a popup menu
    # print(event.x, event.y)
        rowID = self.tree.identify('item', event.x, event.y)
        rowIDrow = self.tree.identify_row(event.y)
        getdevicename = self.tree.item(self.tree.focus())
        thisdevicename = getdevicename['values'][1]
        print("Iam rowIDrow " + rowIDrow)
        if rowID:
            menu = Menu(self.devtblframea, tearoff=0)
            menu.add_separator()
            menu.add_command(label=f"Edit id:{rowID} ({thisdevicename})", command=helloedit)
            menu.add_command(label=f"Delete id:{rowID} ({thisdevicename})", command=hellodelete)
            menu.add_separator()
            menu.add_command(label=f"Create directory id:{rowID} ({thisdevicename})", command=hellocreatedir)
            menu.add_separator()
            menu.add_command(label=f"Create new device", command=hellocreate)
            #menu.add_command(label=f"Add to group ('id' {rowID})", command=groupadd)
            #menu.add_command(label=f"Download config from device ('id' {rowID})", command=tftpconfig)
            #menu.add_command(label=f"Upload config to device ('id' {rowID})", command=tftupload)

            self.tree.selection_set(rowID)
            self.tree.focus_set()
            self.tree.focus(rowID)
        # print("I am 3 " + rowID)
            #menu.post(event.x_root, event.y_root)
            menu.tk_popup(event.x_root, event.y_root)
            self.vsb.update()
        else:
            pass

    self.treebind = self.tree.bind("<<TreeviewSelect>>", selectItem)
    self.tree.bind("<Button-3>", rightClickMenu)
    #treebind = tree.bind("<<TreeviewSelect>>", selectItem)
    #treebind = tree.bind("<<TreeviewSelect>>", getselecteddevice2, add="+")
    ## tree.bind('<<TreeviewSelect>>', getselecteddevice)
    #tree.bind("<Button-3>", rightClickMenu)

# Destroy and re-create the devices database
def clear_all(self):
    #print("(fetchdb.py) clear_all has been accessed")
    try:
        for item in self.tree.get_children():
            self.tree.delete(item)
            self.tree.forget()
            self.vsb.forget()
            self.my_canvas.forget()
    except:
        print("(fetchdb.py) Exception")
    finally:
        # Recrete the fetchall command
        fetchalldb(self, self.devtblframea, self.iam_selecteddevice)

# Create new entry in the devices database
def createdevice(self, cdwindow):
    self.rname = StringVar(self)
    self.rip = StringVar(self)
    self.rusername = StringVar(self)
    self.rpassword = StringVar(self)
    self.rdescription = StringVar(self)
    self.rtype = StringVar(self)
    self.rgfilename = StringVar(self)

    #self.cdwindow = ctk.CTkToplevel()
    self.cdwindow.title("Register (createdevice)")
    self.cdwindow.geometry('500x720+200+200')
    self.cdwindow.attributes('-topmost', 'true')
    self.cdwindow.configure(fg_color="light blue")
    #self.after(250, lambda: self.iconbitmap('pythonicon.ico'))
    #cdwindow = ctk.toplevel_window.focus()
    #cdwindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))
    self.cdwindow.after(250, lambda: self.cdwindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon)))))
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self.createlabel = ctk.CTkLabel(self.cdwindow, text="Create a new device", font=("arial", 22, "bold"))
    self.createlabel.grid(row=0, column=0, sticky="ew", columnspan=3, pady=15)
    self.separator1 = ttk.Separator(self.cdwindow, orient='horizontal')
    self.separator1.grid(row=1, sticky="ew", columnspan=3, padx=(30, 30), pady=10)

    # device Name
    self.dbname = ctk.CTkLabel(self.cdwindow, text="Device name", font=("arial", 18, "bold"), justify='left')
    self.dbname.grid(row=2, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbname = ctk.CTkEntry(self.cdwindow, font=("arial", 14), justify='center', width=230, fg_color="light yellow", textvariable=self.rname) 
    self.ebdbname.grid(row=2, column=1, sticky='w', padx=(30, 30), pady=10)
    # device IP Address
    self.dbip = ctk.CTkLabel(self.cdwindow, text="IP Address", font=("arial", 18, "bold"), justify='left')
    self.dbip.grid(row=3, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbip = ctk.CTkEntry(self.cdwindow, font=("arial", 14), justify='center', width=230, fg_color="light yellow", textvariable=self.rip) #textvariable=rname
    self.ebdbip.grid(row=3, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Username
    self.dbusername = ctk.CTkLabel(self.cdwindow, text="Username", font=("arial", 18, "bold"), justify='left')
    self.dbusername.grid(row=4, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbusername = ctk.CTkEntry(self.cdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.rusername) #textvariable=rname
    self.ebdbusername.grid(row=4, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Password
    self.dbpassword = ctk.CTkLabel(self.cdwindow, text="Password", font=("arial", 18, "bold"), justify='left')
    self.dbpassword.grid(row=5, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbpassword = ctk.CTkEntry(self.cdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.rpassword) #textvariable=rname
    self.ebdbpassword.grid(row=5, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Description
    self.dbdescription = ctk.CTkLabel(self.cdwindow, text="Description", font=("arial", 18, "bold"), justify='left')
    self.dbdescription.grid(row=6, column=0, sticky='nw', padx=(30, 10), pady=10)
    self.ebdbdescription = ctk.CTkTextbox(self.cdwindow, font=("arial", 14), height=200, width=230, fg_color="light yellow", border_width=2, wrap='word') #textvariable=rname
    self.ebdbdescription.grid(row=6, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Type
    self.dbtype = ctk.CTkLabel(self.cdwindow, text="Type", font=("arial", 18, "bold"), justify='left')
    self.dbtype.grid(row=7, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbtype = ctk.CTkEntry(self.cdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.rtype) #textvariable=rname
    self.ebdbtype.grid(row=7, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Goldern filename
    self.dbgfilename = ctk.CTkLabel(self.cdwindow, text="Goldern filename", font=("arial", 18, "bold"), justify='left', text_color="gray")
    self.dbgfilename.grid(row=8, column=0, sticky='w', padx=(30, 10), pady=10)
    self.btnfile = ctk.CTkButton(self.cdwindow, state="disabled", text="File select", font=("arial", 14), fg_color="gray", text_color="black")
    self.btnfile.grid(row=8, column=1, pady=10, padx=(30, 30))
    self.ebdbgfilename = ctk.CTkEntry(self.cdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.rgfilename)
    self.ebdbgfilename.grid(row=9, column=0, sticky='ew', padx=(30, 30), pady=10, columnspan=2)
    
    self.rgfilename.set(value="'Edit' device after creation")
    self.ebdbgfilename.configure(state='disabled', fg_color='gray70')
    
    self.separator2 = ttk.Separator(self.cdwindow, orient='horizontal')
    self.separator2.grid(row=10, sticky="ew", columnspan=3, padx=(30, 30), pady=10)
    self.btngo = ctk.CTkButton(self.cdwindow, text="Create", font=("arial", 14, "bold"), fg_color="green3", hover_color="green4", border_color='green4', border_width=2, text_color="black", command=lambda:insertdevice(self))# 
    self.btngo.grid(row=11, column=0, pady=10, padx=30, sticky='w')
    self.btnexit = ctk.CTkButton(self.cdwindow, text="EXIT", font=("arial", 14, "bold"), fg_color="orange red", hover_color="OrangeRed3", text_color="black", border_width=2, border_color='OrangeRed3', command=self.cdwindow.destroy)
    self.btnexit.grid(row=11, column=1, pady=10, padx=30, sticky='e')
    self.lblcds = ctk.CTkLabel(self.cdwindow, text="", font=("arial", 18, "bold"), justify='left')# 
    self.lblcds.grid(row=12, column=0, pady=10, padx=(30, 10), columnspan=2)

    '''
    def filedialogopen(self):
        print("filedialogopen")
        filename = askopenfilename(parent=self.cdwindow, title="Base File selection")
        print(f"filedialogopen = {filename}")
    '''

    def insertdevice(self):
        #self.lblcds.configure(text="Hello")
        #print(f"Hello 'dosomething' IamSelecteddevice {self.iam_selecteddevice}")
        self.btngo.configure(state="disabled", fg_color="gray", border_color='gray')

        try:
            sqliteConnection = sqlite3.connect(dbfile)
            cursor = sqliteConnection.cursor()
            #print("1) (createdevice.py) Successfull connection to db")
            query = "INSERT INTO devices (id,name,ip,username,password,description,type,golden) VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query,(str(self.ebdbname.get()),str(self.ebdbip.get()),str(self.ebdbusername.get()),str(self.ebdbpassword.get()),str(self.ebdbdescription.get('1.0','end-1c')),str(self.ebdbtype.get()),str(self.ebdbgfilename.get())))
            sqliteConnection.commit()
        except sqlite3.Error as error:
            self.lblcds.configure(text_color="red")
            self.lblcds.configure(text=f"Creation error: {error}")
            #print("The error message is: ", error)
            #print("Exception class is: ", error.__class__)
            #print("Exception is", error.args)
        finally:
            # Cleanup time
            if sqliteConnection:
                sqliteConnection.close()

            # Strip the variables down after use
            #self.rname.set("")
            #self.rip.set("")
            #self.rusername.set("")
            #self.rpassword.set("")
            #self.rdescription.set("")
            #self.rtype.set("")
            #self.rgfilename.set("")

            # Strip the entry boxes down after use
            #self.ebdbname.delete(0, END) # Device name
            #self.ebdbip.delete(0, END) # Device ip
            #self.ebdbusername.delete(0, END) # username
            #self.ebdbpassword.delete(0, END) # password
            #self.ebdbdescription.delete('1.0', END)
            #self.ebdbtype.delete(0, END) # type
            #self.ebdbgfilename.delete(0, END) # filename

            # Change text and entry boxe to gray
            self.ebdbname.configure(state='disabled', fg_color="light gray")
            self.ebdbip.configure(state='disabled', fg_color="light gray")
            self.ebdbusername.configure(state='disabled', fg_color="light gray")
            self.ebdbpassword.configure(state='disabled', fg_color="light gray")
            self.ebdbdescription.configure(state='disabled', fg_color="light gray")
            self.ebdbtype.configure(state='disabled', fg_color="light gray")
            self.ebdbgfilename.configure(state='disabled', fg_color="light gray")
            self.dbname.configure(text_color="gray40")
            self.dbip.configure(text_color="gray40")
            self.dbusername.configure(text_color="gray40")
            self.dbpassword.configure(text_color="gray40")
            self.dbdescription.configure(text_color="gray40")
            self.dbtype.configure(text_color="gray40")
            self.dbgfilename.configure(text_color="gray40")

            # Feedback to user on screen
            #self.lblcds.configure()
            self.lblcds.configure(text=" Device has been created. ", text_color="green4", bg_color="yellow2")
            #self.lblcds.configure()


            # Feedback to user by messagebox
            #msgboxname = str(self.ebdbname.get()) + " with IP address " + str(self.ebdbip.get())
            # messagebox.showinfo(title="New user created", message="Device " + str(msgboxname) + " has been created.")

            # Flush something to investigate ?
            #print(f"The value of self.trackingbool is :{self.trackingbool.get()}")
            clear_all(self)

        try:
            print("Create the directory structure here")
            devicepath = os.path.join(devicesaveddata, self.rname.get())
            if not os.path.exists(devicepath):
                os.mkdir(devicepath)
                print(f"4) New directory created (filesdb.py): {devicepath}")
        except Exception as error:
            print(f"ERROR (329) - {error}")
        finally:
            print("Running Finally")

# Change entry in the devices database
def changedbdevice(self, rdwindow, iam_selecteddevice):
    print(f"1 (changedbentry.py) changedbdevice : {iam_selecteddevice}")
    self.rdwindow.title("Update device details")
    self.rdwindow.geometry('500x740+200+200')
    self.rdwindow.attributes('-topmost', 'true')
    self.rdwindow.configure(fg_color="light blue")
    self.rdwindow.after(250, lambda: self.rdwindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon)))))
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    #self.result_id = IntVar(self)
    self.result_id=0
    #self.rname = StringVar(self, value="")
    self.changername = StringVar(self)
    #self.rip = StringVar(self, value="")
    self.changerip = StringVar(self)
    #self.rusername = StringVar(self, value="")
    self.changerusername = StringVar(self)
    self.changerpassword = StringVar(self)
    self.changerdescription = StringVar(self)
    self.changertype = StringVar(self)

    # self.rgfilename >(changedto)> self.rgfilename1
    self.rgfilename = tk.StringVar(self)

    self.createlabel = ctk.CTkLabel(self.rdwindow, text="Change device (id:", font=("arial", 22, "bold"))
    self.createlabel.grid(row=0, column=0,sticky="ew", columnspan=3, pady=(18, 8))
    self.separator1 = ttk.Separator(self.rdwindow, orient='horizontal')
    self.separator1.grid(row=1, sticky="ew", columnspan=3, padx=(30, 30), pady=10)
    self.createlabel.configure(text=self.createlabel.cget('text') + str(iam_selecteddevice) + ")")
    # device Name
    self.dbname = ctk.CTkLabel(self.rdwindow, text="Device name", font=("arial", 18, "bold"), justify='left')
    self.dbname.grid(row=2, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbname = ctk.CTkEntry(self.rdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.changername) 
    self.ebdbname.grid(row=2, column=1, sticky='w', padx=(30, 30), pady=10)
    #self.ebdbname.insert(0, "Hello")
    # device IP Address
    self.dbip = ctk.CTkLabel(self.rdwindow, text="IP Address", font=("arial", 18, "bold"), justify='left')
    self.dbip.grid(row=3, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbip = ctk.CTkEntry(self.rdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.changerip)
    self.ebdbip.grid(row=3, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Username
    self.dbusername = ctk.CTkLabel(self.rdwindow, text="Username", font=("arial", 18, "bold"), justify='left')
    self.dbusername.grid(row=4, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbusername = ctk.CTkEntry(self.rdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.changerusername)
    self.ebdbusername.grid(row=4, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Password
    self.dbpassword = ctk.CTkLabel(self.rdwindow, text="Password", font=("arial", 18, "bold"), justify='left')
    self.dbpassword.grid(row=5, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbpassword = ctk.CTkEntry(self.rdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.changerpassword)
    self.ebdbpassword.grid(row=5, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Description
    self.dbdescription = ctk.CTkLabel(self.rdwindow, text="Description", font=("arial", 18, "bold"), justify='left')
    self.dbdescription.grid(row=6, column=0, sticky='nw', padx=(30, 10), pady=10)
    self.ebdbdescription = ctk.CTkTextbox(self.rdwindow, font=("arial", 14), height=200, width=230, fg_color="light yellow", border_width=2, wrap='word') # self.changerdescription
    self.ebdbdescription.grid(row=6, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Type
    self.dbtype = ctk.CTkLabel(self.rdwindow, text="Type", font=("arial", 18, "bold"), justify='left')
    self.dbtype.grid(row=7, column=0, sticky='w', padx=(30, 10), pady=10)
    self.ebdbtype = ctk.CTkEntry(self.rdwindow, font=("arial", 14), justify='center', width= 230, fg_color="light yellow", textvariable=self.changertype)
    self.ebdbtype.grid(row=7, column=1, sticky='w', padx=(30, 30), pady=10)
    # device Goldern filename
    self.dbgfilename = ctk.CTkLabel(self.rdwindow, text="Golden config file", font=("arial", 18, "bold"), justify='left')
    self.dbgfilename.grid(row=8, column=0, sticky='ew', padx=(30, 10), pady=10)
    self.btnfile = ctk.CTkButton(self.rdwindow, text="File select", font=("arial", 14), text_color='white', fg_color="purple3", hover_color="purple4", border_color='purple4', border_width=2, command=lambda:filedialogopen(self))
    self.btnfile.grid(row=8, column=1, pady=10, padx=40)
    self.ebdbgfilename = ctk.CTkEntry(self.rdwindow, font=("arial", 14), justify='center', width=230, fg_color="light yellow", textvariable=self.rgfilename)
    self.ebdbgfilename.grid(row=9, column=0, sticky='ew', padx=(30, 30), pady=10, columnspan=2)
    self.ebdbgfilename.configure(state='disabled')
    
    self.separator2 = ttk.Separator(self.rdwindow, orient='horizontal')
    self.separator2.grid(row=10, sticky="ew", columnspan=3, padx=(30, 30), pady=10)
    self.btngo = ctk.CTkButton(self.rdwindow, text="Change", font=("arial", 14, "bold"), fg_color="green3", hover_color="green4", border_color='green4', border_width=2, text_color="black", command=lambda:dbconnectRegister(self, iam_selecteddevice))# 
    self.btngo.grid(row=11, column=0, pady=10, padx=(30, 10))
    self.btnexit = ctk.CTkButton(self.rdwindow, text="EXIT", font=("arial", 14, "bold"), fg_color="orange red", hover_color="OrangeRed3", text_color="black", border_width=2, border_color='OrangeRed3', command=self.rdwindow.destroy)
    self.btnexit.grid(row=11, column=1, pady=10, padx=(30, 10))
    self.lblcds = ctk.CTkLabel(self.rdwindow, text="", font=("arial", 18, "bold"), justify='left')# 
    self.lblcds.grid(row=12, column=0, pady=10, padx=(30, 10), columnspan=2)

    def filedialogopen(self):
        print(type(self.changername))
        basefiledirectory = f"{devicesaveddata}"+f"{self.changername.get()}"
        print(f"basefiledirectory: {devicesaveddata}"+f"{self.changername.get()}")
        # basefiledirectory = f"{devicesaveddata}"+"\\"+f"{self.changername.get()}"
        # print(f"basefiledirectory: {devicesaveddata}"+"\\"+f"{self.changername.get()}")
        getfile = askopenfilename(parent=self.rdwindow, title="Base File selection", initialdir=basefiledirectory)
        #self.rgfilename1.set(str(rgfilename1))
        #print(f"filedialogopen1 = {rgfilename1}")
        
        if len(getfile) == 0:
            print("No file selected")
            return
        
        filebase = os.path.basename(getfile)
        print(f"self.filebase = {filebase}")

        #print(f"self.rgfilename1.get() = {self.rgfilename1.get()}")
        #self.ebdbgfilename.insert(0, "newfilename")
        #global rgfilename
        self.rgfilename.set(filebase)


    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        #print("Successfull connection")
        query = ("SELECT * FROM devices WHERE id = '%s'" % (iam_selecteddevice))
        cursor.execute(query)
        results = cursor.fetchall()
        # sqliteConnection.commit()
        #print(f"Printing the entrytochange record {results}")
        self.result_id = results[0][0]
        #self.result_id.set(int(resid))
        #self.rname = results[0][1]
        self.changername.set(str(results[0][1]))
        #self.rip = results[0][2]
        self.changerip.set(str(results[0][2]))
        self.changerusername.set(str(results[0][3]))
        self.changerpassword.set(str(results[0][4]))
        self.changerdescription.set(str(results[0][5]))
        self.changertype.set(str(results[0][6]))
        self.rgfilename.set(str(results[0][7]))
        
        #print (f"results id =  {self.result_id}")
        #print (f"results name =  {self.rname}")
        #print (f"results ip =  {self.rip}")
        #print (f"results username =  {self.rusername}")
        #print (f"results password =  {self.rpassword}")
        #print (f"results description =  {self.rdescription}")
        #print (f"results type =  {self.rtype}")
        #print (f"results golden file =  {self.rgfilename}")

    except sqlite3.Error as error:
        self.lblcds.configure(text_color="red")
        self.lblcds.configure(text=f"Change request error: {error}")
        print("The error message is (line 452): ",error)
        print("Exception class is (line 453): ", error.__class__)
        print("Exception is (line 454):", error.args)

    # Insert the values into the entry boxes
    #self.ebdbname.insert(0, self.changername.get())
    #self.ebdbip.insert(0, self.rip)
    #self.ebdbip.insert(0, self.changerip.get())

    #self.ebdbusername.insert(0, self.rusername)
    #self.ebdbpassword.insert(0, self.rpassword)
    
    # Need because doesn't work like the rest of the inserts
    self.ebdbdescription.insert('1.0', self.changerdescription.get())
    
    #self.ebdbtype.insert(0, self.rtype)
    #self.ebdbgfilename.insert(0, self.rgfilename)

def dbconnectRegister(self, iam_selecteddevice):
    #print("Register button pressed")
    self.btngo.configure(state="disabled", fg_color="gray", border_color='gray')
    #print("id" + " = " + str(iam_selecteddevice))
    #print("Name" + " = " + str(self.ebdbname.get()))
    #print("IP" + " = " + str(self.ebdbip.get()))
    #print("Username" + " = " + str(self.ebdbusername.get()))
    #print("Password" + " = " + str(self.ebdbpassword.get()))
    #print("Description" + " = " + str(self.ebdbdescription.get('1.0','end-1c')))
    #print("Type" + " = " + str(self.ebdbtype.get()))
    #print("Golden config filename" + " = " + str(self.ebdbgfilename.get()))


    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        #print("Successfull connection")
        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        #print("SQLite Database Version is: ", record)
        query = ("UPDATE devices SET name = ?, ip = ?, username = ?, password = ?, description = ?, type = ?, golden = ? WHERE id = ?")
        inputs = (self.ebdbname.get(),self.ebdbip.get(),self.ebdbusername.get(),self.ebdbpassword.get(),self.ebdbdescription.get('1.0','end-1c'),self.ebdbtype.get(),self.ebdbgfilename.get(), self.result_id)
        cursor.execute(query, inputs)
        sqliteConnection.commit()

    except sqlite3.Error as error:
        print("The error message is (500): ",error)
        print("Exception class is (501): ", error.__class__)
        print("Exception is (502):", error.args)
           
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #msgboxname = str(self.rname.get()) + " with IP address " + str(self.rip.get())
            # self.ebdbname.delete(0, END)
            #self.ebdbip.delete(0, END)
            #self.ebdbusername.delete(0, END)
            #self.ebdbpassword.delete(0, END)
            #self.ebdbdescription.delete('1.0', END)
            #self.ebdbtype.delete(0, END)
            #self.ebdbgfilename.delete(0, END)

            # Change text and entry boxe to gray
            self.ebdbname.configure(state='disabled', fg_color="light gray")
            self.ebdbip.configure(state='disabled', fg_color="light gray")
            self.ebdbusername.configure(state='disabled', fg_color="light gray")
            self.ebdbpassword.configure(state='disabled', fg_color="light gray")
            self.ebdbdescription.configure(state='disabled', fg_color="light gray")
            self.ebdbtype.configure(state='disabled', fg_color="light gray")
            self.ebdbgfilename.configure(state='disabled', fg_color="light gray")
            self.dbname.configure(text_color="gray40")
            self.dbip.configure(text_color="gray40")
            self.dbusername.configure(text_color="gray40")
            self.dbpassword.configure(text_color="gray40")
            self.dbdescription.configure(text_color="gray40")
            self.dbtype.configure(text_color="gray40")
            self.dbgfilename.configure(text_color="gray40")
            self.btnfile.configure(state='disabled', fg_color="gray", border_color='gray')

            self.lblcds.configure(text=f" Device (id:{iam_selecteddevice}) has been changed. ", text_color="green4", bg_color="yellow2")

            # Redraw the device canvas
            clear_all(self)

def deletedbdevice(self, iam_selecteddevice):
    #print(f"I am the selected device id = {iam_selecteddevice}")
    self.deletemsgbox = messagebox.askquestion(title=f"Delete ? (id:{iam_selecteddevice})", message=f"Please confirm that you want to delete entry id:{iam_selecteddevice}", icon='warning')
    if self.deletemsgbox == 'yes':
        try:
            #print (f"I am deletedbdevice row selection is {iam_selecteddevice}")
            sqliteConnection = sqlite3.connect(dbfile)
            cursor = sqliteConnection.cursor()
            #print("Successfull connection")
            query = ("DELETE FROM devices WHERE id = '%s'") % (iam_selecteddevice)
            cursor.execute(query)
            sqliteConnection.commit()
            #print (f"RECORD DELETED deletedbdevice row selection is {iam_selecteddevice}")
            messagebox.showinfo(title='Return', message=f'The record with id:{iam_selecteddevice} was deleted.')
        except sqlite3.Error as error:
            messagebox.showinfo(title='Return', message=f'Problem occured: {error}')
            #print("The error message is: ",error)
            #print("Exception class is: ", error.__class__)
            #print("Exception is", error.args)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            
            # Redraw the device canvas
            clear_all(self)

    else:
        messagebox.showinfo(title='Request Canceled', message=f'You canceled the request.\n id:{iam_selecteddevice} remains in the list.')
'''
# Delete entry from the devices database
def deletedbdevice(self, iam_selecteddevice):
    #print(f"I am the selected device id = {iam_selecteddevice}")
    self.deletemsgbox = messagebox.askquestion(title=f"Delete ? (id:{iam_selecteddevice})", message=f"Please confirm that you want to delete entry id:{iam_selecteddevice}", icon='warning')
    if self.deletemsgbox == 'yes':
        try:
            #print (f"I am deletedbdevice row selection is {iam_selecteddevice}")
            sqliteConnection = sqlite3.connect(dbfile)
            cursor = sqliteConnection.cursor()
            #print("Successfull connection")
            query = ("DELETE FROM devices WHERE id = '%s'") % (iam_selecteddevice)
            cursor.execute(query)
            sqliteConnection.commit()
            #print (f"RECORD DELETED deletedbdevice row selection is {iam_selecteddevice}")
            messagebox.showinfo(title='Return', message=f'The record with id:{iam_selecteddevice} was deleted.')
        except sqlite3.Error as error:
            messagebox.showinfo(title='Return', message=f'Problem occured: {error}')
            #print("The error message is: ",error)
            #print("Exception class is: ", error.__class__)
            #print("Exception is", error.args)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
            
            # Redraw the device canvas
            clear_all(self)

    else:
        messagebox.showinfo(title='Request Canceled', message=f'You canceled the request.\n id:{iam_selecteddevice} remains in the list.')

'''



