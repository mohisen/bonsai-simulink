
# Running

Run the following in the current directory:

    bonsai create simulink-cartpole
    bonsai push
    bonsai train start

    ../../coordinator/coordinator --brain=simulink-cartpole

# Files

* `README.md` - this file
* `bonsai_model.py` - model interface description
* `simulink_cartpole.ink` - inkling file
* `simulink_cartpole.slx` - Simulink model
* `preload.m` - used as a preload function in the Simulink model, to set up the Bonsai coordinator paths
