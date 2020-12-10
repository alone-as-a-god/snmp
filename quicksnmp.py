from pysnmp.hlapi import *
import ipaddress
from time import sleep
from threading import Thread
import concurrent.futures


def get(target, oid, credentials, threaded=False):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(credentials),
        UdpTransportTarget((target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication and threaded==False:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        
        for varBind in varBinds:
            if threaded:
                print(target+":", end="")
            print(' = '.join([x.prettyPrint() for x in varBind]))







def iterateIP(network):                #goes through all ip's in network to check for a SNMP response
    oid = "1.3.6.1.2.1.1.5.0"
    thread = Null
    for ip in ipaddress.IPv4Network(network):
        
        #print(ip) 
        thread = Thread(target = get, args = (str(ip), oid, "public", True))
        thread.start()
    if thread != Null:
        thread.join()  
        
    
    

           
    
        
def threadFunction(arg):
    print("Hü"+str(arg))
    sleep(3)
    print("fertig"+arg)
    
#iterateIP("192.168.188.0/24")

#get("192.168.188.28", "1.3.6.1.2.1.1.5.0", "public")
#get("192.168.188.29", "1.3.6.1.2.1.1.5.0", "public")