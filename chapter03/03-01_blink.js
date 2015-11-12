/*
 * blink.js - BoneScript File to blink the USR1 LED on the BeagleBone Black.
 *
 * Example script for "The BeagleBone Black Primer"
 *
 */
var bbb = require('bonescript');  // Declare a bbb variable, board h/w object
var state = bbb.LOW;              // Declare a variable to represent LED state


bbb.pinMode("USR1", bbb.OUTPUT);  // Set the USR1 LED control to output
setInterval(blink, 1000);         // Call blink fn the LED every 1 second
console.log('Hello, World!');     // Output the classic introduction

/*
 * Function - blink
 *
 * Toggle the value of the state variable between high and low when called.
 */
function blink() {
    if(state == bbb.LOW) {        // If the current state is LOW then...
        state = bbb.HIGH;         // ...change the state to HIGH
    } else {                      // Otherwise, the state is HIGH...
        state = bbb.LOW;          // ...change the state to LOW
    }
    
    bbb.digitalWrite("USR1", state); // Update the USR1 state
}