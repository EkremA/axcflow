# Flow Scripts

In this directory, you will find a collection of Python scripts that are responsible for handling and generating the necessary files for the flow.


- `generate_scripts.py` Methods containing templated tcl scripts for use with yosys-abc as well as OpenSTA.
- `setup.py` High level script to invoke `generation_scripts.py` with additional debug information. Can be called individually.
- `run.py` High level script to invoke the execution of the scripts generated by `generate_scripts.py` with additional debug information. Can be called individually.  
- `utils.py` Fancy colors and other utility is stored here.
