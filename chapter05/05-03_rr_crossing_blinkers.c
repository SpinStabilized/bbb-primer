/**
 * rr_crossing_blinkers.c - Python File to blink LEDs attached to 
 *                          GPIO P9_12 and P9_15.
 *
 * Example program for "The BeagleBone Black Primer"
 */
 
  
#include "iolib.h"

#define PORT 9
#define PIN_A 12
#define PIN_B 15

#define TRUE  1
#define FALSE 0
   
int main() {
  
  	iolib_init();
    iolib_setdir(PORT, PIN_A, DIR_OUT);    // Set the GPIO P9_12 control to output
    iolib_setdir(PORT, PIN_B, DIR_OUT);    // Set the GPIO P9_15 control to output

    pin_low(PORT, PIN_A);                  // Initialize GPIO P9_12 to low (off)
    pin_low(PORT, PIN_B);                  // Initialize GPIO P9_15 to low (off)
   
    int state = FALSE;

    while(TRUE) {  

        if (state) {        // If P9_12 is not high (is low)
            pin_low(PORT, PIN_A);     // ... set P9_12 to high
            pin_high(PORT, PIN_B);      // ... set P9_15 to low

        } else {                     // Otherwise ...
            pin_high(PORT, PIN_A);      // ... set P9_12 to low
            pin_low(PORT, PIN_B);     // ... set P9_15 to high
        } 

        state = !state;
   
        sleep(1);                // Run once every second
   
    }    
     
    iolib_free();
    return(0);  
}