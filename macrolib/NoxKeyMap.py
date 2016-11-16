import os.path
import xml.etree.ElementTree

from macrolib.DataTypes import KeyMapPoint

filepath = os.path.dirname(os.path.realpath(__file__))

class NoxKeyMap:
    KeyMap = None
    
    def __init__(self, infpath = os.path.join(filepath, 'com.vphone.launcher.import_1280x720.xml'), outxRez = 720.0, outyRez = 1280.0):
        self.KeyMap = self.processKeyMapFile(infpath)
        
    def setKeyMap(self, infpath):
        self.KeyMap = self.processKeyMapFile(infpath)
    
    def processKeyMapFile(self, infpath ):
        keyMapDict = {}
        
        tree = xml.etree.ElementTree.parse(infpath)
        root = tree.getroot()
        
        inyRez = [int(key.attrib['height']) for key in root.findall("./Scene")][0]
        inxRez = [int(key.attrib['width']) for key in root.findall("./Scene")][0]
        
        keys = [int(key.attrib['value']) for key in root.findall("./Scene/Item/Key")]
        points = [point.text.split(',') for point in root.findall("./Scene/Item/Key/Point")]
        
        if inxRez != outxRez or inyRez != outyRez:
            for ptIdx in range(0, len(points)):
                if inxRez != outxRez:
                    points[ptIdx][0] = str(round((float(points[ptIdx][0]) * outxRez) / inxRez))
                if inyRez != outyRez:
                    points[ptIdx][1] = str(round((float(points[ptIdx][1]) * outyRez) / inyRez))
        
        KeyMap = dict(zip(keys, [KeyMapPoint(pt[0], pt[1]) for pt in points]))

        return(KeyMap)
        
    def getKeyPoint(self, keyint):
        if type(keyint) is not int:
            keyint = int(asciikey)
        
        if self.KeyMap and keyint in self.KeyMap.keys():
            return self.KeyMap[keyint]
        else:
            return None
        
    def getKeyPointFromChar(self, inchar):
        keyint = ord(inchar)
        
        return self.getKeyPoint(keyint)
    
if __name__ == "__main__":
    keymapper = NoxKeyMap()
    print(keymapper.getKeyPointFromChar('D'))