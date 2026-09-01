import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.wiring_pi")

def test_struct_sunxigpioinfo():
    obj=m.SunxiGPIOInfo()
    _=obj.gpio_base_addr
    _=obj.r_gpio_base_addr
    assert obj.gpio_address == 0
    obj.gpio_address=0
    assert obj.r_gpio_address == 0
    obj.r_gpio_address=0
    _=obj.gpio_base_offset
    _=obj.r_gpio_base_offset
    _=obj.gpio_bank_offset
    _=obj.pull_offset
    _=obj.r_gpio_pull_offset
    _=obj.gpio_cfg_mask
    _=obj.pwm_base_addr
    assert obj.pwm_address == 0
    obj.pwm_address=0
    _=obj.pwm_ctrl
    _=obj.pwm_period
    _=obj.pwm_clk
    _=obj.pwm_en
    _=obj.pwm_type
    _=obj.pwm_bit_en
    _=obj.pwm_bit_act
    _=obj.pwm_bit_sclk
    _=obj.pwm_bit_mode
    _=obj.pwm_bit_pulse

def test_struct_rk3588socinfo():
    obj=m.Rk3588SocInfo()
    assert obj.gpio0_base_address == 0
    obj.gpio0_base_address=0
    assert obj.gpio1_base_address == 0
    obj.gpio1_base_address=0
    assert obj.gpio2_base_address == 0
    obj.gpio2_base_address=0
    assert obj.gpio3_base_address == 0
    obj.gpio3_base_address=0
    assert obj.gpio4_base_address == 0
    obj.gpio4_base_address=0
    assert obj.pmu1_ioc_base_address == 0
    obj.pmu1_ioc_base_address=0
    assert obj.pmu2_ioc_base_address == 0
    obj.pmu2_ioc_base_address=0
    assert obj.bus_ioc_base_address == 0
    obj.bus_ioc_base_address=0
    assert obj.cur_base_address == 0
    obj.cur_base_address=0
    assert obj.pmu1cur_base_address == 0
    obj.pmu1cur_base_address=0
    assert obj.vccio1_4_ioc_base_address == 0
    obj.vccio1_4_ioc_base_address=0
    assert obj.vccio3_5_ioc_base_address == 0
    obj.vccio3_5_ioc_base_address=0
    assert obj.vccio6_ioc_base_address == 0
    obj.vccio6_ioc_base_address=0
    assert obj.pwm0_base_address == 0
    obj.pwm0_base_address=0
    assert obj.pwm1_base_address == 0
    obj.pwm1_base_address=0
    assert obj.pwm2_base_address == 0
    obj.pwm2_base_address=0
    assert obj.pwm3_base_address == 0
    obj.pwm3_base_address=0
    _=obj.pwm_base
    _=obj.pwm_mux
    _=obj.pwm_mux_val
    _=obj.pwm_mux_offset
    _=obj.ch_period_hpr
    _=obj.ch_duty_lpr
    _=obj.ch_crtl

def test_struct_rk3566socinfo():
    obj=m.Rk3566SocInfo()
    assert obj.gpio0_base_address == 0
    obj.gpio0_base_address=0
    assert obj.gpio1_base_address == 0
    obj.gpio1_base_address=0
    assert obj.gpio2_base_address == 0
    obj.gpio2_base_address=0
    assert obj.gpio3_base_address == 0
    obj.gpio3_base_address=0
    assert obj.gpio4_base_address == 0
    obj.gpio4_base_address=0
    assert obj.pmu_grf_base_address == 0
    obj.pmu_grf_base_address=0
    assert obj.sys_grf_base_address == 0
    obj.sys_grf_base_address=0
    assert obj.cru_base_address == 0
    obj.cru_base_address=0
    assert obj.pmu_cru_base_address == 0
    obj.pmu_cru_base_address=0
    assert obj.pwm2_base_address == 0
    obj.pwm2_base_address=0
    assert obj.pwm3_base_address == 0
    obj.pwm3_base_address=0
    _=obj.cru_gate_con
    _=obj.cru_gate_con_offset
    _=obj.pwm_base
    _=obj.pwm_mux
    _=obj.pwm_mux_val
    _=obj.pwm_mux_offset
    _=obj.ch_period_hpr
    _=obj.ch_duty_lpr
    _=obj.ch_crtl

def test_struct_rk3399socinfo():
    obj=m.Rk3399SocInfo()
    assert obj.gpio2_base_address == 0
    obj.gpio2_base_address=0
    assert obj.grf_base_address == 0
    obj.grf_base_address=0
    assert obj.cru_base_address == 0
    obj.cru_base_address=0
    assert obj.pmucru_base_address == 0
    obj.pmucru_base_address=0
    assert obj.pmugrf_base_address == 0
    obj.pmugrf_base_address=0
    assert obj.gpio1_base_address == 0
    obj.gpio1_base_address=0
    assert obj.gpio4_base_address == 0
    obj.gpio4_base_address=0

def test_struct_rk3328socinfo():
    obj=m.Rk3328SocInfo()
    assert obj.gpio2_base_address == 0
    obj.gpio2_base_address=0
    assert obj.gpio3_base_address == 0
    obj.gpio3_base_address=0
    assert obj.cru_base_address == 0
    obj.cru_base_address=0
    assert obj.grf_base_address == 0
    obj.grf_base_address=0

