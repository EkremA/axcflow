
                define_corners wc typ bc
                read_liberty -corner wc "/home/user/eclectx/libs/freepdk-45nm/stdcells-wc.lib"
                read_liberty -corner typ "lib=/home/user/tools/share/pdk/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib"
                read_liberty -corner bc "/home/user/eclectx/libs/freepdk-45nm/stdcells-bc.lib"

                read_verilog "/home/user/eclectx/examples/pico_exact/picorv32_synth.v"
                link_design "picorv32"
                
                set_timing_derate -early 0.9
                set_timing_derate -late 1.1
                create_clock -name clk -period 10 [get_ports clk]
                set_input_delay -clock clk 0 [all_inputs]
                
                report_checks -path_delay min_max
                report_checks -corner typ
                
                set_power_activity -input -activity 0.1
                report_power -corner typ
                exit
                