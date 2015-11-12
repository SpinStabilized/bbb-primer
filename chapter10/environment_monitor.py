#!/usr/bin/env python

import Adafruit_BBIO.ADC as ADC
import time
import phant

# Configue the ADC
ADC.setup()

# Define program constants
TMP36_PIN   = 'AIN0'
PHOTO_PIN   = 'AIN1'

PHANT_PRIVATE_KEY = 'YOUR_PRIVATE_KEY'
PHANT_PUBLIC_KEY  = 'YOUR_PUBLIC_KEY'

SAMPLE_RATE = 0.0033  # Hertz

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

def celsius_to_fahrenheit(degrees_celsius):
	''' Returns the the input celsius temperature as fahrenheit

	Keyword arguments:
	degrees_celsius - ADC reading in volts (Required)

	Return:
	Temperature in fahrenheit
	'''
	return (degrees_celsius * 1.8) + 32

if __name__ == '__main__':

	sparkfun_data = phant.Phant(PHANT_PUBLIC_KEY, 'temperature', 'lights_on',
		                        private_key=PHANT_PRIVATE_KEY)

	while True:
		temperature = tmp36_v_to_t(read_adc_v(TMP36_PIN))
		temperature = celsius_to_fahrenheit(temperature)
		lights_status = lights_on(read_adc_v(PHOTO_PIN))

		try:
			sparkfun_data.log(temperature, lights_status)
		except:
			# If a connection error is encountered, just skip the sample and
			# keep running so as to not crash the service.
			pass

		time.sleep(1/SAMPLE_RATE)
