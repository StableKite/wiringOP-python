#!/usr/bin/env python3
from __future__ import annotations
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'api_manifest.json'
UPSTREAM = ROOT / 'build/upstream/wiringOP'

SCALAR_TYPES = {
    'int','const int','unsigned int','const unsigned int','uint8_t','const uint8_t',
    'uint16_t','const uint16_t','uint32_t','const uint32_t','uint64_t','const uint64_t',
    'bool','ssize_t','size_t','const size_t','unsigned char','const unsigned char',
    'short','const short','unsigned short','const unsigned short','long','const long',
    'unsigned long','const unsigned long'
}
OPTIONAL_LEGACY_ARRAYS = {'piModelNames','piRevisionNames','piMakerNames','piMemorySize'}


def decl(t: str, n: str) -> str:
    if '(*)' in t:
        return t.replace('(*)', f'(*{n})')
    return f'{t} {n}'


def arg_ann(params: list[dict]) -> str:
    if not params:
        return ''
    return ', ' + ', '.join(f'nb::arg("{p["python_name"]}")' for p in params)


def module_basename(h: dict) -> str:
    return h['python_module'].rsplit('.', 1)[-1]


def py_rel_from_module(mod: str) -> Path:
    return Path(*mod.split('.')[1:])


def include_for(h: dict) -> str:
    return f'extern "C" {{\n#include "{h["path"]}"\n}}'


def cpp_type_name(ct: str) -> str:
    x = ct.strip().replace('const ', '').replace('volatile ', '').replace('struct ', '')
    x = x.replace('*', '').strip()
    return x


def struct_class_map(d: dict) -> dict[str, str]:
    out = {}
    for h in d['headers']:
        for s in h['structs']:
            out[s['c_name']] = s['python_name']
    return out


def preamble(h: dict) -> str:
    return f'''// Generated from api_manifest.json. Do not edit directly.
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
{include_for(h)}

namespace nb = nanobind;

'''


def bind_struct(s: dict) -> str:
    cn, py = s['c_name'], s['python_name']
    lines = [f'  auto cls_{py} = nb::class_<{cn}>(m, "{py}").def(nb::init<>());']
    for f in s['fields']:
        fn, pn, ct = f['name'], f['python_name'], f['c_type']
        if f['pointer']:
            lines.append(
                f'  cls_{py}.def_prop_rw("{pn}", '
                f'[]({cn} &self) -> uintptr_t {{ return reinterpret_cast<uintptr_t>(self.{fn}); }}, '
                f'[]({cn} &self, uintptr_t value) {{ self.{fn} = reinterpret_cast<decltype(self.{fn})>(value); }});'
            )
        elif '[' in ct:
            dims = [int(x) for x in re.findall(r'\[(\d+)\]', ct)]
            total = 1
            for x in dims:
                total *= x
            elem = ct.split('[')[0].strip().replace('const ', '')
            if elem in ('uint8_t', 'unsigned char', 'char'):
                lines.append(
                    f'  cls_{py}.def_prop_rw("{pn}", '
                    f'[]({cn} &self) {{ return nb::bytes(reinterpret_cast<const char *>(&self.{fn}[0]), {total}); }}, '
                    f'[]({cn} &self, nb::bytes value) {{ if (nb::len(value) != {total}) '
                    f'throw nb::value_error("{pn} must contain exactly {total} bytes"); '
                    f'std::memcpy(&self.{fn}[0], PyBytes_AS_STRING(value.ptr()), {total}); }});'
                )
            else:
                lines.append(
                    f'  cls_{py}.def_prop_rw("{pn}", '
                    f'[]({cn} &self) {{ nb::list out; const {elem} *p = reinterpret_cast<const {elem} *>(&self.{fn}[0]); '
                    f'for (size_t i=0;i<{total};++i) out.append(p[i]); return nb::tuple(out); }}, '
                    f'[]({cn} &self, nb::sequence seq) {{ if (nb::len(seq) != {total}) '
                    f'throw nb::value_error("{pn} must contain exactly {total} items"); '
                    f'{elem} *p = reinterpret_cast<{elem} *>(&self.{fn}[0]); '
                    f'for (size_t i=0;i<{total};++i) p[i]=nb::cast<{elem}>(seq[i]); }});'
                )
        else:
            lines.append(f'  cls_{py}.def_rw("{pn}", &{cn}::{fn});')
    return '\n'.join(lines)


def buffer_helpers() -> str:
    return r'''
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
'''


def callback_helpers() -> str:
    isr_cases = '\n'.join(f'    case {i}: return &isr_trampoline<{i}>;' for i in range(64))
    thr_cases = '\n'.join(f'    case {i}: return &thread_trampoline<{i}>;' for i in range(16))
    return f'''
static PyObject *g_isr_callbacks[MAX_PIN_NUM] = {{nullptr}};
static std::mutex g_isr_mutex;
template <size_t I> static void isr_trampoline() noexcept {{
    nb::gil_scoped_acquire gil;
    PyObject *cb = g_isr_callbacks[I];
    if (!cb) return;
    Py_INCREF(cb);
    PyObject *r = PyObject_CallNoArgs(cb);
    if (!r) PyErr_WriteUnraisable(cb); else Py_DECREF(r);
    Py_DECREF(cb);
}}
using IsrFn = void (*)();
static IsrFn isr_fn(size_t i) {{ switch(i) {{
{isr_cases}
    default: return nullptr; }} }}

static PyObject *g_thread_callbacks[16] = {{nullptr}};
static std::mutex g_thread_mutex;
template <size_t I> static void *thread_trampoline(void *) noexcept {{
    nb::gil_scoped_acquire gil;
    PyObject *cb = nullptr;
    {{ std::lock_guard<std::mutex> lock(g_thread_mutex); cb = g_thread_callbacks[I]; g_thread_callbacks[I] = nullptr; }}
    if (!cb) return nullptr;
    PyObject *r = PyObject_CallNoArgs(cb);
    if (!r) PyErr_WriteUnraisable(cb); else Py_DECREF(r);
    Py_DECREF(cb);
    return nullptr;
}}
using ThreadFn = void *(*)(void *);
static ThreadFn thread_fn(size_t i) {{ switch(i) {{
{thr_cases}
    default: return nullptr; }} }}
'''


def serial_port_class() -> str:
    # serialContext makes cancellation real (pipe wakeup inside the C layer). OpGuard
    # prevents context destruction racing with any method that is currently using it.
    return r'''
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
'''