def test_struct_s905d3gpioinfo():
    obj=m.S905d3GPIOInfo()
    assert obj.gpio_base_address == 0
    obj.gpio_base_address=0
    assert obj.gpio_ao_base_address == 0
    obj.gpio_ao_base_address=0
    assert obj.gpio_pwm_base_address == 0
    obj.gpio_pwm_base_address=0
    assert obj.gpio_pwm_ao_base_address == 0
    obj.gpio_pwm_ao_base_address=0
    _=obj.gpio_out_en
    _=obj.gpio_out
    _=obj.gpio_in
    _=obj.gpio_pupd
    _=obj.gpio_puen
    _=obj.gpio_mux
    _=obj.gpio_out_en_offset
    _=obj.gpio_out_offset
    _=obj.gpio_in_offset
    _=obj.gpio_pupd_offset
    _=obj.gpio_puen_offset
    _=obj.gpio_mux_offset
    _=obj.pwm_duty_cycle
    _=obj.pwm_misc

def test_struct_a310bgpioinfo():
    obj=m.A310bGPIOInfo()
    assert obj.iomux_base_group0_address == 0
    obj.iomux_base_group0_address=0
    assert obj.iomux_base_group1_address == 0
    obj.iomux_base_group1_address=0
    assert obj.iomux_base_group2_address == 0
    obj.iomux_base_group2_address=0
    assert obj.iomux_base_group3_address == 0
    obj.iomux_base_group3_address=0
    assert obj.iomux_base_group4_address == 0
    obj.iomux_base_group4_address=0
    assert obj.iomux_base_group5_address == 0
    obj.iomux_base_group5_address=0
    assert obj.iomux_base_group7_address == 0
    obj.iomux_base_group7_address=0
    assert obj.gpio_base_group0_address == 0
    obj.gpio_base_group0_address=0
    assert obj.gpio_base_group1_address == 0
    obj.gpio_base_group1_address=0
    assert obj.gpio_base_group2_address == 0
    obj.gpio_base_group2_address=0
    assert obj.gpio_base_group3_address == 0
    obj.gpio_base_group3_address=0
    assert obj.gpio_base_group4_address == 0
    obj.gpio_base_group4_address=0
    assert obj.gpio_base_group5_address == 0
    obj.gpio_base_group5_address=0
    assert obj.gpio_base_group7_address == 0
    obj.gpio_base_group7_address=0
    assert obj.pwm_base_address == 0
    obj.pwm_base_address=0
    _=obj.pwm_prd2_phyaddr
    _=obj.pwm_ch2_pwl_phyaddr
    _=obj.pwm_ch2_pwh_phyaddr
    _=obj.pwm_prd3_phyaddr
    _=obj.pwm_ch3_pwl_phyaddr
    _=obj.pwm_ch3_pwh_phyaddr
    _=obj.pwm_measure_time_phyaddr

def test_struct_a310pgpioinfo():
    obj=m.A310pGPIOInfo()
    assert obj.iomux_base_group0_address == 0
    obj.iomux_base_group0_address=0
    assert obj.iomux_base_group1_address == 0
    obj.iomux_base_group1_address=0
    assert obj.iomux_base_group2_address == 0
    obj.iomux_base_group2_address=0
    assert obj.iomux_base_group3_address == 0
    obj.iomux_base_group3_address=0
    assert obj.iomux_base_group4_address == 0
    obj.iomux_base_group4_address=0
    assert obj.iomux_base_group5_address == 0
    obj.iomux_base_group5_address=0
    assert obj.gpio_base_group0_address == 0
    obj.gpio_base_group0_address=0
    assert obj.gpio_base_group1_address == 0
    obj.gpio_base_group1_address=0
    assert obj.gpio_base_group2_address == 0
    obj.gpio_base_group2_address=0
    assert obj.gpio_base_group3_address == 0
    obj.gpio_base_group3_address=0
    assert obj.gpio_base_group4_address == 0
    obj.gpio_base_group4_address=0
    assert obj.gpio_base_group5_address == 0
    obj.gpio_base_group5_address=0
    assert obj.pwm_base_address == 0
    obj.pwm_base_address=0
    _=obj.pwm_prd1_phyaddr
    _=obj.pwm_ch1_pwl_phyaddr
    _=obj.pwm_ch1_pwh_phyaddr
    _=obj.pwm_measure_time_phyaddr

def test_struct_jh7110socinfo():
    obj=m.Jh7110SocInfo()
    assert obj.sys_iomux_base_address == 0
    obj.sys_iomux_base_address=0

def test_struct_kyx1socinfo():
    obj=m.Kyx1SocInfo()
    assert obj.iomux_base_address == 0
    obj.iomux_base_address=0
    assert obj.gpio_base_address == 0
    obj.gpio_base_address=0

def test_struct_wiringpinodestruct():
    obj=m.WiringPiNodeStruct()
    _=obj.pin_base
    _=obj.pin_max
    _=obj.fd
    _=obj.data0
    _=obj.data1
    _=obj.data2
    _=obj.data3
    assert obj.pin_mode_address == 0
    obj.pin_mode_address=0
    assert obj.pull_up_dn_control_address == 0
    obj.pull_up_dn_control_address=0
    assert obj.digital_read_address == 0
    obj.digital_read_address=0
    assert obj.digital_write_address == 0
    obj.digital_write_address=0
    assert obj.pwm_write_address == 0
    obj.pwm_write_address=0
    assert obj.analog_read_address == 0
    obj.analog_read_address=0
    assert obj.analog_write_address == 0
    obj.analog_write_address=0
    assert obj.next_address == 0
    obj.next_address=0

def test_pi_gpio_layout_oops():
    _=m.pi_gpio_layout_oops("x")

