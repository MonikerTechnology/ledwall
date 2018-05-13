var Accessory = require('../').Accessory;
var Service = require('../').Service;
var Characteristic = require('../').Characteristic;
var uuid = require('../').uuid;

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
