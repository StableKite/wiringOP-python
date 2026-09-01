"""nanobind bindings for wiringPi/wiringPi.h"""

from collections.abc import Callable


class SunxiGPIOInfo:
    def __init__(self) -> None: ...

    @property
    def gpio_base_addr(self) -> int: ...

    @gpio_base_addr.setter
    def gpio_base_addr(self, arg: int, /) -> None: ...

    @property
    def r_gpio_base_addr(self) -> int: ...

    @r_gpio_base_addr.setter
    def r_gpio_base_addr(self, arg: int, /) -> None: ...

    @property
    def gpio_address(self) -> int: ...

    @gpio_address.setter
    def gpio_address(self, arg: int, /) -> None: ...

    @property
    def r_gpio_address(self) -> int: ...

    @r_gpio_address.setter
    def r_gpio_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_offset(self) -> int: ...

    @gpio_base_offset.setter
    def gpio_base_offset(self, arg: int, /) -> None: ...

    @property
    def r_gpio_base_offset(self) -> int: ...

    @r_gpio_base_offset.setter
    def r_gpio_base_offset(self, arg: int, /) -> None: ...

    @property
    def gpio_bank_offset(self) -> int: ...

    @gpio_bank_offset.setter
    def gpio_bank_offset(self, arg: int, /) -> None: ...

    @property
    def pull_offset(self) -> int: ...

    @pull_offset.setter
    def pull_offset(self, arg: int, /) -> None: ...

    @property
    def r_gpio_pull_offset(self) -> int: ...

    @r_gpio_pull_offset.setter
    def r_gpio_pull_offset(self, arg: int, /) -> None: ...

    @property
    def gpio_cfg_mask(self) -> int: ...

    @gpio_cfg_mask.setter
    def gpio_cfg_mask(self, arg: int, /) -> None: ...

    @property
    def pwm_base_addr(self) -> int: ...

    @pwm_base_addr.setter
    def pwm_base_addr(self, arg: int, /) -> None: ...

    @property
    def pwm_address(self) -> int: ...

    @pwm_address.setter
    def pwm_address(self, arg: int, /) -> None: ...

    @property
    def pwm_ctrl(self) -> int: ...

    @pwm_ctrl.setter
    def pwm_ctrl(self, arg: int, /) -> None: ...

    @property
    def pwm_period(self) -> int: ...

    @pwm_period.setter
    def pwm_period(self, arg: int, /) -> None: ...

    @property
    def pwm_clk(self) -> int: ...

    @pwm_clk.setter
    def pwm_clk(self, arg: int, /) -> None: ...

    @property
    def pwm_en(self) -> int: ...

    @pwm_en.setter
    def pwm_en(self, arg: int, /) -> None: ...

    @property
    def pwm_type(self) -> int: ...

    @pwm_type.setter
    def pwm_type(self, arg: int, /) -> None: ...

    @property
    def pwm_bit_en(self) -> int: ...

    @pwm_bit_en.setter
    def pwm_bit_en(self, arg: int, /) -> None: ...

    @property
    def pwm_bit_act(self) -> int: ...

    @pwm_bit_act.setter
    def pwm_bit_act(self, arg: int, /) -> None: ...

    @property
    def pwm_bit_sclk(self) -> int: ...

    @pwm_bit_sclk.setter
    def pwm_bit_sclk(self, arg: int, /) -> None: ...

    @property
    def pwm_bit_mode(self) -> int: ...

    @pwm_bit_mode.setter
    def pwm_bit_mode(self, arg: int, /) -> None: ...

    @property
    def pwm_bit_pulse(self) -> int: ...

    @pwm_bit_pulse.setter
    def pwm_bit_pulse(self, arg: int, /) -> None: ...

class Rk3588SocInfo:
    def __init__(self) -> None: ...

    @property
    def gpio0_base_address(self) -> int: ...

    @gpio0_base_address.setter
    def gpio0_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio1_base_address(self) -> int: ...

    @gpio1_base_address.setter
    def gpio1_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio2_base_address(self) -> int: ...

    @gpio2_base_address.setter
    def gpio2_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio3_base_address(self) -> int: ...

    @gpio3_base_address.setter
    def gpio3_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio4_base_address(self) -> int: ...

    @gpio4_base_address.setter
    def gpio4_base_address(self, arg: int, /) -> None: ...

    @property
    def pmu1_ioc_base_address(self) -> int: ...

    @pmu1_ioc_base_address.setter
    def pmu1_ioc_base_address(self, arg: int, /) -> None: ...

    @property
    def pmu2_ioc_base_address(self) -> int: ...

    @pmu2_ioc_base_address.setter
    def pmu2_ioc_base_address(self, arg: int, /) -> None: ...

    @property
    def bus_ioc_base_address(self) -> int: ...

    @bus_ioc_base_address.setter
    def bus_ioc_base_address(self, arg: int, /) -> None: ...

    @property
    def cur_base_address(self) -> int: ...

    @cur_base_address.setter
    def cur_base_address(self, arg: int, /) -> None: ...

    @property
    def pmu1cur_base_address(self) -> int: ...

    @pmu1cur_base_address.setter
    def pmu1cur_base_address(self, arg: int, /) -> None: ...

    @property
    def vccio1_4_ioc_base_address(self) -> int: ...

    @vccio1_4_ioc_base_address.setter
    def vccio1_4_ioc_base_address(self, arg: int, /) -> None: ...

    @property
    def vccio3_5_ioc_base_address(self) -> int: ...

    @vccio3_5_ioc_base_address.setter
    def vccio3_5_ioc_base_address(self, arg: int, /) -> None: ...

    @property
    def vccio6_ioc_base_address(self) -> int: ...

    @vccio6_ioc_base_address.setter
    def vccio6_ioc_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm0_base_address(self) -> int: ...

    @pwm0_base_address.setter
    def pwm0_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm1_base_address(self) -> int: ...

    @pwm1_base_address.setter
    def pwm1_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm2_base_address(self) -> int: ...

    @pwm2_base_address.setter
    def pwm2_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm3_base_address(self) -> int: ...

    @pwm3_base_address.setter
    def pwm3_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm_base(self) -> int: ...

    @pwm_base.setter
    def pwm_base(self, arg: int, /) -> None: ...

    @property
    def pwm_mux(self) -> int: ...

    @pwm_mux.setter
    def pwm_mux(self, arg: int, /) -> None: ...

    @property
    def pwm_mux_val(self) -> int: ...

    @pwm_mux_val.setter
    def pwm_mux_val(self, arg: int, /) -> None: ...

    @property
    def pwm_mux_offset(self) -> int: ...

    @pwm_mux_offset.setter
    def pwm_mux_offset(self, arg: int, /) -> None: ...

    @property
    def ch_period_hpr(self) -> int: ...

    @ch_period_hpr.setter
    def ch_period_hpr(self, arg: int, /) -> None: ...

    @property
    def ch_duty_lpr(self) -> int: ...

    @ch_duty_lpr.setter
    def ch_duty_lpr(self, arg: int, /) -> None: ...

    @property
    def ch_crtl(self) -> int: ...

    @ch_crtl.setter
    def ch_crtl(self, arg: int, /) -> None: ...

