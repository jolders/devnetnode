# Location of files
# dbfile = "C:\\Shared\\NetDevApp3\\cisco12ct\\netAdmin.db"
# directorypathroot ="C:\\Shared\\NetDevApp3\\cisco12ct"
# devicegroups = "C:\\Shared\\NetDevApp3\\cisco12ct\\devicegroups"
# pythonicon = "C:\\Shared\\NetDevApp3\\cisco12ct\\myicon64.png"
# devicesaveddata = "C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\"
# tftprootdir = "C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\tftp_temp"

#TFTP_SERVER = tftpserver (Windows)
# directorylocation = "C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\tftp_temp\\"
# filesource = "C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\tftp_temp\\"
#filedestination = "C:\\Shared\\NetDevApp3\\cisco12ct\\devicedata\\{hostname}\\"
# changetoDEVICEDATAdirectory = "C:\\Shared\\NetDevApp3\\cisco12ct"

tftpserver = '10.24.35.253'
# tftpserver = '192.168.0.123'

sideframecolour = 'light blue'
bottomframecolour = 'light blue'
topframeacolour = 'light blue'
topframebcolour = 'light blue'

# Linux Format of file locations
dbfile = "/Shared/NetDevApp3/cisco12ct/netAdmin.db"
directorypathroot ="/Shared/NetDevApp3/cisco12ct/"
devicegroups = "/Shared/NetDevApp3/cisco12ct/devicegroups"
pythonicon = "/Shared/NetDevApp3/cisco12ct/pythonicon.ico"
devicesaveddata = "/Shared/NetDevApp3/cisco12ct/devicedata/"
tftprootdir = "/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp"

#TFTP_SERVER = tftpserver Linux
directorylocation = "/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/"
filesource = '/Shared/NetDevApp3/cisco12ct/devicedata/tftp_temp/'
filedestination = '/Shared/NetDevApp3/cisco12ct/devicedata/'
changetoDEVICEDATAdirectory = '/Shared/NetDevApp3/cisco12ct'

listOfCMDs = ['show version',
              'show running-config',
              'show ip interface brief',
              'show ip route',
              'show interface gigabitEthernet 0/0',
              'show interface gigabitEthernet 0/1',
              'show interface gigabitEthernet 0/2',
              'show interface gigabitEthernet 0/3',
              'show interface gigabitEthernet 0/4',
              'show interface gigabitEthernet 1/0',
              'show interface gigabitEthernet 1/1',
              'show arp',
              'show flash:',
              'show vlan']

print("(settings.py) = page test")

# Permission change to folder for TFTP
# chown -R tftp /Shared/NetDevApp3/cisco10/devicedata/tftp_temp


