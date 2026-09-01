import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.pi_nes")

def test_setup_nes_joystick():
    _=m.setup_nes_joystick(1, 1, 1)

def test_read_nes_joystick():
    _=m.read_nes_joystick(1)

def test_constants_and_macros():
    assert hasattr(m,"MAX_NES_JOYSTICKS")
    assert hasattr(m,"NES_RIGHT")
    assert hasattr(m,"NES_LEFT")
    assert hasattr(m,"NES_DOWN")
    assert hasattr(m,"NES_UP")
    assert hasattr(m,"NES_START")
    assert hasattr(m,"NES_SELECT")
    assert hasattr(m,"NES_B")
    assert hasattr(m,"NES_A")
