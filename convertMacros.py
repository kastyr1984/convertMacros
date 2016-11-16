from macrolib import ConvertMacros

if __name__ == '__main__':
    import argparse
    import sys
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='infile', nargs='?', type=argparse.FileType('r'), \
                        required=True, help='input macro file')
    parser.add_argument('-o', dest='outfile', nargs='?', type=argparse.FileType('w'),
                         default=sys.stdout, help='output macro file (prints to terminal if none provided)')
    parser.add_argument('-k', dest='keymapfile', nargs='?', type=argparse.FileType('r'),
                         default=None, required=False, help='input nox keymap, if needed')
    
    parser.add_argument('--in-x', dest='inxRez', default=1280, type=int, \
                        help='input file x resolution, ignored for Nox files')
    parser.add_argument('--in-y', dest='inyRez', default=720, type=int, \
                        help='input file y resolution, ignored for Nox files')
    
    parser.add_argument('--out-x', dest='outxRez', default=1280, type=int, \
                        help='output file x resolution')
    parser.add_argument('--out-y', dest='outyRez', default=720, type=int, \
                        help='output file y resolution')
    
    parser.add_argument('--intype', dest='intype', default=None, \
                        help='input file type, nox or memu')
    parser.add_argument('--outtype', dest='outtype', required=True, \
                        help='output file type, nox or memu')
    
    parser.add_argument('--new-nox', dest='newnox', action='store_true', default=False,\
                            help='output nox files in ScRiPtSePaRaToR style')
    
    parser.add_argument('--phone', dest='phone', action='store_true', default=False,\
                            help='output files with adjustment for phone resolution (testing)')    
    
    args = parser.parse_args()
    
    if args.infile and args.outfile and args.outtype:
        ConvertMacros.processFiles(args.infile, args.outfile, args.outtype, \
                                   intype = args.intype, \
                                   outyRez = args.outyRez, outxRez = args.outxRez, \
                                   inyRez = args.inyRez, inxRez = args.inxRez, \
                                   keymap = args.keymapfile, newnox = args.newnox, \
                                   phone = args.phone)
    else:
        parser.print_help()
        
