# Editorial record

Author-side full manuscript read, argument revision and all-page visual inspection completed on 14 November 2026. Independent certification remains pending. This record is not an independent editorial or visual sign-off.

## Contribution and reader

The paper asks which paired-input voltage measurement can distinguish a distributed capillary membrane mechanism from fitted passive, independent-sensor and pooled nonlinear alternatives. Its reader is a vascular electrophysiologist or modeler planning a discriminating preparation. The contribution is a reproducible conditional benchmark and measurement design, not evidence that the intact brain uses this mechanism.

Moshkforoush et al. (2020) already modeled regional summation, Longden (2026) already proposed paired inputs and upstream electrical recordings, and Rivers (1997) already distinguished cumulative dilation across stimulation geometries. The added result is the matched-single geometry comparison, its restricted pooled-controller invariance, refitted localization controls, an exact output-transform decomposition, and quantitative uncertainty and precision calculations. The title and header remain those fixed by the owner.

## Material worth preserving

Preserve the distinction between registry identity, inspected source support and independent certification; between published endpoint screening and synthetic trace fitting; and between a distributed interaction and a common output nonlinearity. The exposure-footprint failure, unresolved onset discrepancy and weak-Kir regime constrain the result. They are central findings.

The geometry argument identifies the exact class it excludes. It does not exclude branch-specific hidden states or recurrent local source loading. The proposed experiment therefore includes measured or clamped source waveforms and post-intervention single-input controls.

## Reverse outline

1. Abstract: the question, invariant pooled null, model-conditioned contrast and physiological limit.
2. What a paired stimulus can establish: the ambiguity of nonadditive dilation and the external prior art.
3. Electrical network and parameter provenance: current balance, parameter origins, unit convention, free bounds, topology and the common hydraulic readout.
4. Single-site calibration and withheld predictions: reversible single-exposure screening, synthetic rival fitting, identifiability and the held-out split.
5. Separate electrical interaction from output saturation: aligned residuals and their exact decomposition.
6. A geometry contrast with matched single-site signals: the restricted pooled-controller invariance and the source-loading alternative.
7. Held-out responses and competing mechanisms: calibration errors, paired errors, all-model residuals, topology transfer, weak-response behavior and effective KATP input.
8. A measurement that could discriminate the models: geometry, timing, source controls, focal blockade, precision and numerical resolution.
9. Where the inference stops: membrane loading and the physiological processes outside the model.
10. Code and data availability: the reproducibility package, frozen inputs, rights and absence of an analyzed raw experimental dataset.
11. References: sixteen external works, with full-text, abstract-only and identity-only use distinguished in sources.md.

## Strongest rival

A pooled controller with arbitrary deterministic dynamics can produce an electrical interaction but cannot distinguish matched summed inputs. The exact-single oracle and the uniqueness argument therefore supply the main comparison. The bounded tanh filter tests one sequentially fitted architecture: its calibrated passive driver is frozen before fitting three further coefficients. Its fit quality is reported without claiming it is the best possible pooled model.

Distal-active and arteriole-linear variants retain distributed capillary interactions and already have appreciable singleton errors. They remain localization diagnostics and no longer determine protocol selection or sample size. The primary uncertainty calculation varies the distributed parameters against the exact pooled zero, which is independent of rival parameters. It does not establish joint separation among distributed localization variants.

A local voltage-dependent source can be modulated by feedback through a passive network. Experimental singleton waveforms, source-voltage measurements and post-intervention controls remain necessary for interpreting a geometry contrast.

## Decisions and completed author checks

The inherited prose and evidence files were scaffolds; inherited membrane and topology code were audited as untrusted work. Retained the published Kir current and reciprocal graph after checking units and provenance. Replaced fixed-duration resting initialization with current-balance convergence and added a regression test for false passive interaction from baseline drift. Required recovery after the broad exposure instead of accepting large but latched responses. Used a connected exposure patch instead of separately stimulated terminal regions.

The recorded study fixes fitting rules before paired prediction. The oracle is privileged on test topologies; mechanistic rivals receive the same free-parameter count, bounds and multistart schedule. Unequal calibration quality is reported. The selected vector has relatively high Kir conductance and near-lower-bound junctional resistance and is not described as typical tissue.

The authoring team read the final manuscript against sources and recorded outputs. The distal-active model is a localization control within the distributed class. At the simultaneous design the drug effect is numerically resolved but small; it is distinct from the primary pooled-null comparison. Same-family author-side audits do not constitute independent certification.

## Referee-response decisions

H1: replace the obsolete absolute run command with a relative command from simulation/ and use a portable temporary Matplotlib configuration directory. Preserve the prior receipt through the tooling's automatic archive.

H2: normalize the Crane, Neild and Segal author names to ordinary capitalization after checking the complete author list against a fresh Crossref response. Record this typesetting normalization in sources.md. The other bibliography entries contain no all-capital name words.

