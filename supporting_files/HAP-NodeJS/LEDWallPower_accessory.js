var Accessory = require('../').Accessory;
var Service = require('../').Service;
var Characteristic = require('../').Characteristic;
var uuid = require('../').uuid;
var http = require("http"); //Added for the http post requests
var err = null; // in case there were any problems
//

////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
var name = "LEDWallPower";                                       //Name to Show to IOS
var UUID = "hap-nodejs:accessories:LEDWallPower";     //Change the RGBLight to something unique for each light - this should be unique for each node on your system - also find uuid.generate and change it to match
var USERNAME = "BB:A6:AC:2C:5D:C1";              //This must also be unique for each node - make sure you change it!

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


// here's a fake hardware device that we'll expose to HomeKit
var SWITCH = {
  
    setPowerOn: function(on) {
    console.log("Turning the LEDWallPower %s!...", on ? "on" : "off");
    if (on) {
          SWITCH.powerOn = true;
          if(err) { return console.log(err); }
          console.log("...LEDWallPower is now on.");
          postData = {"power":1}; //set power to on
          post(postData); //call the function to send the data
          SWITCH.powerOn = false;
    } else {
          SWITCH.powerOn = false;
          if(err) { return console.log(err); }
          console.log("...LEDWallPower is now off.");
          //req.write(reqBody);
          //client.publish(lightTopic, 'offXXXXX');
          postData = {"power":0};
          post(postData);
    }
  },
    identify: function() {
    console.log("Identify the LEDWallPower.");
    }
}


// Generate a consistent UUID for our LEDWallPower Accessory that will remain the same even when
// restarting our server. We use the `uuid.generate` helper function to create a deterministic
// UUID based on an arbitrary "namespace" and the accessory name.
var switchUUID = uuid.generate('hap-nodejs:accessories:LEDWallPower');

// This is the Accessory that we'll return to HAP-NodeJS that represents our fake light.
var LEDWallPower = exports.accessory = new Accessory(name, switchUUID);

// Add properties for publishing (in case we're using Core.js and not BridgedCore.js)
LEDWallPower.username = "1A:2B:3C:4D:5D:FE";
LEDWallPower.pincode = "031-45-154";

// set some basic properties (these values are arbitrary and setting them is optional)
LEDWallPower
  .getService(Service.AccessoryInformation)
  .setCharacteristic(Characteristic.Manufacturer, "Moniker Technology")
  .setCharacteristic(Characteristic.Model, "Rev-1")
  .setCharacteristic(Characteristic.SerialNumber, "A1S2NASF88EW");

// listen for the "identify" event for this Accessory
LEDWallPower.on('identify', function(paired, callback) {
  SWITCH.identify();
  callback(); // success
});

// Add the actual LEDWallPower Service and listen for change events from iOS.
// We can see the complete list of Services and Characteristics in `lib/gen/HomeKitTypes.js`
LEDWallPower
  .addService(Service.Switch, "LEDWallPower") // services exposed to the user should have "names" like "Fake Light" for us
  .getCharacteristic(Characteristic.On)
  .on('set', function(value, callback) {
    SWITCH.setPowerOn(value);
    callback(); // Our fake LEDWallPower is synchronous - this value has been successfully set
  });

// We want to intercept requests for our current power state so we can query the hardware itself instead of
// allowing HAP-NodeJS to return the cached Characteristic.value.
LEDWallPower
  .getService(Service.Switch)
  .getCharacteristic(Characteristic.On)
  .on('get', function(callback) {

    // this event is emitted when you ask Siri directly whether your light is on or not. you might query
    // the light hardware itself to find this out, then call the callback. But if you take longer than a
    // few seconds to respond, Siri will give up.

    var err = null; // in case there were any problems

    if (SWITCH.powerOn) {
      console.log("Are we on? Yes.");
      callback(err, true);
    }
    else {
      console.log("Are we on? No.");
      callback(err, false);
    }
  });
