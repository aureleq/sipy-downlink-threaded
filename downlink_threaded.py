from network import Sigfox
import socket
import binascii
import time
import _thread

# sigfox threaded function to manage payload TX&RX
def th_send_sigfox(payload):
     # make the socket blocking
    s.setblocking(True)
    # Uplink + Downlink : Send then receive a reply from the network
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)
    output = s.send(payload)
    print("-- thread -- Message sent. Total size: ",  output,  " bytes")
    # response declared in global scope
    global response
    response = s.recv(8)


# init Sigfox for RCZ4
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
# set sigfox Network Emulator Public Key
sigfox.public_key(True)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

print('I am device ',  binascii.hexlify(sigfox.id()) )

message = bytes([0x48, 0x65, 0x6C,  0x6C, 0x6F, 0x20, 0x50, 0x79, 0x63, 0x6F, 0x6D, 0x21])
response = bytes()

# create new thread to manage message TX&RX
_thread.start_new_thread(th_send_sigfox,  (message, ))


print("Here we run our main tasks while waiting for sigfox tx and rx...")
# loop will run for 50 sec max and stop once downlink is received
for i in range (50):
    time.sleep(1)
    print(i, ' ', end='')
    if len(response) > 0:
        print('done!')
        print("Received downlink response: ",  binascii.hexlify(response))
        break
