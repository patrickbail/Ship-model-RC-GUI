import time
import socket
import threading

from tkinter import *
from model.data import DataClass
from frames.senderframe import SenderFrame
from frames.namenframe import NameFrame
from frames.mixerframe import MixerFrame
from frames.kalibframe import KalibFrame
from frames.zuordframe import ZurodFrame

from DataInput import *

FONT_SIZE = 12
HEADER = 2
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())  #Hier IPv4 Adresse des Empfänger Pis hinschreiben
ADDR = (SERVER, PORT)
CLOSED = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #TCP as Transport protocol
client.connect(ADDR)

root = Tk()
root.title("Ship model RC GUI")
root.geometry("800x480")
root.resizable(False, False)

main_data = DataClass()
#print(main_data.data)
bottom_frame = Frame(root)


def change_bottom_frame(sel_frame):
    sel_frame.tkraise()


sender_frame = SenderFrame(bottom_frame, main_data)
kalib_frame = KalibFrame(bottom_frame, main_data)
zuord_frame = ZurodFrame(bottom_frame, main_data)
mixer_frame = MixerFrame(bottom_frame, main_data, zuord_frame)
name_frame = NameFrame(bottom_frame, main_data, sender_frame, mixer_frame, zuord_frame)

for frame in (sender_frame, kalib_frame, mixer_frame, zuord_frame, name_frame):
    frame.grid(row=0, column=0, sticky="nsew")
sender_frame.tkraise()

#Topframe
top_frame = Frame(root)
sender_btn = Button(top_frame, text="Sender", font=(None, FONT_SIZE),
                    padx=40, pady=10, command=lambda: change_bottom_frame(sender_frame))
mixer_btn = Button(top_frame, text="Mixer", font=(None, FONT_SIZE),
                   padx=40, pady=10, command=lambda: change_bottom_frame(mixer_frame))
namen_btn = Button(top_frame, text="Namen", font=(None, FONT_SIZE),
                   padx=40, pady=10, command=lambda: change_bottom_frame(name_frame))
kalib_btn = Button(top_frame, text="Kalibrierung", font=(None, FONT_SIZE),
                   padx=40, pady=10, command=lambda: change_bottom_frame(kalib_frame))
zuord_btn = Button(top_frame, text="Zuordnung", font=(None, FONT_SIZE),
                   padx=40, pady=10, command=lambda: change_bottom_frame(zuord_frame))
sender_btn.pack(side=LEFT)
mixer_btn.pack(side=LEFT)
namen_btn.pack(side=LEFT)
kalib_btn.pack(side=LEFT)
zuord_btn.pack(side=LEFT)

#Init UI
top_frame.pack(side=TOP, fill=BOTH)
bottom_frame.pack(side=BOTTOM, fill=BOTH)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def send_data_to_server():
    while not CLOSED:
        #print(">>>TRANSMITTING DATA")
        transmit_dic = main_data.data['Transmit']
        transmit_data = ""
        for key, values in transmit_dic.items():  #Add Transmit values to string
            if not values[0]:  #If None
                transmit_data = transmit_data + "0000"
            elif len(str(values[0])) < 4:  #If int value has not 4 digits fill it with 0
                transmit_value = str(values[0])
                for i in range(4 - len(transmit_value)):
                    transmit_value = "0" + transmit_value
                transmit_data = transmit_data + transmit_value
            else:
                transmit_data = transmit_data + str(values[0])
        send(transmit_data)  #Send data to receiver
        t0 = time.perf_counter()
        client.settimeout(2)
        try:
            ack = client.recv(3).decode(FORMAT)  #Wait for ACK
            if ack == "ACK":
                #print(f">>>{ack}")
                status = "Connected"
            else:
                status = "Package lost"
        except socket.timeout:
            print(">>>TIMEOUT")
            status = "Timeout"
        except socket.error:
            print(">>>ERROR")
            status = "Error"
        t1 = time.perf_counter() - t0
        #print(f">>>TIME ELAPSED {t1}")
        #sender_frame.set_conn_status(t1, status)
        DataClass.status = status
        DataClass.time = str(t1)[:6]
        time.sleep(0.05)  #Every 5ms
    print(">>>CONNECTION CLOSED NOT TRANSMITTING DATA ANYMORE")


thread = threading.Thread(target=send_data_to_server)  #Thread for sending data to receiver
thread.start()

if __name__ == "__main__":
    #root.mainloop()
    #Main GUI Loop
    try:
        while True:
            #t0 = time.clock()
            main_data.set_achannel_data(*get_achannel())  #Hier achannel daten sammeln
            main_data.set_dchannel_data(*get_dchannel())  #Hier dchannel daten sammeln
            kalib_frame.update_ach_values()  #Updates and calculates all ACh values with corresponding calibrations
            sender_frame.update_ach_vars()  #Updates ACh label variables in sender frame
            sender_frame.update_dch_background()  #Update DCh label background
            mixer_frame.update_mixers()  #Update Mixer values
            zuord_frame.update_transmit_values()  #Update Transmit values
            sender_frame.set_conn_status(main_data.time, main_data.status)  #Show current connection status
            main_data.update_json()
            #Transmit values to receiver
            root.update_idletasks()
            root.update()
            #time.sleep(0.047)
            #t1 = time.clock() - t0
            #print(f">>>TIME ELAPSED: {t1}")
    finally:
        print(">>>DISCONNECTING")
        CLOSED = True
        send("DISCONNECT")
