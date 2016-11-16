from macrolib import MergeMacros

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='infile', nargs=1, type=argparse.FileType('r'), \
                        required=True, help='input macro file')
    parser.add_argument('-m', dest='mergefiles', nargs='+', type=argparse.FileType('r'), \
                        required=True, help='macro file(s) to append or merge')    
    parser.add_argument('-o', dest='outfile', nargs='?', type=argparse.FileType('w'),
                         default=sys.stdout, help='output macro file (prints to terminal if none provided)')
    parser.add_argument('-k', dest='keymapfile', nargs='?', type=argparse.FileType('r'),
                         default=None, required=False, help='input nox keymap, if needed')
    
    parser.add_argument('-l', dest='mergeline', default=None, type=int, \
                        help='line to merge at, defaults to appending merge file')    
    
    parser.add_argument('--in-x', dest='inxRez', default=1280, type=int, \
                        help='input file x resolution, ignored for Nox files')
    parser.add_argument('--in-y', dest='inyRez', default=720, type=int, \
                        help='input file y resolution, ignored for Nox files')
    
    parser.add_argument('--merge-x', dest='mergexRez', default=1280, type=int, \
                        help='merge file x resolution, ignored for Nox files')
    parser.add_argument('--merge-y', dest='mergeyRez', default=720, type=int, \
                        help='merge file y resolution, ignored for Nox files')    
    
    parser.add_argument('--out-x', dest='outxRez', default=1280, type=int, \
                        help='output file x resolution')
    parser.add_argument('--out-y', dest='outyRez', default=720, type=int, \
                        help='output file y resolution')
    
    parser.add_argument('--outtype', dest='outtype', required=True, \
                        help='output file type, nox or memu')
    
    parser.add_argument('--new-nox', dest='newnox', action='store_true', default=False,\
                            help='output nox files in ScRiPtSePaRaToR style')    
    
    args = parser.parse_args()
    
    if args.infile and args.mergefile and args.outfile and args.outtype:
        MergeMacros.mergeMacros(args.infile, args.outfile, args.outtype, args.mergefiles, \
                                outyRez = args.outyRez, outxRez = args.outxRez, \
                                inyRez = args.inyRez, inxRez = args.inxRez, \
                                mergeyRez = args.mergeyRez, mergexRez = args.mergexRez, \
                                keymap = args.keymapfile, newnox = args.newnox)
    else:
        parser.print_help()
