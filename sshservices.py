from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import scrolledtext
from settings import *
import sqlite3
from mysql.connector import Error
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko import client, ssh_exception
from netmiko import Netmiko, ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import time

def getdevicefromid(rowIDrow): 
    print("I am 'getdevicefromid' row id: " + str(rowIDrow))
    try:
        sqliteConnection = sqlite3.connect(dbfile)
        cursor = sqliteConnection.cursor()
        #record = cursor.fetchall()
        query = (f"SELECT * FROM devices WHERE id = {rowIDrow}")
        cursor.execute(query)
        record = cursor.fetchall()
        for row in record:
            retid = row[0]
            retname = row[1]
            retip = row[2]
            retusername = row[3]
            retpassword = row[4]
            
        return retid, retname, retip, retusername, retpassword
        
    except sqlite3.Error as error:
        print("The error (connecttodb.py) message is: ", error)
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)

def runcmdparamiko(self, iam_selecteddevice):
    retid=0
    retname=""
    retip=""
    retusername=""
    retpassword=""
    retid, retname, retip, retusername, retpassword = getdevicefromid(iam_selecteddevice)
    
    print(f"This is runcmdparamiko (self.cmdvarselected.get()): {self.cmdvarselected.get()}")
    print(f"This is runcmdparamiko (iam_selecteddevice): {iam_selecteddevice}")
    print(f"This is runcmdparamiko (id): {str(retid)}")
    print(f"This is runcmdparamiko (name): {retname}")
    print(f"This is runcmdparamiko (ip): {retip}")
    print(f"This is runcmdparamiko (username): {retusername}")
    print(f"This is runcmdparamiko (password): {retpassword}")
    
    ssh_client = client.SSHClient()
    #client.load_host_keys()
    ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())

    ###################
    # Starting the process so feedback on status label
    #####################
    self.returnedname.set(retname) # FEEDBACK Name to main.py
    print(f"runcmdparamiko value setting self.returnedname: {self.returnedname.get()}")
    
    try:
        ssh_client.connect(hostname=retip, port=22, username=retusername, password=retpassword) # look_for_keys=False, allow_agent=False
        print("SSH CONNECTION successfull")
        cmd = self.cmdvarselected.get()
        print(cmd)
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        self.txtcontent.insert(INSERT, f"- - - - * - - - - * - - - - * - START (" + retname + ") - * - - - - * - - - - * - - - - " + "\n")
        for line in stdout.readlines():
            testvar=line.strip()
            self.txtcontent.insert(INSERT, f"{testvar}" + "\n")
        self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - - * - - - - * - - END (" + retname + ") - - * - - - - * - - - - * - - - - " + "\n")
    
    except ssh_exception.NoValidConnectionsError as sshNoValidException:
        print("(sshservices.py 77): No Valid Connections Error SSH connection 'USERNAME ?': %s" % sshNoValidException)
    
    except ssh_exception.AuthenticationException as authException:
        print("(sshservices.py 79): Authentication Type SSH connection exception 'PASSWORD ?': %s" % authException)
    except ssh_exception.BadAuthenticationType as authTypeException:
        print("(sshservices.py 81): Authentication SSH connection exception: %s" % authTypeException)
    except ssh_exception.SSHException as sshException:
        print("(sshservices.py 83): Unable to establish SSH connection: %s" % sshException)
    except Exception as unknown_error:
        print('(sshservices.py 85):Some other error: ' + str(unknown_error))
        self.txtcontent.insert(INSERT, f"- - - - * - - - - * - - - - * - START (" + retname + ") - * - - - - * - - - - * - - - - " + "\n")
        self.txtcontent.insert(INSERT, "\n" + f"{unknown_error}" + "\n")
        self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - - * - - - - * - - END (" + retname + ") - - * - - - - * - - - - * - - - - " + "\n")
    
    finally:
        ssh_client.close()

        
