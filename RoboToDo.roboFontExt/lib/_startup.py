import os

from AppKit import *
from vanilla import *

from mojo.UI import CurrentFontWindow
from mojo.events import addObserver

from lib.UI.toolbarGlyphTools import ToolbarGlyphTools

from todo.models import ToDo, Block, Resource
from todo.views import ToDoWindow

from defconAppKit.windows.baseWindow import BaseWindowController
# TODO: Windows should not open more than one at a time,
#       but OpenWindow doesn't seem to do this... :(
# from mojo.roboFont import OpenWindow

WINDOWS = {}

class ToolBarButtons(object):
    
    base_path = os.path.dirname(__file__)
    
    def __init__(self):
        addObserver(self, "addFontToolbar", "fontWindowWillShowToolbarItems")
        addObserver(self, "addGlyphToolbar", "glyphWindowWillShowToolbarItems")
       
    def addGlyphToolbar(self, info):
        toolbarItems = info['toolbarItems']
        self.addToolbarItem(toolbarItems, 'To-Do', 'roboToDoGlyph', 
                        'toolbarGlyphToDo.pdf', self.openGlyphToDos, index=-2)

    def addFontToolbar(self, info):
        toolbarItems = info['toolbarItems']
        self.addToolbarItem(toolbarItems, 'To-Do', 'roboToDoFont', 
                        'toolbarFontToDo.pdf', self.openFontToDos, index=-2)
    
    def addToolbarItem(self, toolbarItems, label, identifier, filename, callback, index=-1):
        imagePath = os.path.join(self.base_path, 'resources', filename)
        image = NSImage.alloc().initByReferencingFile_(imagePath)
        
        if identifier is 'roboToDoGlyph':
            view = ToolbarGlyphTools((30, 25), 
                                   [dict(image=image, toolTip="To-Do")], 
                                   trackingMode="one")
        
            newItem = dict(itemIdentifier=identifier,
                label = label,
                callback = callback,
                view = view
            )
        else:
            newItem = dict(itemIdentifier=identifier,
                label=label,
                imageObject=image,
                callback=callback
            )
            
        toolbarItems.insert(index, newItem)

    def openGlyphToDos(self, sender):
        window = ToDoWindow(CurrentGlyph())
        window.open()

    def openFontToDos(self, sender):
        window = ToDoWindow(CurrentFont())
        window.open()

ToolBarButtons()
