import re

splitre = re.compile('[,\(\);]')

from macrolib.DataTypes import MacroLine
#from DataTypes import MacroLine

class AutoTouchMacroHandler:
    compress = False
    rotated = False
    outyRez = None
    outxRez = None
    inyRez = None
    inxRez = None
    keyMap = None
    currenttime = None
    handlertype = 'autotouch'
    
    def __init__(self, outyRez = 720.0, outxRez = 1280.0, inyRez = 720.0, inxRez = 1280.0, autoTouchKeyMap = None):
        self.setOutRez(outyRez, outxRez)
        self.setInRez(inyRez, inxRez)
        self.resetTime()
        
        if autoTouchKeyMap:
            self.keyMap = None
            
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
            
        print(self.rotated)
        print([self.inxRez, self.outxRez, self.inyRez, self.outyRez])
        
    def setInRez(self, inyRez, inxRez):
        if not isinstance(inyRez, float):
            inyRez = float(inyRez)
            
        if not isinstance(inxRez, float):
            inxRez = float(inxRez)
            
        self.inyRez = inyRez
        self.inxRez = inxRez
        
        if self.outxRez and self.outyRez:
            self.rotated = self.checkRotated()
            
        print(self.rotated)
        print([self.inxRez, self.outxRez, self.inyRez, self.outyRez])
        
    def resetTime(self, time = 0):
        self.currenttime = time
        
    def processLine(self, instring):
        touchsplit = splitre.split(instring)
        
        if touchsplit[0] == 'usleep':
            sleepval = int(touchsplit[1])
                    
            self.currenttime += sleepval
            
            return None
        
        else:
            time = self.currenttime * 1000
            holdcode = 0
            xPos = 0
            yPos = 0
            
            if touchsplit[0] == 'touchDown':
                presscode = str(int(touchsplit[1]) + 1)
                holdcode = 0
                xPos = int(touchsplit[2])
                yPos = int(touchsplit[3])
                
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
                    
            elif touchsplit[0] == 'touchMove':
                presscode = str(int(touchsplit[1]) + 1)
                holdcode = 2
                xPos = int(touchsplit[2])
                yPos = int(touchsplit[3])
                
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
                    
            elif touchsplit[0] == 'touchUp':
                presscode = str(int(touchsplit[1]) + 1)
                holdcode = 1
            else:
                return None
            
            return MacroLine(time = time, presscode = presscode, holdcode = holdcode, xPos = xPos, yPos = yPos, inyRez = self.inyRez, inxRez = self.inxRez)
    
    def processFile(self, infile):
        returndata = []
        
        for line in infile:
            returnval = self.processLine(line)
            
            if returnval:
                if type(returnval) == tuple:
                    for entry in returnval:
                        returndata.append(entry)
                else:
                    returndata.append(returnval)
                
        self.resetTime(0)
                    
        return returndata
    
    def generateLine(self, time, presscode, holdcode, xPos, yPos, flipX = False, flipY = False):
        #performing basic conversions where needed
        convertedtime = int(round(float(time)))
        sleeptime = convertedtime - self.currenttime
        
        self.currenttime = convertedtime
        
        holdstr = ''
    
        if holdcode == '0':
            holdstr = 'touchDown'
        elif holdcode == '1':
            holdstr = 'touchUp'
        elif holdcode == '2':
            holdstr = 'touchMove'
            
        if flipX:
            xPos = int(self.outxRez - xPos)
        if flipY:
            yPos = int(self.outyRez - yPos)
            
        return ''.join(['usleep(', \
                         str(int(sleeptime)), \
                         ');\n', \
                         holdstr, '(', \
                         str(int(presscode) - 1),  ', ', \
                         str(xPos), ', ', \
                         str(int(yPos)), ');'])
    
if __name__ == "__main__":
    mytest = AutoTouchMacroHandler()
    with open('/home/mikey/Downloads/hiro_macro_on_memu.txt') as infile:
        mytest.processFile(infile)
    