def bind_function(f: dict) -> str:
    c, py, p, ad, rt = f['c_name'], f['python_name'], f['parameters'], f['adaptation'], f['return_type']
    anns = arg_ann(p)
    if ad == 'direct':
        policy = ', nb::rv_policy::reference' if '*' in rt else ''
        return f'  m.def("{py}", &{c}{policy}{anns});'
    if ad == 'missing':
        params = ', '.join(decl(x['c_type'], x['name']) for x in p)
        voids = ' '.join(f'(void){x["name"]};' for x in p)
        ret = '' if rt == 'void' else f' -> {rt}'
        return f'  m.def("{py}", []({params}){ret} {{ {voids} PyErr_SetString(PyExc_NotImplementedError, "{c} is declared by wiringOP but not implemented in this revision"); throw nb::python_error(); }}{anns});'
    if ad == 'legacy_typo':
        return '  m.def("get_response_legacy", [](int client_fd) { return getResponse(client_fd); }, nb::arg("client_fd"));'
    if ad == 'prepared_printf':
        nonmsg = p[:-1]
        params = ', '.join(decl(x['c_type'],x['name']) for x in nonmsg) + (', ' if nonmsg else '') + 'const char *message'
        args = ', '.join(x['name'] for x in nonmsg)
        call = (args + ', ' if args else '') + '"%s", message'
        return f'  m.def("{py}", []({params}) {{ return {c}({call}); }}' + arg_ann(nonmsg + [{'python_name':'message'}]) + ');'
    if ad == 'output_pointers':
        outs = [x for x in p if '*' in x['c_type'] and not x['c_type'].lstrip().startswith('const ')]
        ins = [x for x in p if x not in outs]
        defs, args = [], []
        for x in p:
            if x in outs:
                base = x['c_type'].replace('*','').replace('const ','').strip()
                defs.append(f'{base} {x["name"]}=0;'); args.append('&'+x['name'])
            else: args.append(x['name'])
        vals = ', '.join(x['name'] for x in outs)
        expr = outs[0]['name'] if rt=='void' and len(outs)==1 else (f'nb::make_tuple({vals})' if rt=='void' else f'nb::make_tuple(status, {vals})')
        prefix = '' if rt=='void' else f'{rt} status = '
        params = ', '.join(decl(x['c_type'],x['name']) for x in ins)
        return f'  m.def("{py}", []({params}) {{ {" ".join(defs)} {prefix}{c}({", ".join(args)}); return {expr}; }}' + arg_ann(ins) + ');'
    if ad == 'ds1302_clock_read':
        return f'  m.def("{py}", []() {{ int v[8]={{0}}; {c}(v); nb::list out; for(int x:v) out.append(x); return nb::tuple(out); }});'
    if ad == 'ds1302_clock_write':
        return f'  m.def("{py}", [](nb::sequence seq) {{ if(nb::len(seq)!=8) throw nb::value_error("clock_data must contain 8 items"); int v[8]; for(size_t i=0;i<8;++i)v[i]=nb::cast<int>(seq[i]); {c}(v); }}, nb::arg("clock_data"));'
    if ad == 'lcd_screen_size':
        return f'  m.def("{py}", []() {{ int x=0,y=0; {c}(&x,&y); return nb::make_tuple(x,y); }});'
    if ad == 'lcd_char_def':
        return f'  m.def("{py}", [](int fd,int index,nb::bytes data) {{ if(nb::len(data)!=8) throw nb::value_error("data must contain exactly 8 bytes"); unsigned char v[8]; std::memcpy(v,PyBytes_AS_STRING(data.ptr()),8); {c}(fd,index,v); }}, nb::arg("fd"), nb::arg("index"), nb::arg("data"));'
    if ad == 'maxdetect_read':
        return f'  m.def("{py}", [](int pin) {{ unsigned char b[4]={{0}}; int st={c}(pin,b); return nb::make_tuple(st, nb::bytes(reinterpret_cast<char*>(b),4)); }}, nb::arg("pin"));'
    if ad == 'rht03_read':
        return f'  m.def("{py}", [](int pin) {{ int temp=0,rh=0; int st={c}(pin,&temp,&rh); return nb::make_tuple(st,temp,rh); }}, nb::arg("pin"));'
    if ad == 'w25_manufacturer':
        return f'  m.def("{py}", []() {{ uint8_t b[3]={{0}}; {c}(b); return nb::bytes(reinterpret_cast<char*>(b),3); }});'
    if ad == 'w25_unique_id':
        return f'  m.def("{py}", []() {{ uint8_t b[7]={{0}}; {c}(b); return nb::bytes(reinterpret_cast<char*>(b),7); }});'
    if ad == 'w25_read':
        return f'  m.def("{py}", [](uint32_t addr,uint16_t n) {{ std::vector<uint8_t>b(n); uint16_t got={c}(addr,b.data(),n); if(got>b.size()) got=(uint16_t)b.size(); return nb::bytes(reinterpret_cast<char*>(b.data()),got); }}, nb::arg("addr"), nb::arg("n"));'
    if ad == 'w25_page_write':
        return f'  m.def("{py}", [](uint16_t sect_no,uint16_t inaddr,nb::handle data) {{ PyBufferGuard b(data,PyBUF_CONTIG_RO); if(b.view.len>255) throw nb::value_error("page write is limited to 255 bytes"); if((size_t)inaddr+(size_t)b.view.len>256) throw nb::value_error("write crosses a 256-byte page boundary"); return {c}(sect_no,inaddr,reinterpret_cast<uint8_t*>(b.view.buf),(uint8_t)b.view.len); }}, nb::arg("sect_no"), nb::arg("inaddr"), nb::arg("data"));'
    if ad == 'spi_inout_buffer':
        return f'  m.def("{py}", [](int channel,nb::handle data) {{ PyBufferGuard b(data,PyBUF_WRITABLE|PyBUF_C_CONTIGUOUS); return {c}(channel,reinterpret_cast<unsigned char*>(b.view.buf),(int)b.view.len); }}, nb::arg("channel"), nb::arg("data"));'
    if ad == 'callback_isr':
        return f'  m.def("{py}", [](int pin,int mode,nb::callable cb) {{ if(pin<0||pin>=MAX_PIN_NUM) throw nb::value_error("pin is outside MAX_PIN_NUM"); std::lock_guard<std::mutex> lock(g_isr_mutex); PyObject *q=cb.ptr(); Py_INCREF(q); Py_XDECREF(g_isr_callbacks[pin]); g_isr_callbacks[pin]=q; int rc={c}(pin,mode,isr_fn((size_t)pin)); if(rc<0) Py_CLEAR(g_isr_callbacks[pin]); return rc; }}, nb::arg("pin"), nb::arg("mode"), nb::arg("callback"));'
    if ad == 'callback_thread':
        return f'  m.def("{py}", [](nb::callable cb) {{ size_t slot=16; {{ std::lock_guard<std::mutex> lock(g_thread_mutex); for(size_t i=0;i<16;++i) if(!g_thread_callbacks[i]){{slot=i;Py_INCREF(cb.ptr());g_thread_callbacks[i]=cb.ptr();break;}} }} if(slot==16) throw std::runtime_error("no free callback slots"); int rc={c}(thread_fn(slot)); if(rc<0){{std::lock_guard<std::mutex> lock(g_thread_mutex);Py_CLEAR(g_thread_callbacks[slot]);}} return rc; }}, nb::arg("callback"));'
    if ad == 'mutable_c_string':
        params=[]; prep=[]; args=[]
        for x in p:
            if x['c_type']=='char *':
                params.append(f'const char *{x["name"]}'); prep.append(f'std::vector<char> {x["name"]}_buf({x["name"]},{x["name"]}+std::strlen({x["name"]})+1);'); args.append(x['name']+'_buf.data()')
            else: params.append(decl(x['c_type'],x['name'])); args.append(x['name'])
        return f'  m.def("{py}", []({", ".join(params)}) {{ {" ".join(prep)} return {c}({", ".join(args)}); }}{arg_ann(p)});'
    if ad == 'oled_open':
        return f'  m.def("{py}", [](display_info &disp,const char *filename) {{ std::vector<char>b(filename,filename+std::strlen(filename)+1); return {c}(&disp,b.data()); }}, nb::arg("disp"), nb::arg("filename"));'
    if ad == 'oled_send':
        return f'  m.def("{py}", [](display_info &disp,nb::handle payload) {{ PyBufferGuard b(payload,PyBUF_CONTIG_RO); sized_array s{{(int)b.view.len,reinterpret_cast<const uint8_t*>(b.view.buf)}}; return {c}(&disp,&s); }}, nb::arg("disp"), nb::arg("payload"));'
    if ad == 'oled_putstr':
        return f'  m.def("{py}", [](display_info &disp,uint8_t line,const char *text) {{ std::vector<uint8_t>b(text,text+std::strlen(text)+1); {c}(&disp,line,b.data()); }}, nb::arg("disp"), nb::arg("line"), nb::arg("text"));'
    if ad == 'oled_putstrto':
        return f'  m.def("{py}", [](display_info &disp,uint8_t x,uint8_t y,const char *text) {{ std::vector<char>b(text,text+std::strlen(text)+1); {c}(&disp,x,y,b.data()); }}, nb::arg("disp"), nb::arg("x"), nb::arg("y"), nb::arg("text"));'
    if ad == 'serial_config_init': return f'  m.def("{py}", []() {{ serialConfig v{{}}; {c}(&v); return v; }});'
    if ad == 'serial_get_config': return f'  m.def("{py}", [](int fd) {{ serialConfig v{{}}; int rc={c}(fd,&v); return nb::make_tuple(rc,v); }}, nb::arg("fd"));'
    if ad == 'serial_get_baud': return f'  m.def("{py}", [](int fd) {{ unsigned int v=0; int rc={c}(fd,&v); return nb::make_tuple(rc,v); }}, nb::arg("fd"));'
    if ad == 'serial_read': return f'  m.def("{py}", [](int fd,size_t count) {{ std::vector<char>b(count); ssize_t n; {{nb::gil_scoped_release r;n={c}(fd,b.data(),count);}} if(n<0)throw std::runtime_error("serial read failed"); return nb::bytes(b.data(),(size_t)n); }}, nb::arg("fd"), nb::arg("count"));'
    if ad == 'serial_write': return f'  m.def("{py}", [](int fd,nb::handle data) {{ PyBufferGuard b(data,PyBUF_CONTIG_RO); nb::gil_scoped_release r; return {c}(fd,b.view.buf,(size_t)b.view.len); }}, nb::arg("fd"), nb::arg("data"));'
    if ad == 'serial_read_timeout': return f'  m.def("{py}", [](int fd,size_t count,int timeout_ms,int inter_byte_timeout_ms) {{ std::vector<char>b(count); ssize_t n; {{nb::gil_scoped_release r;n={c}(fd,b.data(),count,timeout_ms,inter_byte_timeout_ms);}} if(n<0)throw std::runtime_error("serial read failed"); return nb::bytes(b.data(),(size_t)n); }}, nb::arg("fd"), nb::arg("count"), nb::arg("timeout_ms"), nb::arg("inter_byte_timeout_ms")=-1);'
    if ad == 'serial_write_timeout': return f'  m.def("{py}", [](int fd,nb::handle data,int timeout_ms) {{ PyBufferGuard b(data,PyBUF_CONTIG_RO); nb::gil_scoped_release r; return {c}(fd,b.view.buf,(size_t)b.view.len,timeout_ms); }}, nb::arg("fd"), nb::arg("data"), nb::arg("timeout_ms"));'
    if ad == 'serial_get_modem_lines': return f'  m.def("{py}", [](int fd) {{ unsigned int v=0; int rc={c}(fd,&v); return nb::make_tuple(rc,v); }}, nb::arg("fd"));'
    if ad == 'serial_get_counters': return f'  m.def("{py}", [](int fd) {{ serialCounters v{{}}; int rc={c}(fd,&v); return nb::make_tuple(rc,v); }}, nb::arg("fd"));'
    if ad == 'serial_get_rs485': return f'  m.def("{py}", [](int fd) {{ serialRS485Config v{{}}; v.structSize=sizeof(v); int rc={c}(fd,&v); return nb::make_tuple(rc,v); }}, nb::arg("fd"));'
    if ad == 'serial_get_hardware_info': return f'  m.def("{py}", [](int fd) {{ serialHardwareInfo v{{}}; int rc={c}(fd,&v); return nb::make_tuple(rc,v); }}, nb::arg("fd"));'
    if ad == 'serial_get_capabilities': return f'  m.def("{py}", [](int fd) {{ uint64_t v=0; int rc={c}(fd,&v); return nb::make_tuple(rc,v); }}, nb::arg("fd"));'
    if ad == 'serial_context_open': return f'  m.def("{py}", [](const char *device,const serialConfig &cfg) -> uintptr_t {{ serialContext *q={c}(device,&cfg); if(!q)throw std::runtime_error("serialContextOpen failed"); return reinterpret_cast<uintptr_t>(q); }}, nb::arg("device"), nb::arg("config"));'
    if ad == 'serial_context_from_fd': return f'  m.def("{py}", [](int fd,int take_ownership) -> uintptr_t {{ serialContext *q={c}(fd,take_ownership); if(!q)throw std::runtime_error("serialContextFromFd failed"); return reinterpret_cast<uintptr_t>(q); }}, nb::arg("fd"), nb::arg("take_ownership")=0);'
    if ad == 'serial_context_close': return f'  m.def("{py}", [](uintptr_t address) {{ {c}(reinterpret_cast<serialContext*>(address)); }}, nb::arg("address"));'
    if ad == 'serial_context_get_fd': return f'  m.def("{py}", [](uintptr_t address) {{ return {c}(reinterpret_cast<const serialContext*>(address)); }}, nb::arg("address"));'
    if ad == 'serial_context_read': return f'  m.def("{py}", [](uintptr_t address,size_t count,int timeout_ms,int inter_byte_timeout_ms) {{ std::vector<char>b(count); ssize_t n; {{nb::gil_scoped_release r;n={c}(reinterpret_cast<serialContext*>(address),b.data(),count,timeout_ms,inter_byte_timeout_ms);}} if(n<0)throw std::runtime_error("serialContextRead failed"); return nb::bytes(b.data(),(size_t)n); }}, nb::arg("address"), nb::arg("count"), nb::arg("timeout_ms")=-1, nb::arg("inter_byte_timeout_ms")=-1);'
    if ad == 'serial_context_write': return f'  m.def("{py}", [](uintptr_t address,nb::handle data,int timeout_ms) {{ PyBufferGuard b(data,PyBUF_CONTIG_RO); nb::gil_scoped_release r; return {c}(reinterpret_cast<serialContext*>(address),b.view.buf,(size_t)b.view.len,timeout_ms); }}, nb::arg("address"), nb::arg("data"), nb::arg("timeout_ms")=-1);'
    if ad in ('serial_context_cancel_read','serial_context_cancel_write'):
        return f'  m.def("{py}", [](uintptr_t address) {{ return {c}(reinterpret_cast<serialContext*>(address)); }}, nb::arg("address"));'
    raise RuntimeError(f'unhandled adaptation {ad} for {c}')