def test_wiring_pi_failure():
    m.wiring_pi_failure(1, "safe text")

def test_wiring_pi_find_node():
    _=m.wiring_pi_find_node(1)

def test_wiring_pi_new_node():
    _=m.wiring_pi_new_node(1, 1)

def test_wiring_pi_version():
    _=m.wiring_pi_version()

def test_wiring_pi_setup():
    _=m.wiring_pi_setup()

def test_wiring_pi_setup_sys():
    _=m.wiring_pi_setup_sys()

def test_wiring_pi_setup_gpio():
    _=m.wiring_pi_setup_gpio()

def test_wiring_pi_setup_phys():
    _=m.wiring_pi_setup_phys()

def test_pin_mode_alt():
    _=m.pin_mode_alt(1, 1)

def test_pin_mode():
    _=m.pin_mode(1, 1)

def test_pull_up_dn_control():
    _=m.pull_up_dn_control(1, 1)

def test_digital_read():
    _=m.digital_read(1)

def test_digital_write():
    _=m.digital_write(1, 1)

def test_digital_read8():
    with pytest.raises(NotImplementedError): m.digital_read8(1)

def test_digital_write8():
    with pytest.raises(NotImplementedError): m.digital_write8(1, 1)

def test_pwm_write():
    _=m.pwm_write(1, 1)

def test_analog_read():
    _=m.analog_read(1)

def test_analog_write():
    _=m.analog_write(1, 1)

def test_wiring_pi_setup_pi_face():
    with pytest.raises(NotImplementedError): m.wiring_pi_setup_pi_face()

def test_wiring_pi_setup_pi_face_for_gpio_prog():
    with pytest.raises(NotImplementedError): m.wiring_pi_setup_pi_face_for_gpio_prog()

def test_pi_board_id():
    _=m.pi_board_id()

def test_wpi_pin_to_gpio():
    _=m.wpi_pin_to_gpio(1)

def test_phys_pin_to_gpio():
    _=m.phys_pin_to_gpio(1)

def test_set_pad_drive():
    _=m.set_pad_drive(1, 1)

def test_get_alt():
    _=m.get_alt(1)

def test_h618_set_pwm_reg():
    _=m.h618_set_pwm_reg(1, m.SunxiGPIOInfo())

def test_s905d3_set_gpio_reg():
    _=m.s905d3_set_gpio_reg(1, m.S905d3GPIOInfo())

def test_rk3588_set_pwm_reg():
    _=m.rk3588_set_pwm_reg(1, m.Rk3588SocInfo())

def test_rk3566_set_pwm_reg():
    _=m.rk3566_set_pwm_reg(1, m.Rk3566SocInfo())

def test_sunxi_pwm_set_enable():
    _=m.sunxi_pwm_set_enable(1)

def test_pwm_tone_write():
    _=m.pwm_tone_write(1, 1)

def test_pwm_set_mode():
    _=m.pwm_set_mode(1, 1)

def test_pwm_set_range():
    _=m.pwm_set_range(1, 1)

def test_pwm_set_clock():
    _=m.pwm_set_clock(1, 1)

def test_gpio_clock_set():
    _=m.gpio_clock_set(1, 1)

def test_digital_read_byte():
    _=m.digital_read_byte()

def test_digital_read_byte2():
    _=m.digital_read_byte2()

def test_digital_write_byte():
    _=m.digital_write_byte(1)

def test_digital_write_byte2():
    _=m.digital_write_byte2(1)

def test_wait_for_interrupt():
    _=m.wait_for_interrupt(1, 1)

def test_wiring_pi_isr():
    seen=[]
    assert m.wiring_pi_isr(1,1,lambda:seen.append(1))==0
    assert seen==[1]

def test_pi_thread_create():
    seen=[]
    assert m.pi_thread_create(lambda:seen.append(1))==0
    assert seen==[1]

def test_pi_lock():
    _=m.pi_lock(1)

def test_pi_unlock():
    _=m.pi_unlock(1)

def test_pi_hi_pri():
    _=m.pi_hi_pri(1)

def test_delay():
    _=m.delay(1)

def test_delay_microseconds():
    _=m.delay_microseconds(1)

def test_millis():
    _=m.millis()

def test_micros():
    _=m.micros()

def test_read_r():
    _=m.read_r(1)

def test_write_r():
    _=m.write_r(1, 1)

def test_orangepi_get_gpio_mode():
    _=m.orangepi_get_gpio_mode(1)

def test_orangepi_set_gpio_mode():
    _=m.orangepi_set_gpio_mode(1, 1)

def test_orangepi_digital_read():
    _=m.orangepi_digital_read(1)

def test_orangepi_digital_write():
    _=m.orangepi_digital_write(1, 1)

def test_orangepi_set_gpio_alt():
    _=m.orangepi_set_gpio_alt(1, 1)

def test_orange_pi_set_gpio_pull_up_dn_control():
    _=m.orange_pi_set_gpio_pull_up_dn_control(1, 1)

def test_orangepi_pwm_set_act():
    _=m.orangepi_pwm_set_act(1, 1)

def test_orangepi_pwm_set_period():
    _=m.orangepi_pwm_set_period(1, 1)

def test_orangepi_pwm_set_clk():
    _=m.orangepi_pwm_set_clk(1, 1)

def test_orangepi_pwm_set_tone():
    _=m.orangepi_pwm_set_tone(1, 1)

def test_set_soc_info():
    _=m.set_soc_info()

def test_variable_wiring_pi_debug():
    x=m.get_wiring_pi_debug();m.set_wiring_pi_debug(x)

