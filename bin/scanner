#!/usr/bin/env python3

import os
import sys
import argparse
from swindle.scanner import Scanner

def main(argv):
    aparser = argparse.ArgumentParser(description='Scan a file.')
    aparser.add_argument('files', metavar='file', type=str, nargs='+',
                               help='a file for the scanner')

    args = aparser.parse_args()
    print(args.files)
    scanner = Scanner(args.files[0])

if __name__ == '__main__':
    main(sys.argv)
