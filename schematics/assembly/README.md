# Prototype assembly access

The [solder-access CSV](Solder_Access_Review.csv) retains 164 recorded opposite-face PTH/courtyard interactions, by reference and pad coordinate. These are geometric warning candidates, not proof of physical collisions or a fresh audit of the current board. Compare each entry with the current PCB and the actual selected part before assembly. A component's courtyard is not an exact body solid.

## Sequencing and physical checks

- Solder, inspect and trim **C804 before RV801**, **C806 before RV402**, and the affected **R701 joint before J701**. Confirm actual body clearance and access rather than forcing a body over a fillet.
- Resolve other CSV interactions by checking tool access, hole fill and trimmed-lead clearance before fitting the opposing body. Opposite-face assembly is not automatically safe merely because footprints do not overlap on the same face.
- Loosely fit the panel, controls and board stack before final soldering. Common jack/pot/switch seating and nut engagement remain unqualified.
- Do not assume unspecified component lift, insulating body coatings or soldermask will prevent shorts. Check metal supports and screw heads against exposed copper.
- Plated-through barrels connect both pad rings. Solder from an accessible face with proper wetting/hole fill; routine reheating from both sides is unnecessary.

The board also has crowded silkscreen. Read references and polarity from the native design when markings are obscured. These notes do not establish collision-free assembly or analog performance. See the [one-module BOM](../../bom/v0.1/BOM.md), [stack and power instructions](../../docs/BUILD.md) and [routing limitations](../routing/README.md).
