import Adafruit_BBIO.UART as UART
import obd


if __name__ == '__main__':

    UART.setup('UART2')
    obd_connection = obd.OBDUArt(port='/dev/ttyO2', baudrate=9600)

    print(repr(obd_connection.command('ATZ')))

    obd_connection.close()
