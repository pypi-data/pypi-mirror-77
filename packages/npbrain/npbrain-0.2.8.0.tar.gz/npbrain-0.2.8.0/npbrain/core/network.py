# -*- coding: utf-8 -*-

import inspect
import time
from pprint import pprint

import numpy as np

from .monitor import SpikeMonitor, StateMonitor
from .neuron import Neurons
from .synapse import Synapses
from ..utils import helper
from ..utils import profile

__all__ = [
    'Network',
]


class Network(object):
    """The main simulation controller in ``NumpyBrain``.

    ``Network`` handles the running of a simulation. It contains a set of
    objects that are added with `add()`. The `run()` method
    actually runs the simulation. The main loop runs according to user add
    orders. The objects in the `Network` are accessible via their names, e.g.
    `net.name` would return the `object` (including neurons, synapses, and
    monitors) with this name.

    """

    def __init__(self, *args, **kwargs):
        # store and neurons and synapses
        self.neurons = []
        self.synapses = []
        self.state_monitors = []
        self.spike_monitors = []

        # store all objects
        self._objsets = helper.Dict()
        self.objects = []

        # store states of objects and synapses
        self._neuron_states = None
        self._synapse_states = None

        # record the current step
        self.current_time = 0.

        # add objects
        self.add(*args, **kwargs)

        # necessary functions
        self._step = None
        self._input = None
        self._neu_state_args = None

    def add(self, *args, **kwargs):
        """Add object (neurons or synapses or monitor) to the network.

        Parameters
        ----------
        args : list, tuple
            The nameless objects.
        kwargs : dict
            The named objects, which can be accessed by `net.xxx`
            (xxx is the name of the object).
        """
        keywords = ['neurons', 'synapses', 'monitors', '_objsets', '_neuron_states',
                    '_synapse_states', 'current_time', 'add', 'run', 'run_time']
        for obj in args:
            self._add_obj(obj)
        for name, obj in kwargs.items():
            self._add_obj(obj)
            self._objsets.unique_add(name, obj)
            if name in keywords:
                raise ValueError('Invalid name: ', name)
            setattr(self, name, obj)

    @staticmethod
    def _get_args(func):
        if hasattr(func, 'py_func'):
            args_ = inspect.getfullargspec(func.py_func)[0]
        else:
            args_ = inspect.getfullargspec(func)[0]
        return args_

    def _get_step_function(self):
        step_func_str = '''\ndef step_func(t, i):'''

        step_func_local = {'syn' + str(oi): syn for oi, syn in enumerate(self.synapses)}
        step_func_local.update({'neu' + str(oi): neu for oi, neu in enumerate(self.neurons)})
        step_func_local.update({'st_mon' + str(oi): mon for oi, mon in enumerate(self.state_monitors)})
        step_func_local.update({'sp_mon' + str(oi): mon for oi, mon in enumerate(self.spike_monitors)})

        obj2name = {neu: 'neu{}'.format(oi) for oi, neu in enumerate(self.neurons)}
        obj2name.update({syn: 'syn{}'.format(oi) for oi, syn in enumerate(self.synapses)})
        obj2name.update({mon: 'st_mon{}'.format(oi) for oi, mon in enumerate(self.state_monitors)})
        obj2name.update({mon: 'sp_mon{}'.format(oi) for oi, mon in enumerate(self.spike_monitors)})

        # synapse update function

        for oi, syn in enumerate(self.synapses):
            # update_state()
            args = self._get_args(syn.update_state)
            step_func_str += '\n\t' + 'syn{}.update_state('.format(oi)
            for arg in args:
                if arg in ['t', 'i']:
                    step_func_str += arg + ", "
                elif arg in ['delay_idx', 'in_idx']:
                    step_func_str += 'syn{}.var2index["g_in"], '.format(oi)
                elif arg in ['output_idx', 'out_idx']:
                    step_func_str += 'syn{}.var2index["g_out"], '.format(oi)
                    print('Define "{}" in {}.update_state(), maybe a wrong operation, '
                          'please check.'.format(arg, syn.name))
                elif arg in ['syn_st', 'syn_state']:
                    step_func_str += 'syn{}.state, '.format(oi)
                elif arg in ['delay_st', 'delay_state']:
                    step_func_str += 'syn{}.delay_state, '.format(oi)
                elif arg in ['pre_st', 'pre_state']:
                    step_func_str += '{}.state, '.format(obj2name[syn.pre])
                elif arg in ['post_st', 'post_state']:
                    step_func_str += '{}.state, '.format(obj2name[syn.post])
                else:
                    raise ValueError('Unknown argument in {}.update_state(): {}'.format(syn.name, arg))
            step_func_str += ')'

            # output_synapse()
            args = self._get_args(syn.output_synapse)
            step_func_str += '\n\t' + 'syn{}.output_synapse('.format(oi)
            for arg in args:
                if args in ['t', 'i']:
                    step_func_str += arg + ', '
                elif arg in ['delay_idx', 'in_idx']:
                    step_func_str += 'syn{}.var2index["g_in"], '.format(oi)
                    print('Define "{}" in {}.output_synapse(), maybe a wrong operation, '
                          'please check.'.format(arg, syn.name))
                elif arg in ['output_idx', 'out_idx']:
                    step_func_str += 'syn{}.var2index["g_out"], '.format(oi)
                elif arg in ['syn_st', 'syn_state']:
                    step_func_str += 'syn{}.state, '.format(oi)
                elif arg in ['delay_st', 'delay_state']:
                    step_func_str += 'syn{}.delay_state, '.format(oi)
                elif arg in ['pre_st', 'pre_state']:
                    step_func_str += '{}.state, '.format(obj2name[syn.pre])
                elif arg in ['post_st', 'post_state']:
                    step_func_str += '{}.state, '.format(obj2name[syn.post])
                else:
                    raise ValueError('Unknown argument in {}.update_state(): {}'.format(syn.name, arg))
            step_func_str += ')'

        # neuron update function
        for oi, neu in enumerate(self.neurons):
            step_func_str += '\n\t' + 'neu{}.update_state('.format(oi)
            args = self._get_args(neu.update_state)
            for arg in args:
                if arg in ['t', 'i']:
                    step_func_str += arg + ', '
                elif arg in ['neu_st', 'neu_state', 'neuron_st', 'neuron_state']:
                    step_func_str += '{}.state, '.format(obj2name[neu])
            step_func_str += ')'

        # state monitor function
        for oi, mon in enumerate(self.state_monitors):
            args = self._get_args(mon.update_state)
            if len(args) == 3:
                step_func_str += '\n\tst_mon{oi}.update_state({obj}.state, st_mon{oi}.state, i)'.format(
                    oi=oi, obj=obj2name[mon.target])
            elif len(args) == 5:
                step_func_str += '\n\tst_mon{oi}.update_state(' \
                                 '{obj}.delay_state, ' \
                                 'st_mon{oi}.state, ' \
                                 '{obj}.var2index["g_out"], ' \
                                 '{obj}.var2index["g_in"], ' \
                                 'i)'.format(oi=oi, obj=obj2name[mon.target])
            elif len(args) == 6:
                step_func_str += '\n\tst_mon{oi}.update_state(' \
                                 '{obj}.state, ' \
                                 '{obj}.delay_state, ' \
                                 'st_mon{oi}.state, ' \
                                 '{obj}.var2index["g_out"], ' \
                                 '{obj}.var2index["g_in"], ' \
                                 'i)'.format(oi=oi, obj=obj2name[mon.target])
            else:
                raise ValueError('Unknown arguments of monitor update_state().')

        # spike monitor function
        for oi, mon in enumerate(self.spike_monitors):
            step_func_str += '\n\tsp_mon{oi}.update_state({obj}.state, sp_mon{oi}.time, sp_mon{oi}.index, t)'.format(
                oi=oi, obj=obj2name[mon.target])

        # update `dalay_idx` and `output_idx`
        for oi, syn in enumerate(self.synapses):
            if syn.delay_len <= 1:
                continue
            step_func_str += '\n\t{syn}.var2index["g_in"] = ({syn}.var2index["g_in"] + 1) % ' \
                             '{syn}.delay_len'.format(syn='syn' + str(oi))
            step_func_str += '\n\t{syn}.var2index["g_out"] = ({syn}.var2index["g_out"] + 1) % ' \
                             '{syn}.delay_len'.format(syn='syn' + str(oi))

        if profile.debug:
            print('\nStep function :')
            print('----------------------------')
            print(step_func_str)
            print()
            pprint(step_func_local)
            print()
        exec(compile(step_func_str, '', 'exec'), step_func_local)
        self._step = step_func_local['step_func']

    def _get_input_function(self, inputs, duration):
        iterable_inputs, fixed_inputs, no_inputs = self._format_inputs_and_receiver(inputs, duration)
        neu_state_args = {}

        input_func_local = {}
        input_func_str = '''\ndef input_func(run_idx, {arg}):'''

        ni = 0
        for receiver, inputs, dur in iterable_inputs:
            input_func_str += '''
    if {du0} <= run_idx <= {du1}:
        obj_idx = run_idx - {du0}
        {neu_st}[-1] = {input}[obj_idx]
    else:
        {neu_st}[-1] = 0.'''.format(du0=dur[0], du1=dur[1], neu_st='neu_st' + str(ni), input='in' + str(ni))
            input_func_local['in' + str(ni)] = inputs
            neu_state_args['neu_st' + str(ni)] = receiver.state
            ni += 1

        for receiver, inputs, dur in fixed_inputs:
            input_func_str += '''
    if {du0} <= run_idx <= {du1}:
        {neu_st}[-1] = {input}
    else:
        {neu_st}[-1] = 0.'''.format(du0=dur[0], du1=dur[1], neu_st='neu_st' + str(ni), input='in' + str(ni))
            input_func_local['in' + str(ni)] = inputs
            neu_state_args['neu_st' + str(ni)] = receiver.state
            ni += 1

        for receiver in no_inputs:
            input_func_str += '''\n    {neu_st}[-1] = 0.'''.format(neu_st='neu_st' + str(ni))
            neu_state_args['neu_st' + str(ni)] = receiver.state
            ni += 1

        input_func_str = input_func_str.format(arg=','.join(neu_state_args.keys()))

        if profile.debug:
            print('\nInput function :')
            print('----------------------------')
            print(input_func_str)
            print()
            pprint(input_func_local)
            print()
        exec(compile(input_func_str, '', 'exec'), input_func_local)
        self._input = helper.autojit(input_func_local['input_func'])
        self._neu_state_args = neu_state_args

    def run(self, duration, report=False, inputs=(), repeat=False, report_percent=0.1):
        """Run the simulation for the given duration.

        This function provides the most convenient way to run the network.
        For example:

        >>> # first of all, define the network we want.
        >>> import npbrain as nn
        >>> lif1 = nn.LIF(10, noise=0.2)
        >>> lif2 = nn.LIF(10, noise=0.5)
        >>> syn = nn.VoltageJumpSynapse(lif1, lif2, 1.0, nn.conn.all2all(lif1.num, lif2.num))
        >>> net = Network(syn, lif1, lif2)
        >>> # next, run the network.
        >>> net.run(100.) # run 100. ms
        >>>
        >>> # if you want to provide input to `lif1`
        >>> # for example, a constant input `11` (more complex inputs please use `input_factory.py`)
        >>> net.run(100., inputs=(lif1, 11.))
        >>>
        >>> # if you want to provide input to `lif1` in the period of 30-50 ms.
        >>> net.run(100., inputs=(lif1, 11., (30., 50.)))
        >>>
        >>> # moreover, if you want to provide input to `lif1` in the period of 30-50 ms,
        >>> # and provide input to `lif2` in the period of 10-100 ms.
        >>> net.run(100., inputs=[(lif1, 11., (30., 50.)), (lif2, -1., (10., 100.))])
        >>>
        >>> # if you want to known the running status in real-time.
        >>> net.run(100., report=True)
        >>>

        Parameters
        ----------
        duration : int, float
            The amount of simulation time to run for.
        report : bool
            Report the progress of the simulation.
        repeat : bool
            Whether repeat run this model. If `repeat=True`, every time
            call this method will initialize the object state.
        inputs : list, tuple
            The receivers, external inputs and durations.
        """

        # 1. initialization
        # ------------------

        # time
        dt = profile.get_dt()
        ts = np.arange(self.current_time, self.current_time + duration, dt)
        ts = np.asarray(ts, dtype=profile.ftype)
        run_length = len(ts)

        # monitors
        for mon in self.state_monitors:
            mon.init_state(run_length)

        # neurons
        if repeat:
            if self._neuron_states is None:
                self._neuron_states = [neu.state.copy() for neu in self.neurons]
            else:
                for neu, state in zip(self.neurons, self._neuron_states):
                    neu.state[:] = state.copy()

        # synapses
        if repeat:
            if self._synapse_states is None:
                self._synapse_states = []
                for syn in self.synapses:
                    state = (None if syn.state is None else syn.state.copy(), syn.delay_state.copy())
                    self._synapse_states.append(state)
            else:
                for syn, state in zip(self.synapses, self._synapse_states):
                    for i, (st, dst) in enumerate(state):
                        if st is not None:
                            syn.state[:] = st.copy()
                        syn.delay_state[:] = dst.copy()

        # generate step function
        if self._step is None:
            self._get_step_function()

        # generate input function
        if self._input is None:
            self._get_input_function(inputs, duration)

        # 2. run
        # ---------
        if report:
            t0 = time.time()
            self._input(run_idx=0, **self._neu_state_args)
            self._step(t=ts[0], i=0)
            print('Compilation used {:.4f} ms.'.format(time.time() - t0))

            print("Start running ...")
            report_gap = int(run_length * report_percent)
            t0 = time.time()
            for run_idx in range(1, run_length):
                self._input(run_idx=run_idx, **self._neu_state_args)
                self._step(t=ts[run_idx], i=run_idx)
                if (run_idx + 1) % report_gap == 0:
                    percent = (run_idx + 1) / run_length * 100
                    print('Run {:.1f}% using {:.3f} s.'.format(percent, time.time() - t0))
            print('Simulation is done. ')
        else:
            for run_idx in range(run_length):
                self._input(run_idx=run_idx, **self._neu_state_args)
                self._step(t=ts[run_idx], i=run_idx)

        # 3. Finally
        # -----------
        self.current_time = duration

    def run_time(self):
        """Get the time points of the network.

        Returns
        -------
        times : numpy.ndarray
            The running time-steps of the network.
        """
        return np.arange(0, self.current_time, profile.get_dt())

    def _add_obj(self, obj):
        if isinstance(obj, Neurons):
            self.neurons.append(obj)
        elif isinstance(obj, Synapses):
            self.synapses.append(obj)
        elif isinstance(obj, StateMonitor):
            self.state_monitors.append(obj)
        elif isinstance(obj, SpikeMonitor):
            self.spike_monitors.append(obj)
        else:
            raise ValueError('Unknown object type: {}'.format(type(obj)))
        self.objects.append(obj)

    def _check_run_order(self):
        for obj in self.objects:
            if isinstance(obj, Synapses):
                syn_order = self.objects.index(obj)
                pre_neu_order = self.objects.index(obj.pre)
                post_neu_order = self.objects.index(obj.post)
                if syn_order > post_neu_order or syn_order > pre_neu_order:
                    raise ValueError('Synapse "{}" must run before than the '
                                     'pre-/post-synaptic neurons.'.format(obj))

    def _format_inputs_and_receiver(self, inputs, duration):
        dt = profile.get_dt()
        # format inputs and receivers
        if len(inputs) > 1 and not isinstance(inputs[0], (list, tuple)):
            if isinstance(inputs[0], Neurons):
                inputs = [inputs]
            else:
                raise ValueError('Unknown input structure.')
        # ---------------------
        # classify input types
        # ---------------------
        # 1. iterable inputs
        # 2. fixed inputs
        iterable_inputs = []
        fixed_inputs = []
        neuron_with_inputs = []
        for input_ in inputs:
            # get "receiver", "input", "duration"
            if len(input_) == 2:
                obj, Iext = input_
                dur = (0, duration)
            elif len(input_) == 3:
                obj, Iext, dur = input_
            else:
                raise ValueError
            err = 'You can assign inputs only for added object. "{}" is not in the network.'
            if isinstance(obj, str):
                try:
                    obj = self._objsets[obj]
                except:
                    raise ValueError(err.format(obj))
            assert isinstance(obj, Neurons), "You can assign inputs only for Neurons."
            assert obj in self.objects, err.format(obj)
            assert len(dur) == 2, "Must provide the start and the end simulation time."
            assert 0 <= dur[0] < dur[1] <= duration
            dur = (int(dur[0] / dt), int(dur[1] / dt))
            neuron_with_inputs.append(obj)

            # judge the type of the inputs.
            if isinstance(Iext, (int, float)):
                Iext = np.ones(obj.num, dtype=profile.ftype) * Iext
                fixed_inputs.append([obj, Iext, dur])
                continue
            size = np.shape(Iext)[0]
            run_length = dur[1] - dur[0]
            if size != run_length:
                if size == 1:
                    Iext = np.ones(obj.num, dtype=profile.ftype) * Iext
                elif size == obj.num:
                    Iext = Iext
                else:
                    raise ValueError('Wrong size of inputs for', obj)
                fixed_inputs.append([obj, Iext, dur])
            else:
                input_size = np.size(Iext[0])
                err = 'The input size "{}" do not match with neuron ' \
                      'group size "{}".'.format(input_size, obj.num)
                assert input_size == 1 or input_size == obj.num, err
                iterable_inputs.append([obj, Iext, dur])
        # 3. no inputs
        no_inputs = []
        for neu in self.neurons:
            if neu not in neuron_with_inputs:
                no_inputs.append(neu)
        return iterable_inputs, fixed_inputs, no_inputs
