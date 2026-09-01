import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.soft_servo")

def test_soft_servo_write():
    _=m.soft_servo_write(1, 1)

def test_soft_servo_setup():
    _=m.soft_servo_setup(1, 1, 1, 1, 1, 1, 1, 1)