def test_variable_pi_model_names():
    assert hasattr(m,"pi_model_names")

def test_variable_pi_revision_names():
    assert hasattr(m,"pi_revision_names")

def test_variable_pi_maker_names():
    assert hasattr(m,"pi_maker_names")

def test_variable_pi_memory_size():
    assert hasattr(m,"pi_memory_size")

def test_variable_wiring_pi_nodes():
    assert isinstance(m.get_wiring_pi_nodes_address(),int)

def test_variable_wiring_pi_gpio():
    assert isinstance(m.get_wiring_pi_gpio_address(),int)

def test_variable_wiring_pi_pwm():
    assert isinstance(m.get_wiring_pi_pwm_address(),int)

def test_variable_wiring_pi_clk():
    assert isinstance(m.get_wiring_pi_clk_address(),int)

def test_variable_wiring_pi_pads():
    assert isinstance(m.get_wiring_pi_pads_address(),int)

def test_variable_wiring_pi_timer():
    assert isinstance(m.get_wiring_pi_timer_address(),int)

def test_variable_wiring_pi_timer_irq_raw():
    assert isinstance(m.get_wiring_pi_timer_irq_raw_address(),int)

def test_constants_and_macros():
    assert hasattr(m,"TRUE")
    assert hasattr(m,"FALSE")
    assert hasattr(m,"MAX_PIN_NUM")
    assert hasattr(m,"PI_MODEL_A")
    assert hasattr(m,"PI_MODEL_B")
    assert hasattr(m,"PI_MODEL_AP")
    assert hasattr(m,"PI_MODEL_BP")
    assert hasattr(m,"PI_MODEL_2")
    assert hasattr(m,"PI_ALPHA")
    assert hasattr(m,"PI_MODEL_CM")
    assert hasattr(m,"PI_MODEL_07")
    assert hasattr(m,"PI_MODEL_CM3")
    assert hasattr(m,"PI_MODEL_ZERO_W")
    assert hasattr(m,"PI_MODEL_3_P")
    assert hasattr(m,"PI_VERSION_1")
    assert hasattr(m,"PI_VERSION_1_1")
    assert hasattr(m,"PI_VERSION_1_2")
    assert hasattr(m,"PI_VERSION_2")
    assert hasattr(m,"PI_MAKER_SONY")
    assert hasattr(m,"PI_MAKER_EGOMAN")
    assert hasattr(m,"PI_MAKER_EMBEST")
    assert hasattr(m,"PI_MAKER_UNKNOWN")
    assert hasattr(m,"H3_GPIO_BASE_ADDR")
    assert hasattr(m,"H3_R_GPIO_BASE_ADDR")
    assert hasattr(m,"H6_GPIO_BASE_ADDR")
    assert hasattr(m,"H6_R_GPIO_BASE_ADDR")
    assert hasattr(m,"A527_GPIO_BASE_ADDR")
    assert hasattr(m,"T736_R_GPIO_BASE_ADDR")
    assert hasattr(m,"H3_PWM_BASE")
    assert hasattr(m,"H6_PWM_BASE")
    assert hasattr(m,"H616_PWM_BASE")
    assert hasattr(m,"SUNXI_V1_PWM_TYPE")
    assert hasattr(m,"SUNXI_V2_PWM_TYPE")
    assert hasattr(m,"SUNXI_V1_PWM_CH0_EN")
    assert hasattr(m,"SUNXI_V1_PWM_CH0_ACT_STA")
    assert hasattr(m,"SUNXI_V1_PWM_SCLK_CH0_GATING")
    assert hasattr(m,"SUNXI_V1_PWM_CH0_MS_MODE")
    assert hasattr(m,"SUNXI_V1_PWM_CH0_PUL_START")
    assert hasattr(m,"SUNXI_V2_PWM_ACT_STA")
    assert hasattr(m,"SUNXI_V2_PWM_SCLK_GATING")
    assert hasattr(m,"SUNXI_V2_PWM_MS_MODE")
    assert hasattr(m,"SUNXI_V2_PWM_PUL_START")
    assert hasattr(m,"SUNXI_V2_PWM1_EN")
    assert hasattr(m,"SUNXI_V2_PWM2_EN")
    assert hasattr(m,"SUNXI_V2_PWM3_EN")
    assert hasattr(m,"SUNXI_V2_PWM4_EN")
    assert hasattr(m,"PWM_CLK_DIV_120")
    assert hasattr(m,"PWM_CLK_DIV_180")
    assert hasattr(m,"PWM_CLK_DIV_240")
    assert hasattr(m,"PWM_CLK_DIV_360")
    assert hasattr(m,"PWM_CLK_DIV_480")
    assert hasattr(m,"PWM_CLK_DIV_12_K")
    assert hasattr(m,"PWM_CLK_DIV_24_K")
    assert hasattr(m,"PWM_CLK_DIV_36_K")
    assert hasattr(m,"PWM_CLK_DIV_48_K")
    assert hasattr(m,"PWM_CLK_DIV_72_K")
    assert hasattr(m,"SUNXI_PUD_OFF")
    assert hasattr(m,"SUNXI_PUD_UP")
    assert hasattr(m,"SUNXI_PUD_DOWN")
    assert hasattr(m,"RK3588_GPIO0_BASE")
    assert hasattr(m,"RK3588_GPIO1_BASE")
    assert hasattr(m,"RK3588_GPIO2_BASE")
    assert hasattr(m,"RK3588_GPIO3_BASE")
    assert hasattr(m,"RK3588_GPIO4_BASE")
    assert hasattr(m,"RK3588_GPIO_SWPORT_DR_L_OFFSET")
    assert hasattr(m,"RK3588_GPIO_SWPORT_DR_H_OFFSET")
    assert hasattr(m,"RK3588_GPIO_SWPORT_DDR_L_OFFSET")
    assert hasattr(m,"RK3588_GPIO_SWPORT_DDR_H_OFFSET")
    assert hasattr(m,"RK3588_GPIO_EXT_PORT_OFFSET")
    assert hasattr(m,"RK3588_CRU_BASE")
    assert hasattr(m,"RK3588_CRU_GATE_CON16_OFFSET")
    assert hasattr(m,"RK3588_CRU_GATE_CON17_OFFSET")
    assert hasattr(m,"RK3588_PMU1_CRU_BASE")
    assert hasattr(m,"RK3588_PMU1_CRU_GATE_CON5_OFFSET")
    assert hasattr(m,"RK3588_GPIO_NUM")
    _=m.RK3588_GPIO_BIT(1)
    assert hasattr(m,"RK3588_PMU1_IOC_BASE")
    assert hasattr(m,"RK3588_PMU1_IOC_GPIO0_A_IOMUX_SEL_L")
    assert hasattr(m,"RK3588_PMU1_IOC_GPIO0_A_IOMUX_SEL_H")
    assert hasattr(m,"RK3588_PMU1_IOC_GPIO0_B_IOMUX_SEL_L")
    assert hasattr(m,"RK3588_PMU2_IOC_BASE")
    assert hasattr(m,"RK3588_PMU2_IOC_GPIO0_B_IOMUX_SEL_H")
    assert hasattr(m,"RK3588_PMU2_IOC_GPIO0_C_IOMUX_SEL_L")
    assert hasattr(m,"RK3588_PMU2_IOC_GPIO0_C_IOMUX_SEL_H")
    assert hasattr(m,"RK3588_PMU2_IOC_GPIO0_D_IOMUX_SEL_L")
    assert hasattr(m,"RK3588_PMU2_IOC_GPIO0_D_IOMUX_SEL_H")
    assert hasattr(m,"RK3588_BUS_IOC_BASE")
    assert hasattr(m,"RK3588_VCCIO1_4_IOC_BASE")
    assert hasattr(m,"RK3588_VCCIO3_5_IOC_BASE")
    assert hasattr(m,"RK3588_VCCIO6_IOC_BASE")
    assert hasattr(m,"RK3588_PMU1_IOC_GPIO0_A_P")
    assert hasattr(m,"RK3588_PMU1_IOC_GPIO0_B_P")
    assert hasattr(m,"RK3588_PMU2_IOC_GPIO0_B_P")
    assert hasattr(m,"RK3588_PMU2_IOC_GPIO0_C_P")
    assert hasattr(m,"RK3588_PMU2_IOC_GPIO0_D_P")
    assert hasattr(m,"RK3588_VCCIO1_4_IOC_GPIO1_A_P")
    assert hasattr(m,"RK3588_VCCIO3_5_IOC_GPIO2_A_P")
    assert hasattr(m,"RK3588_VCCIO6_IOC_GPIO4_A_P")
    assert hasattr(m,"RK3588_PWM0_BASE")
    assert hasattr(m,"RK3588_PWM1_BASE")
    assert hasattr(m,"RK3588_PWM2_BASE")
    assert hasattr(m,"RK3588_PWM3_BASE")
    assert hasattr(m,"RK3588_CRU_GATE_CON19")
    assert hasattr(m,"RK3588_CRU_GATE_CON15")
    assert hasattr(m,"RK3588_PMU1_CRU_GATE_CON1")
    assert hasattr(m,"RK3588_RPT")
    assert hasattr(m,"RK3588_SCALE")
    assert hasattr(m,"RK3588_PRESCALE")
    assert hasattr(m,"RK3588_CLK_SRC_SEL")
    assert hasattr(m,"RK3588_CLK_SEL")
    assert hasattr(m,"RK3588_FORCE_CLK_EN")
    assert hasattr(m,"RK3588_CH_CNT_EN")
    assert hasattr(m,"RK3588_CONLOCK")
    assert hasattr(m,"RK3588_OUTPUT_MODE")
    assert hasattr(m,"RK3588_INACTIVE_POL")
    assert hasattr(m,"RK3588_DUTY_POL")
    assert hasattr(m,"RK3588_PWM_MODE")
    assert hasattr(m,"RK3588_PWM_EN")
    assert hasattr(m,"RK3566_GPIO0_BASE")
    assert hasattr(m,"RK3566_GPIO1_BASE")
    assert hasattr(m,"RK3566_GPIO2_BASE")
    assert hasattr(m,"RK3566_GPIO3_BASE")
    assert hasattr(m,"RK3566_GPIO4_BASE")
    assert hasattr(m,"RK3566_GPIO_SWPORT_DR_L_OFFSET")
    assert hasattr(m,"RK3566_GPIO_SWPORT_DR_H_OFFSET")
    assert hasattr(m,"RK3566_GPIO_SWPORT_DDR_L_OFFSET")
    assert hasattr(m,"RK3566_GPIO_SWPORT_DDR_H_OFFSET")
    assert hasattr(m,"RK3566_GPIO_EXT_PORT_OFFSET")
    assert hasattr(m,"RK3566_PMU_GRF_BASE")
    assert hasattr(m,"RK3566_SYS_GRF_BASE")
    assert hasattr(m,"RK3566_PMU_CRU_BASE")
    assert hasattr(m,"RK3566_CRU_BASE")
    assert hasattr(m,"RK3566_CRU_GATE_CON31_OFFSET")
    assert hasattr(m,"RK3566_CRU_GATE_CON31")
    assert hasattr(m,"RK3566_CRU_GATE_CON32_OFFSET")
    assert hasattr(m,"RK3566_CRU_GATE_CON32")
    assert hasattr(m,"RK3566_PMUCRU_PMUGATE_CON01_OFFSET")
    assert hasattr(m,"RK3566_GRF_GPIO1_A_IOMUX_L_OFFSET")
    assert hasattr(m,"RK3566_GRF_GPIO1_A_P_OFFSET")
    assert hasattr(m,"RK3566_PMU_GRF_GPIO0_A_IOMUX_L_OFFSET")
    assert hasattr(m,"RK3566_PMU_GRF_GPIO0_A_P_OFFSET")
    assert hasattr(m,"RK3566_PWM_MUX_REG")
    assert hasattr(m,"RK3566_PWM2_BASE")
    assert hasattr(m,"RK3566_PWM3_BASE")
    assert hasattr(m,"RK3566_RPT")
    assert hasattr(m,"RK3566_SCALE")
    assert hasattr(m,"RK3566_PRESCALE")
    assert hasattr(m,"RK3566_CLK_SRC_SEL")
    assert hasattr(m,"RK3566_CLK_SEL")
    assert hasattr(m,"RK3566_FORCE_CLK_EN")
    assert hasattr(m,"RK3566_CH_CNT_EN")
    assert hasattr(m,"RK3566_CONLOCK")
    assert hasattr(m,"RK3566_OUTPUT_MODE")
    assert hasattr(m,"RK3566_INACTIVE_POL")
    assert hasattr(m,"RK3566_DUTY_POL")
    assert hasattr(m,"RK3566_PWM_MODE")
    assert hasattr(m,"RK3566_PWM_EN")
    assert hasattr(m,"RK3399_GPIO1_BASE")
    assert hasattr(m,"RK3399_GPIO2_BASE")
    assert hasattr(m,"RK3399_GPIO4_BASE")
    assert hasattr(m,"RK3399_GPIO_NUM")
    _=m.RK3399_GPIO_BIT(1)
    assert hasattr(m,"RK3399_GPIO_SWPORTA_DR_OFFSET")
    assert hasattr(m,"RK3399_GPIO_SWPORTA_DDR_OFFSET")
    assert hasattr(m,"RK3399_GPIO_EXT_PORTA_OFFSET")
    assert hasattr(m,"RK3399_GRF_GPIO2_3_4_P_OFFSET")
    assert hasattr(m,"RK3399_PMUGRF_GPIO0_1_P_OFFSET")
    assert hasattr(m,"RK3399_PMUGRF_BASE")
    assert hasattr(m,"RK3399_GRF_BASE")
    assert hasattr(m,"RK3399_CRU_BASE")
    assert hasattr(m,"RK3399_PMUCRU_BASE")
    assert hasattr(m,"RK3399_CRU_CLKGATE_CON31_OFFSET")
    assert hasattr(m,"RK3399_PMUCRU_CLKGATE_CON1_OFFSET")
    assert hasattr(m,"RK3328_GPIO2_BASE")
    assert hasattr(m,"RK3328_GPIO3_BASE")
    assert hasattr(m,"RK3328_GPIO_NUM")
    assert hasattr(m,"RK3328_GPIO_SWPORTA_DR_OFFSET")
    assert hasattr(m,"RK3328_GPIO_SWPORTA_DDR_OFFSET")
    assert hasattr(m,"RK3328_GPIO_EXT_PORTA_OFFSET")
    assert hasattr(m,"RK3328_GRF_BASE")
    assert hasattr(m,"RK3328_CRU_BASE")
    assert hasattr(m,"RK3328_CRU_CLKGATE_CON16_OFFSET")
    assert hasattr(m,"S905_D3_GPIO_BASE")
    assert hasattr(m,"S905_D3_GPIO_AO_BASE")
    assert hasattr(m,"S905_D3_GPIO_PWM_BASE")
    assert hasattr(m,"S905_D3_GPIO_PWM_AO_BASE")
    assert hasattr(m,"S905_D3_GPIO_A_OUT_EN_REG")
    assert hasattr(m,"S905_D3_GPIO_A_OUT_REG")
    assert hasattr(m,"S905_D3_GPIO_A_IN_REG")
    assert hasattr(m,"S905_D3_GPIO_A_PUPD_REG")
    assert hasattr(m,"S905_D3_GPIO_A_PUEN_REG")
    assert hasattr(m,"S905_D3_GPIO_A_MUX_REG1")
    assert hasattr(m,"S905_D3_GPIO_A_MUX_REG2")
    assert hasattr(m,"S905_D3_GPIO_C_OUT_EN_REG")
    assert hasattr(m,"S905_D3_GPIO_C_OUT_REG")
    assert hasattr(m,"S905_D3_GPIO_C_IN_REG")
    assert hasattr(m,"S905_D3_GPIO_C_PUPD_REG")
    assert hasattr(m,"S905_D3_GPIO_C_PUEN_REG")
    assert hasattr(m,"S905_D3_GPIO_C_MUX_REG")
    assert hasattr(m,"S905_D3_GPIO_H_OUT_EN_REG")
    assert hasattr(m,"S905_D3_GPIO_H_OUT_REG")
    assert hasattr(m,"S905_D3_GPIO_H_IN_REG")
    assert hasattr(m,"S905_D3_GPIO_H_PUPD_REG")
    assert hasattr(m,"S905_D3_GPIO_H_PUEN_REG")
    assert hasattr(m,"S905_D3_GPIO_H_MUX_REG1")
    assert hasattr(m,"S905_D3_GPIO_H_MUX_REG2")
    assert hasattr(m,"S905_D3_GPIO_AO_OUT_EN_REG")
    assert hasattr(m,"S905_D3_GPIO_AO_OUT_REG")
    assert hasattr(m,"S905_D3_GPIO_AO_IN_REG")
    assert hasattr(m,"S905_D3_GPIO_AO_PUPD_REG")
    assert hasattr(m,"S905_D3_GPIO_AO_PUEN_REG")
    assert hasattr(m,"S905_D3_GPIO_AO_MUX_REG1")
    assert hasattr(m,"S905_D3_GPIO_AO_MUX_REG2")
    assert hasattr(m,"S905_D3_PWM_DUTY_CYCLE_F_REG")
    assert hasattr(m,"S905_D3_PWM_MISC_EF_REG")
    assert hasattr(m,"S905_D3_PWM_DUTY_CYCLE_AO_C_REG")
    assert hasattr(m,"S905_D3_PWM_MISC_AO_CD_REG")
    assert hasattr(m,"S905_D3_PWM_CLK_EN_1")
    assert hasattr(m,"S905_D3_PWM_CLK_DIV_1")
    assert hasattr(m,"S905_D3_PWM_CLK_EN_0")
    assert hasattr(m,"S905_D3_PWM_CLK_DIV_0")
    assert hasattr(m,"S905_D3_PWM_CLK_SEL_1")
    assert hasattr(m,"S905_D3_PWM_CLK_SEL_0")
    assert hasattr(m,"S905_D3_PWM_EN_1")
    assert hasattr(m,"S905_D3_PWM_EN_0")
    assert hasattr(m,"A310_B_IOMUX_BASE_GROUP0")
    assert hasattr(m,"A310_B_IOMUX_BASE_GROUP1")
    assert hasattr(m,"A310_B_IOMUX_BASE_GROUP2")
    assert hasattr(m,"A310_B_IOMUX_BASE_GROUP3")
    assert hasattr(m,"A310_B_IOMUX_BASE_GROUP4")
    assert hasattr(m,"A310_B_IOMUX_BASE_GROUP5")
    assert hasattr(m,"A310_B_IOMUX_BASE_GROUP7")
    assert hasattr(m,"A310_B_GPIO_BASE_GROUP0")
    assert hasattr(m,"A310_B_GPIO_BASE_GROUP1")
    assert hasattr(m,"A310_B_GPIO_BASE_GROUP2")
    assert hasattr(m,"A310_B_GPIO_BASE_GROUP3")
    assert hasattr(m,"A310_B_GPIO_BASE_GROUP4")
    assert hasattr(m,"A310_B_GPIO_BASE_GROUP5")
    assert hasattr(m,"A310_B_GPIO_BASE_GROUP7")
    assert hasattr(m,"A310_B_GPIO_DIRECTION_OFFSET")
    assert hasattr(m,"A310_B_GPIO_SET_VALUE_OFFSET")
    assert hasattr(m,"A310_B_GPIO_GET_VALUE_OFFSET")
    assert hasattr(m,"A310_B_PWM_BASE")
    assert hasattr(m,"A310_B_PWM_PRD2_OFFSET")
    assert hasattr(m,"A310_B_PWM_CH2_PWL_OFFSET")
    assert hasattr(m,"A310_B_PWM_CH2_PWH_OFFSET")
    assert hasattr(m,"A310_B_PWM_PRD3_OFFSET")
    assert hasattr(m,"A310_B_PWM_CH3_PWL_OFFSET")
    assert hasattr(m,"A310_B_PWM_CH3_PWH_OFFSET")
    assert hasattr(m,"A310_B_PWM_MEASURE_TIME_OFFSET")
    assert hasattr(m,"A310_P_IOMUX_BASE_GROUP0")
    assert hasattr(m,"A310_P_IOMUX_BASE_GROUP1")
    assert hasattr(m,"A310_P_IOMUX_BASE_GROUP2")
    assert hasattr(m,"A310_P_IOMUX_BASE_GROUP3")
    assert hasattr(m,"A310_P_IOMUX_BASE_GROUP4")
    assert hasattr(m,"A310_P_IOMUX_BASE_GROUP5")
    assert hasattr(m,"A310_P_GPIO_BASE_GROUP0")
    assert hasattr(m,"A310_P_GPIO_BASE_GROUP1")
    assert hasattr(m,"A310_P_GPIO_BASE_GROUP2")
    assert hasattr(m,"A310_P_GPIO_BASE_GROUP3")
    assert hasattr(m,"A310_P_GPIO_BASE_GROUP4")
    assert hasattr(m,"A310_P_GPIO_BASE_GROUP5")
    assert hasattr(m,"A310_P_GPIO_DIRECTION_OFFSET")
    assert hasattr(m,"A310_P_GPIO_SET_VALUE_OFFSET")
    assert hasattr(m,"A310_P_GPIO_GET_VALUE_OFFSET")
    assert hasattr(m,"A310_P_PWM_BASE")
    assert hasattr(m,"A310_P_PWM_PRD1_OFFSET")
    assert hasattr(m,"A310_P_PWM_CH1_PWL_OFFSET")
    assert hasattr(m,"A310_P_PWM_CH1_PWH_OFFSET")
    assert hasattr(m,"A310_P_PWM_MEASURE_TIME_OFFSET")
    assert hasattr(m,"JH7110_SYS_IOMUX_BASE")
    assert hasattr(m,"JH7110_SYS_DOEN_REG_BASE")
    assert hasattr(m,"JH7110_SYS_DOUT_REG_BASE")
    assert hasattr(m,"JH7110_SYS_GPI_REG_BASE")
    assert hasattr(m,"JH7110_SYS_GPIO_IN_REG_BASE")
    assert hasattr(m,"JH7110_DOEN_MASK")
    assert hasattr(m,"JH7110_DOUT_MASK")
    assert hasattr(m,"JH7110_SYS_GPO_PDA_0_74_CFG")
    assert hasattr(m,"JH7110_GPOEN_ENABLE")
    assert hasattr(m,"JH7110_GPOEN_DISABLE")
    assert hasattr(m,"GPIO_NUM_PER_WORD")
    assert hasattr(m,"KYX1_GPIO_BASE")
    assert hasattr(m,"KYX1_IOMUX_BASE")
    assert hasattr(m,"KYX1_FUNC_MASK")
    assert hasattr(m,"KYX1_OFFSET")
    assert hasattr(m,"KYX1_PULL_DIS")
    assert hasattr(m,"KYX1_PULL_UP")
    assert hasattr(m,"KYX1_PULL_DOWN")
    assert hasattr(m,"PI_GPIO_MASK")
    assert hasattr(m,"WPI_MODE_PINS")
    assert hasattr(m,"WPI_MODE_GPIO")
    assert hasattr(m,"WPI_MODE_GPIO_SYS")
    assert hasattr(m,"WPI_MODE_PHYS")
    assert hasattr(m,"WPI_MODE_PIFACE")
    assert hasattr(m,"WPI_MODE_UNINITIALISED")
    assert hasattr(m,"INPUT")
    assert hasattr(m,"OUTPUT")
    assert hasattr(m,"PWM_OUTPUT")
    assert hasattr(m,"GPIO_CLOCK")
    assert hasattr(m,"SOFT_PWM_OUTPUT")
    assert hasattr(m,"SOFT_TONE_OUTPUT")
    assert hasattr(m,"PWM_TONE_OUTPUT")
    assert hasattr(m,"LOW")
    assert hasattr(m,"HIGH")
    assert hasattr(m,"PUD_OFF")
    assert hasattr(m,"PUD_DOWN")
    assert hasattr(m,"PUD_UP")
    assert hasattr(m,"PWM_MODE_MS")
    assert hasattr(m,"PWM_MODE_BAL")
    assert hasattr(m,"INT_EDGE_SETUP")
    assert hasattr(m,"INT_EDGE_FALLING")
    assert hasattr(m,"INT_EDGE_RISING")
    assert hasattr(m,"INT_EDGE_BOTH")
    assert hasattr(m,"PI_MODEL_3")
    assert hasattr(m,"PI_MODEL_LTIE_2")
    assert hasattr(m,"PI_MODEL_ZERO")
    assert hasattr(m,"PI_MODEL_H3")
    assert hasattr(m,"PI_MODEL_ZERO_PLUS_2")
    assert hasattr(m,"PI_MODEL_WIN")
    assert hasattr(m,"PI_MODEL_PRIME")
    assert hasattr(m,"PI_MODEL_PC_2")
    assert hasattr(m,"PI_MODEL_ZERO_PLUS")
    assert hasattr(m,"PI_MODEL_ZERO_2")
    assert hasattr(m,"PI_MODEL_ZERO_2_W")
    assert hasattr(m,"PI_MODEL_ZERO_3_PLUS")
    assert hasattr(m,"PI_MODEL_800")
    assert hasattr(m,"PI_MODEL_4")
    assert hasattr(m,"PI_MODEL_4_LTS")
    assert hasattr(m,"PI_MODEL_RK3399")
    assert hasattr(m,"PI_MODEL_R1_PLUS")
    assert hasattr(m,"PI_MODEL_900")
    assert hasattr(m,"PI_MODEL_5")
    assert hasattr(m,"PI_MODEL_5_B")
    assert hasattr(m,"PI_MODEL_5_PRO")
    assert hasattr(m,"PI_MODEL_5_MAX")
    assert hasattr(m,"PI_MODEL_5_PLUS")
    assert hasattr(m,"PI_MODEL_CM5")
    assert hasattr(m,"PI_MODEL_CM5_TABLET")
    assert hasattr(m,"PI_MODEL_5_ULTRA")
    assert hasattr(m,"PI_MODEL_AI_MAX")
    assert hasattr(m,"PI_MODEL_CM4")
    assert hasattr(m,"PI_MODEL_3_B")
    assert hasattr(m,"PI_MODEL_3_PLUS")
    assert hasattr(m,"PI_MODEL_AI_PRO")
    assert hasattr(m,"PI_MODEL_KUNPENG_PRO")
    assert hasattr(m,"PI_MODEL_AI_STATION")
    assert hasattr(m,"PI_MODEL_RV")
    assert hasattr(m,"PI_MODEL_4_A")
    assert hasattr(m,"PI_MODEL_RV2")
    assert hasattr(m,"PI_MODEL_4_PRO")
    assert hasattr(m,"PI_MODEL_ZERO_3_W")
    assert hasattr(m,"PI_MODEL_ZERO_4")
    assert hasattr(m,"WPI_FATAL")
    assert hasattr(m,"WPI_ALMOST")
