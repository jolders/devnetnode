from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from tkinter import scrolledtext
import customtkinter as ctk
from settings import *
import os
from os.path import exists
import shutil
import json
from PIL import ImageTk, Image



def btndelete(self):
    print("I am btndelete")
    groudevicedir = os.path.join(devicegroups, self.grpnamecbx.get())
    respquest = messagebox.askyesno(title="Delete Group ?", message=f"Are you sure you want to delete {self.grpnamecbx.get()}", parent=self.dwindow)
    if respquest == True:
        print(f"The directory: {str(groudevicedir)} - gets deleted")
        self.btnreset.configure(state='disabled', fg_color='gray')
        self.btndelete.configure(state='disabled', fg_color='gray')
        
        try:
            shutil.rmtree(str(groudevicedir))

        except:
            self.deletegrpstatuslbl.configure(text="An error occured")
            
        self.grpnamecbx.configure(values=self.groupcomboboxoptions)
        self.deletegrpstatuslbl.configure(text=f"{self.grpnamecbx.get()} was deleted")
        self.cgouttxtbx.configure(state='normal') # Output textbox
        self.cgouttxtbx.configure(bg="gray80")
        self.cgouttxtbx.delete('1.0', END) #clear contents
        self.cgouttxtbx.configure(state='disabled')



    else:
        print("Else = Nothing happens")

    

def btnreset(self):
    print("I am btnreset")
    
    self.grpnamebtn.configure(state='normal', text="Set", fg_color='green') # Group select Button
    self.grpnamecbx.configure(state='readonly', fg_color='PaleGreen2') # Group select combobox
    self.cgouttxtbx.configure(state='disabled', bg="gray80") # Group select combobox
    self.cgouttxtbx.configure(state='normal') # Output textbox
    self.cgouttxtbx.configure(bg="gray80")
    self.cgouttxtbx.delete('1.0', END) #clear contents
    self.btnreset.configure(state='disabled', fg_color='gray')
    self.btndelete.configure(state='disabled', fg_color='gray')
    self.deletegrpstatuslbl.configure(text="")


def grpcbxselc(self):
    print("I am delete a group page 'delgroup' (deletegroup.py)")

    if self.grpnamecbx.get() == 'select Group to edit':
        print("please select a valid Group")
        self.deletegrpstatuslbl.configure(text="Please select a valid Group")
        return None

    # Disable the set button
    self.grpnamebtn.configure(state='disabled', fg_color='gray', text="Accepted") # Group select Button
    self.grpnamecbx.configure(state='disabled', fg_color="gray80") # Group select combobox
    self.cgouttxtbx.configure(state='normal') # Output textbox
    self.cgouttxtbx.configure(bg="PaleGreen2")
    
    self.btnreset.configure(state='normal', fg_color='DeepSkyBlue4') #
    self.btndelete.configure(state='normal', fg_color='dark green') #
    #self.btndelete.configure(fg_color="gray", state='normal')
    self.btnreset.configure(state='normal')
    self.deletegrpstatuslbl.configure(text=f"{self.grpnamecbx.get()} was chosen")






    print(f"1) the current working directory is : {os.getcwd()}")
    if os.getcwd() != devicegroups:
        os.chdir(devicegroups)
        print("cwd now changed to os.chdir(devicegroups)")
    
    print(f"1a) The current selected item is : {self.grpnamecbx.get()}")
    #print(f"2a) The groupname is : {self.groupname.get()}")
    groudevicedir = os.path.join(devicegroups, self.grpnamecbx.get())
    print(f"1a) The groudevicedir value is : {str(groudevicedir)}")

    grpfilepath = os.path.join(groudevicedir, self.grpnamecbx.get() + ".json")
    grpfiletoread = open(grpfilepath)
    grpjsondata = json.load(grpfiletoread)
    print(f"1) I am 'inputjsondata' raw: {grpjsondata}")

    # Insert members into scrollbox
    self.cgouttxtbx.insert(INSERT, f"1) Group name is : {self.grpnamecbx.get()}\n")
    self.cgouttxtbx.insert(INSERT, f"2) The directory is : {groudevicedir}\n")
    self.cgouttxtbx.insert(INSERT, f"3) Config file is : {grpfilepath}\n")
    self.cgouttxtbx.insert(INSERT, f"4) Method config is : {grpjsondata['members']}\n")
    self.cgouttxtbx.insert(INSERT, f"5) Method config is : {grpjsondata['method']}\n")
    self.cgouttxtbx.insert(INSERT, f"6) Notes/Commands config is : {grpjsondata['commands']}\n")
    

    items = os.listdir(devicegroups)
    self.groupcomboboxoptions = []
    for item in items:
        if os.path.isdir(item):
            self.groupcomboboxoptions.append(item)
    
    self.cgouttxtbx.configure(state="disabled", bg="PaleGreen2")



