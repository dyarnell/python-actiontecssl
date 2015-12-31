#!/usr/bin/env python

import logging
import argparse
from actiontecssl import ActiontecSSL


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str, help='The host name or IP address'
                                               ' of the remote computer to '
                                               'which you are connecting.')
    parser.add_argument('port', type=int, help='The port number or '
                                               'service name.')
    parser.add_argument('password', type=str, help='Password for the router')

    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING)

    a = ActiontecSSL(host=args.host, port=args.port, password=args.password)
    a.connect()
    print (a.interfaces())
    print (a.processes())
    print (a.ifstats())
    print (a.meminfo())
    print (a.cpus())
