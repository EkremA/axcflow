import sys
import argparse
import os
from flow.utils import bcolors
from flow.generate_scripts import generate_synthesis_script, generate_sta_script

def setup_tcls(topfile, libfile_typ, libfile_wc, libfile_bc):
    topname = os.path.basename(topfile).split('/')[-1].split('.')[0]
    topfile_synthed = topfile.replace(".v", "_synth.v")


    # Generate synthesis script
    print("Generating synthesis script:", "\n----------------------------------------\nModule: ", topname, "\n----------------------------------------\nLibrary: ", libfile_typ, "\n----------------------------------------")
    
    try:
        generate_synthesis_script(topfile, topname, libfile_typ)
        print(bcolors.OKGREEN + "Synthesis script generated successfully!" + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + "Synthesis script generation failed. Please check the following:", e, bcolors.ENDC)
    

    # Generate STA script
    print("Generating STA script:", "\n----------------------------------------\nModule: ", topname, "\n----------------------------------------\nCorners:" , 
          "\nTYPICAL: ", libfile_typ, 
          "\nWORST: ", libfile_wc, 
          "\nBEST: ", libfile_bc,
          "\n----------------------------------------")
    try:
        generate_sta_script(topfile_synthed, topname, libfile_typ, libfile_wc, libfile_bc)
        print(bcolors.OKGREEN + "STA script generated successfully!" + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + "STA script generation failed. Please check the following:", e, bcolors.ENDC)

if __name__ == "__main__":
    print(bcolors.WARNING + "Recommended usage: python runall.py /full/path/to/<topmodule>.v <std_cell_lib_typ> <std_cell_lib_wc> <std_cell_lib_bc> [--stdout]" + bcolors.ENDC)
    work_dir = os.getcwd()
    parser = argparse.ArgumentParser(description="Generate tcl scripts for synthesis (typically yosys-abc) and reports (typically OpenSTA)")
    parser.add_argument("top", help="Full file path to RTL code of topmodule to be synthesized. Must be of form /path/to/<topmodule>.v")
    parser.add_argument("lib", nargs='?', default="{}/libs/freepdk-45nm/stdcells.lib".format(work_dir), help="Standard cell library in .lib format (typical corner case)")
    parser.add_argument("libwc", nargs='?', default="{}/libs/freepdk-45nm/stdcells-wc.lib".format(work_dir), help="For STA: worst case corner cell library in .lib format")
    parser.add_argument("libbc", nargs='?', default="{}/libs/freepdk-45nm/stdcells-bc.lib".format(work_dir), help="For STA: best case corner cell library in .lib format")
    args = parser.parse_args()
    topfile = args.top
    libfile_typ = args.lib
    libfile_wc = args.libwc
    libfile_bc = args.libbc
    print("#################################################")
    setup_tcls(topfile, libfile_typ, libfile_wc, libfile_bc)
    print("#################################################")
