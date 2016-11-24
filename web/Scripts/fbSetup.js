// Initialize Firebase
var config = {
	apiKey: "AIzaSyCy6mjRIu3qmncJnJzbIDNmaAc2RXOLtLw",
	authDomain: "openroonie.firebaseapp.com",
	databaseURL: "https://openroonie.firebaseio.com",
	storageBucket: "openroonie.appspot.com",
	messagingSenderId: "830160485995"
};

firebase.initializeApp(config);

var database = firebase.database();

var consoleId = firebase.database().ref('/');
consoleId.once('value', function(snapshot) {
	var user = snapshot.child('userId').val();
	var console = snapshot.child('consoleId').val();
	
	initConsole(user, console);

});

function initConsole(userId, consoleId){
	console.log("Loading console...");
	Anywhere.LoadConsole("consoles-2.pythonanywhere.com", userId, consoleId, "", false);
}