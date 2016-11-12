import os.path
import re

from MacroLib.MacroHelpers import detectFileType

from MacroLib.NoxMacroHandler import NoxMacroHandler
from MacroLib.MEmuMacroHandler import MEmuMacroHandler

#this script aims to take all the guesswork out of converting macro scripts
#between MEmu and NOX

#all credit goes to /u/MLieBennett and /u/jcarl987 for giving me the tools to
#succeed here, I never would have even started to figure half this stuff out
#on my own

#big shout out to /u/-Pwnology- for making the scripts that make this a
#worthwhile endeavor in the first place
            
def processFiles(infile, outfile, outtype, intype = None, outyRez=720, outxRez = 1280, inyRez = 720, inxRez = 1280, newnox = False, keymap = None):
    #basic filetype detection if intype is not provided
    if not intype:
        intype = detectFileType(infile)
        
    #just in case we get 'NOX' or 'MEmu' as intype arguments
    intype = intype.lower()
    outtype = outtype.lower()
    
    #output data container
    outdata = []
    
    inMacroHandler = None
    outMacroHandler = None
    
    #process the input file
    if intype == 'memu':
        inMacroHandler = MEmuMacroHandler(outyRez, outxRez, inyRez, inxRez)
    elif intype == 'nox':
        inMacroHandler = NoxMacroHandler(outyRez, outxRez, noxKeyMap = keymap, newnoxout = newnox)
        
    if inMacroHandler:
        outdata = inMacroHandler.processFile(infile)
    else:
        #TODO raise error here
        return False
    
    #reuse the original macro handler if we can
    
    #this program is almost overkilling it on resource cheapskateness
    if outdata:
        if outtype != inMacroHandler.handlertype:
            if outtype == 'memu':
                outMacroHandler = MEmuMacroHandler(outyRez, outxRez, inyRez, inxRez)
            elif outtype == 'nox':
                outMacroHandler = NoxMacroHandler(outyRez, outxRez, noxKeyMap = keymap, newnoxout = newnox)
            else:
                #TODO raise error here
                return False
        else:
            outMacroHandler = inMacroHandler
            
        if outMacroHandler:
            for entry in outdata:
                outfile.write(outMacroHandler.generateLine(entry.time, \
                                                           entry.presscode, \
                                                           entry.holdcode, \
                                                           entry.xPos, \
                                                           entry.yPos))
                
                outfile.write('\n')
                
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
    
    args = parser.parse_args()
    
    if args.infile and args.outfile and args.outtype:
        processFiles(args.infile, args.outfile, args.outtype, \
                     intype = args.intype, \
                     outyRez = args.outyRez, outxRez = args.outxRez, \
                     inyRez = args.inyRez, inxRez = args.inxRez, \
                     keymap = args.keymapfile, newnox = args.newnox)
    else:
        parser.print_help()
        