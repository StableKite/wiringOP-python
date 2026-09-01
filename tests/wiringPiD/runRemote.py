import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi_d.run_remote")

def test_run_remote_commands():
    _=m.run_remote_commands(1)

def test_variable_no_local_pins():
    x=m.get_no_local_pins();m.set_no_local_pins(x)
