from machine import UART
import ujson as json
import time

class CameraUART:
    def __init__(self, uart_id=2, tx=17, rx=16, baudrate=115200):
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx, rx=rx, timeout=100)
        self.uart.init(parity=None, stop=1, bits=8)
        self.last_objects = []
        self.count = 0
        time.sleep(0.2)
    
    def update(self):
        """Đọc và phân tích dữ liệu JSON từ UART"""
        if self.uart.any():
            try:
                raw = self.uart.readline()
                if raw:
                    line = raw.decode().strip()
                    data = json.loads(line)
                    if "count" in data and "objects" in data:
                        self.count = data["count"]
                        self.last_objects = data["objects"]
            except Exception as e:
                print("CameraUART JSON error:", e)
    
    def get_objects(self):
        """Gọi update rồi trả về danh sách vật thể"""
        self.update()
        return self.last_objects
    
    def get_count(self):
        """Gọi update rồi trả về số lượng vật thể"""
        self.update()
        return self.count
    
    def get_object(self, index):
        """Trả về object tại vị trí index"""
        self.update()
        if 0 <= index < len(self.last_objects):
            return self.last_objects[index]
        return None
    
    # ========== PHƯƠNG THỨC MỚI ĐỂ ĐỌC CÁC GIÁ TRỊ RIÊNG BIỆT ==========
    
    def get_label(self, index):
        """Trả về label của object tại vị trí index"""
        obj = self.get_object(index)
        return obj.get("label", "") if obj else ""
    
    def get_x(self, index):
        """Trả về tọa độ x của object tại vị trí index"""
        obj = self.get_object(index)
        return obj.get("x", 0) if obj else 0
    
    def get_y(self, index):
        """Trả về tọa độ y của object tại vị trí index"""
        obj = self.get_object(index)
        return obj.get("y", 0) if obj else 0
    
    def get_h(self, index):
        """Trả về chiều cao của object tại vị trí index"""
        obj = self.get_object(index)
        return obj.get("h", 0) if obj else 0
    
    def get_w(self, index):
        """Trả về chiều rộng của object tại vị trí index"""
        obj = self.get_object(index)
        return obj.get("w", 0) if obj else 0
    
    def get_center_x(self, index):
        """Trả về tọa độ x trung tâm của object"""
        obj = self.get_object(index)
        if obj:
            return obj.get("x", 0) + obj.get("w", 0) // 2
        return 0
    
    def get_center_y(self, index):
        """Trả về tọa độ y trung tâm của object"""
        obj = self.get_object(index)
        if obj:
            return obj.get("y", 0) + obj.get("h", 0) // 2
        return 0
    
    def get_center(self, index):
        """Trả về tuple (center_x, center_y) của object"""
        return (self.get_center_x(index), self.get_center_y(index))
    
    def get_area(self, index):
        """Trả về diện tích của object"""
        obj = self.get_object(index)
        if obj:
            return obj.get("w", 0) * obj.get("h", 0)
        return 0


"""
from camera_riscv import *

cam = CameraUART(tx=D3_PIN, rx=D4_PIN, baudrate=115200)

async def task_t_F_U_N():
  while True:
    await asleep_ms(10)
    print('x' + ': ' + str((str(cam.get_objects()) + '')))

async def setup():

  print('App started')

  create_task(task_t_F_U_N())

async def main():
  await setup()
  while True:
    await asleep_ms(100)

run_loop(main())

"""