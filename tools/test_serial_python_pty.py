#!/usr/bin/env python3
from __future__ import annotations

import importlib
import os
import pty
import threading
import time


def main() -> int:
    m = importlib.import_module("wiringop.wiring_pi.wiring_serial")
    master, slave = pty.openpty()
    slave_name = os.ttyname(slave)
    os.close(slave)
    p = None
    try:
        p = m.SerialPort(slave_name, 115200)
        assert p.is_open
        p.timeout = None
        p.write_timeout = 1.0
        p.inter_byte_timeout = None
        assert p.timeout is None and p.inter_byte_timeout is None

        assert p.write(b"abc") == 3
        assert os.read(master, 3) == b"abc"
        os.write(master, b"xyz")
        assert p.read(3) == b"xyz"

        # cancel_read() must wake a blocking read while keeping the port open.
        started = threading.Event()
        done = threading.Event()
        result: dict[str, object] = {}

        def blocked_read() -> None:
            started.set()
            try:
                result["cancel_value"] = p.read(1)
            except BaseException as exc:  # Either b"" or an OS cancellation error is valid.
                result["cancel_exc"] = repr(exc)
            finally:
                done.set()

        t = threading.Thread(target=blocked_read, name="serial-cancel-read")
        t.start()
        assert started.wait(1.0)
        time.sleep(0.05)
        p.cancel_read()
        assert done.wait(1.0), "cancel_read() did not wake blocked read"
        t.join(1.0)
        assert not t.is_alive()
        assert p.is_open

        # close() waits for active I/O. The binding must release the GIL while
        # waiting, otherwise the read thread cannot reacquire it to drop OpGuard.
        started2 = threading.Event()
        done2 = threading.Event()

        def blocked_read_for_close() -> None:
            started2.set()
            try:
                result["close_value"] = p.read(1)
            except BaseException as exc:
                result["close_exc"] = repr(exc)
            finally:
                done2.set()

        t2 = threading.Thread(target=blocked_read_for_close, name="serial-close-read")
        t2.start()
        assert started2.wait(1.0)
        time.sleep(0.05)
        p.close()
        assert done2.wait(1.0), "close() deadlocked while cancelling blocked read"
        t2.join(1.0)
        assert not t2.is_alive()
        assert not p.is_open

        # Reopen is part of the high-level object contract.
        p.open()
        assert p.is_open
        p.close()
        print("PYTHON_SERIAL_PROD_PTY_OK")
        return 0
    finally:
        if p is not None:
            try:
                if p.is_open:
                    p.close()
            except Exception:
                pass
        os.close(master)


if __name__ == "__main__":
    raise SystemExit(main())
