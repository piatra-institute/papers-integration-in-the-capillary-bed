---
title: "Integration in the Capillary Bed: Paired-Input Predictions for Electrical Signaling to Arterioles"
author: "PIATRA . INSTITUTE"
date: "November 2026"
---

## Abstract

Can paired capillary inputs distinguish distributed electrical interaction from independent sensing and a shared vascular nonlinearity? We implement a literature-constrained membrane network, screen single-exposure magnitude and reversibility, and fit rivals only to isolated-input responses. Of 8192 sampled parameter vectors, 29 meet the criteria for the chosen connected exposure footprint; a smaller footprint admits none. Across 128 withheld paired protocols, a nonlinear dynamic filter fits isolated responses with 0.078 mV error but has 0.299 mV prediction error against the distributed model. The central measurement compares sibling and distant input pairs with matched single-site waveforms. The nominal geometry contrast is 0.212 mV, while any controller driven only by their identical pooled inputs predicts zero. Refitted localization ablations retain geometry effects; the nearest nominal gap is 0.107 mV. Distinguishing that gap requires per-condition mean standard error of 0.0192 mV under the stated planning assumptions. Parameter sensitivity and focal-block predictions specify the limits of this comparison. The contribution is a quantified discrimination test, not the already proposed idea of capillary summation. Unknown exposure geometry and coupling, fixed membrane assumptions, and synthetic calibration prevent these predictions from identifying the mechanism used in an intact brain.

## What a paired stimulus can establish

Stimulating separate capillary branches can produce an upstream dilation larger or smaller than the sum of their individual responses. That observation alone does not locate the interaction. Independent local sensors can feed an electrical cable, and a saturating relation between arteriolar voltage and diameter can make the resulting vascular response nonadditive. A useful test must measure the electrical response before that output transformation, compare models that explain the individual inputs, and perturb the path through which they meet.

Longden and colleagues established a potassium-sensitive capillary-to-arteriole electrical pathway and implicated endothelial Kir2.1 channels through electrophysiology, pharmacology and endothelial deletion [@longden2017]. Moshkforoush and colleagues subsequently modeled the inward-rectifier current as both sensor and amplifier. Their network simulations already produced graded responses, threshold excitation and summation of activated regions [@moshkforoush2020]. Postnov and colleagues had already analyzed negative differential conductance and bistability as mechanisms of regenerative conducted responses [@postnov2015]. The relevant question is therefore whether a specified paired-input observation separates distributed amplification from simpler fitted alternatives.

There is also direct precedent for cumulative vascular stimulation. Rivers found that conducted dilation could saturate with additional stimulation sites on one arteriole while responses accumulated across adjacent arterioles [@rivers1997]. Longden's recent framework explicitly proposes paired capillary inputs, temporal combination, current shunts and upstream voltage recordings [@longden2026]. The present contribution is a quantitative comparison attached to that experimental idea: a reproducible calibration and prediction split, an exact separation of electrical interaction from common output saturation, and model-conditioned effect sizes and precision requirements. It does not introduce capillary summation or the paired-electrode experiment.

The source evidence supports distinct routes into the electrical network. Isaacs and colleagues found that hyperpolarizing individual thin-strand pericytes could dilate an upstream arteriole and implicated pericyte ATP-sensitive potassium channels in neurovascular coupling [@isaacs2024]. Hariharan and colleagues connected pericyte KATP activation to glucose availability and upstream blood-flow control [@hariharan2022]. A potassium challenge to endothelial cells and a pericyte KATP input therefore require separate interpretation. The model below treats the former as its primary stimulus and tests an effective KATP conductance separately; it does not resolve pericyte anatomy or infer endogenous metabolic signaling from an imposed conductance.

## Electrical network and parameter provenance

Each capillary node is an endothelial cell. Each arteriolar node combines circumferential endothelial and smooth-muscle units assumed to share a voltage. The membrane balance is

$$C_i\frac{dV_i}{dt}=-I_{\mathrm{bg},i}-I_{\mathrm{Kir},i}-I_{\mathrm{KATP},i}-\sum_j g_{ij}(V_i-V_j),$$

with

$$I_{\mathrm{bg}}=G_{\mathrm{bg}}(V-E_{\mathrm{bg}}),\qquad E_K=\frac{RT}{F}\log\frac{K_o}{K_i},$$

