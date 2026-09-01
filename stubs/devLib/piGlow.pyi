"""nanobind bindings for devLib/piGlow.h"""



def pi_glow1(leg: int, ring: int, intensity: int) -> None: ...

def pi_glow_leg(leg: int, intensity: int) -> None: ...

def pi_glow_ring(ring: int, intensity: int) -> None: ...

def pi_glow_setup(clear: int) -> None: ...

PIGLOW_RED: int = 0

PIGLOW_ORANGE: int = 1

PIGLOW_YELLOW: int = 2

PIGLOW_GREEN: int = 3

PIGLOW_BLUE: int = 4

PIGLOW_WHITE: int = 5
