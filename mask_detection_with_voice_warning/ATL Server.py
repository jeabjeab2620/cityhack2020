from gtts import gTTS
from playsound import playsound
import socket
import time

proper = "Please wear the mask properly"
wear = "Please wear your mask"
good = "Good to proceed"
far = "Please Stay Far Away"
language = 'en'

t2sp = gTTS(text=proper, lang=language,slow=False)
t2sw = gTTS(text=wear, lang=language,slow=False)
t2sg = gTTS(text=good, lang=language,slow=False)
t2sf = gTTS(text=far,lang=language,slow=False)
t2sp.save("proper.mp3")
t2sw.save("wear.mp3")
t2sg.save("good.mp3")
t2sf.save("far.mp3")

localIP     = "192.168.1.22"

localPort   = 20001
bufferSize  = 1024

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

 

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams
sleep = False;
i = 0;
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0].decode("utf-8")
    address = bytesAddressPair[1]
    if i % 50 == 0:
        if(message == "too_close"):
            playsound("far.mp3")
        else:
            if(message =="without_mask"):
                playsound("wear.mp3")
                
            if(message =="mask_weared_incorrect"):
                playsound("proper.mp3")
            if(message == "with_mask"):
                playsound("good.mp3")
        
            
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    i += 1
    print(clientMsg)
    print(clientIP)

