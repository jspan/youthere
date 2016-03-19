#!/usr/bin/env python
'''
Read arduino serial port and log to file
'''
import datetime
import logging
import serial
import sys
import time

SERIAL_DEV = '/dev/ttyUSB0'

CHECK_PERIOD_SEC = 1

def get_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, 'Usage: %s LOG_FILE' % sys.argv[0]
        sys.exit(1)

    log_file = sys.argv[1]

    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')
    logging.info('-> start %s' % (get_timestamp()))

    ser = serial.Serial(SERIAL_DEV, 9600)
    time.sleep(2)

    try:
        while True:
            char = ser.read(ser.inWaiting())
            if char in ['0', '1']:
                logging.info('%s %s' % (char, get_timestamp()))

            time.sleep(CHECK_PERIOD_SEC)

    except serial.serialutil.SerialException, IOError:
        pass

if __name__ == '__main__':
    main()
