import tkinter as tk
from tkinter import *

FONT_SIZE = 12


class MixerFrame(Frame):

    def __init__(self, master, data, zuordframe):
        super().__init__(master)
        self.zuordframe = zuordframe
        self.main_data = data  #Data storage of all channels and mixers
        self.on_image = PhotoImage(file="images/checkbox_on.png")
        self.off_image = PhotoImage(file="images/checkbox_off.png")
        self.mixers_exist = False  #Boolean var to secure that 'Mixer' key exist in data
        self.mixer_ui_updated = False  #Boolean var that check if current selected mixer UI is updated
        self.prev_sel_mixer = ""  #The previous selected mixer
        self.name_var = StringVar()
        self.mixer_sel_var = StringVar()
        self.mixer_menu = [""]
        self.e1_sel_var = StringVar()
        self.e2_sel_var = StringVar()
        self.e_menu = [""]
        self.e1_inv_var = BooleanVar()
        self.e2_inv_var = BooleanVar()
        self.e1_offset_var = IntVar()
        self.e2_offset_var = IntVar()
        self.e1_label = StringVar()
        self.e2_label = StringVar()
        self.method_sel_var = StringVar()
        self.method_sel_var.set("Add")
        self.end_value_label = IntVar()
        self.end_value = 0
        self.mixer_todo = []  #Mixer that have to be updated
        self.mixer_done = []  #Mixer that are updated
        self.update_data = {}  #data that currently stores the tmp_data for the recursive update mixer method
        # Init option menus
        self.mixer_sel_var.set("")
        self.e1_sel_var.set("")
        self.e2_sel_var.set("")
        self.frame1 = Frame(self)
        self.mixer_options = OptionMenu(self.frame1, self.mixer_sel_var, *self.mixer_menu)
        self.frame3 = Frame(self)
        self.eingang1_menu = OptionMenu(self.frame3, self.e1_sel_var, *self.e_menu)
        self.frame4 = Frame(self)
        self.eingang2_menu = OptionMenu(self.frame4, self.e2_sel_var, *self.e_menu)
        # Init option menus and UI
        self.update_option_menus()
        self.initUI()

    def calculate_input_val(self, input_val, inv, offset):
        new_input = input_val
        if inv:
            new_input = 4095 - input_val
        return new_input + offset

    def calculate_method(self, e1, e2, method):
        value = 0
        if method == "Add":
            value = e1 + e2
        elif method == "Multiply":
            value = e1 * e2
        elif method == "Subtract":
            value = e1 - e2
        elif method == "Average":
            value = int((e1 + e2) / 2)
        if value > 4095:
            value = 4095
        elif value < 0:
            value = 0
        return value

    def eval_topkey(self, dic, sub_key):
        if sub_key in dic["VACh"]:
            return "VACh"
        elif sub_key in dic["ACh"]:
            return "ACh"
        elif sub_key in dic["VDCh"]:
            return "VDCh"
        elif sub_key in dic["DCh"]:
            return "DCh"
        if self.mixers_exist:
            if sub_key in dic["Mixer"]:
                return "Mixer"

    def update_mixers(self):
        if self.mixers_exist:
            tmp_data = self.main_data.get_data()
            self.mixer_todo = list(tmp_data['Mixer'].keys())  #Mixer to calculate
            self.mixer_done = []  #Mixer that have been calculated
            self.update_data = tmp_data  #Updated data that will be dumped later after all Mixer have been updated
            #print("MIXER UPDATE START")
            self.update_mixers_vals()
            #print("MIXER UPDATE END")
            tmp_data = self.update_data
            self.update_data = {}
            #self.mixer_ui_updated = False
            self.main_data.update_data(**tmp_data)

    def update_mixers_vals(self):
        # Check if a mixer hasn't been updated
        # If a mixer hasn't been updated update it
        #print("Length mixer_todo: ", len(self.mixer_todo))
        #print("Length mixer_done: ", len(self.mixer_done))
        #print("Mixer_todo: ", self.mixer_todo)
        #print("Mixer_done: ", self.mixer_done)
        if len(self.mixer_todo) != 0:
            mixer_key = self.mixer_todo.pop(0)  #mixer_todo gets one smaller
            #print("Poped ", mixer_key)
            self.mixer_done.append(mixer_key)  #mixer_done gets one bigger
            e1_sub_key = self.update_data['Mixer'][mixer_key][1][0]
            e2_sub_key = self.update_data['Mixer'][mixer_key][2][0]
            e1_val = 0
            e2_val = 0
            top_key_e1 = self.eval_topkey(self.update_data, e1_sub_key)
            top_key_e2 = self.eval_topkey(self.update_data, e2_sub_key)
            #Input 1
            #print("E1 Sub key ", e1_sub_key)
            #print("E1 Top key", top_key_e1)
            if top_key_e1 == "Mixer":  #Is a mixer
                if e1_sub_key in self.mixer_done:  #If Mixer already calculated look up value
                    #print(e1_sub_key + " already has been calculated")
                    e1_val = self.update_data['Mixer'][e1_sub_key][0]
                    e1_val = self.calculate_input_val(e1_val, self.update_data['Mixer'][mixer_key][1][1],
                                                      self.update_data['Mixer'][mixer_key][1][2])  #val, inv, offset
                else:  #If mixer not calculated call recursive
                    #print(e1_sub_key + " has not been calculated")
                    for i in range(len(self.mixer_todo)):  #Search for mixer in mixer_todo to put in front
                        if e1_sub_key == self.mixer_todo[i]:
                            tmp = self.mixer_todo[0]
                            self.mixer_todo[0] = self.mixer_todo[i]
                            self.mixer_todo[i] = tmp
                            break
                    #print("Recursive call")
                    self.update_mixers_vals()  #Recursive call
                    #print("End Recursive call")
                    e1_val = self.update_data['Mixer'][e1_sub_key][0]
                    e1_val = self.calculate_input_val(e1_val, self.update_data['Mixer'][mixer_key][1][1],
                                                      self.update_data['Mixer'][mixer_key][1][2])  #val, inv, offset
            else:  #Not a Mixer
                e1_val = self.update_data[top_key_e1][e1_sub_key][0]
                e1_val = self.calculate_input_val(e1_val, self.update_data['Mixer'][mixer_key][1][1],
                                                  self.update_data['Mixer'][mixer_key][1][2])  #val, inv, offset
            #print("E1 Val: ", e1_val)

            #print("E2 Sub key ", e2_sub_key)
            #print("E2 Top key", top_key_e2)
            # Input 2
            if top_key_e2 == "Mixer":  #Is a mixer
                if e2_sub_key in self.mixer_done:  #If Mixer already calculated look up value
                    #print(e2_sub_key + " already has been calculated")
                    e2_val = self.update_data['Mixer'][e2_sub_key][0]
                    e2_val = self.calculate_input_val(e2_val, self.update_data['Mixer'][mixer_key][2][1],
                                                      self.update_data['Mixer'][mixer_key][2][2])  #val, inv, offset
                else:  #If mixer not calculated call recursive
                    #print(e2_sub_key + " has not been calculated")
                    for i in range(len(self.mixer_todo)):  #Search for mixer in mixer_todo to put in front
                        if e2_sub_key == self.mixer_todo[i]:
                            tmp = self.mixer_todo[0]
                            self.mixer_todo[0] = self.mixer_todo[i]
                            self.mixer_todo[i] = tmp
                            break
                    #print("Recursive call")
                    self.update_mixers_vals()  #Recursive call
                    #print("End Recursive call")
                    e2_val = self.update_data['Mixer'][e2_sub_key][0]
                    e2_val = self.calculate_input_val(e2_val, self.update_data['Mixer'][mixer_key][2][1],
                                                      self.update_data['Mixer'][mixer_key][2][2])  #val, inv, offset
            else:
                e2_val = self.update_data[top_key_e2][e2_sub_key][0]
                e2_val = self.calculate_input_val(e2_val, self.update_data['Mixer'][mixer_key][2][1],
                                                  self.update_data['Mixer'][mixer_key][2][2])  #val, inv, offset
            #print("E2 Val: ", e1_val)

            #Update Mixer value with corresponding method
            self.update_data["Mixer"][mixer_key][0] = self.calculate_method(e1_val, e2_val,
                                                                            self.update_data['Mixer'][mixer_key][3])
            #Issue: If you select new mixer you can not choose previous selected mixer as option for input
            #Update GUI for selected Mixer
            if mixer_key == self.mixer_sel_var.get():
                if mixer_key != self.prev_sel_mixer:  #If previous selected mixer is unequal to current fresh update
                    #print("Current selected Mixer ", mixer_key, " is unequal with Previous selected Mixer ", self.prev_sel_mixer)
                    self.mixer_ui_updated = False
                    self.prev_sel_mixer = mixer_key
                self.update_current_mixer_ui(mixer_key, e1_sub_key, e2_sub_key, e1_val, e2_val)
            self.update_mixers_vals()

    def update_current_mixer_ui(self, mixer_key, e1_sub_key, e2_sub_key, e1_val, e2_val):
        #print("Mixer " + mixer_key + " is on the GUI")
        if not self.mixer_ui_updated:  #Update only once on selection
            self.mixer_ui_updated = True
            self.update_option_menus()  #Update option menus
            self.mixer_sel_var.set(mixer_key)
            self.name_var.set(mixer_key)
            self.e1_sel_var.set(e1_sub_key)
            self.e2_sel_var.set(e2_sub_key)
            self.e1_inv_var.set(self.update_data['Mixer'][mixer_key][1][1])
            self.e2_inv_var.set(self.update_data['Mixer'][mixer_key][2][1])
            self.e1_offset_var.set(self.update_data['Mixer'][mixer_key][1][2])
            self.e2_offset_var.set(self.update_data['Mixer'][mixer_key][2][2])
            self.method_sel_var.set(self.update_data['Mixer'][mixer_key][3])
        #Always update labels
        self.e1_label.set("Wert: " + str(e1_val))
        self.e2_label.set("Wert: " + str(e2_val))
        self.end_value = self.update_data['Mixer'][mixer_key][0]
        self.end_value_label.set("Wert: " + str(self.end_value))

    def new_mixer(self):  #Sets selected Mixer to emtpy string
        self.mixer_sel_var.set("")
        self.prev_sel_mixer = ""
        self.update_option_menus()

    def name_change(self, old_name, new_name):
        if self.mixers_exist:
            tmp_data = self.main_data.get_data()
            for key, values in tmp_data['Mixer'].items():
                if values[1][0] == old_name:
                    values[1][0] = new_name
                if values[2][0] == old_name:
                    values[2][0] = new_name
            self.main_data.update_data(**tmp_data)

    def save_mixer_settings(self):
        tmp_data = self.main_data.get_data()
        mixer_dict = {}
        if self.mixers_exist:  #If mixer profiles exist get the dictionary
            mixer_dict = tmp_data['Mixer']
        if self.mixer_sel_var.get() != "":  #Delete Selected mixer
            mixer_dict.pop(self.mixer_sel_var.get())
        old_name = self.mixer_sel_var.get()
        key = self.name_var.get()
        e1 = [self.e1_sel_var.get(), self.e1_inv_var.get(), self.e1_offset_var.get()]
        e2 = [self.e2_sel_var.get(), self.e2_inv_var.get(), self.e2_offset_var.get()]
        mixer_dict[key] = [self.end_value, e1, e2, self.method_sel_var.get()]
        for mixer_key, values in mixer_dict.items():  #Check if old_name is in other Mixer Profiles and change to new one
            if mixer_key != key:
                if values[1][0] == old_name:
                    values[1][0] = key
                if values[2][0] == old_name:
                    values[2][0] = key
        tmp_data['Mixer'] = mixer_dict
        # Get all the keys to update the menus
        menu_keys_list = []
        mixer_key_list = []
        for top_key in tmp_data.keys():
            menu_keys_list = menu_keys_list + list(tmp_data[top_key].keys())
            if top_key == "Mixer":
                mixer_key_list = mixer_key_list + list(tmp_data[top_key].keys())
        self.mixer_menu = mixer_key_list
        self.e_menu = menu_keys_list
        self.update_option_menus()  #Update option menus
        self.mixers_exist = True  #A Mixer exist now
        self.main_data.update_data(**tmp_data)  #Dump back all the data into the json
        #print(">>> NAME CHANGE OF MIXER IN ZUORD")
        self.zuordframe.name_change("Mixer", old_name, key)
        #print(">>> END OF NAME CHANGE OF MIXER IN ZUORD")

    def set_menus(self):
        tmp_data = self.main_data.get_data()
        if "Mixer" in tmp_data.keys():  #Mixer Profiles exist load them
            self.mixers_exist = True
            self.mixer_menu = self.main_data.get_keys("Mixer")
            if self.mixer_sel_var.get() != "":
                self.mixer_sel_var.set(self.mixer_menu[0])
        vach_keys = self.main_data.get_keys("VACh")
        ach_keys = self.main_data.get_keys("ACh")
        vdch_keys = self.main_data.get_keys("VDCh")
        dch_keys = self.main_data.get_keys("DCh")
        self.e_menu = self.mixer_menu + vach_keys + ach_keys + vdch_keys + dch_keys  #Concat all keys for menu

    def update_option_menus(self):
        self.set_menus()
        self.mixer_options['menu'].delete(0, 'end')
        self.eingang1_menu['menu'].delete(0, 'end')
        self.eingang2_menu['menu'].delete(0, 'end')

        #self.mixer_sel_var.set(self.mixer_menu[0])
        self.e1_sel_var.set(self.e_menu[0])
        self.e2_sel_var.set(self.e_menu[0])

        for option in self.mixer_menu:
            self.mixer_options['menu'].add_command(label=option, command=tk._setit(self.mixer_sel_var, option))
        for option in self.e_menu:
            if option != self.prev_sel_mixer:
                self.eingang1_menu['menu'].add_command(label=option, command=tk._setit(self.e1_sel_var, option))
                self.eingang2_menu['menu'].add_command(label=option, command=tk._setit(self.e2_sel_var, option))

    def initUI(self):
        #Frame 1
        Label(self.frame1, text="Mixer", font=(None, FONT_SIZE), padx=2).pack(side=LEFT)
        self.mixer_options.config(width=20, height=2)
        self.mixer_options.pack(side=LEFT, padx=12)
        neu_btn = Button(self.frame1, text="Neu", font=(None, FONT_SIZE), width=10, command=self.new_mixer)
        neu_btn.pack(side=LEFT, padx=40)
        save_btn = Button(self.frame1, text="Speichern", font=(None, FONT_SIZE), padx=5, command=self.save_mixer_settings)
        save_btn.pack(side=LEFT)

        #Frame 2
        frame2 = Frame(self, pady=10)
        Label(frame2, text="Name", font=(None, FONT_SIZE), padx=2).pack(side=LEFT)
        name_entry = Entry(frame2, width=40, textvariable=self.name_var)
        name_entry.pack(side=LEFT, ipady=6, padx=10)

        #Frame 3
        Label(self.frame3, text="Eingang 1", font=(None, FONT_SIZE), padx=2).pack(side=LEFT)
        self.eingang1_menu.config(width=20, height=2)
        self.eingang1_menu.pack(side=LEFT, padx=10)
        ch_frame = Frame(self.frame3)
        eingang1_inv = Checkbutton(ch_frame, variable=self.e1_inv_var, image=self.off_image, selectimage=self.on_image,
                                   indicatoron=False, onvalue=True, offvalue=False)
        eingang1_inv.pack(side=LEFT)
        Label(ch_frame, text="Inv", font=(None, FONT_SIZE)).pack(side=LEFT, padx=2)
        ch_frame.pack(side=LEFT, padx=10)
        Label(self.frame3, text="Offset", font=(None, FONT_SIZE)).pack(side=LEFT, padx=2)
        e1_offset_entry = Entry(self.frame3, textvariable=self.e1_offset_var)
        e1_offset_entry.pack(side=LEFT, padx=10, ipady=6)
        Label(self.frame3, textvariable=self.e1_label, font=(None, FONT_SIZE)).pack(side=LEFT)

        #Frame 4
        Label(self.frame4, text="Eingang 2", font=(None, FONT_SIZE), padx=2).pack(side=LEFT)
        self.eingang2_menu.config(width=20, height=2)
        self.eingang2_menu.pack(side=LEFT, padx=10)
        ch_frame = Frame(self.frame4)
        eingang2_inv = Checkbutton(ch_frame, variable=self.e2_inv_var, image=self.off_image, selectimage=self.on_image,
                                   indicatoron=False, onvalue=True, offvalue=False)
        eingang2_inv.pack(side=LEFT)
        Label(ch_frame, text="Inv", font=(None, FONT_SIZE)).pack(side=LEFT, padx=2)
        ch_frame.pack(side=LEFT, padx=10)
        Label(self.frame4, text="Offset", font=(None, FONT_SIZE)).pack(side=LEFT, padx=2)
        e2_offset_entry = Entry(self.frame4, textvariable=self.e2_offset_var)
        e2_offset_entry.pack(side=LEFT, padx=10, ipady=6)
        Label(self.frame4, textvariable=self.e2_label, font=(None, FONT_SIZE)).pack(side=LEFT)

        #Frame 5
        frame5 = Frame(self)
        Label(frame5, text="Methode", font=(None, FONT_SIZE), padx=2).pack(side=LEFT)
        methode_menu = OptionMenu(frame5, self.method_sel_var, "Add", "Subtract", "Multiply", "Average")
        methode_menu.config(width=20, height=2)
        methode_menu.pack(side=LEFT, padx=18)

        #Frame 6
        frame6 = Frame(self)
        Label(frame6, textvariable=self.end_value_label, font=(None, FONT_SIZE)).pack(side=LEFT)

        self.frame1.pack(anchor=NW, pady=5)
        frame2.pack(anchor=NW, pady=5)
        self.frame3.pack(anchor=NW, pady=5)
        self.frame4.pack(anchor=NW, pady=5)
        frame5.pack(anchor=NW, pady=5)
        frame6.pack(anchor=NW, pady=5)
        #self.master.pack(anchor=NW, fill=BOTH)
