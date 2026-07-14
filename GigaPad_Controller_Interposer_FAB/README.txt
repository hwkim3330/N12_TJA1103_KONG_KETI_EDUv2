GigaPad Universal Controller Interposer

This folder contains the fabrication outputs for the 42 x 30 mm straight-through controller interposer.
J1 HOST and J2 MODULE are single-row 2.54 mm, 10-pin headers.

Pin order, from pin 1 to pin 10:
3V3, 5V, GND, UART_TX, UART_RX, I2C_SDA, I2C_SCL, BOOT, GPIO_A, GPIO_B

Do not bridge 3V3 and 5V. Use a module-specific adapter for ESP32 DevKit/WROOM,
ESP32-CAM, Arduino Pro Mini, or XIAO. This interposer is not itself a USB or
wireless controller.
