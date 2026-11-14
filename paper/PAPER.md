---
title: "Integration in the Capillary Bed: Paired-Input Predictions for Electrical Signaling to Arterioles"
author: "PIATRA . INSTITUTE"
date: "November 2026"
---

## Abstract

Can paired capillary inputs distinguish distributed electrical interaction from independent sensing and a shared vascular nonlinearity? We implement a literature-constrained membrane network, screen single-exposure magnitude and recovery, fit rivals to isolated-input responses, and compare 128 withheld paired protocols. The central measurement contrasts sibling and distant input pairs with matched single-site waveforms. Uniqueness of a deterministic controller driven by their identical pooled inputs forces its geometry contrast to zero, irrespective of shared output saturation. The nominal distributed model predicts a 0.833 mV contrast under simultaneous stimulation; a conditional planning calculation gives 46 independent observations per condition. Concentration sweeps reveal a nearby sign reversal, while a bounded pooled filter fits poorly and localization ablations retain geometry effects. Only 29 of 8192 sampled vectors pass the initial screen, all above the reported mean-plus-or-minus-SD Kir conductance band. Slow Kir suppression improves recovery near the nominal point but yields no full-screen passes on the tested conductance-band grid. The contribution is an invariant null and a quantified synthetic discrimination design. Its physiological application requires measured source waveforms, preparation-specific timing and a reversible membrane regime compatible with the observed conductances.

## What a paired stimulus can establish

Stimulating separate capillary branches can produce an upstream dilation larger or smaller than the sum of their individual responses. That observation alone does not locate the interaction. Independent local sensors can feed an electrical cable, and a saturating relation between arteriolar voltage and diameter can make the resulting vascular response nonadditive. A useful test must measure the electrical response before that output transformation, compare models that explain the individual inputs, and perturb the path through which they meet.

Longden and colleagues established a potassium-sensitive capillary-to-arteriole electrical pathway and implicated endothelial Kir2.1 channels through electrophysiology, pharmacology and endothelial deletion [@longden2017]. Moshkforoush and colleagues subsequently modeled the inward-rectifier current as both sensor and amplifier. Their network simulations already produced graded responses, threshold excitation and summation of activated regions [@moshkforoush2020]. Postnov and colleagues had already analyzed negative differential conductance and bistability as mechanisms of regenerative conducted responses [@postnov2015]. The relevant question is therefore whether a specified paired-input observation separates distributed amplification from simpler fitted alternatives.

The broader precedent is spatial cable integration [@rall1967]. Wessel and colleagues demonstrated Kir-dependent supralinear summation of paired excitatory inputs in leech and reproduced it with Kir as the only voltage-dependent conductance [@wessel1999]. Their depolarizing inputs deactivate Kir; the capillary mechanism recruits it during hyperpolarization. The matched-single comparison developed here specifies an invariant null for controllers that receive only the summed input waveform.

There is also direct precedent for cumulative vascular stimulation. Rivers found that conducted dilation could saturate with additional stimulation sites on one arteriole while responses accumulated across adjacent arterioles [@rivers1997]. Longden's recent framework explicitly proposes paired capillary inputs, temporal combination, current shunts and upstream voltage recordings [@longden2026]. The present contribution attaches a reproducible calibration and prediction split, an exact separation of electrical interaction from common output saturation, and model-conditioned effect sizes and precision requirements to that experimental idea.

The source evidence supports distinct routes into the electrical network. Isaacs and colleagues found that hyperpolarizing individual thin-strand pericytes could dilate an upstream arteriole and implicated pericyte ATP-sensitive potassium channels in neurovascular coupling [@isaacs2024]. Hariharan and colleagues connected pericyte KATP activation to glucose availability and upstream blood-flow control [@hariharan2022]. A potassium challenge to endothelial cells and a pericyte KATP input therefore require separate interpretation. The model below treats the former as its primary stimulus and tests an effective KATP conductance separately; it does not resolve pericyte anatomy or infer endogenous metabolic signaling from an imposed conductance.

## Electrical network and parameter provenance

Each capillary node is an endothelial cell. Each arteriolar node combines circumferential endothelial and smooth-muscle units assumed to share a voltage. The membrane balance is

$$C_i\frac{dV_i}{dt}=-I_{\mathrm{bg},i}-I_{\mathrm{Kir},i}-I_{\mathrm{KATP},i}-\sum_j g_{ij}(V_i-V_j),$$

with

