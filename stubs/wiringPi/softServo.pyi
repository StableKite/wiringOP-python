"""nanobind bindings for wiringPi/softServo.h"""



def soft_servo_write(pin: int, value: int) -> None: ...

def soft_servo_setup(p0: int, p1: int, p2: int, p3: int, p4: int, p5: int, p6: int, p7: int) -> int: ...