def bind_variables(h: dict) -> str:
    lines=[]
    for v in h['variables']:
        c, py, ct = v['c_name'], v['python_name'], v['c_type']
        if c in OPTIONAL_LEGACY_ARRAYS:
            if 'char *' in ct:
                n=int(re.findall(r'\[(\d+)\]',ct)[-1])
                lines.append(f'  {{ void *sym=dlsym(RTLD_DEFAULT,"{c}"); if(sym){{ const char * const *p=reinterpret_cast<const char * const *>(sym); nb::list x; for(size_t i=0;i<{n};++i)x.append(p[i]?nb::str(p[i]):nb::none()); m.attr("{py}")=nb::tuple(x); }} else m.attr("{py}")=nb::none(); }}')
            else:
                n=int(re.findall(r'\[(\d+)\]',ct)[-1])
                base=ct.split('[')[0].replace('const ','').strip()
                lines.append(f'  {{ void *sym=dlsym(RTLD_DEFAULT,"{c}"); if(sym){{ const {base} *p=reinterpret_cast<const {base} *>(sym); nb::list x; for(size_t i=0;i<{n};++i)x.append(p[i]); m.attr("{py}")=nb::tuple(x); }} else m.attr("{py}")=nb::none(); }}')
        elif '[' in ct:
            dims=[int(x) for x in re.findall(r'\[(\d+)\]',ct)];total=1
            for x in dims: total*=x
            base=ct.split('[')[0].strip()
            if 'char *' in base:
                lines.append(f'  {{ nb::list x; for(size_t i=0;i<{total};++i)x.append({c}[i]?nb::str({c}[i]):nb::none());m.attr("{py}")=nb::tuple(x); }}')
            elif 'char' in base or 'uint8_t' in base:
                lines.append(f'  m.attr("{py}")=nb::bytes(reinterpret_cast<const char *>(&{c}[0]),{total});')
            else:
                b=base.replace('const ','')
                lines.append(f'  {{nb::list x;const {b} *p=reinterpret_cast<const {b} *>(&{c}[0]);for(size_t i=0;i<{total};++i)x.append(p[i]);m.attr("{py}")=nb::tuple(x);}}')
        elif '*' in ct:
            lines.append(f'  m.def("get_{py}_address", []() -> uintptr_t {{ return reinterpret_cast<uintptr_t>({c}); }});')
            if 'const ' not in ct:
                lines.append(f'  m.def("set_{py}_address", [](uintptr_t value) {{ {c}=reinterpret_cast<decltype({c})>(value); }}, nb::arg("address"));')
        elif 'struct ' in ct:
            # static struct values are mutable in their translation unit: explicit accessors.
            if v['storage']=='static':
                st=ct.replace('struct ','').strip()
                lines.append(f'  m.def("get_{py}", []() {{ return {c}; }});')
                lines.append(f'  m.def("set_{py}", []({st} value) {{ {c}=value; }}, nb::arg("value"));')
            else:
                lines.append(f'  m.attr("{py}")=nb::cast({c},nb::rv_policy::reference);')
        elif ct.startswith('const '):
            lines.append(f'  m.attr("{py}")=nb::cast({c});')
        else:
            lines.append(f'  m.def("get_{py}", []() {{ return {c}; }});')
            lines.append(f'  m.def("set_{py}", [](decltype({c}) value) {{ {c}=value; }}, nb::arg("value"));')
    return '\n'.join(lines)


