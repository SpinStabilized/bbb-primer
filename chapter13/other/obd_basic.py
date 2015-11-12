import Adafruit_BBIO.UART as UART
import obd
import logging
import sys

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=logging_format,
                        datefmt='%m-%d %H:%M',
                        filename='obd_basic.log',
                        filemode='w')

    UART.setup('UART2')
    port = '/dev/ttyO2'
    baud = 38400

    try:
        msg = 'Attempting to connect to {} at rate {}'
        logging.info(msg.format(port, baud))
        obd_connect = obd.OBDToUART(port=port, baud=baud)
    except Exception as e:
        msg = 'Unable to open connection to OBD hardware on port {}. Exiting.'
        logging.error(msg.format(port))
        print(msg.format(port))
        sys.exit()

    car = obd.Car(obd_connect)
    cmds = car.valid_mnemonics()
    cmds = [cmd for cmd in cmds if 'mode' not in cmd]
    cmds.sort()

    width = len(max(cmds, key=len))
    for cmd in cmds:
        output_format = '{:<{width}}: {}'
        cmd_response = car.mnemonic_cmd(cmd, as_string=True)
        print(output_format.format(cmd, cmd_response, width=width))
    obd_connect.disconnect()
