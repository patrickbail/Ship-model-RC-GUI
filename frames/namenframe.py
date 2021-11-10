import tkinter as tk
from tkinter import *

FONT_SIZE = 12


class NameFrame(Frame):

    def __init__(self, master, data, senderframe, mixerframe, zuordframe):
        super().__init__(master)
        self.senderframe = senderframe
        self.mixerframe = mixerframe
        self.zuordframe = zuordframe
        self.main_data = data  #Data storage of all channels and mixers
        self.inputs_menu_var = StringVar()
        self.input_menu = self.filtered_keys()  #self.main_data.get_keys()
        self.inputs_menu_var.set(self.input_menu[0])
        self.chng_name_var = StringVar()

        self.frame1 = Frame(self)
        self.inputs_option = OptionMenu(self.frame1, self.inputs_menu_var, *self.input_menu)
        self.inputs_option.config(width=20, height=2, padx=5)

        self.initUI()

    def filtered_keys(self):
        vach_keys = self.main_data.get_keys("VACh")
        vdch_keys = self.main_data.get_keys("VDCh")
        all_keys = vach_keys + vdch_keys
        return all_keys

    def setup_input_menu(self):
        self.input_menu = self.filtered_keys()  #self.main_data.get_keys()
        self.inputs_menu_var.set(self.input_menu[0])

        self.inputs_option['menu'].delete(0, 'end')
        for option in self.input_menu:
            self.inputs_option['menu'].add_command(label=option, command=tk._setit(self.inputs_menu_var, option))

    def save_name(self):
        old_name = self.inputs_menu_var.get()  #Old name from Options menu
        new_name = self.chng_name_var.get()  #New name from Entry box
        tmp_data = self.main_data.get_data()
        if old_name in tmp_data['VACh'].keys():
            top_key = "VACh"
        else:
            top_key = "VDCh"
        #print(top_key)
        values = tmp_data[top_key].pop(old_name)  #Pop old key and return values
        #values[1] = new_name
        tmp_data[top_key][new_name] = values
        key_alias = tmp_data[top_key][new_name][1]  #Key alias for sender frame
        for key, values in tmp_data['Transmit'].items():  #Look for key appearance in Transmit
            if values[2]:
                if values[2] == old_name:
                    values[2] = new_name
        self.main_data.update_data(**tmp_data)  #Update main data
        self.setup_input_menu()  #Refresh Option menu with new names
        self.senderframe.change_name(key_alias, new_name)  #Change the name of the key in sender frame
        self.mixerframe.name_change(old_name, new_name)  #Change the name in Mixer inputs if present
        self.mixerframe.update_option_menus()  #Update option menus in mixer frame
        self.zuordframe.name_change(top_key, old_name, new_name)  #Update option menus in zuord frame
        #print(self.main_data.get_data())

    def initUI(self):
        #Frame 1
        Label(self.frame1, text="Inputs", font=(None, FONT_SIZE), padx=5).pack(side=LEFT)
        self.inputs_option.pack(side=LEFT, padx=72)

        #Frame 2
        frame2 = Frame(self)
        Label(frame2, text="Ändere Namen", font=(None, FONT_SIZE), padx=5).pack(side=LEFT)
        chng_name_entry = Entry(frame2, width=40, textvariable=self.chng_name_var)
        chng_name_entry.pack(side=LEFT, ipady=6, padx=10)

        self.frame1.pack(anchor=NW, pady=5)
        frame2.pack(anchor=NW, pady=5)
        Button(self, text="Speichern", font=(None, FONT_SIZE), width=20, height=2, command=self.save_name).pack(pady=10)