def delgroup(self):
    self.dwindow = tkinter.Toplevel()
    self.dwindow.title("Delete Device Group")
    self.dwindow.geometry('600x477+200+200')
    self.dwindow.resizable(False, False)
    self.dwindow.configure(background='powder blue')
    self.dwindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

    self.dwindow.grid_columnconfigure(0, weight=1)
    # device name
    self.createlabel = ctk.CTkLabel(self.dwindow, text="Delete a Device Group", font=('arial', 22, 'bold'))
    self.createlabel.grid(row=0, column=0,sticky=EW, columnspan=3, pady=(20,16))
    self.separator1 = ttk.Separator(self.dwindow, orient='horizontal')
    self.separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=10)

    # GROUP NAME (Group1, London Routers, WestCoastSwitches)
    self.grpname = ctk.CTkLabel(self.dwindow, text="Group name", font=('arial', 18, 'bold'))
    self.grpname.grid(row=2, column=0,sticky=W, padx=35, pady=10)
    self.grpnamecbx = ctk.CTkComboBox(self.dwindow, values=self.groupcomboboxoptions,  font=('arial', 14, 'bold'), fg_color="pale green", width=230, border_color='green4', 
                                      button_color='green4', button_hover_color='green', dropdown_fg_color='pale green', dropdown_hover_color='PaleGreen3')
    self.grpnamecbx.grid(row=2, column=1, sticky=EW, padx=10, pady=10)
    self.grpnamecbx.set("select Group to edit")
    self.grpnamebtn = ctk.CTkButton(self.dwindow, text="Set", command=lambda:grpcbxselc(self), width=100, fg_color="green", hover_color='green4')
    self.grpnamebtn.grid(row=2, column=2, padx=30, pady=10)

    self.cgouttxtbx = scrolledtext.ScrolledText(self.dwindow, font='arial 10', height = 10, width = 25, bg="gray80", wrap=WORD)
    self.cgouttxtbx.grid(row=4, column=0,sticky=EW, padx=(25, 25), pady=30, columnspan=3)

    self.separator2 = ttk.Separator(self.dwindow, orient='horizontal')
    self.separator2.grid(row=5, sticky=EW, columnspan=3, padx=20, pady=10)

    self.btnreset = ctk.CTkButton(self.dwindow, text="Reset", command=lambda:btnreset(self),  fg_color="gray", state='disabled', hover_color='DeepSkyBlue3', font=('arial', 12, 'bold'), width=100)
    self.btnreset.grid(column=0, row=6, pady=10, padx=25)

    self.btndelete = ctk.CTkButton(self.dwindow, text="Delete", command=lambda:btndelete(self),  fg_color="gray", state='disabled', hover_color='green4', font=('arial', 12, 'bold'), width=100)
    self.btndelete.grid(column=1, row=6, pady=10, padx=25)

    self.btnexit = ctk.CTkButton(self.dwindow, text="EXIT", command=self.dwindow.destroy,  fg_color="red2", hover_color='red3', font=('arial', 12, 'bold'), width=100)
    self.btnexit.grid(column=2, row=6, pady=10, padx=25)

    self.deletegrpstatuslbl = Label(self.dwindow, text="", font=('arial', 14, 'bold'), bg="powder blue", fg='OrangeRed2')
    self.deletegrpstatuslbl.grid(row=7, column=1, sticky=W, padx=(20, 20), pady=10)

    