$$I_{\mathrm{bg}}=G_{\mathrm{bg}}(V-E_{\mathrm{bg}}),\qquad E_K=\frac{RT}{F}\log\frac{K_o}{K_i},$$

$$I_{\mathrm{Kir}}=\frac{\overline G_{\mathrm{Kir}}\sqrt{K_o}(V-E_K)}{1+\exp[(V-E_K-\Delta V_{\mathrm{Kir}})/k_{\mathrm{Kir}}]},\qquad I_{\mathrm{KATP}}=G_{\mathrm{KATP}}(t)(V-E_K).$$

The background current summarizes omitted membrane currents. Kir rectification can supply negative differential conductance: hyperpolarization increases outward potassium current over part of the current-voltage curve, recruiting further hyperpolarization. The primary benchmark implements this published membrane mechanism with fixed channel availability [@moshkforoush2020; @postnov2015]. A separate sensitivity experiment below adds slow Kir loss and a depolarizing reset conductance. Active recruitment in this short network need not form a traveling hyperpolarizing front; the model comparison tests distributed voltage dependence. The model holds ionic reservoirs fixed and treats channel gating as instantaneous. Coupling is reciprocal and resistive. Sealed terminal boundaries make network load an explicit structural assumption.

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

The reported capillary Kir coefficient is 0.18 $\pm$ 0.10 nS/mM$^{1/2}$ and background conductance is 0.06 $\pm$ 0.04 nS [@moshkforoush2020]. The coefficient $\overline G_{\mathrm{Kir}}$ differs from the conductance parameter $G_{\mathrm{Kir}}$ used below: $G_{\mathrm{Kir}}=\overline G_{\mathrm{Kir}}\sqrt{K_{o,\mathrm{rest}}}$. The reported spreads motivate the magnitudes of the author-selected sampling intervals.

The free parameters and selected nominal values are:

| Parameter | Lower | Upper | Nominal |
|--------------------------------------|:------------:|:------------:|:------------:|
| Capillary Kir (nS) | 0.2000 | 0.8000 | 0.6879 |
| Capillary background (nS) | 0.0200 | 0.1000 | 0.0493 |
| Capillary junction resistance (M$\Omega$) | 10.00 | 200.00 | 10.61 |

At the resting potassium concentration, the published Kir coefficient corresponds to a conductance of 0.312 $\pm$ 0.173 nS. Of the 29 accepted vectors, 0 lie within the corresponding mean-plus-or-minus-SD band of 0.139 to 0.485 nS; their conductances span 0.530 to 0.786 nS. The selected homogeneous Kir density and near-lower-bound coupling resistance define a restricted active regime above that descriptive band.

The base tree contains 45 capillary cells and 15 axial arteriolar nodes. A cell step is 20 $\mu$m; the arteriolar segment is 300 $\mu$m long, with 3 circumferential units at each axial position. Each terminal input covers 2 adjacent cells. The withheld geometries add a second tree, giving 90 capillary cells, or an anastomosis, giving 48 capillary cells. All are idealized finite networks with the same membrane law.

The binary tree has 4 segment levels, with 3 cells per segment. The arteriolar readout lies 240 $\mu$m from the capillary junction; the terminal input centers are 220 $\mu$m into the capillary path. In the two-tree variant the junctions are separated by 120 $\mu$m along the arteriole. The sibling comparison uses terminals sharing their last fork; the distant comparison uses terminals in opposite halves of the same tree.

The primary model has homogeneous capillary conductances within a network; parameter uncertainty varies them across model instances. It does not represent cell-to-cell channel heterogeneity. The sampled coupling interval is a selected part of the published exploration range, because capillary junctional resistance has not been directly measured in the cited model study [@moshkforoush2020]. The generated geometry and homogeneous membrane law define the population of model instances to which the predictions apply.

The common output law is

$$D/D_0=1 + 0.30 \,\tanh[\max(H,0)/10],\qquad Q/Q_0=(D/D_0)^4.$$

Here $H$ is hyperpolarization in mV. The chosen fractional diameter ceiling and voltage scale are assumptions, reality-checked against the dilation scale and near-maximal dilation during hyperpolarization reported by Longden and colleagues [@longden2017]. They are fixed across mechanisms and never fitted to paired responses. The flow relation assumes fixed pressure drop, vessel length and viscosity; it is a feeding-segment flow proxy. It does not calculate flow redistribution in the capillary network.

## Single-site calibration and withheld predictions

