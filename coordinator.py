#!/usr/bin/env python3

import json
import logging
import os
import socket
import subprocess
import sys
import threading
import argparse

from aiohttp import web

# FIXME - not needed if using coder variation
import matlab.engine

from bonsai_ai import Simulator, Brain, Config

from datasync import DataSync

sys.path.append('.')

from bonsai_model import Model

_debug = False
_use_coder = True
_brainport = None
_model = Model()
_config = DataSync("config")
_action = DataSync("action")
_state = DataSync("state")

class SimulinkSimulation(Simulator):
    def __init__(self, brainObj, name):
        global _use_coder
        logging.debug("SimulinkSimulation.__init__ starting")
        Simulator.__init__(self, brainObj, name)
        self.episode_started = False
        self.sim_sent_term = False
        if not _use_coder:
            self._simulink_invoke()
        logging.debug("SimulinkSimulation.__init__ finished")

    def episode_start(self, parameters=None):
        global _model, _config, _action, _state
        global _use_coder
        
        if self.episode_started:
            # Were we terminated by the sim or the brain?
            if self.sim_sent_term:
                logging.debug("episode terminated by sim")
            else:
                logging.debug("episode terminated by brain")
                _action.stop()
                if _use_coder:
                    self.simulink.wait()
            
            # Generate an episode_stop since sdk2 doesn't do it.
            self.episode_stop()

        if _use_coder:
            self._simulink_execute()
            
        self.episode_started = True
        self.sim_sent_term = False

        _state.reset()
        _action.reset()
        
        logging.info("--------------------------------")
        logging.debug("episode_start")

        _model.episode_init()

        # Simulator will do a getconfig here, post the config
        _config.post(_model.convert_config(parameters))

        if not _use_coder:
            # This routine will not complete until the getconfig
            # has completed ...
            #
            self._simulink_start()
        
        params = _state.wait()
        
        state = params['state']
        # The terminal and reward are ignored on the initial state

        _model.format_start()
        
        return state
        
    def episode_stop(self):
        global _use_coder
        logging.debug("episode_stop starting")
        if not _use_coder:
            self._simulink_stop()
        self.episode_started = False
        logging.debug("episode_stop finished")
        
    def simulate(self, action):
        global _model, _config, _action, _state
        
        _model.episode_step()
        
        logging.debug("simulate starting action=%s" % (str(action),))

        _action.post(action)
        params = _state.wait()
        
        state = params['state']
        terminal = params['terminal']
        reward = params['reward']

        self.sim_sent_term = terminal
        
        _model.format_step()

        if _use_coder and terminal:
            # terminal is True, simulator will exit, wait for it
            self.simulink.wait()
        
        return state, reward, terminal

    def _simulink_invoke(self):
        """Invoke the standard (non-coder) version of simulink. (Non Simulink Coder)"""
        global _brainport
        global _model
        
        # FIXME - Hook this up to an sdk2 parsed variable
        if not True:
            opts = '-nodesktop -nosplash -minimize'
        else:
            opts = '-desktop'
            
        self.eng = matlab.engine.start_matlab(opts)
        self.eng.eval(
            "global BONSAI_COORDINATOR_PORT; BONSAI_COORDINATOR_PORT = %d;" % (
                _brainport,), nargout=0)

        _model.load(self.eng)

    def _simulink_execute(self):
        """Execute the Simulink Coder version of the simulation. (Simulink Coder)"""
        global _brainport
        global _model
        global _debug
        
        os.environ["BONSAI_COORDINATOR_PORT"] = str(_brainport)
        if _debug:
            os.environ["BONSAI_DEBUG"] = "1"
        self.simulink = subprocess.Popen([_model.executable_name(),])
            
    def _simulink_start(self):
        """Start the standard (non-coder) simulation. (Non Simulink Coder)"""
        self.eng.eval(
            "set_param(bdroot, 'SimulationCommand', 'start')", nargout=0)
        
    def _simulink_stop(self):
        """Start the standard (non-coder) simulation. (Non Simulink Coder)"""
        self.eng.eval(
            "set_param(bdroot, 'SimulationCommand', 'stop')", nargout=0)
        
async def _handle_request(request):
    global _model, _config, _action, _state
    global _use_coder
    
    body = await request.text()
    logging.debug("received request: " + body)
    req = json.loads(body)
    method = req['method']
    params = req['params']
    
    if method == 'getconfig':
        config = _config.wait()
        logging.debug("SIM: returning config")
        msg = {
            'jsonrpc': '2.0',
            'result': { 'config': config, },
            'id': req['id'],
        }
        data = json.dumps(msg)
        logging.debug("sending getconfig response: " + data)
        return web.Response(body=data.encode('utf8'))
        
    elif method == 'step':
        (state, reward, terminal,) = _model.convert_input(params['state'])
        _params = {
            'state': state,
            'reward': reward,
            'terminal': terminal,
        }
        _state.post(_params)
        
        if terminal:
            acts = []
        else:
            # Wait for an action from the brain.
            acts = _model.convert_output(_action.wait())

        # Send the action back to the simulator.
        msg = {
            'jsonrpc': '2.0',
            'result': { 'action': acts },
            'id': req['id'],
        }
        data = json.dumps(msg)
        logging.debug("sending response: " + data)

        return web.Response(body=data.encode('utf8'))
        
    else:
        logging.info("BAD METHOD: ", method)
        sys.exit(1)

def _run_bonsai(args):
    logging.debug("_run_bonsai starting")

    config = Config(args)
    logging.debug(config)

    brain = Brain(config)
    brain.update()

    sim = SimulinkSimulation(brain, "simulink_sim")
    logging.info('%s running' % brain.name)
    while sim.run():
        continue
        
    logging.info('%s finished' % brain.name)
    
if __name__ == "__main__":
    if _debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    logging.info("simulink_sim starting")
        
    # Allocate a socket and bind to an unused port.
    # NOTE - This needs to happen before we start the simulation
    # thread so we can pass the brainport value to the simulation.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    _brainport = sock.getsockname()[1]

    logging.debug("simulink_sim starting thread")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--coder', action='store_true')
    (opts, unknown_args) = parser.parse_known_args(sys.argv)
    _use_coder = opts.coder

    # Start a thread to initiate the simulation
    bonsai_thread = threading.Thread(target=_run_bonsai, args=(unknown_args,))
    bonsai_thread.daemon = True
    bonsai_thread.start()

    logging.debug("simulink_sim creating http server")
    
    # Main thread opens a web service to receive simulation steps.
    app = web.Application()
    app.router.add_post('/', _handle_request)
    logging.info('starting http server on port %d' % (_brainport,))

    # Start the web app
    web.run_app(app, sock=sock, access_log=None)

    logging.info("simulink_sim finished")
