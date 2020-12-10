from pysnmp import hlapi
import quicksnmp
import socket
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import keyboard
import os
import time
from threading import Thread

#for i in range (10):
#    thread = Thread(target = quicksnmp.threadFunction, args=(str(i)))
 #   thread.start()
    
#print("Finsied")