Longden and colleagues reported 23.2 $\pm$ 1.8 mV hyperpolarization during a capillary potassium challenge [@longden2017]. We screen against an author-defined interval from 19.6 to 26.8 mV, with baseline between -45 and -25 mV. The challenge lasts 18 s. Recovery must leave less than 1 mV residual hyperpolarization 5 s after removal. The voltage interval uses twice the reported SEM; the recovery tolerance is a design criterion. This screen constrains the model with a published magnitude and an assumed recovery criterion.

We draw 8192 parameter vectors, uniformly in the conductances and uniformly in log coupling resistance, and compare connected exposure regions of 8 and 16 cells. Each receives one imposed potassium waveform. The imposed waveform covers one connected portion of a distal subtree. Its correspondence to the experimental solution plume is unknown; exposure size is a structural assumption. The smaller and larger regions give the following finite-sample screen:

| Exposed cells | Magnitude accepted | Also recover |
|:----------------:|:----------------------:|:----------------:|
| 8 | 149 | 0 |
| 16 | 223 | 29 |

The primary benchmark uses the larger connected exposure and its 29 confirmed admissible vectors. We select the nominal vector closest to the published voltage mean, before computing paired responses. Many candidates match a voltage endpoint but remain hyperpolarized after stimulus removal. Exposure size cannot be inferred from this endpoint, and this experiment does not identify a unique physiological parameter set.

The selected nominal response is 22.133 mV, from a baseline of -30.740 mV. Its first 1 mV deflection occurs after 30 ms, compared with the published onset latency of 240 $\pm$ 30 ms [@longden2017]. This unresolved onset discrepancy prevents transferring the simulated measurement window directly to a preparation. Experimental trials should use simultaneous stimuli and a response-aligned window chosen from independent single-input recordings before paired trials are collected.

The model-comparison targets are explicitly synthetic: 12 isolated-site voltage traces from the selected model on the base tree, plus its broad-exposure endpoint and recovery. Each mechanistic rival refits 3 parameters within the same conductance and coupling bounds. Endpoint and recovery residuals receive weight 10 in the least-squares objective. Mechanistic fits use a common multistart schedule, and paired responses never enter any fitting objective. Successful optimization does not guarantee an equally good fit; the results below expose each rival's remaining single-site error.

The passive rival retains nonlinear dependence of the imposed potassium current on concentration, evaluated at baseline voltage, followed by linear membrane and junctional propagation. The independent-sensor oracle receives exact isolated responses, including on test topologies, and adds them with the appropriate delay. It is deliberately given more single-site information than a fitted biological model. A spatial ablation leaves the distal capillary branches and anastomosis bridge active while making the unstimulated common trunk and arteriole passive. It tests localization while retaining distributed distal interaction. The compartment ablations retain nonlinear membrane currents only in the capillaries or only in the arteriole. Each is refitted before paired prediction.

The linearization ablates voltage-dependent feedback while preserving baseline current; it is distinct from channel deletion. Linearized membranes use a positive slope floor of 0.001 nS to ensure passive transit. The pooled filter follows $\tau\dot y=-y+a\tanh(x/s)$, where $x$ is the output of the single-site-fitted passive cable, frozen before filter fitting. It fits 3 additional coefficients: $a$, $s$ and $\tau$, on top of the driver parameters. Its time constant is constrained to at least 10 ms, the recording interval. Bounded saturation and a resolved temporal state make this a test of shared nonlinear dynamics; it has more fitted parameters than each mechanistic model.

For the declared fitting weights, the single-site log-parameter sensitivity matrix has condition number 1627.4; the local conductance correlation is 0.993111. Of 513 bounded local perturbations, 503 meet the single-trace RMSE tolerance of 0.25 mV. Among those matches, 241 remain hyperpolarized 5 s after the broad exposure ends, 189 recover but fall below its amplitude criterion, and 73 pass both broad-exposure criteria. These counts expose a nearby persistent-response regime that isolated traces scarcely constrain. The sets describe sensitivity conditional on the model, footprint, fixed constants and sampled domain.

The reported local sensitivity uses log-parameter step 0.00001, for which the checked perturbations retain recovery. Larger perturbations cross a switching boundary. This derivative describes a narrow neighborhood of the selected reversible solution; the sampled response sets expose the nearby persistent-hyperpolarization regime.

