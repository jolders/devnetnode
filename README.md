# devnetnode
An application for Network engineers to manage Cisco devices (Python Tkinter).

# Device key features:
1) Create device profiles (ip address, hostname, Username, password, device type, config file) 
2) Send commands to Cisco IOS devices.
3) Receive requested information from Cisco IOS devices.
4) Backup Cisco IOS devices.
5) Restore Cisco IOS devices.

# Group Devices features:
1) Build groups of devices.
2) Send commands to groups of Cisco devices.
3) Receive information groups of Cisco devices.
4) Backup groups of devices.
5) Restore groups of devices.

# Help with installation and running
****>>>>---YOU WILL NEED TO have installed alot of dependentcies 
sqlite3, mysql.connector
os, os.path(exists)
shutil, time, datetime
tkinter, ttk, scrolledtext, messagebox, filedialog
customtkinter
Netmiko, paramiko
PIL, ImageTk, Image
regex
from 

# Settings File (settings.py).
****>>>>---YOU WILL NEED TO CHANGE ITEMS IN THIS FILE DEPENDING ON YOUR OWN FILE ARRANGEMENT
tftpserver = '10.24.35.253' # Change to your TFTP server
directorylocation = "C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\tftp_temp\\" # Windows directory identification example
directorylocation = "/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/" # Linux directory identification example
# Ammend this list to present commands you want.
listOfCMDs = ['show version','show running-config','show ip interface brief','show ip route','show interface gigabitEthernet 0/0','show vlan']



