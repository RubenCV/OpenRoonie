/**
 * @license
 * Visual Blocks Editor
 *
 * Copyright 2012 Google Inc.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @fileoverview Variable blocks for Blockly.
 * @author fraser@google.com (Neil Fraser)
 */
'use strict';

goog.provide('Blockly.Blocks.variables');

goog.require('Blockly.Blocks');


/**
 * Common HSV hue for all blocks in this category.
 */
Blockly.Blocks.variables.HUE = 330;

Blockly.Blocks['variable_single'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField("var ")
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["char", "char"], ["string", "string"]]), "TYPE")
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
  }
};

Blockly.Blocks['variable_single_name'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("varname"), "VAR");
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['variable_single_name_comma'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField(new Blockly.FieldTextInput("varname"), "VAR")
        .appendField(", ");
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['variable_single_set'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField(new Blockly.FieldTextInput("varname"), "VAR")
        .appendField("= ");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
  }
};

Blockly.Blocks['variable_array_one'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("var ")
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["char", "char"], ["string", "string"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("varname"), "NAME")
        .appendField("[")
        .appendField(new Blockly.FieldTextInput("7"), "VAR1")
        .appendField("]");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setOutput(false);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['variable_array_two'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("var ")
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["bool", "bool"], ["char", "char"], ["string", "string"]]), "TYPE")
        .appendField(new Blockly.FieldTextInput("varname"), "NAME")
        .appendField("[")
        .appendField(new Blockly.FieldTextInput("5"), "VAR1")
        .appendField(", ")
        .appendField(new Blockly.FieldTextInput("5"), "VAR2")
        .appendField("]");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setOutput(false);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['variable_array_one_set'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField(new Blockly.FieldTextInput("varname"), "VARNAME")
        .appendField("[")
        .appendField(new Blockly.FieldTextInput("7"), "VAR1")
        .appendField("] =");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['variable_array_two_set'] = {
  init: function() {
    this.appendValueInput("NAME")
        .appendField(new Blockly.FieldTextInput("varname"), "VARNAME")
        .appendField("[")
        .appendField(new Blockly.FieldTextInput("5"), "VAR1")
        .appendField(", ")
        .appendField(new Blockly.FieldTextInput("5"), "VAR2")
        .appendField("] =");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['variable_array_one_get'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("varname"), "VARNAME")
        .appendField("[")
        .appendField(new Blockly.FieldTextInput("7"), "VAR1")
        .appendField("]");
    this.setPreviousStatement(false);
    this.setNextStatement(false);
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['variable_array_two_get'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("varname"), "VARNAME")
        .appendField("[")
        .appendField(new Blockly.FieldTextInput("5"), "VAR1")
        .appendField(", ")
        .appendField(new Blockly.FieldTextInput("5"), "VAR2")
        .appendField("]");
    this.setPreviousStatement(false);
    this.setNextStatement(false);
    this.setOutput(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};