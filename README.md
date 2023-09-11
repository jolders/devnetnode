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
****>>>>---A list of dependencies (They may be more...)
1) sqlite3, mysql.connector
2) os, os.path
3) shutil, time, datetime
4) tkinter, ttk, scrolledtext, messagebox, filedialog
5) customtkinter
6) Netmiko, paramiko
7) PIL, ImageTk, Image
8) regex

# Settings File (settings.py).
****>>>>---YOU WILL NEED TO CHANGE ITEMS IN THIS FILE DEPENDING ON YOUR OWN INSTALLATION
1) tftpserver = '10.24.35.253' # Change to your TFTP server
2) directorylocation = "C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\tftp_temp\\" # Windows directory identification example
3) directorylocation = "/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/" # Linux directory identification example
# Ammend this list to present commands you want.
1) listOfCMDs = ['show version','show running-config','show ip interface brief','show ip route','show interface gigabitEthernet 0/0','show vlan']



