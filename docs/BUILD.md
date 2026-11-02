# Prototype build notes

**Status:** the complete module has not yet been assembled, calibrated or hardware-qualified. These are preparation notes, not a proven kit manual. Read the [architecture](ARCHITECTURE.md), [BOM](../bom/v0.1/BOM.md) and [panel fit notes](../mechanical/README.md) before building.

## Open the design

Use KiCad 10 and open [`schematics/BBD_Buffer.kicad_pro`](../schematics/BBD_Buffer.kicad_pro). The root schematic links seven electrical sheets. The PCB contains two separate boards side by side: CONTROL on the left, CORE on the right. Do not route copper across the display gap: the remaining inter-board connections are made by the stack connectors.

Custom symbols and footprints resolve through the project-local `sym-lib-table`, `fp-lib-table`, `BBD_Custom.kicad_sym` and `Zangei.pretty/`. Install KiCad's standard symbol, footprint and 3D libraries too. Local STEP/VRML models in `Zangei.3dshapes/` are clearance/review approximations, not exact vendor CAD; STEP siblings support mechanical export, and VRML retains colour. A whole-board FreeCAD review assembly is not a KiCad dependency.

## Parts and substitutions

Use the [one-module BOM](../bom/v0.1/BOM.md) and its grouped/per-reference CSVs for fitted quantities, exact selections and additional sockets/hardware. Confirm supplier specifications and actual body/pin geometry before assembly.

