# ZanGei v0.1 — printable front-panel fit prototype

## Files

- **`ZanGei_v0.1_Panel.FCStd`** — editable native FreeCAD panel source, retained for future mechanical changes.
- **`ZanGei_v0.1_Panel_PRINT_FACE_DOWN.stl`** — watertight mesh, already oriented with the front face on the print bed. Import in millimetres, at 100% scale; do not mirror or auto-rescale.
- **`ZanGei_v0.1_Panel.step`** — solid exchange model, re-imported and checked as one valid solid.
- `Panel_SPEC.json` — exact control and PCB-hole centres extracted from the current PCB, in millimetres, measured from panel top-left.
- `Panel_VALIDATION.json` — executed FreeCAD/STEP/mesh checks.
- Open the [main KiCad project](../schematics/BBD_Buffer.kicad_pro) for current schematics; export a fresh PDF from its root schematic if needed.

## Geometry and mounting

Panel is **40.3 × 128.5 mm**, matching an 8HP / 3U opening. The face is **2 mm** thick. Two narrow rear edge ribs add **3 mm** locally, so maximum depth is **5 mm**, not a 5 mm face at the nuts. Ribs lie outside the centred PCB edge and stop short of the rack rails. `ZanGei` and `v0.1` are recessed on the front.

Two horizontal M3 rack slots are **3.2 × 4.8 mm**, centred **7.5 mm from the left edge**, **3 mm from the top/bottom**; the vertical spacing is **122.5 mm**. This follows [Doepfer's construction drawing](https://www.doepfer.de/a100_man/a100m_e.htm), with horizontal slot allowance for rail alignment. For this width two rack screws are sufficient; the four smaller holes are NOT extra rack screws.

The four **2.2 mm** holes follow the actual CONTROL PCB mounting holes, including the non-corner placements. They are for optional M2 screws/standoffs to support the PCB. They are not countersunk. Select washers, screw lengths and spacer lengths after measuring actual seating; no printed fixed-height spacers are included.

CONTROL PCB registration: left edge **1.4 mm** from panel left, upper edge **9.25 mm** below panel top. Every control axis comes from the actual footprint placement, including the jack's barrel offset, the CHARACTER dual-pot shaft offset and LED centre—not simply the footprint origin.

### Prototype hole diameters

|Feature|Printed CAD diameter|Nominal part requirement|
|---|---:|---:|
|WQP518MA jack|6.20 mm|6.00 mm panel hole|
|Salecom SKS switch|5.15 mm|4.95 mm panel hole|
|M7 pot bushing|7.20 mm|7.00 mm nominal|
|3 mm LED|3.20 mm|3.00 mm body|
|M2 PCB fastener|2.20 mm|2.00 mm screw|

The extra **0.20 mm is a diametral prototype allowance**, not a proven printer compensation. Ream or adjust the `Parameters` hole properties after a test fit. Verify the LED body/bezel arrangement separately; this is a bare-LED hole, not a selected bezel footprint.

## Printing and use

- Start with the supplied face-down orientation, around 0.2 mm layers, at least three perimeters and a solid face/ribs. There are no deliberately unsupported horizontal rear ledges.
- Inspect small engraving in the slicer; a fine nozzle may reproduce `v0.1` better. Labelling quality is secondary to the first fit test.
- Fit parts without force. Use washers and light fastening torque. Do not use jack/pot nuts to pull an incorrectly seated PCB into alignment. The rack screws and mechanical standoffs must carry handling/patching loads.
- **PLA is appropriate for an initial unpowered fit prototype.** Do not leave soldering heat against it. Permanent rack suitability is unqualified: PLA can creep under clamping load and loses stiffness with heat; filament and real temperature matter. PETG or a metal panel is a more sensible later choice if fit is good and the module runs warm. We have not measured panel temperature, so neither overheating nor long-term PLA suitability is established.
- All axes and a valid mesh are verified; **common installed component height is not**. The selected jacks have a 10 mm effective height, while pots/switch seating, washers and pin stand-off still need measurement. Do not solder every panel part permanently before a loose full-panel/PCB fit check.
- Use small knobs in the crowded lower area; confirm knob skirts, M2 screw heads and toggle travel on the physical prototype. This is not an ergonomic or stress-tested production panel.

## Validation scope

FreeCAD 1.1.4 produced one valid solid; exported STEP re-imported as one valid solid. The STL re-imported watertight with 10,696 facets and Z bounds approximately 0–5 mm. This proves a closed printable model and the intended dimensions, not printer accuracy, thread engagement, actual assembly clearance or heat resistance.

Current public references are the [architecture](../docs/ARCHITECTURE.md), [build notes](../docs/BUILD.md) and [BOM](../bom/v0.1/BOM.md). Whole-board FreeCAD review assemblies are local-only generated outputs, not dependencies of the panel or KiCad project.
