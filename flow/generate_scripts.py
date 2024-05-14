import os

def generate_synthesis_script(topmodule_file, topmodule_name, std_cell_lib):
    # Generate synthesis script based on the command-line argument
    directory = topmodule_file.strip(".v").strip(topmodule_name)
    directory = os.path.dirname(topmodule_file)
    synth_tcl_name = "1_run_synth_yosys.tcl"
    synth_tcl_path = os.path.join(directory, synth_tcl_name)
    topmodule_synthed_path = os.path.join(directory, "{}{}".format(topmodule_name, "_synth.v"))
    with open(synth_tcl_path, "w") as f:
        f.write('''
                yosys -import
                
                # read design
                read_verilog "{topmodule_file}"
                
                # generic synthesis
                synth -top {topmodule_name}
                
                # mapping to library
                dfflibmap -liberty {std_cell_lib}
                abc -liberty {std_cell_lib}
                clean
                
                # write synthesized design
                write_verilog "{topmodule_synthed_path}"
                
                # generate a json file for later plotting (e.g. netlistsvg)
                write_json "{topmodule_dir}{topmodule_name}_graph.json"
                exit'''.format(topmodule_file=topmodule_file, topmodule_dir=directory, topmodule_name=topmodule_name, topmodule_synthed_path=topmodule_synthed_path, std_cell_lib=std_cell_lib))


def generate_sta_script(topmodule_file_synthed, topmodule_name, std_cell_lib_typ, std_cell_lib_wc, std_cell_lib_bc):
    # Generate STA script based on the command-line argument
    directory = topmodule_file_synthed.strip("_synth.v").strip(topmodule_name)
    directory = os.path.dirname(topmodule_file_synthed)
    sta_tcl_name = "2_run_sta_sta.tcl"
    sta_tcl_path = os.path.join(directory, sta_tcl_name)
    with open(sta_tcl_path, "w") as f:
        f.write('''
                define_corners wc typ bc
                read_liberty -corner wc "{std_cell_lib_wc}"
                read_liberty -corner typ "{std_cell_lib_typ}"
                read_liberty -corner bc "{std_cell_lib_bc}"

                read_verilog "{topmodule_file_synthed}"
                link_design "{topmodule_name}"
                
                set_timing_derate -early 0.9
                set_timing_derate -late 1.1
                create_clock -name clk -period 10 [get_ports clk]
                set_input_delay -clock clk 0 [all_inputs]
                
                report_checks -path_delay min_max
                report_checks -corner typ
                
                set_power_activity -input -activity 0.1
                report_power -corner typ
                exit
                '''.format(topmodule_file_synthed=topmodule_file_synthed, 
                           topmodule_name=topmodule_name, 
                           std_cell_lib_wc=std_cell_lib_wc, 
                           std_cell_lib_typ=std_cell_lib_typ, 
                           std_cell_lib_bc=std_cell_lib_bc))