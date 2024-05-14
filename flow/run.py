import os
import sys
import argparse
import subprocess
from flow.utils import bcolors

def run_tcls(src_dir, use_stdout=False, no_debug=True):
    if no_debug:
        for file in os.listdir(src_dir):
            if file.endswith("_synth.v"):
                with open(os.path.join(src_dir, file), "r+") as f:
                    lines = f.readlines()
                    #if lines.count("$write") > 0 or lines.count("$display") > 0:
                    #    print(bcolors.WARNING + "[WARNING] Found $write or $display statements in {}_synth.v file. Commenting out...".format(file.strip("_synth.v")) + bcolors.ENDC)
                    for line in lines:
                        if "$write" in line or "$display" in line:
                            f.write("//" + line)
                        else:
                            f.write(line)

    flow_order = []
    for file in os.listdir(src_dir):
        if file.endswith(".tcl"):
            flow_order.append(file)
    flow_order.sort()

    for tclname in flow_order:
            prgrm = tclname.strip(".tcl").split("_")[-1] #designates the type of program to pass the tcl script to, example: 1_run_synth_yosys.tcl --> yosys
            try:
                work_dir = os.getcwd()
                os.chdir(src_dir)
                print("[INFO] Running: ", "{} {}".format(prgrm, tclname))
                if use_stdout:
                    calledprocesserror = subprocess.run([prgrm, tclname], check=True, stdout=sys.stdout, stderr=sys.stderr, text=True)
                with open("{}.log".format(tclname.strip(".tcl")), "w") as f:
                    calledprocesserror = subprocess.run([prgrm, tclname], check=True, capture_output=True, text=True)
                    f.write(calledprocesserror.stdout)
                os.chdir(work_dir)
                print(bcolors.OKGREEN + "[OK] Success: {} {}".format(prgrm, tclname) 
                      + " finished with returncode {}".format(calledprocesserror.returncode) 
                      + bcolors.ENDC)
            except subprocess.CalledProcessError:
                print(bcolors.FAIL + "[ERROR] Failed to run " + "{} {}".format(prgrm, tclname) + bcolors.ENDC)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run all tcl scripts in a given source directory")
    parser.add_argument("src_dir", help="Source directory containing tcl scripts and RTL code")
    parser.add_argument("--stdout", action="store_true", default=False, help="Flag to print stdout and stderr to terminal instead of log files")
    parser.add_argument("--nodebug", action="store_true", default=False, help="Flag to comment out any $write or $display statements in any *_synth.v files")
    args = parser.parse_args()
    src_dir = args.src_dir
    use_stdout = args.stdout
    no_debug = args.nodebug
    if len(sys.argv) < 2:
        print(bcolors.FAIL + "Please provide the source directory containing tcl scripts (python run.py <src_dir>)" + bcolors.ENDC)
        sys.exit(1)
    else:
        print(bcolors.WARNING + "Recommended usage: python runall.py /full/path/to/<topmodule>.v <std_cell_lib_typ> <std_cell_lib_wc> <std_cell_lib_bc> [--stdout] [--nodebug]" + bcolors.ENDC)
        run_tcls(src_dir, use_stdout, no_debug)