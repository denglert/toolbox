#!/usr/bin/env python

import argparse
import sys
import pandas_utils as pdu

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert HDF5 to ASCII.')

    # - Positional arguments
    parser.add_argument("input",  help="input file")
    parser.add_argument("output", help="output file")

    # - Flags
    parser.add_argument('-t', '--tab',           dest='tabular',      action='store_true',
            help="Use tabular separation.")
    parser.add_argument('-ff', '--float-format', dest='float_format', help="Specify the float format.")

    # - Default 
    #parser.set_defaults(tabular=False)

    args = parser.parse_args()
    #args = vars(parser.parse_args())

    print('Input  file: {}'.format( args.input )  )
    print('Output file: {}'.format( args.output ) )

    if args.tabular:
        print('Separator: tab (    )')
        sep = '\t'
    else:
        print('Separator: single space ( )')
        sep = ' '


    if args.float_format:
        float_format = args.float_format
    else:
        float_format = '%.3e'

    print('Float format: {}'.format(float_format))

    # - Call
    pdu.hdf5_to_ascii(args.input, args.output, sep, float_format)
