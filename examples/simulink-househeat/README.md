# Simulink Househeat Example

This is a step-by-step guide for using Bonsai's Universal Coordinator in Python to connect the Bonsai Platform to a Simulink model.

You have to have Matlab and Simulink installed. Trial versions can be downloaded from [TheMathworks](http://www.themathworks.com)

## LOCAL (CLI) GUIDE

We're using the Bonsai Command Line Interface (CLI) for this example. You can always verify training progress on the web at
http://beta.bons.ai

## Pre-requisites to run the example

We strongly recommend to create a virtual environment using [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

    pip install virtualenv
    virtualenv bonsai
    source bonsai/bin/activate

Install Asynchronous HTTP Client/Server

    pip install aiohttp

Install the Bonsai CLI and read our [detailed CLI installation guide](http://docs.bons.ai/guides/cli-guide.html).

    pip install bonsai-cli bonsai-ai


## Install Matlab Engine:

    cd <matlabroot>/extern/engines/python
    python setup.py install


## Running and Training

Run the following in the simulink-househeat directory:

    bonsai create simulink-househeat
    bonsai push
    bonsai train start

    ../../coordinator/coordinator --brain=simulink-househeat

When you are seeing rewards close to X you can stop training. You may need to Ctrl+C to stop in the terminal.

    bonsai train stop    

## Predicting with a BRAIN

Now you can predict using the trained BRAIN.

    ../../coordinator/coordinator --predict

## Files

* `README.md` - This file
* `bonsai_model.py` - Model interface description
* `simulink_househeat.ink` - Inkling file
* `simulink_househeat.slx` - Simulink model
* `sldemo_househeat_data.m` - Simulink model data
* `preload.m` - used as a preload function in the Simulink model, to
  set up the Bonsai coordinator paths
