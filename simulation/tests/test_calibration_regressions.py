"""Regressions for issues found while auditing the inherited implementation."""
import numpy as np
import pytest
from capnet.experiment import Protocol, parameters, trace, connected_patch
from capnet.model import Solver
from capnet.network import build


@pytest.mark.parametrize('topology',['T1','T2','T3'])
def test_boundary_parameter_passive_superposition_after_converged_rest(topology):
    """A drifting burn-in must not masquerade as a passive interaction residual."""
    net=build(topology);solver=Solver(net,2.)
    p=parameters([.8,.02,200.]);rest=solver.rest(p)
    options=dict(mode='passive',rest=rest,record=[net.zone2])
    _,a=trace(solver,p,Protocol(('tip0',),(10.,)),**options)
    _,b=trace(solver,p,Protocol(('tip1',),(10.,),onset=200.),**options)
    _,ab=trace(solver,p,Protocol(('tip0','tip1'),(10.,10.),delay=100.),**options)
    np.testing.assert_allclose(ab,a+b,rtol=0,atol=1e-7)
    _,zero=trace(solver,p,Protocol(('tip0',),(3.,)),**options)
    np.testing.assert_allclose(zero,0.,rtol=0,atol=1e-7)


@pytest.mark.parametrize('count',[8,16])
def test_single_broad_exposure_patch_is_connected(count):
    net=build('T1');patch=set(connected_patch(net,count))
    assert len(patch)==count
    assert all(net.cap[i] for i in patch)
    assert not patch.intersection({15,16,17})
    seen={next(iter(patch))}
    while True:
        grown=seen|{b for a,b in net.cap_edges if a in seen and b in patch}|{a for a,b in net.cap_edges if b in seen and a in patch}
        if grown==seen:break
        seen=grown
    assert seen==patch
