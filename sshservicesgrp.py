from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import scrolledtext
import sqlite3
from mysql.connector import Error
import paramiko
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko import client
from netmiko import Netmiko, ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
import time
import os
from settings import *
import json
from connecttodb import getdevicefromid

def getdevicefromidgrp(rowIDrow): 
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

def grpselectionget(self, groupselection):
    # Group selection get values
    print("Groupselection (sshservicesgrp/grpselectionget()) get values")
    # What directory am I in
    print(f"1) The current working directory is (SSHSERVICESGRP.py): {os.getcwd()}")

    # Change the directory to 'London routers' = 'devicegroups'
    os.chdir(devicegroups)
    groupdevicepath = os.path.join(devicegroups, groupselection)
    os.chdir(groupdevicepath)
    print(f"1a) The current working directory is (SSHSERVICESGRP.py): {os.getcwd()}")
    print(f"1b) The current working directory is (SSHSERVICESGRP.py): {os.getcwd()}")
    # Get the json file
    filepath = os.path.join(groupselection + ".json")
    print(f"1b) (SSHSERVICESGRP.py) filepath = {filepath}")
    filetoread = open(filepath)
    inputjsondata = json.load(filetoread)
    print(f"1c) Data in members: {inputjsondata['members']}")
    return inputjsondata['members']
    # Extract the data from the json file

def runcmdparamikogrp(self, groupselection, cmdselected):
    print(f"1a) This is runcmdparamikogrp (groupselection): {groupselection}")
    print(f"2a) This is runcmdparamikogrp (cmdselected): {cmdselected}")
    grpmemberreturn = grpselectionget(self, groupselection)
    print(f"3) These are the grp members this is runcmdparamikogrp (grpmemberreturn): {grpmemberreturn}")
    print(f"4) This is runcmdparamikogrp (groupselection): {groupselection}")
    print(f"5) This is runcmdparamikogrp (cmdselected): {cmdselected}")
    
    for i in grpmemberreturn:
        retid=0
        retname=""
        retip=""
        retusername=""
        retpassword=""
        #retdescription=[]

        
        print(i)
        getdevicefromidgrp(i)
        
        try:
            retid, retname, retip, retusername, retpassword = getdevicefromidgrp(i)
        except TypeError:
                print(f"Printing load device 'Try block is error exception' ")
        
        print(f"Printing load device 'Try block is success' ")
        print(f"retid: {retid}")
        print(f"retname: {retname}")
        print(f"retip: {retip}")
        print(f"retusername: {retusername}")
        print(f"retpassword: {retpassword}")
        #print(f"retdescription: {retdescription}")

        ssh_client = client.SSHClient()
        #client.load_host_keys()
        ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())

        try:
            ssh_client.connect(hostname=retip, port=22, username=retusername, password=retpassword) # look_for_keys=False, allow_agent=False
            print("SSH CONNECTION successfull")
            cmd = cmdselected
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            # print(stdout.readlines())
            self.txtcontent.insert(INSERT, "- - - - * - - - * - - - - *   START  (" + retname + ")   * - - - * - - - - * - - - - " + "\n")
            for line in stdout.readlines():
                testvar=line.strip()
                self.txtcontent.insert(INSERT, f"{testvar}" + "\n")
            self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - * - - - - *   END  (" + retname + ")   * - - - * - - - - * - - - - " + "\n")
        except:
            self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - * - - - - *   FAILED TO CONNECT  (" + retname + ")   * - - - * - - - - * - - - - " + "\n")
        finally:
            ssh_client.close()
        
