# Simulink Househeat Example

This is a step-by-step guide for training a Bonsai BRAIN using the Simulink Househeat model. You have to have Matlab and Simulink installed. Trial versions can be downloaded from [TheMathworks](http://www.themathworks.com]

## LOCAL (CLI) GUIDE

# Pre-requisites to run the example

Install Asynchronous HTTP Client/Server
    
    pip install aiohttp

We strongly recommend to create a virtual environment using [virtualenv] https://virtualenv.pypa.io/en/stable/installation/)

    pip install virtualenv
    virtualenv bonsai
    source bonsai/bin/activate
    

### CLI INSTALLATION


Install the Bonsai CLI by following our [detailed CLI installation guide](http://docs.bons.ai/guides/cli-guide.html).

    
    pip install bonsai-cli bonsai-ai
    
  
# Install Matlab Engine: 

    
    cd <matlabroot>/extern/engines/python
    python setup.py install
    

# Running and Training

Run the following in the simulink-househeat directory:

    bonsai create simulink-househeat
    bonsai push
    bonsai train start

    ../../coordinator/coordinator --brain=simulink-househeat

# Predictions

    ../../coordinator/coordinator --predict

# Files

* `README.md` - this file
* `bonsai_model.py` - model interface description
* `simulink_househeat.ink` - inkling file
* `simulink_househeat.slx` - Simulink model
* `preload.m` - used as a preload function in the Simulink model, to set up the Bonsai coordinator paths
