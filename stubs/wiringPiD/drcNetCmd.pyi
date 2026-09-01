"""nanobind bindings for wiringPiD/drcNetCmd.h"""



class DrcNetComStruct:
    def __init__(self) -> None: ...

    @property
    def pin(self) -> int: ...

    @pin.setter
    def pin(self, arg: int, /) -> None: ...

    @property
    def cmd(self) -> int: ...

    @cmd.setter
    def cmd(self, arg: int, /) -> None: ...

    @property
    def data(self) -> int: ...

    @data.setter
    def data(self, arg: int, /) -> None: ...

DEFAULT_SERVER_PORT: int = 6124

DRCN_PIN_MODE: int = 1

DRCN_PULL_UP_DN: int = 2

DRCN_DIGITAL_WRITE: int = 3

DRCN_DIGITAL_WRITE8: int = 4

DRCN_ANALOG_WRITE: int = 5

DRCN_PWM_WRITE: int = 6

DRCN_DIGITAL_READ: int = 7

DRCN_DIGITAL_READ8: int = 8

DRCN_ANALOG_READ: int = 9
