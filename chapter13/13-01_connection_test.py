import Adafruit_BBIO.UART as UART
import serial


def obd_read(serial_port):
    '''Read from the serial port until the read prompt, ">", is encountered.'''
    response = ''
    a_byte = serial_port.read()
    while a_byte != '>':
        response = response + a_byte
        a_byte = serial_port.read()

    return response

if __name__ == '__main__':

    UART.setup('UART2')
    obd = serial.Serial(port='/dev/ttyO2', baudrate=9600)
    obd.open()

    obd.write('ATZ' + '\r')
    print(repr(obd_read(obd)))

    obd.close()
