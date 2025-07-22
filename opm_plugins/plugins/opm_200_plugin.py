from plugin_system.base_device import OPMInterface
import pyvisa

plugin_info = {
    "name":"OPM-200",
    "type":"opm",
    "class":"OPM_200"
}

class OPM_200(OPMInterface):
    @classmethod
    def can_connect(cls):
        rm = pyvisa.ResourceManager()
        res = rm.list_resources()
        for i in res:
            try:
                print(f"Trying resource: {i}")
                inst = rm.open_resource(i)
                idn = inst.query("*IDN?")
                if "OPM" in idn:
                    return (i, inst)
            except:
                continue
        return None
    
    def __init__(self,inst):
        self.inst = inst
        self.ch = 0

    def connect(self):
        self.inst.write("*RST")

    def set_wavelength(self,wvl=1310.00):
        self.inst.write(":SENSe"+str(self.ch)+":WAVelength "+str(wvl))

    def set_opm_channel(self,ch=1):
        self.ch = ch
        self.inst.write(":MODule:SELect "+str(ch))

    def set_dark(self):
        self.inst.write(":SENSe{self.ch}:DARK")

    def read_power(self):
        return float(self.inst.query("READ:POWer?"))