$$I_{\mathrm{Kir}}=\frac{\overline G_{\mathrm{Kir}}\sqrt{K_o}(V-E_K)}{1+\exp[(V-E_K-\Delta V_{\mathrm{Kir}})/k_{\mathrm{Kir}}]},\qquad I_{\mathrm{KATP}}=G_{\mathrm{KATP}}(t)(V-E_K).$$

The background current summarizes omitted membrane currents. Kir rectification can supply negative differential conductance: hyperpolarization increases outward potassium current over part of the current-voltage curve, recruiting further hyperpolarization. This is the published mechanism, implemented here without additional channel trafficking, stochastic TRPV4 openings or an imposed reset [@moshkforoush2020; @postnov2015]. Active recruitment in this short network need not form a traveling hyperpolarizing front; the model comparison tests distributed voltage dependence. The model holds ionic reservoirs fixed and treats channel gating as instantaneous. Coupling is reciprocal and resistive. Sealed terminal boundaries make network load an explicit structural assumption.

Table A lists fixed membrane values. They follow the measured capacitance and published model implementation of Moshkforoush and colleagues; the source inventory provides a locator and status for every value [@moshkforoush2020]. Arteriolar conductances and capacitance are per circumferential unit, before lumping. The temperature is the published room-temperature model setting, so timing is not an identified in-vivo prediction.

| Parameter | Value | Origin |
|-----------------------------------------------|:----------------:|------------------------|
| Capillary capacitance | 8 pF | Measured mean |
| Arteriolar unit capacitance | 16 pF | Published model |
| Arteriolar junction resistance | 10 M$\Omega$ | Published model |
| Arteriolar Kir conductance | 0.65 nS | Published model |
| Arteriolar background conductance | 0.20 nS | Published model |
| Background reversal, both compartments | -30 mV | Published model |
| Kir half-inactivation offset | 25 mV | Published model |
| Kir rectification slope | 7 mV | Published model |
| Temperature | 293 K | Published model |
| Intracellular potassium | 150 mM | Published model |
| Resting extracellular potassium | 3 mM | Published bath/model |

The gas and Faraday constants are 8314 mJ mol$^{-1}$ K$^{-1}$ and 96485 C mol$^{-1}$, using the published unit convention.

The reported capillary Kir coefficient is 0.18 $\pm$ 0.10 nS/mM$^{1/2}$ and background conductance is 0.06 $\pm$ 0.04 nS [@moshkforoush2020]. The coefficient $\overline G_{\mathrm{Kir}}$ differs from the conductance parameter $G_{\mathrm{Kir}}$ used below: $G_{\mathrm{Kir}}=\overline G_{\mathrm{Kir}}\sqrt{K_{o,\mathrm{rest}}}$. The reported spreads motivate plausible magnitudes; the sampled intervals are design choices rather than population confidence limits.

The free parameters and selected nominal values are:

| Parameter | Lower | Upper | Nominal |
|--------------------------------------|:------------:|:------------:|:------------:|
| Capillary Kir (nS) | 0.2000 | 0.8000 | 0.6879 |
| Capillary background (nS) | 0.0200 | 0.1000 | 0.0493 |
| Capillary junction resistance (M$\Omega$) | 10.00 | 200.00 | 10.61 |

At the resting potassium concentration, the published Kir coefficient corresponds to a conductance of 0.312 $\pm$ 0.173 nS. The selected homogeneous Kir density is above this central value, while its coupling resistance lies near the lower sampling bound. The model therefore represents a restricted active regime rather than a typical capillary population.

The base tree contains 45 capillary cells and 15 axial arteriolar nodes. A cell step is 20 $\mu$m; the arteriolar segment is 300 $\mu$m long, with 3 circumferential units at each axial position. Each terminal input covers 2 adjacent cells. The withheld geometries add a second tree, giving 90 capillary cells, or an anastomosis, giving 48 capillary cells. All are idealized finite networks with the same membrane law.

The binary tree has 4 segment levels, with 3 cells per segment. The arteriolar readout lies 240 $\mu$m from the capillary junction; the terminal input centers are 220 $\mu$m into the capillary path. In the two-tree variant the junctions are separated by 120 $\mu$m along the arteriole. The sibling comparison uses terminals sharing their last fork; the distant comparison uses terminals in opposite halves of the same tree.

The primary model has homogeneous capillary conductances within a network; parameter uncertainty varies them across model instances. It does not represent cell-to-cell channel heterogeneity. The sampled coupling interval is a selected part of the published exploration range, because capillary junctional resistance has not been directly measured in the cited model study [@moshkforoush2020]. The geometry is generated, not reconstructed from an animal. These distinctions matter when translating a voltage prediction to a preparation.