F1–F2: choose the maximum geometry separation from the nondistributed null on the original candidate grid. Plan against the invariant pooled zero and report nominal and smallest-sampled effect calculations separately. Keep the four-mean residual estimator explicit; do not imply that two nearly overlapping distributed-Kir variants are statistically separated.

F3: replace the sub-recording-interval quadratic fit with a bounded tanh controller, enforce a resolvable time constant and use the calibrated passive driver. Count driver and filter parameters separately. Report boundary optima and worse calibration as negative results.

F4: add the requested dense concentration plot and refined sampled sign brackets. Source-current slopes and the true fork are recorded. The referee's alleged shared node is an inactive terminal during the sibling trial, so the interpretation follows the graph and new diagnostics instead.

F5: report all singleton/recovery counts and the accepted set's lack of overlap with the reported mean-plus-or-minus-SD conductance band. This band is not the complete physiological range, and residual hyperpolarization after a finite recovery window does not prove permanent latching. Test imposed slow Kir suppression and a TRPV4-like conductance on a finite low-conductance grid and near the nominal switching boundary. Distinguish published pharmacological timescales from assumed receptor coactivation, recovery and spatial extent.

F6: use simultaneous input and independent-singleton, response-aligned window selection in the experimental proposal. Freeze the window before paired trials and estimate assay precision anew; the simulated timing and sample sizes are conditional planning examples.

F7: retain active Kir on the anastomosis bridge in the distal-active control and test that the former passive-bridge error changes the paired response.

F8: engage seven verified external references. Wessel demonstrates Kir-mediated summation using one- and two-compartment models; Rall remains an identity-only historical citation. All source claims retain honest inspection depths and their existing verified values. Rall and Crane full texts remain explicit gaps.

F9: remove habitual negative contrasts and narrow the claims directly. Preserve title, argument structure, original equations and good unaffected prose. The availability statement names the repository and pinned external model code. No distinctive neologism is introduced, so coined_terms remains empty.

new:V1: move the concentration figure's legend outside the axes and place both zero-crossing labels in clear regions using axes-relative positions. Preserve the curves, sampled brackets, plot dimensions and manuscript caption. The round-one closure accepted H1 and F1–F9; their scientific changes remain intact. This follow-up changes presentation and re-records the accepted study because its plotting source changed.

The checkout contained status: built despite the instruction that the paper remains published; status was set to published in accordance with the owner's explicit instruction. The existing checks: 2026-11 was retained. Date and all own-address fields remain unchanged. No review file, coverage certification or verified flag is authored by this revision.

## Verification and remaining review

The paired-study execution completed with 25 tests passed, zero failed and zero skipped. Its command is `uv run python run_all.py` from `simulation/`; the prior receipt is preserved byte-for-byte by automatic archival as `verification/paired-study-20261114T162243164275Z.json`. The retained dependency lock, frozen parameter inventory and both source manifests are declared inputs. All 17 input hashes and 10 artifact hashes match the new receipt. Comparing the complete result JSON with the accepted run finds only `/execution/elapsed_seconds` changed. The manuscript and claim ledger remain byte-identical to the accepted versions; all 213 computation bindings still pass against the newly recorded artifact. The ledger contains 240 claims including 16 source claims. All 16 reference identities pass, with electronic-page advisories only. The abstract is 183 words. Standards find no collection self-reference; the manuscript has no em-dashes, “rather than” or “, not” constructions.

The primary authoring agent rendered and personally inspected all 18 final PDF pages at 110 dpi, including the corrected concentration plot on page 14 and Crane citation and bibliography on pages 16–17. Both crossing labels are clear of the curves at the final manuscript width, and the legend lies outside the plotting area. A separate Matplotlib layout diagnostic confirms that neither annotation's text bounding box intersects either curve and that the legend does not overlap the axes. Final renders and command logs are in `/private/tmp/capillary-round2-i8ns_dfk/`. Tables, equations, legends, figure labels and bibliography are legible; the build log has no missing-character, overfull or underfull warnings. This is author-side inspection; independent review records remain untouched.

Final manuscript SHA-256: `ccad96b8a9d3fe401e6d4075fd465daba0abe3bbb9138333d4864a2b88b39a66`. Final PDF SHA-256: `96687e306c6ae46d92e251be37a4b5450f168f55b0e0523ba4ce09ff1cc6669d`. These document author-side inspection, not independent certification.

Final local check: NEEDS_REVIEW, with 246 PASS, 19 NEEDS_REVIEW, 2 NOT_APPLICABLE and zero FAIL. Pending items are claim coverage, 16 source certifications and independent editorial/visual reviews. The reset sensitivity does not identify biological adaptation kinetics, and there is no empirical paired-input dataset in this study.
