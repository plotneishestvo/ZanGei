# ZanGei v0.1 — bill of materials

Quantities are for **one module: 157 schematic components in 64 groups**, plus the separate assembly hardware below. These are fitted quantities, not pack sizes or spare allowances. Supplier links identify the selected parts; availability and physical fit must be checked.

- [Grouped CSV](BOM_GROUPED.csv): quantities, exact schematic values, selected parts and footprints.
- [Per-reference CSV](BOM_PER_REFERENCE.csv): one row per schematic position, with its exact value, footprint and PCB.
- [Build and power precautions](../../docs/BUILD.md), [assembly access](../../schematics/assembly/README.md) and [panel fit](../../mechanical/README.md).

The PCB is mostly through-hole. **Q601 (SOT-23), F603 (1206 PTC) and FB601 (1206 ferrite) are SMD.** U201 V3205SD has a special spaced eight-lead package using a 16-position socket pattern. Do not substitute ordinary DIP8.

## Components

Exact KiCad footprint assignments are in both CSVs. Generic resistors are specified individually by value, tolerance, power and fit; no assortment is required. Exact precision and protection part selections must be retained. R302's source record lacks tolerance/power: verify those rather than assuming a generic resistor specification.


### ICs

| Qty | References | Selected part / specification | Fit / electrical notes |
|---:|---|---|---|
| 1 | U301 | [CD4046BE  CMOS digital Phase-Locked Loop DIL16](https://en.uraltone.com/catalogsearch/result/?q=184-4046BE) | Through-hole DIL16. |
| 1 | U304 | [TC4428AEPA](https://www.digikey.com/en/products/detail/microchip-technology/TC4428AEPA/442809) | Exact A-version complementary inverting/non-inverting driver; through-hole PDIP8, not SOIC/MSOP. |
| 5 | U302, U401, U402, U701, U702 | [TL072ACP - op amp -Texas instruments](https://en.uraltone.com/catalogsearch/result/?q=184-TL072ACP) | Texas Instruments TL072ACP, DIP8; not an automatic NE5532 substitution. |
| 1 | U201 | [Coolaudio V3205SD special spaced 8-lead BBD](https://www.op-electronics.com/en/delay-chips/95-coolaudio-v3205sd.html) | Special spaced eight-lead package in selected holes of a 16-position socket pattern; NOT ordinary consecutive-pin DIP8. |
| 1 | U101 | [Coolaudio V3208D 2048-Stage Low-Noise BBD Analog Delay Line IC (DIP8)](https://en.uraltone.com/catalogsearch/result/?q=184S-V3208D) | Coolaudio 2048-stage BBD, DIP8; distinct from U201 V3205SD. |

### Transistors

| Qty | References | Selected part / specification | Fit / electrical notes |
|---:|---|---|---|
| 1 | Q701 | [2N3904BU](https://www.digikey.com/en/products/detail/onsemi/2N3904BU/1413) | onsemi TO-92; verify received pin order against footprint. |
| 1 | Q401 | [2N5457 J-FET N-channel Fairchild NOS USA](https://en.uraltone.com/catalogsearch/result/?q=181-2N5457-FAIR) | Selected Fairchild NOS part: physical pins 1=D, 2=S, 3=G; other manufacturers may differ. |
| 4 | Q101, Q102, Q201, Q202 | [2N7000 Transistor N-MOSFET, 60V, 200mA, TO-92](https://en.uraltone.com/catalogsearch/result/?q=181-2N7000) | 60 V, 200 mA TO-92; verify received pin order. |
| 1 | Q601 | [AO3401A](https://www.digikey.com/en/products/detail/alpha-omega-semiconductor-inc/AO3401A/1855773) | P-channel SOT-23; SMD. |

### Capacitors

| Qty | References | Selected part / specification | Fit / electrical notes |
|---:|---|---|---|
| 1 | C801 | 10 pF — [C315C100J5G5TA](https://www.digikey.com/en/products/detail/kemet/C315C100J5G5TA/6562319) | 10 pF C0G, 5%, 50 V; P2.54 mm. |
| 1 | C405 | 10 nF — [R82EC2100AA50J](https://www.digikey.com/en/products/detail/kemet/R82EC2100AA50J/2571307) | 10 nF polyester film, 5%, 100 V; P5 mm; nominal body 7.2 x 2.5 mm. |
| 18 | C104, C204, C302, C304, C406, C407, C408, C409, C410, C501, C502, C602, C604, C606, C703, C704, C805, C806 | 100 nF — [C315C104K5R5TA](https://www.digikey.com/en/products/detail/kemet/C315C104K5R5TA/12701330) | 100 nF X7R, 50 V; compact P2.54 mm body required. |
| 2 | C701, C804 | 1 uF — [R82EC4100AA70J](https://www.digikey.com/en/products/detail/kemet/R82EC4100AA70J/9685242) | 1 uF polyester film, 5%, 100 V; P5 mm; nominal body 7.2 x 6 mm, seated height 11.1 mm. Do not substitute ceramic. |
| 1 | C403 | [KEMET 15nF (0.015uF) / 400V polyester film capacitor, radial](https://en.uraltone.com/catalogsearch/result/?q=545-MC5-15N/400V) | 15 nF / 400 V polyester film, radial; check actual body and lead seating. |
| 3 | C301, C402, C803 | 220 pF — [C315C221J5G5TA](https://www.digikey.com/en/products/detail/kemet/C315C221J5G5TA/6562497) | 220 pF C0G, 5%, 50 V; P2.54 mm. |
| 2 | C102, C202 | 33 nF — [R82EC2330AA50J](https://www.digikey.com/en/products/detail/kemet/R82EC2330AA50J/2571333) | 33 nF polyester film, 5%, 100 V; P5 mm; nominal body 7.2 x 2.5 mm. |
| 5 | C101, C106, C201, C206, C401 | [Nichicon 3.3uF / 50V FW audio electrolytic capacitor, radial](https://en.uraltone.com/catalogsearch/result/?q=518-003-1H5X11UFW) | 3.3 uF / 50 V Nichicon FW; nominal D5 x H11 mm, P2.5 mm; polarised. |
| 1 | C702 | 47 pF — [C315C470J5G5TA](https://www.digikey.com/en/products/detail/kemet/C315C470J5G5TA/3725986) | 47 pF C0G, 5%, 50 V; P2.54 mm. |
| 2 | C105, C205 | 4.7 nF — [R82EC1470AA50J](https://www.digikey.com/en/products/detail/kemet/R82EC1470AA50J/2571340) | 4.7 nF polyester film, 5%, 100 V; P5 mm; nominal body 7.2 x 2.5 mm. |
| 1 | C305 | [Panasonic 4.7uF 50V 5x11mm; UralTone518-P-4.7-50](https://en.uraltone.com/4-7uf-50v-panasonic-5x11mm-electrolytic-capacitor.html) | 4.7 uF / 50 V Panasonic; nominal D5 x H11 mm, P2.0 mm; polarised. |
| 4 | C404, C601, C603, C607 | [Nichicon 47uF / 50V electrolytic capacitor, radial](https://en.uraltone.com/catalogsearch/result/?q=518-047-1H6X11UFW) | 47 uF / 50 V Nichicon FW; nominal D6.3 x H11 mm, P2.5 mm; polarised. |
| 1 | C802 | 68 pF — [C315C680J5G5TA](https://www.digikey.com/en/products/detail/kemet/C315C680J5G5TA/12700720) | 68 pF C0G, 5%, 50 V; P2.54 mm. |

### Resistors

| Qty | References | Selected part / specification | Fit / electrical notes |
|---:|---|---|---|
| 2 | R413, R708 | 100 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 6 | R101, R201, R603, R701, R716, R804 | 1000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 9 | R110, R111, R112, R113, R210, R211, R212, R213, R715 | 10000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 14 | R102, R114, R202, R214, R304, R306, R401, R402, R403, R406, R411, R501, R705, R805 | 100 kohm — [MFR-25FBF52-100K](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-100K/13473) | Exact 100000 ohm, 1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 4 | R305, R408, R704, R707 | 1000000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 1 | R407 | 1.2 kohm — [MFR-25FTE52-1K2](https://www.digikey.com/en/products/detail/yageo/MFR-25FTE52-1K2/9139850) | Exact 1200 ohm, 1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 2 | R103, R203 | 120 kohm — [MFR-25FBF52-120K](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-120K/9138049) | Exact 120000 ohm, 1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 2 | R503, R801 | 20000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 1 | R502 | 200 kohm — [MFR-25FBF52-200K](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-200K/13547) | Exact 200000 ohm, 1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 1 | R409 | 2200 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 1 | R410 | 22 kohm — [MFR-25FBF52-22K](https://www.digikey.com/en/products/detail/yageo/MFR-25FBF52-22K/9138098) | Exact 22000 ohm, 1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 1 | R302 | [carbon composition 2.2 Mohm](https://en.uraltone.com/catalogsearch/result/?q=661-2M2) | 2.2 Mohm carbon composition, supplier SKU 661-2M2; tolerance and power rating not recorded in source BOM: confirm before selection. Dedicated P12.70 mm footprint; body envelope 9.25 x 3.6 mm. |
| 1 | R412 | 300000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 1 | R301 | 39 kohm — [MFR50SFTE52-39K](https://www.digikey.com/en/products/detail/yageo/MFR50SFTE52-39K/9151453) | Exact 39000 ohm, 1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 2 | R314, R315 | 4.7 ohm — [MFR50SFTE52-4R7](https://www.digikey.com/en/products/detail/yageo/MFR50SFTE52-4R7/9151582) | Exact 4.7 ohm, 1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 1 | R504 | 40 kohm — [CMF5540K000BHEB](https://www.digikey.com/en/products/detail/vishay-dale/CMF5540K000BHEB/3634122) | Exact 40000 ohm, 0.1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 3 | R106, R206, R404 | 4700 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 1 | R706 | 47000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 1 | R802 | 470000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 2 | R414, R415 | 50 kohm — [MFP50SBBE52-50K](https://www.digikey.com/en/products/detail/yageo/MFP50SBBE52-50K/9127584) | Exact 50000 ohm, 0.1%; axial P10.16 mm. Preserve selected part and verify its rated power/body against manufacturer data. |
| 4 | R108, R109, R208, R209 | 51000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 3 | R107, R207, R717 | 68000 ohm metal-film 0.25W <=1%, axial | Axial metal-film, 0.25 W, <=1%; body <=6.8 x 2.5 mm; form leads to P10.16 mm. |
| 2 | R601, R602 | 10 ohm — [NFR25H0001009JA500](https://www.digikey.com/en/products/detail/vishay-beyschlag-draloric-bc-components/NFR25H0001009JA500/7350581) | 10 ohm, 0.5 W, 5%, Vishay NFR25H flameproof/fusible. Maximum coated body 7.5 x 2.5 mm. Generic metal-film parts are not safety-equivalent. |

### Controls

| Qty | References | Selected part / specification | Fit / electrical notes |
|---:|---|---|---|
| 1 | RV402 | [Alpha RD902F dual B50K, SKU100895-B50K](https://www.exploding-shed.com/alpha-rd902f-dual-vertical/100895-B50K) | Dual linear 50k, 6.35 mm round shaft; exact variant seating/drill fit requires comparison. R414/R415 are exact 50k shunts. |
| 2 | RV404, RV801 | [UT RD901F B10K T18 shaft,624-UT-RD901F-40-15K-B10K](https://en.uraltone.com/ut-rd901f-40-15k-series-10k-lin-9mm-vertical-potentiometer.html) | Single linear 10k; 6 mm T18 knurled shaft. Drawing shows 2.5 mm pitch versus catalogue 2.54 mm; dry-fit common panel plane. |
| 3 | RV301, RV401, RV701 | [RV9 B100K linear D-shaft, SKU101018-B100K](https://www.exploding-shed.com/b100k-potentiometer-rv9-d-shaft/101018-B100K) | Single linear 100k; 6 mm D shaft; includes nut/washer. Verify common panel seating. |
| 1 | RV403 | 10 kohm — [CT-6EP103](https://www.digikey.fi/en/products/detail/nidec-components/CT-6EP103/738304) | Nidec 10k top-adjust cermet; 2.5 mm triangular pitch; nominal 7 x 7 x 5.8 mm, reserved envelope 7.3 x 7.3 x 6.1 mm. |
| 1 | SW201 | [Salecom SKS04SP, SKU100060](https://www.exploding-shed.com/salecom-sks04sp-sub-mini-spdt-on-on-pc/100060) | SPDT ON-ON; straight PCB terminals. |
| 1 | SW801 | [Salecom SKS07SP, SKU100061](https://www.exploding-shed.com/salecom-sks07sp-sub-mini-spdt-on-off-on-pc/100061) | SPDT ON-OFF-ON; straight PCB terminals. Check SKU and positions despite inconsistent seller prose. |

### Diodes, connectors and protection

| Qty | References | Selected part / specification | Fit / electrical notes |
|---:|---|---|---|
| 5 | D401, D402, D403, D702, D703 | [1N4148 (= 1N914)](https://en.uraltone.com/catalogsearch/result/?q=183-1N4148) | DO-35 axial; observe diode polarity, including D401 anode at gate. |
| 2 | D601, D602 | [1N5817 Schottky diode 20V, 1A](https://en.uraltone.com/catalogsearch/result/?q=183-1N5817) | 20 V, 1 A Schottky; observe polarity. |
| 4 | D301, D302, D303, D304 | [BAT85S-TAP](https://www.digikey.com/en/products/detail/vishay-general-semiconductor-diodes-division/BAT85S-TAP/3104127) | Vishay BAT85S-TAP, 30 V / 200 mA, DO-35; maximum capsule 3.9 x 1.7 mm; P7.62 mm. Body-envelope screening is not full assembly qualification. |
| 1 | FB601 | [BLM31PG121SN1L](https://www.digikey.com/en/products/detail/murata-electronics/BLM31PG121SN1L/584265) | 120 ohm at 100 MHz, DCR <=0.1 ohm, current >=0.5 A; 1206 SMD. |
| 1 | J601 | [Exploding Shed 100702 — 2x8 shrouded header](https://www.exploding-shed.com/2x8-shrouded-header/100702) | Vertical keyed/shrouded 2x8, 2.54 mm; verify actual housing seating, pin 1 and cable polarity. |
| 1 | J602 | [Samtec TSW-120-15-G-D cut to 2x3](https://www.digikey.com/en/products/detail/samtec-inc/TSW-120-15-G-D/2686005) | One 2x3 section cut from ONE shared 2x20 TSW-120-15-G-D strip per module; that same strip also supplies J604. Keep 13.21 mm mating posts intact. |
| 1 | J603 | [SSW-103-01-G-D](https://www.digikey.com/en/products/detail/samtec-inc/SSW-103-01-G-D/1112055) | 2x3, 2.54 mm; 8.51 mm socket body. Mate with J602; dry-fit at 20 mm PCB-surface gap. |
| 1 | J604 | [Samtec TSW-120-15-G-D cut to 2x6](https://www.digikey.com/en/products/detail/samtec-inc/TSW-120-15-G-D/2686005) | One 2x6 section from the SAME 2x20 strip as J602; no second full strip required. Keep 13.21 mm mating posts intact. |
| 1 | J605 | [SSW-106-01-G-D](https://www.digikey.com/en/products/detail/samtec-inc/SSW-106-01-G-D/1112052) | 2x6, 2.54 mm; 8.51 mm socket body. Mate with J604; dry-fit at 20 mm PCB-surface gap. |
| 4 | J301, J302, J701, J702 | [Qingpu WQP518MA, Exploding Shed 100515](https://www.exploding-shed.com/thonkiconn-mono-wqp518ma/100515) | Vertical switched mono PCB jack; effective body height 10 mm, M6x0.5 thread; four separate nuts required. Not WQP518MA-BM. |
| 1 | D701 | [WP3A8ID](https://www.digikey.com/en/products/detail/kingbright/WP3A8ID/1747618) | Red diffused 3 mm LED; set panel height before trimming leads. |
| 2 | F601, F602 | [MF-R020-2](https://www.digikey.com/en/products/detail/bourns-inc/MF-R020-2/2561642) | 200 mA hold / 400 mA trip, 60 V radial PTC; D7.4 x T3.1 mm, P5.1 mm, maximum seated height 12.7 mm. Hold current is not an instantaneous limit. |
| 1 | F603 | [1206L025/24YR](https://www.digikey.com/en/products/detail/littelfuse-inc/1206L025-24YR/14320017) | 250 mA hold, 24 V; 1206 SMD with selected Littelfuse land pattern. |

## Additional assembly hardware

These are **additional to the 157 schematic positions**. Mounting holes are not purchased components. A complete module also needs separate CORE and CONTROL PCBs and a front panel; see the [build](../../docs/BUILD.md#fabrication) and [panel](../../mechanical/README.md) notes.

| Qty / module | Required item | Selection and fit notes |
|---:|---|---|
| 4 | M6x0.5 jack nuts | Exploding Shed 100518P020; WQP518MA nuts are separate. |
| 1 | 16-to-16 Eurorack cable, 20 cm | Exploding Shed 1009151620. Ten-conductor cable cannot supply required bus +5 V. Check real stripe/key continuity. |
| 4 | M2 female-female 20 mm board-stack standoffs | Wurth 970200244; nominal prototype choice, requires dry-fit and metal-to-copper isolation check. |
| 8 | M2x5 mm pan-head screws | BFirst MPMS 002 0005 PH; two per board-stack standoff. Verify thread engagement and avoid bottoming/nearby copper. |
| 7 | DIP8 sockets, 2.54 mm pitch / 7.62 mm row spacing | ED08DT candidate; for U101, U304, U302, U401, U402, U701, U702. Check low-profile seating. |
| 2 | DIP16 sockets, 2.54 mm pitch / 7.62 mm row spacing | ED16DT candidate; for U301 and U201. U201 uses only selected holes: never replace it with DIP8. |
| 2 | Rack screws and protective washers | Match actual M3/M2.5 case rail threads; panel slots do not determine the thread. |
| As needed | Insulating washers / films | Check every metal head/post against copper; soldermask alone is not robust insulation. |

### Conditional supports and optional knobs

| Qty / module | Item | Qualification still needed |
|---:|---|---|
| 4, conditional | M2 panel supports, nominally around 10 mm | Wurth 970100244 is a candidate only. Measure common control seating and select joints at the occupied PCB mounting points; two female spacers cannot simply share opposing ordinary screws. |
| 3, optional | Knobs for 6 mm D shafts | RV301, RV401, RV701. Check skirt clearance and flat orientation. |
| 2, optional | Knobs for 6 mm T18 knurled shafts | RV404, RV801. These are not D shafts. |
| 1, optional | 6.35 mm round-bore set-screw knob | RV402 CHARACTER; exact bore/skirt selection remains open. |

## Connector and assembly limits

**ONE 2x20 Samtec TSW-120-15-G-D strip supplies both J602 (2x3) and J604 (2x6) per module**, allowing sacrificial rows when cutting. Their quantities above count fitted sections, not separate full strips. Do not shorten the 13.21 mm mating posts. With the 2.54 mm male insulator and 8.51 mm SSW body, the nominal 20 mm free PCB-surface gap gives 4.26 mm insertion (specified range 3.68–6.35 mm). Verify actual seating/tolerances before soldering; standoffs carry the mechanical load.

Extra spacing under standoff ends reduces contact insertion; nominal insertion drops below 3.68 mm above a 20.58 mm gap, before tolerances. Outer screw-head washers do not change the inner gap. Common control seating, solder fillets, trimmed leads, panel-support joints and knob skirts need a physical fit check. Body-envelope screening for BAT85S and NFR25H does not establish collision-free assembly. Use protected/current-limited first-power commissioning as described in the build notes.
