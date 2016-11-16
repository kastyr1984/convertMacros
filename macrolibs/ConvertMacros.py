import os.path
import re

from MacroHelpers import detectFileType

from NoxMacroHandler import NoxMacroHandler
from MEmuMacroHandler import MEmuMacroHandler

#this script aims to take all the guesswork out of converting macro scripts
#between MEmu and NOX

#all credit goes to /u/MLieBennett and /u/jcarl987 for giving me the tools to
#succeed here, I never would have even started to figure half this stuff out
#on my own

#big shout out to /u/-Pwnology- for making the scripts that make this a
#worthwhile endeavor in the first place
            
def processFiles(infile, outfile, outtype, intype = None, \
                 outyRez = 720, outxRez = 1280, \
                 inyRez = 720, inxRez = 1280, \
                 newnox = False, keymap = None, phone = None):
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
                outline = outMacroHandler.generateLine(entry.time, \
                                                       entry.presscode, \
                                                       entry.holdcode, \
                                                       entry.xPos, \
                                                       entry.yPos)
                
                outfile.write(outline)
                
                outfile.write('\n')
                
                