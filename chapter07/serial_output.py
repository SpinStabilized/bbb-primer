import Adafruit_BBIO.UART as UART
import serial

UART.setup("UART1")
tty1 = serial.Serial(port="/dev/ttyO1", baudrate=9600)

tty1.open()
tty1.write('FE01'.decode('hex'))	
tty1.write('A')
tty1.close()