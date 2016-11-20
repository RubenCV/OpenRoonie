'use strict';

goog.provide('Blockly.JavaScript.functions');
goog.require('Blockly.JavaScript');

Blockly.JavaScript['function_statement'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_var = block.getFieldValue('VAR');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_block = Blockly.JavaScript.statementToCode(block, 'BLOCK');
  var code = 'function ' + dropdown_type + ' ' + text_var + '' + value_name + ' {\n' + statements_block + '}\n';
  
  return code;
};

Blockly.JavaScript['function_statement_no_params'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_var = block.getFieldValue('VAR');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_block = Blockly.JavaScript.statementToCode(block, 'BLOCK');
  var code = 'function ' + dropdown_type + ' ' + text_var + '() {\n' + statements_block + '}\n';
  
  return code;
};

Blockly.JavaScript['function_param'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_var = block.getFieldValue('VAR');
  var code = dropdown_type + ' ' + text_var;
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['function_param_coma'] = function(block) {
  var dropdown_type = block.getFieldValue('TYPE');
  var text_var = block.getFieldValue('VAR');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  if(value_name.indexOf("(") > -1) {
    value_name = value_name.substring(1,value_name.length-1);
  }
  var code = dropdown_type + ' ' + text_var + ', ' + value_name;
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['function_call'] = function(block) {
  var text_fname = block.getFieldValue('FNAME');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);

  var code = text_fname + value_name;
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['function_call_noparams'] = function(block) {
  var text_fname = block.getFieldValue('FNAME');

  var code = text_fname + '()';
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['function_call_ret'] = function(block) {
  var text_var = block.getFieldValue('FUNC');
  var value_name = '(' + Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC) + ')';
  var code = text_var +  value_name + '\n';
  return code;
};

Blockly.JavaScript['function_call_ret_noparams'] = function(block) {
  var text_var = block.getFieldValue('FUNC');
  var code = text_var + '();\n';
  return code;
};

Blockly.JavaScript['return'] = function(block) {
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  value_name = value_name.substring(1,value_name.length-1);
  var code = 'return ' + value_name +';\n';
  return code;
};

Blockly.JavaScript['return_void'] = function(block) {
  var code = 'return;\n';
  return code;
};
