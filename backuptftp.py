import sqlite3
from mysql.connector import Error
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkinter import *
from PIL import ImageTk, Image
from netmiko import ConnectHandler
import time
import os
import shutil
from settings import *
from connecttodb import getdevicefromid
import regex as re

def tftpbtngo(self, selectedid):
    
    # Disable the button from multiple presses
    # put a feeedback here
    self.btnbackup.configure(state='disabled', fg_color="gray", border_color='gray')
    # self.tftpbackupwindow, text="Backup", 
    self.progstatus.set(0.5)
    self.editgrpstatuslbl.configure(text=f"Starting process on id: {selectedid}")
    self.update_idletasks()

    # Disable Backup type field
    # self.bktpeselectlbl.configure(state='disabled')
    # self.bktpeselecchkbx.configure(fg_color="gray75", state='disabled', border_color='gray', button_color='gray')
    # self.bktpeselecbtn.configure(text='Accepted', fg_color="gray", state='disabled')
    # Disable File Identifier
    # self.fileidlbl.configure(state='disabled') # label
    # self.fileidselec.configure(fg_color="gray75", state='disabled', border_color='gray', button_color='gray')
    # self.fileidbtn.configure(text='Accepted', fg_color="gray", state='disabled')

    self.cgouttxtbx.configure(state='normal')
    # self.cgouttxtbx.insert(INSERT, f"id: {selectedid}\n")

    retid=0
    retname=""
    retip=""
    retusername=""
    retpassword=""
    retdescription=""
    rettype=""
    retgolden=""

    retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getdevicefromid(selectedid)
    
    print("1) This is tftpbtngo(backuptftp.py)")
    print(f"2) This is tftpbtngo (iam_selecteddevice): {str(selectedid)}")
    print(f"3) This is tftpbtngo (id): {str(retid)}")
    print(f"4) This is tftpbtngo (name): {retname}")
    print(f"5) This is tftpbtngo (ip): {retip}")
    print(f"6) This is tftpbtngo (username): {retusername}")
    print(f"7) This is tftpbtngo (password): {retpassword}")
    print(f"8) This is tftpbtngo (retdescription): {retdescription}")
    print(f"9) This is tftpbtngo (rettype): {rettype}")
    print(f"10) This is tftpbtngo (retgolden): {retgolden}")
    
    hostname = ""
    filename = ""
    filedatetime = str(time.strftime("%Y-%m-%d-%H-%M-%S"))
    hostname = retname
    # filedestination = f"C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\{hostname}\\" # windows
    # filedestination = f'/Shared/NetDevApp3/cisco12ct/devicedata/' # Linux
    
    # enter the IP for your TFTP server here
    TFTP_SERVER = tftpserver
    print(f"The TFTP_SERVER is: {TFTP_SERVER}")
    print(f"The directorylocation is: {directorylocation}")
    print(f"The filesource is: {filesource}")
    print(f"The filedestination is: {filedestination}")
    print(f"The changetoDEVICEDATAdirectory is: {changetoDEVICEDATAdirectory}")
    
    # cisco_ios
    # cisco_xe
    device = {
    'device_type': f'{rettype}',
    'host': f'{retip}',
    'username': f'{retusername}',
    'password': f'{retpassword}',
    'secret': f'{retpassword}'
    }
    print("--------------")
    print(device['host']) # ip address
    print(device['device_type']) # device type
    print(f"1) self.fileidselec.get(): {self.fileidselec.get()}") # Daily
    print(f"2) self.bktpeselecchkbx.get(): {self.bktpeselecchkbx.get()}") # Running-configuration
    print(f"3) self.fileidselec.get(): {self.fileidselec.get()}") # Daily
    print(f"4) self.tftpselectedid.get(): {self.tftpselectedid.get()}") # 2
    print(f"5) self.setbackuptypevar.get(): {self.setbackuptypevar.get()}") # Golden
    print(f"6) self.setfileidtypevar.get(): {self.setfileidtypevar.get()}")
    self.cgouttxtbx.insert(INSERT, f"1) connecting to device id:{selectedid}"+" "+f"{device['host']}"+"\n")
    print("--------------")

    # put a feeedback here
    self.progstatus.set(0.6)
    self.editgrpstatuslbl.configure(text=f"Backup process running")
    self.update_idletasks()

    try:
        name = f"device{str(1)}"
        net_connect = ConnectHandler(**device)
        print("Try 0a")
        net_connect.enable()
        print(net_connect.find_prompt()[:-1])
        hostname = net_connect.find_prompt()[:-1]
        #copy_command = f"copy running-config tftp://{tftpserver}{directorylocation}"
        copy_command = f"copy {self.setbackuptypevar.get()} tftp://{tftpserver}"
        output = net_connect.send_command_timing(copy_command)
        print(f"Try 1 hostname={hostname}")
        self.cgouttxtbx.insert(INSERT, f"2) connection hostname from device is :{hostname}"+"\n")
        
        # put a feeedback here
        self.progstatus.set(0.7)
        self.editgrpstatuslbl.configure(text=f"Hostname found: {hostname}")
        self.update_idletasks()
        
        
        if "Address or name" in output:
            output += net_connect.send_command_timing("\n")
            print("Try 2")
            self.cgouttxtbx.insert(INSERT, f"3) Accepting the tftp server ip address: {tftpserver}"+"\n")
        if "Destination filename" in output:
            ####### YOU WILL NEED TO HARDCODE THIS ? 
            ################################################################################
            print("backupftp.py tftpbtngo Line:112 Select Windows(111) or Linux(108)")
            #use this for Linux
            output += net_connect.send_command_timing(f"{directorylocation}"+"/"+f"{hostname}_"+f"{filedatetime}_"+f"{self.setbackuptypevar.get()}"+f"_{self.setfileidtypevar.get()}"+"\n")
            self.cgouttxtbx.insert(INSERT, f"4) The TFTP temporary save directory will be: {directorylocation}"+"\n")
            self.cgouttxtbx.insert(INSERT, f"5) The filename will be:\n{hostname}_"+f"{filedatetime}_"+f"{self.setbackuptypevar.get()}"+f"_{self.setfileidtypevar.get()}"+"\n")
            
            # Use this for windows
            # output += net_connect.send_command_timing(f"{hostname}_"+f"{filedatetime}_"+f"{self.setbackuptypevar.get()}"+f"_{self.setfileidtypevar.get()}"+"\n")
            # self.cgouttxtbx.insert(INSERT, f"3) The filename will be: {hostname}_"+f"{filedatetime}_"+f"{self.setbackuptypevar.get()}"+f"_{self.setfileidtypevar.get()}"+"\n")
            ##################################################################################
            
            net_connect.disconnect
            
    except:
        print("A netmiko function exception occurred in tftpconfig(backuptftp.py)")
        self.cgouttxtbx.insert(INSERT, f"6) A netmiko connection exception occurred: {device['host']}\n")
    
    finally:
        try:
            print(type(output))
            self.cgouttxtbx.insert(INSERT, f"6) File was sucessfully transfered: {output[output.rindex('!')+1:]}\n")
        except:
            print("Could not print the output of the netmiko function tftpconfig(backuptftp.py)")
            self.cgouttxtbx.insert(INSERT, f"6) Could not print the output")
    
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

    # self.cgouttxtbx.insert(INSERT, f"CURRENT DIRECTORY2: {os.getcwd()}")

    # self.cgouttxtbx.configure(state='disabled')


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
            print("source = " + f"{source}")
            print("filesource = " + f"{filesource}")
            print("file_name = " + f"{file_name}")
            print("destination = " + f"{destination}")
            print("filedestination = " + f"{filedestination}")
            print("hostname = " + f"{hostname}")

        finally:
            if len(os.listdir(filesource)) > 0:
                print("FOLDER IS GREATER THAN O")
                # shutil.rmtree(filesource)
                for f in os.listdir(filesource):
                    os.remove(os.path.join(filesource, f))
            else:
                print("FOLDER IS NOT GREATER THAN 0")

    else:
        print("Both names DONOT match !")
    
    # put a feeedback here
    self.progstatus.set(1)
    self.editgrpstatuslbl.configure(text=f"Process complete")
    self.cgouttxtbx.insert(INSERT, f"7) Backup process complete")
    self.cgouttxtbx.configure(state='disabled')


