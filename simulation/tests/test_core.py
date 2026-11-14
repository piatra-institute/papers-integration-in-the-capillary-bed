"""Complementary core invariants, independent of fitted scientific conclusions."""

import numpy as np

from capnet.experiment import Protocol, parameters, trace
from capnet.model import K_REST, Params, Solver, site_k
from capnet.network import build


def test_passive_coupling_conserves_capacitance_weighted_charge():
    """With membrane currents removed, junctions redistribute but cannot create charge."""
    net = build('T1')
    solver = Solver(net, dt=2.0)
    p = parameters([[.4, .06, 50.0]])
    rng = np.random.default_rng(2901)
    initial = -30.0 + rng.normal(size=(1, net.n))
    linear = (np.zeros((1, net.n)), np.zeros((1, net.n)))
    final = solver.run(p, lambda t: K_REST, t_end=40.0, v0=initial, linear=linear)
    np.testing.assert_allclose(final @ solver.cmem, initial @ solver.cmem, rtol=0, atol=1e-8)
    assert np.ptp(final) < np.ptp(initial)


def test_uniform_passive_rest_remains_fixed_with_heterogeneous_capacitance():
    net = build('T2')
    solver = Solver(net, dt=2.0)
    p = parameters([[.4, .06, 50.0]])
    rest = np.full((1, net.n), -30.0)
    linear = (np.full((1, net.n), .02), rest)
    final = solver.run(p, lambda t: K_REST, t_end=100.0, v0=rest, linear=linear)
    np.testing.assert_allclose(final, rest, rtol=0, atol=1e-9)


def test_batched_parameter_rows_equal_independent_runs():
    """Shared eigenvectors must not mix independent simulated preparations."""
    net = build('T1')
    solver = Solver(net, dt=2.0)
    p = parameters([[.4, .06, 50.0], [.5, .04, 40.0]])
    rest = solver.rest(p)
    stimulus = site_k(net.n, [net.sites['tip0']], [8.0], onset=20.0, offset=100.0)
    together = solver.run(p, stimulus, t_end=200.0, v0=rest)
    separately = []
    for row in range(p.size):
        single = Params.from_matrix(p.as_matrix()[row:row + 1])
        separately.append(solver.run(single, stimulus, t_end=200.0, v0=rest[row:row + 1]))
    np.testing.assert_allclose(together, np.vstack(separately), rtol=0, atol=1e-9)


def test_delayed_passive_response_uses_time_aligned_single_control():
    net = build('T1')
    solver = Solver(net, dt=2.0)
    p = parameters([[.4, .06, 50.0]])
    rest = solver.rest(p)
    args = dict(mode='passive', rest=rest, record=[net.zone2])
    _, a = trace(solver, p, Protocol(('tip0',), (8.0,), end=1000.0), **args)
    _, b = trace(solver, p, Protocol(('tip1',), (8.0,), onset=250.0, end=1000.0), **args)
    _, ab = trace(solver, p, Protocol(('tip0', 'tip1'), (8.0, 8.0), delay=150.0, end=1000.0), **args)
    np.testing.assert_allclose(ab, a + b, rtol=0, atol=1e-7)


def test_tree_automorphisms_preserve_distal_singleton_trace():
    """Sibling and remote terminal tips must have equal arteriolar singleton drives."""
    net = build('T1')
    solver = Solver(net, dt=2.0)
    p = parameters([[.4, .06, 50.0]])
    rest = solver.rest(p)
    responses = []
    for name in ('tip0', 'tip1', 'tip4'):
        _, h = trace(solver, p, Protocol((name,), (8.0,), end=1000.0), rest=rest, record=[net.zone2])
        responses.append(h)
    for h in responses[1:]:
        np.testing.assert_allclose(h, responses[0], rtol=0, atol=1e-7)


def test_focal_block_uses_its_own_stationary_baseline():
    net = build('T1')
    solver = Solver(net, dt=2.0)
    p = parameters([[.4, .06, 50.0]])
    for mode in ('distributed', 'passive', 'sensor_only'):
        _, h = trace(solver, p, Protocol(('tip0',), (K_REST,), end=300.0),
                     mode=mode, block_nodes=(17,), block_fraction=1.0, record=[net.zone2, 17])
        np.testing.assert_allclose(h, 0.0, rtol=0, atol=1e-7)


def test_sensor_only_fixed_architecture_preserves_tip_symmetry():
    """Potential sensor sites must be fixed symmetrically, not activated by protocol identity."""
    net = build('T1')
    solver = Solver(net, dt=2.0)
    p = parameters([[.7, .05, 12.0]])
    rest = solver.rest(p)
    responses = []
    for name in ('tip0', 'tip1', 'tip4'):
        _, h = trace(solver, p, Protocol((name,), (10.0,), end=1000.0),
                     mode='sensor_only', rest=rest, record=[net.zone2])
        responses.append(h)
    assert np.max(np.abs(responses[0])) > .01
    for h in responses[1:]:
        np.testing.assert_allclose(h, responses[0], rtol=0, atol=1e-7)
