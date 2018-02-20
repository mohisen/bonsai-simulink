How to connect an existing Simulink model to the Bonsai Brain
================================================================

Create a new directory in the examples subdirectory. Copy your
Simulink slx file into this directory.

Copy the preload.m file from one of the other examples into your new
directory.  In your Simulink model File -> Model Properties,
Callbacks, PreLoadFcn enter 'preload' in the text box.

Identify the control element in the Simulink model.  This element
should take state variables as inputs and have one or more output
"actions".

Replace the control element with a bonsai_block:
1. Remove the existing control element.
2. From the Simulink Library Browser -> Simulink -> User-Defined
   Functions insert a "Level-2 MATLAB S-Function"
3. When prompted for the S-Function name type "bonsai_block".
4. In the bonsai_block's "Arguments" field type the
   <number-of-inputs>,<number-of-outputs>.  For example, if your model
   needs a control element with 6 inputs and one output, type "6,1" in
   the Arguments field.

Use a mux to connect your input values to the input port.

Use a demux to connect the ouput port signals to your model.

The bonsai_config block connects configuration values from the brain
to your model.  If no configuration is desired a "dummy" config value
is commonly used.

Insert a bonsai_config block in your model:
1. From the Simulink Library Browser -> Simulink -> User-Defined
   Functions insert a "Level-2 MATLAB S-Function"
2. When prompted for the S-Function name type "bonsai_config".
3. In the bonsai_config "Arguments" field type the
   <number-of-config>.  For example, if your model
   needs 2 config values type "2" in the Arguments field.
   
SPECIAL NOTE: If you are using a dummy config value you should connect
it to an input on the bonsai_block.  This ensures that the
bonsai_config block is correctly evaluated before the bonsai_block.

Construct an inkling file for your model.

Copy the bonsai_model.py file from one of the existing examples into
your directory and update to refelct your model.
