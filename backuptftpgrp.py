from netmiko import ConnectHandler 
from netmiko.ssh_exception import NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import SSHException
# from netmiko.exceptions import NetMikoAuthenticationException
# from netmiko.exceptions import NetMikoTimeoutException
# from netmiko.exceptions import SSHException
import time
import os
import shutil
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import showinfo
from tkinter import scrolledtext
import customtkinter as ctk
import os
from settings import *
import json
from connecttodb import getdevicefromid
from PIL import ImageTk, Image

# This is being used
def grpselectiongettftp(self, groupselection):
    # Group selection get values
    print("Groupselection (backuptftpGRP/grpselectionget()) get values")
    # What directory am I in
    print(f"1) The current working directory is (backuptftpGRP.py): {os.getcwd()}")

    # Change the directory to 'London routers' = 'devicegroups'
    os.chdir(devicegroups)
    groupdevicepath = os.path.join(devicegroups, groupselection)
    os.chdir(groupdevicepath)
    print(f"1a) The current working directory is (backuptftpGRP.py): {os.getcwd()}")
    # Get the json file
    filepath = os.path.join(groupselection + ".json")
    print(f"1b) (backuptftpGRP.py) filepath = {filepath}")
    filetoread = open(filepath)
    inputjsondata = json.load(filetoread)
    print(f"1c) Data in members: {inputjsondata['members']}")
    return inputjsondata['members']
    # Extract the data from the json file

# this is not being used
# !!!! delete this function
'''
def tftpsaveconfiggrp(self, groupselection):
    print(f"1a) This is tftpsaveconfiggrp (groupselection): {groupselection}")
    grpmemberreturntftpgrp = grpselectiongettftp(self, groupselection)
    print(f"3) These are the grp members this is tftpsaveconfiggrp (grpmemberreturn): {grpmemberreturntftpgrp}")
    print(f"4) This is tftpsaveconfiggrp (groupselection): {groupselection}")
    grpmemberreturn = grpselectiongettftp(self, groupselection)

    # Provide a id and get back everything
    for i in grpmemberreturn:
        retid=0
        retname=""
        retip=""
        retusername=""
        retpassword=""
        retdescription=""
        rettype=""
        retgolden=""
        
        print(i)
        getdevicefromid(i)
        
        try:
            retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getdevicefromid(i)
        except TypeError:
                print(f"Printing load device grpselectiongettftp 'Try block is error exception' ")
        
        print(f"retid: {retid}")
        print(f"retname: {retname}")
        print(f"retip: {retip}")
        print(f"retusername: {retusername}")
        print(f"retpassword: {retpassword}")
        print(f"retdescription: {retdescription}")
        print(f"retdescription: {rettype}")
        print(f"retdescription: {retgolden}")

        # Now start the TFTP process
        #TFTP_SERVER = tftpserver
        hostname = ""
        filename = ""
        filedatetime = str(time.strftime("%Y-%m-%d-%H-%M-%S"))
        #directorylocation = "/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/"
        #filesource = '/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/'
        #filedestination = f'/Shared/NetDevApp3/cisco12ct/devicedata/{hostname}/'
        #changetoDEVICEDATAdirectory = '/Shared/NetDevApp3/cisco12ct'

        device = {
             'device_type': f'{rettype}',
             'host': f'{retip}',
             'username': f'{retusername}',
             'password': f'{retpassword}',
             'secret': f'{retpassword}'
             }
        print("--------------")
        print(device['host'])
        print("--------------")
        try:
            name = f"device{str(1)}"
            net_connect = ConnectHandler(**device)
            print("Try 0a")
            net_connect.enable()
            print(net_connect.find_prompt()[:-1])
            hostname = net_connect.find_prompt()[:-1]
            copy_command = f"copy {self.startuporrunning_var.get()} tftp://{tftpserver} {directorylocation}"
            output = net_connect.send_command_timing(copy_command)
            print("Try 1")
            if "Address or name" in output:
                output += net_connect.send_command_timing("\n")
                print("Try 2")
            if "Destination filename" in output:
                # output += net_connect.send_command_timing(f"{hostname}"+"_"+f"{device['host']}_"+"RunningConfig2"+"\n")
                output += net_connect.send_command_timing(f"{directorylocation}"+"/"+f"{hostname}_"+f"{filedatetime}_"+"RunningConfig"+"\n")
                print("Try 3")
                net_connect.disconnect
        
        except:
            print("An netmiko function exception occurred in tftpconfig(backuptftp.py)")
            
        finally:
            try:
                print(output)
            except:
                print("Could not print the output of the netmiko function tftpconfig(backuptftp.py)")
        
        print("Running the second try method")
        print(f"Directory = {directorylocation}")
        print(os.listdir(directorylocation))
        # print("ScanDir = "+ os.scandir(directorylocation))
        print(f"hostname={hostname}")
        print(f"device ip={device['host']}")
        print(f"{retname}")
        print("CURRENT DIRECTORY="+f"{os.getcwd()}")
        os.chdir(changetoDEVICEDATAdirectory)
        print("CURRENT DIRECTORY2="+f"{os.getcwd()}")

        if hostname == retname:
            print("Both names match !")
            try:
                for file_name in os.listdir(filesource):
                    source=filesource+file_name
                    destination=filedestination+"/"+hostname+"/"+file_name
                    if os.path.isfile(source):
                        shutil.copy(source, destination)
            except OSError as error:
                print("Problem copying files to location = " + f"{error}")
            finally:
                if len(os.listdir(filesource)) > 0:
                    print("FOLDER IS GREATER THAN O")
# shutil.rmtree(filesource)
                for f in os.listdir(filesource):
                    os.remove(os.path.join(filesource, f))
                else:
                    print("FOLDER IS NOT GREATER THAN O")
        else:
            print("Both names DONOT match !")
'''



