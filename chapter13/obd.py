import logging
import serial
import json

logger = logging.getLogger(__name__)


class OBDToUART(object):
    '''Interface to the SparkFun OBD to UART hardware.

    This module is designed to interface to the SparkFun Electronics OBD to
    UART hardware board. For more information, please check out the
    SparkFun website. Part ID: WIG-09555

    The methods of this class for sending and receiving commands abstract
    away some of the details and checks the command echo.
    '''

    def __init__(self, port, baud=9600, line_ending='\r', ready_char='>'):
        '''Initialize with a port (required) and baud rate.

        Args:
            port: String indicating the serial port to use
            baud: Integer number for the baud rate

        Raises:
            SerialException: Could not get the port requested.
        '''
        self.line_ending = line_ending
        self.ready_char = ready_char
        self.port = port
        self.baud = baud

        try:
            self._serial = serial.Serial(port=port, baudrate=baud)
        except Exception as e:
            logger.error('Unable to open port {}'.format(port))
            raise e

        self._serial.open()
        self.reset()
        logger.info('Connected to {}.'.format(self.hardware()))
        logger.info('Firmware: '.format(self.firmware()))
        logger.info('Manufacured By: {}'.format(self.manufacturer()))
        logger.info('Serial Number: {}'.format(self.serial_number()))

    def __repr__(self):
        return '<{}>'.format(self.__str__())

    def __str__(self):
        message = 'OBDToUART Object Connected To {} on {}'
        return message.format(self.hardware(), self.port)

    def send(self, command):
        '''Send a command to the device with the line ending added.'''
        command = command + self.line_ending
        self._serial.write(command)

    def read(self):
        '''Get a response from the device.

        Captures all data until a hardware ready character is received. The
        data is then split into a list of cleaned strings.
        '''
        a_byte = self._serial.read()
        response = ''
        while a_byte != self.ready_char:
            response = response + a_byte
            a_byte = self._serial.read()

        response = response.split(self.line_ending)
        response = filter(None, response)
        return response

    def command(self, command=''):
        '''Send a command to the device and return the results.

        This method uses the object's send and read methods to transmit a
        command to the device and wait for the response. The response is
        checked for the expected command echo value, which is not part of
        the returned information.
        '''
        self.send(command)
        response = self.read()
        if response[0] != command:
            error_msg = 'Unexpected Command Echo. Expected {} but received {}.'
            logger.warning(error_msg.format(command, response[0]))

        return response[1:]

    def disconnect(self):
        '''Close out the serial connection.'''
        logger.info('Disconnecting from {}.'.format(self.hardware()))
        self._serial.close()

    def reset(self):
        '''Reset the hardware interface'''
        self.command('ATZ')
        logger.info('Interface Reset')

    def hardware(self):
        '''Retrieve the device hardware identifier'''
        response = self.command('STDI')
        return response[0]

    def firmware(self):
        '''Retrieve the device firmware version'''
        response = self.command('STI')
        return response[0]

    def manufacturer(self):
        '''Retrieve the device manufacturer'''
        response = self.command('STMFR')
        return response[0]

    def serial_number(self):
        '''Retrieve the device serial number'''
        response = self.command('STSN')
        return response[0]

    def auto_protocol(self):
        '''Set the device to autodetect the OBD protocols'''
        response = self.command('ATSP0')
        if 'OK' not in response[0]:
            wrn_msg = 'Auto Set Protocol Error. Response {}'
            logger.warning(wrn_msg.format(response[0]))

    def get_protocol(self):
        '''Determine the OBD protocol in use.'''
        response = self.command('ATDP')
        return response[0]


def to_bytes(str):
    '''Convert a space seperated string of hex numbers into a list'''
    return [int(byte, 16) for byte in str.strip().split(' ')]


def bytes_to_boolean(byte_list):
    '''Interpret a list of bytes as a list of booleans'''
    str_bits = ''.join(['{:0>8b}'.format(b) for b in byte_list])
    return [bool(int(bit)) for bit in str_bits]


def join_bytes(byte_list):
    shift_list = range(2**(len(byte_list) + 1), -1, -8)
    enumerated_bytes = enumerate(byte_list)
    return sum([byte << shift_list[i] for i, byte in enumerated_bytes])


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def rem_ctrl_chars(str):
    ctrl_chars = ''.join([chr(c) for c in range(0x00, 0x20)])
    return str.translate(None, ctrl_chars)