def runcmdnetmiko(self, iam_selecteddevice):
    retid=0
    retname=""
    retip=""
    retusername=""
    retpassword=""
    retid, retname, retip, retusername, retpassword = getdevicefromid(iam_selecteddevice)
    print(f"This is runcmdnetmiko (iam_selecteddevice): {iam_selecteddevice}")
    print(f"This is runcmdparamiko (self.cmdvarselected.get()): {self.cmdvarselected.get()}")
    print(f"This is runcmdparamiko (id): {str(retid)}")
    print(f"This is runcmdparamiko (name): {retname}")
    print(f"This is runcmdparamiko (ip): {retip}")
    print(f"This is runcmdparamiko (username): {retusername}")
    print(f"This is runcmdparamiko (password): {retpassword}")
    
    credentials = {
        'device_type': 'cisco_ios',
        'host': f'{retip}',
        'username': f'{retusername}',
        'password': f'{retpassword}'}
    
    time.sleep(1)
    self.returnedname.set(retname) # FEEDBACK Name to main.py
    print(f"runcmdnetmiko value setting self.returnedname: {self.returnedname.get()}")
    
    try:
        print(f"This is runcmdnetmiko - starting try")
        net_connect = Netmiko(**credentials)
        dev_prompt = net_connect.find_prompt()
        print(f"Device in Enable mode? : {net_connect.check_enable_mode()}")
        print(f"Device in Config mode? : {net_connect.check_config_mode()}")
        sh_output = net_connect.send_command(self.cmdvarselected.get())
        net_connect.disconnect()
        # self.statuslbl.set(f"Successfull: ({dev_prompt})")
        print(f"This is runcmdnetmiko - ending try")
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print(f"This is runcmdnetmiko (error,exception)= {e}")
        # self.statuslbl.set(f"Connection Error to : ({retip})")
    finally:
        try:
            if net_connect:
                net_connect.disconnect()
        except:
            print("Exception (sshservices.py Netmiko) in net_connect")
        

        self.txtcontent.insert(INSERT, "- - - - * - - - * - - - - *   START  (" + retname + ")   * - - - * - - - - * - - - - " + "\n")
        try:
            self.txtcontent.insert(INSERT, f"{sh_output}")
        except:
            self.txtcontent.insert(INSERT, f"Error connecting to device")
        self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - * - - - - *   END  (" + retname + ")   * - - - * - - - - * - - - - " + "\n" + "\n")

    self.returnedname.set(retname)

def runcmdnetmiko_ch(self, iam_selecteddevice):
    retid=0
    retname=""
    retip=""
    retusername=""
    retpassword=""
    retid, retname, retip, retusername, retpassword = getdevicefromid(iam_selecteddevice)
    print(f"This is runcmdnetmiko_ch (iam_selecteddevice): {iam_selecteddevice}")
    print(f"This is runcmdnetmiko_ch (self.cmdvarselected.get()): {self.cmdvarselected.get()}")
    print(f"This is runcmdnetmiko_ch (id): {str(retid)}")
    print(f"This is runcmdnetmiko_ch (name): {retname}")
    print(f"This is runcmdnetmiko_ch (ip): {retip}")
    print(f"This is runcmdnetmiko_ch (username): {retusername}")
    print(f"This is runcmdnetmiko_ch (password): {retpassword}")
    
    cisco_device = {
        'device_type': 'cisco_ios',
        'host': retip,
        'username': retusername,
        'password': retpassword,
        'port': 22,
        'secret': retpassword,
        'verbose': True}
    
    output=""
    self.txtcontent.insert(INSERT, f"- - - - * - - - - * - START - * - - - - * - - - - " + "\n")

    self.returnedname.set(retname) # FEEDBACK Name to main.py
    print(f"runcmdnetmiko_ch value setting self.returnedname: {self.returnedname.get()}")

    try:
        conn = ConnectHandler(**cisco_device)
        conn_prompt = conn.find_prompt()
        if '>' in conn_prompt: conn.enable()
        # print(conn_prompt)
        output = conn.send_command(self.cmdvarselected.get())
        
        print(f"Checking the config mode: {conn.check_config_mode()}")
        
    except:
        print("A connection error in runcmdnetmiko_ch")
    finally:
        # An un-captured error occurred here if unable to log in to router
        conn.disconnect()
    
    self.txtcontent.insert(INSERT, f"{output}")
    self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - - * -  END  - * - - - - * - - - - " + "\n")
    
    '''
    output=""
    try:
        print(f"This is runcmdnetmiko")
        self.txtcontent.insert(INSERT, "Conecting...........")
        connection = Netmiko(host=ip, port=22, username=username, password=password, device_type='cisco_ios')
        output=connection.send_command(cmdselected)
        connection.disconnect()
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print(f"This is runcmdnetmiko (error)= {e}")
    finally:
        if connection == True: 
            connection.disconnect()
            print(f"Connection disconnect runcmdnetmiko")
        self.txtcontent.insert(INSERT, f"{output}")
    '''
    
    
