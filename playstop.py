#!/usr/bin/env python3

import serial
from serial.tools import list_ports
from mpd import MPDClient

MPD_HOST = '192.168.0.200'
MPD_PORT = 6600
MPD_TIMEOUT = 10
SER_TIMEOUT = 5
BAUDRATE = 9600
USB = 'USB VID:PID=2341:8037'


def main():

    comport = None
    search = USB.lower()

    for port in list_ports.comports():
        if search in port[2].lower():
            comport = port[0]
            break

    if not comport:
        raise Exception('comport not found')

    # initialize serial connection
    ser = serial.Serial(comport, BAUDRATE, timeout=SER_TIMEOUT)

    # initialize MPD connection
    client = MPDClient()
    client.timeout = MPD_TIMEOUT

    try:
        client.connect(MPD_HOST, MPD_PORT)
    except Exception as e:
        return print(e)
    else:
        print('connected')

    while ser.isOpen():

        # receive button state
        line = ser.readline()
        line = line.decode()
        line = line.strip()

        if 'STOP' == line:
            print('pause')
            client.pause()  # change to stop()
        elif 'PLAY' == line:
            print('play')
            client.play()

        # get current MPD state
        state = client.status()['state']

        # send MPD state to switch LED on/off
        if state == 'play':
            ser.write(b'PLAY')
        if state == 'pause' or state == 'stop':
            ser.write(b'STOP')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
