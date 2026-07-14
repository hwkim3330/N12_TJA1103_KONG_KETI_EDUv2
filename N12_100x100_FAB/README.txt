N12 100x100 mixed fabrication panel

This panel contains the KETI TJA1103 board, the 3-key GigaPad ESP32-onboard carrier, and two MATEnet 2-wire breakouts.

Upload the complete ZIP to the PCB manufacturer only after selecting the intended ESP32-WROOM module and confirming the assembly BOM. The panel is 100 mm x 100 mm; the controller socket is on the GigaPad PCB and no external interposer is required.

Verification: the KETI board, GigaPad ESP32 carrier, and both MATEnet dongles each report 0 DRC violations and 0 unconnected pads in KiCad 10.0.4. Panel-level courtyard, silkscreen, library, and cross-board net checks are excluded because this file contains four electrically independent boards; use the individual-board reports as the electrical acceptance test.
