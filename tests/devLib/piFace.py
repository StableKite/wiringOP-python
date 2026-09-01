import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.pi_face")

def test_pi_face_setup():
    _=m.pi_face_setup(1)
