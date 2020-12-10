from pysnmp.hlapi import *
import ipaddress
from threading import Thread
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv


def get(target, oid, credentials, threaded=False):          #Default getter function. threaded is used to indentify if called by thread or not
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(credentials),
        UdpTransportTarget((target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication and threaded==False:
        print(errorIndication)                              #if function is called by a thread, no error output (usually just full of "No SNMP response received")

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:        
        for varBind in varBinds:                                            
            if threaded:                                                #if function called by thread, print IP before information
                print(target+":", end="")
            print(' = '.join([x.prettyPrint() for x in varBind]))       


def iterateIP(network):                #goes through all ip's in network to check for a SNMP response           #TODO: Get multiple OIDs instead of just one
    oid = "1.3.6.1.2.1.1.5.0"
    thread = Null
    for ip in ipaddress.IPv4Network(network):                                       #Goes through each IP in network, executes thread with get for each
        thread = Thread(target = get, args = (str(ip), oid, "public", True))
        thread.start()
    if thread != Null:                                                              #Makes sure last thread is finished
        thread.join()  
        
def receiveTraps():                                                                 #checks for incoming traps
    snmpEngine = SnmpEngine()
    TrapAgentAddress='localhost'; 
    Port=162;                                              

    print("Now listening for Trap on "+TrapAgentAddress+":"+str(Port)+"...\n");
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
    )

    config.addV1System(snmpEngine, 'community', 'public')

    def trapOutput(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
        print("Received new Trap message");
        for name, val in varBinds:                                              #iterates through each received oid pair
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))          #pretty Print to make it readable
        return

    ntfrcv.NotificationReceiver(snmpEngine, trapOutput)

    snmpEngine.transportDispatcher.jobStarted(1)  
    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise