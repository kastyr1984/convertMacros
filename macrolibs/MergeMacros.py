import os.path

from DataTypes import *
from MacroHelpers import detectFileType, is_sequence
from MEmuMacroHandler import *
from NoxMacroHandler import *

def mergeMacros(infile, outfile, outtype, mergefiles, outyRez=720, outxRez = 1280, \
                inyRez = 720, inxRez = 1280, mergexRez = 720, mergeyRez = 1280, \
                mergeatline = None, newnox = False, keymap = None):
    myNoxMacroHandler = None
    myMemuMacroHandler = None
    
    indata = []
    mergedata = []
    outdata = []
    
    if not is_sequence(mergefiles):
        if isinstance(mergefiles, str):
            mergefiles = [mergefiles]
        else:
            #TODO raise error here
            return False
    
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