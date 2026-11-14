"""Electrical model of a capillary-arteriole network, integrated for many parameter sets at once.

Membrane equation for every node i (Moshkforoush et al. 2020, model I):

    C_i dV_i/dt = -[I_bg + I_Kir + I_KATP + I_out]_i - sum_j g_ij (V_i - V_j)

    I_bg  = G_bg (V - E_bg)
    I_Kir = Gbar_Kir sqrt([K]o) (V - E_K) / (1 + exp((V - E_K - dV_Kir)/k_Kir))
    I_KATP = G_KATP (V - E_K)

Units: pF, nS, mV, pA, ms. Gap-junction coupling is integrated implicitly
(exact linear solve through a shared generalized eigenbasis), ionic currents
explicitly (semi-implicit Euler).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .network import Network, PA_UNITS_PER_NODE

R_GAS = 8314.0       # mJ mol-1 K-1, as in the published model code
TEMP_K = 293.0       # K, as in the published model code
FARADAY = 96485.0    # C mol-1
RT_F = R_GAS * TEMP_K / FARADAY   # mV
K_IN = 150.0         # mM intracellular K+
K_REST = 3.0         # mM resting extracellular K+
K_KIR = 7.0          # mV Kir slope factor
C_CAP = 8.0          # pF per cEC
C_PA_UNIT = 16.0     # pF per PA EC-SMC unit
R_GJ_PA = 10.0       # MOhm between neighbouring PA units
PARAM_NAMES = ["g_kir", "g_bg", "e_bg", "dv_kir", "r_gj", "g_kir_pa", "g_bg_pa", "e_bg_pa"]


def e_k(k_out):
    return RT_F * np.log(k_out / K_IN)


def i_kir(v, k_out, gbar, dv):
    ek = e_k(k_out)
    return gbar * np.sqrt(k_out) * (v - ek) / (1.0 + np.exp((v - ek - dv) / K_KIR))


def kir_slope(v, k_out, gbar, dv, h=1e-3):
    return (i_kir(v + h, k_out, gbar, dv) - i_kir(v - h, k_out, gbar, dv)) / (2 * h)


@dataclass
class Params:
    """Arrays of shape (S,) for S parameter sets."""
    g_kir: np.ndarray     # nS, cEC Kir conductance at 3 mM [K+]o
    g_bg: np.ndarray      # nS, cEC background conductance
    e_bg: np.ndarray      # mV, cEC background reversal
    dv_kir: np.ndarray    # mV, Kir half-inactivation offset from E_K
    r_gj: np.ndarray      # MOhm, cEC-cEC (and cEC-PA junction) coupling resistance
    g_kir_pa: np.ndarray  # nS per PA unit at 3 mM
    g_bg_pa: np.ndarray   # nS per PA unit
    e_bg_pa: np.ndarray   # mV

    @property
    def size(self) -> int:
        return int(np.asarray(self.g_kir).shape[0])

    @classmethod
    def from_matrix(cls, x: np.ndarray) -> "Params":
        return cls(*[np.asarray(x[:, i], dtype=float) for i in range(len(PARAM_NAMES))])

    def as_matrix(self) -> np.ndarray:
        return np.column_stack([getattr(self, n) for n in PARAM_NAMES])

    def take(self, idx) -> "Params":
        return Params(*[np.asarray(getattr(self, n))[idx] for n in PARAM_NAMES])


class Solver:
    """Batched semi-implicit integrator for one network topology."""

    def __init__(self, net: Network, dt: float = 1.0):
        self.net = net
        self.dt = dt
        n = net.n
        cap = net.cap
        self.cmem = np.where(cap, C_CAP, C_PA_UNIT * PA_UNITS_PER_NODE)
        l_pa = net.laplacian(net.pa_edges, PA_UNITS_PER_NODE * 1e3 / R_GJ_PA)  # nS
        l_cap = net.laplacian(net.cap_edges, 1.0)
        m0 = np.diag(self.cmem / dt) + l_pa
        r = np.linalg.cholesky(m0).T            # m0 = r.T @ r
        rinv = np.linalg.inv(r)
        m1p = rinv.T @ l_cap @ rinv
        lam, u = np.linalg.eigh(0.5 * (m1p + m1p.T))
        self.lam = np.clip(lam, 0.0, None)
        self.w = rinv @ u
        self.n = n

    def node_params(self, p: Params, kir_mask=None):
        """Per-node conductances, shape (S, N)."""
        cap = self.net.cap[None, :]
        gbar = np.where(cap, p.g_kir[:, None], PA_UNITS_PER_NODE * p.g_kir_pa[:, None]) / np.sqrt(K_REST)
        if kir_mask is not None:
            gbar = gbar * kir_mask
        gbg = np.where(cap, p.g_bg[:, None], PA_UNITS_PER_NODE * p.g_bg_pa[:, None])
        ebg = np.where(cap, p.e_bg[:, None], p.e_bg_pa[:, None])
        dv = np.broadcast_to(p.dv_kir[:, None], gbar.shape)
        return gbar, gbg, ebg, dv

    def run(self, p: Params, k_fn, out_fn=None, t_end=6000.0, v0=None, record=None,
            kir_mask=None, linear=None, katp_fn=None, record_every=1):
        """Integrate. k_fn(t) -> [K+]o array broadcastable to (S, N); out_fn(t) -> outward current (pA).

        linear: optional (gslope, vrest) arrays (S, N); nodes with gslope not NaN use a linear
        membrane I = gslope (V - vrest) in place of background + Kir (ablations and rivals).
        Returns final V and, if record is a list of node indices, the recorded traces.
        """
        s = p.size
        gbar, gbg, ebg, dv = self.node_params(p, kir_mask)
        c_s = 1e3 / p.r_gj                              # nS
        scale = 1.0 / (1.0 + c_s[:, None] * self.lam[None, :])
        v = np.full((s, self.n), -30.0) if v0 is None else v0.copy()
        cdt = self.cmem[None, :] / self.dt
        nsteps = int(round(t_end / self.dt))
        rec = []
        times = []
        if linear is not None:
            lin_g, lin_v = linear
            lin_mask = ~np.isnan(lin_g)
            lin_g = np.nan_to_num(lin_g)
            lin_v = np.nan_to_num(lin_v)
        for step in range(nsteps):
            t = step * self.dt
            k = k_fn(t)
            ek = e_k(k)
            ikir = gbar * np.sqrt(k) * (v - ek) / (1.0 + np.exp((v - ek - dv) / K_KIR))
            itot = gbg * (v - ebg) + ikir
            if linear is not None:
                itot = np.where(lin_mask, lin_g * (v - lin_v), itot)
            if katp_fn is not None:
                itot = itot + katp_fn(t) * (v - ek)
            if out_fn is not None:
                itot = itot + out_fn(t)
            rhs = cdt * v - itot
            x = rhs @ self.w
            x *= scale
            v = x @ self.w.T
            if record is not None and (step % record_every == 0):
                rec.append(v[:, record].copy())
                times.append(t + self.dt)
        if record is not None:
            return v, np.array(times), np.stack(rec, axis=1)
        return v

    def rest(self, p: Params, t_end=4000.0, **kw):
        """Converged resting attractor reached from a depolarized start.

        A fixed four-second burn-in is insufficient near a saddle-node. Continue
        only unconverged parameter sets until current balance implies less than
        1e-10 mV/ms drift, preserving the depolarized-start attractor rather than
        root-solving to an arbitrary (possibly unstable) equilibrium.
        """
        kk = np.full((1, self.n), K_REST)
        v = self.run(p, lambda t: kk, t_end=t_end, **kw)
        gb,gl,el,dv = self.node_params(p,kw.get('kir_mask'))
        lp=self.net.laplacian(self.net.pa_edges,PA_UNITS_PER_NODE*1e3/R_GJ_PA)
        lc=self.net.laplacian(self.net.cap_edges)
        for _ in range(20):
            current=gl*(v-el)+i_kir(v,K_REST,gb,dv)+v@lp.T+(1e3/p.r_gj[:,None])*(v@lc.T)
            rate=np.max(abs(current)/self.cmem[None,:],axis=1)
            ix=np.where(rate>1e-10)[0]
            if not len(ix):return v
            v[ix]=self.run(p.take(ix),lambda t:kk,t_end=4000.,v0=v[ix],**kw)
        raise RuntimeError(f'Resting state did not converge; maximum drift {rate.max()} mV/ms')


def site_k(n: int, sites, levels, onset=0.0, offset=np.inf):
    """[K+]o protocol: each site gets its own concentration (array (S,) or scalar) in [onset, offset)."""
    base = np.full((1, n), K_REST)

    def fn(t, _cache={}):
        if onset <= t < offset:
            key = "on"
        else:
            key = "off"
        if key not in _cache:
            if key == "off":
                _cache[key] = base
            else:
                arr = None
                for site, lev in zip(sites, levels):
                    lev = np.atleast_1d(np.asarray(lev, dtype=float))
                    if arr is None:
                        arr = np.repeat(base, lev.shape[0], axis=0)
                    arr[:, site] = lev[:, None]
                _cache[key] = arr
        return _cache[key]

    return fn