def mil_stat_decode(byte_list):
    status = {}
    status['mil_on'] = bool(int(byte_list[0] & 0b10000000))
    status['err_cnt'] = byte_list[0] & 0b01111111
    byte_b = bytes_to_boolean(byte_list[1])[::-1]
    byte_c = bytes_to_boolean(byte_list[2])[::-1]
    byte_d = bytes_to_boolean(byte_list[3])[::-1]
    tests = {}
    tests['misfire'] = {'availible': byte_b[0], 'incomplete': byte_b[4]}
    tests['fuel_sys'] = {'availible': byte_b[1], 'incomplete': byte_b[5]}
    tests['components'] = {'availible': byte_b[2], 'incomplete': byte_b[6]}
    tests['reserved'] = {'availible': byte_b[3], 'incomplete': byte_b[7]}
    tests['catalyst'] = {'availible': byte_c[0], 'incomplete': byte_d[0]}
    tests['heat_cat'] = {'availible': byte_c[1], 'incomplete': byte_d[1]}
    tests['evap'] = {'availible': byte_c[2], 'incomplete': byte_d[2]}
    tests['sec_air'] = {'availible': byte_c[3], 'incomplete': byte_d[3]}
    tests['ac_ref'] = {'availible': byte_c[4], 'incomplete': byte_d[4]}
    tests['o2_sen'] = {'availible': byte_c[5], 'incomplete': byte_d[5]}
    tests['o2_htr'] = {'availible': byte_c[6], 'incomplete': byte_d[6]}
    tests['egr'] = {'availible': byte_c[7], 'incomplete': byte_d[7]}
    status['tests'] = tests
    return status


class Car(object):
    def __init__(self, obd_interface, pid_db_file='pid_db.json'):
        self.obd = obd_interface
        self.valid_modes = [0x01, 0x09]
        self.valid_commands = {}

        self.pid_db = None
        with open(pid_db_file, 'r') as f:
            self.pid_db = json.load(f)

        for pid in self.pid_db:
            self.pid_db[pid]['mode'] = int(self.pid_db[pid]['mode'], 16)
            self.valid_modes.append(self.pid_db[pid]['mode'])
            self.pid_db[pid]['pid'] = int(self.pid_db[pid]['pid'], 16)
            interpret_function = eval(self.pid_db[pid]['interpreter'])
            self.pid_db[pid]['interpreter'] = interpret_function

        self.valid_modes = set(self.valid_modes)
        self.refresh_valid_commands()

    def obd_cmd(self, mode, pid):
        cmd = '{:0>2x}{:0>2x}'.format(mode, pid)
        response = self.obd.command(cmd)

        # Check for some error conditions
        if not response:
            msg = 'No response to command Mode 0x{:0>2x}, PID 0x{:0>2x}.'
            logger.warning(msg.format(mode, pid))
            return []

        if 'NO DATA' in response[0]:
            msg = 'Invalid command. Mode 0x{:0>2x}, PID 0x{:0>2x}.'
            logger.warning(msg.format(mode, pid))
            return []

        if 'SEARCHING' in response[0]:
            response.pop(0)

        # Looks like we have a good response so far, check if we have a
        # multi-line response and condense it if we do
        if len(response) > 1:
                byte_count = int(response[0], 16)
                packets = response[1:]
                data = ''.join([packet[3:] for packet in packets])
                data_bytes = data.split(' ')[:byte_count]
                response = ' '.join(data_bytes)

        else:
            response = response[0]

        # Convert the response into a list of integers
        response = to_bytes(response)
        header = response[:2]
        payload = response[2:]
        if header[0] != mode + 0x40 or header[1] != pid:
            msg = 'Received header did not match command sent.'
            logger.error(msg)
            msg = 'Expected Mode 0x{:0>2x} PID 0x{:0>2x}.'
            logger.error(msg.format(mode, pid))
            msg = 'Found Mode 0x{:0>2x} PID 0x{:0>2x}.'
            logger.error(msg.format(header[0] - 0x40, header[1]))
            return []
        else:
            return payload

    def valid(self, mode, pid):
        if not self.valid_commands:
            self.refresh_valid_commands()

        if mode not in self.valid_commands:
            return False

        if pid >= len(self.valid_commands[mode]):
            return False

        return self.valid_commands[mode][pid]

    def refresh_valid_commands(self):
        self.valid_commands = {}
        for mode in self.valid_modes:
            results = [True]
            while results[-1]:
                    pid = len(results) - 1
                    response = self.obd_cmd(mode, pid)
                    results.extend(bytes_to_boolean(response))
            self.valid_commands[mode] = results

    def valid_mnemonics(self):
        valid_list = []
        for pid in self.pid_db:
            if self.valid(self.pid_db[pid]['mode'], self.pid_db[pid]['pid']):
                valid_list.append(pid)
        return valid_list

    def mnemonic_cmd(self, mnemonic, as_string='False'):
        mode, pid = self.pid_db[mnemonic]['mode'], self.pid_db[mnemonic]['pid']
        resp = self.obd_cmd(mode, pid)
        value = self.pid_db[mnemonic]['interpreter'](resp)
        if as_string:
            units = self.pid_db[mnemonic]['units']
            if len(units) == 1:
                value = [value]

            str_list = ['{} {}'.format(v, u) for v, u in zip(value, units)]
            str_list = ', '.join(str_list)
            return str_list
        else:
            return value
