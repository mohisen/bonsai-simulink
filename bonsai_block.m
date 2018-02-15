function bonsai_block(block)
%%
%% The setup method is used to set up the basic attributes of the
%% S-function such as ports, parameters, etc. Do not add any other
%% calls to the main body of the function.
%%
setup(block);

%endfunction

%% Function: setup ===================================================
%% Abstract:
%%   Set up the basic characteristics of the S-function block such as:
%%   - Input ports
%%   - Output ports
%%   - Dialog parameters
%%   - Options
%%
%%   Required         : Yes
%%   C-Mex counterpart: mdlInitializeSizes
%%
function setup(block)

% Register parameters
block.NumDialogPrms     = 2;
block.DialogPrmsTunable = {'Nontunable', 'Nontunable'};

% Register number of ports
block.NumInputPorts  = 1;
block.NumOutputPorts = 1;

% Setup port properties to be inherited or dynamic
block.SetPreCompInpPortInfoToDynamic;
block.SetPreCompOutPortInfoToDynamic;

% Override input port properties
  block.InputPort(1).Dimensions = block.DialogPrm(1).Data;
  block.InputPort(1).DatatypeID = 0;  % double
  block.InputPort(1).Complexity = 'Real';
  block.InputPort(1).DirectFeedthrough = true;

% Override output port properties
  block.OutputPort(1).Dimensions = block.DialogPrm(2).Data;
  block.OutputPort(1).DatatypeID = 0;  % double
  block.OutputPort(1).Complexity = 'Real';

% Register sample times
%  [0 offset]            : Continuous sample time
%  [positive_num offset] : Discrete sample time
%
%  [-1, 0]               : Inherited sample time
%  [-2, 0]               : Variable sample time
block.SampleTimes = [-1, 0];

% Specify the block simStateCompliance. The allowed values are:
%    'UnknownSimState', < The default setting; warn and assume DefaultSimState
%    'DefaultSimState', < Same sim state as a built-in block
%    'HasNoSimState',   < No sim state
%    'CustomSimState',  < Has GetSimState and SetSimState methods
%    'DisallowSimState' < Error out when saving or restoring the model sim state
block.SimStateCompliance = 'DefaultSimState';

%% -----------------------------------------------------------------
%% The MATLAB S-function uses an internal registry for all
%% block methods. You should register all relevant methods
%% (optional and required) as illustrated below. You may choose
%% any suitable name for the methods and implement these methods
%% as local functions within the same file. See comments
%% provided for each function for more information.
%% -----------------------------------------------------------------

block.RegBlockMethod('ProcessParameters',       @ProcessPrms);
block.RegBlockMethod('PostPropagationSetup',    @DoPostPropSetup);
block.RegBlockMethod('InitializeConditions', @InitializeConditions);
block.RegBlockMethod('Start', @Start);
block.RegBlockMethod('Outputs', @Outputs);     % Required
block.RegBlockMethod('Update', @Update);
block.RegBlockMethod('Derivatives', @Derivatives);
block.RegBlockMethod('Terminate', @Terminate); % Required

block.RegBlockMethod('SetInputPortSamplingMode',@SetInputPortSamplingMode);

%end setup

%%
%% PostPropagationSetup:
%%   Functionality    : Setup work areas and state variables. Can
%%                      also register run-time methods here
%%   Required         : No
%%   C-Mex counterpart: mdlSetWorkWidths
%%
function DoPostPropSetup(block)

%end DoPostPropSetup

%%
%% InitializeConditions:
%%   Functionality    : Called at the start of simulation and if it is 
%%                      present in an enabled subsystem configured to reset 
%%                      states, it will be called when the enabled subsystem
%%                      restarts execution to reset the states.
%%   Required         : No
%%   C-MEX counterpart: mdlInitializeConditions
%%
function InitializeConditions(block)

global EPISODE_DONE
EPISODE_DONE = 0;

%end InitializeConditions

function ProcessPrms(block)

  block.AutoUpdateRuntimePrms;
 
%end ProcessPrms

%%
%% Start:
%%   Functionality    : Called once at start of model execution. If you
%%                      have states that should be initialized once, this 
%%                      is the place to do it.
%%   Required         : No
%%   C-MEX counterpart: mdlStart
%%
function Start(block)

%end Start

%%
%% Outputs:
%%   Functionality    : Called to generate block outputs in
%%                      simulation step
%%   Required         : Yes
%%   C-MEX counterpart: mdlOutputs
%%
function Outputs(block)

global BONSAI_COORDINATOR_PORT
global EPISODE_DONE

%% Once the episode is done we should not generate any more output.
if EPISODE_DONE == 1
     return;
end
                                               
state = py.list({});
for ndx = 1:block.InputPort(1).Dimensions
    append(state, block.InputPort(1).Data(ndx))
end

action = py.bonsai_block.step(BONSAI_COORDINATOR_PORT, state);

%% If the action is an empty list the simulation is being stopped.
n = size(action, 2);
if n == 0
    EPISODE_DONE = 1;
    set_param(bdroot, 'SimulationCommand', 'pause')
    return;
end

for ndx = 1:block.OutputPort(1).Dimensions
    block.OutputPort(1).Data(ndx) = action{ndx};
end

%end Outputs

%%
%% Update:
%%   Functionality    : Called to update discrete states
%%                      during simulation step
%%   Required         : No
%%   C-MEX counterpart: mdlUpdate
%%
function Update(block)

%end Update

%%
%% Derivatives:
%%   Functionality    : Called to update derivatives of
%%                      continuous states during simulation step
%%   Required         : No
%%   C-MEX counterpart: mdlDerivatives
%%
function Derivatives(block)

%end Derivatives

%%
%% Terminate:
%%   Functionality    : Called at the end of simulation for cleanup
%%   Required         : Yes
%%   C-MEX counterpart: mdlTerminate
%%
function Terminate(block)

%end Terminate

function SetInputPortSamplingMode(block, idx, fd)
block.InputPort(idx).SamplingMode = fd;
for ndx = 1:block.NumOutputPorts
    block.OutputPort(ndx).SamplingMode = fd;
end 
