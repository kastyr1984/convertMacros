from macrolib.DataTypes import MacroLine

class MEmuMacroHandler:
    rotated = False
    outyRez = None
    outxRez = None
    inyRez = None
    inxRez = None
    handlertype = 'memu'
    
    def __init__(self, outyRez = 720.0, outxRez = 1280.0, inyRez = 720.0, inxRez = 1280.0):
        self.setOutRez(outyRez, outxRez)
        
        self.setInRez(inyRez, inxRez)
        
    def checkRotated(self):
        return ((self.inxRez > self.inyRez) != (self.outxRez > self.outyRez))
            
    def setOutRez(self, outyRez, outxRez):
        if not isinstance(outyRez, float):
            outyRez = float(outyRez)
            
        if not isinstance(outxRez, float):
            outxRez = float(outxRez)
            
        self.outyRez = outyRez
        self.outxRez = outxRez
        
        if self.inxRez and self.inyRez:
            self.rotated = self.checkRotated()
        
    def setInRez(self, inyRez, inxRez):
        if not isinstance(inyRez, float):
            inyRez = float(inyRez)
            
        if not isinstance(inxRez, float):
            inxRez = float(inxRez)
            
        self.inyRez = inyRez
        self.inxRez = inxRez
        
        if self.outxRez and self.outyRez:
            self.rotated = self.checkRotated()
        
    def processLine(self, instring):
        if '--VINPUT--MULTI:' in instring:
            splitline = instring.split(':')
            
            #pull the values
            time = instring[:instring.index('--')]
            presscode = splitline[1]
            holdcode = splitline[2]
            xPos = int(splitline[3])
            yPos = int(splitline[4])
            
            #sometimes there are more values and I'm yet unsure what they are for
            if len(splitline) == 7:
                xPos2 = int(splitline[5])
                yPos2 = int(splitline[6])
            
            #account for differing resolution settings
            if self.rotated:
                oldxPos = xPos
                xPos = yPos
                yPos = oldxPos
                
                if self.inxRez != self.outyRez:
                    xPos = round(yPos * (self.outyRez / self.inxRez))
                    
                if self.inyRez != self.outxRez:
                    yPos = round(xPos * (self.outxRez / self.inyRez))
            else:
                if self.inyRez != self.outyRez:
                    yPos = round(yPos * (self.outyRez / self.inyRez))
                    
                if self.inxRez != self.outxRez:
                    xPos = round(xPos * (self.outxRez / self.inxRez))
        
            return MacroLine(time = time, presscode = presscode, holdcode = holdcode, xPos = xPos, yPos = yPos, inyRez = self.inyRez, inxRez = self.inxRez)
        else:
            return False
        
    def processFile(self, infile):
        returndata = []
        
        for line in infile:
            #process this line
            linetuple = self.processLine(line)
            
            #if we don't handle this line currently, linetuple will be false
            #we don't bother writing the output
            if linetuple:
                xPos = linetuple.xPos
                yPos = linetuple.yPos
    
                #Seems to be for mouse release events, so we need to examine the
                #previous value and count the differences
                if linetuple.holdcode == '1':
                    if len(returndata) > 0:
                        #xPos = returndata[-1].xPos + linetuple.xPos
                        #yPos = self.inyRez - (linetuple.yPos - returndata[-1].yPos)
                        
                        xPos = returndata[-1].xPos
                        yPos = returndata[-1].yPos
                        
                if linetuple.xPos != xPos or linetuple.yPos != yPos:
                    returndata.append(MacroLine(time = linetuple.time, \
                                                presscode = linetuple.presscode, \
                                                holdcode = linetuple.holdcode, \
                                                xPos = xPos, yPos = yPos, \
                                                inyRez = linetuple.inyRez, \
                                                inxRez = linetuple.inxRez))
                else:
                    returndata.append(linetuple)
                        
        return returndata
    
    def generateLine(self, time, presscode, holdcode, xPos, yPos, flipX = False, flipY = False, *args):
        #Since we effectively treat the MEmu conventions as native, little conversion is really neccessary
        if flipX:
            xPos = int(self.outxRez - xPos)
        if flipY:
            yPos = int(self.outyRez - yPos)
            
        return ''.join([str(int(time)), '--VINPUT--MULTI:', presscode, ':', holdcode, ':', str(int(xPos)), ':', str(int(yPos))])