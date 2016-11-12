import collections

#namedtuple is a bit of an odd choice for use here, especially since there are
#a couple of instances where we want to be able to alter data
#but the speed benefits can help when things get really big
MacroLine = collections.namedtuple('MacroLine', ['time', 'presscode', 'holdcode', 'xPos', 'yPos', 'inyRez', 'inxRez'])

KeyMapPoint = collections.namedtuple('KeyMap', ['xPos', 'yPos'])