The common output law is

$$D/D_0=1 + 0.30 \,\tanh[\max(H,0)/10],\qquad Q/Q_0=(D/D_0)^4.$$

Here $H$ is hyperpolarization in mV. The chosen fractional diameter ceiling and voltage scale are assumptions, reality-checked against the dilation scale and near-maximal dilation during hyperpolarization reported by Longden and colleagues [@longden2017]. They are fixed across mechanisms and never fitted to paired responses. The flow relation assumes fixed pressure drop, vessel length and viscosity; it is a feeding-segment flow proxy. It does not calculate flow redistribution in the capillary network.

## Single-site calibration and withheld predictions

Longden and colleagues reported 23.2 $\pm$ 1.8 mV hyperpolarization during a capillary potassium challenge [@longden2017]. We screen against an author-defined interval from 19.6 to 26.8 mV, with baseline between -45 and -25 mV. The challenge lasts 18 s. Recovery must leave less than 1 mV residual hyperpolarization 5 s after removal. The voltage interval uses twice the reported SEM; the recovery tolerance is a design criterion. This is a published-magnitude and reversibility screen, not a fit to digitized experimental traces.

We draw 8192 parameter vectors, uniformly in the conductances and uniformly in log coupling resistance, and compare connected exposure regions of 8 and 16 cells. Each receives one imposed potassium waveform. The region is a connected portion of a distal subtree, not separately controlled stimulation at multiple sites. Its correspondence to the experimental solution plume is unknown; exposure size is a structural assumption. The smaller and larger regions give the following finite-sample screen:

| Exposed cells | Magnitude accepted | Also recover |
|:----------------:|:----------------------:|:----------------:|
| 8 | 149 | 0 |
| 16 | 223 | 29 |

The primary benchmark uses the larger connected exposure and its 29 confirmed admissible vectors. We select the nominal vector closest to the published voltage mean, before computing paired responses. Many candidates match a voltage endpoint but remain hyperpolarized after stimulus removal. Exposure size cannot be inferred from this endpoint, and this experiment does not identify a unique physiological parameter set.

The selected nominal response is 22.133 mV, from a baseline of -30.740 mV. Its first 1 mV deflection occurs after 30 ms, compared with the published onset latency of 240 $\pm$ 30 ms [@longden2017]. The model responds earlier under this detection rule. Onset definitions and exposure geometry differ, leaving this discrepancy unresolved. The proposed timing offsets are conditional design values; the complete experimental single-input waveform has not been calibrated.

The model-comparison targets are explicitly synthetic: 12 isolated-site voltage traces from the selected model on the base tree, plus its broad-exposure endpoint and recovery. Each mechanistic rival refits 3 parameters within the same conductance and coupling bounds. Endpoint and recovery residuals receive weight 10 in the least-squares objective. Mechanistic fits use a common multistart schedule, and paired responses never enter any fitting objective. Successful optimization does not guarantee an equally good fit; the results below expose each rival's remaining single-site error.

The passive rival retains nonlinear dependence of the imposed potassium current on concentration, evaluated at baseline voltage, followed by linear membrane and junctional propagation. The independent-sensor oracle receives exact isolated responses, including on test topologies, and adds them with the appropriate delay. It is deliberately given more single-site information than a fitted biological model. A stronger spatial ablation leaves the distal capillary branches active while making the unstimulated common trunk and arteriole passive. It retains distributed distal interaction and is therefore a localization control, not an independent-sensor model. The compartment ablations retain nonlinear membrane currents only in the capillaries or only in the arteriole. Each is refitted before paired prediction.

The linearization ablates voltage-dependent feedback while preserving baseline current; it is distinct from channel deletion. Linearized membranes use a positive slope floor of 0.001 nS to ensure passive transit. The compact filter follows $\tau\dot y=-y+a x+b x^2$, where $x$ is the output of a fixed passive network at predeclared published-model parameters. It fits 3 coefficients: $a$, $b$ and $\tau$. It can generate an electrical interaction through its pooled nonlinear state; its capacity is not restricted to adding responses.

For the declared fitting weights, the single-site log-parameter sensitivity matrix has condition number 1627.4; the local conductance correlation is 0.993111. A local sensitivity sample retains 73 of 513 parameter vectors under the single-trace tolerance of 0.25 mV and the broad-exposure criteria. The perturbations are bounded and clipped to the prior limits. These are sensitivity sets conditional on the model, footprint, fixed constants and sampled domain, not posterior credible intervals.

