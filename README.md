# Simulink Overview

Simulink, developed by MathWorks, is a graphical programming environment for modeling, simulating and analyzing multi-domain dynamical systems. Bonsai is using Simulink as a training environment for a Bonsai BRAIN. We’re supporting a wide range of use cases that can be described as control or machine tuning problems. Please review our simulator and sim model requirements guide at <URL>.

# Setup Your Project

# Virtual Environments (optional)

If you want to use a virtual environment like virtualenv, you need to validate that Matlab is using the same python version  that is active in your virutal environment.

    which python

Open Matlab

    pyversion = '<PATH OF ACTIVE PYTHON IN YOUR ENVIRONMENT>'

# Clone the Project

```
# Download directly or git clone
git clone https://github.com/BonsaiAI/bonsai-simulink
```

Clone the simulation project with `git clone`. You can also download a .zip of the files directly from GitHub. For this guide we'll be walking you through the Househeat Simulink demo, one of the supported Bonsai simulation models.

# Install the Bonsai CLI and SDK

If you haven't already, please follow the [Install the CLI][2] guide. This guide will walk you through any prerequisites you may need and then will link you back to this guide when you're done.

```
pip install bonsai-cli bonsai-ai bonsai-gym
```

# Install Prerequisites

# Install Asynchronous HTTP Client/Server
```
pip install aiohttp
```

#Install Matlab Engine:
```
cd <matlabroot>/extern/engines/python
python setup.py install
```

More info: https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html


# Create Your BRAIN

```
bonsai create simulink-househeat
```

Create your BRAIN (and its related project file) with [`bonsai create`][18] and give it a name. We used *simulink-househeat* in the example code but you can name it whatever you'd like. You will view your BRAIN's training progress on the BRAIN's Details page which can be found on the [BRAIN dashboard][5].

```
bonsai push
```

Use [`bonsai push`][19] to upload the cloned househeat project and its associated files to the Bonsai AI Engine for training.

# Train Your BRAIN

Almost there! Time to tell the Bonsai AI Engine to prepare a new BRAIN version for training.

Once you have started training it's time to start running your simulation by starting the coordinator. This will open up Matlab for you and start the simulation automatically; this might take a few minutes. Training on the server will begin automatically and if the simulator gets disconnected, training resumes from the same point when the simulator is reconnected if it's within a day of the disconnect. Please remember to always start training before running the coordinator.

```
bonsai train start
```

```
./coordinator.py --brain=simulink-househeat
```

# View your BRAIN training status

[Blurb about what to expect when the househeat demo is properly trained.]

# Stop Training

```
bonsai train stop
```

Once we've gotten to this level of performance (or sooner if you prefer), CTRL-C to disconnect the simulator, then [`bonsai train stop`][21] will end the training, and proceed to prediction.


# Predict with Your BRAIN

After your BRAIN is finished training it will be able to run through a simulation of househeat, choosing what to do when the temperature changes. How well it does depends on how long you let it train! Run the coordinator file again, but now in prediction mode with `--predict` which will use the version of the latest training session that you just ran. You can use a different version of your BRAIN if you have trained it multiple times by using `--predict=5` if you want the 5th trained version.

```
./coordinator.py --predict
```

## Using Simulink Coder for Parallel Simulations

Simulink Coder provides a mechanism to compile many Simulink models as a fast running C executable file for your operating system. There are three main benefits to training Bonsai BRAINs with these executables.

First is that Simulink Coder executables are return simulations results much faster than raw Simulink files. When training a BRAIN using Deep Reinforcement Learning, this difference in speed can add up. For example, if you train a BRAIN for 1M iterations with a Simulink Coder executable that runs in 0.5s per iteration instead of 1.5s per iteration, your total training time will decrease by 277 hours!

Second, Simulink Coder executables are much easier to connect to the Bonsai platform in parallel because they require a lot less memory and CPU than instances of interactive Simulink models. Continuing the example above, if you run 100 copies your new coder executable in parallel training you've now reduced the training time by an additional 250 hours.

Finally, Simulink Coder executable models can be easily shared with people and teams and used to train Bonsai BRAINS without a Matlab or Simulink license.

More information in Matlab and Simulink Coder: https://www.mathworks.com/products/simulink-coder.html

# How to connect your own model

Please review the HOWTO guide for additional information on how to connect your own Simulink model to the Bonsai AI platform.

[1]: getting-started.html#overview
[2]: cli-install-guide.html#install-prerequisites
[3]: ../references/cli-reference.html
[4]: https://gym.openai.com/envs/MountainCar-v0
[5]: https://beta.bons.ai
[16]: ../images/fully_trained_brain.png
[17]: ../references/cli-reference.html#bonsai-configure
[18]: ../references/cli-reference.html#bonsai-create
[19]: ../references/cli-reference.html#bonsai-push
[20]: ../references/cli-reference.html#bonsai-train-start
[21]: ../references/cli-reference.html#bonsai-train-stop
[22]: https://github.com/BonsaiAI
[23]: ../examples.html
