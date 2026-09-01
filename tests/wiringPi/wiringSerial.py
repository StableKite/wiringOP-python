import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.wiring_serial")

def test_struct_serialconfig():
    obj=m.SerialConfig()
    _=obj.struct_size
    _=obj.version
    _=obj.baud
    _=obj.data_bits
    _=obj.parity
    _=obj.stop_bits
    _=obj.flow_control
    _=obj.xon_char
    _=obj.xoff_char
    _=obj.vmin
    _=obj.vtime
    assert len(obj.reserved) == 4

def test_struct_serialrs485config():
    obj=m.SerialRS485Config()
    _=obj.struct_size
    _=obj.flags
    _=obj.delay_before_send_ms
    _=obj.delay_after_send_ms
    _=obj.receive_address
    _=obj.destination_address
    assert len(obj.reserved8) == 2
    assert len(obj.reserved) == 4

def test_struct_serialcounters():
    obj=m.SerialCounters()
    _=obj.struct_size
    _=obj.cts
    _=obj.dsr
    _=obj.rng
    _=obj.dcd
    _=obj.rx
    _=obj.tx
    _=obj.frame
    _=obj.overrun
    _=obj.parity
    _=obj.brk
    _=obj.buf_overrun
    assert len(obj.reserved) == 4

def test_struct_serialhardwareinfo():
    obj=m.SerialHardwareInfo()
    _=obj.struct_size
    _=obj.hardware_type
    _=obj.fifo_size
    _=obj.baud_base
    _=obj.port_type
    _=obj.line
    _=obj.capabilities
    assert len(obj.reserved) == 6

def test_serial_open():
    _=m.serial_open("x", 1)

def test_serial_close():
    _=m.serial_close(1)

def test_serial_flush():
    _=m.serial_flush(1)

def test_serial_putchar():
    _=m.serial_putchar(1, 1)

def test_serial_puts():
    _=m.serial_puts(1, "x")

def test_serial_printf():
    m.serial_printf(1, "safe text")

def test_serial_data_avail():
    _=m.serial_data_avail(1)

def test_serial_getchar():
    _=m.serial_getchar(1)

def test_serial_config_init():
    c=m.serial_config_init();assert c.baud==9600 and c.data_bits==8

def test_serial_open_config():
    _=m.serial_open_config("x", m.SerialConfig())

def test_serial_get_config():
    rc,c=m.serial_get_config(7);assert rc==0

def test_serial_set_config():
    _=m.serial_set_config(1, m.SerialConfig())

def test_serial_get_baud():
    assert m.serial_get_baud(7)[0]==0

def test_serial_set_baud():
    _=m.serial_set_baud(1, 1)

def test_serial_read():
    assert m.serial_read(7,4)==b"0123"

def test_serial_write():
    assert m.serial_write(7,b"abcd")==4

def test_serial_read_timeout():
    assert m.serial_read_timeout(7,4,10,-1)==b"0123"

def test_serial_write_timeout():
    assert m.serial_write_timeout(7,b"abcd",10)==4

def test_serial_drain():
    _=m.serial_drain(1)

def test_serial_flush_input():
    _=m.serial_flush_input(1)

def test_serial_flush_output():
    _=m.serial_flush_output(1)

def test_serial_input_waiting():
    _=m.serial_input_waiting(1)

def test_serial_output_waiting():
    _=m.serial_output_waiting(1)

def test_serial_send_break():
    _=m.serial_send_break(1, 1)

def test_serial_set_break():
    _=m.serial_set_break(1, 1)

def test_serial_get_modem_lines():
    assert m.serial_get_modem_lines(7)[0]==0

def test_serial_set_modem_lines():
    _=m.serial_set_modem_lines(1, 1, 1)

def test_serial_set_rts():
    _=m.serial_set_rts(1, 1)

def test_serial_set_dtr():
    _=m.serial_set_dtr(1, 1)

def test_serial_get_cts():
    _=m.serial_get_cts(1)

def test_serial_get_dsr():
    _=m.serial_get_dsr(1)

def test_serial_get_ri():
    _=m.serial_get_ri(1)

def test_serial_get_cd():
    _=m.serial_get_cd(1)