def bind_macros(h: dict) -> str:
    lines=[]
    for x in h['macros']:
        if not x.get('bindable'): continue
        c,py=x['c_name'],x['python_name']
        if x['kind']=='function_value':
            args=x.get('args') or ['x'];params=', '.join(f'int {a}' for a in args)
            lines.append(f'  m.def("{py}", []({params}) {{ return {c}({", ".join(args)}); }}'+''.join(f', nb::arg("{a}")' for a in args)+');')
        else:
            lines.append(f'  m.attr("{py}")=nb::cast(({c}));')
    return '\n'.join(lines)


def generate_cpp(d: dict, h: dict) -> str:
    adaptations={f['adaptation'] for f in h['functions']}
    needs_buffer=bool(adaptations & {'spi_inout_buffer','w25_page_write','oled_send','serial_write','serial_write_timeout','serial_context_write'})
    extra=buffer_helpers() if needs_buffer else ''
    if h['path']=='wiringPi/wiringPi.h': extra+=callback_helpers()
    if h['path']=='wiringPi/wiringSerial.h':
        if 'struct PyBufferGuard' not in extra: extra+=buffer_helpers()
        extra+=serial_port_class()
    importdep='  nb::module_::import_("wiringop.wiring_pi.font");\n' if h['path']=='wiringPi/oled.h' else ''
    out=[preamble(h),extra,f'NB_MODULE({module_basename(h)}, m) {{\n  m.doc() = "nanobind bindings for {h["path"]}";\n',importdep]
    for s in h['structs']: out.append(bind_struct(s)+'\n')
    for f in h['functions']: out.append(bind_function(f)+'\n')
    out.append(bind_variables(h)+'\n'); out.append(bind_macros(h)+'\n')
    if h['path']=='wiringPi/wiringSerial.h': out.append('  bind_serial_port(m);\n')
    out.append('}\n')
    return ''.join(out)


def mock_return(rt: str) -> str:
    if rt=='void': return ''
    if '*' in rt: return 'return NULL;'
    if rt=='bool': return 'return true;'
    return 'return 1;'


