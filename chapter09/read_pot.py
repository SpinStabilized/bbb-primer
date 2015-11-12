import Adafruit_BBIO.ADC as ADC
import time
import math
 
# Define program constants
ANALOG_IN    = 'AIN1'
SAMPLE_RATE  = 10     # Hertz

# Short function to handle a bug in the ADC drivers where the value needs to
# be read twice to get an actual value
def read_adc(adc_pin):
    ADC.read_raw(adc_pin)
    return ADC.read_raw(adc_pin)

# Convert the ADC reading (as a % of full range) to a voltage
def adc_to_voltage(adc_reading, vdd_adc=1.8):
    return adc_reading * vdd_adc

# Configue the ADC
ADC.setup()
 
# print out a nice message to let the user know how to quit.
print('Starting, press <control>-c to quit.\n')
 
# Execute until a keyboard interrupt
try:
    old_value = read_adc(ANALOG_IN)
    time.sleep(1/SAMPLE_RATE)
    while True:
        # Check the current value. If it is more than NOISE_WINDOW change,
        # output a message.
        value = read_adc(ANALOG_IN)
        if old_value != value:
            print(value)
         
        # Value becomes the old value and we wait a sample period
        old_value = value
        time.sleep(1/SAMPLE_RATE)

except KeyboardInterrupt:
    pass
