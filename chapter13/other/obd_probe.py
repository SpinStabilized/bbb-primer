import serial
import Adafruit_BBIO.UART as UART

PORT = '/dev/ttyO2'
BAUD = 38400
UART.setup("UART2")


def obd_read(serial_port):
    a_byte = serial_port.read()
    response = ''
    while a_byte != '>':
        response = response + a_byte
        a_byte = serial_port.read()

    return response


def snd_cmd(serial_port, cmd):
    '''Add a "\\r" to the command, send it, and check the response'''
    serial_port.write(cmd + '\r')
    response = obd_read(serial_port)
    response = response.strip().split('\r')
    response = filter(None, response)
    response = [s.strip() for s in response]
    if response[0] != cmd:
        err_msg = 'Unexpected command echo. Expected {} received {}.'
        print(err_msg.format(cmd, response[0]))
    else:
        response.pop(0)

    return '\n'.join(response)


def snd_cmd(serial_port, cmd):
    serial_port.write(cmd + '\r')
    response = obd_read(serial_port)
    response = filter(None, response.strip().split('\r'))
    if response[0] != cmd:
        print('COMM ERROR: Unexpected command echo. Expected {} but received {}'.format(cmd, response[0]))
        return None
    else:
        response.pop(0)

    if response[0] == 'SEARCHING...':
        response.pop(0)

    if len(response) > 1:
        response = process_multi(response)

    return response


def bytes_to_boolean(byte_list):
    str_bits = ''.join(['{:0>8b}'.format(b) for b in byte_list])
    return [False if bit == '0' else True for bit in str_bits]


def to_bytes(str):
    return [hex_to_int(byte) for byte in str.strip().split(' ')]


def hex_to_int(str):
    return int('0x' + str, 16)


def process_multi(multi_line):
    byte_count = hex_to_int(multi_line[0])
    packets = multi_line[1:]
    packets = [line.strip().split(' ')[1:] for line in packets]
    byte_list = [item for sublist in packets for item in sublist]
    if len(byte_list) != byte_count:
        print('Didnt receive the expected number of bytes')
    return ' '.join(byte_list)


def decode_dtc(byte_list):
    first_list = ['P', 'C', 'B', 'U']
    chars = [first_list[((byte_list[0] & 0b11000000) >> 6)],
             (byte_list[0] & 0b00110000) >> 4,
             byte_list[0] & 0b00001111,
             byte_list[1]]
    return '{}{:0>1x}{:0>1x}{:0>2x}'.format(*chars)


def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def bytes_to_boolean(byte_list):
    str_bits = ''.join(['{:0>8b}'.format(b) for b in byte_list])
    return [False if bit == '0' else True for bit in str_bits]


def join_bytes(byte_list):
    shift_list = range(2**(len(byte_list) + 1), -1, -8)
    enumerated_bytes = enumerate(byte_list)
    return sum([byte << shift_list[i] for i, byte in enumerated_bytes])

if __name__ == '__main__':

    obd = serial.Serial(port=PORT, baudrate=BAUD)
    obd.open()

    print(snd_cmd(obd, 'atz'))
    print(snd_cmd(obd, 'atsp0'))
    modes = [0x01, 0x09]
    for mode in modes:

        results = [True]

        while results[-1]:
                pid = len(results) - 1
                cmd = '{:0>2x}{:0>2x}'.format(mode, len(results) - 1)
                response = snd_cmd(obd, cmd)
                if pid == 0 and 'NO DATA' in response[0]:
                    results = ([False] * 0x21)
                else:
                    response = to_bytes(response[0])
                    header, payload = response[0:2], response[2:]
                    bool_list = bytes_to_boolean(payload)
                    results.extend(bool_list)

        for pid, present in enumerate(results):
            if present:
                cmd = '{:0>2x}{:0>2x}'.format(mode, pid)
                print(repr(snd_cmd(obd, cmd)))

    obd.close()
