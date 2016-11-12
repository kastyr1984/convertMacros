import collections
import re

#this script aims to take all the guesswork out of converting macro scripts
#between MEmu and NOX

#all credit goes to /u/MLieBennett and /u/jcarl987 for giving me the tools to
#succeed here, I never would have even started to figure half this stuff out
#on my own

#big shout out to /u/-Pwnology- for making the scripts that make this a
#worthwhile endeavor in the first place

MacroLine = collections.namedtuple('MacroLine', ['time', 'presscode', 'holdcode', 'xPos', 'yPos', 'inyRez', 'inxRez'])

#namedtuple is a bit of an odd choice for use here, especially since there are
#a couple of instances where we want to be able to alter data
#but the speed benefits can help when things get really big

def processMEmuLine(instring, outyRez = 720, outxRez = 1280, inyRez = 720, inxRez = 1280):
    if '--VINPUT--MULTI:1' in instring:
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
        if inyRez != outyRez:
            yPos = round(yPos * (float(outyRez) / float(inyRez)))
            
        if inxRez != outxRez:
            xPos = round(xPos * (float(outxRez) / float(inxRez)))   
    
        return MacroLine(time = time, presscode = presscode, holdcode = holdcode, xPos = xPos, yPos = yPos, inyRez = inyRez, inxRez = inxRez)
    else:
        return False
    
def splitOldNoxLine(instring, outyRez, outxRez):
    splitline = instring.split('|')
    
    #pull the raw values
    holdcode = splitline[0]
    yPos = splitline[1]
    xPos = splitline[2]
    time = splitline[6]
    inyRez = splitline[7]
    inxRez = splitline[8]
    
    #process time
    time = int(time) * 1000
    
    #process resolution
    inyRez = int(inyRez)
    inxRez = int(inxRez)
    
    #process pos values
    #xPos = inxRez - int(xPos)
    xPos = int(xPos)
    #convert y coordinates back
    yPos = inyRez - int(yPos)
    
    #account for differing resolution settings
    if inyRez != outyRez:
        yPos = round(yPos * (float(outyRez) / float(inyRez)))

    if inxRez != outxRez:
        xPos = round(xPos * (float(outxRez) / float(inxRez)))
        
    return MacroLine(time = time, presscode = '1', holdcode = holdcode, xPos = xPos, yPos = yPos, inyRez = inyRez, inxRez = inxRez)

def processMSBRL(instring, outyRez = 720, outxRez = 1280):
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
        
        return MacroLine(time = time, presscode ='1', holdcode = '1', xPos = -1, yPos = outyRez, inyRez = inyRez, inxRez = inxRez)
    else:
        return False

def splitNewNoxLine(instring, outyRez = 720, outxRez = 1280):
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
            yPos = round(yPos * (float(outyRez) / float(inyRez)))
        
        if inxRez != outxRez:
            xPos = round(xPos * (float(outxRez) / float(inxRez)))   
        
        return MacroLine(time = time, presscode = '1', holdcode = holdcode, xPos = xPos, yPos = yPos, inyRez = inyRez, inxRez = inxRez)
    elif 'MSBRL:' in instring:
        return processMSBRL(instring, outyRez = outyRez, outxRez = outxRez)
    else:
        return False
    
def processNoxLine(instring, outyRez = 720, outxRez = 1280):
    if 'ScRiPtSePaRaToR' in instring:
        return splitNewNoxLine(instring, outyRez = outyRez, outxRez = outxRez)
    else:
        return splitOldNoxLine(instring, outyRez = outyRez, outxRez = outxRez)

def generateMEmuLine(time, presscode, holdcode, xPos, yPos):
    #Since we effectively treat the MEmu conventions as native, little conversion is really neccessary
    return ''.join([str(time), '--VINPUT--MULTI:', presscode, ':', holdcode, ':', str(xPos), ':', str(yPos)])
    
def generateNoxLine(time, presscode, holdcode, xPos, yPos, outyRez = 720, outxRez = 1280, newnox = False):
    #Mash the values together, performing basic conversions where needed
    if not newnox:
        return('|'.join([holdcode, \
                         str(outyRez - int(yPos)), \
                         str(xPos), #str(outxRez - xPos), \
                         '0', \
                         '0', \
                         '0', \
                         str(round(float(time) / 1000.0)), \
                         str(outyRez), \
                         str(outxRez)]))
    else:
        return''.join(['0ScRiPtSePaRaToR', str(outxRez), '|', str(outyRez), \
                       '|MULTI:', presscode, ':', holdcode, ':', str(xPos), ':', \
                       str(yPos), 'ScRiPtSePaRaToR', str(round(float(time) / 1000.0))])
    
