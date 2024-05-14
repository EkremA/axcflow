
                yosys -import
                
                # read design
                read_verilog "/home/user/eclectx/examples/pico_exact/picorv32.v"
                
                # generic synthesis
                synth -top picorv32
                
                # mapping to library
                dfflibmap -liberty lib=/home/user/tools/share/pdk/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib
                abc -liberty lib=/home/user/tools/share/pdk/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib
                clean
                
                # write synthesized design
                write_verilog "/home/user/eclectx/examples/pico_exact/picorv32_synth.v"
                
                # generate a json file for later plotting (e.g. netlistsvg)
                write_json "/home/user/eclectx/examples/pico_exactpicorv32_graph.json"
                exit