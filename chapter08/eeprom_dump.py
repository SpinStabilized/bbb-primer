import Adafruit_I2C import Adafruit_I2C



eeprom = Adafruit_I2C(0x57)


print(eeprom.readList(0x00, 4))
	

