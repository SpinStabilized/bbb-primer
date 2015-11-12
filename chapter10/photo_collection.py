import Adafruit_BBIO.ADC as ADC
import time
 
# Configue the ADC
ADC.setup()

# Define program constants
PHOTO_PIN   = 'AIN1'
SAMPLE_RATE = 0.5     # Hertz

def read_adc_v(adc_pin, adc_max_v=1.8):
	''' Read a BBB ADC pin and return the voltage.

	Keyword arguments:
	adc_pin   -- BBB AIN pin to read (required)
	adc_max_v -- Maximum voltage for BBB ADC (default 1.8)

	Return:
	ADC reading as a voltage

	Note: Read the ADC twice to overcome a bug reported in the
	Adafruit_BBIO library documentation.
	'''
	ADC.read(adc_pin)
	return ADC.read(adc_pin) * adc_max_v

def lights_on(volts, threshold=0.15):
	''' Returns True or False is the lights are on or off

	Keyword arguments:
	volts     - ADC reading in volts (Required)
	threshold - value above which the lights are off

	Return:
	Boolean of light status
	'''
	if volts > threshold:
		return True
	else:
		return False


if __name__ == '__main__':

	# Execute until a keyboard interrupt
	try:
	    while True:
	        voltage_reading = read_adc_v(PHOTO_PIN)
	        lights_status = lights_on(voltage_reading)
	        print 'Lights On: {} ({} V)'.format(lights_status, voltage_reading)
	        time.sleep(1/SAMPLE_RATE)

	except KeyboardInterrupt:
	    GPIO.cleanup()