class Rk3566SocInfo:
    def __init__(self) -> None: ...

    @property
    def gpio0_base_address(self) -> int: ...

    @gpio0_base_address.setter
    def gpio0_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio1_base_address(self) -> int: ...

    @gpio1_base_address.setter
    def gpio1_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio2_base_address(self) -> int: ...

    @gpio2_base_address.setter
    def gpio2_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio3_base_address(self) -> int: ...

    @gpio3_base_address.setter
    def gpio3_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio4_base_address(self) -> int: ...

    @gpio4_base_address.setter
    def gpio4_base_address(self, arg: int, /) -> None: ...

    @property
    def pmu_grf_base_address(self) -> int: ...

    @pmu_grf_base_address.setter
    def pmu_grf_base_address(self, arg: int, /) -> None: ...

    @property
    def sys_grf_base_address(self) -> int: ...

    @sys_grf_base_address.setter
    def sys_grf_base_address(self, arg: int, /) -> None: ...

    @property
    def cru_base_address(self) -> int: ...

    @cru_base_address.setter
    def cru_base_address(self, arg: int, /) -> None: ...

    @property
    def pmu_cru_base_address(self) -> int: ...

    @pmu_cru_base_address.setter
    def pmu_cru_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm2_base_address(self) -> int: ...

    @pwm2_base_address.setter
    def pwm2_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm3_base_address(self) -> int: ...

    @pwm3_base_address.setter
    def pwm3_base_address(self, arg: int, /) -> None: ...

    @property
    def cru_gate_con(self) -> int: ...

    @cru_gate_con.setter
    def cru_gate_con(self, arg: int, /) -> None: ...

    @property
    def cru_gate_con_offset(self) -> int: ...

    @cru_gate_con_offset.setter
    def cru_gate_con_offset(self, arg: int, /) -> None: ...

    @property
    def pwm_base(self) -> int: ...

    @pwm_base.setter
    def pwm_base(self, arg: int, /) -> None: ...

    @property
    def pwm_mux(self) -> int: ...

    @pwm_mux.setter
    def pwm_mux(self, arg: int, /) -> None: ...

    @property
    def pwm_mux_val(self) -> int: ...

    @pwm_mux_val.setter
    def pwm_mux_val(self, arg: int, /) -> None: ...

    @property
    def pwm_mux_offset(self) -> int: ...

    @pwm_mux_offset.setter
    def pwm_mux_offset(self, arg: int, /) -> None: ...

    @property
    def ch_period_hpr(self) -> int: ...

    @ch_period_hpr.setter
    def ch_period_hpr(self, arg: int, /) -> None: ...

    @property
    def ch_duty_lpr(self) -> int: ...

    @ch_duty_lpr.setter
    def ch_duty_lpr(self, arg: int, /) -> None: ...

    @property
    def ch_crtl(self) -> int: ...

    @ch_crtl.setter
    def ch_crtl(self, arg: int, /) -> None: ...

class Rk3399SocInfo:
    def __init__(self) -> None: ...

    @property
    def gpio2_base_address(self) -> int: ...

    @gpio2_base_address.setter
    def gpio2_base_address(self, arg: int, /) -> None: ...

    @property
    def grf_base_address(self) -> int: ...

    @grf_base_address.setter
    def grf_base_address(self, arg: int, /) -> None: ...

    @property
    def cru_base_address(self) -> int: ...

    @cru_base_address.setter
    def cru_base_address(self, arg: int, /) -> None: ...

    @property
    def pmucru_base_address(self) -> int: ...

    @pmucru_base_address.setter
    def pmucru_base_address(self, arg: int, /) -> None: ...

    @property
    def pmugrf_base_address(self) -> int: ...

    @pmugrf_base_address.setter
    def pmugrf_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio1_base_address(self) -> int: ...

    @gpio1_base_address.setter
    def gpio1_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio4_base_address(self) -> int: ...

    @gpio4_base_address.setter
    def gpio4_base_address(self, arg: int, /) -> None: ...

class Rk3328SocInfo:
    def __init__(self) -> None: ...

    @property
    def gpio2_base_address(self) -> int: ...

    @gpio2_base_address.setter
    def gpio2_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio3_base_address(self) -> int: ...

    @gpio3_base_address.setter
    def gpio3_base_address(self, arg: int, /) -> None: ...

    @property
    def cru_base_address(self) -> int: ...

    @cru_base_address.setter
    def cru_base_address(self, arg: int, /) -> None: ...

    @property
    def grf_base_address(self) -> int: ...

    @grf_base_address.setter
    def grf_base_address(self, arg: int, /) -> None: ...

