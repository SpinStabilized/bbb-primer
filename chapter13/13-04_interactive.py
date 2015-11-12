import Adafruit_BBIO.UART as UART
import obd

if __name__ == '__main__':

    UART.setup("UART2")
    obd_con = obd.OBDUart(port='/dev/ttyO2', baudrate=9600)

    while True:
        cmd = raw_input('> ')
        if cmd == 'q':
            break
        else:
            response = obd_con.command(cmd)
            for msg in response:
                print msg

    obd_con.close()
