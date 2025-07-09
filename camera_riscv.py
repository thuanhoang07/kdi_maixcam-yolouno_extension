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
import asyncio

# Khởi tạo UART tương ứng
cam = CameraUART(tx=D3_PIN, rx=D4_PIN)

async def read_objects():
    while True:
        await asyncio.sleep_ms(50)
        count = cam.get_count()
        
        if count > 0:
            print(f"Detected {count} objects:")
            
            # Duyệt qua từng object bằng index
            for i in range(count):
                label = cam.get_label(i)
                x = cam.get_x(i)
                y = cam.get_y(i)
                w = cam.get_w(i)
                h = cam.get_h(i)
                # Hiển thị thông tin (bỏ tracked vì không có trong thư viện)
                print(f" - {label}: x={x}, y={y}, w={w}, h={h}")
                
                # Có thể thêm logic xử lý cho từng object ở đây
                # Ví dụ: điều khiển servo theo vị trí object
                if label == "person":
                    center_x = cam.get_center_x(i)
                    center_y = cam.get_center_y(i)
                    print(f"   Person center: ({center_x}, {center_y})")
                
        else:
            # Không có object nào được phát hiện
            print("No objects detected")

async def setup():
    print("App started")
    print("Listening for camera data...")
    
    # Tạo task để đọc dữ liệu camera
    asyncio.create_task(read_objects())

async def main():
    await setup()
    
    # Main loop - có thể thêm logic khác ở đây
    while True:
        await asyncio.sleep_ms(100)
        # Thêm các task khác nếu cần
        pass

# Chạy chương trình
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped")
except Exception as e:
    print(f"Error: {e}")

"""
