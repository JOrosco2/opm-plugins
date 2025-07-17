from plugin_system.base_device import OPMInterface
import pyvisa

plugin_info = {
    "name":"HP8153A",
    "type":"opm",
    "class":"HP8153A"
}

class HP8153A(OPMInterface):
    @classmethod
    def can_connect(cls):
        rm = pyvisa.ResourceManager()
        res = rm.list_resources()
        for i in res:
            try:
                print(f"Trying resource: {i}")
                inst = rm.open_resource(i)
                idn = inst.query("*IDN?")
                if "8153A" in idn:
                    return(i, inst)
            except:
                continue
        return None
    
    def __init__(self,inst):
        self.inst = inst
        self.ch = 1 #channel is 1 indexed

    def connect(self):
        self.inst.write("*RST")

    def set_wavelength(self,wvl=1310.00):
        self.inst.write("SENS"+str(self.ch)+":WAV "+str(wvl)+"NM")
    
    def set_opm_channel(self,ch=1):
        self.ch = ch

    def set_dark(self):
        self.inst.write("SENS" + str(self.ch) + ":CORRection:COLLect:ZERO")
    
    def read_power(self):
        return float(self.inst.query("READ"+str(self.ch)+":POW?"))