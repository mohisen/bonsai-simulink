# Simulink Overview

Simulink, developed by The MathWorks, is a graphical programming environment for modeling, simulating and analyzing multi-domain dynamical systems. Bonsai is using Simulink as a training environment for a Bonsai BRAIN. We’re supporting a wide range of use cases that can be described as control or machine tuning problems. Please review our simulator and sim model requirements guide at <URL>.

## Simulink Bonsai Examples

### Cartpole

The model is based on an inverted pendulum attached to a cart. The objective is to move the cart in a way that stabilizes the pendulum.

Original model URL: (https://www.mathworks.com/help/control/examples/control-of-an-inverted-pendulum-on-a-cart.html)

### Househeat

This example shows how to use Simulink to create the thermal model of a house. This system models the outdoor environment, the thermal characteristics of the house, and the house heating system. Objective for the Bonsai AI is to reach the desired temperature.

Original model URL: (https://www.mathworks.com/help/simulink/examples/thermal-model-of-a-house.html)

Both examples are located in the examples folder including detailed step-by-step instructions.

## Prerequisites

- Bonsai CLI and SDK
- Python3
- Asynchronous HTTP Client/Server
- MATLAB Engine API for Python
- Matlab & Simulink


```
# Download directly or git clone
git clone https://github.com/BonsaiAI/bonsai-simulink
```
## Clone the Project

Clone the simulation project with `git clone`. You can also download a .zip of the files directly from GitHub. For this guide we'll be walking you through the Househeat Simulink demo, one of the supported Bonsai simulation models.


## Using Simulink Coder for Parallel Simulations

Simulink Coder provides a mechanism to compile many Simulink models as a fast running C executable file for your operating system. There are three main benefits to training Bonsai BRAINs with these executables.
First is that Simulink Coder executables are return simulations results much faster than raw Simulink files. When training a BRAIN using Deep Reinforcement Learning, this difference in speed can add up. For example, if you train a BRAIN for 1M iterations with a Simulink Coder executable that runs in 0.5s per iteration instead of 1.5s per iteration, your total training time will decrease by 277 hours!
Second, Simulink Coder executables are much easier to connect to the Bonsai platform in parallel because they require a lot less memory and CPU than instances of interactive Simulink models. Continuing the example above, if you run 100 copies your new coder executable in parallel training you've now reduced the training time by an additional 250 hours.
Finally, Simulink Coder executable models can be easily shared with people and teams and used to train Bonsai BRAINS without a Matlab or Simulink license.

More information in Matlab and Simulink Coder: https://www.mathworks.com/products/simulink-coder.html

## How to connect your own model

Please review the HOWTO file for additional information on how to connect your own Simulink model to the Bonsai AI platform.

## Virtual Environments (optional)

If you want to use a virtual environment like virtualenv, you need to validate that Matlab is using the same python version that is active in your virutal environment.

    which python

Open Matlab

    pyversion = '<PATH OF ACTIVE PYTHON IN YOUR ENVIRONMENT>'
