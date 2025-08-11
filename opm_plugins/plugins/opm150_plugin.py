from plugin_system.base_device import OPMInterface
import os
from ctypes import *

plugin_info = {
    "name":"OPM150",
    "type":"opm",
    "class":"OPM150"
}

class OPM150(OPMInterface):

    @classmethod
    def can_connect(cls):
        handle = ""
        dllPath = os.path.dirname(__file__)
        mydll_path = os.path.join(dllPath,"OP710M_64.dll")

        mydll=cdll.LoadLibrary(mydll_path)

        #Change argtype to equivalent of char**
        GetDeviceDescription = mydll.GetUSBDeviceDescription
        GetDeviceDescription.argtypes = [c_int, POINTER(c_char_p)]

        ReadPower = mydll.ReadPower
        ReadPower.argtypes = [POINTER(c_double)]

        descPtr = c_char_p()
        devCount = c_int()
        devNum = -1

        #Iterate through USB Devices to find an OP710/OPM150
        mydll.GetUSBDeviceCount(byref(devCount))

        for i in range(devCount.value):
            GetDeviceDescription(i,byref(descPtr))
            descString = cast(descPtr, c_char_p)
            handle = descString.value.decode("utf-8")
            print(f"Trying: {handle}")
            if ("OP710" in handle):
                devNum = i
                break

        #No OP710/OPM150 Found. Return empty device
        if devNum < 0:
            return None
        
        usbHandle = c_int64()

        mydll.OpenUSBDevice(devNum,byref(usbHandle))
        
        OpenDriver = mydll.OpenDriver
        OpenDriver.argtypes = [c_int64]
        OpenDriver(usbHandle)

        #set the unit into remote mode and return the device
        mydll.RemoteMode(1)
        print(handle)
        print(mydll)
        return (handle,mydll)

    def __init__(self,inst):
        self.mydll = inst
        self.ch = 0

    def connect(self):
        self.mydll.RemoteMode(1)

    def set_wavelength(self,wvl=1310.00):
        self.mydll.SetWavelength(int(wvl))

    def set_opm_channel(self,ch=1):
        self.ch = ch
        self.mydll.SetActiveChannel(ch)

    def set_dark(self):
        #op710 does not have a zero function
        pass

    def read_power(self):
        power = c_double()
        self.mydll.ReadPower(byref(power))
        return float(power.value)