- U101 is **V3208D**; U201 is **V3205SD**, with a special spaced eight-lead package. Its project footprint uses selected holes of a 16-position socket pattern. It is not an ordinary consecutive-pin DIP8 substitute.
- U304 is **TC4428AEPA**, the complementary-output A-version driver in through-hole PDIP8.
- RV403 is **Nidec CT-6EP103**, replacing Bourns 3362P-1-103LF. The local footprint has pin centres 1=(0,0), 2=(2.5,-2.5), 3=(5,0) mm; pin 2 is the wiper, tied to pin 3 in this circuit. Nominal body is 7 × 7 × 5.8 mm; the labelled model reserves 7.3 × 7.3 × 6.1 mm. The replacement changed the hole pattern, not the electrical topology. [Manufacturer drawing, CT-6EP](https://www.nidec-components.com/e/catalog/trimmer/ct-6.pdf).
- RV404/RV801 use **UralTone 624-UT-RD901F-40-15K-B10K**, 10k linear, with 6 mm T18 knurled shafts. Their drawing matches the selected hole pattern and nominal seating height; catalogue prose says 2.54 mm pitch while the drawing indicates 2.5 mm. Dry-fit received parts. Other single pots have 6 mm D shafts; the CHARACTER dual has a 6.35 mm round shaft. Select knobs accordingly.
- CHARACTER uses a dual linear 50k pot with one exact 50k shunt per gang (R414/R415), giving nominal 25k endpoints with a nonlinear sweep. Do not silently substitute 51k shunts.
- R601/R602 are the selected **10 ohm flameproof/fusible** parts, not arbitrary kit resistors. Resettable PTC hold current is not an instantaneous current limit.

## Stack and connector engagement

Each PCB is **37.5 × 110 mm**, nominally 1.6 mm thick. The panel is **40.3 × 128.5 mm**, for an 8HP / 3U allocation. The centred PCB inset is 1.4 mm per side and 9.25 mm top/bottom. Final depth includes parts, headers and the plugged-in power cable; measure it against the actual case.

The proposed clear gap between facing PCB surfaces is **20 mm**, not 20 mm between board centre planes. CORE sits behind CONTROL without flipping the pad mapping. J602/J603 carry power; J604/J605 carry signals. All numbered pads and four mounting-hole pairs align after the source layout's side-by-side translation.

| CORE | CONTROL | Selected connection |
|---|---|---|
| J602, 2×3 male | J603, 2×3 female | TSW-120-15-G-D stock cut to 2×3; SSW-103-01-G-D |
| J604, 2×6 male | J605, 2×6 female | Same TSW stock cut to 2×6; SSW-106-01-G-D |

One 2×20 male strip supplies both sections per module, allowing sacrificial rows when cutting. Do not shorten the mating posts or replace them with ordinary short headers.

Samtec's selected male has a 2.54 mm insulator and 13.21 mm exposed mating posts; the female body is 8.51 mm high. At a 20 mm gap this gives **4.26 mm nominal insertion**, within the specified **3.68–6.35 mm** range. Solder tails do not contribute to mating reach. The housings do not touch: long exposed pins remain between them. The standoffs, not the contacts, support the boards. This is a nominal dimensional check, not a worst-case tolerance certification. Added washers under spacer ends increase the gap and reduce insertion; physically verify seating and engagement before final soldering. Sources: [TSW](https://suddendocs.samtec.com/catalog_english/tsw_th.pdf), [SSW](https://suddendocs.samtec.com/catalog_english/ssw_th.pdf).

Generic KiCad connector models currently have ordinary pin lengths, not the selected long-post geometry. Do not infer engagement from those models alone. Panel-support lengths/joints, screw clearance and metal-to-copper isolation remain dry-fit checks.

### Stack pin maps

Pin numbers below are logical pad numbers, not a view through the opposite board. Check physical orientation and continuity unpowered.

| J602 ↔ J603 pin | Function |
|---|---|
| 1 | +12 V |
| 2 | GND |
| 3 | −12 V |
| 4 | GND |
| 5 | +5 V |
| 6 | GND |

| J604 ↔ J605 pin | Net |
|---|---|
| 1 | AUDIO_IN_BBD |
| 2 | GND |
| 3 | BBD1_SUM |
| 4 | BBD2_SUM |
| 5 | WET_MIX |
| 6 | GND |
| 7 | OUT_SH |
| 8 | GND |
| 9 | CLK_TIME_SUM |
| 10 | INHIBIT_CV_IN |
| 11 | BBD2_SOURCE |
| 12 | GND |

## Assembly and power precautions

The board is mostly through-hole, but **Q601 (SOT-23), F603 (1206) and FB601 (1206)** are SMD. Opposite-face components and dense placement make solder access and trimmed-lead clearance important. Read the [per-reference solder-access review and sequencing notes](../schematics/assembly/README.md). Existing PTH/courtyard and silkscreen findings are not a claim of collision-free assembly. Plan access and loosely fit the stack/panel before permanently soldering panel parts. Plated-through holes connect their two rings through a copper barrel; solder from whichever face permits proper pad/lead wetting and hole fill, without routinely reheating both faces.

J601 is a **16-pin Eurorack power connector on the rear of CORE**. Looking directly into that mounted connector with the PCB top up: key opening left, negative pair at the top. Check the actual ribbon/header; a keyed shell is not protection against a miswired cable.

| J601 pins | Bus connection |
|---|---|
| 1–2 | −12 V entry |
| 3–8 | GND |
| 9–10 | +12 V entry |
| 11–12 | +5 V entry |
| 13–16 | Not connected |

The module **requires bus +5 V** as well as ±12 V. A ten-conductor ribbon does not supply +5 V. There is no fitted local +12-to-5 V regulator. The +5 V PTC/MOSFET/bead path is not an overvoltage or reverse-current isolator. R603 is a 1k rail-to-ground bleed/load, not a series dropper: it draws nominally 5 mA/25 mW at 5 V and helps load clamp-injected current and discharge capacitance.

Before any rack connection, verify cable continuity, polarity, shorts, solder bridges and isolation at metal mounting hardware. First powered commissioning needs an agreed current-limited/protected arrangement; measure local rails, current, temperature and jack DC voltages. Never use a valuable rack as an unprotected fault test. Clock amplitude/phase timing, bias, gain, feedback behaviour and audible performance still require measurement. Simulations and zero connectivity errors do not establish these.

## Fabrication

Generate fresh **separate CORE and CONTROL** outputs from the current source after any geometry change. Preserve retained footprints, copper, filled zones, pad nets and hole patterns; check each derivative independently for local opens. The combined working file has intentional cross-board airwires, whereas each physical board should have none.

The documented prototype fabrication baseline is OSH Park standard two-layer service, nominal 1.6 mm / 1 oz / ENIG. Important geometry: 0.2 mm minimum routed trace, 0.6/0.3 mm via copper/drill, and 0.15 mm minimum annular ring on narrow TO-92 pads. Supplier capability must be checked against these actual dimensions. A service requiring 0.30 mm component-hole annular rings is incompatible with these pads; changing surface finish alone does not resolve that. CONTROL has **12 plated routed slots**; both boards have **four 2.2 mm non-plated mounting holes**. Preserve slot plating and shape.

Refill/save zones before native upload; OSH Park does not refill them. Inspect the vendor's outline, holes, slots, copper and mask previews. Panelization is possible under vendor-specific rules, but separate jobs avoid paying for this working layout's display gap. Three copies of each design provide three PCB sets. Do not order old generated packages after a footprint change. Generated manufacturing outputs are intentionally local-only and are not included as a tested release package in this repository.
