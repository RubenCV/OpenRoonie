// Global Vars
var editor, workspace, onresize, fileData, roonieData;

//==================== Document Ready ====================//
$(document).ready(function() {
	// Blockly
	var blocklyArea = document.getElementById('blocklyArea');
	var blocklyDiv = document.getElementById('blocklyDiv');
	var rtl = (document.location.search == '?rtl');
	
	workspace = Blockly.inject(blocklyDiv,
		{media: './blockly/media/',
		toolbox: document.getElementById('toolbox')});
		
	onresize = function(e) {
		// Compute the absolute coordinates and dimensions of blocklyArea.
		var element = blocklyArea;
		var x = 0;
		var y = 0;
		do {
			x += element.offsetLeft;
			y += element.offsetTop;
			element = element.offsetParent;
		} while (element);
		// Position blocklyDiv over blocklyArea.
		blocklyDiv.style.left = x + 'px';
		blocklyDiv.style.top = y + 'px';
		blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
		blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
	};
	window.addEventListener('resize', onresize, false);
	
	// Ace Editor
	editor = ace.edit("openRoonieTextArea");
	editor.setTheme("ace/theme/tomorrow_night_eighties");
	editor.session.setMode("ace/mode/javascript");
	document.getElementById("openRoonieTextArea").style.fontSize='14px';


	var fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', function(e) {
        var file = fileInput.files[0];
        var textType = '/text.*/';

        if (file.name.endsWith(".xml")) {
            var reader = new FileReader();

            reader.onload = function(e) {
            	fileData = reader.result;
            }

            reader.readAsText(file);    
        } else {
            alert("Please, upload an XML file.");
        }
    });

    var roonieInput = document.getElementById('roonieInput');
    roonieInput.addEventListener('change', function(e) {
        var file = roonieInput.files[0];
        var textType = '/text.*/';

        if (file.name.endsWith(".roonie")) {
            var reader = new FileReader();

            reader.onload = function(e) {
            	roonieData = reader.result;
            }

            reader.readAsText(file);    
        } else {
            alert("Please, upload a .roonie file.");
        }
    });
});


//==================== Blockly ====================//
function resizeBlockly(){
	// Cambiar a la tab de Blockly
	changeToTab(1);
	
	// Resize de Blockly
	onresize();
	Blockly.svgResize(workspace);
}

// Limpiar el workspace de Blockly
function flushBlocks(){
	Blockly.mainWorkspace.clear();
}


//==================== Ace Editor ====================//
// Limpiar el Editor Ace
function flushCode(){
	editor.setValue("");
	editor.gotoLine(editor.session.getLength());
}


//==================== Consola ====================//
// Cargar la Terminal / Consola
$(function () {
	// Hash del usuario RubenCV @ PythonAnywhere
	var userId = "66de0ly7uel6sfx69be2vji2tpngcw8i";

	// Id de la Consola que esta corriendo OpenRoonie.py
	var consoleId = "4002449";

	//Anywhere.LoadConsole("consoles-2.pythonanywhere.com", userId, consoleId, "", false);
});

// Cargar un archivo con el sourcode (.roonie) ya existente. -> Ej. loadFile("v");
function loadFile(fn){
	Anywhere.sockjs.send('loadFile()\r' + fn + '\r');
}

// Cargar el codigo que este en el editor
function loadCode(){			
	Anywhere.sockjs.send('loadCode()\r' + editor.getValue().split('\n').join('').split('\t').join('').split('\r').join('') + '\r');
}

// Limpiar la consola
function cleanConsole(){
	Anywhere.sockjs.send('cleanConsole()\r');
}

// Correr el codigo obj que ya se habia creado previamente
function runLoadedCode(){
	Anywhere.sockjs.send('runLoadedCode()\r');
}

function resetRoonie(){
	Anywhere.sockjs.send('resetRoonie()\r');
}

// Matar la terminal... por que lo harias!?!??!
function killConsole(){
	alert("Deshabilitado.");
	//Anywhere.sockjs.send('exit()\r');
}


//==================== Tabs ====================//
// Cambiar la tab actual por la que se llame como parametro
function changeToTab(idTab){
	// Cambiar la tab
	var lis = document.getElementsByClassName("nav nav-tabs")[0].getElementsByTagName("li");
	for (var i = 0; i < lis.length; i++) { 
		lis[i].className = "";
	}
	lis[idTab].className = "active";
	
	// Cambiar el contenido de la tab
	var tabsContent = document.getElementsByClassName("tab-content")[0].children;
	for (var i = 0; i < tabsContent.length; i++) { 
		tabsContent[i].className = "tab-pane fade";
		//console.log(tabsContent[i]);
	}
	tabsContent[idTab].className = "tab-pane fade in active";
}

function toCodeTab(){
	// Cambiar a la tab de code
	changeToTab(2);
	
	// Asignar el codigo de blockly al editor ace
	editor.setValue(Blockly.JavaScript.workspaceToCode(workspace));
	editor.gotoLine(editor.session.getLength());
}

function toConsoleTab(){
	// Cambiar a la tab de consola
	changeToTab(3);
	
	// Limpiar la consola
	cleanConsole();
	
	// Mandar el codigo que esta en el editor ace a la consola y ejecutarlo
	loadCode();
}


//==================== Salvar Blocks a XML ====================//
function toXml(){
	var output = document.getElementById('openRoonieTextArea');
	var xml = Blockly.Xml.workspaceToDom(workspace);
	var plaintext = Blockly.Xml.domToPrettyText(xml);
	var data = plaintext;
	
	var filename = document.getElementById("xmlFileName").value;
	filename += ".xml";

	var blob = new Blob([data], {type: 'text/csv'});
    if(window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveBlob(blob, filename);
    }
    else{
        var elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(blob);
        elem.download = filename;        
        document.body.appendChild(elem);
        elem.click();        
        document.body.removeChild(elem);
    }
}

function fromXml(){
	var xml = Blockly.Xml.textToDom(fileData);
	Blockly.Xml.domToWorkspace(xml, workspace);
}

//==================== Salvar codigo a .roonie ====================//
function toRoonie(){
	var data = editor.getValue();
	
	var filename = document.getElementById("roonieFileName").value;
	filename += ".roonie";

	var blob = new Blob([data], {type: 'text/csv'});
    if(window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveBlob(blob, filename);
    }
    else{
        var elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(blob);
        elem.download = filename;        
        document.body.appendChild(elem);
        elem.click();        
        document.body.removeChild(elem);
    }
}

function fromRoonie(){
	editor.setValue(roonieData);
}