"""nanobind bindings for devLib/piNes.h"""



def setup_nes_joystick(d_pin: int, c_pin: int, l_pin: int) -> int: ...

def read_nes_joystick(joystick: int) -> int: ...

MAX_NES_JOYSTICKS: int = 8

NES_RIGHT: int = 1

NES_LEFT: int = 2

NES_DOWN: int = 4

NES_UP: int = 8

NES_START: int = 16

NES_SELECT: int = 32

NES_B: int = 64

NES_A: int = 128
