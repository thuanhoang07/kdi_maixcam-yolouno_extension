// Khối khởi tạo camera UART
Blockly.Blocks['init_camera_uart'] = {
  init: function () {
    this.jsonInit({
      type: "init_camera_uart",
      message0: "Khởi tạo kết nối UART với Maixcam TX %1 RX %2",
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
        }
      ],
      previousStatement: null,
      nextStatement: null,
      colour: "#cb2026",
      tooltip: "Khởi tạo kết nối camera qua UART (baudrate mặc định: 115200)",
      helpUrl: ""
    });
  }
};

Blockly.Python['init_camera_uart'] = function(block) {
  var tx = block.getFieldValue('TX');
  var rx = block.getFieldValue('RX');
  
  Blockly.Python.definitions_['import_riscv_camera'] = 'from camera_riscv import *';
  Blockly.Python.definitions_['create_riscv_camera'] = 'cam = CameraUART(tx=' + tx + '_PIN, rx=' + rx + '_PIN, baudrate=115200)';
  
  return '';
};

// Khối lấy thuộc tính của object theo label
Blockly.Blocks['get_property_by_label'] = {
  init: function () {
    this.jsonInit({
      type: "get_property_by_label",
      message0: "Lấy %1 của label %2",
      args0: [
        {
          type: "field_dropdown",
          name: "PROPERTY",
          options: [
            ["x trung tâm", "center_x"],
            ["y trung tâm", "center_y"],
            ["Chiều rộng w", "w"],
            ["Chiều cao h", "h"]
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
      tooltip: "Lấy thông tin của object theo nhãn (tọa độ trung tâm tính từ giữa màn hình)",
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

// Khối in danh sách nhãn của model
Blockly.Blocks['print_model_labels'] = {
  init: function () {
    this.jsonInit({
      type: "print_model_labels",
      message0: "In danh sách nhãn của model AI",
      previousStatement: null,
      nextStatement: null,
      colour: "#cb2026",
      tooltip: "Yêu cầu MaixCAM gửi danh sách nhãn và in ra terminal",
      helpUrl: ""
    });
  }
};

Blockly.Python['print_model_labels'] = function(block) {
  var code = 'cam.print_model_labels()\n';
  return code;
};