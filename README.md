# Integration in the Capillary Bed

A biophysical modeling study of paired-input electrical signaling from cerebral capillaries to an arteriole. The study compares distributed potassium-channel dynamics with passive conduction, independent local sensors, a bounded pooled dynamic filter and refitted ablations using single-site calibration, held-out paired stimuli and a common vascular output transform.

[Read the paper](https://piatra.institute/papers/integration-in-the-capillary-bed.pdf)

## Reproduce

The simulation is a locked uv project. See [simulation/README.md](simulation/README.md) for model assumptions, source provenance, tests and the recorded-run command. The numerical results and manuscript claim bindings are in `simulation/output/results.json` and `claims.yaml`.

## Build

With `uv`, `pandoc` and `xelatex` installed, run `uv run /absolute/path/to/integration-in-the-capillary-bed/build.py`. From the collection container, run `./papers build integration-in-the-capillary-bed` and `./papers check integration-in-the-capillary-bed`. The PDF is written to `paper/PAPER.pdf`.