The reported local sensitivity uses log-parameter step 0.00001, for which the checked perturbations retain recovery. Larger perturbations cross a switching boundary. This limits the interpretation of a local derivative and reinforces the use of explicitly sampled response sets instead of a Gaussian parameter-confidence claim.

After fitting, the test set comprises 128 paired protocols across 3 topologies. Both inputs use 500 ms pulses. The combinations vary potassium concentration, relative delay and whether the sites are siblings, belong to distant subtrees, lie on different trees or border an anastomosis. Model parameters remain fixed on the withheld topologies; post-fit singles supply residual controls and the privileged independent-sensor oracle, not new fitting targets.

## Separate electrical interaction from output saturation

Let $H_A(t)=V_0-V_A(t)$ denote the positive hyperpolarization produced by input $A$, measured against the resting voltage of that model and condition. For an input at $B$ delayed by $\delta$, align its single-input control to the same delay. Define the time-resolved electrical interaction as

$$R_V(t)=H_{AB}(t)-H_A(t)-H_B(t-\delta).$$

This compares responses at the same time. Subtracting separately timed peak amplitudes would answer a different question and could create an apparent interaction from a linear system. For independent sensors with passive propagation, the electrical residual vanishes for separate sites, regardless of nonlinear dependence of each sensor on its own input. A nonlinear shared state, including an arteriolar membrane, can produce a nonzero residual.

Write the common normalized flow transformation as $F(H)$, including its resting value. The flow interaction is

$$R_Q=F(H_{AB})-F(H_A)-F(H_B)+F(0).$$

The interaction expected from the shared output transformation alone is

$$S_Q=F(H_A+H_B)-F(H_A)-F(H_B)+F(0).$$

Their difference is exactly

$$R_Q-S_Q=F(H_{AB})-F(H_A+H_B).$$

Thus a flow residual may be large even when the electrical residual is zero. Conversely, the common transformation can compress a substantial electrical difference near maximal dilation. We report both quantities. This output contribution includes diameter saturation and the curvature introduced by the flow law; its sign need not always be negative. The subtraction does not establish where an electrical interaction occurs: that requires the compartment-specific ablations and path perturbations.

## A geometry contrast with matched single-site signals

Consider two site pairs on a symmetric tree. The sites have the same distance to the arteriole and produce identical single-site readout traces, but one pair shares more of its capillary path than the other. Let $u_{AB}(t)$ and $u_{AC}(t)$ be the sums of the corresponding single-site traces. For a compact controller with state $z$,

$$\dot z=f(z,u),\qquad y=g(z,u),$$

identical summed input functions and initial states imply identical outputs whenever the state equation has a unique solution. This remains true when $f$ and $g$ are nonlinear and when the common diameter-to-flow transformation follows the controller. Its paired geometry contrast therefore vanishes:

$$G_V(t)=H_{AB}(t)-H_{AC}(t)=0.$$

A distributed network is not restricted to this pooled input description. Its internal voltages can differ because the paths share different cells. A nonzero $G_V$ with matched singles consequently rejects the stated pooled-controller class. It does not reject every compact model: a model with branch-specific hidden states can represent geometry, and local voltage-dependent stimulus conductances can interact through an otherwise passive network. The refitted compartment ablations test spatial localization. Recurrent source loading remains an alternative that measured or clamped source voltages must address.

Equality of singles is an experimental condition to verify, not a property to assume for irregular tissue. The simulation exploits tree symmetry to establish the exact comparison. In a preparation, measured single-site waveform differences must enter the controller prediction and its uncertainty before a geometry effect is assigned to the network. The pair-minus-pair contrast also removes the common baseline and, when singles match, their subtraction terms in the electrical residual.

\clearpage

## Held-out responses and competing mechanisms

Table B compares isolated-site calibration error with prediction error against the distributed generator on the complete withheld paired set. Values are in mV. Broad error is signed endpoint error. Exact entries are supplied by construction. A rival with a poor broad-exposure fit is already distinguished by calibration and provides a weaker held-out comparison.

| Model | Single RMSE | Broad error | Paired RMSE |
|--------------------------------------|:--------------:|:--------------:|:--------------:|
| Distributed Kir | 0.000 | Exact | 0.000 |
| Passive cable | 0.491 | -2.822 | 1.014 |
| Distal-active | 0.262 | -1.841 | 0.652 |
| Capillary-linear | 0.265 | -0.006 | 0.541 |
| Arteriole-linear | 0.208 | -1.879 | 0.543 |
| Dynamic filter | 0.078 | 0.000 | 0.299 |
| Independent oracle | 0.000 | Exact | 0.303 |