class S905d3GPIOInfo:
    def __init__(self) -> None: ...

    @property
    def gpio_base_address(self) -> int: ...

    @gpio_base_address.setter
    def gpio_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio_ao_base_address(self) -> int: ...

    @gpio_ao_base_address.setter
    def gpio_ao_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio_pwm_base_address(self) -> int: ...

    @gpio_pwm_base_address.setter
    def gpio_pwm_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio_pwm_ao_base_address(self) -> int: ...

    @gpio_pwm_ao_base_address.setter
    def gpio_pwm_ao_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio_out_en(self) -> int: ...

    @gpio_out_en.setter
    def gpio_out_en(self, arg: int, /) -> None: ...

    @property
    def gpio_out(self) -> int: ...

    @gpio_out.setter
    def gpio_out(self, arg: int, /) -> None: ...

    @property
    def gpio_in(self) -> int: ...

    @gpio_in.setter
    def gpio_in(self, arg: int, /) -> None: ...

    @property
    def gpio_pupd(self) -> int: ...

    @gpio_pupd.setter
    def gpio_pupd(self, arg: int, /) -> None: ...

    @property
    def gpio_puen(self) -> int: ...

    @gpio_puen.setter
    def gpio_puen(self, arg: int, /) -> None: ...

    @property
    def gpio_mux(self) -> int: ...

    @gpio_mux.setter
    def gpio_mux(self, arg: int, /) -> None: ...

    @property
    def gpio_out_en_offset(self) -> int: ...

    @gpio_out_en_offset.setter
    def gpio_out_en_offset(self, arg: int, /) -> None: ...

    @property
    def gpio_out_offset(self) -> int: ...

    @gpio_out_offset.setter
    def gpio_out_offset(self, arg: int, /) -> None: ...

    @property
    def gpio_in_offset(self) -> int: ...

    @gpio_in_offset.setter
    def gpio_in_offset(self, arg: int, /) -> None: ...

    @property
    def gpio_pupd_offset(self) -> int: ...

    @gpio_pupd_offset.setter
    def gpio_pupd_offset(self, arg: int, /) -> None: ...

    @property
    def gpio_puen_offset(self) -> int: ...

    @gpio_puen_offset.setter
    def gpio_puen_offset(self, arg: int, /) -> None: ...

    @property
    def gpio_mux_offset(self) -> int: ...

    @gpio_mux_offset.setter
    def gpio_mux_offset(self, arg: int, /) -> None: ...

    @property
    def pwm_duty_cycle(self) -> int: ...

    @pwm_duty_cycle.setter
    def pwm_duty_cycle(self, arg: int, /) -> None: ...

    @property
    def pwm_misc(self) -> int: ...

    @pwm_misc.setter
    def pwm_misc(self, arg: int, /) -> None: ...

class A310bGPIOInfo:
    def __init__(self) -> None: ...

    @property
    def iomux_base_group0_address(self) -> int: ...

    @iomux_base_group0_address.setter
    def iomux_base_group0_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group1_address(self) -> int: ...

    @iomux_base_group1_address.setter
    def iomux_base_group1_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group2_address(self) -> int: ...

    @iomux_base_group2_address.setter
    def iomux_base_group2_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group3_address(self) -> int: ...

    @iomux_base_group3_address.setter
    def iomux_base_group3_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group4_address(self) -> int: ...

    @iomux_base_group4_address.setter
    def iomux_base_group4_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group5_address(self) -> int: ...

    @iomux_base_group5_address.setter
    def iomux_base_group5_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group7_address(self) -> int: ...

    @iomux_base_group7_address.setter
    def iomux_base_group7_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group0_address(self) -> int: ...

    @gpio_base_group0_address.setter
    def gpio_base_group0_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group1_address(self) -> int: ...

    @gpio_base_group1_address.setter
    def gpio_base_group1_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group2_address(self) -> int: ...

    @gpio_base_group2_address.setter
    def gpio_base_group2_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group3_address(self) -> int: ...

    @gpio_base_group3_address.setter
    def gpio_base_group3_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group4_address(self) -> int: ...

    @gpio_base_group4_address.setter
    def gpio_base_group4_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group5_address(self) -> int: ...

    @gpio_base_group5_address.setter
    def gpio_base_group5_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group7_address(self) -> int: ...

    @gpio_base_group7_address.setter
    def gpio_base_group7_address(self, arg: int, /) -> None: ...

    @property
    def pwm_base_address(self) -> int: ...

    @pwm_base_address.setter
    def pwm_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm_prd2_phyaddr(self) -> int: ...

    @pwm_prd2_phyaddr.setter
    def pwm_prd2_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_ch2_pwl_phyaddr(self) -> int: ...

    @pwm_ch2_pwl_phyaddr.setter
    def pwm_ch2_pwl_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_ch2_pwh_phyaddr(self) -> int: ...

    @pwm_ch2_pwh_phyaddr.setter
    def pwm_ch2_pwh_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_prd3_phyaddr(self) -> int: ...

    @pwm_prd3_phyaddr.setter
    def pwm_prd3_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_ch3_pwl_phyaddr(self) -> int: ...

    @pwm_ch3_pwl_phyaddr.setter
    def pwm_ch3_pwl_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_ch3_pwh_phyaddr(self) -> int: ...

    @pwm_ch3_pwh_phyaddr.setter
    def pwm_ch3_pwh_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_measure_time_phyaddr(self) -> int: ...

    @pwm_measure_time_phyaddr.setter
    def pwm_measure_time_phyaddr(self, arg: int, /) -> None: ...

