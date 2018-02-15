# Bonsai's Simulink Househeat Example

This is an example of using Bonsai's Universal Coordinator in Python to connect The Bonsai Platform to Simulink in MATLAB.

# Install Prerequisites

You may want to do the following steps within a virtual environment if you don't want to make changes to your current Python packages.

1. pip install aiohttp
2. Install the Python Matlab Engine by [following these instructions](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)

# Training a BRAIN

Run the following in the current directory:

    bonsai create simulink-househeat
    bonsai push
    bonsai train start

    ./coordinator.py --brain=simulink-househeat

When you are done (you may need to Ctrl+C to stop in the terminal):

    bonsai train stop

# Predicting with a BRAIN

Once you have hit sufficient training you can predict with the BRAIN you have finished training.

    ./coordinator.py --predict

# Model Specific Files

* `README.md` - This file
* `bonsai_model.py` - Model interface description
* `simulink_househeat.ink` - Inkling file
* `simulink_househeat.slx` - Simulink model
* `preload.m` - Used as a preload function in the Simulink model, to set up the Bonsai coordinator paths
