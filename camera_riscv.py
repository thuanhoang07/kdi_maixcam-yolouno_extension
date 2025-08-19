from machine import UART
import ujson as json
import time

class CameraUART:
    def __init__(self, uart_id=2, tx=17, rx=16, baudrate=115200):
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx, rx=rx, timeout=100)
        self.uart.init(parity=None, stop=1, bits=8)
        self.last_objects = []
        self.count = 0
        self.model_labels = []  # Danh sách nhãn từ model
        time.sleep(0.2)
    
    def update(self):
        """Đọc và phân tích dữ liệu JSON từ UART"""
        if self.uart.any():
            try:
                raw = self.uart.readline()
                if raw:
                    line = raw.decode().strip()
                    data = json.loads(line)
                    
                    # Xử lý response danh sách nhãn
                    if "l" in data:
                        self.model_labels = data["l"]
                        print(f"[CameraUART] Received {len(self.model_labels)} labels from model")
                    
                    # Xử lý dữ liệu objects bình thường
                    elif "c" in data and "o" in data:
                        self.count = data["c"]
                        self.last_objects = data["o"]
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
    
    # ========== PHƯƠNG THỨC ĐỌC DỮ LIỆU ĐÃ XỬ LÝ ==========
    
    def get_label(self, index):
        """Trả về label của object tại vị trí index"""
        obj = self.get_object(index)
        return obj.get("l", "") if obj else ""
    
    def get_center_x(self, index):
        """Trả về tọa độ x trung tâm của object (đã được MaixCAM tính sẵn)"""
        obj = self.get_object(index)
        return obj.get("x", 0) if obj else 0
    
    def get_center_y(self, index):
        """Trả về tọa độ y trung tâm của object (đã được MaixCAM tính sẵn)"""
        obj = self.get_object(index)
        return obj.get("y", 0) if obj else 0
    
    def get_w(self, index):
        """Trả về chiều rộng của object"""
        obj = self.get_object(index)
        return obj.get("w", 0) if obj else 0
    
    def get_h(self, index):
        """Trả về chiều cao của object"""
        obj = self.get_object(index)
        return obj.get("h", 0) if obj else 0
    
    def get_center(self, index):
        """Trả về tuple (center_x, center_y) của object"""
        return (self.get_center_x(index), self.get_center_y(index))
    
    def get_area(self, index):
        """Trả về diện tích của object"""
        obj = self.get_object(index)
        if obj:
            return obj.get("w", 0) * obj.get("h", 0)
        return 0
    
    def print_model_labels(self):
        """Yêu cầu và in danh sách nhãn của model ra terminal"""
        # Gửi request đến MaixCAM
        request = json.dumps({"request": "get_labels"})
        self.uart.write((request + "\n").encode())
        print("[CameraUART] Requesting model labels...")
        
        # Chờ và đọc response
        timeout = 3000  # 3 giây timeout
        start_time = time.ticks_ms()
        
        while time.ticks_diff(time.ticks_ms(), start_time) < timeout:
            self.update()
            if self.model_labels:
                # In danh sách nhãn ra terminal
                print("=== MODEL LABELS ===")
                print(f"Total labels: {len(self.model_labels)}")
                print("Available labels:")
                for i, label in enumerate(self.model_labels):
                    print(f"  {i}: {label}")
                print("==================")
                return
            time.sleep_ms(10)
        
        print("[CameraUART] Timeout: No response from MaixCAM")

    def get_model_labels(self):
        """Trả về danh sách nhãn của model (nếu đã có)"""
        return self.model_labels


"""
from camera_riscv import *

cam = CameraUART(tx=D3_PIN, rx=D4_PIN, baudrate=115200)

async def task_t_F_U_N():
  while True:
    await asleep_ms(10)
    print('x' + ': ' + str((lambda: [cam.get_w(i) for i in range(cam.get_count()) if cam.get_label(i) == 'person'] or [0])()[0]))

async def setup():

  print('App started')
  print(cam.get_model_labels())

  create_task(task_t_F_U_N())

async def main():
  await setup()
  while True:
    await asleep_ms(100)

run_loop(main())

"""