'use strict';

goog.provide('Blockly.Blocks.functions');
goog.require('Blockly.Blocks');

Blockly.Blocks['function_statement'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField("function ")
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["char", "char"], ["string", "string"], ["void", "void"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("name"), "VAR")
        .appendField("( ");
    this.appendStatementInput("BLOCK");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_statement_no_params'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("function ")
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["char", "char"], ["string", "string"], ["void", "void"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("name"), "VAR")
        .appendField("( )");
    this.appendStatementInput("BLOCK");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_param'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["char", "char"], ["string", "string"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("name"), "VAR")
        .appendField(" )");
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_param_coma'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["char", "char"], ["string", "string"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("name"), "VAR")
        .appendField(", ");
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_call'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField("call function")
        .appendField(new Blockly.FieldTextInput("name"), "FNAME")
        .appendField(" parameters: ");
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_call_noparams'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("call function ")
        .appendField(new Blockly.FieldTextInput("name"), "FNAME")
        .appendField(" no parameters ");
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_call_ret'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField("call function")
        .appendField(new Blockly.FieldTextInput("default"), "FUNC")
        .appendField(" parameters: ");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_call_ret_noparams'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("call function")
        .appendField(new Blockly.FieldTextInput("default"), "FUNC")
        .appendField(" no parameters: ");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['return'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField("return");
    this.setPreviousStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['return_void'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("return");
    this.setPreviousStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};