PIP2 depletion can shift capillary channels toward depolarizing TRPV4 activity and away from hyperpolarizing Kir activity [@harraz2018]. We test an imposed receptor drive coincident with the potassium exposure. During this drive, Kir availability falls exponentially and a complementary ohmic depolarizing conductance rises; both modulations decay exponentially after exposure. The published pharmacological time constants are 384 s for Kir suppression and 294 s for TRPV4 recruitment. We also test an assumed 60 s recruitment timescale, assume 180 s recovery, vary maximal depolarizing conductance, and compare modulation throughout the capillaries with modulation confined to the exposure patch. These are transfers and sensitivity assumptions for the reduced model; the source experiment does not identify a potassium-triggered reset law.

The measured-band grid contains 125 combinations of Kir, background conductance and coupling resistance. It yields 0 full-screen passes across 8 adaptation scenarios. At the higher-conductance nominal point, Kir suppression at the source-reported timescale without the added depolarizing conductance allows all 7 tested vectors to pass, compared with 5 under fixed availability. These vectors comprise the nominal point and log-parameter steps of 0.005 in either direction along each parameter. Refining the successful arm changes its endpoint by at most 0.000103 mV and preserves all passes. Slow suppression therefore relieves the local recovery fragility in this test, while the tested conductance-band grid still fails the joint magnitude-and-recovery screen.

After fitting, the test set comprises 128 paired protocols across 3 topologies. Both inputs use 500 ms pulses. The combinations vary potassium concentration, relative delay and whether the sites are siblings, belong to distant subtrees, lie on different trees or border an anastomosis. Model parameters remain fixed on the withheld topologies; post-fit singles supply residual controls and the privileged independent-sensor oracle.

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

The experimental comparison requires measured equality of the single-input waveforms. The simulation exploits tree symmetry to establish the exact comparison. In a preparation, measured single-site waveform differences must enter the controller prediction and its uncertainty before a geometry effect is assigned to the network. The pair-minus-pair contrast also removes the common baseline and, when singles match, their subtraction terms in the electrical residual.

\clearpage

## Held-out responses and competing mechanisms

Table B compares isolated-site calibration error with prediction error against the distributed generator on the complete withheld paired set. Values are in mV. Broad error is signed endpoint error. Exact entries are supplied by construction. A rival with a poor broad-exposure fit is already distinguished by calibration and provides a weaker held-out comparison.

| Model | Single RMSE | Broad error | Paired RMSE |
|--------------------------------------|:--------------:|:--------------:|:--------------:|
| Distributed Kir | 0.000 | Exact | 0.000 |
| Passive cable | 0.491 | -2.822 | 1.014 |
| Distal-active | 0.262 | -1.841 | 0.659 |
| Capillary-linear | 0.265 | -0.006 | 0.541 |
| Arteriole-linear | 0.208 | -1.879 | 0.543 |
| Sigmoidal filter | 0.575 | -0.063 | 1.149 |
| Independent oracle | 0.000 | Exact | 0.303 |

The independent oracle has exact isolated responses yet can miss paired responses because it imposes additivity. The pooled sigmoidal filter tests a bounded shared nonlinearity with a resolved temporal state. The distal-active and arteriole-linear models test localization within the class of distributed capillary mechanisms. Their remaining single-site errors are reported alongside paired predictions; they do not set the primary discrimination target.

The sequentially fitted sigmoidal controller has single-site RMSE 0.575 mV and paired RMSE 1.149 mV. Its time constant reaches the 10 ms lower bound and its output ceiling reaches the 100 mV upper bound, leaving weak saturation over the fitted input range. This particular bounded architecture fits worse than the passive cable on isolated traces. The invariant pooled-input null applies to the broader class, irrespective of this fit quality.

For the selected base-tree sibling pair, concentration is 10 mM and delay is 0 ms. The fixed averaging window is 500 to 600 ms after trial onset. Table C reports the electrical residual $R_V$, the sibling-minus-distant residual contrast $G_V$, and normalized flow residual $R_Q$ for every model.

| Model | $R_V$ (mV) | $G_V$ (mV) | $R_Q$ |
|--------------------------------------|:----------------:|:----------------:|:----------------:|
| Distributed Kir | 1.9985 | 0.8333 | 0.2994 |
| Passive cable | 0.0000 | 0.0000 | 0.0159 |
| Distal-active | 2.9621 | 0.8006 | 0.4195 |
| Capillary-linear | 0.0249 | 0.0000 | 0.0223 |
| Arteriole-linear | 2.7801 | 0.8477 | 0.4005 |
| Sigmoidal filter | -0.0010 | 0.0000 | 0.0189 |
| Independent oracle | 0.0000 | 0.0000 | 0.0173 |

