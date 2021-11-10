import socket
import threading

from DataOutput import *

HEADER = 2
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f">>>NEW CONNECTION {addr}")
    connected = True
    while connected:
        try:
            conn.settimeout(2)
            print(">>>LISTEN FOR MESSAGE")
            msg_length = conn.recv(HEADER).decode(FORMAT)
            print(">>>MESSAGE RECEIVED")
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == "DISCONNECT":
                    connected = False
                    print(f">>>[{addr}]: {msg}")
                else:
                    print(f">>>[{addr}]: ")
                    for i in range(8):
                        set_achannel(i + 1, int(msg[4 * i:4 * i + 4]))
                    for i in range(16):
                        set_dchannel(i + 1, int(msg[32 + 4 * i: 36 + 4 * i]))
                    print(">>>SENDING BACK ACK")
                    conn.send("ACK".encode(FORMAT))  #Sends ACK to transmitter
                #print(f">>>[{addr}]: {msg}")
        except socket.timeout:
            print(">>>TIMEOUT")
            set_achannel_off()  #Failsave nach 2 sekunden alle analoge channel auf 0
            #Funktion um alle Digitalen channel auf 0 zu setzten
        except socket.error:
            print(">>>ERROR")
            set_achannel_off()  #Failsave nach 2 sekunden alle analoge channel auf 0
            #Funktion um alle Digitalen channel auf 0 zu setzten

    conn.close()


def start():
    server.listen()  #Listen for connections
    print(f">>>SERVER IS LISTENING ON: {SERVER}")
    while True:
        conn, addr = server.accept()  #Accept incoming connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
    #handle_client(conn, addr)


if __name__ == "__main__":
    print(">>>SERVER STARTED")
    start()
