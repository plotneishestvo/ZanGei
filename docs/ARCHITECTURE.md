# Architecture

ZanGei is an experimental **8HP / 3U mono analog bucket-brigade delay**. A bucket-brigade device (BBD) transfers sampled analog charge under a two-phase clock; it is not a digital audio delay. The design favours texture, modulation and feedback character over transparent reproduction. It was inspired by the [Erica Synths EDU BBD project](https://www.ericasynths.lv/shop/diy-kits-1/edu-diy-bbd/).

**Implementation authority:** [`schematics/BBD_Buffer.kicad_pro`](../schematics/BBD_Buffer.kicad_pro), its root schematic and seven linked electrical sheets. This document describes that topology, not a hardware-tested specification. Complete assembly, calibration and performance measurements remain outstanding.

## Audio path

1. **Input and dry branch — `Input_IO.kicad_sch`.** U701A buffers the incoming signal. Its fixed-unity DRY_AUDIO tap feeds the final dry/wet control independently of INPUT. C701 and RV701 attenuate the signal sent toward the delay input summer, U701B. The summer combines that input with FEEDBACK_RETURN; an input limiter and clip indicator accompany this path. INPUT is delay drive, not a master dry-volume control.
2. **First delay — `BBD1_V3208.kicad_sch`.** U101 is a 2048-stage Coolaudio V3208D. Its input conditioning/bias and output loading, discrete followers, summing and filtering form the first delay branch, ending at BBD1_SUM.
3. **Second delay — `BBD2_V3205.kicad_sch`.** U201 is a 4096-stage Coolaudio V3205SD. SW201 selects its source: AUDIO_IN_BBD for parallel operation, or BBD1_SUM for series operation. Each branch retains its own input and reconstruction network. Series operation adds the first delay before the second; it is not a switch at the final output.
4. **Tap blend and shared sample-and-hold — `Wet_Feedback.kicad_sch`.** RV401 blends BBD1_SUM and BBD2_SUM into WET_MIX. U402A buffers the blend before the shared Q401/C403 sample-and-hold (S&H), and U402B buffers the held node into OUT_SH. S&H is an analog switch and hold capacitor used here for reconstruction; there is one shared stage after tap blending, not one per BBD.
5. **Wet recovery and output — `Output_Mix.kicad_sch`.** OUT_SH feeds U702A's wet recovery amplifier. SW801 selects additional feedback capacitance in this amplifier for SOFT / OFF / DARK filtering; it is not a separate filter inserted ahead of the amplifier. RV801 blends recovered wet with DRY_AUDIO. U702B buffers that blend, followed by C804 output DC blocking and R804 output isolation to the output jack.

The two BBDs share a clock but have different stage counts. Their two internal output pins are alternating-phase outputs combined within each branch, not separate stereo outputs. The module has one audio input and one audio output.

## Feedback character

OUT_SH also feeds a separate return path, before the output-only wet-recovery/filter and DRY/WET controls:

**OUT_SH → CHARACTER low-pass → U401A diode-limited drive → AMOUNT → U401B return amplifier → input summer.**

RV402 is a dual-gang CHARACTER control: one gang changes the pre-drive filter and the other changes drive. Each 50k gang is shunted by an exact 50k resistor, giving nominal 25k endpoints with a deliberately nonlinear sweep. RV403 is an internal 10k drive-calibration trimmer, not a panel control. RV404 AMOUNT attenuates after the drive stage. Placing AMOUNT there reduces its interaction with distortion onset, but CHARACTER still affects loop gain; it is not perfectly independent tone/drive control.

R412 is the nominal return-gain calibration resistor. Recovery and loop gain remain prototype choices, not guarantees of calibrated unity, repeat count or stable self-oscillation. The final output's DRY/WET and SOFT/OFF/DARK settings do not sit in this feedback path.

## Clock and CV

`Clock_CV.kicad_sch` uses **CD4046BE U301** as the voltage-controlled oscillator and **TC4428AEPA U304** as the complementary clock driver. Shared phase lines clock both BBDs, and the clock network also supplies the S&H trigger circuitry. Correct amplitude and phase timing must be measured on the assembled prototype; complementary outputs alone do not certify the BBD clock cross-point requirement.

RV301 TIME and the external TIME CV feed the U302B control-voltage summer. The knob alone is intended to cover the local control range; external CV adds or subtracts, with accepted passive-knob/source-impedance interaction and endpoint clamping. This is not a calibrated V/oct interface. U302A is unused and safely parked as a follower.

INHIBIT CV controls the CD4046 inhibit input. Stopping its oscillator is not a dedicated audio mute or a guaranteed indefinite freeze: the dry path remains, and held analog charge can drift. There is no feedback-CV or dry/wet-CV circuit in v0.1.

## Panel controls

| Reference | Control | Role |
|---|---|---|
| RV701 | INPUT | Level sent into the delay/feedback summer; dry tap remains independent |
| RV301 / J302 | TIME / TIME CV | Shared delay-clock control |
| SW201 | PARALLEL / SERIES | Select the second BBD's input source |
| RV401 | Tap blend | Balance first and second reconstructed delay branches |
| RV402 | CHARACTER | Coupled feedback pre-filter and drive |
| RV404 | AMOUNT | Feedback level after drive |
| RV801 | DRY/WET | Final output blend |
| SW801 | SOFT / OFF / DARK | Extra filtering in the output wet-recovery stage |
| J301 | INHIBIT CV | Stop the clock oscillator |
| D701 | Clip LED | Progressive input-level indication; threshold usefulness remains to be measured |

## Physical and power architecture

The two **37.5 × 110 mm** boards stack behind a **40.3 × 128.5 mm** panel. CONTROL carries panel hardware and the input, feedback, CV-summing and output circuitry; CORE carries the BBD stages, clock generation/driver, S&H circuitry and power entry. The wet/feedback schematic sheet spans physical boards: a schematic page is not a PCB partition.

A 2×3 interconnect carries local power and a 2×6 interconnect carries signals. The working PCB shows the boards side by side for editing; electrical links between regions represent those connectors, not missing tracks to route across the gap. See [stack dimensions and pin maps](BUILD.md#stack-and-connector-engagement).

`Power_Stack.kicad_sch` takes **±12 V and +5 V from a 16-conductor Eurorack bus**. The op-amps use ±12 V; BBD/clock circuitry uses local +5 V. Each supply path includes the selected protection/filtering parts. There is no local +12-to-5 V regulator. R603 is a defined +5 V bleed/load for discharge and small clamp-injected currents, not a series voltage dropper. Neither protection components nor a keyed connector make a miswired power ribbon safe.

## Validation boundary

- Breadboard work and simulations informed the circuit; these do not constitute testing of the assembled module.
- Schematic connectivity and routed-board checks are distinct from analog performance and safety qualification.
- Existing opposite-face PTH/courtyard interactions and crowded silkscreen remain documented prototype constraints. Zero local opens is not clean full DRC or proof of solder access.
- Component models include conservative envelopes and generic families. Connector engagement must use the selected long-post dimensions rather than the ordinary header models currently attached in KiCad.
- Panel seating, trimmed leads, connector insertion, spacer isolation and final case depth require physical checks. Protected/current-limited commissioning must precede ordinary rack use.

See the [build notes](BUILD.md), [current BOM](../bom/v0.1/BOM.md) and [datasheet index](datasheets/README.md). No unpublished design notebook is required to understand or open the public design.
