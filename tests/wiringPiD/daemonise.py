import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi_d.daemonise")

def test_daemonise():
    _=m.daemonise("x")
