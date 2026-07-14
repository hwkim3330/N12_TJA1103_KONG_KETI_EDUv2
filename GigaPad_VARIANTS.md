# GigaPad product variants

The product target is a compact, programmable macro keyboard in the same class as the TechKeys SixKeyBoard, with an on-board controller socket. The next fabrication variant is a 3-key board so the controller can be physically mounted on the same PCB without colliding with the switches.

## Files

- `GigaPad6_MX.kicad_pcb` — base USB + BLE six-key macro pad.
- `GigaPad6_MX_Sense.kicad_pcb` — Sense option for the XIAO nRF52840 Sense microphone/IMU module.
- `GigaPad6_MX_LowProfile.kicad_pcb` — alternate low-profile assembly placeholder; use low-profile switches and caps during assembly.
- `GigaPad3_ProMini_Onboard.kicad_pcb` — 3-key, same-board Arduino Pro Mini socket; validated 0 DRC / 0 unconnected.
- `GigaPad3_ESP32_Onboard.kicad_pcb` — 3-key, same-board ESP32-WROOM carrier socket; validated 0 DRC / 0 unconnected.
- `GigaPad_Controller_Interposer.kicad_pcb` — legacy prototype only; do not use for the final product.

## Controller compatibility target

The final controller interface is on the keypad PCB itself. The 3-key revision will use alternate, mutually exclusive on-board socket footprints for:

- Arduino Pro Mini 3.3 V or 5 V variants
- ESP32 module/DevKit carrier footprint selected for the exact board revision
- ESP32-CAM carrier footprint only when the exact camera board is confirmed
- XIAO nRF52840 / XIAO Sense as an alternate assembly

The socket must expose separate 3V3 and 5V rails, GND, UART TX/RX, boot/program control, I2C, and spare GPIO. A 5 V Arduino Pro Mini must never be powered from the 3V3 rail. The exact ESP32-CAM direct footprint remains board-specific and must be selected from the physical module variant before fabrication.

## Product-level requirements

- USB-C wired HID for controllers with native USB.
- BLE HID for ESP32/XIAO-capable controllers.
- Standard 19.05 mm Cherry MX switch pitch.
- Per-key LED provision and a matrix-capable expansion path for the 9-key variant.
- Web-based macro configuration in the firmware layer; the PCB must expose a reliable programming/UART path.
- No unverified direct connection to camera or SD-reserved ESP32-CAM pins.

The ZMK configuration remains shared: USB/BLE, macros, mouse emulation, and runtime keymap configuration through ZMK Studio. The Sense microphone/IMU is optional; the base board remains usable without it.

The current base board was routed with the external Java-free KiCadRoutingTools A* engine and verified with KiCad 10.0.4 CLI: 0 DRC violations and 0 unconnected items. The Sense and LowProfile files are electrically identical validated copies; their assembly options still need their own BOM/3D checks before fabrication. The 100x100 mixed panel remains a manufacturing panel, not the final retail keyboard enclosure.