class A310pGPIOInfo:
    def __init__(self) -> None: ...

    @property
    def iomux_base_group0_address(self) -> int: ...

    @iomux_base_group0_address.setter
    def iomux_base_group0_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group1_address(self) -> int: ...

    @iomux_base_group1_address.setter
    def iomux_base_group1_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group2_address(self) -> int: ...

    @iomux_base_group2_address.setter
    def iomux_base_group2_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group3_address(self) -> int: ...

    @iomux_base_group3_address.setter
    def iomux_base_group3_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group4_address(self) -> int: ...

    @iomux_base_group4_address.setter
    def iomux_base_group4_address(self, arg: int, /) -> None: ...

    @property
    def iomux_base_group5_address(self) -> int: ...

    @iomux_base_group5_address.setter
    def iomux_base_group5_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group0_address(self) -> int: ...

    @gpio_base_group0_address.setter
    def gpio_base_group0_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group1_address(self) -> int: ...

    @gpio_base_group1_address.setter
    def gpio_base_group1_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group2_address(self) -> int: ...

    @gpio_base_group2_address.setter
    def gpio_base_group2_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group3_address(self) -> int: ...

    @gpio_base_group3_address.setter
    def gpio_base_group3_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group4_address(self) -> int: ...

    @gpio_base_group4_address.setter
    def gpio_base_group4_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_group5_address(self) -> int: ...

    @gpio_base_group5_address.setter
    def gpio_base_group5_address(self, arg: int, /) -> None: ...

    @property
    def pwm_base_address(self) -> int: ...

    @pwm_base_address.setter
    def pwm_base_address(self, arg: int, /) -> None: ...

    @property
    def pwm_prd1_phyaddr(self) -> int: ...

    @pwm_prd1_phyaddr.setter
    def pwm_prd1_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_ch1_pwl_phyaddr(self) -> int: ...

    @pwm_ch1_pwl_phyaddr.setter
    def pwm_ch1_pwl_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_ch1_pwh_phyaddr(self) -> int: ...

    @pwm_ch1_pwh_phyaddr.setter
    def pwm_ch1_pwh_phyaddr(self, arg: int, /) -> None: ...

    @property
    def pwm_measure_time_phyaddr(self) -> int: ...

    @pwm_measure_time_phyaddr.setter
    def pwm_measure_time_phyaddr(self, arg: int, /) -> None: ...

class Jh7110SocInfo:
    def __init__(self) -> None: ...

    @property
    def sys_iomux_base_address(self) -> int: ...

    @sys_iomux_base_address.setter
    def sys_iomux_base_address(self, arg: int, /) -> None: ...

class Kyx1SocInfo:
    def __init__(self) -> None: ...

    @property
    def iomux_base_address(self) -> int: ...

    @iomux_base_address.setter
    def iomux_base_address(self, arg: int, /) -> None: ...

    @property
    def gpio_base_address(self) -> int: ...

    @gpio_base_address.setter
    def gpio_base_address(self, arg: int, /) -> None: ...

class WiringPiNodeStruct:
    def __init__(self) -> None: ...

    @property
    def pin_base(self) -> int: ...

    @pin_base.setter
    def pin_base(self, arg: int, /) -> None: ...

    @property
    def pin_max(self) -> int: ...

    @pin_max.setter
    def pin_max(self, arg: int, /) -> None: ...

    @property
    def fd(self) -> int: ...

    @fd.setter
    def fd(self, arg: int, /) -> None: ...

    @property
    def data0(self) -> int: ...

    @data0.setter
    def data0(self, arg: int, /) -> None: ...

    @property
    def data1(self) -> int: ...

    @data1.setter
    def data1(self, arg: int, /) -> None: ...

    @property
    def data2(self) -> int: ...

    @data2.setter
    def data2(self, arg: int, /) -> None: ...

    @property
    def data3(self) -> int: ...

    @data3.setter
    def data3(self, arg: int, /) -> None: ...

    @property
    def pin_mode_address(self) -> int: ...

    @pin_mode_address.setter
    def pin_mode_address(self, arg: int, /) -> None: ...

    @property
    def pull_up_dn_control_address(self) -> int: ...

    @pull_up_dn_control_address.setter
    def pull_up_dn_control_address(self, arg: int, /) -> None: ...

    @property
    def digital_read_address(self) -> int: ...

    @digital_read_address.setter
    def digital_read_address(self, arg: int, /) -> None: ...

    @property
    def digital_write_address(self) -> int: ...

    @digital_write_address.setter
    def digital_write_address(self, arg: int, /) -> None: ...

    @property
    def pwm_write_address(self) -> int: ...

    @pwm_write_address.setter
    def pwm_write_address(self, arg: int, /) -> None: ...

    @property
    def analog_read_address(self) -> int: ...

    @analog_read_address.setter
    def analog_read_address(self, arg: int, /) -> None: ...

    @property
    def analog_write_address(self) -> int: ...

    @analog_write_address.setter
    def analog_write_address(self, arg: int, /) -> None: ...

    @property
    def next_address(self) -> int: ...

    @next_address.setter
    def next_address(self, arg: int, /) -> None: ...

def pi_gpio_layout_oops(why: str) -> None: ...

def wiring_pi_failure(fatal: int, message: str) -> int: ...

def wiring_pi_find_node(pin: int) -> WiringPiNodeStruct: ...

def wiring_pi_new_node(pin_base: int, num_pins: int) -> WiringPiNodeStruct: ...

def wiring_pi_version() -> tuple: ...

def wiring_pi_setup() -> int: ...

def wiring_pi_setup_sys() -> int: ...

def wiring_pi_setup_gpio() -> int: ...

def wiring_pi_setup_phys() -> int: ...

def pin_mode_alt(pin: int, mode: int) -> None: ...

def pin_mode(pin: int, mode: int) -> None: ...

def pull_up_dn_control(pin: int, pud: int) -> None: ...

def digital_read(pin: int) -> int: ...

def digital_write(pin: int, value: int) -> None: ...

def digital_read8(pin: int) -> int: ...

def digital_write8(pin: int, value: int) -> None: ...

def pwm_write(pin: int, value: int) -> None: ...

def analog_read(pin: int) -> int: ...

def analog_write(pin: int, value: int) -> None: ...

def wiring_pi_setup_pi_face() -> int: ...

def wiring_pi_setup_pi_face_for_gpio_prog() -> int: ...

def pi_board_id() -> int: ...

def wpi_pin_to_gpio(wpi_pin: int) -> int: ...

def phys_pin_to_gpio(phys_pin: int) -> int: ...

def set_pad_drive(group: int, value: int) -> None: ...

def get_alt(pin: int) -> int: ...

def h618_set_pwm_reg(pin: int, sunxi_gpio_info_ptr: SunxiGPIOInfo) -> None: ...

def s905d3_set_gpio_reg(pin: int, s905d3_gpio_info_ptr: S905d3GPIOInfo) -> None: ...

def rk3588_set_pwm_reg(pin: int, rk3588_soc_info_ptr: Rk3588SocInfo) -> None: ...

