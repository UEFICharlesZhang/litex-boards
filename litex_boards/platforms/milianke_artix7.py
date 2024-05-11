#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2018-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import Xilinx7SeriesPlatform, VivadoProgrammer
from litex.build.openocd import OpenOCD

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk50", 0, Pins("V4"), IOStandard("SSTL135")),
    ("cpu_reset", 0, Pins("R14"), IOStandard("LVCMOS33")), # KEY1

    # Leds
    ("user_led",  0, Pins("E21"), IOStandard("LVCMOS33")),
    ("user_led",  1, Pins("D21"), IOStandard("LVCMOS33")),
    ("user_led",  2, Pins("E22"), IOStandard("LVCMOS33")),
    ("user_led",  3, Pins("D22"), IOStandard("LVCMOS33")),

    # Buttons
    # ("user_btn", 0, Pins("R14"), IOStandard("LVCMOS33")), #KEY1
    ("user_btn", 1, Pins("P14"), IOStandard("LVCMOS33")),#KEY2
    ("user_btn", 2, Pins("N14"), IOStandard("LVCMOS33")),#KEY3
    ("user_btn", 3, Pins("N13"), IOStandard("LVCMOS33")),#KEY4
    # ("user_btn", 4, Pins("M18"), IOStandard("LVCMOS33")),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("R17")),
        Subsignal("rx", Pins("P16")),
        IOStandard("LVCMOS33"),
    ),

    # SPIFlash
    ("spiflash", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("mosi", Pins("P22")),
        Subsignal("miso", Pins("R22")),
        Subsignal("vvp",  Pins("P21")),
        Subsignal("hold", Pins("R21")),
        IOStandard("LVCMOS33")
    ),
    ("spiflash4x", 0,  # clock needs to be accessed through STARTUPE2
        Subsignal("cs_n", Pins("T19")),
        Subsignal("dq",   Pins("P22", "R22", "P21", "R21")),
        IOStandard("LVCMOS33")
    ),
    # SDCard
    ("spisdcard", 0,
        Subsignal("clk",  Pins("W17")),
        Subsignal("mosi", Pins("AA19"), Misc("PULLUP True")),
        Subsignal("cs_n", Pins("AB12"), Misc("PULLUP True")),
        Subsignal("miso", Pins("V17"), Misc("PULLUP True")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS33"),
    ),
    ("sdcard", 0,
        Subsignal("data", Pins("V17 AB18 Y19 AB12"), Misc("PULLUP True")),
        Subsignal("cmd",  Pins("AA19"),              Misc("PULLUP True")),
        Subsignal("clk",  Pins("W17")),
        Subsignal("cd",   Pins("AA18")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS33"),
    ),

    # DDR3 SDRAM
    # MT41K128M16JT-125K
    ("ddram", 0,
        Subsignal("a", Pins("AB3 AA6 Y3 Y2 AB6 AA3 Y7 AA4",
                            "AA8 Y4 Y9 AB7 AA5 W5 AB8"),
            IOStandard("SSTL135")),
        Subsignal("ba",    Pins("AB2 AB5 W2"), IOStandard("SSTL135")),
        Subsignal("ras_n", Pins("V2"), IOStandard("SSTL135")),
        Subsignal("cas_n", Pins("AA1"), IOStandard("SSTL135")),
        Subsignal("we_n",  Pins("W1"), IOStandard("SSTL135")),
        # cs_n is hardwired on the board
        Subsignal("cs_n",  Pins("Y1"), IOStandard("SSTL135")),
        Subsignal("dm", Pins("P2 J6 D2 H2"), IOStandard("SSTL135")),
        Subsignal("dq", Pins(
            "P6 R1 M5 N4 N5 N2 M6 P1",
            "L3 J4 M3 K4 M2 K3 L4 L5",
            "B1 E2 B2 F3 A1 G1 C2 F1",
            "J5 H5 K1 G4 H4 G3 H3 G2"
            ),
            IOStandard("SSTL135"),
            Misc("IN_TERM=UNTUNED_SPLIT_40")),
        Subsignal("dqs_p", Pins("P5 M1 E1 K2"),
            IOStandard("DIFF_SSTL135"),
            Misc("IN_TERM=UNTUNED_SPLIT_40")),
        Subsignal("dqs_n", Pins("P4 L1 D1 J2"),
            IOStandard("DIFF_SSTL135"),
            Misc("IN_TERM=UNTUNED_SPLIT_40")),
        Subsignal("clk_p", Pins("T5"), IOStandard("DIFF_SSTL135")),
        Subsignal("clk_n", Pins("U5"), IOStandard("DIFF_SSTL135")),
        Subsignal("cke",   Pins("Y6"), IOStandard("SSTL135")),
        Subsignal("odt",   Pins("AB1"), IOStandard("SSTL135")),
        Subsignal("reset_n", Pins("W4"), IOStandard("SSTL135")),
        Misc("SLEW=FAST"),
    ),
    # RGMII Ethernet (RTL8211FD)
    ("eth_clocks", 0,
        Subsignal("tx", Pins("AB21")),
        Subsignal("rx", Pins("W19")),
        IOStandard("LVCMOS33")
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("U17")),
        Subsignal("mdio",    Pins("N17")),
        Subsignal("mdc",     Pins("U18")),
        Subsignal("rx_ctl",  Pins("V18")),
        Subsignal("rx_data", Pins("V19 W20 AA20 AA21")),
        Subsignal("tx_ctl",  Pins("AB22")),
        Subsignal("tx_data", Pins("W21 W22 Y21 Y22")),
        IOStandard("LVCMOS33")
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = []
# PMODS --------------------------------------------------------------------------------------------


# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk50"
    default_clk_period = 1e9/50e6

    def __init__(self, toolchain="vivado"):
        Xilinx7SeriesPlatform.__init__(self, "xc7a100t-2fgg484", _io, _connectors, toolchain=toolchain)
        self.add_platform_command("set_property INTERNAL_VREF 0.900 [get_iobanks 34]")
        self.toolchain.bitstream_commands = \
            ["set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]"]
        self.toolchain.additional_commands = \
            ["write_cfgmem -force -format mcs -interface spix4 -size 16 "
            "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.mcs"]
    def create_programmer(self):
        return VivadoProgrammer()

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk50",             loose=True), 1e9/50e6)
        self.add_period_constraint(self.lookup_request("eth_clocks:rx", 0, loose=True), 1e9/125e6)
        self.add_period_constraint(self.lookup_request("eth_clocks:rx", 1, loose=True), 1e9/125e6)
