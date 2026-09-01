import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi_d.network")

def test_get_client_ip():
    _=m.get_client_ip()

def test_get_response_legacy():
    assert m.get_response_legacy(3)==103

def test_setup_server():
    _=m.setup_server(1)

def test_send_greeting():
    _=m.send_greeting(1)

def test_send_challenge():
    _=m.send_challenge(1)

def test_get_response():
    _=m.get_response(1)

def test_password_match():
    _=m.password_match("x")

def test_close_server():
    _=m.close_server(1)
