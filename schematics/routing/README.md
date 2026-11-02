# Routed prototype: scope and limitations

Open the [main KiCad project](../BBD_Buffer.kicad_pro) and [PCB](../BBD_Buffer.kicad_pcb). The working layout contains separate **CONTROL** and **CORE** outlines side by side. Fabrication outputs must be generated separately for each physical board.

## Inter-board links

The combined layout intentionally retains 12 cross-region connections, carried by J602/J603 (power) and J604/J605 (signals):

`+12V`, `+5V`, `-12V`, `AUDIO_IN_BBD`, `BBD1_SUM`, `BBD2_SOURCE`, `BBD2_SUM`, `CLK_TIME_SUM`, `GND`, `INHIBIT_CV_IN`, `OUT_SH`, `WET_MIX`.

**Never route these links as copper across the display gap.** Verify each separated board for local opens and check the real mating connectors unpowered. See the [stack pin maps](../../docs/BUILD.md#stack-pin-maps).

## Routing and ground intent

The documented routing baseline uses two copper layers, a 0.2 mm trace floor, 0.6/0.3 mm via copper/drill, 0.2 mm netclass clearance, 0.5 mm copper-edge clearance and 0.25 mm copper/hole clearance. Confirm the current native rules when regenerating fabrication outputs.

Each physical board has a GND pour on both faces. Ground pads have explicit routed lead-outs; direct pour-to-pad connection is set to **None**, so the fills join routed GND tracks/vias rather than automatically supplying thermal spokes. This is not proof of an optimal return path or electromagnetic compatibility.

## What remains to be checked

Earlier separated-board checks reported zero local opens and zero routing/copper/hole/edge errors. Those are historical observations, **not a current fabrication or full-DRC certificate**. Refill zones and rerun ERC/DRC on current source and separated outputs before fabrication.

Opposite-face PTH/courtyard interactions, crowded silkscreen, control seating, lead trimming, stack engagement and assembly access remain prototype limitations. The [assembly guide and per-reference review](../assembly/README.md) retain useful access constraints. A zero-open result does not establish collision-free assembly.

Clock routing, high-impedance paths and analog returns need engineering review and bench measurements for feedthrough, noise, phase timing and stability. Track-length totals are not measured per-chip clock skew. No complete-module analog performance is claimed. Follow the [build and protected first-power notes](../../docs/BUILD.md).
