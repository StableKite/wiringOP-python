import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.soft_pwm")

def test_soft_pwm_create():
    _=m.soft_pwm_create(1, 1, 1)

def test_soft_pwm_write():
    _=m.soft_pwm_write(1, 1)

def test_soft_pwm_stop():
    _=m.soft_pwm_stop(1)