def runcmdnetmikogrp(self, groupselection, cmdselected):
    grpmemberreturn = grpselectionget(self, groupselection)
    self.txtcontent.insert(INSERT, "- - - - * - - - * - - - - *   START  (" + groupselection + ")   * - - - * - - - - * - - - - " + "\n")
    for i in grpmemberreturn:
        retid=0
        retname=""
        retip=""
        retusername=""
        retpassword=""
        #retdescription=""
        
        print(i)
        # getdevicefromid(i)

        try:
            retid, retname, retip, retusername, retpassword = getdevicefromidgrp(i)
        except TypeError:
                print(f"Printing load device 'Try block is error exception' ")
        
        print(f"Printing load device 'Try block is success' ")
        print(f"retid: {retid}")
        print(f"retname: {retname}")
        print(f"retip: {retip}")
        print(f"retusername: {retusername}")
        print(f"retpassword: {retpassword}")
        #print(f"retdescription: {retdescription}")
        
        credentials = {'device_type': 'cisco_ios', 'host': f'{retip}', 'username': f'{retusername}', 'password': f'{retpassword}'}
        
        print(f"This is runcmdnetmikogrp (ip): {retip}")
        print(f"This is runcmdnetmikogrp (username): {retusername}")
        print(f"This is runcmdnetmikogrp (password): {retpassword}")
        print(f"This is runcmdnetmikogrp (cmdselected): {cmdselected}")
        
        time.sleep(0.3)
        
        try:
            print(f"This is runcmdnetmikogrp - starting try")
            net_connect = Netmiko(**credentials)
            dev_prompt = net_connect.find_prompt()
            print(f"Device in Enable mode? : {net_connect.check_enable_mode()}")
            print(f"Device in Config mode? : {net_connect.check_config_mode()}")
            sh_output = net_connect.send_command(cmdselected)
            net_connect.disconnect()
            self.statuslbl.set(f"Successfull: ({dev_prompt})")
            print(f"This is runcmdnetmikogrp - ending try")
        except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            print(f"This is runcmdnetmikogrp (error,exception)= {e}")
            self.statuslbl.set(f"Connection Error to : ({retip})")
        finally:
            if net_connect == True:
                net_connect.disconnect()

            # DISPLAY THE LOOP OUTPUT TO THE USER
            self.txtcontent.insert(INSERT, "- - - - * - - - * - - - - *   START  (" + retname + ")   * - - - * - - - - * - - - - " + "\n")
            self.txtcontent.insert(INSERT, f"{sh_output}")
            self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - * - - - - *   END  (" + retname + ")   * - - - * - - - - * - - - - " + "\n" + "\n")

    self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - * - - - - *   END  (" + groupselection + ")   * - - - * - - - - * - - - - " + "\n")

def runcmdnetmikogrp_ch(self, groupselection, cmdselected):
    print(f"1) This is runcmdnetmikogrp_ch (groupselection): {groupselection}")
    print(f"2) This is runcmdnetmikogrp_ch (cmdselected): {cmdselected}")
    grpmemberreturn = grpselectionget(self, groupselection)
    self.txtcontent.insert(INSERT, "- - - - * - - - * - - - - *   START  (" + groupselection + ")   * - - - * - - - - * - - - - " + "\n")
    for i in grpmemberreturn:
        retid=0
        retname=""
        retip=""
        retusername=""
        retpassword=""
        #retdescription=""
        
        print(i)
        # getdevicefromid(i)

        try:
            retid, retname, retip, retusername, retpassword = getdevicefromidgrp(i)
        except TypeError:
                print(f"3) Printing load device 'Try block is error exception' ")
        
        print(f"4) Printing load device 'Try block is success' ")
        print(f"5) retid: {retid}")
        print(f"6) retname: {retname}")
        print(f"7) retip: {retip}")
        print(f"8) retusername: {retusername}")
        print(f"9) retpassword: {retpassword}")
        #print(f"10) retdescription: {retdescription}")

        credentials = {'device_type': 'cisco_ios', 'host': f'{retip}', 'username': f'{retusername}', 'password': f'{retpassword}'}
        
        print(f"11) This is runcmdnetmikogrp_ch (ip): {retip}")
        print(f"12) This is runcmdnetmikogrp_ch (username): {retusername}")
        print(f"13) This is runcmdnetmikogrp_ch (password): {retpassword}")
        print(f"14) This is runcmdnetmikogrp_ch (cmdselected): {cmdselected}")

        cisco_device = {'device_type': 'cisco_ios', 'host': retip, 'username': retusername,
                         'password': retpassword, 'port': 22, 'secret': retpassword, 'verbose': True}
        
        try:
            conn = ConnectHandler(**cisco_device)
            conn_prompt = conn.find_prompt()
            if '>' in conn_prompt: conn.enable()
            # print(conn_prompt)
            output = conn.send_command(cmdselected)
            print(f"Checking the config mode: {conn.check_config_mode()}")

        except:
            print("A connection error in runcmdnetmiko_ch")
        
        finally:
            conn.disconnect()
            self.txtcontent.insert(INSERT, "- - - - * - - - * - - - - *   START  (" + retname + ")   * - - - * - - - - * - - - - " + "\n")
            self.txtcontent.insert(INSERT, f"{output}")
            self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - * - - - - *   END  (" + retname + ")   * - - - * - - - - * - - - - " + "\n" + "\n")

        self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - * - - - - *   END  (" + groupselection + ")   * - - - * - - - - * - - - - " + "\n")

