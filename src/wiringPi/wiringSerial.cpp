// Generated from api_manifest.json. Do not edit directly.
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <Python.h>
#include <algorithm>
#include <array>
#include <cerrno>
#include <condition_variable>
#include <cstdint>
#include <cstring>
#include <dlfcn.h>
#include <mutex>
#include <stdexcept>
#include <string>
#include <vector>
#include <unistd.h>
extern "C" {
#include "wiringPi/wiringSerial.h"
}

namespace nb = nanobind;


struct PyBufferGuard {
    Py_buffer view{};
    bool active = false;
    PyBufferGuard(nb::handle obj, int flags) {
        if (PyObject_GetBuffer(obj.ptr(), &view, flags) != 0)
            throw nb::python_error();
        active = true;
    }
    ~PyBufferGuard() { if (active) PyBuffer_Release(&view); }
    PyBufferGuard(const PyBufferGuard &) = delete;
    PyBufferGuard &operator=(const PyBufferGuard &) = delete;
};

class SerialPort {
public:
    SerialPort(const char *device, int baud = 115200) : device_(device ? device : "") {
        serialConfigInit(&config_cache_);
        config_cache_.baud = (uint32_t) baud;
        open_locked();
    }
    SerialPort(const char *device, const serialConfig &cfg) : device_(device ? device : ""), config_cache_(cfg) {
        open_locked();
    }
    ~SerialPort() noexcept { try { close(); } catch (...) { } }
    SerialPort(const SerialPort &) = delete;
    SerialPort &operator=(const SerialPort &) = delete;

    class OpGuard {
    public:
        explicit OpGuard(SerialPort &owner) : owner_(owner) {
            std::lock_guard<std::mutex> lock(owner_.state_);
            if (!owner_.ctx_ || owner_.closing_) throw nb::value_error("serial port is closed");
            ++owner_.active_ops_;
            ctx_ = owner_.ctx_;
        }
        ~OpGuard() {
            std::lock_guard<std::mutex> lock(owner_.state_);
            if (owner_.active_ops_ > 0) --owner_.active_ops_;
            if (owner_.active_ops_ == 0) owner_.idle_.notify_all();
        }
        serialContext *ctx() const { return ctx_; }
        int fd() const {
            int fd = serialContextGetFd(ctx_);
            if (fd < 0) throw_errno("serialContextGetFd");
            return fd;
        }
    private:
        SerialPort &owner_;
        serialContext *ctx_ = nullptr;
    };

    void open() {
        std::lock_guard<std::mutex> lock(state_);
        if (ctx_) throw nb::value_error("serial port is already open");
        open_locked();
    }
    void close() {
        serialContext *ctx = nullptr;
        {
            std::unique_lock<std::mutex> lock(state_);
            if (!ctx_) return;
            closing_ = true;
            ctx = ctx_;
            // Wake operations that may currently be blocked in poll().
            (void) serialContextCancelRead(ctx);
            (void) serialContextCancelWrite(ctx);
            idle_.wait(lock, [&]{ return active_ops_ == 0; });
            int fd = serialContextGetFd(ctx);
            if (fd >= 0) {
                serialConfig tmp{};
                if (serialGetConfig(fd, &tmp) == 0) config_cache_ = tmp;
            }
            ctx_ = nullptr;
            closing_ = false;
        }
        serialContextClose(ctx);
    }
    bool is_open() const { std::lock_guard<std::mutex> lock(state_); return ctx_ != nullptr; }
    int fileno() { OpGuard op(*this); return op.fd(); }
    nb::str port() const { return nb::str(device_.c_str()); }
    nb::str name() const { return nb::str(device_.c_str()); }

    serialConfig config() {
        OpGuard op(*this); serialConfig c{};
        if (serialGetConfig(op.fd(), &c) < 0) throw_errno("serialGetConfig");
        { std::lock_guard<std::mutex> lock(state_); config_cache_ = c; }
        return c;
    }
    void set_config(const serialConfig &c) {
        OpGuard op(*this);
        if (serialSetConfig(op.fd(), &c) < 0) throw_errno("serialSetConfig");
        std::lock_guard<std::mutex> lock(state_); config_cache_ = c;
    }

    unsigned int baudrate() { return config().baud; }
    void set_baudrate(unsigned int value) { auto c=config(); c.baud=value; set_config(c); }
    unsigned int bytesize() { return config().dataBits; }
    void set_bytesize(unsigned int value) { auto c=config(); c.dataBits=(uint8_t)value; set_config(c); }
    nb::str parity() {
        switch (config().parity) {
            case SERIAL_PARITY_NONE: return nb::str("N");
            case SERIAL_PARITY_ODD: return nb::str("O");
            case SERIAL_PARITY_EVEN: return nb::str("E");
            case SERIAL_PARITY_MARK: return nb::str("M");
            case SERIAL_PARITY_SPACE: return nb::str("S");
            default: return nb::str("?");
        }
    }
    void set_parity(const char *value) {
        if (!value || !value[0] || value[1]) throw nb::value_error("parity must be one of N/O/E/M/S");
        auto c=config();
        switch (value[0]) {
            case 'N': case 'n': c.parity=SERIAL_PARITY_NONE; break;
            case 'O': case 'o': c.parity=SERIAL_PARITY_ODD; break;
            case 'E': case 'e': c.parity=SERIAL_PARITY_EVEN; break;
            case 'M': case 'm': c.parity=SERIAL_PARITY_MARK; break;
            case 'S': case 's': c.parity=SERIAL_PARITY_SPACE; break;
            default: throw nb::value_error("parity must be one of N/O/E/M/S");
        }
        set_config(c);
    }
    double stopbits() {
        switch (config().stopBits) {
            case SERIAL_STOP_BITS_ONE: return 1.0;
            case SERIAL_STOP_BITS_ONE_POINT_FIVE: return 1.5;
            case SERIAL_STOP_BITS_TWO: return 2.0;
            default: return 0.0;
        }
    }
    void set_stopbits(double value) {
        auto c=config();
        if (value == 1.0) c.stopBits=SERIAL_STOP_BITS_ONE;
        else if (value == 1.5) c.stopBits=SERIAL_STOP_BITS_ONE_POINT_FIVE;
        else if (value == 2.0) c.stopBits=SERIAL_STOP_BITS_TWO;
        else throw nb::value_error("stopbits must be 1, 1.5, or 2");
        set_config(c);
    }
    bool xonxoff() { return (config().flowControl & SERIAL_FLOW_XON_XOFF) != 0; }
    void set_xonxoff(bool value) { auto c=config(); if(value)c.flowControl|=SERIAL_FLOW_XON_XOFF;else c.flowControl&=~SERIAL_FLOW_XON_XOFF;set_config(c); }
    bool rtscts() { return (config().flowControl & SERIAL_FLOW_RTS_CTS) != 0; }
    void set_rtscts(bool value) { auto c=config(); if(value)c.flowControl|=SERIAL_FLOW_RTS_CTS;else c.flowControl&=~SERIAL_FLOW_RTS_CTS;set_config(c); }
    bool dsrdtr() const { return false; }
    void set_dsrdtr(bool value) { if (value) { PyErr_SetString(PyExc_NotImplementedError, "Linux tty has no portable automatic DSR/DTR flow-control mode"); throw nb::python_error(); } }

