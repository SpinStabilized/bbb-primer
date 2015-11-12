#!/usr/bin/env python

import Adafruit_BBIO.UART as UART
import obd
import time
from datetime import datetime

SAMPLE_RATE = 2  # Hertz
TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M-%S'

if __name__ == '__main__':

    UART.setup("UART2")
    obd_con = obd.OBDUart(port='/dev/ttyO2', baudrate=9600)
    car = obd.Car(obd_con)

    start_time = datetime.now().strftime(TIMESTAMP_FORMAT)
    output_file = 'data_{}.jpeg'.format(start_time)

    try:
        with open(output_file, 'w') as f:
            while True:
                f.write('{}, {}'.format(car.speed(), car.tachometer()))
                time.sleep(1/SAMPLE_RATE)

    except KeyboardInterrupt:
        obd_con.close
