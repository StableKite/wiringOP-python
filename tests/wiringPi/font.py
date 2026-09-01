import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.font")

def test_struct_fontinfo():
    obj=m.FontInfo()
    _=obj.width
    _=obj.height
    _=obj.spacing
    _=obj.offset
    assert obj.data_address == 0
    obj.data_address=0

def test_variable_font1_data():
    assert hasattr(m,"font1_data")

def test_variable_font2_data():
    assert hasattr(m,"font2_data")

def test_variable_font3_data():
    assert hasattr(m,"font3_data")

def test_variable_font1():
    x=m.get_font1();m.set_font1(x)

def test_variable_font2():
    x=m.get_font2();m.set_font2(x)

def test_variable_font3():
    x=m.get_font3();m.set_font3(x)