    static int timeout_object_to_ms(nb::handle value, const char *name) {
        if (value.is_none()) return -1;
        double seconds = nb::cast<double>(value);
        if (seconds < 0) throw nb::value_error(name);
        if (seconds > 2147483.0) throw nb::value_error("timeout is too large");
        return (int) (seconds * 1000.0 + 0.5);
    }
    static nb::object timeout_ms_to_object(int ms) {
        if (ms < 0) return nb::none();
        return nb::cast((double)ms / 1000.0);
    }
    nb::object timeout() const { std::lock_guard<std::mutex> lock(state_); return timeout_ms_to_object(read_timeout_ms_); }
    void set_timeout(nb::object value) { int v=timeout_object_to_ms(value,"timeout must be None or non-negative"); std::lock_guard<std::mutex> lock(state_); read_timeout_ms_=v; }
    nb::object write_timeout() const { std::lock_guard<std::mutex> lock(state_); return timeout_ms_to_object(write_timeout_ms_); }
    void set_write_timeout(nb::object value) { int v=timeout_object_to_ms(value,"write_timeout must be None or non-negative"); std::lock_guard<std::mutex> lock(state_); write_timeout_ms_=v; }
    nb::object inter_byte_timeout() const { std::lock_guard<std::mutex> lock(state_); return timeout_ms_to_object(inter_byte_timeout_ms_); }
    void set_inter_byte_timeout(nb::object value) { int v=timeout_object_to_ms(value,"inter_byte_timeout must be None or non-negative"); std::lock_guard<std::mutex> lock(state_); inter_byte_timeout_ms_=v; }

    int read_timeout_ms() const { std::lock_guard<std::mutex> lock(state_); return read_timeout_ms_; }
    void set_read_timeout_ms(int v) { if(v < -1) throw nb::value_error("timeout must be -1 or non-negative"); std::lock_guard<std::mutex> lock(state_); read_timeout_ms_=v; }
    int write_timeout_ms() const { std::lock_guard<std::mutex> lock(state_); return write_timeout_ms_; }
    void set_write_timeout_ms(int v) { if(v < -1) throw nb::value_error("timeout must be -1 or non-negative"); std::lock_guard<std::mutex> lock(state_); write_timeout_ms_=v; }
    int inter_byte_timeout_ms() const { std::lock_guard<std::mutex> lock(state_); return inter_byte_timeout_ms_; }
    void set_inter_byte_timeout_ms(int v) { if(v < -1) throw nb::value_error("timeout must be -1 or non-negative"); std::lock_guard<std::mutex> lock(state_); inter_byte_timeout_ms_=v; }

    nb::bytes read(size_t count) {
        OpGuard op(*this); std::vector<char> data(count); ssize_t n; int timeout_ms, inter_byte_timeout_ms;
        { std::lock_guard<std::mutex> lock(state_); timeout_ms=read_timeout_ms_; inter_byte_timeout_ms=inter_byte_timeout_ms_; }
        { nb::gil_scoped_release release; n=serialContextRead(op.ctx(), data.data(), count, timeout_ms, inter_byte_timeout_ms); }
        if(n<0) throw_errno("serialContextRead");
        return nb::bytes(data.data(), (size_t)n);
    }
    ssize_t read_into(nb::handle obj) {
        PyBufferGuard b(obj, PyBUF_WRITABLE | PyBUF_C_CONTIGUOUS); OpGuard op(*this); ssize_t n; int timeout_ms, inter_byte_timeout_ms;
        { std::lock_guard<std::mutex> lock(state_); timeout_ms=read_timeout_ms_; inter_byte_timeout_ms=inter_byte_timeout_ms_; }
        { nb::gil_scoped_release release; n=serialContextRead(op.ctx(), b.view.buf, (size_t)b.view.len, timeout_ms, inter_byte_timeout_ms); }
        if(n<0) throw_errno("serialContextRead"); return n;
    }
    ssize_t write(nb::handle obj) {
        PyBufferGuard b(obj, PyBUF_CONTIG_RO); OpGuard op(*this); ssize_t n; int timeout_ms;
        { std::lock_guard<std::mutex> lock(state_); timeout_ms=write_timeout_ms_; }
        { nb::gil_scoped_release release; n=serialContextWrite(op.ctx(), b.view.buf, (size_t)b.view.len, timeout_ms); }
        if(n<0) throw_errno("serialContextWrite"); return n;
    }
    nb::bytes read_all() { int count=in_waiting(); return read(count > 0 ? (size_t)count : 0); }
    nb::bytes read_until(nb::bytes expected, size_t size=0) {
        const char *needle=PyBytes_AS_STRING(expected.ptr()); size_t needle_len=(size_t)PyBytes_GET_SIZE(expected.ptr());
        if (needle_len == 0) throw nb::value_error("expected must not be empty");
        std::vector<char> out; if (size) out.reserve(size);
        while (!size || out.size() < size) {
            size_t want = 1;
            int waiting = in_waiting();
            if (waiting > 0) want=(size_t)waiting;
            if (size && want > size-out.size()) want=size-out.size();
            nb::bytes chunk=read(want); size_t n=(size_t)PyBytes_GET_SIZE(chunk.ptr());
            if (!n) break;
            const char *p=PyBytes_AS_STRING(chunk.ptr()); out.insert(out.end(),p,p+n);
            if (out.size() >= needle_len && std::search(out.begin(),out.end(),needle,needle+needle_len) != out.end()) break;
        }
        return nb::bytes(out.data(),out.size());
    }

