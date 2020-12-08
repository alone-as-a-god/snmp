from pysnmp import hlapi
import quicksnmp
import socket
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import keyboard
import os
import time

menuLogo = ".-./`)    .-'''-. .---.  .---..-./`) .-------.    .-'''-.            .-'''-. ,---.   .--.,---.    ,---..-------.  \n\\ .-.')  / _     \\|   |  |_ _|\\ .-.')\\  _(`)_ \\  / _     \\          / _     \\|    \\  |  ||    \\  /    |\\  _(`)_ \\ \n/ `-' \\ (`' )/`--'|   |  ( ' )/ `-' \\| (_ o._)| (`' )/`--'         (`' )/`--'|  ,  \\ |  ||  ,  \\/  ,  || (_ o._)| \n `-'`\"`(_ o _).   |   '-(_{;}_)`-'`\"`|  (_,_) /(_ o _).           (_ o _).   |  |\\_ \\|  ||  |\\_   /|  ||  (_,_) / \n .---.  (_,_). '. |      (_,_) .---. |   '-.-'  (_,_). '.          (_,_). '. |  _( )_\\  ||  _( )_/ |  ||   '-.-'  \n |   | .---.  \\  :| _ _--.   | |   | |   |     .---.  \\  :        .---.  \\  :| (_ o _)  || (_ o _) |  ||   |      \n |   | \\    `-'  ||( ' ) |   | |   | |   |     \\    `-'  |        \\    `-'  ||  (_,_)\\  ||  (_,_)  |  ||   |      \n |   |  \\       / (_{;}_)|   | |   | /   )      \\       /          \\       / |  |    |  ||  |      |  |/   )      \n '---'   `-...-'  '(_,_) '---' '---' `---'       `-...-'            `-...-'  '--'    '--''--'      '--'`---'      "

def cls():                                              #checks if os is linux or windows, creates a corresponding clear command
    os.system('cls' if os.name=='nt' else 'clear')

def receiveTraps():                                         #todo: function doesn't work when located in quicksnmp file
    snmpEngine = engine.SnmpEngine()
    TrapAgentAddress='localhost'; 
    Port=162;                                               #162 is default, since iReasoning uses the same default port

    print("Now listening for Trap on "+TrapAgentAddress+":"+str(Port));
    print('--------------------------------------------------------------------------');
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
    )

    #Configure community here
    config.addV1System(snmpEngine, 'my-area', 'public')

    def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
            varBinds, cbCtx):
        print("Received new Trap message");
        for name, val in varBinds:                                              #iterates through each received oid pair
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))          #pretty Print to make it readable
        return

    ntfrcv.NotificationReceiver(snmpEngine, cbFun)

    snmpEngine.transportDispatcher.jobStarted(1)  
    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise

#1.3.6.1.2.1.1.4.0 = sysContact
#1.3.6.1.2.1.1.5.0 = sysName
#1.3.6.1.2.1.1.3.0 = upTime
#1.3.6.1.2.1.1.1.0 = sysDescr
#1.3.6.1.2.1.1.6.0 = sysLocation

while True:
    cls()
    print(menuLogo+"\n\n")

    cmd = input("Enter a command: ")
    if(cmd=="/help"):
        print("Welcome to iShips SNMP™")
        print("Your current version supports the following commands:")
        print("/help - Displays the current message")
        print("/get - Gives you the option to input IP, Port and CommunityData to read out information via SNMP")
        print("/receive - Starts a SNMP Trap Listener which checks and reads incoming Traps. Be aware that after executing this command, you cannot go back unless you close this program and restart it again")
        print("If you are finished with reading this, please press ENTER to return to the main menu")
        while True:
            if(keyboard.is_pressed("enter")):
                
                cls()
                break
    elif(cmd=="/receive"):
        receiveTraps()
    elif(cmd=="/get"):
        while True:
            ipaddress = input("Enter an IP-Adress: ")

            if(ipaddress!="localhost"):                     #checks if valid ip address was entered
                try:
                    socket.inet_aton(ipaddress)
                except socket.error:
                    print("Please enter a valid IP-Adress")
            break

        commName = input("Enter a Community Name: ")
        print(quicksnmp.get(ipaddress, ['1.3.6.1.2.1.1.5.0','1.3.6.1.2.1.1.4.0','1.3.6.1.2.1.1.3.0','1.3.6.1.2.1.1.1.0','.1.3.6.1.2.1.1.6.0'], hlapi.CommunityData(commName)))

    elif(cmd=="/set"):
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

