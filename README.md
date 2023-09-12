# devnetnode
1) An application for Network engineers to manage Cisco devices (Python Tkinter).
2) Python & Netmiko provide funtional aspects.
3) Tkinter and Customtkinter presents a GUI to the user.

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

# Netmiko issues (version issue)
Sometimes Netmiko will complain.
"No module named 'netmiko.ssh_exception'"
1) # Change:
2) from netmiko.ssh_exception import NetMikoAuthenticationException
3) from netmiko.ssh_exception import NetMikoTimeoutException
4) from netmiko.ssh_exception import SSHException
1) # To:
2) from netmiko.exceptions import NetMikoAuthenticationException
3) from netmiko.exceptions import NetMikoTimeoutException
4) from netmiko.exceptions import SSHException




