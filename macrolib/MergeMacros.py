import os.path

from macrolib.DataTypes import *
from macrolib.MacroHelpers import detectFileType, is_sequence
from macrolib.MEmuMacroHandler import *
from macrolib.NoxMacroHandler import *

#This function merges one or more "mergefiles" into an "infile"
#and outputs either to the outfile or to the stdout.

def mergeMacros(infile, outfile, outtype, mergefiles, outyRez = 720.0, outxRez = 1280.0, \
                inyRez = 720.0, inxRez = 1280.0, mergexRez = 720.0, mergeyRez = 1280.0, \
                mergeatline = None, newnox = False, keymap = None):
    
    myNoxMacroHandler = None
    myMEmuMacroHandler = None
    myHiroMacroHandler = None
    
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
    
    for valtype in (intype, outtype):
        if valtype == 'memu':
            if not myMEmuMacroHandler:
                myMEmuMacroHandler = MEmuMacroHandler(outyRez = outyRez, outxRez = outxRez)
            
        elif valtype == 'nox':
            if not myNoxMacroHandler:
                myNoxMacroHandler = NoxMacroHandler(outyRez = outyRez, outxRez = outxRez, noxKeyMap = keymap, newnoxout = newnox)
                
        elif valtype == 'hiro':
            if not myHiroMacroHandler:
                myHiroMacroHandler = HiroMacroHandler(outyRez = outyRez, outxRez = outxRez, hiroKeyMap = keymap)
            
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
    elif intype == 'hiro':
        myHiroMacroHandler.setOutRez(outyRez, outxRez)
        myHiroMacroHandler.setInRez(inyRez, inxRez)
        
        indata = myHiroMacroHandler.processFile(infile)
        
    baseintime = None
    basemergetime = None
    currenttime = None
    
    #print(mergedata)
    
    #handles when files are to be appended
    if mergeatline in (None, False):
        mergeatline = len(indata)
        
    #handles when files are merged
    if mergeatline <= len(indata):
        #get lines from infile
        for line in indata[:mergeatline]:
            outdata.append(line)
            currenttime = int(line.time)
            
        baseintime = currenttime
    
    for mergefile in mergefiles:
        #print(mergefile)
        
        mergetype = detectFileType(mergefile)
        
        if mergetype == 'memu':
            if not myMEmuMacroHandler:
                myMEmuMacroHandler = MEmuMacroHandler(outyRez = outyRez, outxRez = outxRez)

        elif mergetype == 'nox':
            if not myNoxMacroHandler:
                myNoxMacroHandler = NoxMacroHandler(outyRez = outyRez, outxRez = outxRez, noxKeyMap = keymap, newnoxout = newnox)
                
        elif mergetype == 'hiro':
            if not myHiroMacroHandler:
                myHiroMacroHandler = HiroMacroHandler(outyRez = outyRez, outxRez = outxRez, hiroKeyMap = keymap)
        
        if mergetype == 'memu':
            myMEmuMacroHandler.setOutRez(outyRez, outxRez)
            myMEmuMacroHandler.setInRez(mergeyRez, mergexRez)
            
            mergedata = myMEmuMacroHandler.processFile(mergefile)
        elif mergetype == 'nox':
            myNoxMacroHandler.setOutRez(outyRez, outxRez)
            
            mergedata = myNoxMacroHandler.processFile(mergefile)
            
        elif mergetype == 'hiro':
            myHiroMacroHandler.setOutRez(outyRez, outxRez)
            myHiroMacroHandler.setInRez(inyRez, inxRez)
            
            mergedata = myHiroMacroHandler.processFile(mergefile)
                    
        for line in mergedata:
            currenttime = baseintime + int(line.time)
            outdata.append(MacroLine(currenttime, \
                                     line.presscode, line.holdcode, \
                                     line.xPos, line.yPos, \
                                     line.inyRez, line.inxRez))
            
        baseintime = currenttime
    
    for line in indata[mergeatline:]:
        currenttime = baseintime + int(line.time)
        
        outdata.append(MacroLine(currenttime, \
                                 line.presscode, line.holdcode, \
                                 line.xPos, line.yPos, \
                                 line.inyRez, line.inxRez))
    if outtype == 'memu':
        if not myMEmuMacroHandler:
            myMEmuMacroHandler = MEmuMacroHandler(outyRez = outyRez, outxRez = outxRez)
        else:
            myMEmuMacroHandler.setOutRez(outyRez, outxRez)
            
        for entry in outdata:
            outfile.write(myMEmuMacroHandler.generateLine(entry.time, \
                                                          entry.presscode, \
                                                          entry.holdcode, \
                                                          entry.xPos, \
                                                          entry.yPos))
            
            outfile.write('\n')
                
    elif outtype == 'nox':
        if not myNoxMacroHandler:
            myNoxMacroHandler = NoxMacroHandler(outyRez = outyRez, outxRez = outxRez, noxKeyMap = keymap, newnoxout = newnox)
        else:
            myNoxMacroHandler.setOutRez(outyRez, outxRez)
            
        for entry in outdata:
            outfile.write(myNoxMacroHandler.generateLine(entry.time, \
                                                        entry.presscode, \
                                                        entry.holdcode, \
                                                        entry.xPos, \
                                                        entry.yPos))
            
            outfile.write('\n')
                
    elif outtype == 'hiro':
        if not myHiroMacroHandler:
            myHiroMacroHandler = HiroMacroHandler(outyRez = outyRez, outxRez = outxRez, hiroKeyMap = keymap)
        else:
            myHiroMacroHandler.setOutRez(outyRez, outxRez)
            
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