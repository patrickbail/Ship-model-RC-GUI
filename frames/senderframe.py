from tkinter import *

FONT_SIZE = 12


class SenderFrame(Frame):

    def __init__(self, master, data):
        super().__init__(master)
        self.on_image = PhotoImage(file="images/checkbox_on.png")
        self.off_image = PhotoImage(file="images/checkbox_off.png")
        self.main_data = data  # Data storage of all channels and mixers
        self.vdch_vars = {}  # Dictionary for VDChannels
        self.vach_vars = {}  # Dictionary for VAChannels
        self.ach_vars = []
        self.dch_labels = []
        self.conn_status_var = StringVar()
        self.conn_time_var = StringVar()
        self.init_data()  # Init dictionary data
        self.initUI()  # Init UI

    def init_data(self):
        #print("INIT DATA FROM SENDER")
        # Init VDCh dictionary
        for i in range(4):
            for j in range(4):
                self.vdch_vars['VDCh' + str(4 * i + j + 1)] = [IntVar(), StringVar()]
        # Init VACh dictionary and ACh label variables
        for i in range(8):
            self.vach_vars['VACh' + str(i + 1)] = [IntVar(), StringVar()]  #Init VACh dictionary
            self.ach_vars.append(StringVar())  #Init ACh label vars
        # Get saved data from json and set values
        tmp_data = self.main_data.get_data()
        # Get all VACh keys and values
        for key, values in tmp_data['VACh'].items():
            self.vach_vars[values[1]][0].set(values[0])  # Init int value
            self.vach_vars[values[1]][1].set(key)  # Init str value for Label
        # Get all VDCh keys and values
        for key, values in tmp_data['VDCh'].items():
            self.vdch_vars[values[1]][0].set(values[0])  # Init int value
            self.vdch_vars[values[1]][1].set(key)  # Init str value for Label
        # Get all ACh values
        for key, values in tmp_data['ACh'].items():
            self.ach_vars[int(key[len(key) - 1]) - 1].set(key + ": " + str(values[0]))

    def update_ach_vars(self):
        tmp_data = self.main_data.get_data()
        for key, values in tmp_data['ACh'].items():
            self.ach_vars[int(key[len(key) - 1]) - 1].set(key + ": " + str(values[0]))

    def update_dch_background(self):
        tmp_data = self.main_data.get_data()
        for i in range(16):
            nbr = str(i + 1)
            if len(nbr) == 1:
                nbr = "0" + nbr
            if tmp_data['DCh']['D' + nbr][0] == 0:
                self.dch_labels[i].config(bg="#f0f0f0")
            else:
                self.dch_labels[i].config(bg="#ff0000")

    def change_name(self, key, new_name):  # Change str value not key
        #print("NAME CHANGE")
        #print(key)
        #print(new_name)
        if key in self.vdch_vars.keys():  # If old name in VDCh dictionary
            self.vdch_vars[key][1].set(new_name)
        elif key in self.vach_vars.keys():  # If old name in VACh dictionary
            self.vach_vars[key][1].set(new_name)

    def slide_event(self, junk):
        #print("--------------VACh Sliders--------------")
        tmp_data = self.main_data.get_data()  # Get current data from json
        for key, values in tmp_data['VACh'].items():
            int_value = self.vach_vars[values[1]][0].get()
            tmp_data['VACh'][key][0] = int_value
            #print("Key: " + key + " Int Value: " + str(int_value) + " Alias: " + values[1])
        self.main_data.update_data(**tmp_data)  # Dump changed VACh dictionary back into json

    def checkbox_event(self):
        #print("--------------VDCh Checkboxes--------------")
        tmp_data = self.main_data.get_data()  # Get current data from json
        for key, values in tmp_data['VDCh'].items():
            int_value = self.vdch_vars[values[1]][0].get()
            tmp_data['VDCh'][key][0] = int_value
            #print("Key: " + key + " Int Value: " + str(int_value) + " Alias: " + values[1])
        self.main_data.update_data(**tmp_data)  # Dump changed VDCh dictionary back into json

    def set_conn_status(self, time, status):
        self.conn_status_var.set("Status: " + status)
        self.conn_time_var.set("Response time: " + time)

    def initUI(self):
        left_frame = Frame(self)
        right_frame = Frame(self)

        # Leftframe of Bottomframe
        # VDChannel Checkboxes
        ch_frame = Frame(left_frame, relief=RIDGE, borderwidth=1)
        for row in range(4):
            for col in range(4):
                # self.vdch_vars['VDCh' + str(4 * row + col + 1)] = (IntVar(), StringVar())
                # self.vdch_vars['VDCh' + str(4 * row + col + 1)][1].set("VDCh" + str(4 * row + col + 1))
                cell_frame = Frame(ch_frame)
                Checkbutton(cell_frame, variable=self.vdch_vars['VDCh' + str(4 * row + col + 1)][0], onvalue=4095,
                            offvalue=0, command=self.checkbox_event,
                            image=self.off_image, selectimage=self.on_image, indicatoron=False).pack(side=LEFT)
                Label(cell_frame, textvariable=self.vdch_vars['VDCh' + str(4 * row + col + 1)][1],
                      font=(None, FONT_SIZE)).pack(side=LEFT, padx=4)
                cell_frame.grid(row=row, column=col, padx=10)
        ch_frame.pack(padx=2)

        # VAChannel Sliders
        sl_frame = Frame(left_frame, relief=RIDGE, borderwidth=1)
        frame1 = Frame(sl_frame)
        frame2 = Frame(sl_frame)
        for i in range(8):
            # self.vach_vars['VACh' + str(i + 1)] = (IntVar(), StringVar())
            # self.vach_vars['VACh' + str(i + 1)][1].set("VACh" + str(i + 1))
            Label(frame1, textvariable=self.vach_vars['VACh' + str(i + 1)][1], font=(None, FONT_SIZE)).pack(side=LEFT,
                                                                                                            padx=2)
            Scale(frame2, from_=0, to=4095, length=200, variable=self.vach_vars['VACh' + str(i + 1)][0],
                  command=self.slide_event).pack(side=LEFT, padx=5)
        frame1.pack(anchor=W)
        frame2.pack(anchor=W)
        sl_frame.pack(pady=10, padx=2)

        # Rightframe of Bottomframe
        # ACh/DCh data visuals and status
        data_frame = Frame(right_frame, relief=RIDGE, borderwidth=1, padx=40, pady=20)
        frame1 = Frame(data_frame)
        frame2 = Frame(data_frame)
        frame3 = Frame(data_frame)
        for i in range(8):
            Label(frame1, textvariable=self.ach_vars[i], font=(None, FONT_SIZE)).pack()
            # self.ach_labels[i].pack()
        for row in range(4):
            for col in range(4):
                dId = str(4 * row + col + 1)
                if len(dId) == 1:
                    dId = "0" + dId
                self.dch_labels.append(Label(frame2, text="D" + dId, font=(None, FONT_SIZE)))
                self.dch_labels[len(self.dch_labels) - 1].grid(row=row, column=col)
        self.conn_status_var.set("Status: NA")
        self.conn_time_var.set("Response time: NA")
        Label(frame3, textvariable=self.conn_status_var, font=(None, FONT_SIZE)).pack()
        Label(frame3, textvariable=self.conn_time_var, font=(None, FONT_SIZE)).pack()
        frame1.pack()
        frame2.pack(pady=10)
        frame3.pack()
        data_frame.pack()

        left_frame.pack(side=LEFT, fill=BOTH)
        right_frame.pack(side=RIGHT, fill=BOTH)
        # self.main_data.update_data(True, **self.vdch_vars, **self.scale_bars)
        # values = self.scale_bars.pop("VACh3")
        # values[1].set("Test3")
        # self.scale_bars['Test3'] = values

        # self.update_json(self.scale_bars)
        # print(self.scale_bars[0].get())
        # self.master.pack(side=BOTTOM, fill=BOTH)
