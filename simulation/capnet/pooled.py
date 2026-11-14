"""A bounded pooled controller with a resolvable relaxation time."""
import numpy as np


def saturating_filter_trace(x, theta, dt=10.):
    """Exact zero-order-hold update of tau*y' = -y + a*tanh(x/s).

    The output is bounded by a in magnitude, with positive concentration scale
    s. A time constant at least as long as the recording interval is required.
    The driver is the passive cable fitted to isolated-input data, then frozen.
    """
    a, s, tau = theta
    if a < 0 or s <= 0 or dt <= 0 or tau < dt:
        raise ValueError('Require a >= 0, s > 0 and tau >= dt > 0')
    x = np.asarray(x)
    forcing = a * np.tanh(x / s)
    alpha = np.exp(-dt / tau)
    y = np.zeros_like(x, dtype=float)
    for i in range(x.shape[-1]):
        y[..., i] = (y[..., i-1] if i else 0) * alpha + (1-alpha) * forcing[..., i]
    return y
