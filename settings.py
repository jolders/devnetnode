# Location of files
# dbfile = "C:\\Shared\devnetnode\\devnetnode\\netAdmin.db"
# directorypathroot ="C:\\Shared\devnetnode\\devnetnode"
# devicegroups = "C:\\Shared\devnetnode\\devnetnode\\devicegroups"
# pythonicon = "C:\\Shared\devnetnode\\devnetnode\\myicon64.png"
# devicesaveddata = "C:\\Shared\devnetnode\\devnetnode\\devicedata\\"
# tftprootdir = "C:\\Shared\devnetnode\\devnetnode\\devicedata\\tftp_temp"

#TFTP_SERVER = tftpserver (Windows)
# directorylocation = "C:\\Shared\devnetnode\\devnetnode\\devicedata\\tftp_temp\\"
# filesource = "C:\\Shared\devnetnode\\devnetnode\\tftp_temp\\"
#filedestination = "C:\\Shared\devnetnode\\devnetnode\\devicedata\\{hostname}\\"
# changetoDEVICEDATAdirectory = "C:\\Shared\devnetnode\\devnetnode"

tftpserver = '10.24.35.253'
# tftpserver = '192.168.0.123'

sideframecolour = 'light blue'
bottomframecolour = 'light blue'
topframeacolour = 'light blue'
topframebcolour = 'light blue'

# Linux Format of file locations
dbfile = "/Shared/devnetnode/devnetnode/netAdmin.db"

directorypathroot ="/Shared/devnetnode/devnetnode/"
devicegroups = "/Shared/devnetnode/devnetnode/devicegroups"
pythonicon = "/Shared/devnetnode/devnetnode/pythonicon.ico"
devicesaveddata = "/Shared/devnetnode/devnetnode/devicedata/"
tftprootdir = "/Shared/devnetnode/devnetnode/devicedata/tftp_temp"

#TFTP_SERVER = tftpserver Linux
directorylocation = "/Shared/devnetnode/devnetnode/devicedata/tftp_temp/"
filesource = '/Shared/devnetnode/devnetnode/devicedata/tftp_temp/'
filedestination = '/Shared/devnetnode/devnetnode/devicedata/'
changetoDEVICEDATAdirectory = '/Shared/devnetnode/devnetnode'

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


