import Adafruit_BBIO.ADC as ADC
import time
 
# Define program constants
ANALOG_IN      = 'AIN0'
SAMPLE_RATE    = 100     # Hertz

# Short function to handle a bug in the ADC drivers where the value needs to
# be read twice to get an actual value
def read_adc(adc_pin):
    ADC.read(adc_pin)
    return ADC.read(adc_pin)

# Configue the ADC
ADC.setup()
 
# Execute until a keyboard interrupt
try:
    while True:
        value = read_adc(ANALOG_IN)
        print(value * 1.8)
        time.sleep(1/SAMPLE_RATE)

except KeyboardInterrupt:
    pass
