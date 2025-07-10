// Khối lấy số lượng objects
Blockly.Blocks['get_object_count'] = {
  init: function () {
    this.jsonInit({
      type: "get_object_count",
      message0: "số lượng objects",
      output: "Number",
      colour: "#cb2026",
      tooltip: "Trả về số lượng objects được phát hiện",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_object_count'] = function(block) {
  var code = 'cam.get_count()';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Khối khởi tạo camera UART
Blockly.Blocks['init_camera_uart'] = {
  init: function () {
    this.jsonInit({
      type: "init_camera_uart",
      message0: "khởi tạo camera UART TX %1 RX %2 baudrate %3",
      args0: [
        {
          type: "field_dropdown",
          name: "TX",
          options: digitalPins
        },
        {
          type: "field_dropdown",
          name: "RX",
          options: digitalPins
        },
        {
          type: "field_number",
          name: "BAUDRATE",
          value: 115200
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: "#cb2026",
      tooltip: "Khởi tạo kết nối camera qua UART",
      helpUrl: ""
    });
  }
};

Blockly.Python['init_camera_uart'] = function(block) {
  var tx = block.getFieldValue('TX');
  var rx = block.getFieldValue('RX');
  var baudrate = block.getFieldValue('BAUDRATE');
  
  Blockly.Python.definitions_['import_riscv_camera'] = 'from camera_riscv import *';
  Blockly.Python.definitions_['create_riscv_camera'] = 'cam = CameraUART(tx=' + tx + '_PIN, rx=' + rx + '_PIN, baudrate=' + baudrate + ')';
  
  return '';
};

// Khối lấy thuộc tính của object theo label (ĐÃ CẬP NHẬT)
Blockly.Blocks['get_property_by_label'] = {
  init: function () {
    this.jsonInit({
      type: "get_property_by_label",
      message0: "lấy %1 của label %2",
      args0: [
        {
          type: "field_dropdown",
          name: "PROPERTY",
          options: [
            ["x trung tâm", "center_x"],
            ["y trung tâm", "center_y"],
            ["chiều rộng", "w"],
            ["chiều cao", "h"]
          ]
        },
        {
          type: "input_value",
          name: "LABEL",
          check: "String"
        }
      ],
      output: "Number",
      colour: "#cb2026",
      tooltip: "Lấy thông tin của object theo nhãn",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_property_by_label'] = function(block) {
  var property = block.getFieldValue('PROPERTY');
  var label = Blockly.Python.valueToCode(block, 'LABEL', Blockly.Python.ORDER_ATOMIC) || '""';
  
  // Tạo code để tìm object đầu tiên có label phù hợp và lấy property
  var code = '(lambda: [cam.get_' + property + '(i) for i in range(cam.get_count()) if cam.get_label(i) == ' + label + '] or [0])()[0]';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// ĐÃ BỎ khối get_center_by_label

// Khối lấy danh sách tất cả objects
Blockly.Blocks['get_all_objects'] = {
  init: function () {
    this.jsonInit({
      type: "get_all_objects",
      message0: "danh sách tất cả objects",
      output: "Array",
      colour: "#cb2026",
      tooltip: "Trả về list chứa tất cả objects được phát hiện",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_all_objects'] = function(block) {
  var code = 'cam.get_objects()';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Khối lấy object theo index
Blockly.Blocks['get_object_at_index'] = {
  init: function () {
    this.jsonInit({
      type: "get_object_at_index",
      message0: "object thứ %1",
      args0: [
        {
          type: "input_value",
          name: "INDEX",
          check: "Number"
        }
      ],
      output: "Object",
      colour: "#cb2026",
      tooltip: "Trả về dictionary chứa thông tin object (label, x, y, w, h)",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_object_at_index'] = function(block) {
  var index = Blockly.Python.valueToCode(block, 'INDEX', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'cam.get_object(' + index + ')';
  return [code, Blockly.Python.ORDER_ATOMIC];
};