#!/usr/bin/nodejs

if ((process.version.split('.')[1]|0) < 10) {
	console.log('Please, upgrade your node version to 0.10+');
	process.exit();
}

var net = require('net');
var util = require('util');
var crypto = require('crypto');

// Options set to connect with mitm server
var options = {
	'port': 6969,
	'host': '54.83.207.90',
}

// This constant is set using the stdin log from the test challenge.
// The problem statement does not say that we need to read it in runtime.
// However it shouldn't be hard to adapt.
const KEYPHRASE = 'DenimAggressiveTapirIsCurious';

// These are the protocols and keys used to spy as a mitm.
var mitmServer, mitmClient;
var mitmServerSecret, mitmServerPublic, mitmClientSecret;

var socket = net.connect(options, function() {}); // Wait for MITM service to talk.

socket.on('data', function(data) {

	data = data.toString().trim().split(':'); // MITM service spec.

	if (data[0] == 'Error') {
		console.log('Something happened');
	} else if (data[0] == 'CLIENT->SERVER') { // Intercepting message from client.
		data = data[1].split('|'); // From client code.
		if (data[0] == 'hello?') {
			// Attempt to connect.
			socket.write(data[0]);
		} else if (data[0] == 'key') {
			// Intercept prime and public key and create the mitmServer.
			mitmServer = crypto.createDiffieHellman(data[1], 'hex'); // From server code.
			mitmServer.generateKeys();
			mitmServerSecret = mitmServer.computeSecret(data[2], 'hex');
			mitmServerPublic = mitmServer.getPublicKey('hex'); // This will be sent later to the client.

			// Create mitmClient.
			mitmClient = crypto.createDiffieHellman(256); // From client code.
			mitmClient.generateKeys();
			
			// Send mitmClient credentials to the server instead of the originals.
			socket.write(util.format('key|%s|%s\n', mitmClient.getPrime('hex'), mitmClient.getPublicKey('hex')));
		} else if (data[0] == 'keyphrase') {
			// Intercept keyphrase and send KEYPHRASE instead.
			
			// The intercepted keyphrase can be decipher uncommenting the following lines.
			//
			// var decipher = crypto.createDecipheriv('aes-256-ecb', mitmServerSecret, '');
			// var clientKeyphrase = decipher.update(data[1], 'hex', 'utf8')+decipher.final('utf8');
			// console.log('Client keyphrase '+clientKeyphrase); // log to spy the client message

			// Cipher KEYPHRASE and send it to server using mitmClient.
			// mitmClientSecret has been initialized with a message from the server.
			var cipher = crypto.createCipheriv('aes-256-ecb', mitmClientSecret, ''); 
			var keyphrase = cipher.update(KEYPHRASE, 'utf8', 'hex')+cipher.final('hex');
			socket.write(util.format('keyphrase|%s\n', keyphrase)); 
		}
	} else { // Intercepting message from server.
		data = data[1].split('|'); // From server code.
		if (data[0] == 'hello!') {
			// Connection established.
			socket.write(data[0]);
		} else if (data[0] == 'key') {
			// Create clientSecret using the server info
			mitmClientSecret = mitmClient.computeSecret(data[1], 'hex'); // From client code.

			// Pass mitmServerPublic to client instead
			socket.write(util.format('key|%s\n', mitmServerPublic));
		} else if (data[0] == 'result') {
			// Decipher our message to complete the mission
			var decipher = crypto.createDecipheriv('aes-256-ecb', mitmClientSecret, '');
			var message = decipher.update(data[1], 'hex', 'utf8') + decipher.final('utf8');
			console.log(message); // Mission completed!

			// Cipher it with mitmServer to pass it to the client
			var cipher = crypto.createCipheriv('aes-256-ecb', mitmServerSecret, '');
			var result = cipher.update(message, 'utf8', 'hex')+cipher.final('hex');
			socket.end(util.format('result|%s\n', result));
		}
	}

});
