import os.path
import xml.etree.ElementTree

from DataTypes import KeyMapPoint

filepath = os.path.dirname(os.path.realpath(__file__))

class NoxKeyMap:
    KeyMap = None
    
    def __init__(self, infpath = os.path.join(filepath, 'com.vphone.launcher.import_1280x720.xml')):
        self.KeyMap = self.processKeyMapFile(infpath)
        
    def setKeyMap(self, infpath):
        self.KeyMap = self.processKeyMapFile(infpath)
    
    def processKeyMapFile(self, infpath ):
        keyMapDict = {}
        
        tree = xml.etree.ElementTree.parse(infpath)
        root = tree.getroot()
        
        keys = [int(key.attrib['value']) for key in root.findall("./Scene/Item/Key")]
        points = [point.text.split(',') for point in root.findall("./Scene/Item/Key/Point")]
        
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