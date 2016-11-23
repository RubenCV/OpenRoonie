/**
 * @license
 * Visual Blocks Language
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
 * @fileoverview Generating JavaScript for math blocks.
 * @author q.neutron@gmail.com (Quynh Neutron)
 */
'use strict';

goog.provide('Blockly.JavaScript.math');

goog.require('Blockly.JavaScript');


Blockly.JavaScript['math_number'] = function(block) {
  // Numeric value.
  var code = parseFloat(block.getFieldValue('NUM'));
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['math_arithmetic'] = function(block) {
  // Basic arithmetic operators, and power.
  var OPERATORS = {
    'ADD': [' + ', Blockly.JavaScript.ORDER_ADDITION],
    'MINUS': [' - ', Blockly.JavaScript.ORDER_SUBTRACTION],
    'MULTIPLY': [' * ', Blockly.JavaScript.ORDER_MULTIPLICATION],
    'DIVIDE': [' / ', Blockly.JavaScript.ORDER_DIVISION]
  };
  var tuple = OPERATORS[block.getFieldValue('OP')];
  var operator = tuple[0];
  var order = tuple[1];
  var argument0 = Blockly.JavaScript.valueToCode(block, 'A', order) || '0';
  var argument1 = Blockly.JavaScript.valueToCode(block, 'B', order) || '0';

  if(argument0.indexOf("(") == 0) {
    argument0 = argument0.substring(1,argument0.length-1);
  }

  if(argument1.indexOf("(") == 0) {
    argument1 = argument1.substring(1,argument1.length-1);
  }

  var code;
  // Power in JavaScript requires a special case since it has no operator.
  if (!operator) {
    code = 'Math.pow(' + argument0 + ', ' + argument1 + ')';
    return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
  }
  code = argument0 + operator + argument1;
  return [code, order];
};

Blockly.JavaScript['math_random'] = function(block) {
  // Numeric value.
  var argument0 = Blockly.JavaScript.valueToCode(block, 'A', Blockly.JavaScript.ORDER_NONE);
  var argument1 = Blockly.JavaScript.valueToCode(block, 'B', Blockly.JavaScript.ORDER_NONE);

  if(argument0.indexOf("(") == 0) {
    argument0 = argument0.substring(1,argument0.length-1);
  }

  if(argument1.indexOf("(") == 0) {
    argument1 = argument1.substring(1,argument1.length-1);
  }

  var code = 'random(' + argument0 + ', ' + argument1 + ')';
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};