def test_serial_set_input_flow():
    _=m.serial_set_input_flow(1, 1)

def test_serial_set_output_flow():
    _=m.serial_set_output_flow(1, 1)

def test_serial_set_exclusive():
    _=m.serial_set_exclusive(1, 1)

def test_serial_get_low_latency():
    _=m.serial_get_low_latency(1)

def test_serial_set_low_latency():
    _=m.serial_set_low_latency(1, 1)

def test_serial_get_counters():
    assert m.serial_get_counters(7)[0]==0

def test_serial_tx_empty():
    _=m.serial_tx_empty(1)

def test_serial_get_rs485():
    assert m.serial_get_rs485(7)[0]==0

def test_serial_set_rs485():
    _=m.serial_set_rs485(1, m.SerialRS485Config())

def test_serial_get_rx_trigger():
    _=m.serial_get_rx_trigger(1)

def test_serial_set_rx_trigger():
    _=m.serial_set_rx_trigger(1, 1)

def test_serial_get_wakeup():
    _=m.serial_get_wakeup(1)

def test_serial_set_wakeup():
    _=m.serial_set_wakeup(1, 1)

def test_serial_get_hardware_info():
    assert m.serial_get_hardware_info(7)[0]==0

def test_serial_get_capabilities():
    assert m.serial_get_capabilities(7)[0]==0

def test_serial_context_open():
    cfg=m.serial_config_init();a=m.serial_context_open("mock",cfg);assert isinstance(a,int) and a!=0;m.serial_context_close(a)

def test_serial_context_from_fd():
    a=m.serial_context_from_fd(7,0);assert m.serial_context_get_fd(a)==7;m.serial_context_close(a)

def test_serial_context_close():
    cfg=m.serial_config_init();a=m.serial_context_open("mock",cfg);m.serial_context_close(a)

def test_serial_context_get_fd():
    a=m.serial_context_from_fd(7,0);assert m.serial_context_get_fd(a)==7;m.serial_context_close(a)

def test_serial_context_read():
    a=m.serial_context_from_fd(7,0);assert m.serial_context_read(a,4,10,-1)==b"0123";m.serial_context_close(a)

def test_serial_context_write():
    a=m.serial_context_from_fd(7,0);assert m.serial_context_write(a,b"abcd",10)==4;m.serial_context_close(a)

def test_serial_context_cancel_read():
    a=m.serial_context_from_fd(7,0);assert m.serial_context_cancel_read(a)==0;m.serial_context_close(a)

def test_serial_context_cancel_write():
    a=m.serial_context_from_fd(7,0);assert m.serial_context_cancel_write(a)==0;m.serial_context_close(a)