def backupgrouptftp(self):
    print("(backuptfptgrp.py) backupgrouptftp")

    # GROUP COMBOBOX SELECTION DROPDOWN
    self.tftpgrpcombxstrgrp = []
    self.tftpgrpcombxstrgrp_var = ctk.StringVar(self)


    # The group is selected and the function gets a list of mebers id from the json file
    self.membersofselecgrp = []

    # Create a variable that will hold [id, hostname, ipaddress, username, password, type]
    self.selectedgrpbucket_var = []
    self.selectedgrpbucket_var_ids = []

    # Checkbox selection changes value 'startup-config' or 'running-config'
    self.startuporrunning_var = ctk.StringVar(self)

    # Switch on group selection combobox to on / off
    self.grpnameswitch_var = ctk.StringVar(self)

    # Switch on file identifier combobox on / off
    self.fileidswitch_var = ctk.StringVar(self)

    items = os.listdir(devicegroups)
    self.groupcomboboxoptions = []
    for item in items:
        if os.path.isdir(item):
            self.tftpgrpcombxstrgrp.append(item)
    
    def tftpgrpcombxstrgrp_callback(self):
        self.backuptftpgrptbl.delete(*self.backuptftpgrptbl.get_children())
        print(f"command=self.tftpgrpcombxstrgrp_callback: {self.grpnamecbx.get()}")
        self.tftpgrpcombxstrgrp_var.set(self.grpnamecbx.get())
        print(f"self.tftpgrpcombxstrgrp_var: {self.tftpgrpcombxstrgrp_var.get()}")

        # Get the details of the group
        self.membersofselecgrp = grpselectiongettftp(self, self.tftpgrpcombxstrgrp_var.get())
        print(f"members of the group is : {self.membersofselecgrp}")

        count = 0

        # provide members id to get the details of the members
        for i in self.membersofselecgrp:
            count += 1
            print(f"Getting group member with id: {i}")
            retid=0
            retname=""
            retip=""
            retusername=""
            retpassword=""
            retdescription=""
            rettype=""
            retgolden=""

            retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getdevicefromid(i)
            print(f"retid: {retid}")
            print(f"retname: {retname}")
            print(f"retip: {retip}")
            print(f"retusername: {retusername}")
            print(f"retpassword: {retpassword}")
            print(f"retdescription: {retdescription}")
            print(f"retdescription: {rettype}")
            print(f"retdescription: {retgolden}")

            # Insert data into the treeview
            # Restricted description to 10 string characters (retdescription[:10])
            self.backuptftpgrptbl.insert(parent='', index='end', iid=count, text=count, values=(f'{retid}',f'{retname}',f'{retip}',f'{rettype}',f'{retdescription[:10]}'))
            #self.tftpbackupwindowgrp.geometry('680x820')

            # Enable services
            self.grpnameswitch.configure(state='normal', fg_color='yellow2', button_color='dark slate gray', border_color='dark slate gray', progress_color='pale green', text_color='black')

            # Status label update here
            self.editgrpstatuslbl.configure(text='Confirm selection')
        
    def grpnameswitch_event():
        print(f"grpnamebtn_event set button value = {self.grpnameswitch.get()}")
        print(f"grpnameswitch_var set button value = {self.grpnameswitch_var.get()}")

        # Switch = Locked
        if self.grpnameswitch_var.get() == 'on':
            print(f"grpnameswitch_var set button value 'on' = {self.grpnameswitch_var.get()}")
            
            # Disable groupselect combobox
            self.grpnamecbx.configure(state='disabled', fg_color="gray80", button_color='gray', border_color='gray')
            self.grpnamelbl.configure(state='disabled')
            self.backuptftpgrptbl.configure(style="dbgray.Treeview")

            # Enable check boxes & file identifier
            self.bktypelbl.configure(state='normal')
            self.chkbxrunningcfg.configure(state='normal', fg_color="green", hover_color="dark slate gray", border_color="dark slate gray", text_color_disabled="dark slate gray")
            self.chkbxstartupcfg.configure(state='normal', fg_color="green", hover_color="dark slate gray", border_color="dark slate gray", text_color_disabled="dark slate gray")
            self.fileidlbl.configure(state='normal')
            self.fileidselec.configure(state='normal', fg_color="yellow2", font=('arial', 14, 'bold'), border_color='dark slate gray', button_color='dark slate gray', dropdown_fg_color='khaki', border_width=2, dropdown_hover_color='khaki3', dropdown_font=('arial', 14, 'bold'))
            self.fileidswitch.configure(state='normal', fg_color="yellow2", button_color='dark slate gray', border_color='dark slate gray')


        # Switch = unlocked
        if self.grpnameswitch_var.get() == 'off':
            print(f"grpnameswitch_var set button value 'off' = {self.grpnameswitch_var.get()}")

            # Enable groupselect combobox
            self.grpnamecbx.configure(state='normal', fg_color="yellow2", button_color='dark slate gray', border_color='dark slate gray')
            self.grpnamelbl.configure(state='normal')
            self.backuptftpgrptbl.configure(style="db.Treeview")

            # Disable check boxes & file identifier
            self.bktypelbl.configure(state='disabled')
            self.chkbxrunningcfg.configure(state='disabled', fg_color="gray", hover_color="gray", border_color="gray", text_color_disabled="gray")
            self.chkbxstartupcfg.configure(state='disabled', fg_color="gray", hover_color="gray", border_color="gray", text_color_disabled="gray")
            self.fileidlbl.configure(state='disabled')
            self.fileidselec.configure(state='disabled', fg_color="gray80", button_color='gray', border_color='gray')
            self.fileidswitch.configure(state='disabled', fg_color='gray50', button_color='gray30', border_color='gray30', progress_color='gray30', text_color='gray20')

        count = 0
        # provide members id to get the details of the members
        for i in self.membersofselecgrp:
            count += 1
            print(f"Getting group member with id: {i}")
            retid=0
            retname=""
            retip=""
            retusername=""
            retpassword=""
            retdescription=""
            rettype=""
            retgolden=""

            retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getdevicefromid(i)
            print(f"retid: {retid}")
            print(f"retname: {retname}")
            print(f"retip: {retip}")
            print(f"retusername: {retusername}")
            print(f"retpassword: {retpassword}")
            print(f"retdescription: {retdescription}")
            print(f"retdescription: {rettype}")
            print(f"retdescription: {retgolden}")

            self.selectedgrpbucket_var.append([retid, retname, retip, retusername, retpassword, rettype])
            self.selectedgrpbucket_var_ids.append(retid)

            print(self.selectedgrpbucket_var)
            print(self.selectedgrpbucket_var_ids)
            #print (strip('[').strip(']')(str(self.selectedgrpbucket_var_ids)))
            #self.outputxtbx.insert(INSERT, f"Bucket= {self.selectedgrpbucket_var}")

        # Disable groupselect combobox
        # self.grpnamecbx.configure(state='disabled')
        # Status label update here
        self.editgrpstatuslbl.configure(text=f'{self.tftpgrpcombxstrgrp_var.get()} selected')



    def btnbackup_event():
        print("btnbackup_event")
        print(self.selectedgrpbucket_var)
        self.outputxtbx.configure(state='normal')
        self.btnbackup.configure(state='disabled', fg_color='gray', border_color='gray40')
        self.fileidswitch.configure(state='disabled', fg_color='gray50', button_color='gray30', border_color='gray30', progress_color='gray', text_color='gray20')

        print(f"self.startuporrunning_var = {self.startuporrunning_var.get()}")

        count = 0
        self.update_idletasks()

        for i in self.selectedgrpbucket_var:
            bucketid = 0
            buckethostname = ""
            bucketip = ""
            bucketusername = ""
            bucketpassword = ""
            buckettype = ""

            bucketid = self.selectedgrpbucket_var[count][0]
            buckethostname = self.selectedgrpbucket_var[count][1]
            bucketip = self.selectedgrpbucket_var[count][2]
            bucketusername = self.selectedgrpbucket_var[count][3]
            bucketpassword = self.selectedgrpbucket_var[count][4]
            buckettype = self.selectedgrpbucket_var[count][5]

            print(f"id: {bucketid} hostname: {buckethostname} ip: {bucketip} username: {bucketusername} password: {bucketpassword} type: {buckettype}")
            count += 1

            device = {
                'device_type': f'{buckettype}',
                'host': f'{bucketip}',
                'username': f'{bucketusername}',
                'password': f'{bucketpassword}',
                'secret': f'{bucketpassword}'
                }
            
            print("--------------")
            print(device['host'])
            print("--------------")

            # Now start the TFTP process
            #TFTP_SERVER = tftpserver
            hostname = ""
            filename = ""
            filedatetime = str(time.strftime("%Y-%m-%d-%H-%M-%S"))
            #directorylocation = "/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/"
            #filesource = '/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/'
            #filedestination = f'/Shared/NetDevApp3/cisco12ct/devicedata/{hostname}/'
            #changetoDEVICEDATAdirectory = '/Shared/NetDevApp3/cisco12ct'

            self.outputxtbx.insert(INSERT, f"Starting ***--- {buckethostname} ({bucketip}) ---*** \n")
            copy_command = (f"copy {self.startuporrunning_var.get()} tftp://{tftpserver} {directorylocation}")
            print(copy_command)

            try:
                net_connect = ConnectHandler(**device)
                print("Try Block: position 1")
                net_connect.enable()
                print(net_connect.find_prompt()[:-1])
                hostname = net_connect.find_prompt()[:-1]
                copy_command = (f"copy {self.startuporrunning_var.get()} tftp://{tftpserver}{directorylocation}")
                self.outputxtbx.insert(INSERT, f"Command:\n{copy_command}")
                output = net_connect.send_command_timing(copy_command)
                print("Try Block: position 2")
                if "Address or name" in output:
                    output += net_connect.send_command_timing("\n")
                    print("Try Block (IF): position 3a")
                if "Destination filename" in output:
                    # output += net_connect.send_command_timing(f"{hostname}"+"_"+f"{device['host']}_"+"RunningConfig2"+"\n")
                    output += net_connect.send_command_timing(f"{directorylocation}"+"/"+f"{hostname}_"+f"{filedatetime}_"+f"{self.startuporrunning_var.get()}_"+f"{self.fileidselec.get()}"+"\n")
                    print(f"OUTPUT=:{output}")
                    print("Try Block (IF): position 3b")
                    net_connect.disconnect
            except NetMikoAuthenticationException as AuthException:
                print("326 Authentication Error %s" % AuthException)
                self.outputxtbx.insert(INSERT, f"***--- {buckethostname} ({bucketip}) ---*** \n Authentication Error \n {AuthException}")
                continue
            except NetMikoTimeoutException as TimeoutException:
                #raise ConnectError(TimeoutException.args[0])
                print("331 No Valid Connections Error SSH connection 'USERNAME ?': %s" % TimeoutException)
                self.outputxtbx.insert(INSERT, f"Timeout Exception Error ***--- {buckethostname} ({bucketip}) ---*** \n {TimeoutException}")
                continue
            except SSHException as sshexception:
                print("An netmiko sshexception Error %s" % sshexception)
                self.outputxtbx.insert(INSERT, f"SSHException Error ***--- {buckethostname} ({bucketip}) ---*** \n {sshexception}")
                continue
            except Exception as unknown_error:
                print("339 An netmiko Unknown Error %s"+ str(unknown_error))
                self.outputxtbx.insert(INSERT, f"Unknown Error ***--- {buckethostname} ({bucketip}) ---*** \n  \n {unknown_error}")
                continue
            finally:
                if net_connect == True: net_connect.disconnect
                self.update_idletasks()
                self.outputxtbx.insert(INSERT, f"\nMoving file from temporary location.\n")
                self.outputxtbx.see('end')

            print("Running the second try method")
            print(f"Directory = {directorylocation}")
            print(os.listdir(directorylocation))
            # print("ScanDir = "+ os.scandir(directorylocation))
            print(f"hostname={hostname}")
            print(f"device ip={device['host']}")
            print(f"{buckethostname}")
            print("CURRENT DIRECTORY="+f"{os.getcwd()}")
            os.chdir(changetoDEVICEDATAdirectory)
            print("CURRENT DIRECTORY2="+f"{os.getcwd()}")

            if hostname == buckethostname:
                print("Both names match !")
                try:
                    for file_name in os.listdir(filesource):
                        source=filesource+file_name
                        destination=filedestination+"/"+hostname+"/"+file_name
                        self.outputxtbx.insert(INSERT, f"Filename:\n{file_name}\n")
                        if os.path.isfile(source):
                            shutil.copy(source, destination)
                            self.outputxtbx.insert(INSERT, f"Location:\n{filedestination}{hostname}\n")
                except OSError as error:
                    print("Problem copying files to location = " + f"{error}")
                    print("source = " + f"{source}")
                    print("filesource = " + f"{filesource}")
                    print("file_name = " + f"{file_name}")
                    print("destination = " + f"{destination}")
                    print("filedestination = " + f"{filedestination}")
                    print("hostname = " + f"{hostname}")
                finally:
                    self.outputxtbx.insert(INSERT, f"\n---*---*---*---*---*---*---*---*---*---*---*---*---*--- \n")
                    if len(os.listdir(filesource)) > 0:
                        print("FOLDER IS GREATER THAN O")
                        # shutil.rmtree(filesource)
                        for f in os.listdir(filesource):
                            os.remove(os.path.join(filesource, f))
                    else:
                        print("FOLDER IS NOT GREATER THAN 0")
            else:
                print("Both names DONOT match !")
        
        # close out the Lookup
        self.outputxtbx.configure(state='disabled')
        self.editgrpstatuslbl.configure(text='Task complete')


                

    # running-config checkbox
    def chkbxrunningcfg_event(self):
        print("chkbxrunningcfg running-config checkbox")
        self.startuporrunning_var.set("running-config")
        print(f"{self.startuporrunning_var.get()}")
        self.chkbxstartupcfg.deselect()
    
    # startup-config checkbox
    def chkbxstartupcfg_event(self):
        print("chkbxstartupcfg startup-config checkbox")
        self.startuporrunning_var.set("startup-config")
        print(f"{self.startuporrunning_var.get()}")
        self.chkbxrunningcfg.deselect()
    
    def fileidselec_callback(self):
        print("fileidselec_callback")
        self.editgrpstatuslbl.configure(text=f'Confirm "{self.fileidselec.get()}" selection')
        self.fileidselec.configure(width=220)

    def fileidswitch(self):
        print(f"fileidswitch value = {self.fileidswitch_var.get()}")
        self.fileidselec.configure(width=220)

        # Switch locked
        if self.fileidswitch_var.get() == 'on':
            print("The switch is locked")

            if self.fileidselec.get() == "Select" :
                print("Please select a valid File Identifier")
                messagebox.showinfo(parent=self.tftpbackupwindowgrp, title='Selection invalid', message='Please select a valid file identifier.')
                self.fileidswitch.deselect()
            
                
            else:
                # Disable Group selection switch
                # self.grpnameswitch.configure(state='normal')
                self.grpnameswitch.configure(state='disabled', progress_color='gray', fg_color='gray50', button_color='gray30', border_color='gray30')
                self.bktypelbl.configure(state='disabled')
                self.chkbxrunningcfg.configure(state='disabled', fg_color="gray", border_color="gray", text_color_disabled="gray")
                self.chkbxstartupcfg.configure(state='disabled', fg_color="gray", border_color="gray", text_color_disabled="gray")
                self.fileidlbl.configure(fg='gray')
                self.fileidselec.configure(state='disabled', fg_color="gray80", button_color='gray', border_color='gray')
                self.fileidswitch.configure(fg_color='yellow2')
                # not
                # self.fileidselec.configure(state='normal', fg_color="yellow2", font=('arial', 14, 'bold'), border_color='dark slate gray', button_color='dark slate gray', dropdown_fg_color='khaki', border_width=2, dropdown_hover_color='khaki3', dropdown_font=('arial', 14, 'bold'))

                print("You are good to activate the output and upload button.")

                # Activate the output textscroll
                self.outputxtbx.configure(state='normal', bg="light yellow")
                self.outputxtbx.insert(INSERT, f"Group: {self.tftpgrpcombxstrgrp_var.get()}\n")
                self.outputxtbx.insert(INSERT, f"Member ID's: {str(self.selectedgrpbucket_var_ids)[1:-1]}\n")
                self.outputxtbx.insert(INSERT, f"Backing up the: {self.startuporrunning_var.get()}\n")
                self.outputxtbx.insert(INSERT, f"File identified as: '{self.fileidselec.get()}'\n")
                self.outputxtbx.configure(state='disabled')


                # Activate the Backup process button
                self.btnbackup.configure(state='normal', fg_color='green', border_color='green4')

                self.editgrpstatuslbl.configure(text='Ready to run backup request')

                
            
        else:
            print("The switch is off")
            # Remove any text from output box
            self.outputxtbx.configure(state='normal', bg="light yellow")
            self.outputxtbx.delete('1.0', END)
            self.outputxtbx.configure(bg="gray64", state='disabled')
            self.btnbackup.configure(state='disabled', fg_color='gray', border_color='gray40')


        # Switch unlocked
        if self.fileidswitch_var.get() == 'off':
            print("The switch is NOT locked")
            self.grpnameswitch.configure(state='normal', progress_color='pale green', fg_color='yellow2', button_color='dark slate gray', border_color='dark slate gray')
            self.bktypelbl.configure(state='normal', fg='black')
            self.chkbxrunningcfg.configure(state='normal', fg_color="green", hover_color="dark slate gray", border_color="dark slate gray", text_color_disabled="dark slate gray")
            self.chkbxstartupcfg.configure(state='normal', fg_color="green", hover_color="dark slate gray", border_color="dark slate gray", text_color_disabled="dark slate gray")
            self.fileidlbl.configure(state='normal', fg='black')
            self.fileidselec.configure(state='normal', fg_color="yellow2", font=('arial', 14, 'bold'), border_color='dark slate gray', button_color='dark slate gray', dropdown_fg_color='khaki', border_width=2, dropdown_hover_color='khaki3', dropdown_font=('arial', 14, 'bold'))
            self.editgrpstatuslbl.configure(text='Unlocked for change')




    # create a window here
    self.tftpbackupwindowgrp = tk.Toplevel(master=self)
    self.tftpbackupwindowgrp.title("Backup group TFTP")
    self.tftpbackupwindowgrp.geometry('781x830+200+200')
    self.tftpbackupwindowgrp.minsize(500,800)
    self.tftpbackupwindowgrp.maxsize(900,850)
    self.tftpbackupwindowgrp.configure(background='powder blue')
    self.tftpbackupwindowgrp.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))

    # Disable root window when this one is active
    self.tftpbackupwindowgrp.attributes('-topmost', 'true')
    self.tftpbackupwindowgrp.transient(self)
    self.tftpbackupwindowgrp.update_idletasks()
    self.tftpbackupwindowgrp.grab_set()

    self.tftpbackupwindowgrp.grid_columnconfigure(0, weight=1)
    self.tftpbackupwindowgrp.grid_columnconfigure(1, weight=1)
    self.tftpbackupwindowgrp.grid_columnconfigure(2, weight=1)

    # top title
    self.createlabel = ctk.CTkLabel(self.tftpbackupwindowgrp, text="Backup a Group configuration (TFTP)", font=('arial', 22, 'bold'))
    self.createlabel.grid(row=0, column=0,sticky=EW, columnspan=3, pady=(20,16))
    self.separator1 = ttk.Separator(self.tftpbackupwindowgrp, orient='horizontal')
    self.separator1.grid(row=1, sticky=EW, columnspan=3, padx=(40,10), pady=10)

    # Group Selection ()
    self.grpnamelbl = Label(self.tftpbackupwindowgrp, text="Group selection", font=('arial', 14, 'bold'), bg="powder blue", fg='black')
    self.grpnamelbl.grid(row=2, column=0, sticky=W, padx=(25,10), pady=10)
    self.grpnamecbx = ctk.CTkComboBox(self.tftpbackupwindowgrp, width=220, fg_color="yellow2", font=('arial', 14, 'bold'), border_color='dark slate gray', button_color='dark slate gray', dropdown_fg_color='khaki', border_width=2, dropdown_hover_color='khaki3', dropdown_font=('arial', 14, 'bold'), variable=self.tftpgrpcombxstrgrp_var, values=self.tftpgrpcombxstrgrp, command=lambda v:tftpgrpcombxstrgrp_callback(self))
    self.grpnamecbx.grid(row=2, column=1, sticky='w', padx=(20,5), pady=10)
    self.grpnamecbx.set("select a group")
    self.grpnameswitch = ctk.CTkSwitch(self.tftpbackupwindowgrp, text="Unlock | Lock", command=grpnameswitch_event, variable=self.grpnameswitch_var, 
                                             onvalue="on", offvalue="off", switch_width=40, switch_height=20, fg_color='gray50', 
                                             button_color='gray30', border_width=2, border_color='gray30', progress_color='pale green', text_color='gray20')
    self.grpnameswitch.grid(row=2, column=2)
    self.grpnameswitch.configure(state='disabled')

    
    #self.grpnamebtn = ctk.CTkButton(self.tftpbackupwindowgrp, text="Set", width=120, fg_color='green4', hover_color='green', font=('arial', 12, 'bold'), border_width=2, border_color='dark green', command=grpnamebtn_event)
    #self.grpnamebtn.grid(row=2, column=2, padx=(15,0), pady=10)

    # Treeview to show group (id, name, ip, filename)
    self.backuptftpgrptbl = ttk.Treeview(self.tftpbackupwindowgrp, selectmode='none', height=10, style="db.Treeview") #height=19, 
    self.backuptftpgrptbl.grid(row=3, column=0, sticky=EW, padx=(25,0), pady=10, columnspan=3)  #, expand=True, anchor='n', side='left'
    # Adding a vertical scrollbar to Treeview widget
    self.bktftpgrptblscroll = ttk.Scrollbar(self.tftpbackupwindowgrp, orient=tk.VERTICAL, command=self.backuptftpgrptbl.yview)
    self.backuptftpgrptbl.configure(yscrollcommand=self.bktftpgrptblscroll.set)
    self.bktftpgrptblscroll.grid(row=3, column=3, sticky='nes', padx=(0,30), pady=10)
    
    
    # Treeview config
    self.backuptftpgrptbl["columns"] = ("1", "2", "3", "4", "5")
    self.backuptftpgrptbl['show'] = 'headings'
    self.backuptftpgrptbl.column("1", width=50, anchor='center')
    self.backuptftpgrptbl.column("2", width=100, anchor='center')
    self.backuptftpgrptbl.column("3", width=100, anchor='center')
    self.backuptftpgrptbl.column("4", width=100, anchor='center')
    self.backuptftpgrptbl.column("5", width=200, anchor='center')
    self.backuptftpgrptbl.heading("1", text="id")
    self.backuptftpgrptbl.heading("2", text="hostname")
    self.backuptftpgrptbl.heading("3", text="ip")
    self.backuptftpgrptbl.heading("4", text="type")
    self.backuptftpgrptbl.heading("5", text="Description")

    # Reseting the geometry adjusts the treeview and scrollbar to fit
    self.tftpbackupwindowgrp.geometry('780x820')

    # Checkbox selection changes self.startuporrunning_var value
    self.bktypelbl = Label(self.tftpbackupwindowgrp, text="Backup Type", font=('arial', 14, 'bold'), bg='powder blue', fg='black', state='disabled')
    self.bktypelbl.grid(row=4, column=0,sticky=W, padx=(25,10), pady=10)
    self.chkbxrunningcfg = ctk.CTkCheckBox(self.tftpbackupwindowgrp, text="running-config", onvalue="on", offvalue="off", fg_color="gray", hover_color="dark slate gray", border_color="gray", border_width=2, text_color_disabled="gray", command=lambda:chkbxrunningcfg_event(self))
    self.chkbxrunningcfg.grid(row=4, column=1, pady=(10,10), padx=(40,20))
    self.chkbxstartupcfg = ctk.CTkCheckBox(self.tftpbackupwindowgrp, text="startup-config", onvalue="on", offvalue="off", fg_color="gray", hover_color="dark slate gray", border_color="gray", border_width=2, text_color_disabled="gray", command=lambda:chkbxstartupcfg_event(self))
    self.chkbxstartupcfg.grid(row=4, column=2, pady=(10,10), padx=(40,20))
    self.chkbxrunningcfg.select()
    self.startuporrunning_var.set("running-config")
    self.chkbxrunningcfg.configure(state='disabled')
    self.chkbxstartupcfg.configure(state='disabled')

    # File idenfifier
    # # File idenfifier Daily Weekly monthly Goldern ?
    # File Identifier
    self.fileidlbl = Label(self.tftpbackupwindowgrp, state='disabled', text="File identifier", font=('arial', 14, 'bold'), bg='powder blue', fg='black')
    self.fileidlbl.grid(row=5, column=0,sticky=W, padx=(25,10), pady=10)
    self.fileidoptions = ['Daily','Weekly','Monthly','Golden','Silver']
    self.fileidselec = ctk.CTkComboBox(self.tftpbackupwindowgrp, state='normal', font=('arial', 14, 'bold'), values=self.fileidoptions, dropdown_font=('arial', 16, 'bold'), command=lambda v:fileidselec_callback(self), width=220)
    self.fileidselec.grid(row=5, column=1,sticky=W, padx=(15,10), pady=10)
    self.fileidselec.set("Select")
    self.fileidselec.configure(state='disabled')
    self.fileidswitch = ctk.CTkSwitch(self.tftpbackupwindowgrp, text="Unlock | Lock", state='disabled', command=lambda:fileidswitch(self), variable=self.fileidswitch_var, onvalue="on", offvalue="off", switch_width=40, switch_height=20, fg_color='gray50', button_color='gray30', border_width=2, border_color='gray30', progress_color='pale green', text_color='gray20')
    self.fileidswitch.grid(row=5, column=2, padx=(15,25), pady=10)

    self.separator2 = ttk.Separator(self.tftpbackupwindowgrp, orient='horizontal')
    self.separator2.grid(row=6, sticky=EW, columnspan=3, padx=(40,0), pady=10)

    self.outputxtbx = scrolledtext.ScrolledText(self.tftpbackupwindowgrp, font='arial 12', height = 10, width = 25, bg="gray64", wrap=WORD, state='disabled') #bg="light goldenrod yellow"
    self.outputxtbx.grid(row=7, column=0, sticky=EW, padx=(25,0), pady=10, columnspan=3)

    self.progstatus = ctk.CTkProgressBar(self.tftpbackupwindowgrp, progress_color='green4', border_width=1, border_color='dark slate gray')
    self.progstatus.grid(row=8, column=0, sticky=EW, padx=(25,0), pady=5, columnspan=3)
    self.progstatus.set(0)

    self.btnbackup = ctk.CTkButton(self.tftpbackupwindowgrp, text="Backup", width=120, fg_color='gray', hover_color='green4', font=('arial', 12, 'bold'), border_width=2, border_color='gray40', command=btnbackup_event, state='disabled') 
    self.btnbackup.grid(row=9, column=0,  pady=5, padx=(25,1), sticky=W)
    self.editgrpstatuslbl = Label(self.tftpbackupwindowgrp, text="Select a Group", font=('arial', 14, 'bold'), bg="powder blue", fg='OrangeRed2')
    self.editgrpstatuslbl.grid(row=9, column=1, pady=5, sticky=W, padx=10) # padx=(0)
    self.btnexit = ctk.CTkButton(self.tftpbackupwindowgrp, text="EXIT", width=120, fg_color="red2", font=('arial', 12, 'bold'), command=self.tftpbackupwindowgrp.destroy, hover_color='red4', border_width=2, border_color='red4') # , command=onexitcleanup
    self.btnexit.grid(row=9, column=2, pady=5, padx=(0,0), sticky=E)






