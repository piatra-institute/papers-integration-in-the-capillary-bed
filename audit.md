# Audit

## 2026-11-14 — Complete and audit the inherited paper

Scope: completed the brief, external-literature audit, membrane-network implementation, single-site-only calibration and sensitivity analysis, held-out paired study, claim ledger, manuscript, figures and reproducibility package. Preserved the owner's title, header and slug. Audited inherited code and treated seed conversations as ideation. No other PIATRA work supplies evidence or terminology.

Changes: checked every bibliography identity against Crossref; froze source copies and the parameter inventory; separated assumptions and published values; corrected resting initialization; tested recovery and exposure footprint; refitted passive and localization controls; added an exact-single oracle and a parameter-matched nonlinear dynamic filter; quantified electrical/output residuals, geometry discrimination and measurement precision. The final text reports the onset discrepancy, a regime where additivity suffices, recurrent source-loading ambiguity and the numerically unresolved nearest-rival drug separation.

Verification:

- Recorded execution: `verification/paired-study.json`, PASS, with 18 tests passed, zero failed and zero skipped. Code, lock, frozen inputs and generated artifacts match the receipt. Source-manifest file hashes were checked against retained files.
- References: 9 cited IDs resolve to 9 entries; all registry identities pass. Two page-field advisories reflect electronic article locators. Eight full texts and one abstract were inspected; inaccessible material is identified in sources.md.
- Claims: 201 total: 180 computation bindings, 10 source claims and 11 definitions/assumptions/interpretations. Every numerical binding passes. Independent source certification and claim coverage remain pending.
- Standards: no collection self-reference; abstract 190 words; no FAIL. Metadata and CITATION.cff agree with the manuscript.
- Build: 14-page PDF; no missing-character, overfull or underfull warnings in the final build log. Rendered at 80 dpi and personally inspected every page. Revised pagination keeps comparison tables intact and avoids a float interrupting a paragraph. Hashes and inspection scope are in editorial.md; no independent review record was created.
- Final local check: `NEEDS_REVIEW`, exit 3: 206 PASS, 13 NEEDS_REVIEW, 2 NOT_APPLICABLE and zero FAIL. Pending items are coverage, 10 source certifications and independent editorial/visual records. Full command output is in `verification/final-check.txt`; structured output is in `verification/final-check.json`.

Author-side reading does not satisfy the cross-family review requirement. `coverage: pending` and `reviewed_manuscript_sha256: null` are preserved. No review record, seed, existing execution receipt, other repository, commit, push or deployment was changed.


## 2026-11-14 — Respond to external referee findings H1 and F1–F9

Revised the design around the exact matched-input pooled-controller null, preserving the title, thesis and section structure. Simultaneous stimulation gives a nominal geometry contrast of 0.833 mV and a four-mean planning count of 46 observations per condition; smallest sampled effects give 129 and 96. Distributed localization controls no longer determine the primary design or sample size. The bounded tanh controller uses the calibrated passive driver and a resolved time constant; its poorer singleton fit and active parameter bounds are reported.

Added the requested concentration-boundary figure and step-refined sign brackets. Corrected the referee's node interpretation using the actual graph and stimulated-source current slopes. Exposed the full local screen counts: 503 singleton matches, 241 persistent responses at the recovery endpoint, 189 recovered low-amplitude responses and 73 joint passes. None of the 29 accepted vectors lies in the reported mean-plus-or-minus-SD Kir band. The imposed slow-reset extension produced no full-screen passes on the 125-vector band grid across eight adaptation scenarios, while source-timescale Kir-only suppression restored all seven nominal perturbations. These are finite model tests; source pharmacology does not establish potassium-triggered receptor kinetics. Experimental timing is now selected from independent response-aligned single-input recordings before paired trials.

