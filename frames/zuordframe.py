import tkinter as tk
from tkinter import *

FONT_SIZE = 12


class ZurodFrame(Frame):

    def __init__(self, master, data):
        super().__init__(master)
        self.main_data = data  #Data storage of all channels and mixers
        self.pwm_options = []  #Array of all keys for pwm
        self.dch_options = []  #Array of all keys for dch
        self.pwm_menus = []  #Array of all pwm options menu objects
        self.pwm_vars = []  #Array of all variables for pwm option menu objects
        self.d_menus = []  #Array of all dch options menu objects
        self.d_vars = []  #Array of all variables for dch option menu objects
        #Init something
        self.set_menus()
        self.initUI()
        self.update_option_menus()

    def set_menus(self):
        tmp_data = self.main_data.get_data()
        mixer_keys = []
        if "Mixer" in tmp_data.keys():  #If Mixer Profiles exist load them
            mixer_keys = self.main_data.get_keys("Mixer")
        vach_keys = self.main_data.get_keys("VACh")
        ach_keys = self.main_data.get_keys("ACh")
        vdch_keys = self.main_data.get_keys("VDCh")
        dch_keys = self.main_data.get_keys("DCh")
        self.pwm_options = mixer_keys + vach_keys + ach_keys  #Concat all keys from mixer,VACh and ACh for pwm menu
        self.dch_options = vdch_keys + dch_keys  #Concat all keys from VDCh and DCh for dch menu

    def update_option_menus(self):
        self.set_menus()
        tmp_data = self.main_data.get_data()
        #Delte current menus in options
        for menu in self.pwm_menus:
            menu['menu'].delete(0, 'end')
        for menu in self.d_menus:
            menu['menu'].delete(0, 'end')
        #Set the selected vars according to data in json
        for i in range(8):
            to_set = ""
            if tmp_data['Transmit']['PWM' + str(i + 1)][2]:  #Check if not None
                to_set = tmp_data['Transmit']['PWM' + str(i + 1)][2]
            self.pwm_vars[i].set(to_set)
        for i in range(16):
            to_set = ""
            nbr = str(i + 1)
            if len(nbr) == 1:
                nbr = "0" + nbr
            if tmp_data['Transmit']['D' + nbr][2]:  #Check if not None
                to_set = tmp_data['Transmit']['D' + nbr][2]
            self.d_vars[i].set(to_set)
        #Set up the options in ever options menu
        for option in self.pwm_options:  #For every option in pwm_options
            for i in range(8):  #For every pwm menu add option
                self.pwm_menus[i]['menu'].add_command(label=option, command=tk._setit(self.pwm_vars[i], option))
        for option in self.dch_options:  #For every option in dch_options
            for i in range(16):  #For every dch menu add option
                self.d_menus[i]['menu'].add_command(label=option, command=tk._setit(self.d_vars[i], option))

    def name_change(self, top_key, old_name, new_name):
        #print(">>>Topkey ", top_key)
        #print(">>>Old name ", old_name)
        #print(">>>New name ", new_name)
        tmp_data = self.main_data.get_data()
        for key, values in tmp_data['Transmit'].items():  #Search for top_key and old_name if they are in Transmit
            if values[1] == top_key and values[2] == old_name:
                values[2] = new_name
                self.main_data.update_data(**tmp_data)  #Dump back data
                break
        self.update_option_menus()  #Update option menus

    def eval_topkey(self, dic, sub_key):
        if sub_key in dic["VACh"]:
            return "VACh"
        elif sub_key in dic["ACh"]:
            return "ACh"
        elif sub_key in dic["VDCh"]:
            return "VDCh"
        elif sub_key in dic["DCh"]:
            return "DCh"
        if "Mixer" in dic:
            if sub_key in dic["Mixer"]:
                return "Mixer"

    def save_transmit_settings(self):
        tmp_data = self.main_data.get_data()
        #print(">>>SAVING TRANSMIT DATA")
        for i in range(8):
            sub_key = self.pwm_vars[i].get()
            if sub_key:
                top_key = self.eval_topkey(tmp_data, sub_key)
                value = tmp_data[top_key][sub_key][0]
                tmp_data['Transmit']['PWM' + str(i + 1)] = [value, top_key, sub_key]
        for i in range(16):
            sub_key = self.d_vars[i].get()
            if sub_key:
                top_key = self.eval_topkey(tmp_data, sub_key)
                #print("Topkey ", top_key)
                #print("Subkey ", sub_key)
                value = tmp_data[top_key][sub_key][0]
                nbr = str(i + 1)
                if len(nbr) == 1:
                    nbr = "0" + nbr
                tmp_data['Transmit']['D' + nbr] = [value, top_key, sub_key]
        #print(">>>END OF SAVING TRANSMIT DATA")

    def update_transmit_values(self):
        #print(">>>UPDATING TRANSMIT DATA")
        tmp_data = self.main_data.get_data()
        for key, values in tmp_data['Transmit'].items():
            if values[2]:
                try:
                    values[0] = tmp_data[values[1]][values[2]][0]
                except:
                    values[0] = values[0]
        self.main_data.update_data(**tmp_data)
        #print(">>>END OF UPDATING TRANSMIT DATA")

    def initUI(self):

        grid = Frame(self)

        i = 1
        #pwm_option_0 = self.pwm_options[0]
        #dch_option_0 = self.dch_options[0]
        for row in range(8):
            Label(grid, text="PWM" + str(row + 1), font=(None, FONT_SIZE), padx=5).grid(row=row, column=0, padx=5)
            self.pwm_vars.append(StringVar())
            self.pwm_vars[row].set("")
            self.pwm_menus.append(OptionMenu(grid, self.pwm_vars[row], *self.pwm_options))
            self.pwm_menus[row].config(width=20, height=2, padx=5)
            self.pwm_menus[row].grid(row=row, column=1, padx=10)

            Label(grid, text="D" + str(i), font=(None, FONT_SIZE), padx=5).grid(row=row, column=2, padx=5)
            self.d_vars.append(StringVar())
            self.d_vars[len(self.d_vars) - 1].set("")
            self.d_menus.append(OptionMenu(grid, self.d_vars[len(self.d_vars) - 1], *self.dch_options))
            self.d_menus[len(self.d_vars) - 1].config(width=20, height=2, padx=5)
            self.d_menus[len(self.d_vars) - 1].grid(row=row, column=3, padx=10)
            i += 1

            Label(grid, text="D" + str(i), font=(None, FONT_SIZE), padx=5).grid(row=row, column=4, padx=5)
            self.d_vars.append(StringVar())
            self.d_vars[len(self.d_vars) - 1].set("")
            self.d_menus.append(OptionMenu(grid, self.d_vars[len(self.d_vars) - 1], *self.dch_options))
            self.d_menus[len(self.d_vars) - 1].config(width=20, height=2, padx=5)
            self.d_menus[len(self.d_vars) - 1].grid(row=row, column=5, padx=10)
            i += 1

        grid.pack(pady=10)
        Button(self, text="Speichern", font=(None, FONT_SIZE), width=20, command=self.save_transmit_settings).pack(
            anchor=W, ipady=5)
