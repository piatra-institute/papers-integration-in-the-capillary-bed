"""Checks that the pooled alternative has the declared kinetics and bound."""
import numpy as np
import pytest
from capnet.pooled import saturating_filter_trace


def test_saturating_controller_step_matches_continuous_solution():
    times = np.arange(1, 11) * 10.
    observed = saturating_filter_trace(np.full(10, 2.), (3., 1., 50.))
    expected = 3. * np.tanh(2.) * (1. - np.exp(-times / 50.))
    np.testing.assert_allclose(observed, expected, rtol=1e-14, atol=1e-14)
    assert observed[0] < expected[-1] < 3.


def test_saturating_controller_rejects_unresolved_time_constant():
    with pytest.raises(ValueError):
        saturating_filter_trace(np.ones(10), (1., 1., .1))


def test_pooled_controller_saturates_and_ignores_branch_labels():
    a = np.linspace(0., 100., 100)
    b = a[::-1]
    f = lambda x: saturating_filter_trace(x, (2., 1., 10.))
    assert np.max(np.abs(f(a+b))) <= 2.
    np.testing.assert_array_equal(f(a+b), f(b+a))
    assert np.max(np.abs(f(a+b)-f(a)-f(b))) > 1.