    void flush() { drain(); }
    void drain() { OpGuard op(*this); int rc; { nb::gil_scoped_release r; rc=serialDrain(op.fd()); } if(rc<0) throw_errno("serialDrain"); }
    void reset_input_buffer() { OpGuard op(*this); if(serialFlushInput(op.fd())<0) throw_errno("serialFlushInput"); }
    void reset_output_buffer() { OpGuard op(*this); if(serialFlushOutput(op.fd())<0) throw_errno("serialFlushOutput"); }
    int in_waiting() { OpGuard op(*this); int v=serialInputWaiting(op.fd()); if(v<0) throw_errno("serialInputWaiting"); return v; }
    int out_waiting() { OpGuard op(*this); int v=serialOutputWaiting(op.fd()); if(v<0) throw_errno("serialOutputWaiting"); return v; }
    void send_break(double duration=0.25) { if(duration<0)throw nb::value_error("duration must be non-negative"); OpGuard op(*this); int ms=(int)(duration*1000.0+0.5); int rc; {nb::gil_scoped_release r;rc=serialSendBreak(op.fd(),(unsigned int)ms);} if(rc<0)throw_errno("serialSendBreak"); }
    bool break_condition() const { std::lock_guard<std::mutex> lock(state_); return break_condition_; }
    void set_break_condition(bool on) { OpGuard op(*this); if(serialSetBreak(op.fd(),on?1:0)<0)throw_errno("serialSetBreak"); std::lock_guard<std::mutex> lock(state_);break_condition_=on; }

    bool rts() { OpGuard op(*this); unsigned int l=0;if(serialGetModemLines(op.fd(),&l)<0)throw_errno("serialGetModemLines");return(l&SERIAL_MODEM_RTS)!=0; }
    void set_rts(bool v) { OpGuard op(*this);if(serialSetRTS(op.fd(),v?1:0)<0)throw_errno("serialSetRTS"); }
    bool dtr() { OpGuard op(*this); unsigned int l=0;if(serialGetModemLines(op.fd(),&l)<0)throw_errno("serialGetModemLines");return(l&SERIAL_MODEM_DTR)!=0; }
    void set_dtr(bool v) { OpGuard op(*this);if(serialSetDTR(op.fd(),v?1:0)<0)throw_errno("serialSetDTR"); }
    bool cts(){OpGuard op(*this);int v=serialGetCTS(op.fd());if(v<0)throw_errno("serialGetCTS");return v!=0;}
    bool dsr(){OpGuard op(*this);int v=serialGetDSR(op.fd());if(v<0)throw_errno("serialGetDSR");return v!=0;}
    bool ri(){OpGuard op(*this);int v=serialGetRI(op.fd());if(v<0)throw_errno("serialGetRI");return v!=0;}
    bool cd(){OpGuard op(*this);int v=serialGetCD(op.fd());if(v<0)throw_errno("serialGetCD");return v!=0;}
    void set_input_flow_control(bool v){OpGuard op(*this);if(serialSetInputFlow(op.fd(),v?1:0)<0)throw_errno("serialSetInputFlow");}
    void set_output_flow_control(bool v){OpGuard op(*this);if(serialSetOutputFlow(op.fd(),v?1:0)<0)throw_errno("serialSetOutputFlow");}

    bool exclusive() const { std::lock_guard<std::mutex> lock(state_); return exclusive_; }
    void set_exclusive(bool v){OpGuard op(*this);if(serialSetExclusive(op.fd(),v?1:0)<0)throw_errno("serialSetExclusive");std::lock_guard<std::mutex>lock(state_);exclusive_=v;}
    bool low_latency(){OpGuard op(*this);int v=serialGetLowLatency(op.fd());if(v<0)throw_errno("serialGetLowLatency");return v!=0;}
    void set_low_latency(bool v){OpGuard op(*this);if(serialSetLowLatency(op.fd(),v?1:0)<0)throw_errno("serialSetLowLatency");}
    serialCounters counters(){OpGuard op(*this);serialCounters c{};if(serialGetCounters(op.fd(),&c)<0)throw_errno("serialGetCounters");return c;}
    bool tx_empty(){OpGuard op(*this);int v=serialTxEmpty(op.fd());if(v<0)throw_errno("serialTxEmpty");return v!=0;}
    serialRS485Config rs485_mode(){OpGuard op(*this);serialRS485Config c{};c.structSize=sizeof(c);if(serialGetRS485(op.fd(),&c)<0)throw_errno("serialGetRS485");return c;}
    void set_rs485_mode(const serialRS485Config &c){OpGuard op(*this);if(serialSetRS485(op.fd(),&c)<0)throw_errno("serialSetRS485");}
    int rx_trigger(){OpGuard op(*this);int v=serialGetRxTrigger(op.fd());if(v<0)throw_errno("serialGetRxTrigger");return v;}
    void set_rx_trigger(int v){OpGuard op(*this);if(serialSetRxTrigger(op.fd(),(unsigned int)v)<0)throw_errno("serialSetRxTrigger");}
    bool wakeup(){OpGuard op(*this);int v=serialGetWakeup(op.fd());if(v<0)throw_errno("serialGetWakeup");return v!=0;}
    void set_wakeup(bool v){OpGuard op(*this);if(serialSetWakeup(op.fd(),v?1:0)<0)throw_errno("serialSetWakeup");}
    serialHardwareInfo hardware_info(){OpGuard op(*this);serialHardwareInfo i{};if(serialGetHardwareInfo(op.fd(),&i)<0)throw_errno("serialGetHardwareInfo");return i;}
    uint64_t capabilities(){OpGuard op(*this);uint64_t c=0;if(serialGetCapabilities(op.fd(),&c)<0)throw_errno("serialGetCapabilities");return c;}

