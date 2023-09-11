from settings import *
from tkinter import *
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import ImageTk, Image
import customtkinter as ctk
import sqlite3
from mysql.connector import Error
import os
from os.path import exists
import json
from connecttodb import getdevicefromid
import shutil
from netmiko import ConnectHandler 
from netmiko.exceptions import NetMikoAuthenticationException
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
#from netmiko.ssh_exception import NetMikoAuthenticationException
#from netmiko.ssh_exception import NetMikoTimeoutException
#from netmiko.ssh_exception import SSHException


def configuploadtftpgroup(self):

    # Generates the IDs of the members of the group
    self.idsofmembers=[]
    
    # dropdown group selection box and selection in the box is the var value
    self.tftpgrpseleccbx = []
    self.tftpgrpcombxstr_var = ctk.StringVar(self)

    # holding the switch value on / off
    self.grpnameswitch_var = ctk.StringVar(self)

    # tftp particulars
    self.tftpselectedid=StringVar(self)
    self.setbackuptypevar=StringVar(self) # Bakup type (startup, running)
    self.setfileidtypevar=StringVar(self) # File identifier (weekly, golden ?)
    self.filename = StringVar(self)
    self.filedest = StringVar(self)
    self.filesrc = StringVar(self)
    self.tftprootdir = StringVar(self)
    self.tftprootdir.set(tftprootdir) # C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\tftp_temp

    # Values of the checkboxes
    self.checkboxcopygrp_var = ctk.StringVar(value="off") # Copy(merge) config
    self.checkboxreplgrp_var = ctk.StringVar(value="off")# Replace running config
    self.checkboxcrsgrp_var = ctk.StringVar(value="off") # 'copy running > startup'
    self.checkboxcstrngrp_var = ctk.StringVar(value="off") # copy startup > running
    self.chkbxrunningcfgrp_var = ctk.StringVar(value="off") # running-config
    self.chkbxstartupcfgrp_var = ctk.StringVar(value="off") # startup-config 

    self.tftpuploadcmd = ctk.StringVar(self)
    
    # Evaluate the value of the checkbox to determin running or startup
    self.running_startup_vargrp = StringVar(self)

    #self.returnedid = IntVar(self)
    #self.returnedname = StringVar(self)
    #self.returnedip = StringVar(self)
    #self.returnedusername = StringVar(self)
    #self.returnedpassword = StringVar(self)
    #self.returneddescription = StringVar(self)
    #self.returnedtype = StringVar(self)
    #self.returnedgolden = StringVar(self)
    
    print("configuploadtftpgroup")
    self.tftpuploadgroupw = tk.Toplevel()
    self.tftpuploadgroupw.geometry("730x820+200+200")
    self.tftpuploadgroupw.title("TFTP Upload to group")
    self.tftpuploadgroupw.configure(background='powder blue')
    #self.tftpuploadgroupw.resizable(False, False)
    self.tftpuploadgroupw.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

    # Disable root window when this one is active
    self.tftpuploadgroupw.attributes('-topmost', 'true')
    self.tftpuploadgroupw.transient(self)
    self.tftpuploadgroupw.update_idletasks()
    self.tftpuploadgroupw.grab_set()

    #self.tftpuploadgroupw.grid_columnconfigure(0, weight=1)
    #self.tftpuploadgroupw.grid_columnconfigure(0, weight=0)
    #self.tftpuploadgroupw.grid_columnconfigure(1, weight=0)
    #self.tftpuploadgroupw.grid_columnconfigure(2, weight=2)
    
    def tftpgrpgobtn(self):
        self.grpnotetxtbx.configure(state='normal', bg="light goldenrod yellow")
        self.grpnotetxtbx.insert('end', "This is a list of id members of the group\n")
        self.grpnotetxtbx.insert('end', f"{self.idsofmembers}\n")
        # Disable the GoGroup button
        self.tftpgrpgo.configure(state='disabled', fg_color='gray', border_color='gray')
        # Disable the switch
        self.grpnameswitch.configure(state='disabled', fg_color='gray50', button_color='gray30', border_color='gray30', progress_color='gray', text_color='gray20')
        # Disable checkbox selections
        self.checkboxcopygrp.select()
        self.checkboxcopygrp.configure(state='disabled', fg_color="gray", border_color="gray") # Copy(merge) config
        self.chkbxrunningcfgrp.select()
        self.chkbxrunningcfgrp.configure(state='disabled', fg_color="gray", border_color="gray") # running-config
        self.checkboxreplgrp.deselect()
        self.checkboxreplgrp.configure(state='disabled', fg_color="gray", border_color="gray") # Replace running-config
        self.chkbxstartupcfgrp.deselect()
        self.chkbxstartupcfgrp.configure(state='disabled', fg_color="gray", border_color="gray") # startup-config
        self.checkboxcrsgrp.deselect()
        self.checkboxcrsgrp.configure(state='disabled', fg_color="gray", border_color="gray") # copy running > startup
        self.checkboxcstrngrp.deselect()
        self.checkboxcstrngrp.configure(state='disabled', fg_color="gray", border_color="gray") # copy startup > running


        count = 0
        for i in self.idsofmembers:
            count += 1
            print(f"{i}")
            retid = 0
            retname = ""
            retip = ""
            retusername = ""
            retpassword = ""
            retdescription = ""
            rettype = ""
            retgolden = ""
            
            retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getdevicefromid(i)
            print(f"{retid}"+f"{retname}"+f"{retip}"+f"{retusername}"+f"{retpassword}"+f"{retdescription}"+f"{rettype}"+f"{retgolden}")
            self.grpnotetxtbx.insert('end', f"id:{retid}\nhostname:{retname}\nip:{retip}\nfile:{retgolden}\n")

            self.progstatus1.set(0.3)
            self.update_idletasks()

            os.chdir(self.tftprootdir.get())
            print(f"4b) Upload to Device name: {retname}")
            print(f"4c) The current working directory is : {os.getcwd()}")
            # What is the file name
            print(f"4d) File name to look for is: {retgolden}")

            self.grpnotetxtbx.insert(INSERT, f"2) Looking for file in the TFTP staging area:\n{retgolden}\n")
            
            # Evaluate the value of the checkbox to determin running or startup
            # # self.running_startup_var = StringVar()
            if self.chkbxstartupcfgrp_var.get() == "on":
                self.running_startup_vargrp.set("startup-config")
                print(f"chkbxrunningcfgrp_var value = {self.chkbxrunningcfgrp_var.get()}")
            elif self.chkbxrunningcfgrp_var.get() == "on":
                self.running_startup_vargrp.set("running-config")
                print(f"chkbxstartupcfgrp_var value = {self.chkbxstartupcfgrp_var.get()}")
            else:
                print("uploadtftp.py(tftprouter) error occured getting checbxstartupcfg_var or checbxrunningcfg_var")

            if os.path.isfile(retgolden):
                print("4)d File exist in the TFTP staging directory: so lets go")

                self.tftpstatuslbl.configure(text=f'Running task on: {retname}') # font=('arial', 12, 'bold'), 
                self.progstatuslbl.configure(text=f"id:{retid} ({retname})")
                self.update_idletasks()

                cisco_device = {
                    'device_type': f'{rettype}',
                    'host': f'{retip}',
                    'username': f'{retusername}',
                    'password': f'{retpassword}',
                    'port': 22,
                    'secret': f'{retpassword}',
                    'verbose': True}
                
                self.grpnotetxtbx.insert(INSERT, f"3) Initiating Connection to : {retname}\n")

                conn = ConnectHandler(**cisco_device)
                conn_prompt = conn.find_prompt()
                if '>' in conn_prompt: conn.enable()
                output = conn.send_command(f"\n") # what do enter into the devices command line to accept a tftp upload ?
                print(f"Checking the config mode: {conn.check_config_mode()}")
                self.grpnotetxtbx.insert(INSERT, f"4) The config mode on the device is: {conn.check_config_mode()}\n")

                self.progstatus1.set(0.4)
                self.update_idletasks()

                try:
                    name = f"device{str(1)}"
                    net_connect = ConnectHandler(**cisco_device)
                    print("Try 1a")
                    net_connect.enable()
                    hostname = net_connect.find_prompt()[:-1]
                    print(f"The hosname found on the device is: {hostname}")
                    self.grpnotetxtbx.insert(INSERT, f"5) The hostname on the device is: {hostname}\n")
                    
                    print(f"The value of checkboxcopygrp_var is: {self.checkboxcopygrp_var.get()}")
                    
                    self.tftpstatuslbl.configure(font=('arial', 12, 'bold'), text='Task in progress')
                    self.progstatus1.set(0.5)
                    self.update_idletasks()

                    if self.checkboxcopygrp_var.get() == "on": # Copy(merge) config
                        # Option1 Copy tftp > 'running-config' Option2 Copy tftp > 'startup-config'
                        # option changes due to value in running_startup_var
                        print("Option2 'startup-config checkboxcopygrp_var")
                        self.tftpuploadcmd.set(f"copy tftp://{tftpserver}{tftprootdir}/{retgolden} {self.running_startup_vargrp.get()}")
                        self.grpnotetxtbx.insert(INSERT, f"6) Sending the command: {self.tftpuploadcmd.get()}\n")
                        print(f"Try 1b (uploadtftp)copy_command:{self.tftpuploadcmd.get()}")
                        output = net_connect.send_command_timing(self.tftpuploadcmd.get())
                        if "Address or name" in output:
                            output += net_connect.send_command_timing(f"{tftpserver}\n")
                            print("Try 2")
                        if "Source filename" in output:
                            output += net_connect.send_command_timing(f"{retgolden}\n")
                            print("Try 3")
                            net_connect.disconnect
                        if "Destination filename" in output:
                            output += net_connect.send_command_timing(f"\n")
                            print("Try 4 ---- I THINK IT DID IT")
                            self.grpnotetxtbx.insert(INSERT, f"7) Running the command on the device.\n")
                        
                        self.progstatus1.set(0.7)
                        self.update_idletasks()

                        # 'running-config' checkbox on + 'copy running > startup' checkbox on
                        print(f"COPY IF~chkbxrunningcfgrp_var on: {self.chkbxrunningcfgrp_var.get()}")
                        print(f"COPY IF~checkboxcrsgrp_var on: {self.checkboxcrsgrp_var.get()}")
                        if self.chkbxrunningcfgrp_var.get() == "on" and self.checkboxcrsgrp_var.get() == "on":
                            print("This is TFTP > running-config and copy startup > running")
                            print(f"This is TFTP > running-config on: {self.chkbxrunningcfgrp_var.get()}")
                            print(f"copy running > startup on: {self.checkboxcrsgrp_var.get()}")
                            # Running = copy running-config startup-config
                            copy_command1 = "copy running-config startup-config"
                            output1 = net_connect.send_command_timing(copy_command1)
                            self.grpnotetxtbx.insert(INSERT, f"Output1:\n{output1}\n")
                        
                            if "Destination filename" in output1:
                                output1 += net_connect.send_command_timing("\n")
                                self.grpnotetxtbx.insert(INSERT, f"copy running-config startup-config: COMPLETED\n{output1}\n")
                            else:
                                print("else - self.checkboxcrs_var.get() Destination filename not found ")
                                print(f"'copy running > startup'=off: {self.checkboxcrsgrp_var.get()} ")
                    
                            self.progstatus1.set(0.8)
                            self.update_idletasks()

                        # Copy(merge) config = on
                        # running config checkbox + copy running > startup
                        print(f"COPY IF~chkbxstartupcfgrp_var on: {self.chkbxstartupcfgrp_var.get()}")
                        print(f"COPY IF~checkboxcstrngrp_var on: {self.checkboxcstrngrp_var.get()}")
                        if self.chkbxstartupcfgrp_var.get() == "on" and self.checkboxcstrngrp_var.get() == "on":
                            print("This is TFTP > startup-config and copy startup > running")
                            print(f"This is TFTP > startup on: {self.chkbxstartupcfgrp_var.get()}")
                            print(f"copy startup > running on: {self.checkboxcstrngrp_var.get()}")
                            # Running = copy running-config startup-config
                            copy_command1 = "copy startup-config running-config "
                            output1 = net_connect.send_command_timing(copy_command1)
                            self.grpnotetxtbx.insert(INSERT, f"Output1:\n{output1}\n")
                            
                            if "Destination filename" in output1:
                                output1 += net_connect.send_command_timing("\n")
                                self.grpnotetxtbx.insert(INSERT, f"copy startup-config running-config: COMPLETED\n{output1}\n")
                            
                            else:
                                print("else - self.checkboxcrs_var.get() Destination filename not found ")
                                print(f"'copy running > startup'=off: {self.checkboxcstrngrp_var.get()} ")
                            
                            self.progstatus1.set(0.8)
                            self.update_idletasks()
                        
                        # copy startup-config > running-config
                        print(f"COPY IF~chkbxstartupcfg_var on: {self.chkbxstartupcfgrp_var.get()}")
                        print(f"COPY IF~checkboxcstrn_var on: {self.checkboxcstrngrp_var.get()}")
                        if self.chkbxstartupcfgrp_var.get() == "on" and self.checkboxcstrngrp_var.get() == "on":
                            print("This is TFTP > startup and copy startup > running")
                            print(f"This is TFTP > startup on: {self.chkbxstartupcfgrp_var.get()}")
                            print(f"copy startup > running on: {self.checkboxcstrngrp_var.get()}")
                            # Running = copy running-config startup-config
                            copy_command1 = "copy startup-config running-config"
                            output1 = net_connect.send_command_timing(copy_command1)
                            self.grpnotetxtbx.insert(INSERT, f"Output1:\n{output1}\n")
                            
                            if "Destination filename" in output1:
                                output1 += net_connect.send_command_timing("\n")
                                self.grpnotetxtbx.insert(INSERT, f"startup-config > running-config output:\n{output1}\n")
                                self.grpnotetxtbx.insert(INSERT, "------------------------------------------------\n")
                                self.grpnotetxtbx.insert(INSERT, f"Request completed: startup-config has been copied to the running-config\n")
                                self.grpnotetxtbx.insert(INSERT, "------------------------------------------------\n")
                            else:
                                print("else - self.checkboxcrs_var.get() Destination filename not found ")
                                print(f"'copy running > startup'=off: {self.checkboxcrsgrp_var.get()} ")
                            
                            self.progstatus1.set(0.8)
                            self.grpnotetxtbx.see('end')
                            self.update_idletasks()
                        
                    elif self.checkboxreplgrp_var.get() == "on":
                        # CONFIGURE REPLACE checkboxrepl
                        print("CONFIGURE REPLACE")
                        print(f"CONFIGURE REPLACE self.checkboxreplgrp_var: {self.checkboxreplgrp_var.get()}")
                        self.tftpuploadcmd.set(f"configure replace tftp://{tftpserver}{tftprootdir}/{retgolden} force") 
                        self.grpnotetxtbx.insert(INSERT, f"6) Sending the command: {self.tftpuploadcmd.get()}\n")
                        print(f"Try 1b (uploadtftp)copy_command:{self.tftpuploadcmd.get()}")
                        output = net_connect.send_command_timing(self.tftpuploadcmd.get())
                        self.grpnotetxtbx.insert(INSERT, f"7) Output:\n{output}\n")

                        if self.checkboxcrsgrp_var.get() == "on":
                            # Running = copy running-config startup-config
                            copy_command1 = "copy running-config startup-config"
                            output1 = net_connect.send_command_timing(copy_command1)
                            self.grpnotetxtbx.insert(INSERT, f"8) Output1:\n{output1}\n")
                        
                            if "Destination filename" in output1:
                                output1 += net_connect.send_command_timing("\n")
                                self.grpnotetxtbx.insert(INSERT, f"8a) running-config > startup-config output:\n{output1}\n")
                                self.grpnotetxtbx.insert(INSERT, "------------------------------------------------\n")
                                self.grpnotetxtbx.insert(INSERT, f"Request completed: running-config has been copied to the startup-config\n")
                                self.grpnotetxtbx.insert(INSERT, "------------------------------------------------\n")
                            else:
                                print("else - self.checkboxcrs_var.get() Destination filename not found ")
                                print(f"'copy running > startup'=off: {self.checkboxcrsgrp_var.get()} ")
                        else:
                            print("self.checkboxcrs_var.get() == 'off' so not running 'copy running > startup'")
                            print(f"'copy running > startup'=off: {self.checkboxcrsgrp_var.get()} ")

                        self.progstatus.set(0.8)
                        self.grpnotetxtbx.see('end')
                        self.update_idletasks()
                
                # Write some more specific exception classes for Netmiko exceptions
                # netmiko.exceptions.NetmikoTimeoutException
                except NetMikoAuthenticationException as AuthException:
                    print("(uploadtftpgroup.py 289): Authentication Error" % AuthException)
                    self.grpnotetxtbx.insert(INSERT, "5) (uploadtftpgroup.py 290) Authentication Error \n"% AuthException)
                    continue
                except NetMikoTimeoutException as TimeoutException:
                    #raise ConnectError(TimeoutException.args[0])
                    print("(uploadtftpgroup.py 293): No Valid Connections Error SSH connection 'USERNAME ?': %s" % TimeoutException)
                    self.grpnotetxtbx.insert(INSERT, "5) (uploadtftpgroup.py 295) TimeoutException Error \n" % TimeoutException)
                    continue
                except SSHException as sshexception:
                    print("An netmiko sshexception Error" % sshexception)
                    self.grpnotetxtbx.insert(INSERT, "5) (uploadtftpgroup.py 299) An netmiko SSHException Error \n" % sshexception)
                    continue
                except Exception as unknown_error:
                    print("An netmiko function exception occurred in tftpconfig(uploadtftpgroup.py)"+ str(unknown_error))
                    self.grpnotetxtbx.insert(INSERT, "5) An error occured in the try block unknown_error\n" % unknown_error)
                    continue

                finally:
                    print("Doing net_connect.disconnect")
                    net_connect.disconnect
                    self.grpnotetxtbx.insert(INSERT, "------------------------------------------------\n")
                    self.grpnotetxtbx.insert(INSERT, f"Request was completed {retname} has a new {self.running_startup_vargrp.get()}\n")
                    self.grpnotetxtbx.insert(INSERT, "------------------------------------------------\n")
                    print(f"The file I want to delete is:\n{tftprootdir}/{retgolden}")
                    # Lets delete the file from the staging area
                    if os.path.exists(f"{tftprootdir}/{retgolden}"):
                        os.remove(f"{tftprootdir}/{retgolden}")
                        print("File Deleted from TFTP Staging area")
                    else:
                        print(f"I couldn't delete the file:\n{tftprootdir}/{retgolden}")
                        self.grpnotetxtbx.insert(INSERT, f"9) (finally|else 352) I couldn't delete the file:\n{tftprootdir}/{retgolden}")


                    self.grpnotetxtbx.insert(INSERT, F"-----------------------------End ({retname})-------------------------------\n")
                    self.tftpstatuslbl.configure(text='Task Completed')
                    self.grpnotetxtbx.see('end')
                    self.progstatus1.set(1)
                    self.update_idletasks()

            
            else:
                print("4e) File is not in the tftp directory")
                self.grpnotetxtbx.insert(INSERT, f"File or Location ERROR\n")
                self.grpnotetxtbx.insert(INSERT, f"1) Expected file:\n {retgolden}\n")
                self.grpnotetxtbx.insert(INSERT, f"2) Expected location:\n {self.tftprootdir.get()}\n")
        
        self.grpnotetxtbx.insert(INSERT, f"--------------------Tasks Finished ({self.tftpgrpcombxstr_var.get()})-------------------------------")
        self.grpnotetxtbx.see('end')
        self.grpnotetxtbx.configure(state='disabled', bg="light goldenrod yellow")




    # Populate the Groups into the Combobox selection dropdown
    def populatemembxg(self, *args, **kwargs):
        #self.tftpgrpcombx.configure(state='normal')
        os.chdir(devicegroups)
        #print(f"1a) The current working directory is : {os.getcwd()}")
        #print(f"devicegroups = {devicegroups}")
        items = os.listdir(devicegroups)
        print(f"items = {items}")
        for item in items:
            if os.path.isdir(item):
                #print(f"item = {item}")
                self.tftpgrpseleccbx.append(item)
                #print(f"self.tftpgrpseleccbx = {self.tftpgrpseleccbx}")
        
        self.tftpgrpcombx.configure(values=self.tftpgrpseleccbx)


    def tftpgrpcombxcallback(self):
        print(f"grpseleccbxcallback")
        print("Clear the table if not clear")
        #self.tftpgrptbl.delete(*self.tftpgrptbl.get_children())
        #self.tftpgrptbl.delete(*self.tftpgrptbl.get_children())
        print(f"Whats the group in the dropdown box ?: {self.tftpgrpcombx.get()}")
        #print(f"TryAgain = {self.grpnamecbx.get()}")
        #self.grpconfirmbtn.configure(state='enabled', fg_color='green')
        #self.grploadbtn.configure(state='enabled', fg_color='green')

        # Auto generate the table
        self.grpnameswitch.configure(state='normal', fg_color='pale green', button_color='dark slate gray', border_color='dark slate gray', text_color='black')
        tftpgrpcbxselc(self)


        
    # Checkbox = Copy(merge) config (uploadtftp = checkboxcopy_event)
    def checkboxcopygrp_event(self):
        print(f"I am checkboxcopygrp_event: {self.checkboxcopygrp.get()}")
        if self.checkboxcopygrp.get() == "on":
            # deactivate 'Replace running config'
            self.checkboxreplgrp.deselect()
            # Activate 'running-config'
            self.chkbxrunningcfgrp.configure(border_color="dark slate gray", state="normal")
            # Activate 'startup-config'
            self.chkbxstartupcfgrp.configure(border_color="dark slate gray", state="normal")
            # Activate 'copy startup > running'
            self.checkboxcstrngrp.configure(border_color="dark slate gray", state="normal")
            #'copy  running > startup'
            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(border_color="dark slate gray", state="normal")
            #'copy startup > running'
            self.checkboxcstrngrp.deselect() 
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled")
            # select running config by default
            self.chkbxrunningcfgrp.select()

        else:
            # activate 'Replace running config'
            self.checkboxreplgrp.select()
            #  deactivate & disable 'running-config'
            self.chkbxrunningcfgrp.deselect()
            self.chkbxrunningcfgrp.configure(border_color="gray", state="disabled")
            #  deactivate & disable 'startup-config'
            self.chkbxstartupcfgrp.deselect()
            self.chkbxstartupcfgrp.configure(border_color="gray", state="disabled")
            # deselect and disable 'copy startup > running'
            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled")
            #'copy  running > startup'
            self.checkboxcrsgrp.deselect() 
            self.checkboxcrsgrp.configure(border_color="dark slate gray", state="normal")

    # Checkbox = Replace running config
    def checkboxreplgrp_event(self):
        print(f"I am checkboxreplgrp_event: {self.checkboxreplgrp.get()}")
        self.checkboxcopygrp.deselect()
        #self.checkboxreplgrp.configure(fg_color="green4")

        if self.checkboxreplgrp.get() == "on":
            #'copy  running > startup'
            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(border_color="dark slate gray", state="normal")
            #'copy startup > running'
            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled")
            #  deactivate & disable 'running-config'
            self.chkbxrunningcfgrp.deselect()
            self.chkbxrunningcfgrp.configure(border_color="gray", state="disabled")
            #  deactivate & disable 'startup-config'
            self.chkbxstartupcfgrp.deselect()
            self.chkbxstartupcfgrp.configure(border_color="gray", state="disabled")

            self.running_startup_vargrp.set("running-config")
        else:
            # Copy(merge) config selected
            self.checkboxcopygrp.select()
            # running-config active and selected
            self.chkbxrunningcfgrp.configure(border_color="dark slate gray", state="normal")
            self.chkbxrunningcfgrp.select()
            #  activate 'startup-config'
            self.chkbxstartupcfgrp.deselect()
            self.chkbxstartupcfgrp.configure(border_color="dark slate gray", state="normal")
            # deactivate 'copy running > startup'
            self.checkboxcrsgrp.deselect()
    
    # Checkbox = running config #chkbxrunningcfg
    def chkbxrunningcfgrp_event(self):
        print(f"I am chkbxrunningcfgrp_event: {self.chkbxrunningcfgrp.get()}")
        if self.chkbxrunningcfgrp.get()=="on":
            self.chkbxstartupcfgrp.deselect()
            #'copy  running > startup'
            self.checkboxcrsgrp.configure(border_color="dark slate gray", state="normal") 
            # copy startup > running
            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled") #'copy startup > running'

        else:
            self.chkbxstartupcfgrp.select()
            # 'copy running > startup' deselect and disable
            self.checkboxcrsgrp.deselect() #'copy  running > startup'
            self.checkboxcrsgrp.configure(border_color="gray", state="disabled") #'copy  running > startup'
            # copy startup > running deselect and enable
            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(border_color="dark slate gray", state="normal") #'copy startup > running'

    # Checkbox = startup config
    def chkbxstartupcfgrp_event(self):
        print(f"I am chkbxstartupcfgrp_event: {self.chkbxstartupcfgrp.get()}")
        self.checkboxcstrngrp.deselect()

        if self.chkbxstartupcfgrp.get() == "on":
            # 'running-config' = deselect
            self.chkbxrunningcfgrp.deselect()
            # 'copy running > startup' deselect
            self.checkboxcrsgrp.deselect()
            # copy 'startup > running' enable
            self.checkboxcstrngrp.configure(border_color="dark slate gray", state="normal")
            # 'copy running > startup' disable
            self.checkboxcrsgrp.configure(border_color="gray", state="disabled")
        
        else:
            # running-config select
            self.chkbxrunningcfgrp.select()
            # 'copy running > startup' deselect & normalise
            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(border_color="dark slate gray", state="normal")
            # copy 'startup > running' disabled
            self.checkboxcstrngrp.configure(border_color="gray", state="disabled") 

    # Checkbox = copy runnning > startup #checkboxcrs
    def checkboxcrsgrp_event(self):
        print(f"I am checkboxcrsgrp_event: {self.checkboxcrsgrp.get()}")
    
    # copy startup > runnning
    def checkboxcstrngrp_event(self):
        print(f"I am checkboxcstrngrp_event: {self.checkboxcstrngrp.get()}")

    def tftpgrpcbxselc(self):
        self.tftpgrptbl.delete(*self.tftpgrptbl.get_children())
        print("set button")
        print(f"set button value = {self.tftpgrpcombx.get()}")

        print("Go off and populate the table with the groups details")

        # Get the members of the selected group
        # Get into the right folder
        groudevicepath = os.path.join(devicegroups, self.tftpgrpcombx.get())
        # load the file
        dest_path = os.path.join(groudevicepath, self.tftpgrpcombx.get() + ".json")
        filetoread = open(dest_path)
        inputjsondata = json.load(filetoread)
        print(f"Addbutton filetoread = {filetoread}")
        print(f"Addbutton inputjsondata = {inputjsondata}")

        # change members selection
        #inputjsondata['members'] = fvmemselec
        print(f"1) Data in members: {inputjsondata['members']}")

        self.idsofmembers=inputjsondata['members']
        print(f"idsofmembers: {self.idsofmembers}")
        
        count = 0

        for i in self.idsofmembers:
            count += 1
            print(f"{i}")
            retid = 0
            retname = ""
            retip = ""
            retusername = ""
            retpassword = ""
            retdescription = ""
            rettype = ""
            retgolden = ""
            
            retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getdevicefromid(i)
            print(f"{retid}"+f"{retname}"+f"{retip}"+f"{retusername}"+f"{retpassword}"+f"{retdescription}"+f"{rettype}"+f"{retgolden}")
            self.tftpgrptbl.insert(parent='', index='end', iid=count, text=count, values=(f'{retid}',f'{retname}',f'{retip}',f'{retgolden}'))
        
        # count the number of devices in the group display in status label
        self.tftpstatuslbl.configure(text="Number of devices in group: " + str(count))

    def tftpgrpconfirm(self):
        print("tftpgrpconfirm(self): Pressed / switched")
  
        '''
        # This section gets the treeview data and copys the file to the sataging tftp area
        devlist = []
        devlistcount = 0
        #print(f"devlist 0 1 = {devlist[0][1]}")
        for child in self.tftpgrptbl.get_children():
            devlist.append(self.tftpgrptbl.item(child)['values'])

        for file in devlist:
            print(f"devlistcount: {str(devlistcount)}")
            # file source
            self.filesrc.set(f"{devicesaveddata}/{devlist[devlistcount][1]}/{devlist[devlistcount][3]}")
            # file destination
            self.filedest.set(f"{tftprootdir}/{devlist[devlistcount][3]}")
            print(f"self.filesrc: {self.filesrc.get()}")
            print(f"self.filedest: {self.filedest.get()}")
            # copy file
            
            try:
                shutil.copy(self.filesrc.get(), self.filedest.get())
                self.grpnotetxtbx.insert(INSERT, f"{devlistcount}) File ready: {devlist[devlistcount][3]}\n")

            except:
                print(f"File copy problem {devlist[devlistcount][3]}")
                self.grpnotetxtbx.insert(INSERT, f"{devlistcount}) Problem preparing file: {devlist[devlistcount][3]}\n")


            devlistcount +=1
        '''
        



        if self.grpnameswitch_var.get() == 'on':
            print(f"571 - self.grpnameswitch_var = on : {self.grpnameswitch_var.get()}")

            # Disable Grop selection box
            self.tftpgrpcombx.configure(state='disabled', fg_color='gray80', border_color='gray', button_color='gray')

            # Treeview gray out
            self.tftpgrptbl.configure(style="dbgray.Treeview")

            # Enable checkbox selections
            self.checkboxcopygrp.configure(state='normal', fg_color="green4", border_color="dark slate gray") # Copy(merge) config
            self.chkbxrunningcfgrp.configure(state='normal', fg_color="green4", border_color="dark slate gray") # running-config
            self.checkboxreplgrp.configure(state='normal', fg_color="green4", border_color="dark slate gray") # Replace running-config
            self.chkbxstartupcfgrp.configure(state='normal', fg_color="green4", border_color="dark slate gray") # startup-config
            self.checkboxcrsgrp.configure(state='normal', fg_color="green4", border_color="dark slate gray") # copy running > startup
            self.checkboxcstrngrp.configure(fg_color="green4", border_color="gray") # copy startup > running
            

            # Go Button
            self.tftpgrpgo.configure(state='normal', fg_color="green4", border_color='dark green')

            
            # Output box
            self.grpnotetxtbx.configure(state='normal', bg="light goldenrod yellow")
            devlist = []
            devlistcount = 0
            #print(f"devlist 0 1 = {devlist[0][1]}")
            for child in self.tftpgrptbl.get_children():
                devlist.append(self.tftpgrptbl.item(child)['values'])
            
            for file in devlist:
                print(f"devlistcount: {str(devlistcount)}")
                # file source
                self.filesrc.set(f"{devicesaveddata}/{devlist[devlistcount][1]}/{devlist[devlistcount][3]}")
                # file destination
                self.filedest.set(f"{tftprootdir}/{devlist[devlistcount][3]}")
                print(f"self.filesrc: {self.filesrc.get()}")
                print(f"self.filedest: {self.filedest.get()}")
                # copy file

                try:
                    shutil.copy(self.filesrc.get(), self.filedest.get())
                    self.grpnotetxtbx.insert(INSERT, f"{devlistcount+1}) File ready: {devlist[devlistcount][3]}\n")
                
                except:
                    print(f"File copy problem {devlist[devlistcount][3]}")
                    self.grpnotetxtbx.insert(INSERT, f"{devlistcount+1}) Problem preparing file: {devlist[devlistcount][3]}\n")
                    
                devlistcount +=1
            self.grpnotetxtbx.configure(state='disabled')


        if self.grpnameswitch_var.get() == 'off':
            print(f"self.grpnameswitch_var = off : {self.grpnameswitch_var.get()}")

            # Enable group selection combobox
            self.tftpgrpcombx.configure(state='normal', fg_color='yellow2', border_color='dark slate gray', button_color='dark slate gray') 

            # Treeview selection normal
            self.tftpgrptbl.configure(style="db.Treeview")

            # clear the output scroolbar
            self.grpnotetxtbx.configure(state='normal')
            self.grpnotetxtbx.delete('1.0', END)
            self.grpnotetxtbx.configure(state='disabled', bg="gray60")

            # DO I NEED TO CLEAR THE TFTP TEMPORARY AREA ?
            #print("594 - DO I NEED TO CLEAR THE TFTP TEMPORARY AREA ? = yes")
            if len(os.listdir(filesource)) > 0:
                print(" 617 - (uploadtftpgroup) Clearing the TFTP AREA of any existing files")
                # shutil.rmtree(filesource)
                for f in os.listdir(filesource):
                    os.remove(os.path.join(filesource, f))
            
            # Disable checkbox selections
            self.checkboxcopygrp.select()
            self.checkboxcopygrp.configure(state='disabled', fg_color="gray", border_color="gray") # Copy(merge) config
            self.chkbxrunningcfgrp.select()
            self.chkbxrunningcfgrp.configure(state='disabled', fg_color="gray", border_color="gray") # running-config
            self.checkboxreplgrp.deselect()
            self.checkboxreplgrp.configure(state='disabled', fg_color="gray", border_color="gray") # Replace running-config
            self.chkbxstartupcfgrp.deselect()
            self.chkbxstartupcfgrp.configure(state='disabled', fg_color="gray", border_color="gray") # startup-config
            self.checkboxcrsgrp.deselect()
            self.checkboxcrsgrp.configure(state='disabled', fg_color="gray", border_color="gray") # copy running > startup
            self.checkboxcstrngrp.deselect()
            self.checkboxcstrngrp.configure(state='disabled', fg_color="gray", border_color="gray") # copy startup > running

            # Deactivate Go Button
            self.tftpgrpgo.configure(state='disabled', fg_color="gray", border_color='gray')


    # Top Frame
    self.topframea = ctk.CTkFrame(master=self.tftpuploadgroupw, fg_color='powder blue', height=30) # OUTPUT DATA AREA
    self.topframea.pack(fill='both', expand=False, side='top')
    self.topframea.pack_propagate(True)
    self.lbltopa = ctk.CTkLabel(self.topframea, text="Upload a configuration to a group of devices.", font=('arial', 22, 'bold'))
    self.lbltopa.pack(pady=(15,7), side='top')
    self.separator1 = ttk.Separator(self.topframea, orient='horizontal')
    self.separator1.pack(padx=20, pady=(5,10), fill='x', expand=True, side='top')

    self.grpname = ctk.CTkLabel(self.topframea, text="Group name", font=('arial', 18, 'bold'))
    self.grpname.pack(anchor='w', padx=(30,30), pady=(1,20), side='left')
    self.tftpgrpcombx = ctk.CTkComboBox(self.topframea, state='normal', command=lambda v: tftpgrpcombxcallback(self), variable=self.tftpgrpcombxstr_var, width=270, height=30, fg_color='yellow2', font=('arial', 14, 'bold'), border_color='dark slate gray', button_color='dark slate gray', dropdown_fg_color='khaki', border_width=2, dropdown_hover_color='khaki3', dropdown_font=('arial', 14, 'bold')) # , values=memseleccbxvar
    self.tftpgrpcombx.pack(padx=(60,0), pady=(1,20), side='left')
    self.tftpgrpcombx.set("Group Selection")
    #self.grpconfirmbtn = ctk.CTkButton(self.topframea, text="Confirm", state='disabled', width=100, fg_color="gray", hover_color='green4', command=lambda:tftpgrpconfirm(self)) # 
    #self.grpconfirmbtn.pack(padx=(0,30), pady=(1,20), side='right')
    #self.grploadbtn = ctk.CTkButton(self.topframea, text="Load", state='disabled', width=100, fg_color="gray", hover_color='green4', command=lambda:tftpgrpcbxselc(self)) # 
    #self.grploadbtn.pack(padx=(0,10), pady=(1,20), side='right')
    self.grpnameswitch = ctk.CTkSwitch(self.topframea, text="Unlock | Lock", onvalue="on", offvalue="off", switch_width=40, switch_height=20, fg_color='gray50', button_color='gray30', border_width=2, border_color='gray30', progress_color='yellow', text_color='gray20', command=lambda:tftpgrpconfirm(self), variable=self.grpnameswitch_var) # command=grpnameswitch_event, variable=self.grpnameswitch_var,
    self.grpnameswitch.pack(padx=(0,30), pady=(1,20), side='right')
    self.grpnameswitch.configure(state='disabled')


    # Center Frame
    self.centerframe = ctk.CTkFrame(master=self.tftpuploadgroupw, fg_color="powder blue") # OUTPUT DATA AREA
    self.centerframe.pack(fill='both', expand=True, side='top')
    self.topframea.pack_propagate(True)
    
    # Output textscroll
    self.grpnotetxtbx = scrolledtext.ScrolledText(master=self.centerframe, font='arial 12', height=10,  bg="gray60", wrap=WORD, state='disabled')
    self.grpnotetxtbx.pack(side="bottom", expand='True', fill='x', padx=(20,20))
    
    # Treeview to show group (id, name, ip, filename)
    self.tftpgrptbl = ttk.Treeview(self.centerframe, selectmode='none', height=10, style="db.Treeview") #height=19, 
    self.tftpgrptbl.pack(side="left", expand='True', fill='both', padx=(20,0))  #fill='x', expand=True, anchor='n', side='left'
    # Adding a vertical scrollbar to Treeview widget
    self.tftpgrptblscroll = ttk.Scrollbar(self.centerframe, orient ="vertical", command=self.tftpgrptbl.yview)
    self.tftpgrptbl.configure(yscrollcommand=self.tftpgrptblscroll.set)
    self.tftpgrptblscroll.pack(side='right', expand='False', fill='y', anchor=E, padx=(0,20))
    # Treeview config
    self.tftpgrptbl["columns"] = ("1", "2", "3", "4")
    self.tftpgrptbl['show'] = 'headings'
    self.tftpgrptbl.column("1", width=50, anchor='center')
    self.tftpgrptbl.column("2", width=100, anchor='center')
    self.tftpgrptbl.column("3", width=100, anchor='center')
    self.tftpgrptbl.column("4", width=400, anchor='e')
    self.tftpgrptbl.heading("1", text="id")
    self.tftpgrptbl.heading("2", text="hostname")
    self.tftpgrptbl.heading("3", text="ip")
    self.tftpgrptbl.heading("4", text="File")

    # Bottom Frame
    self.bottomframe1 = ctk.CTkFrame(master=self.tftpuploadgroupw, fg_color="powder blue") # OUTPUT DATA AREA
    self.bottomframe1.pack(fill='x')
    #self.bottomframe1.pack_propagate(False)

    self.separator2 = ttk.Separator(master=self.bottomframe1, orient='horizontal')
    self.separator2.pack(padx=20, pady=(4,5), fill='x', expand=True, side='top')

    self.checkboxcopygrp = ctk.CTkCheckBox(self.bottomframe1, state='disabled', command=lambda:checkboxcopygrp_event(self), variable=self.checkboxcopygrp_var, text="Copy(merge) config", onvalue="on", offvalue="off", fg_color="gray", hover_color="dark slate gray", border_color="gray", border_width=2, text_color_disabled="gray")
    self.checkboxcopygrp.pack(side='left', anchor='n', pady=(10,10), padx=(60,20))
    self.checkboxreplgrp = ctk.CTkCheckBox(self.bottomframe1, state='disabled', command=lambda:checkboxreplgrp_event(self), variable=self.checkboxreplgrp_var, text="Replace running-config", onvalue="on", offvalue="off", fg_color="gray", hover_color="dark slate gray", border_color="gray", border_width=2, text_color_disabled="gray")
    self.checkboxreplgrp.pack(side='left', anchor='n', pady=(10,10), padx=(20,20))
    self.separator3a = ttk.Separator(master=self.bottomframe1, orient='vertical')
    self.separator3a.pack(fill='y', expand=False, side='left', padx=20)
    self.checkboxcrsgrp = ctk.CTkCheckBox(self.bottomframe1, state='disabled',command=lambda:checkboxcrsgrp_event(self), variable=self.checkboxcrsgrp_var, text="copy runnning > startup", onvalue="on", offvalue="off", fg_color="gray", hover_color="dark slate gray", border_color="gray", border_width=2, text_color_disabled="gray")
    self.checkboxcrsgrp.pack(side='left', anchor='n', pady=(10,10), padx=(40,20))
    
    self.bottomframe2 = ctk.CTkFrame(master=self.tftpuploadgroupw, fg_color="powder blue") # OUTPUT DATA AREA
    self.bottomframe2.pack(fill='x', ipadx=10)
    #self.bottomframe2.pack_propagate(False)
    self.chkbxrunningcfgrp = ctk.CTkCheckBox(self.bottomframe2, state='disabled', command=lambda:chkbxrunningcfgrp_event(self), variable=self.chkbxrunningcfgrp_var, text="running-config", onvalue="on", offvalue="off", fg_color="gray", hover_color="dark slate gray", border_color="gray", border_width=2, text_color_disabled="gray")
    self.chkbxrunningcfgrp.pack(side='left', anchor='n', pady=(10,10), padx=(60,20))
    self.chkbxstartupcfgrp = ctk.CTkCheckBox(self.bottomframe2, state='disabled',command=lambda:chkbxstartupcfgrp_event(self), variable=self.chkbxstartupcfgrp_var, text="startup-config", onvalue="on", offvalue="off", fg_color="gray", hover_color="dark slate gray", border_color="gray", border_width=2, text_color_disabled="gray")
    self.chkbxstartupcfgrp.pack(side='left', anchor='n', pady=(10,10), padx=(50,70))
    self.separator3b = ttk.Separator(master=self.bottomframe2, orient='vertical')
    self.separator3b.pack(fill='y', expand=False, side='left', padx=20, pady=(0,1))
    self.checkboxcstrngrp = ctk.CTkCheckBox(self.bottomframe2, state='disabled', command=lambda:checkboxcstrngrp_event(self), variable=self.checkboxcstrngrp_var, text="copy startup > runnning", onvalue="on", offvalue="off", fg_color="green4", hover_color="dark slate gray", border_color="gray", border_width=2, text_color_disabled="gray")
    self.checkboxcstrngrp.pack(side='left', anchor='n', pady=(10,10), padx=(40,20))
    
    self.bottomframe3 = ctk.CTkFrame(master=self.tftpuploadgroupw, fg_color="powder blue") # OUTPUT DATA AREA
    self.bottomframe3.pack(fill='x', ipadx=50, pady=1)
    self.separator4 = ttk.Separator(master=self.bottomframe3, orient='horizontal')
    self.separator4.pack(padx=20, pady=(5,5), fill='x', expand=True, side='top')
    self.tftpgrpgo = ctk.CTkButton(self.bottomframe3, state='disabled', text="GoGroup", width=150, fg_color="gray", hover_color='green4', command=lambda:tftpgrpgobtn(self))
    self.tftpgrpgo.pack(padx=(30,30), pady=(10,5), side='left')
    self.tftpstatuslbl = Label(self.bottomframe3, text="Select a Group ", font=('arial', 14, 'bold'), bg="powder blue", fg='OrangeRed2')
    self.tftpstatuslbl.pack(padx=(30,30), pady=(10,5), side='left')
    self.tftpgrpexit = ctk.CTkButton(self.bottomframe3, text="Exit", width=150, fg_color="red3", hover_color='red4', command=self.tftpuploadgroupw.destroy, font=('arial', 12, 'bold'), border_width=2, border_color='red4')
    self.tftpgrpexit.pack(padx=(30,30), pady=(10,5), side='right')
    
    self.bottomframe4 = ctk.CTkFrame(master=self.tftpuploadgroupw, fg_color="powder blue") # OUTPUT DATA AREA
    self.bottomframe4.pack(fill='x', pady=1)
    self.progstatuslbl = Label(self.bottomframe4, text="id:", font=('arial', 14, 'bold'), bg="powder blue", fg='OrangeRed2')
    self.progstatuslbl.pack(padx=(40,30), pady=(5,15), side='left')
    self.progstatus1 = ctk.CTkProgressBar(self.bottomframe4, progress_color='green4', border_width=1, border_color='dark slate gray', width=500)
    self.progstatus1.pack(padx=(40,30), pady=(5,15), side='right')
    self.progstatus1.set(0)

    # Setup the default values for the checkboxes
    self.checkboxcopygrp.select()
    self.chkbxrunningcfgrp.select()
    
    populatemembxg(self)
    