The independent oracle has exact isolated responses yet can miss paired responses because it imposes additivity. The pooled dynamic filter is the stronger test of ordinary shared nonlinearity: it can create an electrical residual without a distributed state. The distal-active and arteriole-linear models retain distributed capillary dynamics, so their agreement with the full model concerns localization of the active membrane, not the existence of every distributed interaction.

For the selected base-tree sibling pair, concentration is 10 mM and delay is 250 ms. The fixed averaging window is 750 to 850 ms after trial onset. Table C reports the electrical residual $R_V$, the sibling-minus-distant residual contrast $G_V$, and normalized flow residual $R_Q$ for every model.

| Model | $R_V$ (mV) | $G_V$ (mV) | $R_Q$ |
|--------------------------------------|:----------------:|:----------------:|:----------------:|
| Distributed Kir | 0.6328 | 0.2119 | 0.0917 |
| Passive cable | 0.0000 | 0.0000 | 0.0148 |
| Distal-active | 1.2784 | 0.3241 | 0.1897 |
| Capillary-linear | 0.0191 | 0.0000 | 0.0144 |
| Arteriole-linear | 1.1654 | 0.3193 | 0.1727 |
| Dynamic filter | 0.0807 | 0.0000 | 0.0149 |
| Independent oracle | 0.0000 | 0.0000 | 0.0042 |

For this distributed response, the shared output-transform contribution is 0.0042 and the remaining contribution is 0.0874, in normalized flow units. Before rounding, these sum to the total flow residual. The flow law therefore changes the observed interaction, but it does not generate the electrical geometry contrast.

\clearpage

![Paired predictions after single-site calibration. The shaded time window is the selected scalar measurement. The heatmap varies stimulus concentration and delay; bars compare the same geometry contrast across fitted mechanisms. The sensitivity sets vary distributed-model parameters while keeping rival fits fixed.](figures/paired_predictions.pdf){width=100%}

\clearpage

The topology test also changes which paths share a feeding segment. Table D gives electrical interaction residuals at the selected concentration and delay, including pairs on distinct trees and across the added anastomosis. All fitting remains confined to the base tree; the full grid is in the recorded results file.

| Topology and pair | Distributed (mV) | Filter (mV) |
|----------------------------------------------|:---------------------:|:---------------------:|
| Base tree, distant branches | 0.4209 | 0.0807 |
| Two trees, separate origins | 0.2237 | 0.0660 |
| Loop, bridge-adjacent tips | 0.4262 | 0.0770 |

A predeclared weak-Kir, high-leak corner produces a peak single-site response of 0.0554 mV and a peak absolute paired electrical residual of 0.0136 mV. Its end-of-trial hyperpolarization is 0.000002 mV. At this response scale, an additive approximation can suffice for measurements coarser than the interaction; electrical nonlinearity alone is not a reason to require the full network model.

With the assumed effective KATP conductance of 0.10 nS per stimulated cell, the separate KATP scenario gives a single-site response of 1.105 mV, a paired response of 2.171 mV and residual -0.040 mV. This is a current-scale sensitivity test motivated by pericyte signaling [@isaacs2024; @hariharan2022]. It does not estimate a pericyte channel conductance from those experiments or identify a metabolic input pathway.

![Exact decomposition of the selected paired flow interaction into the common output transformation and the contribution remaining when electrical additivity is imposed.](figures/saturation_decomposition.pdf){width=88%}

## A measurement that could discriminate the models

The most separating candidate in the examined base-tree grid uses 10 mM potassium, 500 ms pulses and a second-input delay of 250 ms. Compare a sibling pair with an equally distant pair in opposite halves of the tree, using the same first input in both trials. The predicted arteriolar geometry contrast is 0.212 mV. The closest tested localization ablation differs by 0.107 mV; the nondistributed rivals differ by 0.212 mV. This is a finite-grid selection for the nominal fit, not a global optimum over anatomical networks or drugs.

At this same protocol and time window, the source-screen ensemble spans 0.128 to 0.271 mV, and the single-trace sensitivity set spans 0.134 to 0.280 mV. These intervals compare varying distributed parameters with fixed nominal rival fits. They neither integrate uncertainty in each rival nor establish separation over the entire physiological parameter space. The pooled-controller invariance remains exact only when its summed single-input drives are matched.

