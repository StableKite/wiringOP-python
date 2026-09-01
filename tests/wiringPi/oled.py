import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.oled")

def test_struct_displayinfo():
    obj=m.DisplayInfo()
    _=obj.address
    _=obj.file
    _=obj.font
    assert len(obj.buffer) == 1024

def test_struct_sizedarray():
    obj=m.SizedArray()
    _=obj.size
    assert obj.array_address == 0
    obj.array_address=0

def test_oled_close():
    _=m.oled_close(m.DisplayInfo())

def test_oled_open():
    d=m.DisplayInfo();assert m.oled_open(d,"/dev/null")==0 and d.file==42

def test_oled_send():
    d=m.DisplayInfo();assert m.oled_send(d,b"abc")==3

def test_oled_init():
    _=m.oled_init(m.DisplayInfo())

def test_oled_send_buffer():
    _=m.oled_send_buffer(m.DisplayInfo())

def test_oled_clear():
    _=m.oled_clear(m.DisplayInfo())

def test_oled_putstr():
    d=m.DisplayInfo();m.oled_putstr(d,0,"abc")

def test_oled_putpixel():
    _=m.oled_putpixel(m.DisplayInfo(), 1, 1, 1)

def test_oled_putstrto():
    d=m.DisplayInfo();m.oled_putstrto(d,0,0,"abc")

def test_variable_display_config():
    assert hasattr(m,"display_config")

def test_variable_display_draw():
    assert hasattr(m,"display_draw")

def test_constants_and_macros():
    assert hasattr(m,"OLED_I2C_ADDR")
    assert hasattr(m,"OLED_CTRL_BYTE_CMD_SINGLE")
    assert hasattr(m,"OLED_CTRL_BYTE_CMD_STREAM")
    assert hasattr(m,"OLED_CTRL_BYTE_DATA_STREAM")
    assert hasattr(m,"OLED_CMD_SET_CONTRAST")
    assert hasattr(m,"OLED_CMD_DISPLAY_RAM")
    assert hasattr(m,"OLED_CMD_DISPLAY_ALLON")
    assert hasattr(m,"OLED_CMD_DISPLAY_NORMAL")
    assert hasattr(m,"OLED_CMD_DISPLAY_INVERTED")
    assert hasattr(m,"OLED_CMD_DISPLAY_OFF")
    assert hasattr(m,"OLED_CMD_DISPLAY_ON")
    assert hasattr(m,"OLED_CMD_SET_MEMORY_ADDR_MODE")
    assert hasattr(m,"OLED_CMD_SET_COLUMN_RANGE")
    assert hasattr(m,"OLED_CMD_SET_PAGE_RANGE")
    assert hasattr(m,"OLED_CMD_SET_DISPLAY_START_LINE")
    assert hasattr(m,"OLED_CMD_SET_SEGMENT_REMAP")
    assert hasattr(m,"OLED_CMD_SET_MUX_RATIO")
    assert hasattr(m,"OLED_CMD_SET_COM_SCAN_MODE")
    assert hasattr(m,"OLED_CMD_SET_DISPLAY_OFFSET")
    assert hasattr(m,"OLED_CMD_SET_COM_PIN_MAP")
    assert hasattr(m,"OLED_CMD_NOP")
    assert hasattr(m,"OLED_CMD_SET_DISPLAY_CLK_DIV")
    assert hasattr(m,"OLED_CMD_SET_PRECHARGE")
    assert hasattr(m,"OLED_CMD_SET_VCOMH_DESELCT")
    assert hasattr(m,"OLED_CMD_SET_CHARGE_PUMP")
    assert hasattr(m,"OLED_SET_PAGE_ADDRESS")