def rk3566_set_pwm_reg(pin: int, rk3566_soc_info_ptr: Rk3566SocInfo) -> None: ...

def sunxi_pwm_set_enable(en: int) -> None: ...

def pwm_tone_write(pin: int, freq: int) -> None: ...

def pwm_set_mode(pin: int, mode: int) -> None: ...

def pwm_set_range(pin: int, range: int) -> None: ...

def pwm_set_clock(pin: int, divisor: int) -> None: ...

def gpio_clock_set(pin: int, freq: int) -> None: ...

def digital_read_byte() -> int: ...

def digital_read_byte2() -> int: ...

def digital_write_byte(value: int) -> None: ...

def digital_write_byte2(value: int) -> None: ...

def wait_for_interrupt(pin: int, m_s: int) -> int: ...

def wiring_pi_isr(pin: int, mode: int, callback: Callable) -> int: ...

def pi_thread_create(callback: Callable) -> int: ...

def pi_lock(key: int) -> None: ...

def pi_unlock(key: int) -> None: ...

def pi_hi_pri(pri: int) -> int: ...

def delay(how_long: int) -> None: ...

def delay_microseconds(how_long: int) -> None: ...

def millis() -> int: ...

def micros() -> int: ...

def read_r(addr: int) -> int: ...

def write_r(val: int, addr: int) -> None: ...

def orangepi_get_gpio_mode(pin: int) -> int: ...

def orangepi_set_gpio_mode(pin: int, mode: int) -> int: ...

def orangepi_digital_read(pin: int) -> int: ...

def orangepi_digital_write(pin: int, value: int) -> int: ...

def orangepi_set_gpio_alt(pin: int, mode: int) -> int: ...

def orange_pi_set_gpio_pull_up_dn_control(pin: int, pud: int) -> None: ...

def orangepi_pwm_set_act(pin: int, act_cys: int) -> None: ...

def orangepi_pwm_set_period(pin: int, period_cys: int) -> None: ...

def orangepi_pwm_set_clk(pin: int, clk: int) -> None: ...

def orangepi_pwm_set_tone(pin: int, freq: int) -> None: ...

def set_soc_info() -> None: ...

def get_wiring_pi_debug() -> int: ...

def set_wiring_pi_debug(value: int) -> None: ...

pi_model_names: None = None

pi_revision_names: None = None

pi_maker_names: None = None

pi_memory_size: None = None

def get_wiring_pi_nodes_address() -> int: ...

def set_wiring_pi_nodes_address(address: int) -> None: ...

def get_wiring_pi_gpio_address() -> int: ...

def set_wiring_pi_gpio_address(address: int) -> None: ...

def get_wiring_pi_pwm_address() -> int: ...

def set_wiring_pi_pwm_address(address: int) -> None: ...

def get_wiring_pi_clk_address() -> int: ...

def set_wiring_pi_clk_address(address: int) -> None: ...

def get_wiring_pi_pads_address() -> int: ...

def set_wiring_pi_pads_address(address: int) -> None: ...

def get_wiring_pi_timer_address() -> int: ...

def set_wiring_pi_timer_address(address: int) -> None: ...

def get_wiring_pi_timer_irq_raw_address() -> int: ...

def set_wiring_pi_timer_irq_raw_address(address: int) -> None: ...

TRUE: bool = True

FALSE: bool = False

MAX_PIN_NUM: int = 64

PI_MODEL_A: int = 0

PI_MODEL_B: int = 1

PI_MODEL_AP: int = 2

PI_MODEL_BP: int = 3

PI_MODEL_2: int = 4

PI_ALPHA: int = 5

PI_MODEL_CM: int = 6

PI_MODEL_07: int = 7

PI_MODEL_CM3: int = 10

PI_MODEL_ZERO_W: int = 12

PI_MODEL_3_P: int = 13

PI_VERSION_1: int = 0

PI_VERSION_1_1: int = 1

PI_VERSION_1_2: int = 2

PI_VERSION_2: int = 3

PI_MAKER_SONY: int = 0

PI_MAKER_EGOMAN: int = 1

PI_MAKER_EMBEST: int = 2

PI_MAKER_UNKNOWN: int = 3

H3_GPIO_BASE_ADDR: int = 29491200

H3_R_GPIO_BASE_ADDR: int = 32514048

H6_GPIO_BASE_ADDR: int = 50376704

H6_R_GPIO_BASE_ADDR: int = 117579776

A527_GPIO_BASE_ADDR: int = 33554432

T736_R_GPIO_BASE_ADDR: int = 117592064

H3_PWM_BASE: int = 29496320

H6_PWM_BASE: int = 50372608

H616_PWM_BASE: int = 50372608

SUNXI_V1_PWM_TYPE: int = 1

SUNXI_V2_PWM_TYPE: int = 2

SUNXI_V1_PWM_CH0_EN: int = 16

SUNXI_V1_PWM_CH0_ACT_STA: int = 32

SUNXI_V1_PWM_SCLK_CH0_GATING: int = 64

SUNXI_V1_PWM_CH0_MS_MODE: int = 128

SUNXI_V1_PWM_CH0_PUL_START: int = 256

SUNXI_V2_PWM_ACT_STA: int = 256

SUNXI_V2_PWM_SCLK_GATING: int = 16

SUNXI_V2_PWM_MS_MODE: int = 512

SUNXI_V2_PWM_PUL_START: int = 1024

SUNXI_V2_PWM1_EN: int = 2

SUNXI_V2_PWM2_EN: int = 4

SUNXI_V2_PWM3_EN: int = 8

SUNXI_V2_PWM4_EN: int = 16

PWM_CLK_DIV_120: int = 0

PWM_CLK_DIV_180: int = 1

PWM_CLK_DIV_240: int = 2

PWM_CLK_DIV_360: int = 3

PWM_CLK_DIV_480: int = 4

PWM_CLK_DIV_12_K: int = 8

PWM_CLK_DIV_24_K: int = 9

PWM_CLK_DIV_36_K: int = 10

PWM_CLK_DIV_48_K: int = 11

PWM_CLK_DIV_72_K: int = 12