    void cancel_read(){OpGuard op(*this);if(serialContextCancelRead(op.ctx())<0)throw_errno("serialContextCancelRead");}
    void cancel_write(){OpGuard op(*this);if(serialContextCancelWrite(op.ctx())<0)throw_errno("serialContextCancelWrite");}

private:
    void open_locked() {
        ctx_ = serialContextOpen(device_.c_str(), &config_cache_);
        if (!ctx_) throw_errno("serialContextOpen");
        int fd=serialContextGetFd(ctx_);
        if (fd < 0) fail_open_locked("serialContextGetFd");
        // These two properties are cached Python-side state, like pySerial's
        // break/exclusive settings. Reapply them when a previously closed port
        // is opened again so the property value cannot diverge from the OS state.
        if (break_condition_ && serialSetBreak(fd,1) < 0) fail_open_locked("serialSetBreak");
        if (exclusive_ && serialSetExclusive(fd,1) < 0) fail_open_locked("serialSetExclusive");
    }
    [[noreturn]] void fail_open_locked(const char *op) {
        int e=errno; serialContext *ctx=ctx_; ctx_=nullptr; serialContextClose(ctx); errno=e; throw_errno(op);
    }
    [[noreturn]] static void throw_errno(const char *op){int e=errno;throw std::runtime_error(std::string(op)+" failed: "+std::strerror(e));}
    std::string device_;
    serialConfig config_cache_{};
    serialContext *ctx_=nullptr;
    int read_timeout_ms_=-1,write_timeout_ms_=-1,inter_byte_timeout_ms_=-1;
    mutable std::mutex state_;
    std::condition_variable idle_;
    size_t active_ops_=0;
    bool closing_=false,break_condition_=false,exclusive_=false;
};