def mock_body(f: dict) -> str | None:
    c,rt,p=f['c_name'],f['return_type'],f['parameters']
    if c=='wiringPiVersion': return '*major=2;*minor=61;'
    if c=='piBoardId': return '*model=17;'
    if c=='ds1302clockRead': return 'for(int i=0;i<8;++i)clockData[i]=10+i;'
    if c=='lcd128x64orientCoordinates': return '*x+=1;*y+=2;'
    if c=='lcd128x64getScreenSize': return '*x=128;*y=64;'
    if c=='maxDetectRead': return 'buffer[0]=1;buffer[1]=2;buffer[2]=3;buffer[3]=4;return 1;'
    if c=='readRHT03': return '*temp=234;*rh=567;return 1;'
    if c=='W25Q64_readManufacturer': return 'd[0]=0xEF;d[1]=0x40;d[2]=0x17;'
    if c=='W25Q64_readUniqieID': return 'for(int i=0;i<7;++i)d[i]=(uint8_t)(0x10+i);'
    if c in ('W25Q64_read','W25Q64_fastread'): return 'for(uint16_t i=0;i<n;++i)buf[i]=(uint8_t)(addr+i);return n;'
    if c=='W25Q64_pageWrite': return '(void)sect_no;(void)inaddr;(void)data;return n;'
    if c=='wiringPiSPIDataRW': return 'for(int i=0;i<len;++i)data[i]^=0xA5;return len;'
    if c=='wiringPiISR': return 'if(function)function();return 0;'
    if c=='piThreadCreate': return 'if(fn)fn(NULL);return 0;'
    if c=='getClientIP': return 'return "127.0.0.1";'
    if c=='getResponse': return 'return clientFd+100;'
    if c=='oled_open': return 'disp->file=42;disp->address=0x3c;(void)filename;return 0;'
    if c=='oled_send': return '(void)disp;return payload?payload->size:-1;'
    if c=='serialConfigInit': return 'memset(config,0,sizeof(*config));config->structSize=sizeof(*config);config->version=SERIAL_CONFIG_VERSION;config->baud=9600;config->dataBits=8;config->parity=SERIAL_PARITY_NONE;config->stopBits=SERIAL_STOP_BITS_ONE;config->xonChar=0x11;config->xoffChar=0x13;'
    if c=='serialOpen': return '(void)device;mock_serial_config.baud=(uint32_t)baud;return 7;'
    if c=='serialOpenConfig': return '(void)device;if(config)mock_serial_config=*config;return 7;'
    if c=='serialGetConfig': return '(void)fd;*config=mock_serial_config;return 0;'
    if c=='serialSetConfig': return '(void)fd;mock_serial_config=*config;return 0;'
    if c=='serialGetBaud': return '(void)fd;*baud=mock_serial_config.baud;return 0;'
    if c=='serialSetBaud': return '(void)fd;mock_serial_config.baud=baud;return 0;'
    if c in ('serialRead','serialReadTimeout'):
        extra='(void)timeoutMs;(void)interByteTimeoutMs;' if c=='serialReadTimeout' else ''
        return f'(void)fd;{extra}for(size_t i=0;i<count;++i)((unsigned char*)buffer)[i]=(unsigned char)(0x30+(i%10));return(ssize_t)count;'
    if c in ('serialWrite','serialWriteTimeout'):
        extra='(void)timeoutMs;' if c=='serialWriteTimeout' else ''
        return f'(void)fd;(void)buffer;{extra}return(ssize_t)count;'
    if c in ('serialInputWaiting','serialOutputWaiting'): return '(void)fd;return 3;'
    if c=='serialGetModemLines': return '(void)fd;*lines=SERIAL_MODEM_RTS|SERIAL_MODEM_DTR|SERIAL_MODEM_CTS;return 0;'
    if c in ('serialGetCTS','serialGetDSR','serialGetRI','serialGetCD'): return '(void)fd;return 1;'
    if c=='serialGetLowLatency': return '(void)fd;return 1;'
    if c=='serialGetCounters': return '(void)fd;memset(counters,0,sizeof(*counters));counters->structSize=sizeof(*counters);counters->rx=12;counters->tx=34;return 0;'
    if c=='serialTxEmpty': return '(void)fd;return 1;'
    if c=='serialGetRS485': return '(void)fd;*config=mock_rs485;config->structSize=sizeof(*config);return 0;'
    if c=='serialSetRS485': return '(void)fd;mock_rs485=*config;return 0;'
    if c=='serialGetRxTrigger': return '(void)fd;return mock_rx_trigger;'
    if c=='serialSetRxTrigger': return '(void)fd;mock_rx_trigger=(int)bytes;return 0;'
    if c=='serialGetWakeup': return '(void)fd;return mock_wakeup;'
    if c=='serialSetWakeup': return '(void)fd;mock_wakeup=enabled;return 0;'
    if c=='serialGetHardwareInfo': return '(void)fd;memset(info,0,sizeof(*info));info->structSize=sizeof(*info);info->hardwareType=SERIAL_HARDWARE_RK3588_UART;info->fifoSize=64;info->capabilities=SERIAL_CAP_CUSTOM_BAUD|SERIAL_CAP_RTS_CTS|SERIAL_CAP_RK3588_UART|SERIAL_CAP_FIFO|SERIAL_CAP_CANCEL_IO;return 0;'
    if c=='serialGetCapabilities': return '(void)fd;*capabilities=SERIAL_CAP_CUSTOM_BAUD|SERIAL_CAP_RTS_CTS|SERIAL_CAP_RK3588_UART|SERIAL_CAP_FIFO|SERIAL_CAP_CANCEL_IO;return 0;'
    if c=='serialContextOpen': return '(void)device;if(config)mock_serial_config=*config;mock_context.fd=7;return &mock_context;'
    if c=='serialContextFromFd': return '(void)takeOwnership;mock_context.fd=fd;return &mock_context;'
    if c=='serialContextClose': return '(void)context;'
    if c=='serialContextGetFd': return 'return context?context->fd:-1;'
    if c=='serialContextRead': return '(void)timeoutMs;(void)interByteTimeoutMs;if(!context)return-1;for(size_t i=0;i<count;++i)((unsigned char*)buffer)[i]=(unsigned char)(0x30+(i%10));return(ssize_t)count;'
    if c=='serialContextWrite': return '(void)timeoutMs;if(!context)return-1;(void)buffer;return(ssize_t)count;'
    if c in ('serialContextCancelRead','serialContextCancelWrite'): return 'return context?0:-1;'
    if c in ('digitalRead8','digitalWrite8','wiringPiSetupPiFace','wiringPiSetupPiFaceForGpioProg','getResponce'): return None
    uses=''.join(f'(void){x["name"]};' for x in p)
    return uses+mock_return(rt)


def generate_mock(h: dict) -> str:
    lines=['#include <stdint.h>\n#include <stddef.h>\n#include <stdbool.h>\n#include <string.h>\n',f'#include "{h["path"]}"\n']
    if h['path']=='wiringPi/wiringSerial.h':
        lines.append('struct serialContext { int fd; int ownFd; int cancelRead[2]; int cancelWrite[2]; };\nstatic serialConfig mock_serial_config={.structSize=sizeof(serialConfig),.version=SERIAL_CONFIG_VERSION,.baud=9600,.dataBits=8,.stopBits=SERIAL_STOP_BITS_ONE};\nstatic serialRS485Config mock_rs485={.structSize=sizeof(serialRS485Config)};\nstatic struct serialContext mock_context={.fd=7};\nstatic int mock_rx_trigger=16;static int mock_wakeup=0;\n')
    for v in h['variables']:
        if v['storage']!='extern': continue
        ct,c=v['c_type'],v['c_name']
        if '[' in ct:
            base=ct.split('[')[0].strip();dims=''.join(re.findall(r'\[\d+\]',ct));lines.append(f'{base} {c}{dims}={{0}};\n')
        else: lines.append(f'{ct} {c}=0;\n')
    for f in h['functions']:
        body=mock_body(f)
        if body is None: continue
        params=', '.join(decl(x['c_type'],x['name']) for x in f['parameters']) or 'void'
        if f['variadic']: params+=', ...'
        lines.append(f'{f["return_type"]} {f["c_name"]}({params}) {{ {body} }}\n')
    return ''.join(lines)


def test_value_for_param(p: dict, structs: dict[str,str]) -> str:
    t=p['c_type']
    if t=='bool': return 'True'
    if t in SCALAR_TYPES: return '1'
    if t=='const char *': return '"x"'
    if '*' in t:
        cn=cpp_type_name(t)
        if cn in structs: return f'm.{structs[cn]}()'
        return '0'
    return '1'


