from macrolib.DataTypes import MacroLine
from macrolib.NoxKeyMap import *

class NoxMacroHandler:
    rotated = False
    outyRez = None
    outxRez = None
    keyMap = None
    newnoxout = False
    handlertype = 'nox'
    
    def __init__(self, outyRez = 720.0, outxRez = 1280.0, noxKeyMap = None, newnoxout = False):
        self.setOutRez(outyRez, outxRez)
        
        if noxKeyMap:
            self.keyMap = NoxKeyMap(noxKeyMap)
            
        if newnoxout:
            self.newnoxout = newnoxout
            
    def checkRotated(self, inxRez = None, inyRez = None):
        if inxRez == None:
            inxRez = self.inxRez
        if inyRez == None:
            inyRez = self.inyRez
        
        return ((inxRez > inyRez) != (self.outxRez > self.outyRez))
            
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
        #xPos = int(xPos) - round(self.outxRez / 80.0)
        xPos = int(xPos)
        #convert y coordinates back
        yPos = inyRez - int(yPos)
        
        #account for differing resolution settings
        if inyRez != self.outyRez:
            yPos = round(yPos * (self.outyRez / float(inyRez)))
    
        if inxRez != self.outxRez:
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
            if self.checkRotated(inxRez, inyRez):
                oldxPos = xPos
                xPos = yPos
                yPos = oldxPos
                
                if self.inxRez != self.outyRez:
                    xPos = round(yPos * (self.outyRez / inxRez))
                    
                if self.inyRez != self.outxRez:
                    yPos = round(xPos * (self.outxRez / inyRez))                
            else:
                if inyRez != self.outyRez:
                    yPos = round(yPos * (self.outyRez / float(inyRez)))
                
                if inxRez != self.outxRez:
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
    
    def generateLine(self, time, presscode, holdcode, xPos, yPos, flipX = False, flipY = False):
        #Mash the values together, performing basic conversions where needed
        if flipX:
            xPos = int(self.outxRez - xPos)
        if flipY:
            yPos = int(self.outyRez - yPos)
        
        if not self.newnoxout:
            return('|'.join([holdcode, \
                             str(int(self.outyRez - int(yPos))), \
                             str(int(xPos)), \
                             '0', \
                             '0', \
                             '0', \
                             str(int(round(float(time) / 1000.0))), \
                             str(int(self.outyRez)), \
                             str(int(self.outxRez))]))
        else:
            return''.join(['0ScRiPtSePaRaToR', str(int(self.outxRez)), '|', str(int(self.outyRez)), \
                           '|MULTI:', presscode, ':', holdcode, ':', str(int(xPos)), ':', \
                           str(int(yPos)), 'ScRiPtSePaRaToR', str(int(round(float(time) / 1000.0)))])
        