# # # # # # # # # # ----- RAW Paramiko SSH  ----- # # # # # # # # # # 
''' # SAVE AS AN EXAMPLE OF ALTERNATIVE SSH CONNECTION VIA SHELL
def pariamiko_raw(self, ip, username, password):

    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    deviceconnection = {'hostname': '', 'port': '22', 'username': '', 'password': ''}
    deviceconnection["hostname"]=ip
    deviceconnection["username"]=username
    deviceconnection["password"]=password

    
    try:
        print(f"Trying to connect to {deviceconnection['hostname']}")
        client.connect(**deviceconnection, look_for_keys=False, allow_agent=False)
        print(client.get_transport().is_active())
        
        shell = client.invoke_shell()
        shell.send('terminal length 0\n')
        time.sleep(.2)
        shell.send('show run\n')
        time.sleep(5)
        output = shell.recv(65535)
        time.sleep(.2)
        mystr = output.decode(encoding='utf-8')
        print(mystr)
        self.txtcontent.insert(INSERT, f"{mystr}")
    except:
        print("FAILED TO CONNECT")
        print(client.get_transport().is_active())
    finally:
        client.close()
        print("CLOSING CONNECTION TO THE DEVICE")
'''


def runcmdnetmiko_ch_config(self, iam_selecteddevice):
    retid=0
    retname=""
    retip=""
    retusername=""
    retpassword=""
    retid, retname, retip, retusername, retpassword = getdevicefromid(iam_selecteddevice)
    print(f"This is runcmdparamiko (iam_selecteddevice): {iam_selecteddevice}")
    print(f"This is runcmdparamiko (id): {str(retid)}")
    print(f"This is runcmdparamiko (name): {retname}")
    print(f"This is runcmdparamiko (ip): {retip}")
    print(f"This is runcmdparamiko (username): {retusername}")
    print(f"This is runcmdparamiko (password): {retpassword}")

    
    cmd_list =[]
    thisoutput=StringVar()
    conn_prompt=""
    
    credentials = {
        'device_type': 'cisco_ios',
        'host': retip,
        'username': retusername,
        'password': retpassword,
        'port': 22,
        'secret': retusername,
        'verbose': True}
    
    # print(f"TASK 1 runcmdnetmiko_ch_config (cmds): ({iam_selecteddevice})")
    self.txtcontent.insert(INSERT, f"- - - - * - - - - * - START - * - - - - * - - - - " + "\n")
    
    # get the contents of the listbox and give it a list
    custcmdsget = self.cmdtxtbox.get("1.0", END)
    print(f"I am  in [cmdframebox.printcustcmds]: {custcmdsget}")
    for line in custcmdsget.split("\n"):
        print(f"{line}")
        #self.varselected.set(custcmdsget)
    cmd_list = [y for y in (x.strip() for x in custcmdsget.splitlines()) if y]
    print(f"I am  in [cmdlist.printcustcmds]{cmd_list}")
    # self.varselected.set(cmd_list)

    self.returnedname.set(retname) # FEEDBACK Name to main.py
    print(f"runcmdnetmiko_ch_config value setting self.returnedname: {self.returnedname.get()}")

    try:
        print(f"Try block 1 (cmds): ({cmd_list})")
        net_connect = ConnectHandler(**credentials)
        # Enter the ENABLE command on the router
        conn_prompt = net_connect.find_prompt()
        if '>' in conn_prompt: net_connect.enable()
        # print(f"Try block 2 (con prompt): ({conn_prompt})")
        thisoutput= net_connect.send_config_set(cmd_list)
        self.txtcontent.insert(INSERT, f"{thisoutput}")
        
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
        print(f"Netmiko_CH_config error: {e}")
        
    finally:
        #net_connect.exit_config_mode()
        #print(f"Finally 1 whats the command prompt: ({conn_prompt})")
        wmout=StringVar()
        wmout = net_connect.send_command('write memory')
        net_connect.disconnect()
        
        self.txtcontent.insert(INSERT, f"{wmout}")
        self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - - * -  END  - * - - - - * - - - - " + "\n")
