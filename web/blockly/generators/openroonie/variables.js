'use strict';
goog.provide('Blockly.JavaScript.variables');
goog.require('Blockly.JavaScript');


Blockly.JavaScript['variable_single'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_var = block.getFieldValue('VAR');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  //get rid of parenthesis
  if(value_name.indexOf("(") == 0) {
    value_name = value_name.substring(1,value_name.length-1);
  }
  var code = 'var ' + dropdown_type + ' ' + value_name + ';\n';
  return code;
};

Blockly.JavaScript['variable_single_name'] = function(block) {
  var text_var = block.getFieldValue('VAR');
  var code = text_var;
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['variable_single_name_comma'] = function(block) {
  var text_var = block.getFieldValue('VAR');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  if(value_name.indexOf("(") == 0) {
    value_name = value_name.substring(1,value_name.length-1);
  }
  var code = text_var + ', ' + value_name;
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['variable_single_set'] = function(block) {
  var text_name = block.getFieldValue('VAR');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);

  if(value_name.indexOf("(") > -1) {
    value_name = value_name.substring(1,value_name.length-1);
  }
  var code = text_name + ' = ' + value_name + ';\n';
  return code;
};

Blockly.JavaScript['variable_array_one'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_var = block.getFieldValue('NAME');
  var dim1 = block.getFieldValue('VAR1');

  var code = 'var ' + dropdown_type + ' ' + text_var + ' [' + dim1 + '];\n';
  return code;
};

Blockly.JavaScript['variable_array_two'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_var = block.getFieldValue('NAME');
  var dim1 = block.getFieldValue('VAR1');
  var dim2 = block.getFieldValue('VAR2');

  var code = 'var ' + dropdown_type + ' ' + text_var + ' [' + dim1 + ', ' + dim2 + '];\n';
  return code;
};

Blockly.JavaScript['variable_array_one_set'] = function(block) {
  var text_var = block.getFieldValue('VARNAME');
  var dim1 = block.getFieldValue('VAR1');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  value_name = value_name.substring(1,value_name.length-1);
  var code = text_var + '[' + dim1 + '] = ' + value_name + ';\n';
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['variable_array_two_set'] = function(block) {
  var text_var = block.getFieldValue('VARNAME');
  var dim1 = block.getFieldValue('VAR1');
  var dim2 = block.getFieldValue('VAR2');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  value_name = value_name.substring(1,value_name.length-1);
  var code = text_var + '[' + dim1 + ', ' + dim2 + '] = ' + value_name + ';\n';
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['variable_array_one_get'] = function(block) {
  var text_var = block.getFieldValue('VARNAME');
  var dim1 = block.getFieldValue('VAR1');
  var code = text_var + '[' + dim1 + ']';
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['variable_array_two_get'] = function(block) {
  var text_var = block.getFieldValue('VARNAME');
  var dim1 = block.getFieldValue('VAR1');
  var dim2 = block.getFieldValue('VAR2');
  var code = text_var + '[' + dim1 + ', ' + dim2 + ']';
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['variable_read'] = function(block) {
  // Print statement.
  var code = block.getFieldValue('VAR');
  return 'read(' + code + ');\n';
};