def generate_test(d: dict,h: dict,structs: dict[str,str]) -> str:
    lines=[f'import importlib\nimport pytest\n\nm=importlib.import_module("{h["python_module"]}")\n']
    for s in h['structs']:
        lines.append(f'\ndef test_struct_{s["python_name"].lower()}():\n    obj=m.{s["python_name"]}()\n')
        for fld in s['fields']:
            pn,ct=fld['python_name'],fld['c_type']
            if fld['pointer']: lines.append(f'    assert obj.{pn} == 0\n    obj.{pn}=0\n')
            elif '[' in ct:
                total=1
                for q in re.findall(r'\[(\d+)\]',ct): total*=int(q)
                lines.append(f'    assert len(obj.{pn}) == {total}\n')
            else: lines.append(f'    _=obj.{pn}\n')
    for f in h['functions']:
        py,ad,c=f['python_name'],f['adaptation'],f['c_name'];lines.append(f'\ndef test_{py}():\n')
        if ad=='missing': lines.append(f'    with pytest.raises(NotImplementedError): m.{py}('+', '.join('1' for _ in f['parameters'])+')\n');continue
        if ad=='legacy_typo': lines.append('    assert m.get_response_legacy(3)==103\n');continue
        if ad=='callback_isr': lines.append('    seen=[]\n    assert m.wiring_pi_isr(1,1,lambda:seen.append(1))==0\n    assert seen==[1]\n');continue
        if ad=='callback_thread': lines.append('    seen=[]\n    assert m.pi_thread_create(lambda:seen.append(1))==0\n    assert seen==[1]\n');continue
        if ad=='spi_inout_buffer': lines.append('    b=bytearray([1,2,3]);assert m.wiring_pi_spi_data_rw(0,b)==3;assert b==bytearray([0xA4,0xA7,0xA6])\n    with pytest.raises((TypeError,BufferError)):m.wiring_pi_spi_data_rw(0,b"abc")\n');continue
        if ad=='ds1302_clock_read': lines.append('    assert m.ds1302_clock_read()==tuple(range(10,18))\n');continue
        if ad=='ds1302_clock_write': lines.append('    m.ds1302_clock_write(range(8))\n    with pytest.raises(ValueError):m.ds1302_clock_write([1])\n');continue
        if ad=='lcd_char_def': lines.append('    m.lcd_char_def(1,0,b"12345678")\n    with pytest.raises(ValueError):m.lcd_char_def(1,0,b"x")\n');continue
        if ad=='lcd_screen_size': lines.append('    assert m.lcd128x64_get_screen_size()==(128,64)\n');continue
        if c=='lcd128x64orientCoordinates': lines.append('    assert m.lcd128x64orient_coordinates()==(1,2)\n');continue
        if ad=='maxdetect_read': lines.append('    assert m.max_detect_read(1)==(1,b"\\x01\\x02\\x03\\x04")\n');continue
        if ad=='rht03_read': lines.append('    assert m.read_rht03(1)==(1,234,567)\n');continue
        if ad=='w25_manufacturer': lines.append('    assert m.w25q64_read_manufacturer()==bytes.fromhex("ef4017")\n');continue
        if ad=='w25_unique_id': lines.append('    assert m.w25q64_read_unique_id()==bytes(range(0x10,0x17))\n');continue
        if ad=='w25_read': lines.append(f'    assert m.{py}(0x20,4)==bytes([0x20,0x21,0x22,0x23])\n');continue
        if ad=='w25_page_write': lines.append(f'    assert m.{py}(0,0,b"abc")==3\n    with pytest.raises(ValueError):m.{py}(0,250,b"0123456789")\n');continue
        if ad=='serial_config_init': lines.append('    c=m.serial_config_init();assert c.baud==9600 and c.data_bits==8\n');continue
        if ad=='serial_get_config': lines.append('    rc,c=m.serial_get_config(7);assert rc==0\n');continue
        if ad=='serial_get_baud': lines.append('    assert m.serial_get_baud(7)[0]==0\n');continue
        if ad in ('serial_read','serial_read_timeout'):
            suffix=',10,-1' if ad=='serial_read_timeout' else ''
            lines.append(f'    assert m.{py}(7,4{suffix})==b"0123"\n');continue
        if ad in ('serial_write','serial_write_timeout'):
            suffix=',10' if ad=='serial_write_timeout' else ''
            lines.append(f'    assert m.{py}(7,b"abcd"{suffix})==4\n');continue
        if ad in ('serial_get_modem_lines','serial_get_counters','serial_get_rs485','serial_get_hardware_info','serial_get_capabilities'):
            lines.append(f'    assert m.{py}(7)[0]==0\n');continue
        if ad=='serial_context_open': lines.append('    cfg=m.serial_config_init();a=m.serial_context_open("mock",cfg);assert isinstance(a,int) and a!=0;m.serial_context_close(a)\n');continue
        if ad=='serial_context_from_fd': lines.append('    a=m.serial_context_from_fd(7,0);assert m.serial_context_get_fd(a)==7;m.serial_context_close(a)\n');continue
        if ad=='serial_context_close': lines.append('    cfg=m.serial_config_init();a=m.serial_context_open("mock",cfg);m.serial_context_close(a)\n');continue
        if ad=='serial_context_get_fd': lines.append('    a=m.serial_context_from_fd(7,0);assert m.serial_context_get_fd(a)==7;m.serial_context_close(a)\n');continue
        if ad=='serial_context_read': lines.append('    a=m.serial_context_from_fd(7,0);assert m.serial_context_read(a,4,10,-1)==b"0123";m.serial_context_close(a)\n');continue
        if ad=='serial_context_write': lines.append('    a=m.serial_context_from_fd(7,0);assert m.serial_context_write(a,b"abcd",10)==4;m.serial_context_close(a)\n');continue
        if ad in ('serial_context_cancel_read','serial_context_cancel_write'):
            lines.append(f'    a=m.serial_context_from_fd(7,0);assert m.{py}(a)==0;m.serial_context_close(a)\n');continue
        if ad.startswith('oled_'):
            if ad=='oled_open': lines.append('    d=m.DisplayInfo();assert m.oled_open(d,"/dev/null")==0 and d.file==42\n')
            elif ad=='oled_send': lines.append('    d=m.DisplayInfo();assert m.oled_send(d,b"abc")==3\n')
            elif ad=='oled_putstr': lines.append('    d=m.DisplayInfo();m.oled_putstr(d,0,"abc")\n')
            else: lines.append('    d=m.DisplayInfo();m.oled_putstrto(d,0,0,"abc")\n')
            continue
        if ad=='prepared_printf':
            args=[test_value_for_param(x,structs) for x in f['parameters'][:-1]]+['"safe text"'];lines.append(f'    m.{py}({", ".join(args)})\n');continue
        if ad=='mutable_c_string':
            args=[('"x"' if x['c_type']=='char *' else test_value_for_param(x,structs)) for x in f['parameters']];lines.append(f'    m.{py}({", ".join(args)})\n');continue
        if ad=='output_pointers':
            ins=[x for x in f['parameters'] if not ('*' in x['c_type'] and not x['c_type'].lstrip().startswith('const '))];args=[test_value_for_param(x,structs) for x in ins];lines.append(f'    _=m.{py}({", ".join(args)})\n');continue
        if ad=='direct':
            args=[test_value_for_param(x,structs) for x in f['parameters']];lines.append(f'    _=m.{py}({", ".join(args)})\n');continue
        lines.append(f'    assert callable(m.{py})\n')
    for v in h['variables']:
        py,ct=v['python_name'],v['c_type'];lines.append(f'\ndef test_variable_{py}():\n')
        if v['c_name'] in OPTIONAL_LEGACY_ARRAYS or '[' in ct or ct.startswith('const '): lines.append(f'    assert hasattr(m,"{py}")\n')
        elif '*' in ct: lines.append(f'    assert isinstance(m.get_{py}_address(),int)\n')
        elif 'struct ' in ct and v['storage']=='static': lines.append(f'    x=m.get_{py}();m.set_{py}(x)\n')
        else: lines.append(f'    x=m.get_{py}();m.set_{py}(x)\n')
    bm=[x for x in h['macros'] if x.get('bindable')]
    if bm:
        lines.append('\ndef test_constants_and_macros():\n')
        for x in bm:
            if x['kind']=='function_value': lines.append(f'    _=m.{x["python_name"]}(1)\n')
            else: lines.append(f'    assert hasattr(m,"{x["python_name"]}")\n')
    if h['path']=='wiringPi/wiringSerial.h':
        lines.append(r'''
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
''')
    return ''.join(lines)


