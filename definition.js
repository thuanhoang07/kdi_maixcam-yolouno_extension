Blockly.Python['get_object_center'] = function(block) {
  var axis = block.getFieldValue('AXIS');
  var index = Blockly.Python.valueToCode(block, 'INDEX', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'cam.get_object_center(' + index + ')[' + axis + ']';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Block để lấy dữ liệu theo tên label
Blockly.Blocks['get_data_by_label'] = {
  init: function () {
    this.jsonInit({
      type: "get_data_by_label",
      message0: "lấy %1 của %2",
      args0: [
        {
          type: "field_dropdown",
          name: "FIELD",
          options: [
            ["x", '"x"'],
            ["y", '"y"'],
            ["chiều rộng", '"w"'],
            ["chiều cao", '"h"']
          ]
        },
        {
          type: "input_value",
          name: "LABEL",
          check: "String"
        }
      ],
      output: "Number",
      colour: 230,
      tooltip: "Lấy thông tin từ vật thể theo tên (ví dụ: person, car, tv)",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_data_by_label'] = function(block) {
  var field = block.getFieldValue('FIELD');
  var label = Blockly.Python.valueToCode(block, 'LABEL', Blockly.Python.ORDER_ATOMIC) || '""';
  var code = 'cam.get_object_by_label(' + label + ', ' + field + ')';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Block để kiểm tra có phát hiện label cụ thể không
Blockly.Blocks['has_label'] = {
  init: function () {
    this.jsonInit({
      type: "has_label",
      message0: "phát hiện %1 ?",
      args0: [
        {
          type: "input_value",
          name: "LABEL",
          check: "String"
        }
      ],
      output: "Boolean",
      colour: 230,
      tooltip: "Kiểm tra xem có phát hiện vật thể với tên cụ thể không",
      helpUrl: ""
    });
  }
};

Blockly.Python['has_label'] = function(block) {
  var label = Blockly.Python.valueToCode(block, 'LABEL', Blockly.Python.ORDER_ATOMIC) || '""';
  var code = '(cam.find_object_by_label(' + label + ') >= 0)';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Block để đếm số lượng object với label cụ thể
Blockly.Blocks['count_label'] = {
  init: function () {
    this.jsonInit({
      type: "count_label",
      message0: "số lượng %1",
      args0: [
        {
          type: "input_value",
          name: "LABEL",
          check: "String"
        }
      ],
      output: "Number",
      colour: 230,
      tooltip: "Đếm số lượng vật thể với tên cụ thể",
      helpUrl: ""
    });
  }
};

Blockly.Python['count_label'] = function(block) {
  var label = Blockly.Python.valueToCode(block, 'LABEL', Blockly.Python.ORDER_ATOMIC) || '""';
  var code = 'len(cam.find_all_objects_by_label(' + label + '))';
  return [code, Blockly.Python.ORDER_ATOMIC];
};Blockly.Blocks['init_camera_uart'] = {
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
      colour: 230,
      tooltip: "Khởi tạo kết nối camera qua UART",
      helpUrl: ""
    });
  }
};

Blockly.Python['init_camera_uart'] = function(block) {
  var baudrate = block.getFieldValue('BAUDRATE');
  var tx = block.getFieldValue('TX');
  var rx = block.getFieldValue('RX');
  Blockly.Python.definitions_['import_riscv_camera'] = 'from camera_riscv import *';
  Blockly.Python.definitions_['create_riscv_camera'] = 'cam = CameraUART(baudrate=' + baudrate + ', tx=' + tx + '_PIN, rx=' + rx + '_PIN)\n';
  var code = '';
  return code;
};

// Block để lấy số lượng objects
Blockly.Blocks['get_object_count'] = {
  init: function () {
    this.jsonInit({
      type: "get_object_count",
      message0: "số lượng vật thể phát hiện",
      output: "Number",
      colour: 230,
      tooltip: "Trả về số lượng vật thể được phát hiện",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_object_count'] = function(block) {
  var code = 'cam.get_object_count()';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Block để lấy dữ liệu từ object cụ thể
Blockly.Blocks['get_object_data'] = {
  init: function () {
    this.jsonInit({
      type: "get_object_data",
      message0: "lấy %1 của vật thể thứ %2",
      args0: [
        {
          type: "field_dropdown",
          name: "FIELD",
          options: [
            ["tên", '"label"'],
            ["tọa độ x", '"x"'],
            ["tọa độ y", '"y"'],
            ["chiều rộng", '"w"'],
            ["chiều cao", '"h"']
          ]
        },
        {
          type: "input_value",
          name: "INDEX",
          check: "Number"
        }
      ],
      output: null,
      colour: 230,
      tooltip: "Lấy thông tin từ vật thể cụ thể (đánh số từ 0)",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_object_data'] = function(block) {
  var field = block.getFieldValue('FIELD');
  var index = Blockly.Python.valueToCode(block, 'INDEX', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'cam.get_object_data(' + index + ', ' + field + ')';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Block để kiểm tra có phát hiện vật thể không
Blockly.Blocks['has_objects'] = {
  init: function () {
    this.jsonInit({
      type: "has_objects",
      message0: "phát hiện vật thể?",
      output: "Boolean",
      colour: 230,
      tooltip: "Kiểm tra xem có phát hiện vật thể nào không",
      helpUrl: ""
    });
  }
};

Blockly.Python['has_objects'] = function(block) {
  var code = 'cam.has_objects()';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Block để lấy tọa độ trung tâm của object
Blockly.Blocks['get_object_center'] = {
  init: function () {
    this.jsonInit({
      type: "get_object_center",
      message0: "tọa độ trung tâm %1 của vật thể thứ %2",
      args0: [
        {
          type: "field_dropdown",
          name: "AXIS",
          options: [
            ["x", "0"],
            ["y", "1"]
          ]
        },
        {
          type: "input_value",
          name: "INDEX",
          check: "Number"
        }
      ],
      output: "Number",
      colour: 230,
      tooltip: "Lấy tọa độ trung tâm của vật thể",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_object_center'] = function(block) {
  var axis = block.getFieldValue('AXIS');
  var index = Blockly.Python.valueToCode(block, 'INDEX', Blockly.Python.ORDER_ATOMIC) || '0';
  var code = 'cam.get_object_center(' + index + ')[' + axis + ']';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Block cũ để tương thích ngược
Blockly.Blocks['get_camera_data'] = {
  init: function () {
    this.jsonInit({
      type: "get_camera_data",
      message0: "lấy dữ liệu %1 từ camera",
      args0: [
        {
          type: "field_dropdown",
          name: "FIELD",
          options: [
            ["label", "0"],
            ["x", "1"],
            ["y", "2"],
            ["w", "3"],
            ["h", "4"]
          ]
        }
      ],
      output: "String",
      colour: 230,
      tooltip: "Trả về giá trị được chọn từ vật thể đầu tiên",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_camera_data'] = function(block) {
  const field = block.getFieldValue('FIELD');
  var code = 'cam.get_data(' + parseInt(field) + ')';
  return [code, Blockly.Python.ORDER_ATOMIC];
};