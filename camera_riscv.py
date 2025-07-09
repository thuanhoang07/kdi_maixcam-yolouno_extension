from machine import UART
import time
import ujson as json  # Bắt buộc phải có ujson

class CameraUART:
    def __init__(self, uart_id=2, tx=17, rx=16, baudrate=115200):
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx, rx=rx, timeout=100)
        self.uart.init(parity=None, stop=1, bits=8)
        self.objects = []  # List of detected objects
        self.buffer = ""  # Buffer for incomplete JSON
        time.sleep(0.2)

    def update(self):
        """Read and parse JSON data from UART"""
        if self.uart and self.uart.any():
            try:
                # Read available data
                raw = self.uart.read()
                if raw:
                    # Add to buffer
                    self.buffer += raw.decode('utf-8', errors='ignore')
                    
                    # Process complete JSON objects (ending with newline)
                    while '\n' in self.buffer:
                        json_line, self.buffer = self.buffer.split('\n', 1)
                        json_line = json_line.strip()
                        
                        if json_line:
                            try:
                                # Parse JSON using ujson
                                data = json.loads(json_line)
                                
                                # Update objects list
                                if "count" in data and "objects" in data:
                                    self.objects = data["objects"]
                                    
                            except ValueError as e:  # ujson raises ValueError
                                print(f"JSON parse error: {e}")
                            except Exception as e:
                                print(f"Error processing data: {e}")
                                        
            except Exception as e:
                print(f"CameraUART error: {e}")

    def get_object_count(self):
        """Get number of detected objects"""
        self.update()
        return len(self.objects)

    def get_object_data(self, object_index, field):
        """Get data from specific object
        object_index: index of object (0 to count-1)
        field: "label", "x", "y", "w", "h"
        """
        self.update()
        
        if 0 <= object_index < len(self.objects):
            obj = self.objects[object_index]
            if field in obj:
                return obj[field]
        
        return "" if field == "label" else 0

    def get_all_objects(self):
        """Get list of all detected objects"""
        self.update()
        return self.objects

    def has_objects(self):
        """Check if any objects are detected"""
        self.update()
        return len(self.objects) > 0

    def get_object_center(self, object_index):
        """Get center coordinates of object"""
        if 0 <= object_index < len(self.objects):
            obj = self.objects[object_index]
            center_x = obj['x'] + obj['w'] // 2
            center_y = obj['y'] + obj['h'] // 2
            return center_x, center_y
        
        return 0, 0
    
    def find_object_by_label(self, label):
        """Find first object with specific label
        Returns index or -1 if not found"""
        self.update()
        for i, obj in enumerate(self.objects):
            if obj.get('label') == label:
                return i
        return -1
    
    def find_all_objects_by_label(self, label):
        """Find all objects with specific label
        Returns list of indices"""
        self.update()
        indices = []
        for i, obj in enumerate(self.objects):
            if obj.get('label') == label:
                indices.append(i)
        return indices
    
    def get_object_by_label(self, label, field):
        """Get data from first object with specific label
        field: "label", "x", "y", "w", "h"
        """
        index = self.find_object_by_label(label)
        if index >= 0:
            return self.get_object_data(index, field)
        return "" if field == "label" else 0
    
    # Compatibility methods for old interface
    def get_data(self, index):
        """Legacy method for compatibility
        index: 0=label, 1=x, 2=y, 3=w, 4=h
        """
        field_map = {0: "label", 1: "x", 2: "y", 3: "w", 4: "h"}
        if index in field_map:
            return self.get_object_data(0, field_map[index])
        return "" if index == 0 else 0