def runcmdnetmikogrp_ch_config(self, groupselection): #, cmdselected
    print(f"1) This is runcmdnetmikogrp_ch_config (groupselection): {groupselection}")
    #print(f"2) This is runcmdnetmikogrp_ch_config (cmdselected): {cmdselected}")
    grpmemberreturn = grpselectionget(self, groupselection)
    self.txtcontent.insert(INSERT, "- - - - * - - - * - - - - *   START  (" + groupselection + ")   * - - - * - - - - * - - - - " + "\n")

    for i in grpmemberreturn:
        retid=0
        retname=""
        retip=""
        retusername=""
        retpassword=""
        #retdescription=""

        print(i)
        # getdevicefromid(i)

        try:
            retid, retname, retip, retusername, retpassword = getdevicefromidgrp(i)
        except TypeError:
                print(f"3) Printing load device 'Try block is error exception' ")
        
        print(f"4) Printing load device 'Try block is success' ")
        print(f"5) retid: {retid}")
        print(f"6) retname: {retname}")
        print(f"7) retip: {retip}")
        print(f"8) retusername: {retusername}")
        print(f"9) retpassword: {retpassword}")
        #print(f"10) retdescription: {retdescription}")

        credentials = {'device_type': 'cisco_ios', 'host': f'{retip}', 'username': f'{retusername}', 'password': f'{retpassword}'}
        
        print(f"11) This is runcmdnetmikogrp_ch (ip): {retip}")
        print(f"12) This is runcmdnetmikogrp_ch (username): {retusername}")
        print(f"13) This is runcmdnetmikogrp_ch (password): {retpassword}")
        #print(f"14) This is runcmdnetmikogrp_ch (cmdselected): {cmdselected}")

        cisco_device = {'device_type': 'cisco_ios', 'host': retip, 'username': retusername,
                         'password': retpassword, 'port': 22, 'secret': retpassword, 'verbose': True}
        
        cmd_list =[]
        thisoutput = StringVar()
        conn_prompt = ""
        
        #print(f"TASK 1 runcmdnetmikogrp_ch_config (cmds): ({cmdselected})")
        
        # get the contents of the listbox and give it a list
        # print("printcustcmds")
        custcmdsget = self.cmdtxtbox.get("1.0", END)
        # print(f"I am  in [cmdframebox.printcustcmds]: {custcmdsget}")
        for line in custcmdsget.split("\n"):
             print(f"runcmdnetmikogrp_ch_config (cmds): {line}")
        #self.varselected.set(custcmdsget)
        cmd_list = [y for y in (x.strip() for x in custcmdsget.splitlines()) if y]
        print(f"I am  in [cmdlist.printcustcmds]{cmd_list}")
        # self.varselected.set(cmd_list)
        
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
             self.txtcontent.insert(INSERT, f"{e}")
        
        finally:
            # net_connect.exit_config_mode()
            # print(f"Finally 1 whats the command prompt: ({conn_prompt})")
            wmout=StringVar()
            wmout = net_connect.send_command('write memory')
            net_connect.disconnect()
            self.txtcontent.insert(INSERT, f"{wmout}")
        
        self.txtcontent.insert(INSERT, "\n" + "- - - - * - - - - * -  END  - * - - - - * - - - - " + "\n")