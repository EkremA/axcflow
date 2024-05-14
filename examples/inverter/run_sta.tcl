set NANGATE45_WC_LIB "/home/user/eclectx/freepdk-45nm/stdcells-wc.lib"
set NANGATE45_TYP_LIB "/home/user/eclectx/freepdk-45nm/stdcells.lib"
set NANGATE45_BC_LIB  "/home/user/eclectx/freepdk-45nm/stdcells-bc.lib"

define_corners wc typ bc
read_liberty -corner wc $NANGATE45_WC_LIB
read_liberty -corner typ $NANGATE45_TYP_LIB
read_liberty -corner bc $NANGATE45_BC_LIB
read_verilog synth_inverter.v
link_design inverter
set_timing_derate -early 0.9
set_timing_derate -late 1.1
create_clock -name clk -period 10
set_input_delay -clock clk 0 {a}
report_checks -path_delay min_max
report_checks -corner typ
exit
