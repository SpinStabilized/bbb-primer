/*
 * rr_crossing_blinkers.js - BoneScript File to blink LEDs attached to 
 *                           GPIO P9_12 and P9_15.
 *
 * Example script for "The BeagleBone Black Primer"
 *
 */
var bbb = require('bonescript');  // Declare a bbb variable, board h/w object
var state1 = bbb.LOW;          // Declare a variable to represent GPIO P9_12 state
var state2 = bbb.LOW;          // Declare a variable to represent GPIO P9_15 state


bbb.pinMode("P9_12", bbb.OUTPUT); // Set the GPIO P9_12 control to output
bbb.pinMode("P9_15", bbb.OUTPUT); // Set the GPIO P9_15 control to output
setInterval(blink, 1000);         // Alternate blinking LEDs every 1 second

/*
 * Function - blink
 *
 * Toggle the value of the state variable between high and low when called.
 */
function blink() {
    if(state1 == bbb.LOW) {       // If P9_12 is LOW...
        state1 = bbb.HIGH;        // ... set P9_12 to HIGH
        state2 = bbb.LOW;         // ... set P9_15 to LOW
    } else {                      // Otherwise...
        state1 = bbb.LOW;         // ... set P9_12 to LOW
        state2 = bbb.HIGH;        // ... set P9_15 to HIGH
    }
    
    bbb.digitalWrite("P9_12", state1); // Update the GPIO P9_12 state
    bbb.digitalWrite("P9_15", state2); // Update the GPIO P9_15 state
}