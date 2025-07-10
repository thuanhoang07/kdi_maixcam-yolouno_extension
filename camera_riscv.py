from machine import UART
import ujson as json
import time

class CameraUART:
    def __init__(self, uart_id=2, tx=17, rx=16, baudrate=115200):
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx, rx=rx, timeout=100)
        self.uart.init(parity=None, stop=1, bits=8)
        self.last_objects = []
        self.count = 0
        # Kích thước sẽ được tự động cập nhật từ model_info
        self.screen_width = None
        self.screen_height = None
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
                        
                        # Tự động cập nhật kích thước màn hình từ model_info
                        if "model_info" in data:
                            model_info = data["model_info"]
                            if "input_width" in model_info and "input_height" in model_info:
                                if self.screen_width is None or self.screen_height is None:
                                    print(f"[CameraUART] Detected model size: {model_info['input_width']}x{model_info['input_height']}")
                                self.screen_width = model_info["input_width"]
                                self.screen_height = model_info["input_height"]
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
    
    # ========== PHƯƠNG THỨC CHUYỂN ĐỔI TỌA ĐỘ ==========
    
    def _convert_x_to_center_origin(self, x):
        """Chuyển tọa độ x từ gốc góc trái trên về gốc giữa màn hình"""
        if self.screen_width is None:
            print("Warning: Screen width not detected yet, using default")
            return x - 160  # Fallback mặc định cho YOLO11
        return x - (self.screen_width // 2)
    
    def _convert_y_to_center_origin(self, y):
        """Chuyển tọa độ y từ gốc góc trái trên về gốc giữa màn hình (y âm ở trên, y dương ở dưới)"""
        if self.screen_height is None:
            print("Warning: Screen height not detected yet, using default")
            return 112 - y  # Fallback mặc định cho YOLO11
        return (self.screen_height // 2) - y
    
    # ========== PHƯƠNG THỨC MỚI ĐỂ ĐỌC CÁC GIÁ TRỊ RIÊNG BIỆT ==========
    
    def get_label(self, index):
        """Trả về label của object tại vị trí index"""
        obj = self.get_object(index)
        return obj.get("label", "") if obj else ""
    
    def get_x(self, index):
        """Trả về tọa độ x của object tại vị trí index (gốc góc trái trên)"""
        obj = self.get_object(index)
        return obj.get("x", 0) if obj else 0
    
    def get_y(self, index):
        """Trả về tọa độ y của object tại vị trí index (gốc góc trái trên)"""
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
        """Trả về tọa độ x trung tâm của object (gốc tọa độ ở giữa màn hình)"""
        obj = self.get_object(index)
        if obj:
            # Tính tọa độ x trung tâm theo gốc góc trái trên
            center_x_original = obj.get("x", 0) + obj.get("w", 0) // 2
            # Chuyển đổi về gốc tọa độ giữa màn hình
            return self._convert_x_to_center_origin(center_x_original)
        return 0
    
    def get_center_y(self, index):
        """Trả về tọa độ y trung tâm của object (gốc tọa độ ở giữa màn hình)"""
        obj = self.get_object(index)
        if obj:
            # Tính tọa độ y trung tâm theo gốc góc trái trên
            center_y_original = obj.get("y", 0) + obj.get("h", 0) // 2
            # Chuyển đổi về gốc tọa độ giữa màn hình
            return self._convert_y_to_center_origin(center_y_original)
        return 0
    
    def get_center(self, index):
        """Trả về tuple (center_x, center_y) của object với gốc tọa độ ở giữa màn hình"""
        return (self.get_center_x(index), self.get_center_y(index))
    
    def get_area(self, index):
        """Trả về diện tích của object"""
        obj = self.get_object(index)
        if obj:
            return obj.get("w", 0) * obj.get("h", 0)
        return 0


"""
from camera_riscv import *

# Khởi tạo camera (kích thước màn hình sẽ tự động được cập nhật từ model)
cam = CameraUART(tx=D3_PIN, rx=D4_PIN, baudrate=115200)

async def task_t_F_U_N():
  while True:
    await asleep_ms(10)
    # Ví dụ: in tọa độ trung tâm với gốc tọa độ ở giữa màn hình
    if cam.get_count() > 0:
        center_x = cam.get_center_x(0)  # Từ -160 đến +160
        center_y = cam.get_center_y(0)  # Từ -112 đến +112
        print(f'Object 0 center: ({center_x}, {center_y})')

async def setup():
  print('App started')
  create_task(task_t_F_U_N())

async def main():
  await setup()
  while True:
    await asleep_ms(100)

run_loop(main())
"""