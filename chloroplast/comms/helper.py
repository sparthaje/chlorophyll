# Shreepa Parthaje

import glob
import sys

from serial import Serial, SerialException
from serial.tools import list_ports

from .printer import log


def list_serial_ports(debug):
    """ Lists serial port names
        :raises EnvironmentError: On unsupported or unknown platforms
        :returns A list of the serial ports available on the system
        :source http://stackoverflow.com/questions/12090503/ddg#14224477
   """

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except SerialException:
            pass

    if debug and len(result) == 0 and len(list_ports.comports()) > 0:
        log(f'Fix permissions for these devices (sudo chmod 777): {[port.device for port in list_ports.comports()]}',
            'WARNING')
        log('Or close the serial port if its already open\n', 'WARNING')

    return result


def get_port(settings):
    """ Based on the env settings, either chooses the first available port or allows the user to pick the port """
    ports = list_serial_ports(settings['DEBUG'])

    if settings['PRODUCTION']:
        ports = [port for port in ports if 'USB' in port]
        if len(ports) > 1:
            ports = ports[:1]

    if len(ports) == 0:
        if settings['PRODUCTION']:
            raise OSError('No serial device connected')
        else:
            if settings['DEBUG']:
                log('No serial device connected\n', 'FAIL')
            return None

    if len(ports) == 1:
        port_index = 0
    else:
        port_index = int(input(f'Choose which serial port to use (0-{len(ports) - 1}): {ports}: '))

    return ports[port_index]
