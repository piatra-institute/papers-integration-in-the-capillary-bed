"""Finite sensitivity experiment for an imposed slow channel-reset mechanism.

Moshkforoush et al. 2020, Methods, Modulation of Kir and TRPV4 Currents by
PIP2, describes exponential Kir suppression and reciprocal TRPV4 recruitment
on minute time scales. Harraz et al. 2018 establishes reciprocal modulation,
not a quantitative potassium-triggered feedback law. The coactivated receptor
drive, ohmic TRPV4 surrogate, rates and spatial scope below are assumptions.
"""
from dataclasses import asdict
from itertools import product

import numpy as np

from capnet.experiment import Protocol, SlowReset, connected_patch, parameters, trace
from capnet.model import Solver
from capnet.network import build


def _features(t, h):
    return np.column_stack((h[:, (t > 17900) & (t <= 18000), 0].mean(axis=1),
                            h[:, (t > 22900), 0].mean(axis=1)))


def _summarize(features, rest):
    baseline = (rest >= -45.) & (rest <= -25.)
    amplitude = (features[:, 0] >= 19.6) & (features[:, 0] <= 26.8)
    recovery = abs(features[:, 1]) < 1.
    return {
        'n': len(features),
        'amplitude_and_baseline_pass': int((amplitude & baseline).sum()),
        'recovery_pass': int(recovery.sum()),
        'all_criteria_pass': int((baseline & amplitude & recovery).sum()),
        'persistent_hyperpolarization_after_5s': int((features[:, 1] >= 1.).sum()),
        'endpoint_mv_min': float(features[:, 0].min()),
        'endpoint_mv_max': float(features[:, 0].max()),
        'absolute_recovery_mv_max': float(abs(features[:, 1]).max()),
        'endpoint_and_recovery_mv': features.tolist(),
    }


def run_resetting_study(nominal):
    """Evaluate fixed grids; no parameters are fitted to make resetting work."""
    net = build('T1')
    net.sites['broad'] = connected_patch(net, 16)
    solver = Solver(net, 2.)
    measured_bounds = np.array([.18-.10, .18+.10])*np.sqrt(3.)
    axes = [np.linspace(*measured_bounds, 5), np.linspace(.02, .10, 5),
            np.geomspace(10., 200., 5)]
    grid = np.array(list(product(*axes)))
    # The same +/-0.5% changes expose the unadapted nominal switching boundary.
    perturbations = [np.array(nominal, dtype=float)]
    labels = ['nominal']
    for j, name in enumerate(('g_kir', 'g_bg', 'r_gj')):
        for direction in (-1, 1):
            x = np.array(nominal, dtype=float)
            x[j] *= np.exp(direction * .005)
            perturbations.append(x)
            labels.append(name + ('_minus' if direction < 0 else '_plus'))
    x = np.vstack((grid, perturbations))
    p = parameters(x)
    rest = solver.rest(p)
    protocol = Protocol(('broad',), (10.,), onset=0., duration=18000., end=23000.)
    scenarios = [('no_reset', None)]
    # Harraz Fig.6 reports PGE2 modulation at 6.4 min (Kir) and 4.9 min
    # (TRPV4). Applying those rates here is a transfer assumption; the 1 min
    # arm probes faster unmeasured modulation. Neither is a K-only kinetic fit.
    for tau, trpv4_tau in ((60000., 60000.), (384000., 294000.)):
        for conductance in (0., .02, .08):
            scenarios.append((f'all_tau{int(tau)}_g{conductance}',
                              SlowReset(depletion_tau_ms=tau, trpv4_depletion_tau_ms=trpv4_tau,
                                        trpv4_max_ns=conductance)))
        scenarios.append((f'patch_tau{int(tau)}_g0.02',
                          SlowReset(depletion_tau_ms=tau, trpv4_depletion_tau_ms=trpv4_tau,
                                    trpv4_max_ns=.02,
                                    scope='exposed_patch')))
    rows = []
    for label, reset in scenarios:
        t, h = trace(solver, p, protocol, rest=rest, record=[net.zone2],
                     dt_record=10., slow_reset=reset)
        features = _features(t, h)
        row = {'label': label, 'reset': asdict(reset) if reset else None,
               'measured_conductance_grid': _summarize(features[:len(grid)], rest[:len(grid), net.zone2]),
               'nominal_perturbations': _summarize(features[len(grid):], rest[len(grid):, net.zone2])}
        rows.append(row)
        print('Slow-reset sensitivity', label,
              row['measured_conductance_grid']['all_criteria_pass'],
              row['nominal_perturbations']['all_criteria_pass'], flush=True)
    # Check both an amplitude-suppressing arm and the arm that could restore
    # recovery near the nominal switching boundary.
    fine_solver = Solver(net, .5)
    fine_p = parameters(np.array(perturbations))
    fine_rest = fine_solver.rest(fine_p)
    numerical_checks = []
    for label in ('all_tau60000_g0.02', 'all_tau384000_g0.0'):
        check_reset = next(reset for name, reset in scenarios if name == label)
        coarse = next(row for row in rows if row['label'] == label)
        ft, fh = trace(fine_solver, fine_p, protocol, rest=fine_rest, record=[net.zone2],
                       dt_record=10., slow_reset=check_reset)
        fine_features = _features(ft, fh)
        coarse_features = np.array(coarse['nominal_perturbations']['endpoint_and_recovery_mv'])
        numerical_checks.append({
            'scenario': label, 'dt_coarse_ms': 2., 'dt_fine_ms': .5,
            'maximum_endpoint_change_mv': float(abs(fine_features[:, 0]-coarse_features[:, 0]).max()),
            'maximum_recovery_change_mv': float(abs(fine_features[:, 1]-coarse_features[:, 1]).max()),
            'fine_nominal_perturbations': _summarize(fine_features, fine_rest[:, net.zone2]),
        })
    return {
        'mechanism': 'Imposed receptor-associated exponential Kir suppression and complementary ohmic depolarizing conductance; no identified potassium-to-PIP2 feedback law.',
        'source_citation_ids': ['moshkforoush2020', 'harraz2018'],
        'assumptions': 'Receptor drive coincides with potassium exposure. Modulation recovers exponentially after removal. Rates, maximum depolarizing conductance, reversal, and spatial scope are design sensitivities, not fitted physiological values. Arteriolar membranes are unchanged.',
        'temperature_k': 293.,
        'published_pge2_modulation_tau_ms': {'kir': 384000., 'trpv4': 294000.},
        'faster_assumed_modulation_tau_ms': 60000.,
        'assumed_recovery_tau_ms': 180000.,
        'grid_parameters': grid.tolist(),
        'grid_axes': [axis.tolist() for axis in axes],
        'measured_kir_bounds_ns': measured_bounds.tolist(),
        'grid_count': len(grid),
        'scenario_count': len(scenarios),
        'adaptation_scenario_count': len(scenarios)-1,
        'nominal_perturbation_labels': labels,
        'nominal_perturbation_parameters': np.array(perturbations).tolist(),
        'nominal_log_perturbation': .005,
        'duration_ms': protocol.duration,
        'recovery_observation_ms': protocol.end-protocol.duration,
        'rows': rows,
        'any_adapted_measured_grid_pass': any(row['measured_conductance_grid']['all_criteria_pass'] for row in rows[1:]),
        'adapted_measured_grid_pass_total': sum(row['measured_conductance_grid']['all_criteria_pass'] for row in rows[1:]),
        'numerical_checks': numerical_checks,
    }