SUNXI_PUD_OFF: int = 0

SUNXI_PUD_UP: int = 1

SUNXI_PUD_DOWN: int = 2

RK3588_GPIO0_BASE: int = 4253679616

RK3588_GPIO1_BASE: int = 4274126848

RK3588_GPIO2_BASE: int = 4274192384

RK3588_GPIO3_BASE: int = 4274257920

RK3588_GPIO4_BASE: int = 4274323456

RK3588_GPIO_SWPORT_DR_L_OFFSET: int = 0

RK3588_GPIO_SWPORT_DR_H_OFFSET: int = 4

RK3588_GPIO_SWPORT_DDR_L_OFFSET: int = 8

RK3588_GPIO_SWPORT_DDR_H_OFFSET: int = 12

RK3588_GPIO_EXT_PORT_OFFSET: int = 112

RK3588_CRU_BASE: int = 4252762112

RK3588_CRU_GATE_CON16_OFFSET: int = 2112

RK3588_CRU_GATE_CON17_OFFSET: int = 2116

RK3588_PMU1_CRU_BASE: int = 4252958720

RK3588_PMU1_CRU_GATE_CON5_OFFSET: int = 2068

RK3588_GPIO_NUM: int = 64

def RK3588_GPIO_BIT(x: int) -> int: ...

RK3588_PMU1_IOC_BASE: int = 4250861568

RK3588_PMU1_IOC_GPIO0_A_IOMUX_SEL_L: int = 0

RK3588_PMU1_IOC_GPIO0_A_IOMUX_SEL_H: int = 4

RK3588_PMU1_IOC_GPIO0_B_IOMUX_SEL_L: int = 8

RK3588_PMU2_IOC_BASE: int = 4250877952

RK3588_PMU2_IOC_GPIO0_B_IOMUX_SEL_H: int = 0

RK3588_PMU2_IOC_GPIO0_C_IOMUX_SEL_L: int = 4

RK3588_PMU2_IOC_GPIO0_C_IOMUX_SEL_H: int = 8

RK3588_PMU2_IOC_GPIO0_D_IOMUX_SEL_L: int = 12

RK3588_PMU2_IOC_GPIO0_D_IOMUX_SEL_H: int = 16

RK3588_BUS_IOC_BASE: int = 4250894336

RK3588_VCCIO1_4_IOC_BASE: int = 4250898432

RK3588_VCCIO3_5_IOC_BASE: int = 4250902528

RK3588_VCCIO6_IOC_BASE: int = 4250910720

RK3588_PMU1_IOC_GPIO0_A_P: int = 32

RK3588_PMU1_IOC_GPIO0_B_P: int = 36

RK3588_PMU2_IOC_GPIO0_B_P: int = 40

RK3588_PMU2_IOC_GPIO0_C_P: int = 44

RK3588_PMU2_IOC_GPIO0_D_P: int = 48

RK3588_VCCIO1_4_IOC_GPIO1_A_P: int = 272

RK3588_VCCIO3_5_IOC_GPIO2_A_P: int = 288

RK3588_VCCIO6_IOC_GPIO4_A_P: int = 320

RK3588_PWM0_BASE: int = 4253745152

RK3588_PWM1_BASE: int = 4270653440

RK3588_PWM2_BASE: int = 4273864704

RK3588_PWM3_BASE: int = 4273930240

RK3588_CRU_GATE_CON19: int = 4252764236

RK3588_CRU_GATE_CON15: int = 4252764220

RK3588_PMU1_CRU_GATE_CON1: int = 4252960772

RK3588_RPT: int = 24

RK3588_SCALE: int = 16

RK3588_PRESCALE: int = 12

RK3588_CLK_SRC_SEL: int = 10

RK3588_CLK_SEL: int = 9

RK3588_FORCE_CLK_EN: int = 8

RK3588_CH_CNT_EN: int = 7

RK3588_CONLOCK: int = 6

RK3588_OUTPUT_MODE: int = 5

RK3588_INACTIVE_POL: int = 4

RK3588_DUTY_POL: int = 3

RK3588_PWM_MODE: int = 1

RK3588_PWM_EN: int = 0

RK3566_GPIO0_BASE: int = 4258660352

RK3566_GPIO1_BASE: int = 4269015040

RK3566_GPIO2_BASE: int = 4269080576

RK3566_GPIO3_BASE: int = 4269146112

RK3566_GPIO4_BASE: int = 4269211648

RK3566_GPIO_SWPORT_DR_L_OFFSET: int = 0

RK3566_GPIO_SWPORT_DR_H_OFFSET: int = 4

RK3566_GPIO_SWPORT_DDR_L_OFFSET: int = 8

RK3566_GPIO_SWPORT_DDR_H_OFFSET: int = 12

RK3566_GPIO_EXT_PORT_OFFSET: int = 112

RK3566_PMU_GRF_BASE: int = 4257349632

RK3566_SYS_GRF_BASE: int = 4257611776

RK3566_PMU_CRU_BASE: int = 4258267136

RK3566_CRU_BASE: int = 4258398208

RK3566_CRU_GATE_CON31_OFFSET: int = 892

RK3566_CRU_GATE_CON31: int = 4258399100

RK3566_CRU_GATE_CON32_OFFSET: int = 896

RK3566_CRU_GATE_CON32: int = 4258399104

RK3566_PMUCRU_PMUGATE_CON01_OFFSET: int = 388

RK3566_GRF_GPIO1_A_IOMUX_L_OFFSET: int = 0

RK3566_GRF_GPIO1_A_P_OFFSET: int = 128

RK3566_PMU_GRF_GPIO0_A_IOMUX_L_OFFSET: int = 0

RK3566_PMU_GRF_GPIO0_A_P_OFFSET: int = 32

RK3566_PWM_MUX_REG: int = 4257611888

RK3566_PWM2_BASE: int = 4268687360

RK3566_PWM3_BASE: int = 4268752896

RK3566_RPT: int = 24

RK3566_SCALE: int = 16

RK3566_PRESCALE: int = 12

RK3566_CLK_SRC_SEL: int = 10

