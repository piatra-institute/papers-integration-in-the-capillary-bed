"""Protocols and controls. Every comparator is fitted on single-site traces only."""
from dataclasses import dataclass
import numpy as np
from scipy.optimize import least_squares
from .model import Solver, Params, i_kir, kir_slope, e_k, K_REST

MODES = ('distributed', 'passive', 'capillary_linear', 'arteriole_linear', 'sensor_only')
FREE = [0, 1, 4]
BROAD_CELLS = 16
BOUNDS = np.array([[.2, .02, 10.], [.8, .10, 200.]])
BASE = np.array([.4, .06, -30., 25., 50., .65, .2, -30.])

@dataclass(frozen=True)
class Protocol:
    sites: tuple
    levels: tuple
    delay: float = 0.
    duration: float = 500.
    onset: float = 100.
    end: float = 1600.


@dataclass(frozen=True)
class SlowReset:
    """Imposed slow channel modulation, not an identified PIP2 kinetic model.

    A hypothetical receptor drive starts with the first pulse and ends with the
    last. Kir availability falls exponentially while this drive is present and
    recovers exponentially afterwards. A complementary ohmic depolarizing
    conductance represents the sign of TRPV4 recruitment, not its GHK law or
    stochastic openings. Time constants, conductance and spatial scope are
    declared sensitivity assumptions. Potassium alone is not asserted to cause
    receptor activation.
    """
    depletion_tau_ms: float = 60000.
    trpv4_depletion_tau_ms: float | None = None
    recovery_tau_ms: float = 180000.
    trpv4_max_ns: float = .02
    kir_loss_fraction: float = 1.
    reversal_mv: float = 0.
    scope: str = 'all_capillaries'

    def activation(self, t, onset, offset, tau_ms=None):
        if t <= onset:
            return 0.
        duration = min(t, offset) - onset
        z = -np.expm1(-duration / (tau_ms or self.depletion_tau_ms))
        if t > offset:
            z *= np.exp(-(t-offset)/self.recovery_tau_ms)
        return float(z)


def parameters(x):
    x = np.atleast_2d(x)
    mat = np.tile(BASE, (len(x), 1))
    mat[:, FREE] = x
    return Params.from_matrix(mat)


def pack(p):
    return p.as_matrix()[:, FREE]


def sample(rng, n):
    a = rng.uniform(BOUNDS[0], BOUNDS[1], size=(n, 3))
    a[:, 2] = np.exp(rng.uniform(np.log(BOUNDS[0, 2]), np.log(BOUNDS[1, 2]), n))
    return a


