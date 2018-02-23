# How to connect an existing Simulink model to the Bonsai Brain

## Introduction

This how-to describes steps needed to connect your own Simulink model to the Bonsai platform. It follows the same approach we took for the other examples.

## Step by Step Guide

Create a new directory in the examples subdirectory. Copy your own Simulink slx file into this directory.

Copy the preload.m file from one of the other examples into your new directory. In your Simulink model File -> Model Properties, Callbacks, PreLoadFcn enter 'preload' in the text box.

Identify the control element in the Simulink model.  This element should take state variables as inputs and have one or more output
"actions". Look up what we did in the examples and review the associated Inkling code.

## Bonsai Block integration

Replace the control element with a bonsai_block:
1. Remove the existing control element.
2. From the Simulink Library Browser -> Simulink -> User-Defined Functions insert a "Level-2 MATLAB S-Function"
3. When prompted for the S-Function name type "bonsai_block".
4. In the bonsai_block's "Arguments" field type the <number-of-inputs>,<number-of-outputs>. For example, if your model needs a control element with 6 inputs and one output, type "6,1" in the Arguments field.

## Additional Block Parameters

Use a mux to connect your input values to the input port and use a demux to connect the output port signals to your model.

## Bonsai Config

The bonsai_config block connects configuration values from the brain to your model.  If no configuration is desired a "dummy" config value is commonly used.

Insert a bonsai_config block in your model:
1. From the Simulink Library Browser -> Simulink -> User-Defined Functions insert a "Level-2 MATLAB S-Function"
2. When prompted for the S-Function name type "bonsai_config".
3. In the bonsai_config "Arguments" field type the <number-of-config>.  For example, if your model needs 2 config values type "2" in the Arguments field.

SPECIAL NOTE: If you are using a dummy config value you should connect it to an input on the bonsai_block. This ensures that the bonsai_config block is correctly evaluated before the bonsai_block.

## Deconstruct your problem

## State, actions, terminal and reward

Construct an inkling file for your model.
- Inkling guide at http://docs.bons.ai/guides/inkling-guide.html
- Bonsai training videos at https://www.youtube.com/watch?v=VcwzDqReLPk&list=PLAktfMEMCsOY9HUZKIuGI6yqefGBuszAV

## Finalizing your model

Copy the bonsai_model.py file from one of the existing examples into your directory and update to reflect your model.

## Create a Bonsai Brain and start training using your model

Create a brain for your model:

    bonsai create your-model
    bonsai push
    bonsai train start

    ../../coordinator/coordinator --brain=your-model
