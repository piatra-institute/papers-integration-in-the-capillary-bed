# Scientific audit notes

These are author-side mathematical and scientific checks, not independent editorial certification.

## A geometry contrast immune to shared scalar saturation

Let a rival represent each input site by a fixed single-site drive waveform h_i(t), allow arbitrary internal temporal states z, and compute dz/dt = F(z, sum_i h_i(t), theta), y = G(z, sum_i h_i(t), theta). F and G may be nonlinear and may include a fixed diameter-to-flow map. If two paired protocols have identical summed drive waveforms, identical starting states, and the same parameters, uniqueness of the state equation implies identical complete output trajectories. Therefore the difference between these paired trajectories is exactly zero for this entire scalar-input rival class, irrespective of how its parameters were fitted. This is stronger than subtracting single responses through an unknown output nonlinearity.

In a symmetric single-tree network, terminal sites have equal single-site waveforms by graph symmetry. A sibling-tip pair and a pair on different higher-order branches consequently provide identical summed singleton drive waveforms to this rival, while their capillary shared paths differ. Report the geometry contrast at a preselected time/window, alongside each pair's ordinary interaction residual. Prove singleton equality numerically to solver precision; unequal amplitudes or timing would invalidate this particular invariance argument. A common scalar output map cannot create a geometry contrast when its arguments are identical.

The theorem is about rivals with the specified scalar input. It does not exclude multi-input controllers with site-specific hidden states, stimulus-dependent network admittance, or a nonlinear source whose waveform changes when another site is stimulated. It also does not identify capillary rather than arteriolar nonlinearity in a topology with multiple distinct capillary-to-arteriole contacts.

## The stronger local-sensor alternative

An additive oracle formed by summing exact singleton traces has zero electrical residual, but independently fitted nonlinear sensors coupled back through a passive cable need not. A remote input changes a sensor's local voltage and therefore its ionic current. Even voltage-independent stimulus-gated conductances can change network loading. A sensor-only Kir variant with passive unstimulated capillary membrane is therefore a useful stronger control. It should retain both stimulated sites as active for the pair, be fitted only to singles using the same objective, and be separately identified from the strictly independent-source comparator.

Capillary-only and arteriole-only Kir variants isolate the location of the nonlinearity more directly. Their free parameters should be refitted to the same singleton targets. A failure to achieve comparable singleton fit weakens any held-out error ranking; state the difference explicitly.

## Interventions and input monitoring

Focal Kir blockade on an unstimulated shared path can test whether transit membrane matters. Global barium also alters sensing and arteriolar response and does not localize the interaction. Re-measure baseline and both singleton responses after blockade; compare paired residuals within each drug condition. Monitor local voltage at input sites because a drug can alter both input generation and propagation. Behringer and Segal's endothelial tube experiments provide precedent for matching local voltage responses when comparing conduction under altered membrane conductance.

A particularly stringent conceptual test clamps or directly measures both source voltage trajectories. A cable with fixed linear membrane properties and those source boundary trajectories predicts the remaining voltage field linearly, even if the sources were generated nonlinearly. A residual in an unstimulated path after accounting for measured boundary waveforms more directly rejects passive transit. Dual voltage clamp in capillaries may be technically demanding, so this is a conditional design criterion rather than a claimed routine assay.

## Precision and uncertainty

For D = V_AB - V_A - V_B + V_0 with four independent condition means, each based on n independent preparations with per-preparation standard deviation sigma, SE(D) = 2 sigma/sqrt(n). A geometry contrast with a common first input and common baseline is V_AB - V_AC - V_B + V_C, so it also has four terms. A geometry contrast between disjoint pairs with a common baseline has six terms, and a drug difference between independently measured residuals has eight. Paired covariance may lower or raise these uncertainties and must be measured. Repeated imaging frames do not substitute for independent preparations.

Broad published endpoint windows, even windows chosen as twice a reported SEM, are calibration admissibility envelopes rather than a likelihood for these idealized networks. An accepted parameter ensemble gives a sensitivity range conditional on its sampling law, bounds, topology, and endpoint choices. It is not a posterior credible interval or a confidence interval on intact-brain behavior. Report the retained sample size and all acceptance criteria, including any selection on interaction, to avoid a self-fulfilling ensemble.

## Inherited-code checks

The inherited current units are consistent: pF times mV/ms and nS times mV are both pA; 1000/R in MOhm converts to nS. The implicit coupling eigenbasis is algebraically consistent with inversion of diag(C/dt) + L_PA + g_cap L_cap. Test this against a direct solve, verify a constant voltage is in the Laplacian nullspace, demonstrate passive superposition, and establish time-step convergence near the regime giving the largest interaction. The inherited temperature of 293 K is an ex vivo room-temperature setting, not an intact-brain temperature.