A suitable preparation would first establish stable baseline and reversible single-input responses, verify the exposure footprint, and match the isolated voltage waveforms at the selected sites. Record both the feeding arteriole and an unstimulated capillary segment while interleaving single and paired trials. Measure voltage at the stimulated regions as well: the second input can change a local source through electrical loading. If those source waveforms differ between the pair geometries, include their measured differences in the passive-transit prediction. Voltage-clamped source boundaries would provide a stricter test where technically feasible.

An idealized 90% reduction of Kir conductance in the unstimulated common trunk changes the arteriolar geometry contrast from 0.2119 to 0.2072 mV, a change of -0.0047 mV. The corresponding capillary-trunk contrasts are 0.2535 and 0.2475 mV. Each condition is re-equilibrated and has its own single-input controls. This small drug effect makes focal blockade an auxiliary localization measurement; the simulation does not establish that a real drug can selectively reproduce the imposed conductance change.

Global Kir blockade tests pathway involvement but also changes input sensing and arteriolar membrane currents. A KATP antagonist belongs in a separate pericyte-input arm, with measured or matched source hyperpolarization, because loss of input generation can mimic loss of propagation [@isaacs2024; @hariharan2022]. Neither intervention substitutes for the geometry comparison or for post-intervention singles.

For the residual geometry contrast, cancellation leaves four condition means. If each mean has independent standard error $s$, then $\operatorname{SE}(G_V)=2s$. At two-sided significance 5% and power 80%, the nominal nearest-rival gap requires $s\leq$ 0.0192 mV, equivalent to a contrast standard error of 0.0383 mV. With an assumed per-preparation standard deviation of 1 mV and independent observations, the planning calculation gives 2724 observations per condition. This noise level is an assumption, not a measured property of the proposed assay; covariance between repeated conditions must be estimated, and repeated imaging frames are not independent preparations.

Detecting the nominal drug-induced change requires per-condition mean standard error no larger than 0.000598 mV under an independent eight-mean comparison. Its nearest-rival drug gap is only 0.000027 mV, while time-step refinement changes that gap by 0.000056 mV. This pharmacological separation is below the demonstrated discretization uncertainty, so a precision requirement for choosing between those drug-response mechanisms is not defensible from this run.

Reducing the integration step from 2.0 to 0.5 ms changes the selected geometry contrast by 0.000602 mV and the nearest-rival gap by 0.000498 mV. The corresponding change in the drug geometry effect is 0.000000301 mV. The unperturbed geometry distinction is numerically resolved at the reported scale, while the physiological transfer remains conditional on the assumed membrane law and geometry.

## Where the inference stops

A model-generated paired response is a prediction of an assumed mechanism. Its discrepancy from a fitted rival measures distinguishability within the specified comparison, not predictive error against an observed paired response. Single-site agreement narrows a model family but does not independently validate its spatial mechanism. Unmeasured coupling, channel heterogeneity, membrane resetting and boundary loads remain potential sources of disagreement with tissue.

Conducted signaling also depends on the membrane through which current travels. Endothelial-tube experiments demonstrate that opening potassium channels can reduce electrical transmission by increasing membrane current loss, and detailed endothelial models describe how membrane and junctional resistance jointly control conduction [@behringer2012; @kapela2018]. These results explain why changing conductance cannot be interpreted simply as changing gain. Global channel blockade can suppress the stimulus, alter the resting state and alter propagation simultaneously. It is useful as a pathway control, but localization requires remeasured singles and a perturbation confined to an unstimulated segment.

The simulations use idealized electrical topologies and an imposed arteriolar output law. They do not solve blood redistribution through a compliant network, red-cell partition, oxygen transport, metabolic feedback or neuronal activity. The normalized flow output describes the stipulated feeding segment under fixed hydraulic conditions. The proposed experiment would test whether the predicted electrical response class exists and where its nonlinearity lies.

## Code and data availability

The reproducibility package is prepared for https://github.com/piatra-institute/papers-integration-in-the-capillary-bed and contains the Python model, dependency lock, frozen parameter inventory, source manifest, protocols, tests, recorded outputs and claim bindings. No external raw experimental dataset was analyzed. Registry records and primary-source inspection copies retain their original rights, documented in sources.md. The official model scripts used to check constants were obtained from the pinned revision listed in the source manifest, with their MIT license preserved. Data fetching is separate from the offline analysis; all randomness uses the recorded seed.

## References
