import re

linere = re.compile("(touch(?:Down [0-4] [0-9]{1,} [0-9]{1,}|Up [0-9]{1,})\nsleep [0-9]{1,})")

from macrolib.DataTypes import MacroLine
#from DataTypes import MacroLine

class HiroMacroHandler:
    compress = False
    outyRez = None
    outxRez = None
    inyRez = None
    inxRez = None
    keyMap = None
    currenttime = None
    handlertype = 'hiro'
    
    def __init__(self, outyRez = 720.0, outxRez = 1280.0, inyRez = 720.0, inxRez = 1280.0, hiroKeyMap = None):
        self.setOutRez(outyRez, outxRez)
        self.setInRez(inyRez, inxRez)
        self.resetTime()
        
        if hiroKeyMap:
            self.keyMap = None
            
    def setOutRez(self, outyRez, outxRez):
        if not isinstance(outyRez, float):
            outyRez = float(outyRez)
            
        if not isinstance(outxRez, float):
            outxRez = float(outxRez)
            
        self.outyRez = outyRez
        self.outxRez = outxRez
        
    def setInRez(self, inyRez, inxRez):
        if not isinstance(inyRez, float):
            outyRez = float(inyRez)
            
        if not isinstance(inxRez, float):
            inxRez = float(inxRez)
            
        self.inyRez = inyRez
        self.inxRez = inxRez
        
    def resetTime(self, time = 0):
        self.currenttime = time
        
    def processLine(self, instring):
        touchsplit = instring.split(' ')
        
        if touchsplit[0] == 'sleep':
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
                if self.inyRez != self.outyRez:
                    yPos = round(yPos * (self.outyRez / self.inyRez))
                    
                if self.inxRez != self.outxRez:
                    xPos = round(xPos * (self.outxRez / self.inxRez))
                    
            elif touchsplit[0] == 'touchUp':
                presscode = str(int(touchsplit[1]) + 1)
                holdcode = 1
            elif touchsplit[0] == 'touchPress':
                presscode = str(int(touchsplit[1]) + 1)
                holdcode = 0
                xPos = int(touchsplit[2])
                yPos = int(touchsplit[3])
                
                #account for differing resolution settings
                if self.inyRez != self.outyRez:
                    yPos = round(yPos * (self.outyRez / self.inyRez))
                    
                if self.inxRez != self.outxRez:
                    xPos = round(xPos * (self.outxRez / self.inxRez))
                    
                return (MacroLine(time = time, presscode = presscode, holdcode = holdcode, xPos = xPos, yPos = yPos, inyRez = self.inyRez, inxRez = self.inxRez), \
                        MacroLine(time = time + 100000, presscode = presscode, holdcode = 0, xPos = 0, yPos = 0, inyRez = self.inyRez, inxRez = self.inxRez))
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
    
        #for returnval in returndata:
        #    print(self.generateLine(returnval.time, returnval.presscode, returnval.holdcode, returnval.xPos, returnval.yPos))
                    
        return returndata
    
    def generateLine(self, time, presscode, holdcode, xPos, yPos):
        #performing basic conversions where needed
        convertedtime = int(round(float(time) / 1000.0))
        sleeptime = convertedtime - self.currenttime
        
        self.currenttime = convertedtime
        
        holdstr = ''
    
        if holdcode == '0':
            holdstr = 'touchDown'
        elif holdcode == '1':
            holdstr = 'touchUp'
        elif holdcode == '2':
            holdstr = 'touchMove'
        elif holdcode == '132':
            holdstr = 'touchPress'
            
        return ''.join(['sleep ', \
                         str(int(sleeptime)), \
                         '\n', \
                         holdstr, ' ', \
                         str(int(presscode) - 1),  ' ', \
                         str(xPos), ' ', \
                         str(int(yPos))])
    
    def generateCompressedLines(self, linedata):
        matchedlines = {}
        returndata = []
        
        for line in linedata:
            if line.holdcode == '0':
                if line.presscode not in matchedlines:
                    matchedlines[line.presscode] = line
                else:
                    #todo: raise error here
                    pass
            elif line.holdcode == '1':
                if line.presscode in matchedlines:
                    baseline = matchedlines[line.presscode]
                    del matchedlines[line.presscode]
                    
                    returndata.append(MacroLine(time = line.time, \
                                                presscode = baseline.presscode, \
                                                holdcode = '132', \
                                                xPos = baseline.xPos, \
                                                yPos = baseline.yPos, \
                                                inyRez = baseline.inyRez, \
                                                inxRez = baseline.inxRez))
                    
                else:
                    #todo: raise error here
                    pass
            else:
                returndata.append(line)
                    
        return returndata
    
if __name__ == "__main__":
    mytest = HiroMacroHandler()
    with open('/home/mikey/Downloads/hiro_macro_on_memu.txt') as infile:
        mytest.processFile(infile)
    