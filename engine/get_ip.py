import socket, sys    



""" def getRaspiAdd():
    address = sockpytet.gethostbyname("raspberrypi.mshome.net")
    return address
 """
hostname = socket.gethostname()   
IPAddr = socket.gethostbyname(hostname)    
#print("Your Computer Name is:" + hostname)    
IPAddr = str(IPAddr)
print(IPAddr) 
sys.stdout.flush()