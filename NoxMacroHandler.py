from DataTypes import *
from NoxKeyMap import *

class NoxMacroHandler:
    outyRez = None
    outxRez = None
    keyMap = None
    newnoxout = False
    handlertype = 'nox'
    
    def __init__(self, outyRez, outxRez, noxKeyMap = None, newnoxout = False):
        self.setOutRez(outyRez, outxRez)
        
        if noxKeyMap:
            self.keyMap = NoxKeyMap(noxKeyMap)
            
        if newnoxout:
            self.newnoxout = newnoxout
            
    def setOutRez(self, outyRez, outxRez):
        if not isinstance(outyRez, float):
            outyRez = float(outyRez)
            
        if not isinstance(outxRez, float):
            outxRez = float(outxRez)
            
        self.outyRez = outyRez
        self.outxRez = outxRez
    
    def splitOldNoxLine(self, instring):
        splitline = instring.split('|')
        
        #pull the raw values
        holdcode = splitline[0]
        yPos = splitline[1]
        xPos = splitline[2]
        keyPress = splitline[3]
        time = splitline[6]
        inyRez = splitline[7]
        inxRez = splitline[8]
        
        #process time
        time = int(time) * 1000
        
        #process resolution
        inyRez = int(inyRez)
        inxRez = int(inxRez)
        
        if holdcode in ('3', '4') and keyPress and noxKeyMap:
            keypoint = noxKeyMap.getKeyPoint(keyPress)
            
            if keypoint:
                holdcode = str(int(holdcode - 2))
                xPos, yPos = keypoint
                
        #process pos values
        xPos = int(xPos)
        #convert y coordinates back
        yPos = inyRez - int(yPos)
        
        #account for differing resolution settings
        if inyRez != self.outyRez:
            yPos = round(yPos * (self.outyRez / float(inyRez)))
    
        if inxRez != outxRez:
            xPos = round(xPos * (self.outxRez / float(inxRez)))
            
        return MacroLine(time = time, presscode = '1', holdcode = holdcode, xPos = xPos, yPos = yPos, inyRez = inyRez, inxRez = inxRez)
    
    def processMSBRL(self, instring):
        if 'MSBRL' in instring:
            #split the strings and pull the raw values
            sepsplit = instring.split('ScRiPtSePaRaToR')
            
            time = sepsplit[2]
            
            pipesplit = sepsplit[1].split('|')
            inxRez = pipesplit[0]
            inyRez = pipesplit[1]
            
            #process time
            time = int(time) * 1000
            
            #process resolution
            inyRez = int(inyRez)
            inxRez = int(inxRez)    
            
            return MacroLine(time = time, presscode ='1', holdcode = '1', xPos = -1, yPos = self.outyRez, inyRez = inyRez, inxRez = inxRez)
        else:
            return False
    
    def splitNewNoxLine(self, instring):
        if 'MULTI:1:' in instring:
            #split the strings and pull the raw values
            sepsplit = instring.split('ScRiPtSePaRaToR')
            
            time = sepsplit[2]
            
            pipesplit = sepsplit[1].split('|')
            inxRez = pipesplit[0]
            inyRez = pipesplit[1]
            
            colonsplit = pipesplit[2].split(':')
            presscode = colonsplit[1]
            holdcode = colonsplit[2]
            xPos = colonsplit[3]
            yPos = colonsplit[4]
            
            #process time
            time = int(time) * 1000
            
            #process resolution
            inyRez = int(inyRez)
            inxRez = int(inxRez)
            
            #process pos values
            xPos = int(xPos)
            #convert y coordinates back
            yPos = int(yPos)
            
            #account for differing resolution settings
            if inyRez != outyRez:
                yPos = round(yPos * (self.outyRez / float(inyRez)))
            
            if inxRez != outxRez:
                xPos = round(xPos * (self.outxRez / float(inxRez)))   
            
            return MacroLine(time = time, presscode = '1', holdcode = holdcode, xPos = xPos, yPos = yPos, inyRez = inyRez, inxRez = inxRez)
        elif 'MSBRL:' in instring:
            return self.processMSBRL(instring)
        else:
            return False
        
    def processLine(self, instring):
        if 'ScRiPtSePaRaToR' in instring:
            return self.splitNewNoxLine(instring)
        else:
            return self.splitOldNoxLine(instring)     
    
    def processFile(self, infile):
        returndata = []
    
        for line in infile:
            linetuple = self.processLine(line)
            
            if linetuple:
                returndata.append(linetuple)
                    
        return returndata
    
    def generateLine(self, time, presscode, holdcode, xPos, yPos):
        #Mash the values together, performing basic conversions where needed
        if not self.newnoxout:
            return('|'.join([holdcode, \
                             str(self.outyRez - int(yPos)), \
                             str(xPos), #str(outxRez - xPos), \
                             '0', \
                             '0', \
                             '0', \
                             str(round(float(time) / 1000.0)), \
                             str(self.outyRez), \
                             str(self.outxRez)]))
        else:
            return''.join(['0ScRiPtSePaRaToR', str(self.outxRez), '|', str(self.outyRez), \
                           '|MULTI:', presscode, ':', holdcode, ':', str(xPos), ':', \
                           str(yPos), 'ScRiPtSePaRaToR', str(round(float(time) / 1000.0))])       