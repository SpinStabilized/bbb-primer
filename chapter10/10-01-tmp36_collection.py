import Adafruit_BBIO.ADC as ADC
import time
 
# Configue the ADC
ADC.setup()

# Define program constants
TMP36_PIN   = 'AIN0'
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

def tmp36_v_to_t(volts):
	''' Calibration function for the TMP36 Temperature sensor.

	Keyword arguments:
	volts - TMP36 reading in Volts

	Return:
	Reading in degC
	'''
	return (100 * volts) - 50

if __name__ == '__main__':

	# Execute until a keyboard interrupt
	try:
	    while True:
	        voltage_reading = read_adc_v(TMP36_PIN)
	        temperature = tmp36_v_to_t(voltage_reading)
	        print 'Temperature: {:.2f} C'.format(temperature)
	        time.sleep(1/SAMPLE_RATE)

	except KeyboardInterrupt:
	    pass
