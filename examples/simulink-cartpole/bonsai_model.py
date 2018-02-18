#!/usr/bin/env python3

import logging
import math

_STEPLIMIT = 1000

class Model:
    def load(self, eng):
        """
        Load the specified simulink model
        """
        eng.eval("load_system('simulink_cartpole')", nargout=0)

    def executable_name(self):
        """
        Returns the name of the executable (Simulink Coder Only)
        """
        return "./simulink_cartpole"

    def episode_init(self):
        self.nsteps = 0
        self.action = None
        self.state = None
        self.reward = None
        self.terminal = None
        self.total_reward = 0.0

    def episode_step(self):
        self.nsteps += 1
        
    def convert_config(self, conf):
        """
        Called with a dictionary of config from ther brain
        convert to a list of config constants for the simulation.
        """
        if len(conf) == 0:
            # In prediction mode the brain doesn't supply config.
            conf['dummy'] = -1.0
        return [ conf['dummy'], ]

    def convert_input(self, inlist):
        """
        Called with a list of inputs from the model,
        returns (state, reward, terminal)
        """

        # First map the state list into a state dictionary.
        self.state = {
            'x':		inlist[0],
            'dx':		inlist[1],
            'theta':		inlist[2],
            'dtheta':		inlist[3],
        }

        self.terminal = abs(self.state["theta"]) > 0.261799 or self.nsteps >= _STEPLIMIT

        if self.terminal:
            self.reward = 0.0
        else:
            self.reward = 1.0

        
        if self.nsteps > 0:
            self.total_reward += self.reward

        return self.state, self.reward, self.terminal

    def convert_output(self, act):
        """
        Called with a dictionary of actions, returns an ordered
        list of outputs for the model.
        """
        outlist = []
        if act is not None:
            self.action = act
            outlist = [ act['f'], ]

        return outlist

    def format_start(self):
        logging.info("  itr     f =>       x      dx     theta  dtheta = t    rwd")
        logging.info("               %7.3f %7.3f   %7.3f %7.3f" % (
            self.state['x'],
            self.state['dx'],
            self.state['theta'],
            self.state['dtheta'],
        ))

    def format_step(self):
        if self.terminal:
            totrwdstr = " %6.3f" % self.total_reward
        else:
            totrwdstr = ""
            
        logging.info(" %4d %5.1f => %7.3f %7.3f   %7.3f %7.3f = %i %6.3f%s" % (
            self.nsteps,
            self.action['f'],
            self.state['x'],
            self.state['dx'],
            self.state['theta'],
            self.state['dtheta'],
            self.terminal,
            self.reward,
            totrwdstr,
        ))