def generate_doc(h: dict) -> str:
    L=[f'# `{h["path"]}`\n\n',f'Python-модуль: `{h["python_module"]}`.\n\n','Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.\n\n']
    if h['path']=='wiringPi/wiringSerial.h':
        L.append('## Расширенный UART\n\nLegacy `serialOpen()` и старый ABI сохранены без изменения. Новый API добавляет произвольный baud через Linux `termios2/BOTHER`, 5–8 бит, parity N/O/E/M/S (если поддерживает драйвер), 1/1.5/2 stop bits, XON/XOFF, RTS/CTS, modem lines, таймауты, break, exclusive/low-latency, error counters, Linux RS-485, RX FIFO trigger, wakeup, hardware/capability discovery и cancellable `serialContext`. На RK3588/DesignWare обнаруживаются FIFO, DMA description, auto RTS/CTS и расширенные RS-485 capabilities без прямого MMIO-конфликта с ядром. `SerialPort` использует один C syscall/poll path для bulk `read`/`write`, writable buffer в `read_into`, освобождает GIL на блокирующем I/O и реально реализует `cancel_read`/`cancel_write` через wakeup pipe. URL/network handlers pySerial намеренно не входят в hardware UART слой. Автоматический DSR/DTR flow-control не имеет переносимого Linux tty API и при попытке включения явно выдаёт `NotImplementedError`; ручной DTR доступен.\n\n')
    if h['functions']:
        L.append('## Функции\n\n')
        for f in h['functions']:
            ps=', '.join(p['python_name'] for p in f['parameters']);L.append(f'- `{f["c_name"]}` → `{f["python_name"]}({ps})`; C return `{f["return_type"]}`; адаптация `{f["adaptation"]}`.\n')
        L.append('\n')
    if h['structs']:
        L.append('## Структуры\n\n')
        for s in h['structs']:
            L.append(f'### `{s["python_name"]}` (`{s["c_name"]}`)\n\n')
            for f in s['fields']:L.append(f'- `{f["name"]}` → `{f["python_name"]}`: `{f["c_type"]}`.\n')
            L.append('\n')
    if h['variables']:
        L.append('## Данные и глобальные значения\n\n')
        for v in h['variables']:
            note='; отсутствующие legacy extern arrays в production представлены как `None`' if v['c_name'] in OPTIONAL_LEGACY_ARRAYS else ''
            L.append(f'- `{v["c_name"]}` → `{v["python_name"]}` (`{v["c_type"]}`, `{v["storage"]}`){note}.\n')
        L.append('\n')
    if h['macros']:
        L.append('## Макросы\n\n')
        for x in h['macros']:
            state='экспортируется' if x.get('bindable') else 'остаётся C-only'
            L.append(f'- `{x["c_name"]}` → `{x["python_name"]}`: {state}; `{x["kind"]}`; определение `{x.get("definition",x.get("body",""))}`.\n')
    return ''.join(L)


def production_sources() -> list[str]:
    prod=[]
    for p in sorted((UPSTREAM/'wiringPi').glob('*.c')): prod.append(p.relative_to(UPSTREAM).as_posix())
    for p in sorted((UPSTREAM/'devLib').glob('*.c')):
        if p.name!='piFaceOld.c': prod.append(p.relative_to(UPSTREAM).as_posix())
    for p in sorted((UPSTREAM/'wiringPiD').glob('*.c')):
        if p.name!='wiringpid.c': prod.append(p.relative_to(UPSTREAM).as_posix())
    assert len(prod)==48, len(prod)
    return prod