def test_constants_and_macros():
    assert hasattr(m,"SERIAL_CONFIG_VERSION")
    assert hasattr(m,"SERIAL_CONFIG_STRUCT_SIZE")
    assert hasattr(m,"SERIAL_PARITY_NONE")
    assert hasattr(m,"SERIAL_PARITY_ODD")
    assert hasattr(m,"SERIAL_PARITY_EVEN")
    assert hasattr(m,"SERIAL_PARITY_MARK")
    assert hasattr(m,"SERIAL_PARITY_SPACE")
    assert hasattr(m,"SERIAL_STOP_BITS_ONE")
    assert hasattr(m,"SERIAL_STOP_BITS_ONE_POINT_FIVE")
    assert hasattr(m,"SERIAL_STOP_BITS_TWO")
    assert hasattr(m,"SERIAL_FLOW_NONE")
    assert hasattr(m,"SERIAL_FLOW_XON_XOFF")
    assert hasattr(m,"SERIAL_FLOW_RTS_CTS")
    assert hasattr(m,"SERIAL_MODEM_RTS")
    assert hasattr(m,"SERIAL_MODEM_DTR")
    assert hasattr(m,"SERIAL_MODEM_CTS")
    assert hasattr(m,"SERIAL_MODEM_DSR")
    assert hasattr(m,"SERIAL_MODEM_RI")
    assert hasattr(m,"SERIAL_MODEM_CD")
    assert hasattr(m,"SERIAL_MODEM_LOOP")
    assert hasattr(m,"SERIAL_RS485_ENABLED")
    assert hasattr(m,"SERIAL_RS485_RTS_ON_SEND")
    assert hasattr(m,"SERIAL_RS485_RTS_AFTER_SEND")
    assert hasattr(m,"SERIAL_RS485_RX_DURING_TX")
    assert hasattr(m,"SERIAL_RS485_TERMINATE_BUS")
    assert hasattr(m,"SERIAL_RS485_ADDRESS_MODE")
    assert hasattr(m,"SERIAL_RS485_RX_ADDRESS")
    assert hasattr(m,"SERIAL_RS485_DEST_ADDRESS")
    assert hasattr(m,"SERIAL_RS485_MODE_RS422")
    assert hasattr(m,"SERIAL_CAP_CUSTOM_BAUD")
    assert hasattr(m,"SERIAL_CAP_MARK_SPACE_PARITY")
    assert hasattr(m,"SERIAL_CAP_XON_XOFF")
    assert hasattr(m,"SERIAL_CAP_RTS_CTS")
    assert hasattr(m,"SERIAL_CAP_MODEM_CONTROL")
    assert hasattr(m,"SERIAL_CAP_MODEM_STATUS")
    assert hasattr(m,"SERIAL_CAP_EXCLUSIVE")
    assert hasattr(m,"SERIAL_CAP_LOW_LATENCY")
    assert hasattr(m,"SERIAL_CAP_RS485")
    assert hasattr(m,"SERIAL_CAP_ICOUNT")
    assert hasattr(m,"SERIAL_CAP_TX_EMPTY")
    assert hasattr(m,"SERIAL_CAP_RX_TRIGGER")
    assert hasattr(m,"SERIAL_CAP_WAKEUP")
    assert hasattr(m,"SERIAL_CAP_8250")
    assert hasattr(m,"SERIAL_CAP_DW_APB_UART")
    assert hasattr(m,"SERIAL_CAP_RK3588_UART")
    assert hasattr(m,"SERIAL_CAP_DMA_DESCRIBED")
    assert hasattr(m,"SERIAL_CAP_AUTO_RTS_CTS")
    assert hasattr(m,"SERIAL_CAP_FIFO")
    assert hasattr(m,"SERIAL_CAP_CANCEL_IO")
    assert hasattr(m,"SERIAL_HARDWARE_UNKNOWN")
    assert hasattr(m,"SERIAL_HARDWARE_8250")
    assert hasattr(m,"SERIAL_HARDWARE_DW_APB_UART")
    assert hasattr(m,"SERIAL_HARDWARE_RK3588_UART")

def test_serial_port_high_level():
    p=m.SerialPort("mock",115200)
    assert p.is_open and p.fileno()==7 and p.port=="mock" and p.name=="mock"
    p.baudrate=123456;assert p.baudrate==123456 and p.baud==123456
    p.bytesize=8;p.parity="N";p.stopbits=1;p.xonxoff=True;p.rtscts=True
    p.timeout=0.01;p.write_timeout=0.01;p.inter_byte_timeout=None
    assert p.read(4)==b"0123"
    b=bytearray(4);assert p.read_into(b)==4 and b==b"0123"
    assert p.write(memoryview(b"abcd"))==4
    assert p.in_waiting==3 and p.out_waiting==3
    assert p.hardware_info.fifo_size==64
    assert p.capabilities & m.SERIAL_CAP_RK3588_UART
    assert p.capabilities & m.SERIAL_CAP_CANCEL_IO
    assert p.cts and p.dsr and p.ri and p.cd
    p.rts=True;p.dtr=True;p.set_input_flow_control(True);p.set_output_flow_control(True)
    p.break_condition=True;assert p.break_condition;p.break_condition=False
    p.cancel_read();p.cancel_write()
    p.close();assert not p.is_open
    p.open();assert p.is_open;p.close()

def test_serial_port_dsrdtr_reports_linux_limit():
    p=m.SerialPort("mock",9600)
    assert p.dsrdtr is False
    with pytest.raises(NotImplementedError): p.dsrdtr=True
    p.close()
