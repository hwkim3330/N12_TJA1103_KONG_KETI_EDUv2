# GigaPad controller adapters

`GigaPad_Controller_Interposer.kicad_pcb` is the common electrical interface. J1 is the keyboard-side host and J2 is the module-side connector. Both are single-row 2.54 mm, 10-pin headers with straight-through routing.

| Pin | Signal | Purpose |
|---:|---|---|
| 1 | 3V3 | 3.3 V rail |
| 2 | 5V | USB/bus 5 V rail |
| 3 | GND | Ground |
| 4 | UART_TX | Programming/serial |
| 5 | UART_RX | Programming/serial |
| 6 | I2C_SDA | Optional expansion |
| 7 | I2C_SCL | Optional expansion |
| 8 | BOOT | Module boot/program control |
| 9 | GPIO_A | Key matrix/optional input |
| 10 | GPIO_B | Key matrix/optional input |

The interposer intentionally does not pretend that every ESP32 board has the same pinout. The following module adapters are separate designs:

- ESP32 DevKit/WROOM: BLE/UART-capable adapter; wired USB requires a board with native USB or a USB-UART path.
- ESP32-CAM: adapter must be selected for the exact camera board revision; camera and SD-reserved pins are not assumed to be free.
- Arduino Pro Mini: select 3.3 V or 5 V at the adapter and use the UART header for programming.
- XIAO nRF52840/Sense: existing carrier remains supported.

Never bridge pins 1 and 2. The correct rail is selected on the module adapter, not on the straight-through interposer.
