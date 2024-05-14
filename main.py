import os
import flow.setup as setup
import flow.run as run
from flow.utils import bcolors
import argparse
"""

"""


if __name__ == "__main__":
    print(bcolors.HEADER)
    print("""
                         ..                             ..                                
               .H88x.  :~)88:              oec :  x .d88"                x=~              
              x888888X ~:8888             @88888   5888R          u.    88x.   .e.   .e.  
      u      ~   "8888X  %88"       .     8"*88%   '888R    ...ue888b  '8888X.x888:.x888  
   us888u.        X8888        .udR88N    8b.       888R    888R Y888r  `8888  888X '888k 
.@88 "8888"    .xxX8888xxxd>  <888'888k  u888888>   888R    888R I888>   X888  888X  888X 
9888  9888    :88888888888"   9888 'Y"    8888R     888R    888R I888>   X888  888X  888X 
9888  9888    ~   '8888       9888        8888P     888R    888R I888>   X888  888X  888X 
9888  9888   xx.  X8888:    . 9888        *888>     888R   u8888cJ888   .X888  888X. 888~ 
9888  9888  X888  X88888x.x"  ?8888u../   4888     .888B .  "*888*P"    `%88%``"*888Y"    
"888*""888" X88% : '%8888"     "8888P'    '888     ^*888%     'Y"         `~     `"       
 ^Y"   ^Y'   "*=~    `""         "P'       88R       "%                                   
                                           88>                                            
                                           48                                             
                                           '8                                             
""")
    print("")
    print("Welcome to the axcflow!")
    print("Ekrem Altuntop, 2024")
    print(bcolors.ENDC)

    workdir = os.getcwd()
    parser = argparse.ArgumentParser(description="Generate tcl scripts for synthesis (typically yosys-abc) and reports (typically OpenSTA) and run them in order.")
    parser.add_argument("top", help="Full file path to RTL code of topmodule to be synthesized. Must be of form /path/to/<topmodule>.v")
    parser.add_argument("lib", nargs='?', default="{}/libs/freepdk-45nm/stdcells.lib".format(workdir), help="Standard cell library in .lib format (typical corner case)")
    parser.add_argument("libwc", nargs='?', default="{}/libs/freepdk-45nm/stdcells-wc.lib".format(workdir), help="For STA: worst case corner cell library in .lib format")
    parser.add_argument("libbc", nargs='?', default="{}/libs/freepdk-45nm/stdcells-bc.lib".format(workdir), help="For STA: best case corner cell library in .lib format")
    parser.add_argument("--stdout", action="store_true", default=False, help="Flag to print stdout and stderr (debug and also STA reports) to terminal instead of respective log files")
    parser.add_argument("--nodebug", action="store_true", default=False, help="Flag to comment out any $write or $display statements in the *_synth.v file")
    args = parser.parse_args()
    topfile = args.top
    topname = os.path.basename(topfile).split('/')[-1].split('.')[0]

    try:
        print("######################## Generate .tcl scripts #########################")
        setup.setup_tcls(topfile, args.lib, args.libwc, args.libbc)
        print("########################   Run .tcl scripts    ##########################")
        run.run_tcls(topfile.strip(".v").strip(topname), use_stdout=args.stdout, no_debug=args.nodebug)
        if args.stdout:
            print(bcolors.OKGREEN + "[SUCCESS] Flow completed successfully! Check terminal output for details." + bcolors.ENDC)
        else:
            print(bcolors.OKGREEN + "[SUCCESS] Flow completed successfully! Check the logs in the source directory for more information." + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + "[ERROR] Flow failed to complete with error:", e, bcolors.ENDC)
        exit(1)