# THIS FUNCTION IS NOW REDUNDANT ooooohh no its not
'''
def tftpsaveconfig1(self, iam_selecteddevice):

    self.progstatus.set(0.4)
    self.editgrpstatuslbl.configure(text=f"Config process on id:{iam_selecteddevice}")
    self.update_idletasks()

    # Get iam_selecteddevice values (connecttodb.py > getdevicefromid(privide id))
    # return retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden
    retid=0
    retname=""
    retip=""
    retusername=""
    retpassword=""
    retdescription=""
    rettype=""
    retgolden=""

    retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getdevicefromid(iam_selecteddevice)
    
    print("1) This is tftpconfig(backuptftp.py)")
    print(f"2) This is tftpsaveconfig (iam_selecteddevice): {str(iam_selecteddevice)}")
    print(f"3) This is tftpsaveconfig (id): {str(retid)}")
    print(f"4) This is tftpsaveconfig (name): {retname}")
    print(f"5) This is tftpsaveconfig (ip): {retip}")
    print(f"6) This is tftpsaveconfig (username): {retusername}")
    print(f"7) This is tftpsaveconfig (password): {retpassword}")
    print(f"8) This is tftpsaveconfig (retdescription): {retdescription}")
    print(f"9) This is tftpsaveconfig (rettype): {rettype}")
    print(f"10) This is tftpsaveconfig (retgolden): {retgolden}")
    print(f"The tftpserver is: {tftpserver}")

    # enter the IP for your TFTP server here
    
    TFTP_SERVER = tftpserver
    print(f"The TFTP_SERVER is: {TFTP_SERVER}")
    
    hostname = ""
    filename = ""
    
    directorylocation = "/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/"
    filesource = '/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/'
    filedestination = f'/Shared/NetDevApp3/cisco12ct/devicedata/{hostname}/'
    changetoDEVICEDATAdirectory = f'/Shared/NetDevApp3/cisco12ct'
    
    filedatetime = str(time.strftime("%Y-%m-%d-%H-%M-%S"))
    
    device = {
    'device_type': 'cisco_ios',
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
        copy_command = f"copy running-config tftp:/{tftpserver}{directorylocation}"
        print(f"Copycommand=: {copy_command}")
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
                print("FOLDER IS NOT GREATER THAN 0")

    else:
        print("Both names DONOT match !")

'''