def trace(solver, p, protocol, mode='distributed', rest=None, record=None,
          dt_record=10., block_nodes=(), block_fraction=0., katp=False,
          slow_reset=None):
    """Positive hyperpolarization. Linear controls preserve resting current and tangent.

    The sensor-only control keeps full voltage-dependent Kir in distal branches
    (distance >= 70 um) and anastomosis bridge cells; proximal trunk and PA are linear.
    independent-sensor oracle is implemented by summing isolated full-model responses.
    Focal block is conducted with its own baseline, then contemporaneous singles.
    """
    net = solver.net
    if record is None:
        record = [net.zone2, 17]  # PA and first capillary trunk's distal cell
    dt = solver.dt
    if rest is None:
        rest = solver.rest(p)
    gbar, gbg, ebg, dv = solver.node_params(p)
    vbase = rest.copy()
    kir_mask = np.ones(net.n)
    kir_mask[list(block_nodes)] = 1. - block_fraction
    if block_nodes and block_fraction:
        rest = solver.rest(p, kir_mask=kir_mask)
        vbase = rest.copy()
        gbar *= kir_mask
    irest = gbg*(rest-ebg) + i_kir(rest, K_REST, gbar, dv)
    slope = np.maximum(gbg + kir_slope(rest, K_REST, gbar, dv), .001)
    if mode == 'distributed':
        lm = np.zeros(net.n, dtype=bool)
    elif mode == 'passive':
        lm = np.ones(net.n, dtype=bool)
    elif mode == 'capillary_linear':
        lm = net.cap.copy()
    elif mode == 'arteriole_linear':
        lm = net.pa.copy()
    elif mode == 'sensor_only':
        lm = np.ones(net.n, dtype=bool)
        lm[net.cap & ((net.dist_um >= 70.) | np.isnan(net.dist_um))] = False
    else:
        raise ValueError(mode)
    scale = 1./(1. + (1e3/p.r_gj[:,None])*solver.lam[None,:])
    v = rest.copy()
    k = np.full((1,net.n), K_REST)
    cdt = solver.cmem[None,:]/dt
    every = int(round(dt_record/dt))
    out, times = [], []
    cache = {}
    if slow_reset is not None:
        if mode != 'distributed':
            raise ValueError('Slow-reset sensitivity is defined only for the distributed membrane law')
        if slow_reset.scope == 'all_capillaries':
            reset_mask = net.cap[None, :]
        elif slow_reset.scope == 'exposed_patch':
            reset_mask = np.zeros((1, net.n), dtype=bool)
            for name in protocol.sites:
                reset_mask[:, net.sites[name]] = True
        else:
            raise ValueError(slow_reset.scope)
    for step in range(int(round(protocol.end/dt))):
        t = step*dt
        active = tuple(protocol.onset + (protocol.delay if j else 0) <= t < protocol.onset + (protocol.delay if j else 0) + protocol.duration for j in range(len(protocol.sites)))
        if active not in cache:
            k = np.full((1, net.n), K_REST)
            gkatp = np.zeros((1, net.n))
            for j,(name,level) in enumerate(zip(protocol.sites,protocol.levels)):
                if active[j]:
                    if katp:
                        gkatp[:,net.sites[name]] = level
                    else:
                        k[:,net.sites[name]] = level
            # Frozen-voltage K sensing is additive input to tangent membranes.
            forcing = i_kir(rest,k,gbar,dv)-i_kir(rest,K_REST,gbar,dv)
            cache[active] = k,gkatp,forcing
        k,gkatp,forcing = cache[active]
        ikir = i_kir(v,k,gbar,dv)
        ionic = gbg*(v-ebg)+ikir
        if slow_reset is not None:
            activation = slow_reset.activation(t, protocol.onset,
                protocol.onset + protocol.delay + protocol.duration)
            trpv4_activation = slow_reset.activation(t, protocol.onset,
                protocol.onset + protocol.delay + protocol.duration,
                slow_reset.trpv4_depletion_tau_ms)
            ionic += reset_mask * (
                -activation * slow_reset.kir_loss_fraction * ikir
                + trpv4_activation * slow_reset.trpv4_max_ns * (v - slow_reset.reversal_mv))
        lin = irest+slope*(v-rest)+forcing
        ionic = np.where(lm[None,:],lin,ionic)
        if katp:
            ionic += gkatp*(v-e_k(k))
        rhs=cdt*v-ionic
        v=((rhs@solver.w)*scale)@solver.w.T
        if (step+1)%every == 0:
            out.append(vbase[:,record]-v[:,record]);times.append(t+dt)
    return np.asarray(times),np.stack(out,axis=1)


def connected_patch(net, count=16):
    """One connected exposure region grown from the first distal subtree root.

    Breadth-first ordering balances its daughter branches; no PA nodes and no
    proximal common trunk cells are exposed. Cell-count is a design assumption.
    """
    roots=np.flatnonzero(net.cap & (net.dist_um==70.))
    queue=[int(roots[0])];seen=set();result=[]
    adjacency={i:[] for i in range(net.n)}
    for a,b in net.cap_edges:
        if net.cap[a] and net.cap[b]:adjacency[a].append(b);adjacency[b].append(a)
    while queue and len(result)<count:
        i=queue.pop(0)
        if i in seen or net.dist_um[i]<70.:continue
        seen.add(i);result.append(i)
        queue.extend(sorted(adjacency[i]))
    if len(result)!=count:raise ValueError('Exposure region exceeds available connected subtree')
    return np.array(result,dtype=int)


def flow(h):
    """Fixed dimensionless diameter then constant-pressure Poiseuille proxy."""
    diameter=1.+.30*np.tanh(np.maximum(h,0.)/10.)
    return diameter**4


def residual(a,b,ab):
    electrical=ab-a-b
    saturation=flow(a+b)-flow(a)-flow(b)+1.
    total=flow(ab)-flow(a)-flow(b)+1.
    return {'voltage':electrical,'flow':total,'saturation':saturation,'beyond_saturation':total-saturation}


def filter_trace(x,theta,dt=10.):
    """Three free parameters: pooled gain a, quadratic gain b, low-pass tau.

    y'=(-y+a*x+b*x^2)/tau; x is a fixed passive cable output, normalized by
    1mV. The quadratic pooled sensor can yield positive or negative interaction.
    Exact zero-order hold time update removes filter-integration instability.
    """
    a,b,tau=theta
    forcing=a*x+b*x*x
    alpha=np.exp(-dt/max(tau,1e-6))
    y=np.zeros_like(x)
    for i in range(x.shape[-1]):
        y[...,i]=(y[...,i-1] if i else 0)*alpha+(1-alpha)*forcing[...,i]
    return y
