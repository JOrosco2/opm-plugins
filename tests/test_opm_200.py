import pytest
import time
from plugins.opm_200_plugin import OPM_200

dev,inst = OPM_200.can_connect()
plugin = OPM_200(inst)

def test_set_channel():
    plugin.set_opm_channel(ch=1)

def test_set_wavlenghth():
    plugin.set_wavelength(wvl=1550.00)
    time.sleep(10)
    plugin.set_wavelength(wvl=1290.00)

def test_read_power():
    resp = plugin.read_power()
    assert isinstance(resp,float)
    print(f"Power = {resp:+07.3f} dBm")