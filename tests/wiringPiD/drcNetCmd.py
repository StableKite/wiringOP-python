import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi_d.drc_net_cmd")

def test_struct_drcnetcomstruct():
    obj=m.DrcNetComStruct()
    _=obj.pin
    _=obj.cmd
    _=obj.data

def test_constants_and_macros():
    assert hasattr(m,"DEFAULT_SERVER_PORT")
    assert hasattr(m,"DRCN_PIN_MODE")
    assert hasattr(m,"DRCN_PULL_UP_DN")
    assert hasattr(m,"DRCN_DIGITAL_WRITE")
    assert hasattr(m,"DRCN_DIGITAL_WRITE8")
    assert hasattr(m,"DRCN_ANALOG_WRITE")
    assert hasattr(m,"DRCN_PWM_WRITE")
    assert hasattr(m,"DRCN_DIGITAL_READ")
    assert hasattr(m,"DRCN_DIGITAL_READ8")
    assert hasattr(m,"DRCN_ANALOG_READ")
