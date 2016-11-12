import os.path

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