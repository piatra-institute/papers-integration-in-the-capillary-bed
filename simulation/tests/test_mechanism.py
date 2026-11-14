import numpy as np
from capnet.network import build
from capnet.model import Solver, e_k, i_kir
from capnet.experiment import parameters, Protocol, trace, residual, flow, filter_trace


def test_nernst_and_kir_reversal():
    assert -100 < e_k(3) < -98
    assert abs(i_kir(e_k(3),3,.2,25))<1e-12
    assert i_kir(-40,10,.2,25)>0


def test_graph_conservation_and_symmetry():
    for key in ['T1','T2','T3']:
        net=build(key);lap=net.laplacian(net.cap_edges+net.pa_edges)
        assert np.max(abs(lap.sum(axis=1)))==0
        assert np.array_equal(lap,lap.T)
        assert np.linalg.eigvalsh(lap)[0]>-1e-12


def test_eigenbasis_matches_direct_linear_step():
    net=build();so=Solver(net,2);p=parameters([[.5,.04,40]])
    rng=np.random.default_rng(12);rhs=rng.normal(size=net.n)
    mat=np.diag(so.cmem/2)+net.laplacian(net.pa_edges,300)+net.laplacian(net.cap_edges,25)
    fast=((rhs@so.w)/(1+25*so.lam))@so.w.T
    assert np.max(abs(fast-np.linalg.solve(mat,rhs)))<1e-11


def test_passive_superposition_and_geometry():
    net=build();so=Solver(net,2);p=parameters([[.5,.04,40]]);v=so.rest(p)
    _,a=trace(so,p,Protocol(('tip0',),(8,)),mode='passive',rest=v)
    _,b=trace(so,p,Protocol(('tip1',),(8,)),mode='passive',rest=v)
    _,ab=trace(so,p,Protocol(('tip0','tip1'),(8,8)),mode='passive',rest=v)
    assert np.max(abs(ab-a-b))<1e-8
    assert np.max(abs(a-b))<1e-8


def test_decomposition_is_exact_and_flow_common():
    a=np.array([1.,5.,20.]);b=np.array([2.,5.,10.]);ab=np.array([3.,12.,25.])
    r=residual(a,b,ab)
    assert np.allclose(r['beyond_saturation'],flow(ab)-flow(a+b))
    assert flow(0)==1
    assert flow(1e6)==1.3**4


def test_nonlinear_filter_can_interact_but_geometry_is_invariant():
    x=np.ones(100)
    f=lambda z:filter_trace(z,[1,.3,50])
    assert np.max(f(2*x)-2*f(x))>.5
    assert np.array_equal(f(x+x),f(2*x))