def cmake_text(d: dict) -> str:
    mocks='\n'.join(f'  support/mock_backend/{h["path"][:-2]}.c' for h in d['headers'])
    prodtxt='\n'.join('  ${WIRINGOP_SOURCE}/'+x for x in production_sources())
    blocks=[]
    for h in d['headers']:
        src='src/'+h['path'][:-2]+'.cpp'
        base=module_basename(h)
        rel=py_rel_from_module(h['python_module'])
        parent=rel.parent.as_posix()
        outdir='${CMAKE_BINARY_DIR}/python/wiringop' + ('' if parent=='.' else '/'+parent)
        install_dir='wiringop' + ('' if parent=='.' else '/'+parent)
        stub='stubs/'+h['path'][:-2]+'.pyi'
        t='nb_'+re.sub(r'[^A-Za-z0-9_]','_',h['path'][:-2])
        blocks.append(f'''add_library({t} MODULE {src})
target_include_directories({t} PRIVATE ${{NB_ROOT}}/include ${{NB_ROOT}}/ext/robin_map/include ${{WIRINGOP_SOURCE}} ${{WIRINGOP_SOURCE}}/wiringPi ${{WIRINGOP_SOURCE}}/devLib ${{WIRINGOP_SOURCE}}/wiringPiD)
target_compile_definitions({t} PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
target_link_libraries({t} PRIVATE nanobind_runtime wiringop_backend Python::Module Threads::Threads dl m)
set_target_properties({t} PROPERTIES PREFIX "" OUTPUT_NAME "{base}" LIBRARY_OUTPUT_DIRECTORY "{outdir}")
install(TARGETS {t} LIBRARY DESTINATION "{install_dir}" RUNTIME DESTINATION "{install_dir}")
install(FILES "${{CMAKE_CURRENT_SOURCE_DIR}}/{stub}" DESTINATION "{install_dir}" RENAME "{base}.pyi")
''')
    return f'''cmake_minimum_required(VERSION 3.18)
project(wiringop_nanobind LANGUAGES C CXX)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Local release policy: maximum safe optimization by default.
if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()
if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options("$<$<CONFIG:Release>:-O3>" "$<$<CONFIG:Release>:-DNDEBUG>")
endif()
option(WIRINGOP_ENABLE_IPO "Enable interprocedural/LTO optimization in Release" ON)
if(WIRINGOP_ENABLE_IPO)
  include(CheckIPOSupported)
  check_ipo_supported(RESULT WIRINGOP_IPO_SUPPORTED OUTPUT WIRINGOP_IPO_ERROR LANGUAGES C CXX)
  if(NOT WIRINGOP_IPO_SUPPORTED)
    message(FATAL_ERROR "Release LTO/IPO is required but unsupported: ${{WIRINGOP_IPO_ERROR}}")
  endif()
  set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELEASE ON)
endif()

# CPU-specific tuning is deliberately enabled only for a native Orange Pi 5 build.
set(WIRINGOP_ORANGEPI5_NATIVE OFF)
set(WIRINGOP_BOARD_MODEL "")
if(CMAKE_SYSTEM_NAME STREQUAL "Linux" AND NOT CMAKE_CROSSCOMPILING
   AND CMAKE_SYSTEM_PROCESSOR MATCHES "^(aarch64|arm64)$"
   AND EXISTS "/proc/device-tree/model")
  file(STRINGS "/proc/device-tree/model" WIRINGOP_BOARD_MODEL LIMIT_COUNT 1)
  if(WIRINGOP_BOARD_MODEL MATCHES "Orange Pi 5")
    set(WIRINGOP_ORANGEPI5_NATIVE ON)
  endif()
endif()
if(WIRINGOP_ORANGEPI5_NATIVE)
  if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang" OR CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options("$<$<CONFIG:Release>:-mcpu=native>")
  endif()
  message(STATUS "Orange Pi 5 native build: enabling -mcpu=native")
else()
  message(STATUS "Generic Release build: -O3 + LTO/IPO without CPU-specific tuning")
endif()

find_package(Python 3.9 REQUIRED COMPONENTS Interpreter Development.Module)
find_package(Threads REQUIRED)
set(NB_ROOT "" CACHE PATH "Path to exact nanobind 2.14.0 package/source tree")
if(NOT NB_ROOT)
  execute_process(
    COMMAND "${{Python_EXECUTABLE}}" -c "import pathlib, nanobind; print(pathlib.Path(nanobind.__file__).resolve().parent)"
    RESULT_VARIABLE NB_DISCOVERY_STATUS
    OUTPUT_VARIABLE NB_DISCOVERED_ROOT
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_VARIABLE NB_DISCOVERY_ERROR
  )
  if(NOT NB_DISCOVERY_STATUS EQUAL 0 OR NOT NB_DISCOVERED_ROOT)
    message(FATAL_ERROR "Unable to discover nanobind 2.14.0 from Python: ${{NB_DISCOVERY_ERROR}}")
  endif()
  set(NB_ROOT "${{NB_DISCOVERED_ROOT}}" CACHE PATH "Path to exact nanobind 2.14.0 package/source tree" FORCE)
endif()
file(READ "${{NB_ROOT}}/include/nanobind/nanobind.h" NB_HEADER)
if(NOT NB_HEADER MATCHES "NB_VERSION_MAJOR 2" OR NOT NB_HEADER MATCHES "NB_VERSION_MINOR 14" OR NOT NB_HEADER MATCHES "NB_VERSION_PATCH 0" OR NOT NB_HEADER MATCHES "NB_VERSION_DEV +0")
  message(FATAL_ERROR "nanobind source must be exactly version 2.14.0")
endif()
option(WIRINGOP_USE_MOCK "Build against hardware-free mock ABI" OFF)
set(WIRINGOP_SOURCE "" CACHE PATH "Prepared wiringOP source; auto-prepared from the pinned submodule when empty")
if(NOT WIRINGOP_SOURCE)
  set(WIRINGOP_SOURCE "${{CMAKE_BINARY_DIR}}/upstream/wiringOP")
  execute_process(
    COMMAND "${{Python_EXECUTABLE}}" "${{CMAKE_CURRENT_SOURCE_DIR}}/tools/prepare_wiringop.py"
            --project-root "${{CMAKE_CURRENT_SOURCE_DIR}}" --output "${{WIRINGOP_SOURCE}}"
    WORKING_DIRECTORY "${{CMAKE_CURRENT_SOURCE_DIR}}"
    RESULT_VARIABLE WIRINGOP_PREPARE_STATUS
    OUTPUT_VARIABLE WIRINGOP_PREPARE_OUTPUT
    ERROR_VARIABLE WIRINGOP_PREPARE_ERROR
  )
  if(NOT WIRINGOP_PREPARE_STATUS EQUAL 0)
    message(FATAL_ERROR "Failed to prepare pinned wiringOP source: ${{WIRINGOP_PREPARE_ERROR}}")
  endif()
endif()
add_library(nanobind_runtime STATIC "${{NB_ROOT}}/src/nb_combined.cpp")
target_include_directories(nanobind_runtime PUBLIC "${{NB_ROOT}}/include" "${{NB_ROOT}}/ext/robin_map/include" PRIVATE "${{NB_ROOT}}/src")
target_link_libraries(nanobind_runtime PUBLIC Python::Module)
target_compile_definitions(nanobind_runtime PRIVATE NB_COMPACT_ASSERTIONS)
if(WIRINGOP_USE_MOCK)
 add_library(wiringop_backend STATIC
{mocks}
 )
else()
 add_library(wiringop_backend STATIC
{prodtxt}
 )
endif()
target_include_directories(wiringop_backend PUBLIC "${{WIRINGOP_SOURCE}}" "${{WIRINGOP_SOURCE}}/wiringPi" "${{WIRINGOP_SOURCE}}/devLib" "${{WIRINGOP_SOURCE}}/wiringPiD")
target_compile_definitions(wiringop_backend PRIVATE CONFIG_ORANGEPI _GNU_SOURCE)
find_library(CRYPT_LIBRARY NAMES crypt)
if(CRYPT_LIBRARY)
  target_link_libraries(wiringop_backend PUBLIC ${{CRYPT_LIBRARY}})
elseif(NOT WIRINGOP_USE_MOCK)
  message(FATAL_ERROR "libcrypt is required by wiringOP network/drcNet code")
endif()
file(COPY "${{CMAKE_CURRENT_SOURCE_DIR}}/python/wiringop" DESTINATION "${{CMAKE_BINARY_DIR}}/python" PATTERN "__pycache__" EXCLUDE PATTERN "*.pyc" EXCLUDE)
install(DIRECTORY "${{CMAKE_CURRENT_SOURCE_DIR}}/python/wiringop/" DESTINATION wiringop FILES_MATCHING PATTERN "*.py" PATTERN "py.typed" PATTERN "__pycache__" EXCLUDE PATTERN "*.pyc" EXCLUDE)
{''.join(blocks)}
'''


def pyproject_text() -> str:
    return '''[build-system]
requires = ["scikit-build-core>=0.10", "nanobind==2.14.0"]
build-backend = "scikit_build_core.build"

[project]
name = "wiringop-nanobind"
version = "0.1.0"
description = "Complete Pythonic nanobind bindings for OrangePi wiringOP"
requires-python = ">=3.9"
license = {text = "LGPL-3.0-or-later"}

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["*.py"]
addopts = ["--import-mode=importlib"]
'''


def main() -> None:
    d=json.loads(MANIFEST.read_text());structs=struct_class_map(d)
    for name in ('src','tests','docs','stubs','support/mock_backend','python/wiringop'):
        p=ROOT/name
        if p.exists(): shutil.rmtree(p)
        p.mkdir(parents=True,exist_ok=True)
    (ROOT/'python/wiringop/__init__.py').write_text('"""Pythonic nanobind bindings for wiringOP."""\n__version__="0.1.0"\n',encoding='utf-8')
    (ROOT/'python/wiringop/py.typed').write_text('',encoding='utf-8')
    for h in d['headers']:
        for base,suffix,text in (
            ('src','.cpp',generate_cpp(d,h)),
            ('tests','.py',generate_test(d,h,structs)),
            ('docs','.md',generate_doc(h)),
            ('support/mock_backend','.c',generate_mock(h)),
        ):
            p=ROOT/base/Path(h['path']).with_suffix(suffix);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
        pkg=ROOT/'python'/Path(*h['python_module'].split('.')[:-1]);pkg.mkdir(parents=True,exist_ok=True)
        q=pkg
        while q!=ROOT/'python' and q.is_relative_to(ROOT/'python'):
            init=q/'__init__.py'
            if not init.exists(): init.write_text('',encoding='utf-8')
            q=q.parent
    (ROOT/'CMakeLists.txt').write_text(cmake_text(d),encoding='utf-8')
    (ROOT/'pyproject.toml').write_text(pyproject_text(),encoding='utf-8')
    (ROOT/'.gitignore').write_text('build/\ndist/\n*.egg-info/\n__pycache__/\n*.py[cod]\n*.so\n*.dylib\n*.dll\n.pytest_cache/\n.venv/\nhardware_validation/*.tar.gz\n',encoding='utf-8')
    license_src=ROOT/'extern/wiringOP/COPYING.LESSER'
    if license_src.is_file(): shutil.copyfile(license_src,ROOT/'LICENSE')
    print(f'generated {len(d["headers"])} mirrored units')

if __name__=='__main__': main()
