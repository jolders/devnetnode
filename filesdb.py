# processes = psutil / pip install psutil
# pathlib # purepath / home / cwd exists rename
from pprint import pprint
import psutil
import os
from os.path import exists
import shutil # Copying Moving Deleting
from tkinter import *
from tkinter import scrolledtext
# import tkinter as tk
from settings import *
import pathlib # filesystem paths
from connecttodb import getdevicefromid
import sqlite3
from mysql.connector import Error
from datetime import datetime


def saveframeoutput(self):
    # If grp checkbox = false use : thisdevicename = self.returnedname.get()
    # If grp checkbox = true use : thisdevicename = self.grpsectselect.get()
    thisdevicename=""
    saveoutputroot=""
    
    if self.groupswitch_var.get() == "on":
        thisdevicename = f"{self.groupoptionselected.get()}"
        print(f"ON=self.groupswitch_var on/off value")
        print(f"ON=self.groupswitch_var thisdevicename: {thisdevicename}")
        saveoutputroot = f"/Shared/NetDevApp3/cisco12ct/devicegroups/"
        print(f"ON=self.groupswitch_var saveoutputroot : {saveoutputroot}")
    else:
        print(f"OFF=self.groupswitch_var value: {self.groupswitch_var.get()}")
        thisdevicename = f"{self.returnedname.get()}"
        print(f"OFF=self.groupswitch_var off value")
        print(f"OFF=self.groupswitch_var thisdevicename: {thisdevicename}")
        saveoutputroot = f"/Shared/NetDevApp3/cisco12ct/devicedata/"
        print(f"OFF=self.groupswitch_var saveoutputroot : {saveoutputroot}")
                                                                    

    print(f"1) self.groupswitch_var on/off value (filesdb.py): {str(self.groupswitch_var.get())}")
    print(f"1) self.groupoptionselected.get() = (filesdb.py)=: {str(self.groupoptionselected.get())}")
    print(f"1) self.groupoptionselected.get() = (filesdb.py)=: {str(self.returnedname.get())}")
    print(f"1) saveoutput thisdevicename (filesdb.py): {thisdevicename}")
    
    #Create a folder
    print(f"2) The current working directory is (filesdb.py): {os.getcwd()}")
    print(f"2) devicesaveddata: {devicesaveddata}")
    print(f"2) thisdevicename : {thisdevicename}")
    devicepath = os.path.join(saveoutputroot, thisdevicename)
    print(f"2) The devicepath directory is (filesdb.py): {devicepath}")
    
    if not os.path.exists(devicepath):
        os.mkdir(devicepath)
        print(f"4) New directory created (filesdb.py): {devicepath}")
    
    # change directory to current directory
    os.chdir(os.path.join(saveoutputroot, thisdevicename))
    print(f"5) Directory path root is now (filesdb.py): {os.getcwd()}")
    print(f"5) devicesaveddata: {devicesaveddata}")
    print(f"5) thisdevicename (thisdevicename): {devicesaveddata}")
    
    
    mydatetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S"+".txt")
    print(f"6) (filesdb.py) mydatetime: {mydatetime}")
    
    '''
    if exists(myfilename):
        print("The file already exists")
    else:
        print("The file does not exist")
        try:
            print("START - create file")
            second = open(myfilename, 'x')
            print("END - create file")
        except:
            print("A problem creating a base file")
    '''
    
            
    # Capture data in the window
    stufftowrite = self.txtcontent.get("1.0", END)
    print(f"7) This is stuff captured from txtcontent (filesdb.py): {stufftowrite}")
    
    
            
    appenddata = open(mydatetime, 'w', encoding="utf-8")
    appenddata.write(stufftowrite)
    appenddata.close()
    
    #return base dir to base
    os.chdir(directorypathroot)
    print(f"8) The current working directory is (filesdb.py) : {os.getcwd()}")
