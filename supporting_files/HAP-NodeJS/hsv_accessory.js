var Accessory = require('../').Accessory;
var Service = require('../').Service;
var Characteristic = require('../').Characteristic;
var uuid = require('../').uuid;
var http = require("http"); //Added for the http post requests
var lightState = 0;


////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
////////////////CHANGE THESE SETTINGS TO MATCH YOUR SETUP BEFORE RUNNING!!!!!!!!!!!!!//////////////////////////
var name = "HSVdataControl";                                       //Name to Show to IOS
var UUID = "hap-nodejs:accessories:HSVdataControl";     //Change the RGBLight to something unique for each light - this should be unique for each node on your system
var USERNAME = "00:00:00:00:00:A2";              //This must also be unique for each node - make sure you change it!

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

//setup HK light object
// Generate a consistent UUID for our LEDWallPower Accessory that will remain the same even when
// restarting our server. We use the `uuid.generate` helper function to create a deterministic
// UUID based on an arbitrary "namespace" and the accessory name.
var lightUUID = uuid.generate(UUID);


//DISPLAYNAME!!!
// This is the Accessory that we'll return to HAP-NodeJS that represents our fake light.
var light = exports.accessory = new Accessory(name, lightUUID);


// Add properties for publishing (in case we're using Core.js and not BridgedCore.js)
light.username = USERNAME;
light.pincode = "031-45-154";

//add a light service and setup the On Characteristic
light
  .addService(Service.Lightbulb)
  .getCharacteristic(Characteristic.On)
  .on('get', function(callback) {
    callback(null, lightAction.getState());
  });

  light
  .getService(Service.Lightbulb)
  .getCharacteristic(Characteristic.On)
  .on('set', function(value, callback) {
    lightAction.setState(value);
    callback();
  });

//Add and setup Brightness
  light
  .getService(Service.Lightbulb)
  .addCharacteristic(Characteristic.Brightness)
  .on('set', function(value, callback){
    lightAction.setBrightness(value);
    callback()
  });

light
  .getService(Service.Lightbulb)
  .getCharacteristic(Characteristic.Brightness)
  .on('get', function(callback){
    callback(null, lightAction.getBrightness())
  });

//Add and setup Saturation
  light
  .getService(Service.Lightbulb)
  .addCharacteristic(Characteristic.Saturation)
  .on('set', function(value, callback){
    lightAction.setSaturation(value);
    callback()
  });

light
  .getService(Service.Lightbulb)
  .getCharacteristic(Characteristic.Saturation)
  .on('get', function(callback){
    callback(null, lightAction.getSaturation())
  });

//Add and setup Hue
light
  .getService(Service.Lightbulb)
  .addCharacteristic(Characteristic.Hue)
  .on('set', function(value, callback){
    lightAction.setHue(value);
    callback()
  });

light
  .getService(Service.Lightbulb)
  .getCharacteristic(Characteristic.Hue)
  .on('get', function(callback){
    callback(null, lightAction.getHue())
  });



// here's a fake temperature sensor device that we'll expose to HomeKit
var lightAction = {

  //initialize the various state variables
  currentState: 0,
  currentBrightness: 0,
  currentHue: 0,
  currentSaturation: 0,

  lastBrightness: 0,
  lastHue: 0,
  lastSaturation: 0,


  //On Characteristic set/get
  getState: function() { return this.currentState;},
  setState: function(newState){

    if((newState == true && this.currentState == 0) || (newState == false && this.currentState == 1) ){
      console.log("Setting new outlet state: " + newState.toString());
      if(newState == true){
        //client.publish(lightTopic, 'p1');
        postData = {"type":"power","power":1}; //set power to on
        post(postData); //call the function to send the data
        this.currentState = 1;
      }
      else{
        //client.publish(lightTopic, 'p0');
        postData = {"type":"power","power":0}; //set power to on
        post(postData); //call the function to send the data
        this.currentState = 0;
      }
    }

  },

  //Brightness Characteristic set/get
  getBrightness: function(){return this.currentBrightness;},
  setBrightness: function(newBrightness){
    this.currentBrightness = newBrightness;
    this.updateLight();
  },


  //Saturation Characteristic set/get
  getSaturation: function(){return this.currentSaturation;},
  setSaturation: function(newSaturation){
    this.currentSaturation = newSaturation;
    this.updateLight();
  },


  //Hue Characteristic set/get
  getHue: function(){return this.currentHue;},
  setHue: function(newHue){
    this.currentHue = newHue;
    this.updateLight();
  },


  //other light setting functions
  updateState: function() {
    this.currentState = lightState;
  },

  updateLight: function(){
    if(this.lastSaturation != this.currentSaturation || this.lastHue != this.currentHue || this.lastBrightness != this.currentBrightness){
      pubBrightness = this.currentBrightness / 100;
      pubHue = this.currentHue / 360;
      pubSaturation = this.currentSaturation / 100;
      //toPublish = 'HSVXXXXX' + pubHue.toFixed(3).toString() + ',' + pubSaturation.toFixed(3).toString() + ',' + pubBrightness.toFixed(3).toString()
      //client.publish(lightTopic, toPublish);
      postData = {"type":"HSV","HSV":{"H":pubHue.toFixed(3).toString(),"S":pubSaturation.toFixed(3).toString(),"V":pubBrightness.toFixed(3).toString()}}; //set power to on
      post(postData); //call the function to send the data
      this.lastBrightness = this.currentBrightness;
      this.lastHue = this.currentHue;
      this.lastSaturation = this.currentSaturation;
    }
  }

}



// update the characteristic values so interested iOS devices can get notified
setInterval(function() {
  light
    .getService(Service.Lightbulb)
    .setCharacteristic(Characteristic.On, lightAction.currentState);
  light
    .getService(Service.Lightbulb)
    .setCharacteristic(Characteristic.Brightness, lightAction.getBrightness());
  light
    .getService(Service.Lightbulb)
    .setCharacteristic(Characteristic.Hue, lightAction.getHue());
  light
    .getService(Service.Lightbulb)
    .setCharacteristic(Characteristic.Saturation, lightAction.getSaturation());

}, 2000);
