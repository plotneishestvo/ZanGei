# Historical circuit studies

These retained, self-contained studies explain earlier circuit choices. They do **not** read the current KiCad design or validate its topology, values, power protection, clock edges, BBD behaviour or complete feedback-loop stability. Treat their generated findings as results for their embedded circuit models only.

| Input | Scope | Requirements / invocation |
|---|---|---|
| [clock_cv_active.py](clock_cv_active.py) | Buffered TIME-knob and half-scale external-CV candidate. The current design has a passive knob and parked U302A, so this is historical. Typical-node clamping uses illustrative Schottky and legacy op-amp models; no power-off/ESD/tolerance qualification. | Python 3, ngspice: `python simulation/clock_cv_active.py` |
| [wet_character_components.py](wet_character_components.py) | Search over historical 100k dual-gang CHARACTER candidates using ideal static calculations and selected ngspice checks. The current design uses 50k gangs shunted by 50k; embedded targets and candidates are not its specification. No BBD/S&H/full-loop model. | Python 3, NumPy, ngspice: `python simulation/wet_character_components.py` |
| [buffer_qucs.cir](buffer_qucs.cir) | Ideal unity buffer followed by a gain-two driver; educational input/output study, not the integrated module. | Qucs-S with ngspice, or `ngspice -b simulation/buffer_qucs.cir` |
| [input_buffer_ngspice.cir](input_buffer_ngspice.cir) | Ideal-source version of the same early buffer/driver study. Interactive plot deck. | `ngspice simulation/input_buffer_ngspice.cir` |

Run the Python commands from the repository root. Outputs are generated under ignored `tmp/clock-active-fix/simulation/` and `tmp/wet-character-components/`; neither directory is an input dependency. The scripts use the included [TI TL072 model](models/TL072_TI.lib), whose original notices remain applicable. The wet-character search runs many candidates and prints historical findings; it is not a quick regression test. Paths containing spaces may require adapting ngspice include quoting.

See the [architecture](../docs/ARCHITECTURE.md) for the implemented circuit and [build notes](../docs/BUILD.md) for prototype measurements still required.
