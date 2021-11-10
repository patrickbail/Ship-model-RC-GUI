import json
from json.decoder import JSONDecodeError


class DataClass:
    data = {}
    status = "NA"
    time = "NA"

    def __init__(self):
        try:
            with open("profile.json", "r", encoding="utf-8") as json_file:
                try:
                    tmp_data = json.load(json_file)
                    print("DATA EXIST, NO INIT")
                    DataClass.data = tmp_data
                except JSONDecodeError:
                    print("DATA DOES NOT EXIST, INIT DATA")
                    self.init_data()
        except FileNotFoundError:
            print("FILE DOES NOT EXIST, INIT DATA")
            self.init_data()

    def init_data(self):
        print("INIT JSON DATA FOR VACH, VDCH, ACH, DCH and Transmit")
        data_vach = {}
        data_ach = {}
        data_vdch = {}
        data_dch = {}
        data_transmit = {}
        for i in range(8):
            key = "VACh" + str(i + 1)
            data_vach[key] = [0, key]  # VACh Int value, Alias
            data_ach[key[1:]] = [0, None, None, None]  # ACh Int Values, max, mid, min
            data_transmit['PWM' + str(i + 1)] = [None, None, None]  # PWM Int value, top_key, sub_key
        for i in range(16):
            nbr = str(i + 1)
            key = "VDCh" + nbr
            data_vdch[key] = [0, key]  # VDCh Int Value, Alias
            if len(nbr) == 1:  # DCh
                nbr = "0" + nbr
            key = "D" + nbr
            data_dch[key] = [0, key]  #DCh Int Value
            data_transmit[key] = [None, None, None]  # DCh Int value, top_key, sub_key
        DataClass.data['VACh'] = data_vach
        DataClass.data['ACh'] = data_ach
        DataClass.data['VDCh'] = data_vdch
        DataClass.data['DCh'] = data_dch
        DataClass.data['Transmit'] = data_transmit
        DataClass.update_json()

    @classmethod
    def set_achannel_data(cls, *args):
        for i in range(len(args)):
            key = 'ACh' + str((i + 1))
            cls.data['ACh'][key][0] = args[i]

    @classmethod
    def set_dchannel_data(cls, *args):
        for i in range(len(args)):
            nbr = str(i + 1)
            if len(nbr) == 1:
                nbr = '0' + nbr
            key = 'D' + nbr
            cls.data['DCh'][key] = [args[i], key]

    @classmethod
    def update_json(cls):
        with open("profile.json", "w") as json_file:
            json.dump(cls.data, json_file, ensure_ascii=False, indent=4)

    @classmethod
    def update_data(cls, **kwargs):
        #print("UPDATE DATA")
        for key, values in kwargs.items():
            cls.data[key] = values
        cls.update_json()

    @classmethod
    def get_data(cls):
        return cls.data

    @classmethod
    def get_keys(cls, top_key):
        return list(cls.data[top_key].keys())
