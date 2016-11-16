import os.path

#from DataTypes import MacroLine

#Misc helper functions for other programs

#Basic filetype detection heuristics
def detectFileType(file):
    if os.path.splitext(file.name)[-1].lower() == '.mir':
        return 'memu'
    else:
        origin = file.tell()
        
        inline = file.readline()
        
        if 'ScRiPtSePaRaToR' in inline:
            returnval = 'nox'
        elif '--VINPUT--' in inline:
            returnval = 'memu'
        elif '|' in inline:
            returnval = 'nox'
            
        file.seek(origin)
        
        return returnval

#detect if a variable is a sequence and not a string

def is_sequence(arg):
        return (not hasattr(arg, "strip") and
                hasattr(arg, "__getitem__") or
                hasattr(arg, "__iter__"))   