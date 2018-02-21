#!/usr/bin/env python3

import logging
import math

_STEPLIMIT = 500

class Model:
    def load(self, eng):
        """
        Load the specified simulink model.
        """
        eng.eval("load_system('rolling_mill')", nargout=0)

    def executable_name(self):
        """
        Returns the name of the executable (Simulink Coder Only).
        """
        return "./rolling_mill"

    def episode_init(self):
        """
        This method is called at the beginning of each episode.
        """
        self.nsteps = 0
        self.action = None
        self.state = None
        self.reward = None
        self.terminal = None
        self.total_reward = 0.0

    def episode_step(self):
        """
        This method is called at the beginning of each iteration.
        """
        self.nsteps += 1
        
    def convert_config(self, conf):
        """
        Convert the dictionary of config from the brain into an ordered
        list of config for the simulation.
        """
        if len(conf) == 0:
            # In prediction mode the brain doesn't supply config.
            conf['dummy'] = -1.0
        return [ conf['dummy'], ]

    def convert_input(self, inlist):
        """
        Called with a list of inputs from the model,
        returns (state, reward, terminal).
        """

        # First map the ordered state list from the simulation into a
        # state dictionary for the brain.
        self.state = {
            'f_x':		inlist[0],
            'f_y':		inlist[1],
            'delta_x':		inlist[2],
            'delta_y':		inlist[3],
        }

        self.reward = 1.0 - pow(abs(self.state['delta_x']) + abs(self.state['delta_y']), 0.4)/0.4

        self.terminal = self.reward < 0.0 or self.nsteps >= _STEPLIMIT

        if self.nsteps > 0:
            self.total_reward += self.reward

        return self.state, self.reward, self.terminal

    def convert_output(self, act):
        """
        Called with a dictionary of actions from the brain, returns an
        ordered list of outputs for the simulation model.
        """
        outlist = []
        if act is not None:
            self.action = act
            outlist = [
                act['u_x'],
                act['u_y'],
            ]

        return outlist

    def format_start(self):
        """
        Emit a formatted header and initial state line at the beginning
        of each episode.
        """
        logging.info("  itr   u_x   u_y =>         f_x         f_y        dx      dy = t    rwd")
        logging.info("                     %11.1f %11.1f   %7.3f %7.3f" % (
            self.state['f_x'],
            self.state['f_y'],
            self.state['delta_x'],
            self.state['delta_y'],
        ))

    def format_step(self):
        """
        Emit a formatted line for each iteration.
        """
        if self.terminal:
            totrwdstr = " %6.3f" % self.total_reward
        else:
            totrwdstr = ""
            
        logging.info(" %4d %5.1f %5.1f => %11.1f %11.1f   %7.3f %7.3f = %i %6.3f%s" % (
            self.nsteps,
            self.action['u_x'],
            self.action['u_y'],
            self.state['f_x'],
            self.state['f_y'],
            self.state['delta_x'],
            self.state['delta_y'],
            self.terminal,
            self.reward,
            totrwdstr,
        ))

