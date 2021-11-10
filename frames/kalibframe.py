from tkinter import *

FONT_SIZE = 12


class KalibFrame(Frame):

    def __init__(self, master, data):
        super().__init__(master)
        self.main_data = data  #Data storage of all channels and mixers
        self.ach_menu = ["ACh1", "ACh2", "ACh3", "ACh4", "ACh5", "ACh6", "ACh7", "ACh8"]
        self.ach_menu_var = StringVar()
        self.error_label_var = StringVar()
        self.value_label_var = StringVar()
        self.max_var = StringVar()
        self.mid_var = StringVar()
        self.min_var = StringVar()
        self.ui_updated = False
        self.prev_sel = ""
        self.initUI()

    def update_ach_values(self):
        tmp_data = self.main_data.get_data()
        for ach in self.ach_menu:
            new_val = tmp_data['ACh'][ach][0]
            if None not in tmp_data['ACh'][ach]:
                new_val = self.calculate_value(tmp_data['ACh'][ach][0], tmp_data['ACh'][ach][1],
                                               tmp_data['ACh'][ach][2], tmp_data['ACh'][ach][3])
                tmp_data['ACh'][ach][0] = new_val
            if self.ach_menu_var.get() == ach:
                if self.prev_sel != ach:
                    self.prev_sel = ach
                    self.ui_updated = False
                self.value_label_var.set("Wert: " + str(new_val))
                if None not in tmp_data['ACh'][ach] and not self.ui_updated:
                    self.ui_updated = True
                    self.max_var.set(tmp_data['ACh'][ach][1])
                    self.mid_var.set(tmp_data['ACh'][ach][2])
                    self.min_var.set(tmp_data['ACh'][ach][3])
                elif not self.ui_updated:
                    self.ui_updated = True
                    self.max_var.set("")
                    self.mid_var.set("")
                    self.min_var.set("")
        self.main_data.update_data(**tmp_data)

    def calculate_value(self, current_val, max_val, mid_val, min_val):
        if current_val <= mid_val:
            return int(((current_val - min_val) / (mid_val - min_val)) * 2047)
        else:
            return int(((current_val - mid_val - 1) / (max_val - mid_val - 1)) * 2047 + 2048)

    def save_settings(self):
        if self.max_var.get() and self.mid_var.get() and self.min_var.get():
            #print("SAVE CALIBRATION SETTINGS")
            tmp_data = self.main_data.get_data()
            tmp_data['ACh'][self.ach_menu_var.get()][1] = int(self.max_var.get())
            tmp_data['ACh'][self.ach_menu_var.get()][2] = int(self.mid_var.get())
            tmp_data['ACh'][self.ach_menu_var.get()][3] = int(self.min_var.get())
            new_value = self.calculate_value(tmp_data['ACh'][self.ach_menu_var.get()][0],
                                             int(self.max_var.get()), int(self.mid_var.get()),
                                             int(self.min_var.get()))
            tmp_data['ACh'][self.ach_menu_var.get()][0] = new_value
            self.value_label_var.set("Wert: " + str(new_value))
            self.error_label_var.set("")
            self.main_data.update_data(**tmp_data)
        else:
            #print("MAX, MID OR MIN ARE NOT FILLED IN")
            self.error_label_var.set("Maximum-, Mittel- oder Minimumswert sind nicht eingetragen worden")

    def initUI(self):
        #Frame 1
        frame1 = Frame(self)
        Label(frame1, text="ACh", font=(None, FONT_SIZE), padx=5).pack(side=LEFT)
        self.ach_menu_var.set("ACh1")
        ach_menu = OptionMenu(frame1, self.ach_menu_var, *self.ach_menu)
        ach_menu.config(width=20, height=2, padx=5)
        ach_menu.pack(side=LEFT, padx=10)
        #ach_combobox = ttk.Combobox(frame1, width=20, font=(None, FONT_SIZE), values=["ACh1", "ACh2", "ACh2"])
        #ach_combobox.current(1)
        #ach_combobox.pack(side=LEFT, padx=10, ipady=10)
        Label(frame1, textvariable=self.value_label_var, font=(None, FONT_SIZE)).pack(side=LEFT, padx=30)

        #Frame 2
        frame2 = Frame(self)
        Label(frame2, text="Max", font=(None, FONT_SIZE), padx=5).pack(side=LEFT)
        max_entry = Entry(frame2, width=20, textvariable=self.max_var)
        max_entry.pack(side=LEFT, padx=18, ipady=6)
        #Button(frame2, text="Set", font=(None, FONT_SIZE), width=10).pack(side=LEFT, padx=20)

        #Frame 3
        frame3 = Frame(self)
        Label(frame3, text="Mittel", font=(None, FONT_SIZE), padx=5).pack(side=LEFT)
        mid_entry = Entry(frame3, width=20, textvariable=self.mid_var)
        mid_entry.pack(side=LEFT, padx=10, ipady=6)
        #Button(frame3, text="Set", font=(None, FONT_SIZE), width=10).pack(side=LEFT, padx=28)

        #Frame 4
        frame4 = Frame(self)
        Label(frame4, text="Min", font=(None, FONT_SIZE), padx=5).pack(side=LEFT)
        min_entry = Entry(frame4, width=20, textvariable=self.min_var)
        min_entry.pack(side=LEFT, padx=22, ipady=6)
        #Button(frame4, text="Set", font=(None, FONT_SIZE), width=10).pack(side=LEFT, padx=16)

        frame1.pack(anchor=NW, pady=5)
        frame2.pack(anchor=NW, pady=5)
        frame3.pack(anchor=NW, pady=5)
        frame4.pack(anchor=NW, pady=5)
        Button(self, text="Speichern", font=(None, FONT_SIZE), width=20, height=2, command=self.save_settings).pack(
            pady=10)
        self.error_label_var.set("")
        Label(self, textvariable=self.error_label_var, font=(None, FONT_SIZE)).pack()