def tftpdevicebackup(self):
    
    devicesdetails = []
    self.tftpselectedid=StringVar()
    self.setbackuptypevar=StringVar() # Bakup type (startup, running)
    self.setfileidtypevar=StringVar() # File identifier (weekly, golden ?)

    sqliteConnection = sqlite3.connect(dbfile)
    cursor = sqliteConnection.cursor()
    #record = cursor.fetchall()
    query = (f"SELECT * FROM devices")
    cursor.execute(query)
    record = cursor.fetchall()
    for row in record:
        retid = row[0]
        retname = row[1]
        retip = row[2]
        retusername = row[3]
        retpassword = row[4]
        retdescription = row[5]
        rettype = row[6]
        retgolden = row[7]
        #retid, retname, retip, retusername, retpassword, retdescription, rettype, retgolden = getalldevices(self)
        devicesdetails.append(f"id:{retid}" + " " +  f"{retname}" + " " + f"({retip})")
        # print(f"{retid},{retname},{retip},{retusername},{retpassword},{retdescription},{rettype},{retgolden}")
        self.tftpselectedid.set(str(retid))
    
    def activatebackupbtn(self):
        if self.bktpeselecchkbx.get() !="Select" and self.fileidselec.get() !="Select":
            print("Both buton are not select")
            self.btnbackup.configure(state='normal', fg_color="green", hover_color='green4', border_width=2, border_color='dark green')
        else:
            print("A button must be select")
    
    def setbackuptype(self):
        self.setbackuptypevar.set(self.bktpeselecchkbx.get())
        if self.bktpeselecchkbx.get() =="Select":
            tk.messagebox.showinfo(title="Backup type selection error", message="Please select a valid backup type option.", icon='error', parent=self.tftpbackupwindow)
        else:
            self.devnotetxtbx.insert(INSERT, f"----------------------------------\nBackup type: {self.setbackuptypevar.get()}\n")
            # deactivate Type Identifier
            self.bktpeselectlbl.configure(state='disabled')
            self.bktpeselecchkbx.configure(border_color='gray', button_color='gray', fg_color="gray75", state='disabled')
            # self.bktpeselecchkbx.set(value="Select")
            self.bktpeselecbtn.configure(text="Accepted", fg_color="gray", state='disabled')
            # Activate File Identifier
            self.fileidlbl.configure(state='normal') # label
            self.fileidselec.configure(fg_color="pale green", state='readonly', border_color='dark slate gray', button_color='dark slate gray', button_hover_color='green4', dropdown_fg_color='pale green', dropdown_hover_color='PaleGreen3')
            self.fileidselec.set(value="Select")
            self.fileidbtn.configure(state='normal', fg_color="green", hover_color='green4')
        
            # This just asks if both coboboxes have a valid selection
            # activatebackupbtn(self)
 
            # put a feeedback here
            self.progstatus.set(0.2)
            # print(f"setbackuptype (353): {self.setbackuptypevar.get()}")
            self.editgrpstatuslbl.configure(text=f'{self.setbackuptypevar.get()} accepted')
    
    def setfileidtype(self):
        print("backuptftp.py fileidtype")
        self.setfileidtypevar.set(self.fileidselec.get())
        #self.devnotetxtbx.insert(INSERT, f"File identifier: {self.setbackuptypevar.get()}\n")
        #print(f"True or False or value : {self.fileidselec.state()}")

        if self.fileidselec.get() =="Select":
            tk.messagebox.showinfo(title="backup type", message="Please select a valid File identifier option.", icon='error', parent=self.tftpbackupwindow)
        else:
            self.devnotetxtbx.insert(INSERT, f"----------------------------------\nFile identifier: {self.fileidselec.get()}\n")
            # Deactivate File Identifier ('Daily','Weekly','Monthly','Golden','Silver')
            self.fileidlbl.configure(state='disabled')
            self.fileidselec.configure(border_color='gray', button_color='gray', fg_color="gray75", state='disabled')
            self.fileidbtn.configure(text="Accepted", fg_color="gray", state='disabled')
            # This just asks if both coboboxes have a valid selection
            activatebackupbtn(self)
            # put a feeedback here
            self.progstatus.set(0.3)
            self.editgrpstatuslbl.configure(text=f'File identified as: {self.setfileidtypevar.get()}')

    def setdevice(self):
        if self.devnamecbx.get() == "select a device":
            tk.messagebox.showinfo(title="Device selection error", message="Please select a valid Device option.", icon='error', parent=self.tftpbackupwindow)
        else:
            cbxid = re.findall(r'^\D*(\d+)', self.devnamecbx.get())
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
            print(f"{retid1},{retname1},{retip1},{retusername1},{retpassword1},{retdescription1},{rettype1},{retgolden1}")
            
            self.tftpselectedid.set(str(retid1))

            # DeActivate Device Selection
            self.devname.configure(state='disabled')
            self.devnamebtn.configure(text="Accepted", fg_color="gray", state='disabled') # button to select device once selected
            self.devnamecbx.configure(border_color='gray', button_color='gray', fg_color="gray75", state='disabled')
            
            # Activate Backup Type
            self.bktpeselectlbl.configure(state='normal')
            self.bktpeselecchkbx.configure(fg_color="pale green", state='readonly', border_color='dark slate gray', button_color='dark slate gray', button_hover_color='green4', dropdown_fg_color='pale green', dropdown_hover_color='PaleGreen3')
            self.bktpeselecchkbx.set(value="Select")
            self.bktpeselecbtn.configure(state='normal', fg_color="green", hover_color='green4')
            
            self.devnotelbl.configure(state='normal') # label
            self.devnotetxtbx.configure(state='normal', bg="light yellow", wrap=WORD) # label
            self.devnotetxtbx.insert(INSERT, f"Device id: {retid1}\n"+f"Device Name: {retname1}\n"+f"Device IP address: {retip1}\n")

            # put a feeedback here
            self.progstatus.set(0.1)
            self.editgrpstatuslbl.configure(text=f'{retname1} accepted')


    print("backuptftp.py / tftpdevicebackup")
    self.tftpbackupwindow = tk.Toplevel(master=self)
    self.tftpbackupwindow.title("Register")
    self.tftpbackupwindow.geometry('600x820+200+200')
    self.tftpbackupwindow.configure(background='powder blue')
    self.tftpbackupwindow.wm_iconphoto(False, (ImageTk.PhotoImage(Image.open(pythonicon))))
    
    # Disable root window when this one is active
    self.tftpbackupwindow.attributes('-topmost', 'true')
    self.tftpbackupwindow.transient(self)
    self.tftpbackupwindow.update_idletasks()
    self.tftpbackupwindow.grab_set()
    #self.tftpbackupwindow.wait_window()

    self.tftpbackupwindow.grid_columnconfigure(0, weight=1)
    # top title
    self.createlabel = ctk.CTkLabel(self.tftpbackupwindow, text="Backup a device configuration (TFTP)", font=('arial', 22, 'bold'))
    self.createlabel.grid(row=0, column=0,sticky=EW, columnspan=3, pady=(20,16))
    self.separator1 = ttk.Separator(self.tftpbackupwindow, orient='horizontal')
    self.separator1.grid(row=1, sticky=EW, columnspan=3, padx=20, pady=10)
    
    # Device Selection ([1,RTR1, (1.1.1.1)],[2,SW1,(2.2.2.2)],)
    self.devname = Label(self.tftpbackupwindow, text="Device selection", font=('arial', 14, 'bold'), bg="powder blue", fg='black')
    self.devname.grid(row=2, column=0,sticky=W, padx=(25,10), pady=10)
    self.devnamecbx = ctk.CTkComboBox(self.tftpbackupwindow, width=220, font=('arial', 14, 'bold'), fg_color="pale green", values=devicesdetails, border_color='dark slate gray', button_color='dark slate gray', button_hover_color='green4', dropdown_fg_color='pale green', dropdown_hover_color='PaleGreen3', dropdown_font=('arial', 16, 'bold'))
    self.devnamecbx.grid(row=2, column=1, sticky=EW, padx=(15,10), pady=10)
    self.devnamecbx.set("select a device")
    self.devnamebtn = ctk.CTkButton(self.tftpbackupwindow, text="Set", width=100, fg_color="green", hover_color='green4', command=lambda:setdevice(self)) # command=grpcbxselc,
    self.devnamebtn.grid(row=2, column=2, padx=(15,25), pady=10)

    # Backup Type
    self.bktpeselectlbl = Label(self.tftpbackupwindow, text="Backup type", font=('arial', 14, 'bold'), bg="powder blue", fg='black', state=DISABLED)
    self.bktpeselectlbl.grid(row=3, column=0 ,sticky=W, padx=(25,10), pady=10)
    self.bktpeselecchkbxvalues = ['running-config', 'startup-config']
    self.bktpeselecchkbx = ctk.CTkComboBox(self.tftpbackupwindow, font=('arial', 14, 'bold'), state='disabled', values=self.bktpeselecchkbxvalues, dropdown_font=('arial', 16, 'bold'))
    self.bktpeselecchkbx.grid(row=3, column=1,sticky=EW, padx=(15,10), pady=10)
    self.bktpeselecbtn = ctk.CTkButton(self.tftpbackupwindow, text="Set", state=DISABLED, width=100, fg_color="gray", hover_color='green4', command=lambda:setbackuptype(self)) # , command=memselectfun
    self.bktpeselecbtn.grid(row=3, column=2, padx=(15,25), pady=10)
    
    # File Identifier
    self.fileidlbl = Label(self.tftpbackupwindow, text="File identifier", font=('arial', 14, 'bold'), bg='powder blue', fg='black', state=DISABLED)
    self.fileidlbl.grid(row=4, column=0,sticky=W, padx=(25,10), pady=10)
    self.fileidoptions = ['Daily','Weekly','Monthly','Golden','Silver']
    self.fileidselec = ctk.CTkComboBox(self.tftpbackupwindow, state='disabled', font=('arial', 14, 'bold'), values=self.fileidoptions, dropdown_font=('arial', 16, 'bold'))
    self.fileidselec.grid(row=4, column=1,sticky=EW, padx=(15,10), pady=10)
    self.fileidbtn = ctk.CTkButton(self.tftpbackupwindow, text="Set", state=DISABLED, width=100, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'), command=lambda:setfileidtype(self)) #, command=confmethodselect
    self.fileidbtn.grid(row=4, column=2, padx=(15,25), pady=10)   

    # device Notes
    self.devnotelbl = Label(self.tftpbackupwindow, text="Notes", font='arial 14 bold', bg='powder blue', fg='black', state=DISABLED)
    self.devnotelbl.grid(row=5, column=0,sticky=NW, padx=25, pady=10)
    
    #grpdesetry = Text(ewindow, font='arial 14', height = 10, width = 25, bg="light yellow", wrap=WORD)
    self.devnotetxtbx = scrolledtext.ScrolledText(self.tftpbackupwindow, font='arial 12', height = 10, width = 25, bg="gray70", wrap=WORD, state=DISABLED)
    self.devnotetxtbx.grid(row=6, column=0, sticky=EW, padx=(25, 10), pady=(20), columnspan=2)
    # self.devnotetxtbtn = ctk.CTkButton(self.tftpbackupwindow, text="Set", state='disabled', width=100, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold')) # command=grpcmdstxtbx, 
    # self.devnotetxtbtn.grid(row=6, column=2, sticky=S, padx=30, pady=10) 

    # self.separator2 = ttk.Separator(self.tftpbackupwindow, orient='horizontal')
    # self.separator2.grid(row=7, sticky=EW, columnspan=3, padx=20, pady=10)
    
    self.progstatus = ctk.CTkProgressBar(self.tftpbackupwindow, progress_color='green4', border_width=1, border_color='dark slate gray')
    self.progstatus.grid(row=7, column=0, sticky=EW, padx=30, pady=10, columnspan=3)
    self.progstatus.set(0)
    
    self.btnbackup = ctk.CTkButton(self.tftpbackupwindow, text="Backup", state='disabled', width=120, fg_color="gray", hover_color='green4', font=('arial', 12, 'bold'), command=lambda:tftpbtngo(self, self.tftpselectedid.get())) #, command=lambda:callchangegroupfile(self, *args, **kwargs)
    self.btnbackup.grid(column=0, row=8, pady=10, padx=(25,0), sticky=W)
    
    self.editgrpstatuslbl = Label(self.tftpbackupwindow, text="Select a device", font=('arial', 14, 'bold'), bg="powder blue", fg='OrangeRed2')
    self.editgrpstatuslbl.grid(row=8, column=1, padx=(0,55), pady=10, sticky=EW)
    
    self.btnexit = ctk.CTkButton(self.tftpbackupwindow, text="EXIT", width=120, fg_color="red2", font=('arial', 12, 'bold'), command=self.tftpbackupwindow.destroy, hover_color='red4', border_width=2, border_color='red4') # , command=onexitcleanup
    self.btnexit.grid(column=2, row=8, pady=10, padx=(0,25), sticky=E)
    self.cgouttxtbx = scrolledtext.ScrolledText(self.tftpbackupwindow, font='arial 10', height = 11, width = 25, bg="light goldenrod yellow", wrap=WORD, state=DISABLED)
    self.cgouttxtbx.grid(row=9, column=0,sticky=EW, padx=(25, 25), pady=10, columnspan=3)

    
