import numpy as np

from capnet.experiment import Protocol, SlowReset, parameters, trace
from capnet.model import Solver
from capnet.network import build


def test_reset_activation_is_continuous_and_recovers_after_drive():
    reset = SlowReset(depletion_tau_ms=60000., recovery_tau_ms=180000.)
    assert reset.activation(0., 100., 18100.) == 0.
    assert reset.activation(100., 100., 18100.) == 0.
    at_offset = reset.activation(18100., 100., 18100.)
    np.testing.assert_allclose(at_offset, 1-np.exp(-.3))
    np.testing.assert_allclose(reset.activation(198100., 100., 18100.), at_offset/np.e)
    assert abs(reset.activation(18100.+1e-4, 100., 18100.)-at_offset) < 1e-9


def test_disabled_reset_is_identical_to_primary_membrane_model():
    net = build()
    solver = Solver(net, 2.)
    p = parameters([.4, .06, 50.])
    rest = solver.rest(p)
    q = Protocol(('tip0',), (10.,), end=800.)
    t, h = trace(solver, p, q, rest=rest)
    rt, rh = trace(solver, p, q, rest=rest,
                   slow_reset=SlowReset(kir_loss_fraction=0., trpv4_max_ns=0.))
    np.testing.assert_array_equal(rt, t)
    np.testing.assert_array_equal(rh, h)


def test_slow_reset_changes_response_and_preserves_pre_stimulus_rest():
    net = build()
    solver = Solver(net, 2.)
    p = parameters([.4, .06, 50.])
    rest = solver.rest(p)
    q = Protocol(('tip0',), (10.,), duration=1000., end=1600.)
    t, h = trace(solver, p, q, rest=rest)
    rt, rh = trace(solver, p, q, rest=rest,
                   slow_reset=SlowReset(depletion_tau_ms=60000., trpv4_max_ns=.02))
    np.testing.assert_allclose(rh[:, rt<=100], 0., atol=1e-7)
    assert np.max(abs(rh-h)) > .001


def test_distal_active_control_includes_anastomosis_bridge():
    """Turning bridge nodes passive must change a bridge-adjacent paired response."""
    net = build('T3')
    bridges = net.cap & np.isnan(net.dist_um)
    assert bridges.sum() == 3
    solver = Solver(net, 2.)
    p = parameters([.7, .05, 12.])
    rest = solver.rest(p)
    q = Protocol(('tip3', 'tip4'), (10., 10.), delay=250.)
    _, active = trace(solver, p, q, mode='sensor_only', rest=rest)
    # This relabeling reproduces the former NaN comparison bug without
    # changing graph edges, capacitance, or the stimulated sites.
    net.dist_um[bridges] = 0.
    _, passive = trace(solver, p, q, mode='sensor_only', rest=rest)
    assert np.max(abs(active-passive)) > .01
