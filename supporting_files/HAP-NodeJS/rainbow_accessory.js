var Accessory = require('../').Accessory;
var Service = require('../').Service;
var Characteristic = require('../').Characteristic;
var uuid = require('../').uuid;
var http = require("http"); //Added for the http post requests
var err = null; // in case there were any problems

////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
var name = "rainbow";                                       //Name to Show to IOS
var UUID = "hap-nodejs:accessories:rainbow";     //Change the RGBLight to something unique for each light - this should be unique for each node on your system
var USERNAME = "00:01:00:2C:5D:C2";              //This must also be unique for each node - make sure you change it!


////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////


var postData; //This is where the post data gets stored for calling post(postdata);

// This is how we will communicate with the LED wall
function post(data) {
  var reqBody = JSON.stringify(data); //Convert JSON to string so it can be measured and sent

  var options = {
    host: "localhost",
    port: 321,
    path: "/",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(reqBody) //Gotcha!
    }
  };

  var req = http.request(options, function (res) {
    var responseString = "";

    res.on("data", function (data) {
        responseString += data;
        // save all the data from response
    });
    res.on("end", function () {
        console.log(responseString); 
        // print to console when response ends
    });
  });

  req.on('error', function(err) { //catch errors if the connection fails i.e. the server on the other end isn't running or maybe the adress is wrong
    // Error handling here
    console.log(err);
  });
  req.write(reqBody); //Send the data
  req.end(); //Close the connection - change or add delay to recive
}


var state = false;

var accUUID = uuid.generate('hap-nodejs:accessories:rainbow');

var acc = exports.accessory = new Accessory(name, accUUID);

function unFlip() {
  console.log("Unflipping...");
  state = false;

  acc.getService(Service.Switch)
    .getCharacteristic(Characteristic.On)
    .updateValue(state);
}

acc.username = "1A:A1:AA:AA:AA:AA";
acc.pincode = "031-45-154";

acc.on('identify', function(paired, callback) {
  console.log("Identify switch");
  callback();
});

acc.addService(Service.Switch, "Switch")
  .getCharacteristic(Characteristic.On)
  .on('get', function(callback) {
    console.log("The current state is %s", state ? "on" : "off");

    callback(null, state);
  })
  .on('set', function(value, callback) {
    console.log("The switch has been flipped");
    //send message
    //client.publish(lightTopic, 'unflip');
    postData = {"type":"mode","mode":"rainbow"}; //set power to on
    post(postData); //call the function to send the data
    state = value;
    if(value) setTimeout(unFlip, 100);
    callback();
  });
