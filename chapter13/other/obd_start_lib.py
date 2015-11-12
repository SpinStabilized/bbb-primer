import serial


class OBDUart(object):

    def __init__(self, port, baudrate, line_end='\r', prompt='>', echo=True):
        self.port = port
        self.baudrate = baudrate
        self.line_end = line_end
        self.prompt = prompt
        self.echo = echo

        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate)
        self.ser.open()

    def send(self, command):
        self.serial.write(command + self.line_end)

    def read(self):
        '''Read from the serial port until the prompt is encountered.'''
        response = ''
        a_byte = self.ser.read()
        while a_byte != self.prompt:
            response = response + a_byte
            a_byte = self.ser.read()

        return response

    def close(self):
        self.serial.close()

    def command(self, command):
        self.send(command)
        response = self.read()

        response = response.split(self.line_end)
        response = filter(None, response)
        response = [line.strip() for line in response]

        if self.echo:
            if command not in response[0]:
                msg = 'obd.OBDUart: Echo check failed. Found {}, expected {}.'
                raise Exception(msg.format(response[0]), command)
            else:
                response.pop(0)

        return response

class Car(object):

    def __init__(self, obd_connection):
        self.obd_connection = obd_connection

        initialize_response = self.obd_connection.command('ATZ')
        if 'ELM' not in initialize_response:
            raise Exception('obd.Car.init: OBDUart Initilization Failed')

        autoset_interface = self.obd_connection.command('ATSP0')
        if 'OK' not in autoset_interface:
            raise Exception('obd.Car.init: OBDUart Interface Autoset Failed')

    def raw_command(self, command):
        return self.obd_connection.command(command)

    def command(self, mode, pid):
        command_string = '{:0>2x}{:0>2x}'.format(mode, pid)
        response = self.raw_command.command(command_string)

        response = response.strip()
        response = response.split(' ')

        for byte in response:
            byte = int(byte.strip(), 16)

        response_mode = response[0] - 0x40
        response_pid = response[1]
        response_data = response[2:]

        if response_mode != mode or response_pid != pid:
            raise Exception('obd.Car.command: Recieved unexpected Mode or PID')

        return response_data

    def speed(self):
        speed = self.command(0x01, 0x0D)
        return speed[0]

    def tachometer(self):
        tach = self.command(0x01, 0x0C)
        tach = (tach[0] << 8) | tach[1]
        return tach


