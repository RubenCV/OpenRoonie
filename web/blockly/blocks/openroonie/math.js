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
 * @fileoverview Math blocks for Blockly.
 * @author q.neutron@gmail.com (Quynh Neutron)
 */
'use strict';

goog.provide('Blockly.Blocks.math');

goog.require('Blockly.Blocks');


/**
 * Common HSV hue for all blocks in this category.
 */
Blockly.Blocks.math.HUE = 230;

Blockly.Blocks['math_number'] = {
  /**
   * Block for numeric value.
   * @this Blockly.Block
   */
  init: function() {
    this.setHelpUrl(Blockly.Msg.MATH_NUMBER_HELPURL);
    this.setColour(Blockly.Blocks.math.HUE);
    this.appendDummyInput()
        .appendField(new Blockly.FieldNumber('0'), 'NUM');
    this.setOutput(true, 'Number');
    // Assign 'this' to a variable for use in the tooltip closure below.
    var thisBlock = this;
    // Number block is trivial.  Use tooltip of parent block if it exists.
    this.setTooltip(function() {
      var parent = thisBlock.getParent();
      return (parent && parent.getInputsInline() && parent.tooltip) ||
          Blockly.Msg.MATH_NUMBER_TOOLTIP;
    });
  }
};

Blockly.Blocks['math_arithmetic'] = {
  /**
   * Block for basic arithmetic operator.
   * @this Blockly.Block
   */
  init: function() {
    this.jsonInit({
      "message0": "%1 %2 %3",
      "args0": [
        {
          "type": "input_value",
          "name": "A",
          "check": "Number"
        },
        {
          "type": "field_dropdown",
          "name": "OP",
          "options":
            [[Blockly.Msg.MATH_ADDITION_SYMBOL, 'ADD'],
             [Blockly.Msg.MATH_SUBTRACTION_SYMBOL, 'MINUS'],
             [Blockly.Msg.MATH_MULTIPLICATION_SYMBOL, 'MULTIPLY'],
             [Blockly.Msg.MATH_DIVISION_SYMBOL, 'DIVIDE']]
        },
        {
          "type": "input_value",
          "name": "B",
          "check": "Number"
        }
      ],
      "inputsInline": true,
      "output": "Number",
      "colour": Blockly.Blocks.math.HUE,
      "helpUrl": Blockly.Msg.MATH_ARITHMETIC_HELPURL
    });
    // Assign 'this' to a variable for use in the tooltip closure below.
    var thisBlock = this;
    this.setTooltip(function() {
      var mode = thisBlock.getFieldValue('OP');
      var TOOLTIPS = {
        'ADD': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_ADD,
        'MINUS': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_MINUS,
        'MULTIPLY': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_MULTIPLY,
        'DIVIDE': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_DIVIDE,
        'POWER': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_POWER
      };
      return TOOLTIPS[mode];
    });
  }
};

Blockly.Blocks['math_random'] = {
  /**
   * Block for comparison operator.
   * @this Blockly.Block
   */

   init: function() {
    this.jsonInit({
      "message0": "random (%1 , %2)",
      "args0": [
        {
          "type": "input_value",
          "name": "A",
          "check": "Number"
        },
        {
          "type": "input_value",
          "name": "B",
          "check": "Number"
        }
      ],
      "inputsInline": true,
      "output": "Number",
      "colour": Blockly.Blocks.math.HUE,
      "helpUrl": Blockly.Msg.MATH_ARITHMETIC_HELPURL
    });
  // Assign 'this' to a variable for use in the tooltip closure below.
    var thisBlock = this;
    this.setTooltip(function() {
      var mode = thisBlock.getFieldValue('OP');
      var TOOLTIPS = {
        'ADD': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_ADD,
        'MINUS': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_MINUS,
        'MULTIPLY': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_MULTIPLY,
        'DIVIDE': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_DIVIDE,
        'POWER': Blockly.Msg.MATH_ARITHMETIC_TOOLTIP_POWER
      };
      return TOOLTIPS[mode];
    });
  }



   /*
  init: function() {

    this.setColour(Blockly.Blocks.math.HUE);
    this.setOutput(true, 'Boolean');
    this.appendValueInput('A')
        .appendField("rand(");
    this.appendValueInput('B')
        .appendField(", ");
    this.appendDummyInput()
        .appendField(") ");
    this.setInputsInline(true);
  }*/
};