static void bind_serial_port(nb::module_ &m) {
    nb::class_<SerialPort>(m,"SerialPort")
      .def(nb::init<const char *,int>(),nb::arg("port"),nb::arg("baudrate")=115200)
      .def(nb::init<const char *,const serialConfig &>(),nb::arg("port"),nb::arg("config"))
      .def("open",&SerialPort::open)
      // close() can wait for an I/O method whose nanobind GIL guard must reacquire
      // the GIL before its OpGuard decrements active_ops_. Do not hold the GIL here.
      .def("close",&SerialPort::close,nb::call_guard<nb::gil_scoped_release>())
      .def_prop_ro("is_open",&SerialPort::is_open).def("fileno",&SerialPort::fileno)
      .def_prop_ro("port",&SerialPort::port).def_prop_ro("name",&SerialPort::name)
      .def_prop_rw("config",&SerialPort::config,&SerialPort::set_config)
      .def_prop_rw("baudrate",&SerialPort::baudrate,&SerialPort::set_baudrate)
      .def_prop_rw("baud",&SerialPort::baudrate,&SerialPort::set_baudrate)
      .def_prop_rw("bytesize",&SerialPort::bytesize,&SerialPort::set_bytesize)
      .def_prop_rw("parity",&SerialPort::parity,&SerialPort::set_parity)
      .def_prop_rw("stopbits",&SerialPort::stopbits,&SerialPort::set_stopbits)
      .def_prop_rw("xonxoff",&SerialPort::xonxoff,&SerialPort::set_xonxoff)
      .def_prop_rw("rtscts",&SerialPort::rtscts,&SerialPort::set_rtscts)
      .def_prop_rw("dsrdtr",&SerialPort::dsrdtr,&SerialPort::set_dsrdtr)
      .def_prop_rw("timeout",&SerialPort::timeout,&SerialPort::set_timeout,nb::for_setter(nb::arg("value").none()))
      .def_prop_rw("write_timeout",&SerialPort::write_timeout,&SerialPort::set_write_timeout,nb::for_setter(nb::arg("value").none()))
      .def_prop_rw("inter_byte_timeout",&SerialPort::inter_byte_timeout,&SerialPort::set_inter_byte_timeout,nb::for_setter(nb::arg("value").none()))
      .def_prop_rw("read_timeout_ms",&SerialPort::read_timeout_ms,&SerialPort::set_read_timeout_ms)
      .def_prop_rw("write_timeout_ms",&SerialPort::write_timeout_ms,&SerialPort::set_write_timeout_ms)
      .def_prop_rw("inter_byte_timeout_ms",&SerialPort::inter_byte_timeout_ms,&SerialPort::set_inter_byte_timeout_ms)
      .def("read",&SerialPort::read,nb::arg("size")=1)
      .def("read_into",&SerialPort::read_into,nb::arg("buffer"))
      .def("readinto",&SerialPort::read_into,nb::arg("buffer"))
      .def("write",&SerialPort::write,nb::arg("data"))
      .def("read_all",&SerialPort::read_all)
      .def("read_until",&SerialPort::read_until,nb::arg("expected")=nb::bytes("\n"),nb::arg("size")=0)
      .def("flush",&SerialPort::flush).def("drain",&SerialPort::drain)
      .def("reset_input_buffer",&SerialPort::reset_input_buffer).def("reset_output_buffer",&SerialPort::reset_output_buffer)
      .def_prop_ro("in_waiting",&SerialPort::in_waiting).def_prop_ro("out_waiting",&SerialPort::out_waiting)
      .def("send_break",&SerialPort::send_break,nb::arg("duration")=0.25)
      .def_prop_rw("break_condition",&SerialPort::break_condition,&SerialPort::set_break_condition)
      .def_prop_rw("rts",&SerialPort::rts,&SerialPort::set_rts).def_prop_rw("dtr",&SerialPort::dtr,&SerialPort::set_dtr)
      .def_prop_ro("cts",&SerialPort::cts).def_prop_ro("dsr",&SerialPort::dsr).def_prop_ro("ri",&SerialPort::ri).def_prop_ro("cd",&SerialPort::cd)
      .def("set_input_flow_control",&SerialPort::set_input_flow_control,nb::arg("enable"))
      .def("set_output_flow_control",&SerialPort::set_output_flow_control,nb::arg("enable"))
      .def_prop_rw("exclusive",&SerialPort::exclusive,&SerialPort::set_exclusive)
      .def_prop_rw("low_latency",&SerialPort::low_latency,&SerialPort::set_low_latency)
      .def_prop_ro("counters",&SerialPort::counters).def_prop_ro("tx_empty",&SerialPort::tx_empty)
      .def_prop_rw("rs485_mode",&SerialPort::rs485_mode,&SerialPort::set_rs485_mode)
      .def_prop_rw("rs485",&SerialPort::rs485_mode,&SerialPort::set_rs485_mode)
      .def_prop_rw("rx_trigger",&SerialPort::rx_trigger,&SerialPort::set_rx_trigger)
      .def_prop_rw("wakeup",&SerialPort::wakeup,&SerialPort::set_wakeup)
      .def_prop_ro("hardware_info",&SerialPort::hardware_info).def_prop_ro("capabilities",&SerialPort::capabilities)
      .def("cancel_read",&SerialPort::cancel_read).def("cancel_write",&SerialPort::cancel_write);
}
NB_MODULE(wiring_serial, m) {
  m.doc() = "nanobind bindings for wiringPi/wiringSerial.h";
  auto cls_SerialConfig = nb::class_<serialConfig>(m, "SerialConfig").def(nb::init<>());
  cls_SerialConfig.def_rw("struct_size", &serialConfig::structSize);
  cls_SerialConfig.def_rw("version", &serialConfig::version);
  cls_SerialConfig.def_rw("baud", &serialConfig::baud);
  cls_SerialConfig.def_rw("data_bits", &serialConfig::dataBits);
  cls_SerialConfig.def_rw("parity", &serialConfig::parity);
  cls_SerialConfig.def_rw("stop_bits", &serialConfig::stopBits);
  cls_SerialConfig.def_rw("flow_control", &serialConfig::flowControl);
  cls_SerialConfig.def_rw("xon_char", &serialConfig::xonChar);
  cls_SerialConfig.def_rw("xoff_char", &serialConfig::xoffChar);
  cls_SerialConfig.def_rw("vmin", &serialConfig::vmin);
  cls_SerialConfig.def_rw("vtime", &serialConfig::vtime);
  cls_SerialConfig.def_prop_rw("reserved", [](serialConfig &self) { nb::list out; const uint32_t *p = reinterpret_cast<const uint32_t *>(&self.reserved[0]); for (size_t i=0;i<4;++i) out.append(p[i]); return nb::tuple(out); }, [](serialConfig &self, nb::sequence seq) { if (nb::len(seq) != 4) throw nb::value_error("reserved must contain exactly 4 items"); uint32_t *p = reinterpret_cast<uint32_t *>(&self.reserved[0]); for (size_t i=0;i<4;++i) p[i]=nb::cast<uint32_t>(seq[i]); });
  auto cls_SerialRS485Config = nb::class_<serialRS485Config>(m, "SerialRS485Config").def(nb::init<>());
  cls_SerialRS485Config.def_rw("struct_size", &serialRS485Config::structSize);
  cls_SerialRS485Config.def_rw("flags", &serialRS485Config::flags);
  cls_SerialRS485Config.def_rw("delay_before_send_ms", &serialRS485Config::delayBeforeSendMs);
  cls_SerialRS485Config.def_rw("delay_after_send_ms", &serialRS485Config::delayAfterSendMs);
  cls_SerialRS485Config.def_rw("receive_address", &serialRS485Config::receiveAddress);
  cls_SerialRS485Config.def_rw("destination_address", &serialRS485Config::destinationAddress);
  cls_SerialRS485Config.def_prop_rw("reserved8", [](serialRS485Config &self) { return nb::bytes(reinterpret_cast<const char *>(&self.reserved8[0]), 2); }, [](serialRS485Config &self, nb::bytes value) { if (nb::len(value) != 2) throw nb::value_error("reserved8 must contain exactly 2 bytes"); std::memcpy(&self.reserved8[0], PyBytes_AS_STRING(value.ptr()), 2); });
  cls_SerialRS485Config.def_prop_rw("reserved", [](serialRS485Config &self) { nb::list out; const uint32_t *p = reinterpret_cast<const uint32_t *>(&self.reserved[0]); for (size_t i=0;i<4;++i) out.append(p[i]); return nb::tuple(out); }, [](serialRS485Config &self, nb::sequence seq) { if (nb::len(seq) != 4) throw nb::value_error("reserved must contain exactly 4 items"); uint32_t *p = reinterpret_cast<uint32_t *>(&self.reserved[0]); for (size_t i=0;i<4;++i) p[i]=nb::cast<uint32_t>(seq[i]); });
  auto cls_SerialCounters = nb::class_<serialCounters>(m, "SerialCounters").def(nb::init<>());
  cls_SerialCounters.def_rw("struct_size", &serialCounters::structSize);
  cls_SerialCounters.def_rw("cts", &serialCounters::cts);
  cls_SerialCounters.def_rw("dsr", &serialCounters::dsr);
  cls_SerialCounters.def_rw("rng", &serialCounters::rng);
  cls_SerialCounters.def_rw("dcd", &serialCounters::dcd);
  cls_SerialCounters.def_rw("rx", &serialCounters::rx);
  cls_SerialCounters.def_rw("tx", &serialCounters::tx);
  cls_SerialCounters.def_rw("frame", &serialCounters::frame);
  cls_SerialCounters.def_rw("overrun", &serialCounters::overrun);
  cls_SerialCounters.def_rw("parity", &serialCounters::parity);
  cls_SerialCounters.def_rw("brk", &serialCounters::brk);
  cls_SerialCounters.def_rw("buf_overrun", &serialCounters::bufOverrun);
  cls_SerialCounters.def_prop_rw("reserved", [](serialCounters &self) { nb::list out; const uint32_t *p = reinterpret_cast<const uint32_t *>(&self.reserved[0]); for (size_t i=0;i<4;++i) out.append(p[i]); return nb::tuple(out); }, [](serialCounters &self, nb::sequence seq) { if (nb::len(seq) != 4) throw nb::value_error("reserved must contain exactly 4 items"); uint32_t *p = reinterpret_cast<uint32_t *>(&self.reserved[0]); for (size_t i=0;i<4;++i) p[i]=nb::cast<uint32_t>(seq[i]); });
  auto cls_SerialHardwareInfo = nb::class_<serialHardwareInfo>(m, "SerialHardwareInfo").def(nb::init<>());
  cls_SerialHardwareInfo.def_rw("struct_size", &serialHardwareInfo::structSize);
  cls_SerialHardwareInfo.def_rw("hardware_type", &serialHardwareInfo::hardwareType);
  cls_SerialHardwareInfo.def_rw("fifo_size", &serialHardwareInfo::fifoSize);
  cls_SerialHardwareInfo.def_rw("baud_base", &serialHardwareInfo::baudBase);
  cls_SerialHardwareInfo.def_rw("port_type", &serialHardwareInfo::portType);
  cls_SerialHardwareInfo.def_rw("line", &serialHardwareInfo::line);
  cls_SerialHardwareInfo.def_rw("capabilities", &serialHardwareInfo::capabilities);
  cls_SerialHardwareInfo.def_prop_rw("reserved", [](serialHardwareInfo &self) { nb::list out; const uint32_t *p = reinterpret_cast<const uint32_t *>(&self.reserved[0]); for (size_t i=0;i<6;++i) out.append(p[i]); return nb::tuple(out); }, [](serialHardwareInfo &self, nb::sequence seq) { if (nb::len(seq) != 6) throw nb::value_error("reserved must contain exactly 6 items"); uint32_t *p = reinterpret_cast<uint32_t *>(&self.reserved[0]); for (size_t i=0;i<6;++i) p[i]=nb::cast<uint32_t>(seq[i]); });
  m.def("serial_open", &serialOpen, nb::arg("device"), nb::arg("baud"));
  m.def("serial_close", &serialClose, nb::arg("fd"));
  m.def("serial_flush", &serialFlush, nb::arg("fd"));
  m.def("serial_putchar", &serialPutchar, nb::arg("fd"), nb::arg("c"));
  m.def("serial_puts", &serialPuts, nb::arg("fd"), nb::arg("s"));
  m.def("serial_printf", [](const int fd, const char *message) { return serialPrintf(fd, "%s", message); }, nb::arg("fd"), nb::arg("message"));
  m.def("serial_data_avail", &serialDataAvail, nb::arg("fd"));
  m.def("serial_getchar", &serialGetchar, nb::arg("fd"));
  m.def("serial_config_init", []() { serialConfig v{}; serialConfigInit(&v); return v; });
  m.def("serial_open_config", &serialOpenConfig, nb::arg("device"), nb::arg("config"));
  m.def("serial_get_config", [](int fd) { serialConfig v{}; int rc=serialGetConfig(fd,&v); return nb::make_tuple(rc,v); }, nb::arg("fd"));
  m.def("serial_set_config", &serialSetConfig, nb::arg("fd"), nb::arg("config"));
  m.def("serial_get_baud", [](int fd) { unsigned int v=0; int rc=serialGetBaud(fd,&v); return nb::make_tuple(rc,v); }, nb::arg("fd"));
  m.def("serial_set_baud", &serialSetBaud, nb::arg("fd"), nb::arg("baud"));
  m.def("serial_read", [](int fd,size_t count) { std::vector<char>b(count); ssize_t n; {nb::gil_scoped_release r;n=serialRead(fd,b.data(),count);} if(n<0)throw std::runtime_error("serial read failed"); return nb::bytes(b.data(),(size_t)n); }, nb::arg("fd"), nb::arg("count"));
  m.def("serial_write", [](int fd,nb::handle data) { PyBufferGuard b(data,PyBUF_CONTIG_RO); nb::gil_scoped_release r; return serialWrite(fd,b.view.buf,(size_t)b.view.len); }, nb::arg("fd"), nb::arg("data"));
  m.def("serial_read_timeout", [](int fd,size_t count,int timeout_ms,int inter_byte_timeout_ms) { std::vector<char>b(count); ssize_t n; {nb::gil_scoped_release r;n=serialReadTimeout(fd,b.data(),count,timeout_ms,inter_byte_timeout_ms);} if(n<0)throw std::runtime_error("serial read failed"); return nb::bytes(b.data(),(size_t)n); }, nb::arg("fd"), nb::arg("count"), nb::arg("timeout_ms"), nb::arg("inter_byte_timeout_ms")=-1);
  m.def("serial_write_timeout", [](int fd,nb::handle data,int timeout_ms) { PyBufferGuard b(data,PyBUF_CONTIG_RO); nb::gil_scoped_release r; return serialWriteTimeout(fd,b.view.buf,(size_t)b.view.len,timeout_ms); }, nb::arg("fd"), nb::arg("data"), nb::arg("timeout_ms"));
  m.def("serial_drain", &serialDrain, nb::arg("fd"));
  m.def("serial_flush_input", &serialFlushInput, nb::arg("fd"));
  m.def("serial_flush_output", &serialFlushOutput, nb::arg("fd"));
  m.def("serial_input_waiting", &serialInputWaiting, nb::arg("fd"));
  m.def("serial_output_waiting", &serialOutputWaiting, nb::arg("fd"));
  m.def("serial_send_break", &serialSendBreak, nb::arg("fd"), nb::arg("duration_ms"));
  m.def("serial_set_break", &serialSetBreak, nb::arg("fd"), nb::arg("enabled"));
  m.def("serial_get_modem_lines", [](int fd) { unsigned int v=0; int rc=serialGetModemLines(fd,&v); return nb::make_tuple(rc,v); }, nb::arg("fd"));
  m.def("serial_set_modem_lines", &serialSetModemLines, nb::arg("fd"), nb::arg("set_mask"), nb::arg("clear_mask"));
  m.def("serial_set_rts", &serialSetRTS, nb::arg("fd"), nb::arg("enabled"));
  m.def("serial_set_dtr", &serialSetDTR, nb::arg("fd"), nb::arg("enabled"));
  m.def("serial_get_cts", &serialGetCTS, nb::arg("fd"));
  m.def("serial_get_dsr", &serialGetDSR, nb::arg("fd"));
  m.def("serial_get_ri", &serialGetRI, nb::arg("fd"));
  m.def("serial_get_cd", &serialGetCD, nb::arg("fd"));
  m.def("serial_set_input_flow", &serialSetInputFlow, nb::arg("fd"), nb::arg("enabled"));
  m.def("serial_set_output_flow", &serialSetOutputFlow, nb::arg("fd"), nb::arg("enabled"));
  m.def("serial_set_exclusive", &serialSetExclusive, nb::arg("fd"), nb::arg("enabled"));
  m.def("serial_get_low_latency", &serialGetLowLatency, nb::arg("fd"));
  m.def("serial_set_low_latency", &serialSetLowLatency, nb::arg("fd"), nb::arg("enabled"));
  m.def("serial_get_counters", [](int fd) { serialCounters v{}; int rc=serialGetCounters(fd,&v); return nb::make_tuple(rc,v); }, nb::arg("fd"));
  m.def("serial_tx_empty", &serialTxEmpty, nb::arg("fd"));
  m.def("serial_get_rs485", [](int fd) { serialRS485Config v{}; v.structSize=sizeof(v); int rc=serialGetRS485(fd,&v); return nb::make_tuple(rc,v); }, nb::arg("fd"));
  m.def("serial_set_rs485", &serialSetRS485, nb::arg("fd"), nb::arg("config"));
  m.def("serial_get_rx_trigger", &serialGetRxTrigger, nb::arg("fd"));
  m.def("serial_set_rx_trigger", &serialSetRxTrigger, nb::arg("fd"), nb::arg("bytes"));
  m.def("serial_get_wakeup", &serialGetWakeup, nb::arg("fd"));
  m.def("serial_set_wakeup", &serialSetWakeup, nb::arg("fd"), nb::arg("enabled"));
  m.def("serial_get_hardware_info", [](int fd) { serialHardwareInfo v{}; int rc=serialGetHardwareInfo(fd,&v); return nb::make_tuple(rc,v); }, nb::arg("fd"));
  m.def("serial_get_capabilities", [](int fd) { uint64_t v=0; int rc=serialGetCapabilities(fd,&v); return nb::make_tuple(rc,v); }, nb::arg("fd"));
  m.def("serial_context_open", [](const char *device,const serialConfig &cfg) -> uintptr_t { serialContext *q=serialContextOpen(device,&cfg); if(!q)throw std::runtime_error("serialContextOpen failed"); return reinterpret_cast<uintptr_t>(q); }, nb::arg("device"), nb::arg("config"));
  m.def("serial_context_from_fd", [](int fd,int take_ownership) -> uintptr_t { serialContext *q=serialContextFromFd(fd,take_ownership); if(!q)throw std::runtime_error("serialContextFromFd failed"); return reinterpret_cast<uintptr_t>(q); }, nb::arg("fd"), nb::arg("take_ownership")=0);
  m.def("serial_context_close", [](uintptr_t address) { serialContextClose(reinterpret_cast<serialContext*>(address)); }, nb::arg("address"));
  m.def("serial_context_get_fd", [](uintptr_t address) { return serialContextGetFd(reinterpret_cast<const serialContext*>(address)); }, nb::arg("address"));
  m.def("serial_context_read", [](uintptr_t address,size_t count,int timeout_ms,int inter_byte_timeout_ms) { std::vector<char>b(count); ssize_t n; {nb::gil_scoped_release r;n=serialContextRead(reinterpret_cast<serialContext*>(address),b.data(),count,timeout_ms,inter_byte_timeout_ms);} if(n<0)throw std::runtime_error("serialContextRead failed"); return nb::bytes(b.data(),(size_t)n); }, nb::arg("address"), nb::arg("count"), nb::arg("timeout_ms")=-1, nb::arg("inter_byte_timeout_ms")=-1);
  m.def("serial_context_write", [](uintptr_t address,nb::handle data,int timeout_ms) { PyBufferGuard b(data,PyBUF_CONTIG_RO); nb::gil_scoped_release r; return serialContextWrite(reinterpret_cast<serialContext*>(address),b.view.buf,(size_t)b.view.len,timeout_ms); }, nb::arg("address"), nb::arg("data"), nb::arg("timeout_ms")=-1);
  m.def("serial_context_cancel_read", [](uintptr_t address) { return serialContextCancelRead(reinterpret_cast<serialContext*>(address)); }, nb::arg("address"));
  m.def("serial_context_cancel_write", [](uintptr_t address) { return serialContextCancelWrite(reinterpret_cast<serialContext*>(address)); }, nb::arg("address"));

  m.attr("SERIAL_CONFIG_VERSION")=nb::cast((SERIAL_CONFIG_VERSION));
  m.attr("SERIAL_CONFIG_STRUCT_SIZE")=nb::cast((SERIAL_CONFIG_STRUCT_SIZE));
  m.attr("SERIAL_PARITY_NONE")=nb::cast((SERIAL_PARITY_NONE));
  m.attr("SERIAL_PARITY_ODD")=nb::cast((SERIAL_PARITY_ODD));
  m.attr("SERIAL_PARITY_EVEN")=nb::cast((SERIAL_PARITY_EVEN));
  m.attr("SERIAL_PARITY_MARK")=nb::cast((SERIAL_PARITY_MARK));
  m.attr("SERIAL_PARITY_SPACE")=nb::cast((SERIAL_PARITY_SPACE));
  m.attr("SERIAL_STOP_BITS_ONE")=nb::cast((SERIAL_STOP_BITS_ONE));
  m.attr("SERIAL_STOP_BITS_ONE_POINT_FIVE")=nb::cast((SERIAL_STOP_BITS_ONE_POINT_FIVE));
  m.attr("SERIAL_STOP_BITS_TWO")=nb::cast((SERIAL_STOP_BITS_TWO));
  m.attr("SERIAL_FLOW_NONE")=nb::cast((SERIAL_FLOW_NONE));
  m.attr("SERIAL_FLOW_XON_XOFF")=nb::cast((SERIAL_FLOW_XON_XOFF));
  m.attr("SERIAL_FLOW_RTS_CTS")=nb::cast((SERIAL_FLOW_RTS_CTS));
  m.attr("SERIAL_MODEM_RTS")=nb::cast((SERIAL_MODEM_RTS));
  m.attr("SERIAL_MODEM_DTR")=nb::cast((SERIAL_MODEM_DTR));
  m.attr("SERIAL_MODEM_CTS")=nb::cast((SERIAL_MODEM_CTS));
  m.attr("SERIAL_MODEM_DSR")=nb::cast((SERIAL_MODEM_DSR));
  m.attr("SERIAL_MODEM_RI")=nb::cast((SERIAL_MODEM_RI));
  m.attr("SERIAL_MODEM_CD")=nb::cast((SERIAL_MODEM_CD));
  m.attr("SERIAL_MODEM_LOOP")=nb::cast((SERIAL_MODEM_LOOP));
  m.attr("SERIAL_RS485_ENABLED")=nb::cast((SERIAL_RS485_ENABLED));
  m.attr("SERIAL_RS485_RTS_ON_SEND")=nb::cast((SERIAL_RS485_RTS_ON_SEND));
  m.attr("SERIAL_RS485_RTS_AFTER_SEND")=nb::cast((SERIAL_RS485_RTS_AFTER_SEND));
  m.attr("SERIAL_RS485_RX_DURING_TX")=nb::cast((SERIAL_RS485_RX_DURING_TX));
  m.attr("SERIAL_RS485_TERMINATE_BUS")=nb::cast((SERIAL_RS485_TERMINATE_BUS));
  m.attr("SERIAL_RS485_ADDRESS_MODE")=nb::cast((SERIAL_RS485_ADDRESS_MODE));
  m.attr("SERIAL_RS485_RX_ADDRESS")=nb::cast((SERIAL_RS485_RX_ADDRESS));
  m.attr("SERIAL_RS485_DEST_ADDRESS")=nb::cast((SERIAL_RS485_DEST_ADDRESS));
  m.attr("SERIAL_RS485_MODE_RS422")=nb::cast((SERIAL_RS485_MODE_RS422));
  m.attr("SERIAL_CAP_CUSTOM_BAUD")=nb::cast((SERIAL_CAP_CUSTOM_BAUD));
  m.attr("SERIAL_CAP_MARK_SPACE_PARITY")=nb::cast((SERIAL_CAP_MARK_SPACE_PARITY));
  m.attr("SERIAL_CAP_XON_XOFF")=nb::cast((SERIAL_CAP_XON_XOFF));
  m.attr("SERIAL_CAP_RTS_CTS")=nb::cast((SERIAL_CAP_RTS_CTS));
  m.attr("SERIAL_CAP_MODEM_CONTROL")=nb::cast((SERIAL_CAP_MODEM_CONTROL));
  m.attr("SERIAL_CAP_MODEM_STATUS")=nb::cast((SERIAL_CAP_MODEM_STATUS));
  m.attr("SERIAL_CAP_EXCLUSIVE")=nb::cast((SERIAL_CAP_EXCLUSIVE));
  m.attr("SERIAL_CAP_LOW_LATENCY")=nb::cast((SERIAL_CAP_LOW_LATENCY));
  m.attr("SERIAL_CAP_RS485")=nb::cast((SERIAL_CAP_RS485));
  m.attr("SERIAL_CAP_ICOUNT")=nb::cast((SERIAL_CAP_ICOUNT));
  m.attr("SERIAL_CAP_TX_EMPTY")=nb::cast((SERIAL_CAP_TX_EMPTY));
  m.attr("SERIAL_CAP_RX_TRIGGER")=nb::cast((SERIAL_CAP_RX_TRIGGER));
  m.attr("SERIAL_CAP_WAKEUP")=nb::cast((SERIAL_CAP_WAKEUP));
  m.attr("SERIAL_CAP_8250")=nb::cast((SERIAL_CAP_8250));
  m.attr("SERIAL_CAP_DW_APB_UART")=nb::cast((SERIAL_CAP_DW_APB_UART));
  m.attr("SERIAL_CAP_RK3588_UART")=nb::cast((SERIAL_CAP_RK3588_UART));
  m.attr("SERIAL_CAP_DMA_DESCRIBED")=nb::cast((SERIAL_CAP_DMA_DESCRIBED));
  m.attr("SERIAL_CAP_AUTO_RTS_CTS")=nb::cast((SERIAL_CAP_AUTO_RTS_CTS));
  m.attr("SERIAL_CAP_FIFO")=nb::cast((SERIAL_CAP_FIFO));
  m.attr("SERIAL_CAP_CANCEL_IO")=nb::cast((SERIAL_CAP_CANCEL_IO));
  m.attr("SERIAL_HARDWARE_UNKNOWN")=nb::cast((SERIAL_HARDWARE_UNKNOWN));
  m.attr("SERIAL_HARDWARE_8250")=nb::cast((SERIAL_HARDWARE_8250));
  m.attr("SERIAL_HARDWARE_DW_APB_UART")=nb::cast((SERIAL_HARDWARE_DW_APB_UART));
  m.attr("SERIAL_HARDWARE_RK3588_UART")=nb::cast((SERIAL_HARDWARE_RK3588_UART));
  bind_serial_port(m);
}
