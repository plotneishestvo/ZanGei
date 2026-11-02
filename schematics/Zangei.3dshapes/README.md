# ZanGei review models

All files here are project-local **review approximations**, not certified vendor CAD. Body dimensions are selected-part/drawing based where known; conservative envelopes and illustrative shafts/lead forming are used where qualification is incomplete. Read [MODEL_MANIFEST.json](MODEL_MANIFEST.json) per model. Presence of a model does not validate the PCB footprint, common panel plane, connector engagement, solder access or stack clearance.

Coloured `.wrl` meshes are linked from the actual PCB/custom footprint library. Coordinates are converted from millimetres to KiCad VRML units (2.54mm), with PCB-local Y inverted into model Y. Available sibling `.step` files support solid export; KiCad STEP export can use `--subst-models` to substitute them. Historical solid checks are not a current whole-assembly validation. STEP export renders these generated shapes grey in KiCad; VRML retains body colours.

The generated FreeCAD model-collection document is not needed to open KiCad and is kept local-only. Retain the actual STEP/VRML files. The local footprint containing `NoModel` in its legacy library name now has a preview model; its identifier is intentionally retained to preserve schematic/PCB association.

Do not attach IC-body overlays by matching the substring `Socket`: connector `PinSocket` footprints are not IC sockets. Only DIP/V3205 IC packages receive chip-body overlays.

Actual main PCB: [`../BBD_Buffer.kicad_pcb`](../BBD_Buffer.kicad_pcb). See [stack/model limitations](../../docs/BUILD.md#stack-and-connector-engagement) and [assembly access](../assembly/README.md). Generic KiCad connector models do not represent the selected long-post Samtec variant; check its dimensions rather than trusting apparent model engagement.
