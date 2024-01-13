# devnetnode
1) An application for Network engineers to manage Cisco devices (Python Tkinter).
2) Python & Netmiko provide funtional aspects.
3) Tkinter and Customtkinter presents a GUI to the user.

# Youtube introduction
1) https://www.youtube.com/watch?v=k-OvfekZ0YQ

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
9) tftpd-hpa (TFTP Server)

# Settings File (settings.py).
****>>>>---YOU SHOULD BE GOOD TO USE LINUX FILE DIRECTORY forwardslash, WINDOWS SHOULD SORT IT OUT
1) tftpserver = '10.24.35.253' # Change to your TFTP server
2) directorylocation = "C:\\Shared\\NetDevApp3\\devnetnode\\devicedata\\tftp_temp\\" # ****>>>>--- settings.py for a Windows environment
3) directorylocation = "/Shared/NetDevApp3/devnetnode/devicedata/tftp_temp/" # ****>>>>--- settings.py for a Linux environment

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

# TFTP server issues
1) tftpserver = '192.168.0.123' (settings.py = Change this to suit your server ip)
2) sudo apt install tftpd-hpa
3) sudo nano /etc/default/tftpd-hpa
4) /etc/default/tftpd-hpa 
5)  TFTP_USERNAME="tftp" 
6)  TFTP_DIRECTORY="/" 
7)  TFTP_ADDRESS=":69" 
8)  TFTP_OPTIONS="--secure --create"
9)  sudo chown tftp tftp_temp/
10) service tftpd-hpa restart  
11) sudo systemctl status tftp-hpa.service
12) sudo systemctl restart tftp-hpa.servic





