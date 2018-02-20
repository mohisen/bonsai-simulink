#!/usr/bin/env python3

import logging
import math

class Model:
    def load(self, eng):
        """
        Load the specified simulink model.
        """
        eng.eval("load_system('simulink_househeat')", nargout=0)

    def executable_name(self):
        """
        Returns the name of the executable (Simulink Coder Only).
        """
        return "./simulink_househeat"

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
            conf['outside_phase'] = 0.0
        return [ conf['outside_phase'], ]

    def convert_input(self, inlist):
        """
        Called with a list of inputs from the model,
        returns (state, reward, terminal).
        """

        # First map the ordered state list from the simulation into a
        # state dictionary for the brain.
        self.state = {
            'heat_cost':		inlist[0],
            'set_temp':			inlist[1],
            'room_temp':		inlist[2],
            'room_temp_change':		inlist[3],
            'outside_temp':		inlist[4],
            'outside_temp_change':	inlist[5],
        }

        tdiff = math.fabs(self.state['set_temp'] - self.state['room_temp'])

        # 1 degree ^ 0.4 = 1.0
        self.reward = 1.0 - pow(tdiff, 0.4)/1.32
        
        self.terminal = self.nsteps >= 240 or self.reward < 0.0

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
            outlist = [ act['heater_on'], ]

        return outlist

    def format_start(self):
        """
        Emit a formatted header and initial state line at the beginning
        of each episode.
        """
        logging.info(" itr h =>    cost  set   troom   droom tout dout = t    rwd")
        logging.info("          %7.1f %4.1f %7.1f %7.1f %4.1f %4.1f" % (
            self.state['heat_cost'],
            self.state['set_temp'],
            self.state['room_temp'],
            self.state['room_temp_change'],
            self.state['outside_temp'],
            self.state['outside_temp_change'],
        ))

    def format_step(self):
        """
        Emit a formatted line for each iteration.
        """
        if self.terminal:
            totrwdstr = " %6.3f" % self.total_reward
        else:
            totrwdstr = ""
            
        logging.info(" %3d %1.0f => %7.1f %4.1f %7.1f %7.1f %4.1f %4.1f = %i %6.3f%s" % (
            self.nsteps,
            self.action['heater_on'],
            self.state['heat_cost'],
            self.state['set_temp'],
            self.state['room_temp'],
            self.state['room_temp_change'],
            self.state['outside_temp'],
            self.state['outside_temp_change'],
            self.terminal,
            self.reward,
            totrwdstr,
        ))

