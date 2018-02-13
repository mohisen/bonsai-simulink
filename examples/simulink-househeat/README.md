
# Running

Run the following in the current directory:

    bonsai create simulink-househeat
    bonsai push
    bonsai train start

    ../../coordinator/coordinator --brain=simulink-househeat

# Files

* `README.md` - this file
* `bonsai_model.py` - model interface description
* `simulink_househeat.ink` - inkling file
* `simulink_househeat.slx` - Simulink model
* `preload.m` - used as a preload function in the Simulink model, to set up the Bonsai coordinator paths
