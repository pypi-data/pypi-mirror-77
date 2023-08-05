# -*- coding: utf-8 -*-

import numpy as np

from npbrain.core import integrate
from npbrain.core.synapse import *
from npbrain.utils.helper import get_clip

__all__ = [
    'AMPA1',
    'AMPA2',
]


def AMPA1(pre, post, connection, g_max=0.10, E=0., tau_decay=2.0, delay=None, name='AMPA_ChType1'):
    """AMPA conductance-based synapse (type 1).

    .. math::

        I_{syn}&=\\bar{g}_{syn} s (V-E_{syn})

        \\frac{d s}{d t}&=-\\frac{s}{\\tau_{decay}}+\\sum_{k} \\delta(t-t_{j}^{k})

    Parameters
    ----------
    pre : Neurons
        The pre-synaptic neuron group.
    post : Neurons
        The post-synaptic neuron group.
    connection : tuple
        The connectivity.
    g_max
    E
    tau_decay
    delay
    name

    Returns
    -------
    synapse : Synapses
        The constructed AMPA synapses.
    """

    pre_ids, post_ids, anchors = connection

    var2index = {'s': 0}
    num, num_pre, num_post = len(pre_ids), pre.num, post.num
    state = init_syn_state(num_syn=num, variables=[('s', 0.)])
    delay_state = init_delay_state(num_post=num_post, delay=delay)

    @integrate(signature='{f}[:]({f}[:], {f})')
    def int_f(s, t):
        return - s / tau_decay

    def update_state(syn_st, delay_st, t, delay_idx, pre_state):
        # calculate synaptic state
        s = int_f(syn_st[0], t)
        spike_idx = np.where(pre_state[-3] > 0.)[0]
        for i in spike_idx:
            idx = anchors[:, i]
            s[idx[0]: idx[1]] += 1
        syn_st[0] = s
        # get post-synaptic values
        g = np.zeros(num_post)
        for i in range(num_pre):
            idx = anchors[:, i]
            post_idx = post_ids[idx[0]: idx[1]]
            g[post_idx] += s[idx[0]: idx[1]]
        delay_st[delay_idx] = g

    if hasattr(post, 'ref') and getattr(post, 'ref') > 0.:

        def output_synapse(delay_st, output_idx, post_state):
            g_val = delay_st[output_idx]
            post_val = - g_max * g_val * (post_state[0] - E)
            post_state[-1] += post_val * post_state[-5]

    else:

        def output_synapse(delay_st, output_idx, post_state):
            g_val = delay_st[output_idx]
            post_val = - g_max * g_val * (post_state[0] - E)
            post_state[-1] += post_val

    return Synapses(**locals())


def AMPA2(pre, post, connection, g_max=0.42, E=0., alpha=0.98, beta=0.18,
          T=0.5, T_duration=0.5, delay=None, name='AMPA_ChType2'):
    """AMPA conductance-based synapse (type 2).

    .. math::

        I_{syn}&=\\bar{g}_{syn} s (V-E_{syn})

        \\frac{ds}{dt} &=\\alpha[T](1-s)-\\beta s

    Parameters
    ----------
    pre : Neurons
        The pre-synaptic neuron group.
    post : Neurons
        The post-synaptic neuron group.
    connection : tuple
        The connectivity.
    g_max
    E
    alpha
    beta
    T
    T_duration
    delay
    name

    Returns
    -------
    synapse : Synapses
        The constructed AMPA synapses.
    """

    pre_ids, post_ids, anchors = connection

    var2index = {'s': 0, 'syn_sp_time': 1}
    num, num_pre, num_post = len(pre_ids), pre.num, post.num
    state = init_syn_state(num_syn=num, variables=[('s', 0.), ('syn_sp_time', -1e5)])
    delay_state = init_delay_state(num_post=num_post, delay=delay)

    clip = get_clip()

    @integrate(signature='{f}[:]({f}[:], {f}, {f}[:])')
    def int_s(s, t, TT):
        return alpha * TT * (1 - s) - beta * s

    def update_state(syn_st, delay_st, t, delay_idx, pre_state):
        # get synaptic state
        s = syn_st[0]
        last_spike = syn_st[1]
        pre_spike = pre_state[-3]
        # calculate synaptic state
        spike_idx = np.where(pre_spike > 0.)[0]
        for i in spike_idx:
            idx = anchors[:, i]
            last_spike[idx[0]: idx[1]] = t
        TT = ((t - last_spike) < T_duration).astype(np.float64) * T
        s = clip(int_s(s, t, TT), 0., 1.)
        syn_st[0] = s
        syn_st[1] = last_spike
        # get post-synaptic values
        g = np.zeros(num_post)
        for i in range(num_pre):
            idx = anchors[:, i]
            post_idx = post_ids[idx[0]: idx[1]]
            g[post_idx] += s[idx[0]: idx[1]]
        delay_st[delay_idx] = g

    if hasattr(post, 'ref') and getattr(post, 'ref') > 0.:

        def output_synapse(delay_st, output_idx, post_state):
            g_val = delay_st[output_idx]
            post_val = - g_max * g_val * (post_state[0] - E)
            post_state[-1] += post_val * post_state[-5]

    else:

        def output_synapse(delay_st, output_idx, post_state):
            g_val = delay_st[output_idx]
            post_val = - g_max * g_val * (post_state[0] - E)
            post_state[-1] += post_val

    return Synapses(**locals())
