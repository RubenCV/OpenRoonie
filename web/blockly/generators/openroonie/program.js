'use strict';

goog.provide('Blockly.JavaScript.program');
goog.require('Blockly.JavaScript');

Blockly.JavaScript['program'] = function(block) {
  var text_id = block.getFieldValue('ID');
  var code = 'program ' + text_id + ';\n';
  return code;
};

Blockly.JavaScript['main'] = function(block) {
  var statements_name = Blockly.JavaScript.statementToCode(block, 'NAME');
  var code = 'main {\n' + statements_name + '}\n';
  return code;
};