For this distributed response, the shared output-transform contribution is 0.0173 and the remaining contribution is 0.2821, in normalized flow units. Before rounding, these sum to the total flow residual. The flow law therefore changes the observed interaction, but it does not generate the electrical geometry contrast.

![Paired predictions after single-site calibration. The shaded time window is the selected scalar measurement. The heatmap varies stimulus concentration and delay; bars compare the same geometry contrast across fitted mechanisms. The sensitivity sets vary distributed-model parameters against the invariant pooled-controller prediction of zero.](figures/paired_predictions.pdf){width=100%}

\clearpage

The topology test also changes which paths share a feeding segment. Table D gives electrical interaction residuals at the selected concentration and delay, including pairs on distinct trees and across the added anastomosis. All fitting remains confined to the base tree; the full grid is in the recorded results file.

| Topology and pair | Distributed (mV) | Filter (mV) |
|----------------------------------------------|:---------------------:|:---------------------:|
| Base tree, distant branches | 1.1652 | -0.0010 |
| Two trees, separate origins | 0.4755 | -0.0011 |
| Loop, bridge-adjacent tips | 1.3012 | -0.0010 |

A predeclared weak-Kir, high-leak corner produces a peak single-site response of 0.0554 mV and a peak absolute paired electrical residual of 0.0136 mV. Its end-of-trial hyperpolarization is 0.000002 mV. At this response scale, an additive approximation can suffice for measurements coarser than the interaction; electrical nonlinearity alone is not a reason to require the full network model.

With the assumed effective KATP conductance of 0.10 nS per stimulated cell, the separate KATP scenario gives a single-site response of 1.105 mV, a paired response of 2.171 mV and residual $-0.040$ mV. This is a current-scale sensitivity test motivated by pericyte signaling [@isaacs2024; @hariharan2022]. It does not estimate a pericyte channel conductance from those experiments or identify a metabolic input pathway.

![Exact decomposition of the selected paired flow interaction into the common output transformation and the contribution remaining when electrical additivity is imposed.](figures/saturation_decomposition.pdf){width=88%}

## A measurement that could discriminate the models

Against the pooled-input null, the most separating candidate in the declared base-tree grid uses 10 mM potassium, 500 ms pulses and simultaneous inputs, with 0 ms delay. Compare a sibling pair with an equally distant pair in opposite halves of the tree, using the same first input in both trials. The nominal arteriolar geometry contrast is 0.833 mV. The distal-active and arteriole-linear controls retain distributed capillary dynamics and already have appreciable broad-exposure calibration error, so their small pairwise differences do not determine the design or its precision target.

At this protocol and the simulated averaging window, the source-screen ensemble spans 0.494 to 0.983 mV, and the single-trace sensitivity set spans 0.572 to 0.968 mV. The comparison is with the pooled-controller invariant zero, so uncertainty in that controller's parameters cannot widen the null when its input functions match. These finite sampled envelopes quantify sensitivity against the invariant null; discriminating among distributed localization variants remains a separate estimation problem.

The contrast changes sign as concentration rises. With simultaneous input it is -0.0649 mV at 12 mM, with a sampled zero-crossing bracket of 11.80 to 11.85 mM. With 250 ms delay the bracket is 12.05 to 12.10 mM. Both brackets retain opposite endpoint signs under time-step refinement. Over the sampled 9.0 to 10.5 mM band, the simultaneous contrast stays positive and spans 0.463 to 0.835 mV. At higher concentration, stimulated cells move from negative to positive Kir differential conductance, with greater current loss in the sibling geometry. This operating-point change is consistent with source shunting overcoming the shared-path advantage; it limits concentration tolerance of the proposed comparison.

