from pysnmp import hlapi
import quicksnmp
import socket


#1.3.6.1.2.1.1.4.0 = sysContact
#1.3.6.1.2.1.1.5.0 = sysName
#1.3.6.1.2.1.1.3.0 = upTime
#1.3.6.1.2.1.1.1.0 = sysDescr
#1.3.6.1.2.1.1.6.0 = sysLocation

print("iShip sein SNMP omg")

while True:
    ipaddress = input("Enter an IP-Adress: ")

    if(ipaddress!="localhost"):
        try:
            socket.inet_aton(ipaddress)
        except socket.error:
            print("Please enter a valid IP-Adress")
    break

commName = input("Enter a Community Name: ")


print(quicksnmp.get(ipaddress, ['1.3.6.1.2.1.1.5.0','1.3.6.1.2.1.1.4.0','1.3.6.1.2.1.1.3.0','1.3.6.1.2.1.1.1.0','.1.3.6.1.2.1.1.6.0'], hlapi.CommunityData(commName)))