Fixed the passive anastomosis-bridge bug and added regression checks. Added seven Crossref-verified prior works, distinguished Wessel's actual compartment models from the referee's branched-cable description, and retained honest fulltext/abstract/identity inspection boundaries. Rall full text and Crane full text remain unavailable; neither is represented as fully inspected. Rewrote the abstract after the body to 183 words, removed habitual negative contrasts, updated availability and reproducibility instructions, and rebound all affected claims. The pre-existing checks: 2026-11 contract was retained. The checkout's status: built conflicted with the owner's instruction to retain publication; it was set to published. Date, web_slug, repo and github remain unchanged. No new neologism is claimed.

Verification:

- Recorded `paired-study` with the portable command `uv run python run_all.py` from simulation/, the existing dependency lock, three declared frozen inputs, and ten result/test/figure artifacts. All 25 tests passed, with zero failures or skips. The previous execution receipt was archived automatically and is byte-identical to its original git version; no receipt was manually edited.
- All 213 computational bindings pass in the 240-claim ledger. Existing verified flags remain false, coverage remains pending, and reviewed_manuscript_sha256 remains null. All 16 reference identities pass after a transient registry rate limit was retried; electronic article locators produce advisory page differences only.
- Ran metadata, citation, vendor, build, standards and claims commands from the collection root. CITATION.cff is the generated file. Standards report no self-reference and an abstract below the word limit.
- Built the 18-page PDF, rendered every page at 110 dpi and inspected all pages as an authoring team. Corrected an isolated paragraph page and a figure interrupting a paragraph, re-rendered, and inspected changed pages again. Final rendering hashes and inspection scope are in editorial.md. No missing-character, overfull or underfull build warnings remain.
- Final local check: NEEDS_REVIEW, exit 3, with 246 PASS, 19 NEEDS_REVIEW, 2 NOT_APPLICABLE and zero FAIL. Remaining review items are coverage, source certification and independent editorial/visual records.

No editorial-review.json, visual-review.json, reviews/ material, archived chats, other repository, commit, push or publication was changed. Review certification is left to the independent reviewer.

## 2026-11-14 — Round-two presentation corrections

Read the binding standards, referee reports and round-one closure. Preserved the ten closed findings, H1 and F1–F9. Addressed H2 by normalizing Crane, Neild and Segal's author names after a fresh curl lookup of Crossref DOI 10.1080/10739680490457836; documented the capitalization change in sources.md. No other bibliography entry contains all-capital name words, and no reference was added. Addressed new:V1 by moving Figure 3's legend outside the axes and placing the zero-crossing labels clear of both curves. The curves, brackets, caption and figure dimensions are unchanged.

Re-recorded `paired-study` with the existing relative command, dependency lock, three frozen-input declarations and ten artifact declarations. All 25 tests passed without failures or skips. All 17 input hashes and 10 artifact hashes match the receipt. The tooling archived the prior receipt as `verification/paired-study-20261114T162243164275Z.json`, byte-identical to its incoming version. The complete results JSON differs only in elapsed time; all scientific results, including the negative conductance-band reset experiment, are unchanged. All 213 computation bindings still match, so no claim rebinding was needed. The manuscript and ledger remain byte-identical to their accepted versions, including the 183-word abstract, availability statement, evidence depths and verified flags.

Ran refs --verify, metadata, citation, vendor, build, standards and claims from the collection root. All 16 reference identities pass; electronic article locators produce advisory page differences only. Personally inspected all 18 rebuilt PDF pages at 110 dpi. Figure 3's labels and external legend are clear at final width; the Crane citation and bibliography use ordinary capitalization. The build log has no missing-character, overfull or underfull warnings. Manuscript and final PDF hashes are recorded in editorial.md.

Final `./papers check integration-in-the-capillary-bed --json`: NEEDS_REVIEW, exit 3, with 246 PASS, 19 NEEDS_REVIEW, 2 NOT_APPLICABLE and zero FAIL. Pending items are independent claim coverage, source certification and editorial/visual records. Retained `status: published`, date, web_slug, repo, github, `checks: 2026-11` and `coined_terms: []` exactly. No owner decision was required; no review record, archival chat, other repository, commit, push or publication was changed.
