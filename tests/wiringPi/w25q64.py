import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.w25q64")

def test_w25q64_begin():
    _=m.w25q64_begin(1)

def test_w25q64_read_status_reg1():
    _=m.w25q64_read_status_reg1()

def test_w25q64_read_status_reg2():
    _=m.w25q64_read_status_reg2()

def test_w25q64_read_manufacturer():
    assert m.w25q64_read_manufacturer()==bytes.fromhex("ef4017")

def test_w25q64_read_unique_id():
    assert m.w25q64_read_unique_id()==bytes(range(0x10,0x17))

def test_w25q64_is_busy():
    _=m.w25q64_is_busy()

def test_w25q64_power_down():
    _=m.w25q64_power_down()

def test_w25q64_write_enable():
    _=m.w25q64_write_enable()

def test_w25q64_write_disable():
    _=m.w25q64_write_disable()

def test_w25q64_read():
    assert m.w25q64_read(0x20,4)==bytes([0x20,0x21,0x22,0x23])

def test_w25q64_fast_read():
    assert m.w25q64_fast_read(0x20,4)==bytes([0x20,0x21,0x22,0x23])

def test_w25q64_erase_sector():
    _=m.w25q64_erase_sector(1, True)

def test_w25q64_erase64_block():
    _=m.w25q64_erase64_block(1, True)

def test_w25q64_erase32_block():
    _=m.w25q64_erase32_block(1, True)

def test_w25q64_erase_all():
    _=m.w25q64_erase_all(True)

def test_w25q64_page_write():
    assert m.w25q64_page_write(0,0,b"abc")==3
    with pytest.raises(ValueError):m.w25q64_page_write(0,250,b"0123456789")
