var Accessory = require('../').Accessory;
var Service = require('../').Service;
var Characteristic = require('../').Characteristic;
var uuid = require('../').uuid;
var err = null; // in case there were any problems


////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
var name = "RainMode";                                       //Name to Show to IOS
var UUID = "hap-nodejs:accessories:RGBLight";     //Change the RGBLight to something unique for each light - this should be unique for each node on your system
var USERNAME = "AC:AF:AC:2C:5D:C1";              //This must also be unique for each node - make sure you change it!

var MQTT_IP = '192.168.1.174'
var lightTopic = '/deskLEDs'
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////

// here's a fake hardware device that we'll expose to HomeKit
var SWITCH = {
    setPowerOn: function(on) {
    console.log("Turning the LEDswitch %s!...", on ? "on" : "off");
    if (on) {
          SWITCH.powerOn = true;
          if(err) { return console.log(err); }
          console.log("...LEDswitch is now on.");
          client.publish(lightTopic, 'p1');
    } else {
          SWITCH.powerOn = false;
          if(err) { return console.log(err); }
          console.log("...LEDswitch is now off.");
          client.publish(lightTopic, 'p0');
    }
  },
    identify: function() {
    console.log("Identify the LEDswitch.");
    }
}

// MQTT Setup
var mqtt = require('mqtt');
var options = {
  port: 1883,
  host: MQTT_IP,
  clientId: 'FGAK35243'
};
var client = mqtt.connect(options);
client.on('message', function(topic, message) {

});

// Generate a consistent UUID for our LEDswitch Accessory that will remain the same even when
// restarting our server. We use the `uuid.generate` helper function to create a deterministic
// UUID based on an arbitrary "namespace" and the accessory name.
var switchUUID = uuid.generate('hap-nodejs:accessories:Switch');

// This is the Accessory that we'll return to HAP-NodeJS that represents our fake light.
var LEDswitch = exports.accessory = new Accessory(name, switchUUID);

// Add properties for publishing (in case we're using Core.js and not BridgedCore.js)
LEDswitch.username = "1A:2B:3C:4D:5D:FE";
LEDswitch.pincode = "031-45-154";

// set some basic properties (these values are arbitrary and setting them is optional)
LEDswitch
  .getService(Service.AccessoryInformation)
  .setCharacteristic(Characteristic.Manufacturer, "Moniker Technology")
  .setCharacteristic(Characteristic.Model, "Rev-1")
  .setCharacteristic(Characteristic.SerialNumber, "A1S2NASF88EW");

// listen for the "identify" event for this Accessory
LEDswitch.on('identify', function(paired, callback) {
  SWITCH.identify();
  callback(); // success
});

// Add the actual LEDswitch Service and listen for change events from iOS.
// We can see the complete list of Services and Characteristics in `lib/gen/HomeKitTypes.js`
LEDswitch
  .addService(Service.Switch, "LEDswitch") // services exposed to the user should have "names" like "Fake Light" for us
  .getCharacteristic(Characteristic.On)
  .on('set', function(value, callback) {
    SWITCH.setPowerOn(value);
    callback(); // Our fake LEDswitch is synchronous - this value has been successfully set
  });

// We want to intercept requests for our current power state so we can query the hardware itself instead of
// allowing HAP-NodeJS to return the cached Characteristic.value.
LEDswitch
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