def processMEmuFile(infile, outyRez = 720, outxRez = 1280, inyRez = 720, inxRez = 1280):
    returndata = []
    
    for line in infile:
        #process this line
        linetuple = processMEmuLine(line, outyRez = outyRez, outxRez = outxRez, inyRez = inyRez, inxRez = inxRez)
        
        #if we don't handle this line currently, linetuple will be false
        #we don't bother writing the output
        if linetuple:
            xPos = linetuple.xPos
            yPos = linetuple.yPos

            #Seems to be for mouse release events, so we need to examine the
            #previous value and count the differences
            if linetuple.holdcode == '1':
                if len(returndata) > 0:
                    xPos = returndata[-1].xPos + linetuple.xPos
                    yPos = inyRez - (linetuple.yPos - returndata[-1].yPos)
                    
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
            
def processNoxFile(infile, outyRez = 720, outxRez = 1280):
    returndata = []

    for line in infile:
        linetuple = processNoxLine(line, outyRez = outyRez, outxRez = outxRez)
        
        if linetuple:
            returndata.append(linetuple)
                
    return returndata
            
def processFiles(infile, outfile, intype, outtype, outyRez=720, outxRez = 1280, inyRez = 720, inxRez = 1280, newnox = False):
    #just in case we get 'NOX' or 'MEmu' as intype arguments
    intype = intype.lower()
    outtype = outtype.lower()
    
    #output data container
    outdata = []
    
    #process the input file
    if intype == 'nox':
        outdata = processNoxFile(infile, outyRez, outxRez)
    elif intype == 'memu':
        outdata = processMEmuFile(infile, outyRez, outxRez, inyRez, inxRez)
    else:
        #TODO raise error here
        return False
        
    #write the output file
    if outdata:
        if outtype.lower() == 'nox':
            for entry in outdata:
                outfile.write(generateNoxLine(entry.time, \
                                              entry.presscode, \
                                              entry.holdcode, \
                                              entry.xPos, \
                                              entry.yPos, \
                                              outyRez = outyRez, \
                                              outxRez = outxRez, \
                                              newnox = newnox))
                
                outfile.write('\n')
                            
        elif outtype.lower() == 'memu':
            for entry in outdata:
                if entry.presscode in ('2', '3'):
                    #TODO handle button presses here
                    pass
                else:
                    outfile.write(generateMEmuLine(entry.time, \
                                                   entry.presscode, \
                                                   entry.holdcode, \
                                                   entry.xPos, \
                                                   entry.yPos))
                
                outfile.write('\n')
                    
        else:
            #TODO raise error here
            return False
                
if __name__ == '__main__':
    import argparse
    import sys
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='infile', nargs='?', type=argparse.FileType('r'), \
                        required=True)
    parser.add_argument('-o', dest='outfile', nargs='?', type=argparse.FileType('w'),
                         default=sys.stdout)
    
    parser.add_argument('--in-x', dest='inxRez', default=1280, type=int, \
                        help='input file x resolution, ignored for Nox files')
    parser.add_argument('--in-y', dest='inyRez', default=720, type=int, \
                        help='input file x resolution, ignored for Nox files')
    
    parser.add_argument('--out-x', dest='outxRez', default=1280, type=int, \
                        help='output file x resolution')
    parser.add_argument('--out-y', dest='outyRez', default=720, type=int, \
                        help='output file x resolution')
    
    parser.add_argument('--intype', dest='intype', required=True, \
                        help='input file type, nox or memu')
    parser.add_argument('--outtype', dest='outtype', required=True, \
                        help='output file type, nox or memu')
    
    #parser.add_argument('--flip-xy', dest='flipxy', action='store_true', default=False,\
    #                    help='flip output x and y values')
    parser.add_argument('--new-nox', dest='newnox', action='store_true', default=False,\
                            help='output nox files in ScRiPtSePaRaToR style')    
    
    args = parser.parse_args()
    
    if args.infile and args.outfile and args.intype and args.outtype:
        if args.intype.lower() == 'nox':
            #ignore input x and y if the input file is Nox, since values are interally
            #holdcoded anyway
            processFiles(args.infile, args.outfile, args.intype, args.outtype, \
                         args.outyRez, args.outxRez, \
                         newnox = args.newnox)
        elif args.intype.lower() == 'memu':
            processFiles(args.infile, args.outfile, args.intype, args.outtype, \
                         args.outyRez, args.outxRez, \
                         args.inyRez, args.inxRez, \
                         newnox = args.newnox)
    else:
        parser.print_help()
        