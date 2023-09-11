import sqlite3
from mysql.connector import Error
import os
from settings import *
from tkinter import *
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import ttk, scrolledtext, messagebox
import shutil
from netmiko import Netmiko, ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from connecttodb import getdevicefromid
from PIL import ImageTk, Image
import regex as re

# this file uploads a configuration file to a Cisco device
# configuploadtftp
# Pulled in from the right click on treeview on devices may not be required
def configuploadtftp(self):
    devicesdetails = []
    self.tftpselectedid=StringVar()
    self.setbackuptypevar=StringVar() # Bakup type (startup, running)
    self.setfileidtypevar=StringVar() # File identifier (weekly, golden ?)
    self.filename = StringVar()
    self.filedest = StringVar()
    self.filesrc = StringVar()
    self.tftprootdir = StringVar()
    self.tftprootdir.set(tftprootdir) # C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\tftp_temp

    self.checkboxcopy_var = ctk.StringVar(value="on") # Checkbox value for COPY/MERGE selection
    self.checkboxrepl_var = ctk.StringVar(value="off") # Checkbox value for REPLACE selection
    self.checkboxcrs_var = ctk.StringVar(value="off") # Checkbox value for COPYRUNSTART selection
    self.chkbxrunningcfg_var = ctk.StringVar(value="on") # running config
    self.chkbxstartupcfg_var = ctk.StringVar(value="off") # startup config
    self.checkboxcstrn_var = ctk.StringVar(value="off") # 'copy running > startup'

    self.tftpuploadcmd = ctk.StringVar()

    # Evaluate the value of the checkbox to determin running or startup
    self.running_startup_var = StringVar()

    self.returnedid = IntVar(self)
    self.returnedname = StringVar()
    self.returnedip = StringVar()
    self.returnedusername = StringVar()
    self.returnedpassword = StringVar()
    self.returneddescription = StringVar()
    self.returnedtype = StringVar()
    self.returnedgolden = StringVar()

    sqliteConnection = sqlite3.connect(dbfile)
    cursor = sqliteConnection.cursor()
    #record = cursor.fetchall()
    query = (f"SELECT * FROM devices")
    cursor.execute(query)
    record = cursor.fetchall()
    for row in record:
        self.returnedid.set(row[0])
        self.returnedname.set(row[1])
        self.returnedip.set(row[2])
        self.returnedusername.set(row[3])
        self.returnedpassword.set(row[4])
        self.returneddescription.set(row[5])
        self.returnedtype.set(row[6])
        self.returnedgolden.set(row[7])
        #retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getalldevices(self)
        devicesdetails.append(f"id:{str(self.returnedid.get())}" + " " +  f"{self.returnedname.get()}" + " " + f"({self.returnedip.get()})")
        # print(f"{retid},{retname},{retip},{retusername},{retpassword},{retdescription},{rettype},{retgolden}")
        self.tftpselectedid.set(str(self.returnedid.get()))
    
    print("1) This is configuploadtftp(uploadtftp.py)")
    # print(f"2) This is configuploadtftp (iam_selecteddevice): {str(iam_selecteddevice)}")
    print(f"3) This is configuploadtftp (id): {str(self.returnedid.get())}")
    print(f"4) This is configuploadtftp (name): {self.returnedname.get()}")
    print(f"5) This is configuploadtftp (ip): {self.returnedip.get()}")
    print(f"6) This is configuploadtftp (username): {self.returnedusername.get()}")
    print(f"7) This is configuploadtftp (password): {self.returnedpassword.get()}")
    print(f"8) This is configuploadtftp (retdescription): {self.returneddescription.get()}")
    print(f"9) This is configuploadtftp (rettype): {self.returnedtype.get()}")
    print(f"10) This is configuploadtftp (retgolden): {self.returnedgolden.get()}")
    

    # Pressing the 'Upload button'
    def tftptorouter(self):
        self.progstatus.set(0.3)
        self.btnupload.configure(state='disabled', fg_color='gray', border_color='gray') # Button
        self.checkboxcopy.configure(state='disabled', fg_color='gray', border_color='gray') # "Copy(merge) config"
        self.checkboxrepl.configure(state='disabled', fg_color='gray', border_color='gray') # "Replace running config"
        self.checkboxcrs.configure(state='disabled', fg_color='gray', border_color='gray') # "copy runnning > startup"
        self.chkbxrunningcfg.configure(state='disabled', fg_color='gray', border_color='gray') # "running-config"
        self.chkbxstartupcfg.configure(state='disabled', fg_color='gray', border_color='gray') # "startup-config"
        self.checkboxcstrn.configure(state='disabled', fg_color='gray', border_color='gray') # "copy startup > runnning"
        self.update_idletasks()


        #print(f"4a) The current working directory is : {os.getcwd()}")
        #filelocated = '/Shared/NetDevApp3/cisco11/devicedata/tftp_temp/'
        os.chdir(self.tftprootdir.get())
        print(f"4b) Upload to Device name: {self.returnedname.get()}")
        print(f"4c) The current working directory is : {os.getcwd()}")
        # What is the file name
        print(f"4d) File name to look for is: {self.filename.get()}")

        # AT THIS POINT MAKE SURE YOU HAVE GOT ALL THE CISCO SEVICE TYPE LOGIN/ACCESS variable in place
        self.grpdesetry.insert(INSERT, f"2) Looking for file in the TFTP staging area:\n{self.filename.get()}\n")

        # Evaluate the value of the checkbox to determin running or startup
        # self.running_startup_var = StringVar()
        
        if self.chkbxstartupcfg_var.get() == "on":
            self.running_startup_var.set("startup-config")
            print(f"checbxrunningcfg_var value = {self.chkbxrunningcfg_var.get()}")
        elif self.chkbxrunningcfg_var.get() == "on":
            self.running_startup_var.set("running-config")
            print(f"checbxstartupcfg_var value = {self.chkbxstartupcfg_var.get()}")
        else:
            print("uploadtftp.py(tftprouter) error occured getting checbxstartupcfg_var or checbxrunningcfg_var")


        
        if os.path.isfile(self.filename.get()):
            print("4)d File exist so lets go")
            
            self.statuslbl.configure(font=('arial', 12, 'bold'), text='Starting to run task')
            self.update_idletasks()
            
            cisco_device = {
                'device_type': f'{self.returnedtype.get()}',
                'host': f'{self.returnedip.get()}',
                'username': f'{self.returnedusername.get()}',
                'password': f'{self.returnedpassword.get()}',
                'port': 22,
                'secret': f'{self.returnedpassword.get()}',
                'verbose': True}
            
            self.grpdesetry.insert(INSERT, f"3) Initiating Connection to : {self.returnedname.get()}\n")

            conn = ConnectHandler(**cisco_device)
            conn_prompt = conn.find_prompt()
            if '>' in conn_prompt: conn.enable()
            output = conn.send_command(f"\n") # what do enter into the devices command line to accept a tftp upload ?
            print(f"Checking the config mode: {conn.check_config_mode()}")
            self.grpdesetry.insert(INSERT, f"4) The config mode on the device is: {conn.check_config_mode()}\n")
            
            self.progstatus.set(0.4)
            self.update_idletasks()
            
            # Router#copy tftp: running-config
            # Address or name of remote host []? 10.104.207.171
            # Source filename []? backup_cfg_for_my_router
            # Destination filename [running-config]?
            try:
                name = f"device{str(1)}"
                net_connect = ConnectHandler(**cisco_device)
                print("Try 1a")
                net_connect.enable()
                hostname = net_connect.find_prompt()[:-1]
                print(f"The hosname found on the device is: {hostname}")
                self.grpdesetry.insert(INSERT, f"5) The hostname on the device is: {hostname}\n")

                print(f"The value of checkboxcopy_var is: {self.checkboxcopy_var.get()}")

                self.statuslbl.configure(font=('arial', 12, 'bold'), text='Task in progress')
                self.progstatus.set(0.5)
                self.update_idletasks()


                if self.checkboxcopy_var.get() == "on": # Copy(merge) config
                    # Option1 Copy tftp > 'running-config' Option2 Copy tftp > 'startup-config'
                    # option changes due to value in running_startup_var
                    print("Option2 'startup-config checkboxcopy_var")
                    self.tftpuploadcmd.set(f"copy tftp://{tftpserver}{tftprootdir}/{self.filename.get()} {self.running_startup_var.get()}") 
                    self.grpdesetry.insert(INSERT, f"6) Sending the command: {self.tftpuploadcmd.get()}\n")
                    print(f"Try 1b (uploadtftp)copy_command:{self.tftpuploadcmd.get()}")
                    output = net_connect.send_command_timing(self.tftpuploadcmd.get())
                    if "Address or name" in output:
                        output += net_connect.send_command_timing(f"{tftpserver}\n")
                        print("Try 2")
                    if "Source filename" in output:
                        output += net_connect.send_command_timing(f"{self.filename.get()}\n")
                        print("Try 3")
                        net_connect.disconnect
                    if "Destination filename" in output:
                        output += net_connect.send_command_timing(f"\n")
                        print("Try 4 ---- I THINK IT DID IT")
                        self.grpdesetry.insert(INSERT, f"7) Running the command on the device.\n")
                    
                    self.progstatus.set(0.7)
                    self.update_idletasks()

                    # 'running-config' checkbox on + 'copy running > startup' checkbox on
                    print(f"COPY IF~chkbxrunningcfg_var on: {self.chkbxrunningcfg_var.get()}")
                    print(f"COPY IF~checkboxcrs_var on: {self.checkboxcrs_var.get()}")
                    if self.chkbxrunningcfg_var.get() == "on" and self.checkboxcrs_var.get() == "on":
                        print("This is TFTP > running-config and copy startup > running")
                        print(f"This is TFTP > running-config on: {self.chkbxrunningcfg_var.get()}")
                        print(f"copy running > startup on: {self.checkboxcrs_var.get()}")
                        # Running = copy running-config startup-config
                        copy_command1 = "copy running-config startup-config"
                        output1 = net_connect.send_command_timing(copy_command1)
                        self.grpdesetry.insert(INSERT, f"Output1:\n{output1}\n")
                        
                        if "Destination filename" in output1:
                            output1 += net_connect.send_command_timing("\n")
                            self.grpdesetry.insert(INSERT, f"running-config > startup-config output:\n{output1}\n")
                            self.grpdesetry.insert(INSERT, "------------------------------------------------\n")
                            self.grpdesetry.insert(INSERT, f"Request completed: running-config has been copied to the startup-config\n")
                            self.grpdesetry.insert(INSERT, "------------------------------------------------\n")
                        else:
                            print("else - self.checkboxcrs_var.get() Destination filename not found ")
                            print(f"'copy running > startup'=off: {self.checkboxcrs_var.get()} ")
                    
                        self.progstatus.set(0.8)
                        self.update_idletasks()


                    # running config checkbox + copy running > startup
                    print(f"COPY IF~chkbxstartupcfg_var on: {self.chkbxstartupcfg_var.get()}")
                    print(f"COPY IF~checkboxcstrn_var on: {self.checkboxcstrn_var.get()}")
                    if self.chkbxstartupcfg_var.get() == "on" and self.checkboxcstrn_var.get() == "on":
                        print("This is TFTP > startup-config and copy startup > running")
                        print(f"This is TFTP > startup on: {self.chkbxstartupcfg_var.get()}")
                        print(f"copy startup > running on: {self.checkboxcstrn_var.get()}")
                        # Running = copy running-config startup-config
                        copy_command1 = "copy startup-config running-config "
                        output1 = net_connect.send_command_timing(copy_command1)
                        self.grpdesetry.insert(INSERT, f"Output1:\n{output1}\n")
                        
                        if "Destination filename" in output1:
                            output1 += net_connect.send_command_timing("\n")
                            self.grpdesetry.insert(INSERT, f"copy startup-config running-config: COMPLETED\n{output1}\n")
                        else:
                            print("else - self.checkboxcrs_var.get() Destination filename not found ")
                            print(f"'copy running > startup'=off: {self.checkboxcstrn_var.get()} ")

                        self.progstatus.set(0.8)
                        self.update_idletasks()
                    
                    # copy startup-config > running-config
                    print(f"COPY IF~chkbxstartupcfg_var on: {self.chkbxstartupcfg_var.get()}")
                    print(f"COPY IF~checkboxcstrn_var on: {self.checkboxcstrn_var.get()}")
                    if self.chkbxstartupcfg_var.get() == "on" and self.checkboxcstrn_var.get() == "on":
                        print("This is TFTP > startup and copy startup > running")
                        print(f"This is TFTP > startup on: {self.chkbxstartupcfg_var.get()}")
                        print(f"copy startup > running on: {self.checkboxcstrn_var.get()}")
                        # Running = copy running-config startup-config
                        copy_command1 = "copy startup-config running-config"
                        output1 = net_connect.send_command_timing(copy_command1)
                        self.grpdesetry.insert(INSERT, f"Output1:\n{output1}\n")
                        
                        if "Destination filename" in output1:
                            output1 += net_connect.send_command_timing("\n")
                            self.grpdesetry.insert(INSERT, f"startup-config > running-config output:\n{output1}\n")
                            self.grpdesetry.insert(INSERT, "------------------------------------------------\n")
                            self.grpdesetry.insert(INSERT, f"Request completed: startup-config has been copied to the running-config.\n")
                            self.grpdesetry.insert(INSERT, "------------------------------------------------\n")

                        else:
                            print("else - self.checkboxcrs_var.get() Destination filename not found ")
                            print(f"'copy running > startup'=off: {self.checkboxcrs_var.get()} ")

                        self.progstatus.set(0.8)
                        self.update_idletasks()
    
                elif self.checkboxrepl_var.get() == "on":
                    # CONFIGURE REPLACE checkboxrepl
                    print("CONFIGURE REPLACE")
                    print(f"CONFIGURE REPLACE self.checkboxrepl_var: {self.checkboxrepl_var.get()}")
                    self.tftpuploadcmd.set(f"configure replace tftp://{tftpserver}{tftprootdir}/{self.filename.get()} force") 
                    self.grpdesetry.insert(INSERT, f"6) Sending the command: {self.tftpuploadcmd.get()}\n")
                    print(f"Try 1b (uploadtftp)copy_command:{self.tftpuploadcmd.get()}")
                    output = net_connect.send_command_timing(self.tftpuploadcmd.get())
                    self.grpdesetry.insert(INSERT, f"7) Output:\n{output}\n")

                    if self.checkboxcrs_var.get() == "on":
                        # Running = copy running-config startup-config
                        copy_command1 = "copy running-config startup-config"
                        output1 = net_connect.send_command_timing(copy_command1)
                        self.grpdesetry.insert(INSERT, f"8) Output1:\n{output1}\n")
                        
                        if "Destination filename" in output1:
                            output1 += net_connect.send_command_timing("\n")
                            self.grpdesetry.insert(INSERT, f"8a) Capturing running-config > startup-config output:\n{output1}\n")
                            self.grpdesetry.insert(INSERT, "------------------------\n")
                            self.grpdesetry.insert(INSERT, f"Request completed: running-config has been copied to the startup-config\n")
                            self.grpdesetry.insert(INSERT, "------------------------")
                        else:
                            print("else - self.checkboxcrs_var.get() Destination filename not found ")
                            print(f"'copy running > startup'=off: {self.checkboxcrs_var.get()} ")
                    else:
                        print("self.checkboxcrs_var.get() == 'off' so not running 'copy running > startup'")
                        print(f"'copy running > startup'=off: {self.checkboxcrs_var.get()} ")

                    self.progstatus.set(0.8)
                    self.update_idletasks()
            
            except:
                print("An netmiko function exception occurred in tftpconfig(uploadtftp.py)")
                self.grpdesetry.insert(INSERT, "5) An error occured in the try block \n")
            
            finally:
                print("Doing net_connect.disconnect")
                net_connect.disconnect
                self.grpdesetry.insert(INSERT, "------------------------------------------------\n")
                self.grpdesetry.insert(INSERT, f"Request completed: {self.returnedname.get()} has a new {self.running_startup_var.get()}\n")
                self.grpdesetry.insert(INSERT, "------------------------------------------------")
                print(f"The file I want to delete is:\n{tftprootdir}/{self.filename.get()}")
                # Lets delete the file from the staging area
                if os.path.exists(f"{tftprootdir}/{self.filename.get()}"):
                    os.remove(f"{tftprootdir}/{self.filename.get()}")
                    print("File Deleted from TFTP Staging area")
                else:
                    print(f"I couldn't delete the file:\n{tftprootdir}/{self.filename.get()}")

                self.statuslbl.configure(text='Task Completed')
                self.grpdesetry.see('end')
                self.progstatus.set(1)
                self.update_idletasks()



        else:
            print("4e) File is not in the temporary linux directory")
            self.grpdesetry.insert(INSERT, f"File or Location ERROR")
            self.grpdesetry.insert(INSERT, f"1) Expected file:\n {self.filename.get()}\n")
            self.grpdesetry.insert(INSERT, f"2) Expected location:\n {self.tftprootdir.get()}\n")
        

    # this is when you select a file and press set button on file selection.
    def capturefile(self):
        #self.lbxcontenttopindex = 0
        #self.lbxcontenttopindex  = self.lbxcontenttop.curselection()
        
        if self.lbxcontenttop.curselection() == ():
            print("lbxcontenttopindex has no value")
            tk.messagebox.showinfo(title="Selection error", message="Please select a valid file option.", icon='error', parent=self.tftpuploadwindow)
        else:
            print(f"lbxcontenttopindex HAS A VALUE:{self.lbxcontenttop.get(self.lbxcontenttop.curselection())}")

            try:
                print(f"3a) Capture the file selected in txtcontenttop = {self.lbxcontenttop.get(self.lbxcontenttop.curselection())}")
                self.filename.set(self.lbxcontenttop.get(self.lbxcontenttop.curselection()))
                
                print(f"3b) The current working directory is : {os.getcwd()}")

                # WINDOWS
                '''
                self.filedest.set(f"{tftprootdir}\\{self.filename.get()}")
                print(f"Linux tftprootdir = {tftprootdir}")
                print(f"Linux self.filename.get() = {self.filename.get()}")
                print(f"Linux filesdestination self.filedest.get() = {self.filedest.get()}")
                print("========================================================")
                self.filesrc.set(f"{devicesaveddata}\\{self.returnedname.get()}\\{self.filename.get()}")
                print(f"Linux devicesaveddata = {devicesaveddata}")
                print(f"Linux self.returnedname = {self.returnedname.get()}")
                print(f"Linux self.filename.get() = {self.filename.get()}")
                print(f"Linux filesource self.filesrc.get() = {self.filesrc.get()}")
                '''
                
                # LINUX
                self.filedest.set(f"{tftprootdir}/{self.filename.get()}")
                print(f"Linux tftprootdir = {tftprootdir}")
                print(f"Linux self.filename.get() = {self.filename.get()}")
                print(f"Linux filesdestination self.filedest.get() = {self.filedest.get()}")
                print("========================================================")
                self.filesrc.set(f"{devicesaveddata}/{self.returnedname.get()}/{self.filename.get()}")
                print(f"Linux devicesaveddata = {devicesaveddata}")
                print(f"Linux self.returnedname = {self.returnedname.get()}")
                print(f"Linux self.filename.get() = {self.filename.get()}")
                print(f"Linux filesource self.filesrc.get() = {self.filesrc.get()}")
                
                try:
                    # Change elements on the window
                    # self.devname.configure(state='disabled') # disable the label
                    self.selectdevicecbx.configure(fg_color="gray64", border_color='gray40', button_color='gray40', button_hover_color='gray40', state='disabled', text_color_disabled='white')
                    self.lbxcontenttop.configure(selectbackground="gray40", background='gray64')
                    self.lbxcontenttop.bindtags((self, "all")) # disables reselection but keeps selected highlighted 
                    self.btnselect.configure(text="Accepted", state='disabled', fg_color="gray", text_color_disabled="white")
                    self.grpdesetry.config(state=NORMAL)
                    self.grpdesetry.config(background="light yellow")
                    self.btnupload.configure(state='normal', fg_color="green", border_color='dark green')
                    # Copy file to the tftp temp area
                    shutil.copy(self.filesrc.get(), self.filedest.get())
                    self.grpdesetry.insert(INSERT, f"1) The file has been copied to the TFTP staging area: \n {self.filename.get()} \n")
                    print(f"Copied {self.filename.get()}")
                    
                    self.progstatus.set(0.2)
                    #self.statuslbl.configure(font=('arial', 10, 'bold'), text=f'{(self.filename.get()[:26])}...')
                    self.statuslbl.configure(text=f'Ready for uploading')


                except:
                    print("Copy Error to TFTP area")
                    self.grpdesetry.insert(INSERT, f"Problem copying file to staging area: \n {self.filename.get()} \n")
                    self.grpdesetry.insert(INSERT, f"File source: \n {self.filesrc.get()} \n")
                    self.grpdesetry.insert(INSERT, f"File Destination: \n {self.filedest.get()} \n")
            
            except:
                print(f"5a) lbxcontenttop.get is FALSE")
                print(f"3b) The current self.filename.get() : {self.filename.get()}")

    
    def selectdevicecbxcallback(self):
        # EVERYTIME THE COMBOBOX IS CHANGED CLEAR THE 'lbxcontenttop' TEXTBOX
        self.lbxcontenttop.delete(0, 'end')
        
        print("selectdevicecbxcallback")
        print(self.selectdevicecbx.get())
        self.btnselect.configure(fg_color="green", state='normal')
        self.lbxcontenttop.configure(state='normal', background='pale green')

        cbxid = re.findall(r'^\D*(\d+)', self.selectdevicecbx.get())
        cbxidstr = str(cbxid[0])
        # print(f"This is the selected item in the combobox: {cbxidstr}")

        retid1 = 0
        retname1 = ""
        retip1 = ""
        retusername1 = ""
        retpassword1 = ""
        retdescription1 = ""
        rettype1 = ""
        retgolden1 = ""

        retid1, retname1, retip1, retusername1, retpassword1, retdescription1, rettype1, retgolden1 = getdevicefromid(cbxidstr)
            
        self.returnedid.set(retid1)
        self.returnedname.set(retname1)
        self.returnedip.set(retip1)
        self.returnedusername.set(retusername1)
        self.returnedpassword.set(retpassword1)
        self.returneddescription.set(retdescription1)
        self.returnedtype.set(rettype1)
        self.returnedgolden.set(retgolden1)

        print(f"1) uploadtftp.py setdevice (retid1): {self.returnedid.get()}")
        print(f"2) uploadtftp.py setdevice (retname1): {self.returnedname.get()}")
        print(f"3) uploadtftp.py setdevice (retip1): {self.returnedip.get()}")
        print(f"4) uploadtftp.py setdevice (retusername1): {self.returnedusername.get()}")
        print(f"5) uploadtftp.py setdevice (retpassword1): {self.returnedpassword.get()}")
        print(f"6) uploadtftp.py setdevice (retdescription1): {self.returneddescription.get()}")
        print(f"7) uploadtftp.py setdevice (rettype1): {self.returnedtype.get()}")
        print(f"8) uploadtftp.py setdevice (retgolden1): {self.returnedgolden.get()}")

        try:
            print(f"1) uploadtftp.py 'setdevice' The current working directory is : {os.getcwd()}")
            devicedir = os.path.join(devicesaveddata, retname1)
            os.chdir(devicedir)
            print(f"1a) The current working directory is : {os.getcwd()}")
            print(f"1b) The devicesaveddata is : {devicesaveddata}")
            filesindir = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in filesindir:
                print(f)
                self.lbxcontenttop.insert('end', f)
        except:
            print(f"1ca) directory is : {os.getcwd()}")
            print(f"1db) The devicesaveddata is : {devicesaveddata}")
            print(f"1ec) directory could not be found : {devicedir}")
            self.lbxcontenttop.insert('end', "A problem exists")
            self.lbxcontenttop.insert('end', "The device directory could not be found")
            self.lbxcontenttop.insert('end', f"{devicedir}")
        
        self.progstatus.set(0.1)
        self.statuslbl.configure(text=f'{self.returnedname.get()} selected')


    # Copy(merge) config checkbox
    def checkboxcopy_event(self):
        if self.checkboxcopy.get() == "on":
            print(f"checkboxcopy_event value 'Copy(merge) config' (on): {self.checkboxcopy.get()}")
            print(f"checkboxrepl_event value 'Replace running config' (off): {self.checkboxrepl.get()}")
            self.checkboxrepl.deselect() # deactivate 'Replace running config'
            # Activate 'running-config'
            self.chkbxrunningcfg.configure(border_color="dark slate gray", state="normal")
            # Activate 'startup-config'
            self.chkbxstartupcfg.configure(border_color="dark slate gray", state="normal")
            # Activate 'copy startup > running'
            self.checkboxcstrn.configure(border_color="dark slate gray", state="normal")
            self.checkboxcrs.deselect() #'copy  running > startup'
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal")
            self.checkboxcstrn.deselect() #'copy startup > running'
            self.checkboxcstrn.configure(border_color="gray", state="disabled")
            # select running config by default
            self.chkbxrunningcfg.select()
        
        else:
            print(f"checkboxcopy_event value 'Copy(merge) config' (off): {self.checkboxcopy.get()}")
            print(f"checkboxrepl_event value 'Replace running config' (on): {self.checkboxrepl.get()}")
            self.checkboxrepl.select() # activate 'Replace running config'
            #  deactivate & disable 'running-config'
            self.chkbxrunningcfg.deselect()
            self.chkbxrunningcfg.configure(border_color="gray", state="disabled")
            #  deactivate & disable 'startup-config'
            self.chkbxstartupcfg.deselect()
            self.chkbxstartupcfg.configure(border_color="gray", state="disabled")
            # deselect and disable 'copy startup > running'
            self.checkboxcstrn.deselect() #'copy startup > running'
            self.checkboxcstrn.configure(border_color="gray", state="disabled")
            self.checkboxcrs.deselect() #'copy  running > startup'
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal")


    # Replace running config Checkbox
    def checkboxrepl_event(self):
        self.checkboxcopy.deselect()

        if self.checkboxrepl.get() == "on":
            print(f"checkboxrepl_event value 'Replace running config' (on): {self.checkboxrepl.get()}")
            self.checkboxcrs.deselect() #'copy  running > startup'
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal") #'copy  running > startup'
            self.checkboxcstrn.deselect()
            self.checkboxcstrn.configure(border_color="gray", state="disabled") #'copy startup > running'
            #  deactivate & disable 'running-config'
            self.chkbxrunningcfg.deselect()
            self.chkbxrunningcfg.configure(border_color="gray", state="disabled")
            #  deactivate & disable 'startup-config'
            self.chkbxstartupcfg.deselect()
            self.chkbxstartupcfg.configure(border_color="gray", state="disabled")
            
            self.running_startup_var.set("running-config")
        
        else:
            # If Replace running config off
            print(f"checkboxrepl_event value 'Replace running config' (off): {self.checkboxrepl.get()}")
            self.checkboxcopy.select() # Copy(merge) config selected
            # running-config active and selected
            self.chkbxrunningcfg.configure(border_color="dark slate gray", state="normal")
            self.chkbxrunningcfg.select()
            #  activate 'startup-config'
            self.chkbxstartupcfg.deselect()
            self.chkbxstartupcfg.configure(border_color="dark slate gray", state="normal")
            # deactivate 'copy running > startup'
            self.checkboxcrs.deselect()

    # runnning-config checkbox
    def chkbxrunningcfg_event(self):
        #self.checkboxcstrn.deselect()
        if self.chkbxrunningcfg_var.get()=="on":
            print(f"chkbxrunningcfg_event (on): {self.chkbxrunningcfg_var.get()}")
            self.chkbxstartupcfg.deselect()
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal") #'copy  running > startup'
            self.checkboxcstrn.deselect()
            self.checkboxcstrn.configure(border_color="gray", state="disabled") #'copy startup > running'
        
        else:
            print(f"chkbxrunningcfg_event (off): {self.chkbxrunningcfg_var.get()}")
            self.chkbxstartupcfg.select()
            # 'copy running > startup' deselect and disable
            self.checkboxcrs.deselect() #'copy  running > startup'
            self.checkboxcrs.configure(border_color="gray", state="disabled") #'copy  running > startup'
            # copy startup > running deselect and enable
            self.checkboxcstrn.deselect()
            self.checkboxcstrn.configure(border_color="dark slate gray", state="normal") #'copy startup > running'
    
    # startup-config Checkbox
    def chkbxstartupcfg_event(self):
        self.checkboxcstrn.deselect()

        if self.chkbxrunningcfg_var.get() == "on":
            print(f"chkbxstartupcfg_event (on): {self.chkbxstartupcfg_var.get()}")
            self.chkbxrunningcfg.deselect() # 'running-config' = deselect
            self.checkboxcrs.deselect() # 'copy running > startup' deselect
            self.checkboxcstrn.configure(border_color="dark slate gray", state="normal") # copy 'startup > running' enable
            self.checkboxcrs.configure(border_color="gray", state="disabled") # 'copy running > startup' disable
        
        else:
            print(f"chkbxstartupcfg_event 'startup-config' (off): {self.chkbxstartupcfg.get()}")
            # running-config select
            self.chkbxrunningcfg.select()
            # 'copy running > startup' deselect & normalise
            self.checkboxcrs.deselect()
            self.checkboxcrs.configure(border_color="dark slate gray", state="normal")
            self.checkboxcstrn.configure(border_color="gray", state="disabled") # copy 'startup > running' disabled
    
    # 'copy running > startup' Checkbox
    def checkboxcrs_event(self):
        print(f"checkboxcrs_event ('copy running > startup'): {self.checkboxcrs_var.get()}")
        

    #  'copy running > startup'
    def checkboxcstrn_event(self):
        print(f"checkboxcstrn_event: {self.checkboxcstrn_var.get()}")


    self.tftpuploadwindow = tk.Toplevel()
    self.tftpuploadwindow.geometry("600x790+200+200")
    self.tftpuploadwindow.title("TFTP Upload to device")
    self.tftpuploadwindow.configure(background='powder blue')
    self.tftpuploadwindow.resizable(False, False)
    self.tftpuploadwindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

    # Disable root window when this one is active
    self.tftpuploadwindow.attributes('-topmost', 'true')
    self.tftpuploadwindow.transient(self)
    self.tftpuploadwindow.update_idletasks()
    self.tftpuploadwindow.grab_set()

    self.tftpuploadwindow.grid_columnconfigure(0, weight=1)
    #self.tftpuploadwindow.grid_columnconfigure(0, weight=0)
    #self.tftpuploadwindow.grid_columnconfigure(1, weight=0)
    #self.tftpuploadwindow.grid_columnconfigure(2, weight=2)
    
    # top label
    self.lbltopa = ctk.CTkLabel(self.tftpuploadwindow, text="TFTP Upload config to device", font=('arial', 22, 'bold'))
    self.lbltopa.grid(row=0, column=0,sticky=EW, columnspan=3, pady=(15,10))
    #lbltopb = Label(top, background='powder blue', font='arial 14 bold italic', text=retusername) #textvariable=ipaddress
    #lbltopb.grid(row=0,column=1, sticky='w', pady=10)
    self.separator1 = ttk.Separator(self.tftpuploadwindow, orient='horizontal')
    self.separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=8)

    # Select device combobox
    self.devname = Label(self.tftpuploadwindow, text="Device selection", font=('arial', 14, 'bold'), bg="powder blue", fg='black')
    self.devname.grid(row=2, column=0,sticky=W, padx=(25,5), pady=(10))
    self.selectdevicecbx = ctk.CTkComboBox(self.tftpuploadwindow, width=350, font=('arial', 14, 'bold'), fg_color="pale green", border_color='dark slate gray', button_color='dark slate gray', button_hover_color='green4', dropdown_fg_color='pale green', dropdown_hover_color='PaleGreen3', values=devicesdetails, command=lambda v:selectdevicecbxcallback(self)) # '''values=devicesdetails,'''
    self.selectdevicecbx.set(value="select a device")
    self.selectdevicecbx.grid(row=2, column=1, sticky=E, padx=(10,30), pady=10, columnspan=2)
    
    self.lbxcontenttop = Listbox(self.tftpuploadwindow, height=12, width=180, selectbackground="green4", background='gray70', activestyle=NONE, selectmode=SINGLE, state='disabled')
    self.lbxcontenttop.grid(row=3, column=0, padx=(25, 0), pady=(10), sticky=EW, columnspan=2)
    
    self.btnselect = ctk.CTkButton(self.tftpuploadwindow, text="Select", command=lambda:capturefile(self), width=80, fg_color="gray", hover_color='green4', state='disabled')
    self.btnselect.grid(row=3, column=2, padx=(0,30), pady=10, sticky=SE)
    self.horizspr1 = ttk.Separator(self.tftpuploadwindow, orient='horizontal')
    self.horizspr1.grid(row=5, column=0, sticky=EW, columnspan=3, padx=20, pady=10)
    self.grpdesetry = scrolledtext.ScrolledText(self.tftpuploadwindow, font='arial 12', height=10, width=10, bg="gray70", wrap=WORD, state=DISABLED)
    self.grpdesetry.grid(row=6, column=0, sticky=EW, padx=(25, 30), pady=10, columnspan=3)
    
    # Checkboxes copy/merge config | Replace config | copy run start
    self.checkboxcopy = ctk.CTkCheckBox(self.tftpuploadwindow, text="Copy(merge) config", command=lambda:checkboxcopy_event(self), variable=self.checkboxcopy_var, onvalue="on", offvalue="off", fg_color="green4", hover_color="dark slate gray", border_color="dark slate gray", border_width=2, text_color_disabled="gray")
    self.checkboxcopy.grid(row=7, column=0, pady=10, sticky=W, padx=(25,0))
    self.checkboxrepl = ctk.CTkCheckBox(self.tftpuploadwindow, text="Replace running config", command=lambda:checkboxrepl_event(self), variable=self.checkboxrepl_var, onvalue="on", offvalue="off", fg_color="green4", hover_color="dark slate gray", border_color="dark slate gray", border_width=2, text_color_disabled="gray")
    self.checkboxrepl.grid(row=7, column=1, pady=10, sticky=W)
    self.checkboxcrs = ctk.CTkCheckBox(self.tftpuploadwindow, text="copy runnning > startup", command=lambda:checkboxcrs_event(self), variable=self.checkboxcrs_var, onvalue="on", offvalue="off", fg_color="green4", hover_color="dark slate gray", border_color="dark slate gray", border_width=2, text_color_disabled="gray")
    self.checkboxcrs.grid(row=7, column=2, pady=10, padx=(0,35))
    self.chkbxrunningcfg = ctk.CTkCheckBox(self.tftpuploadwindow, text="running-config", command=lambda:chkbxrunningcfg_event(self), variable=self.chkbxrunningcfg_var, onvalue="on", offvalue="off", fg_color="green4", hover_color="dark slate gray", border_color="dark slate gray", border_width=2, text_color_disabled="gray")
    self.chkbxrunningcfg.grid(row=8, column=0, pady=10, sticky=W, padx=(25,0))
    self.chkbxstartupcfg = ctk.CTkCheckBox(self.tftpuploadwindow, text="startup-config", command=lambda:chkbxstartupcfg_event(self), variable=self.chkbxstartupcfg_var, onvalue="on", offvalue="off", fg_color="green4", hover_color="dark slate gray", border_color="dark slate gray", border_width=2, text_color_disabled="gray")
    self.chkbxstartupcfg.grid(row=8, column=1, pady=10, sticky=W)
    self.checkboxcstrn = ctk.CTkCheckBox(self.tftpuploadwindow, text="copy startup > runnning", command=lambda:checkboxcstrn_event(self), variable=self.checkboxcstrn_var, onvalue="on", offvalue="off", fg_color="green4", hover_color="dark slate gray", border_color="dark slate gray", border_width=2, text_color_disabled="gray")
    self.checkboxcstrn.grid(row=8, column=2, pady=10, padx=(0,35))
    self.virtspr1 = ttk.Separator(self.tftpuploadwindow, orient='vertical')
    self.virtspr1.grid(row=7, column=1, sticky='nsw', rowspan=2, pady=(10,5), padx=(180,1))
    
    self.horizspr2 = ttk.Separator(self.tftpuploadwindow, orient='horizontal')
    self.horizspr2.grid(row=9, column=0, sticky=EW, columnspan=3, padx=(20), pady=(10))

    self.btnupload = ctk.CTkButton(self.tftpuploadwindow, text="Upload", command=lambda:tftptorouter(self), state='disabled', width=240, fg_color="gray", font=('arial', 12, 'bold'), hover_color='green4', border_width=2, border_color='gray')
    self.btnupload.grid(row=11, column=0, padx=30, pady=10, sticky=W)
    self.btnclose = ctk.CTkButton(self.tftpuploadwindow, text = "Exit", width=140, fg_color="red3", font=('arial', 12, 'bold'), hover_color='red4', border_width=2, border_color='red4', command=self.tftpuploadwindow.destroy)
    self.btnclose.grid(row=11, column=2,  pady=10, sticky=E, padx=(10,30))
    self.statuslbl = tk.Label(self.tftpuploadwindow, text="Select a device", font=('arial', 12, 'bold'), bg='powder blue', fg='OrangeRed2')
    self.statuslbl.grid(row=11, column=1)

    self.progstatus = ctk.CTkProgressBar(self.tftpuploadwindow, progress_color='green4', border_width=1, border_color='dark slate gray')
    self.progstatus.grid(row=12, column=0, sticky=EW, padx=30, pady=5, columnspan=3)
    self.progstatus.set(0)
