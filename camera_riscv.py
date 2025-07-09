from machine import UART
import time

class CameraUART:
    def __init__(self, uart_id=2, tx=17, rx=16, baudrate=115200):
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx, rx=rx, timeout=100)
        self.uart.init(parity=None, stop=1, bits=8)
        self.last_data = ["", 0, 0, 0, 0]  # [label, x, y, w, h]
        time.sleep(0.2)

    def update(self):
        if self.uart and self.uart.any():
            try:
                raw = self.uart.readline()
                if raw:
                    line = raw.decode().strip()
                    parts = line.split(',')
                    if len(parts) == 5:
                        self.last_data = [
                            parts[0],
                            int(parts[1]),
                            int(parts[2]),
                            int(parts[3]),
                            int(parts[4])
                        ]
            except Exception as e:
                print("CameraUART error:", e)

    def get_data(self, index):
        self.update()
        return self.last_data[index]
