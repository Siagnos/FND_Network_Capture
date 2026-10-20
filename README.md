# Self-stabilising network capture in functional neurological disorder

Reproducible computational supplement to the manuscript *Self-stabilising network capture in functional neurological disorder: a testable cortico-subcortical dynamical framework* (Das & Dutta).

The repository contains one script for each manuscript figure (Figures 1–6), plus independent numerical checks of the underlying models. All Python source files, including the one-command runner, are under `src/`. Pre-rendered figures are in `figures/` and reference numerical results in `results/`.

## Run all figures and tests

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/run_all.py --suite all
```

The six figures (PNG, LZW-TIFF, PDF), Figure 6 CSV, and validation outputs are written to `outputs/`. For `--suite figures` or `--suite validation`, only the requested workflow runs.

## Figure sources

| Manuscript figure | Executable source | Scope |
|---|---|---|
| Figure 1 | `src/make_figure1.py` | Recurrent logistic equilibria and an explicitly illustrative slowing trajectory |
| Figure 2 | `src/make_figure2.py` | Effective potential, analytic folds and stochastic example |
| Figure 3 | `src/make_figure3.py` | Coupled brain–body feedback and gain-dependent trajectories |
| Figure 4 | `src/make_figure4.py` | Three-state defensive feedback with conditional residual input and joint parameter changes |
| Figure 5 | `src/make_figure5.py` | Barriers and three **predeclared-seed**, synthetic example paths |
| Figure 6 | `src/make_figure6.py` | N=1000 per condition, D=0.004/0.006/0.008, Wilson intervals |

`src/validate_model.py` and `src/validate_defensive_reset.py` provide complementary numerical checks; `tests/test_model_invariants.py` tests analytic invariants.

## Alternative execution

- **GitHub Codespaces:** Code → Codespaces → Create, then run commands above.
- **Windows:** use `py -3` instead of `python` where required.
- **Google Colab:** open `notebooks/Run_FND_Network_Capture.ipynb` and select Run all.
- **GitHub Actions:** every push and pull request runs the tests, regenerates all figures and uploads them as a downloadable artefact.

## Scientific interpretation

These are **synthetic mathematical illustrations, not patient data or clinically calibrated simulations**. Potential bistability requires chosen nonlinearities and parameter regimes; it does not establish that specific subcortical nuclei cause FND. Figure 1C imposes a switch in a separate illustrative time series; Figure 4C uses a nonzero post-pulse input, and Figure 4D changes two intervention terms as effective gain continues to adapt. Figure 5 example paths are not treatment-effect estimates. Figure 6 timing schedules do **not** dose-match the sequential arms, so treatment sequencing must not be inferred. A parameter change labelled tilt/flatten is not a demonstrated physiological effect of any therapy. See `docs/MODEL_AND_REPRODUCIBILITY.md`.

## Repository contents

| Path | Contents |
|---|---|
| `src/` | Figure scripts, validation scripts and `run_all.py` |
| `tests/` | Unit tests of analytic model invariants |
| `figures/` | Pre-rendered Figures 1–6 (PNG) |
| `results/` | Reference numerical outputs (CSV, JSON) produced by the scripts |
| `docs/` | Model specification, reference values and SHA-256 file manifest |
| `notebooks/` | Google Colab notebook |

## Citation

If you use this code, please cite the associated manuscript and this repository. Citation metadata are provided in `CITATION.cff`.

## Licence

Released under the MIT License; see `LICENSE`.