RK3566_CLK_SEL: int = 9

RK3566_FORCE_CLK_EN: int = 8

RK3566_CH_CNT_EN: int = 7

RK3566_CONLOCK: int = 6

RK3566_OUTPUT_MODE: int = 5

RK3566_INACTIVE_POL: int = 4

RK3566_DUTY_POL: int = 3

RK3566_PWM_MODE: int = 1

RK3566_PWM_EN: int = 0

RK3399_GPIO1_BASE: int = 4285726720

RK3399_GPIO2_BASE: int = 4286054400

RK3399_GPIO4_BASE: int = 4286119936

RK3399_GPIO_NUM: int = 64

def RK3399_GPIO_BIT(x: int) -> int: ...

RK3399_GPIO_SWPORTA_DR_OFFSET: int = 0

RK3399_GPIO_SWPORTA_DDR_OFFSET: int = 4

RK3399_GPIO_EXT_PORTA_OFFSET: int = 80

RK3399_GRF_GPIO2_3_4_P_OFFSET: int = 64

RK3399_PMUGRF_GPIO0_1_P_OFFSET: int = 64

RK3399_PMUGRF_BASE: int = 4281466880

RK3399_GRF_BASE: int = 4286046208

RK3399_CRU_BASE: int = 4285923328

RK3399_PMUCRU_BASE: int = 4285857792

RK3399_CRU_CLKGATE_CON31_OFFSET: int = 892

RK3399_PMUCRU_CLKGATE_CON1_OFFSET: int = 260

RK3328_GPIO2_BASE: int = 4280483840

RK3328_GPIO3_BASE: int = 4280549376

RK3328_GPIO_NUM: int = 64

RK3328_GPIO_SWPORTA_DR_OFFSET: int = 0

RK3328_GPIO_SWPORTA_DDR_OFFSET: int = 4

RK3328_GPIO_EXT_PORTA_OFFSET: int = 80

RK3328_GRF_BASE: int = 4279238656

RK3328_CRU_BASE: int = 4282646528

RK3328_CRU_CLKGATE_CON16_OFFSET: int = 576

S905_D3_GPIO_BASE: int = 4284694528

S905_D3_GPIO_AO_BASE: int = 4286578688

S905_D3_GPIO_PWM_BASE: int = 4291923968

S905_D3_GPIO_PWM_AO_BASE: int = 4286586880

S905_D3_GPIO_A_OUT_EN_REG: int = 4284694816

S905_D3_GPIO_A_OUT_REG: int = 4284694817

S905_D3_GPIO_A_IN_REG: int = 4284694818

S905_D3_GPIO_A_PUPD_REG: int = 4284694847

S905_D3_GPIO_A_PUEN_REG: int = 4284694861

S905_D3_GPIO_A_MUX_REG1: int = 4284694973

S905_D3_GPIO_A_MUX_REG2: int = 4284694974

S905_D3_GPIO_C_OUT_EN_REG: int = 4284694803

S905_D3_GPIO_C_OUT_REG: int = 4284694804

S905_D3_GPIO_C_IN_REG: int = 4284694805

S905_D3_GPIO_C_PUPD_REG: int = 4284694843

S905_D3_GPIO_C_PUEN_REG: int = 4284694857

S905_D3_GPIO_C_MUX_REG: int = 4284694969

S905_D3_GPIO_H_OUT_EN_REG: int = 4284694809

S905_D3_GPIO_H_OUT_REG: int = 4284694810

S905_D3_GPIO_H_IN_REG: int = 4284694811

S905_D3_GPIO_H_PUPD_REG: int = 4284694845

S905_D3_GPIO_H_PUEN_REG: int = 4284694859

S905_D3_GPIO_H_MUX_REG1: int = 4284694971

S905_D3_GPIO_H_MUX_REG2: int = 4284694972

S905_D3_GPIO_AO_OUT_EN_REG: int = 4286578953

S905_D3_GPIO_AO_OUT_REG: int = 4286578957

S905_D3_GPIO_AO_IN_REG: int = 4286578954

S905_D3_GPIO_AO_PUPD_REG: int = 4286578955

S905_D3_GPIO_AO_PUEN_REG: int = 4286578956

S905_D3_GPIO_AO_MUX_REG1: int = 4286578949

S905_D3_GPIO_AO_MUX_REG2: int = 4286578950

S905_D3_PWM_DUTY_CYCLE_F_REG: int = 4291923969

S905_D3_PWM_MISC_EF_REG: int = 4291923970

S905_D3_PWM_DUTY_CYCLE_AO_C_REG: int = 4286586880

S905_D3_PWM_MISC_AO_CD_REG: int = 4286586882

S905_D3_PWM_CLK_EN_1: int = 23

S905_D3_PWM_CLK_DIV_1: int = 16

S905_D3_PWM_CLK_EN_0: int = 15

S905_D3_PWM_CLK_DIV_0: int = 8

S905_D3_PWM_CLK_SEL_1: int = 6

S905_D3_PWM_CLK_SEL_0: int = 4

S905_D3_PWM_EN_1: int = 1

S905_D3_PWM_EN_0: int = 0

A310_B_IOMUX_BASE_GROUP0: int = 3288334336

A310_B_IOMUX_BASE_GROUP1: int = 3288334336

A310_B_IOMUX_BASE_GROUP2: int = 2184314880

A310_B_IOMUX_BASE_GROUP3: int = 2184314880

A310_B_IOMUX_BASE_GROUP4: int = 2685665280

A310_B_IOMUX_BASE_GROUP5: int = 12886802432

A310_B_IOMUX_BASE_GROUP7: int = 17181179904

A310_B_GPIO_BASE_GROUP0: int = 3288596480

A310_B_GPIO_BASE_GROUP1: int = 3288662016

A310_B_GPIO_BASE_GROUP2: int = 2182021120

A310_B_GPIO_BASE_GROUP3: int = 2182086656

A310_B_GPIO_BASE_GROUP4: int = 2685796352

A310_B_GPIO_BASE_GROUP5: int = 12886343680

A310_B_GPIO_BASE_GROUP7: int = 17181245440

