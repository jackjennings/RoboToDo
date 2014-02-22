import os

from AppKit import *
from vanilla import *

from mojo.UI import CurrentFontWindow
from mojo.events import addObserver

from lib.UI.toolbarGlyphTools import ToolbarGlyphTools

from todo.models import ToDo, Block, Resource
from todo.views import ToDoWindow

from defconAppKit.windows.baseWindow import BaseWindowController

class ToolBarButtons(object):
    
    base_path = os.path.dirname(__file__)
    
    def __init__(self):
        addObserver(self, "addFontToolbar", "fontDidOpen")
        addObserver(self, "addFontToolbar", "newFontDidOpen")
        addObserver(self, "addGlyphToolbar", "glyphWindowDidOpen")
       
    def addGlyphToolbar(self, info):
        window = info['window']
        if window is None:
            return
        self.addToolbar(window, 'To-Do', 'roboToDoGlyph', 
                        'toolbarGlyphToDo.pdf', self.openGlyphToDos, index=-2)

    def addFontToolbar(self, info):
        window = CurrentFontWindow()
        if window is None:
            return
        self.addToolbar(window, 'To-Do', 'roboToDoFont', 
                        'toolbarFontToDo.pdf', self.openFontToDos, index=-2)
    
    def addToolbar(self, window, label, identifier, filename, callback, index=-1):
        w = window.window()
        imagePath = os.path.join(self.base_path, 'resources', filename)
        image = NSImage.alloc().initByReferencingFile_(imagePath)
        
        if identifier is 'roboToDoGlyph':
            view = ToolbarGlyphTools((30, 25), 
                                   [dict(image=image, toolTip="To-Do")], 
                                   trackingMode="one")
        
            item = dict(itemIdentifier=identifier,
                label = label,
                callback = callback,
                view = view
            )
        else:
            item = dict(itemIdentifier=identifier,
                label=label,
                imageObject=image,
                callback=callback
            )
            
        w._createToolbarItem(item)
        w._toolbarDefaultItemIdentifiers.remove(item["itemIdentifier"])
        w._toolbarDefaultItemIdentifiers.insert(index, item["itemIdentifier"])
        
        numberOfItems = w.getNSWindow().toolbar()._numberOfItems()
        index = (numberOfItems + index) % numberOfItems
        
        w.getNSWindow().toolbar().insertItemWithItemIdentifier_atIndex_(item["itemIdentifier"], index)

    def openGlyphToDos(self, sender):
        window = ToDoWindow(CurrentGlyph())
        window.open()

    def openFontToDos(self, sender):
        window = ToDoWindow(CurrentFont())
        window.open()

ToolBarButtons()
