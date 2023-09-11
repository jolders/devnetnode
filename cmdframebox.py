from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import scrolledtext
from settings import *

#Add Menu


def showcmdframe(self, choice, *args, **kwargs):
    # this shows the correct frame in the cmd window based on the combo selection.
    print("this is showcmdframe")
    print(f"combobox selected is :{choice}")
    # self.lblUpdate.config(text=f"Using: {connectselect} ")
    '''
    self.listOfCMDs = ['show version',
                       'show running-config',
                       'show ip interface brief',
                       'show ip route'
                       'show interface gigabitEthernet 0/0',
                       'show interface gigabitEthernet 0/1',
                       'show interface gigabitEthernet 0/2',
                       'show interface gigabitEthernet 0/3',
                       'show interface gigabitEthernet 0/4',
                       'show interface gigabitEthernet 1/0',
                       'show interface gigabitEthernet 1/1',
                       'show arp',
                       'show flash:'
                       'show vlan'
                       ]
    '''
    
                       
    '''
    def populatebox():
        for i in listOfCMDs:
            self.listBox.insert("end", i)
    '''
    

    
    if choice == "Paramiko":
        #self.statustext.set("Method: Paramiko")
        #if self.btncopy["state"] == "active" or "normal": self.btncopy["state"] = "disabled"
        #if self.btnpaste["state"] == "active" or "normal": self.btnpaste["state"] = "disabled"
        # self.btnpaste.config(state='disabled')

        self.btncopy.configure(state='disabled')
        self.btnpaste.configure(state='disabled')
        
        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()
        
        self.cmdframecontainer = Frame(self.cmdframea, background="light sky blue")
        self.cmdframecontainer.pack(fill='both', expand=TRUE, anchor='n', side=TOP)

        #self.btnsipb=ttk.Button(self.cmdframea, text="Run the selected command", command=self.runcmdselection)
        #self.btnsipb.pack(side='left', anchor='s')
        
        self.listbox = Listbox(self.cmdframecontainer, 
                               activestyle='none', 
                               font=("Helvetica", 11, "bold"),
                               highlightthickness=0,
                               selectforeground='black',
                               background='light goldenrod yellow',
                               selectbackground="palegreen",
                               exportselection=False) # exportselection=False on combobox and listbox to clear conflict
        self.listbox.pack(side = LEFT, fill = 'both', expand=True, anchor='nw', padx=(15, 5), pady=(10, 5))
        self.scrollbar = Scrollbar(self.cmdframecontainer)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)

        '''
        self.listbox.insert(0, 'show version')
        self.listbox.insert(1, 'show running-config')
        '''        
        # listOfCMDs located in the settigs file    
        for i in listOfCMDs:
            self.listbox.insert("end", i)
                
        self.listbox.select_set(1)
        self.cmdvarselected.set("show running-config")
        self.statusvarcmd2.set(value=self.cmdvarselected.get())
                
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)
        
        def localindex_selected(event):
            selected_indices = self.listbox.curselection()
            selected_index = selected_indices[0]
            selected_value = self.listbox.get(selected_index)
            self.cmdvarselected.set(selected_value)
            print(f"localindex_selected: {selected_value}")
            print(f"localindex_selected cmdvarselected value: {self.cmdvarselected.get()}")
            self.statusvarcmd2.set(value=self.cmdvarselected.get())  # Update status label
        
        self.listbox.bind('<<ListboxSelect>>', localindex_selected)
    
    elif choice == "Netmiko":
        #self.statustext.set("Method: Netmiko")
        self.btncopy.configure(state='disabled')
        self.btnpaste.configure(state='disabled')
        
        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()
          
        self.cmdframecontainer = Frame(self.cmdframea, background="light sky blue")
        self.cmdframecontainer.pack(fill='both', expand=TRUE, anchor='n', side=TOP)

        #self.btnsipb=ttk.Button(self.cmdframea, text="Run the selected command", command=self.runcmdselection)
        #self.btnsipb.pack(side='left', anchor='s')
        
        self.listbox = Listbox(self.cmdframecontainer, 
                               activestyle='none', 
                               font=("Helvetica", 11, "bold"),
                               highlightthickness=0,
                               selectforeground='black',
                               background='light goldenrod yellow',
                               selectbackground="palegreen",
                               exportselection=False) # exportselection=False on combobox and listbox to clear conflict
        self.listbox.pack(side = LEFT, fill = 'both', expand=True, anchor='nw', padx=(15, 5), pady=(10, 5))
        self.scrollbar = Scrollbar(self.cmdframecontainer)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)

        '''
        self.listbox.insert(0, 'show version')
        self.listbox.insert(1, 'show running-config')
        '''        
        # listOfCMDs located in the settigs file    
        for i in listOfCMDs:
            self.listbox.insert("end", i)
                
        self.listbox.select_set(1)
        self.cmdvarselected.set("show running-config")
        self.statusvarcmd2.set(value=self.cmdvarselected.get())
                
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)
        
        def localindex_selected(event):
            selected_indices = self.listbox.curselection()
            selected_index = selected_indices[0]
            selected_value = self.listbox.get(selected_index)
            self.cmdvarselected.set(selected_value)
            print(f"localindex_selected: {selected_value}")
            print(f"localindex_selected cmdvarselected value: {self.cmdvarselected.get()}")
            self.statusvarcmd2.set(value=self.cmdvarselected.get())  # Update status label
        
        self.listbox.bind('<<ListboxSelect>>', localindex_selected)
        
        #return self.cmdcmdvarselected.get()

    elif choice == "Netmiko_ch":
        #self.statustext.set("Method: Netmiko_ch")
        self.btncopy.configure(state='disabled')
        self.btnpaste.configure(state='disabled')
        
        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()
          
        self.cmdframecontainer = Frame(self.cmdframea, background="light sky blue")
        self.cmdframecontainer.pack(fill='both', expand=TRUE, anchor='n', side=TOP)

        #self.btnsipb=ttk.Button(self.cmdframea, text="Run the selected command", command=self.runcmdselection)
        #self.btnsipb.pack(side='left', anchor='s')
        
        self.listbox = Listbox(self.cmdframecontainer, 
                               activestyle='none', 
                               font=("Helvetica", 11, "bold"),
                               highlightthickness=0,
                               selectforeground='black',
                               background='light goldenrod yellow',
                               selectbackground="palegreen",
                               exportselection=False) # exportselection=False on combobox and listbox to clear conflict
        self.listbox.pack(side = LEFT, fill = 'both', expand=True, anchor='nw', padx=(15, 5), pady=(10, 5))
        self.scrollbar = Scrollbar(self.cmdframecontainer)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
                
        '''
        self.listbox.insert(0, 'show version')
        self.listbox.insert(1, 'show running-config')
        '''        
        # listOfCMDs located in the settigs file    
        for i in listOfCMDs:
            self.listbox.insert("end", i)

        self.listbox.select_set(1)
        self.cmdvarselected.set("show running-config")
        self.statusvarcmd2.set(value=self.cmdvarselected.get())
                
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)
        
        def localindex_selected(event):
            selected_indices = self.listbox.curselection()
            selected_index = selected_indices[0]
            selected_value = self.listbox.get(selected_index)
            self.cmdvarselected.set(selected_value)
            print(f"localindex_selected: {selected_value}")
            print(f"localindex_selected cmdvarselected value: {self.cmdvarselected.get()}")
            self.statusvarcmd2.set(value=self.cmdvarselected.get())  # Update status label
        
        self.listbox.bind('<<ListboxSelect>>', localindex_selected)
        
    elif choice == "Netmiko_ch_config":
        #self.statustext.set("Method: Netmiko_ch_config")
        self.btncopy.configure(state='normal')
        self.btnpaste.configure(state='normal')
        
        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()

        
        self.cmdframecontainer = Frame(self.cmdframea, background="light sky blue")
        self.cmdframecontainer.pack(fill='both', expand=TRUE, anchor='n', side=TOP)
        
        self.cmdtxtbox = scrolledtext.ScrolledText(self.cmdframecontainer, 
                                                   wrap=WORD, 
                                                   background='light goldenrod yellow', 
                                                   font=("Helvetica", 11, "bold"),
                                                   height=5) #, height=23, width=83
        self.cmdtxtbox.pack(side = LEFT, fill = 'both', expand=True, anchor='nw', padx=(15, 5), pady=(10, 5))
        
        # POP UP MENU
        def copy_select(): # copy selected text to clipboard
            global cmddata
            if self.cmdtxtbox.selection_get():
                cmddata=self.cmdtxtbox.selection_get() # copy selected text to clipboard
                self.clipboard_clear()
                self.clipboard_append(cmddata)
            
        def paste_select():
            global data
            self.cmdtxtbox.insert(tk.END,self.clipboard_get()) # Paste data from clipboard
        
        self.statusvarcmd2.set(value="Netmiko config multiline")  # Update status label
        
        
        #Add Menu
        popup = Menu(self.cmdtxtbox, tearoff=0)
        #Adding Menu Items
        popup.add_command(label="Copy", command=lambda:copy_select())
        popup.add_command(label="Paste", command=lambda:paste_select())
        
        def menu_popup(event):
        # display the popup menu
            try:
                popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                #Release the grab
                popup.grab_release()

        self.bind("<Button-3>", menu_popup)
    
    else: 
        #self.statustext.set("Method: Undefined")
        self.btncopy.configure(state='disabled')
        self.btnpaste.configure(state='disabled')
        
        for widgets in self.cmdframea.winfo_children():
            widgets.destroy()


        
        
        
        


        
        