![Concentration sensitivity of the nominal geometry contrast. Shaded narrow bands mark sampled zero-crossing brackets; the wider band marks the examined positive operating interval. The curves use each protocol's simulated averaging window.](figures/concentration_boundary.pdf){width=88%}

\clearpage

A suitable preparation would first establish stable baseline and reversible single-input responses, verify the exposure footprint, and match the isolated voltage waveforms at the selected sites. Choose pulse duration and a common averaging window from a separate set of single-input recordings, aligning the window to the observed onset and relaxation. Freeze those choices before interleaving single and simultaneous paired trials. The simulation window supplies a reproducible model summary; the preparation-specific window requires its own effect-size estimate. Record both the feeding arteriole and an unstimulated capillary segment. Measure voltage at the stimulated regions as well: the second input can change a local source through electrical loading. If those source waveforms differ between the pair geometries, include their measured differences in the passive-transit prediction. Voltage-clamped source boundaries would provide a stricter test where technically feasible.

An idealized 90% reduction of Kir conductance in the unstimulated common trunk changes the arteriolar geometry contrast from 0.8333 to 0.8259 mV, a change of -0.0074 mV. The corresponding capillary-trunk contrasts are 1.2409 and 1.2320 mV. Each condition is re-equilibrated and has its own single-input controls. This small drug effect makes focal blockade an auxiliary localization measurement; the simulation does not establish that a real drug can selectively reproduce the imposed conductance change.

Global Kir blockade tests pathway involvement but also changes input sensing and arteriolar membrane currents. A KATP antagonist belongs in a separate pericyte-input arm, with measured or matched source hyperpolarization, because loss of input generation can mimic loss of propagation [@isaacs2024; @hariharan2022]. Neither intervention substitutes for the geometry comparison or for post-intervention singles.

For measured singleton controls, the common first input cancels, leaving $H_{AB}-H_{AC}-H_B+H_C$. If these four condition means have independent standard error $s$, then $\operatorname{SE}(G_V)=2s$. At two-sided significance 5% and power 80%, the nominal gap from the pooled zero requires $s\leq$ 0.1487 mV, equivalent to a contrast standard error of 0.2974 mV. Assuming a per-preparation standard deviation of 1 mV gives 46 observations per condition. Using the smallest sampled source-screen and single-trace effects instead gives 129 and 96 observations per condition. These calculations concern the simulated window and assumed noise; a response-aligned assay requires pilot estimates of its effect and covariance. Repeated imaging frames are not independent preparations.

Detecting the nominal drug-induced change requires per-condition mean standard error no larger than 0.000928 mV under an independent eight-mean comparison. Time-step refinement changes this drug effect by 0.000020 mV. The effect is numerically resolved but small relative to the unperturbed geometry contrast; it supplies an auxiliary measurement whose power must be assessed in the preparation.

Reducing the integration step from 2.0 to 0.5 ms changes the selected geometry contrast by 0.001994 mV and the gap from the pooled zero by 0.001994 mV. The corresponding change in the drug geometry effect is 0.000019839 mV. The unperturbed geometry distinction is numerically resolved at the reported scale, while the physiological transfer remains conditional on the assumed membrane law and geometry.

## Where the inference stops

A model-generated paired response is a prediction of an assumed mechanism. Its discrepancy from a fitted rival measures distinguishability within this synthetic comparison. Single-site agreement narrows a model family but does not independently validate its spatial mechanism. Unmeasured coupling, channel heterogeneity, membrane resetting and boundary loads remain potential sources of disagreement with tissue.

Crane and colleagues measured conducted hyperpolarization exceeding passive predictions in arterioles [@crane2004]. Vascular models identify cell arrangement and coupling as determinants of transmission and temporal filtering [@diep2005]. Nonlinear membrane dynamics can still yield an exponential spatial profile [@hald2012]. Opening membrane channels can dissipate signals despite intact junctions [@segal2015].

Conducted signaling also depends on the membrane through which current travels. Endothelial-tube experiments demonstrate that opening potassium channels can reduce electrical transmission by increasing membrane current loss, and detailed endothelial models describe how membrane and junctional resistance jointly control conduction [@behringer2012; @kapela2018]. These results explain why changing conductance cannot be interpreted simply as changing gain. Global channel blockade can suppress the stimulus, alter the resting state and alter propagation simultaneously. It is useful as a pathway control, but localization requires remeasured singles and a perturbation confined to an unstimulated segment.

The simulations use idealized electrical topologies and an imposed arteriolar output law. They do not solve blood redistribution through a compliant network, red-cell partition, oxygen transport, metabolic feedback or neuronal activity. The normalized flow output describes the stipulated feeding segment under fixed hydraulic conditions. The proposed experiment would test whether the predicted electrical response class exists and where its nonlinearity lies.

## Code and data availability

The repository, https://github.com/piatra-institute/papers-integration-in-the-capillary-bed, contains the Python model, dependency lock, frozen parameter inventory, source manifest, protocols, tests, recorded outputs and claim bindings. No external raw experimental dataset was analyzed. Registry records and primary-source inspection copies retain their original rights, documented in sources.md. The official Moshkforoush model scripts used to check constants are pinned to commit `759d6a9f2002ab7367791c65118500091749d75e` of `ntsoukias/Capillary-Kir-Model`, under the MIT license. Data fetching is separate from the offline analysis; all randomness uses the recorded seed.

## References
