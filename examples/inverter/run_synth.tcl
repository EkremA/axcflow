
set NANGATE45_STD_LIB "/home/user/eclectx/freepdk-45nm/stdcells.lib"

yosys -import

# read design
read_verilog inverter.v

# generic synthesis
synth -top inverter

# mapping to mycells.lib
dfflibmap -liberty  $NANGATE45_STD_LIB
abc -liberty $NANGATE45_STD_LIB
clean

# write synthesized design
write_verilog synth_inverter.v
exit