A310_B_GPIO_DIRECTION_OFFSET: int = 4

A310_B_GPIO_SET_VALUE_OFFSET: int = 0

A310_B_GPIO_GET_VALUE_OFFSET: int = 80

A310_B_PWM_BASE: int = 3288858624

A310_B_PWM_PRD2_OFFSET: int = 32

A310_B_PWM_CH2_PWL_OFFSET: int = 36

A310_B_PWM_CH2_PWH_OFFSET: int = 40

A310_B_PWM_PRD3_OFFSET: int = 44

A310_B_PWM_CH3_PWL_OFFSET: int = 48

A310_B_PWM_CH3_PWH_OFFSET: int = 52

A310_B_PWM_MEASURE_TIME_OFFSET: int = 264

A310_P_IOMUX_BASE_GROUP0: int = 2757099520

A310_P_IOMUX_BASE_GROUP1: int = 2757099520

A310_P_IOMUX_BASE_GROUP2: int = 2757099520

A310_P_IOMUX_BASE_GROUP3: int = 4201512960

A310_P_IOMUX_BASE_GROUP4: int = 2333474816

A310_P_IOMUX_BASE_GROUP5: int = 2214723584

A310_P_GPIO_BASE_GROUP0: int = 2756706304

A310_P_GPIO_BASE_GROUP1: int = 2756771840

A310_P_GPIO_BASE_GROUP2: int = 2756837376

A310_P_GPIO_BASE_GROUP3: int = 4201316352

A310_P_GPIO_BASE_GROUP4: int = 2333081600

A310_P_GPIO_BASE_GROUP5: int = 2215510016

A310_P_GPIO_DIRECTION_OFFSET: int = 4

A310_P_GPIO_SET_VALUE_OFFSET: int = 0

A310_P_GPIO_GET_VALUE_OFFSET: int = 80

A310_P_PWM_BASE: int = 2214592512

A310_P_PWM_PRD1_OFFSET: int = 20

A310_P_PWM_CH1_PWL_OFFSET: int = 24

A310_P_PWM_CH1_PWH_OFFSET: int = 28

A310_P_PWM_MEASURE_TIME_OFFSET: int = 264

JH7110_SYS_IOMUX_BASE: int = 319029248

JH7110_SYS_DOEN_REG_BASE: int = 0

JH7110_SYS_DOUT_REG_BASE: int = 64

JH7110_SYS_GPI_REG_BASE: int = 128

JH7110_SYS_GPIO_IN_REG_BASE: int = 280

JH7110_DOEN_MASK: int = 63

JH7110_DOUT_MASK: int = 127

JH7110_SYS_GPO_PDA_0_74_CFG: int = 288

JH7110_GPOEN_ENABLE: int = 0

JH7110_GPOEN_DISABLE: int = 1

GPIO_NUM_PER_WORD: int = 32

KYX1_GPIO_BASE: int = 3556872192

KYX1_IOMUX_BASE: int = 3556892672

KYX1_FUNC_MASK: int = 65399

KYX1_OFFSET: int = 1020

KYX1_PULL_DIS: int = 0

KYX1_PULL_UP: int = 49152

KYX1_PULL_DOWN: int = 40960

PI_GPIO_MASK: int = 4294967232

WPI_MODE_PINS: int = 0

WPI_MODE_GPIO: int = 1

WPI_MODE_GPIO_SYS: int = 2

WPI_MODE_PHYS: int = 3

WPI_MODE_PIFACE: int = 4

WPI_MODE_UNINITIALISED: int = -1

INPUT: int = 0

OUTPUT: int = 1

PWM_OUTPUT: int = 2

GPIO_CLOCK: int = 3

SOFT_PWM_OUTPUT: int = 4

SOFT_TONE_OUTPUT: int = 5

PWM_TONE_OUTPUT: int = 6

LOW: int = 0

HIGH: int = 1

PUD_OFF: int = 0

PUD_DOWN: int = 1

PUD_UP: int = 2

PWM_MODE_MS: int = 0

PWM_MODE_BAL: int = 1

INT_EDGE_SETUP: int = 0

INT_EDGE_FALLING: int = 1

INT_EDGE_RISING: int = 2

INT_EDGE_BOTH: int = 3

PI_MODEL_3: int = 0

PI_MODEL_LTIE_2: int = 1

PI_MODEL_ZERO: int = 2

PI_MODEL_H3: int = 3

PI_MODEL_ZERO_PLUS_2: int = 4

PI_MODEL_WIN: int = 5

PI_MODEL_PRIME: int = 6

PI_MODEL_PC_2: int = 7

PI_MODEL_ZERO_PLUS: int = 8

PI_MODEL_ZERO_2: int = 9

PI_MODEL_ZERO_2_W: int = 10

PI_MODEL_ZERO_3_PLUS: int = 11

PI_MODEL_800: int = 15

PI_MODEL_4: int = 16

PI_MODEL_4_LTS: int = 17

PI_MODEL_RK3399: int = 18

PI_MODEL_R1_PLUS: int = 22

PI_MODEL_900: int = 23

PI_MODEL_5: int = 24

PI_MODEL_5_B: int = 25

PI_MODEL_5_PRO: int = 26

PI_MODEL_5_MAX: int = 27

PI_MODEL_5_PLUS: int = 28

PI_MODEL_CM5: int = 29

PI_MODEL_CM5_TABLET: int = 39

PI_MODEL_5_ULTRA: int = 40

PI_MODEL_AI_MAX: int = 41

PI_MODEL_CM4: int = 50

PI_MODEL_3_B: int = 51

PI_MODEL_3_PLUS: int = 60

PI_MODEL_AI_PRO: int = 70

PI_MODEL_KUNPENG_PRO: int = 71

PI_MODEL_AI_STATION: int = 75

PI_MODEL_RV: int = 80

PI_MODEL_4_A: int = 90

PI_MODEL_RV2: int = 100

PI_MODEL_4_PRO: int = 110

PI_MODEL_ZERO_3_W: int = 111

PI_MODEL_ZERO_4: int = 112

WPI_FATAL: bool = True

WPI_ALMOST: bool = False
