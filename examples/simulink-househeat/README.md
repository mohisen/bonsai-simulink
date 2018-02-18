# Simulink Househeat Sample

## LOCAL (CLI) GUIDE

### CLI INSTALLATION
1. We strongly recommend to create a virtual environment using virtualenv (https://virtualenv.pypa.io/en/stable/installation/)
2. Install the Bonsai CLI by following our [detailed CLI installation guide](http://docs.bons.ai/guides/cli-guide.html).

    ```
    pip install bonsai-cli bonsai-ai
    ```

# Install pre-requisites

Install Asynchronous HTTP Client/Server
    ```
    pip install aiohttp
    ```
#Install Matlab Engine: 

    ```
    cd <matlabroot>/extern/engines/python
    python setup.py install
    ```

# Running

Run the following in the simulink-househeat directory:

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
