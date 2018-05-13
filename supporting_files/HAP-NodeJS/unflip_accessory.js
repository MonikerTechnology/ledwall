var Accessory = require('../').Accessory;
var Service = require('../').Service;
var Characteristic = require('../').Characteristic;
var uuid = require('../').uuid;

////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
var name = "unflip";                                       //Name to Show to IOS
var UUID = "hap-nodejs:accessories:HSVdata";     //Change the RGBLight to something unique for each light - this should be unique for each node on your system
var USERNAME = "00:01:00:2C:5D:C1";              //This must also be unique for each node - make sure you change it!

var MQTT_IP = '127.0.0.1'
var lightTopic = '/LEDwall'
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////



var state = false;

var accUUID = uuid.generate('hap-nodejs:accessories:switch');

var acc = exports.accessory = new Accessory("Switch", accUUID);

function unFlip() {
  console.log("Unflipping...");
  state = false;

  acc.getService(Service.Switch)
    .getCharacteristic(Characteristic.On)
    .updateValue(state);
}

acc.username = "1A:AA:AA:AA:AA:AA";
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
    state = value;
    if(value) setTimeout(unFlip, 100);
    callback();
  });
