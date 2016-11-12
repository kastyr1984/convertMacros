import os.path

from DataTypes import *
from macroHelpers import detectFileType
from MEmuMacroHandler import *
from NoxMacroHandler import *

def mergeMacros(infile, mergefile, outfile, outtype, outyRez=720, outxRez = 1280, \
                inyRez = 720, inxRez = 1280, mergexRez = 720, mergeyRez = 1280, \
                mergeatline = None, newnox = False, keymap = None):
    myNoxMacroHandler = None
    myMemuMacroHandler = None
    
    indata = []
    mergedata = []
    outdata = []
    
    intype = detectFileType(infile)
    mergetype = detectFileType(mergefile)
    
    for valtype in (intype, mergetype, outtype):
        if valtype == 'memu':
            if not myMEmuMacroHandler:
                myMemuMacroHandler = MEmuMacroHandler()
            
        elif valtype == 'nox':
            if not myNoxMacroHandler:
                myNoxMacroHandler = NoxMacroHandler(noxKeyMap = keymap, newnoxout = newnox)
            
        else:
            #TODO raise error here
            return False
        
    if intype == 'memu':
        myMEmuMacroHandler.setOutRez(outyRez, outxRez)
        myMEmuMacroHandler.setInRez(inyRez, inxRez)
        
        indata = myMEmuMacroHandler.processFile(infile)
    elif intype == 'nox':
        myNoxMacroHandler.setOutRez(outyRez, outxRez)
        
        indata = myNoxMacroHandler.processFile(infile)
        
    if mergetype == 'memu':
        myMEmuMacroHandler.setOutRez(outyRez, outxRez)
        myMEmuMacroHandler.setInRez(mergeyRez, mergexRez)
        
        mergedata = myMEmuMacroHandler.processFile(mergefile)
    elif mergetype == 'nox':
        myNoxMacroHandler.setOutRez(outyRez, outxRez)
        
        mergedata = myNoxMacroHandler.processFile(mergefile)
        
    baseintime = None
    basemergetime = None
    currenttime = None
    
    #print(mergedata)
    
    #handles when files are to be appended
    if mergeatline in (None, False):
        mergeatline = len(indata)
        
    if mergeatline <= len(indata):
        #get lines from infile
        for line in indata[:mergeatline]:
            outdata.append(line)
            currenttime = line.time
            
        baseintime = currenttime
            
        for line in mergedata:
            currenttime = baseintime + line.time
            outdata.append(MacroLine(currenttime, \
                                     line.presscode, line.holdcode, \
                                     line.xPos, line.yPos, \
                                     line.inyRez, line.inxRez))
    
        basemergetime = currenttime
    
        for line in indata[mergeatline:]:
            currenttime = line.time + basemergetime
            
            outdata.append(MacroLine(currenttime, \
                                     line.presscode, line.holdcode, \
                                     line.xPos, line.yPos, \
                                     line.inyRez, line.inxRez))
    if outtype == 'memu':
        if myMEmuMacroHandler:
            myMEmuMacroHandler.setOutRez(outyRez, outxRez)
            for entry in outdata:
                outfile.write(myMEmuMacroHandler.generateLine(entry.time, \
                                                              entry.presscode, \
                                                              entry.holdcode, \
                                                              entry.xPos, \
                                                              entry.yPos))
                
                outfile.write('\n')
                
    elif outtype == 'nox':
        if myNoxMacroHandler:
            myNoxMacroHandler.setOutRez(outyRez, outxRez)
            for entry in outdata:
                outfile.write(myNoxMacroHandler.generateLine(entry.time, \
                                                            entry.presscode, \
                                                            entry.holdcode, \
                                                            entry.xPos, \
                                                            entry.yPos))
                
                outfile.write('\n')
                
    else:
        #TODO raise error here
        return False
                
if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='infile', nargs='?', type=argparse.FileType('r'), \
                        required=True, help='input macro file')
    parser.add_argument('-m', dest='mergefile', nargs='?', type=argparse.FileType('r'), \
                        required=True, help='macro file to append or merge')    
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
    
    parser.add_argument('--in-x', dest='inxRez', default=1280, type=int, \
                        help='merge file x resolution, ignored for Nox files')
    parser.add_argument('--in-y', dest='inyRez', default=720, type=int, \
                        help='merge file y resolution, ignored for Nox files')    
    
    parser.add_argument('--out-x', dest='outxRez', default=1280, type=int, \
                        help='output file x resolution')
    parser.add_argument('--out-y', dest='outyRez', default=720, type=int, \
                        help='output file y resolution')
    
    parser.add_argument('--outtype', dest='outtype', required=True, \
                        help='output file type, nox or memu')
    
    #parser.add_argument('--flip-xy', dest='flipxy', action='store_true', default=False,\
    #                    help='flip output x and y values')
    parser.add_argument('--new-nox', dest='newnox', action='store_true', default=False,\
                            help='output nox files in ScRiPtSePaRaToR style')    
    
    args = parser.parse_args()
    
    if args.infile and args.mergefile and args.outfile and args.outtype:
        mergeMacros(args.infile, args.mergefile, args.outfile, args.outtype, \
                    outyRez = args.outyRez, outxRez = args.outxRez, \
                    inyRez = args.inyRez, outxRez = args.inxRez, \
                    mergeyRez = args.mergeyRez, mergexRez = args.mergexRez, \
                     keymap = args.keymapfile, newnox = args.newnox)
    else:
        parser.print_help()
