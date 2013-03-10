import os

from AppKit import *
from vanilla import *

from mojo.UI import CurrentFontWindow

from defconAppKit.windows.baseWindow import BaseWindowController

from todo.helpers import GlyphToDoList, FontToDoList
from todo.models import *

class ToDoWindow(BaseWindowController):
    
    base_path = os.path.dirname(__file__)

    def __init__(self, resource):
        self.bottomBarHeight = 22
        self.resource = Resource(resource)
        self.identifier = 'window-%s' % self.resource.getGlyph()
        self.glyphName = self.resource.getGlyph()
                
        if self.resource.type is 'font':
            self.w = FloatingWindow((550,400), 
                                    "All To-Do Items", 
                                    autosaveName="robotodoList", 
                                    minSize=(550,300))
            self.w.todosList = FontToDoList((0,0,0,-self.bottomBarHeight), 
                                            resource,
                                            doubleClickCallback=self.doubleClickCallback)
        else:
            self.w = FloatingWindow((550,400), 
                                    "To-Do Items for /%s" % self.glyphName, 
                                    autosaveName="robotodoListGlyph", 
                                    minSize=(550,300))
            self.w.todosList = GlyphToDoList((0,0,0,-self.bottomBarHeight), 
                                             resource, 
                                             doubleClickCallback=self.doubleClickCallback)
        
        self.w._window.setContentBorderThickness_forEdge_(self.bottomBarHeight, NSMinYEdge)
        
        self.w.addToDo = ImageButton((0,-self.bottomBarHeight,self.bottomBarHeight + 4,self.bottomBarHeight), 
                                     imagePath = os.path.join(self.base_path, '..', 'resources', 'bottomAddToDo.pdf'),
                                     callback = self.newToDo, bordered = False)
        
        self.w.clearCompleted = Button((-110, -self.bottomBarHeight + 4, 100, 14), 
                                       "Clear Completed", sizeStyle = 'mini',
                                       callback=self.clearCompleteToDos)
        
    def newToDo(self, sender):
        self.s = Sheet((400, 200), self.w)
        
        self.s.note = TextEditor((0, 0, 0, 150), "")
        self.s.note._textView.setTextContainerInset_(NSMakeSize(15, 15))
        self.s.note._nsObject.setBorderType_(0)
        
        self.s.rule = HorizontalLine((0, 150, 0, 1))
        
        self.s.cancelButton = Button((-190,-35, 80,20), "Cancel",
                                     callback=self.cancelToDo)
        self.s.createButton = Button((-95,-35, 80,20), "Create",
                                     callback=self.createToDo)
        
        if self.resource.type is 'font':
            glyphs = ['*']
            for glyph in self.resource.source:
                glyphs.append(glyph.name)
            glyphs.sort()
            
            self.s.popup = PopUpButton((15, -35, 80, 20), glyphs)
        
        self.s.setDefaultButton(self.s.createButton)
        self.s.open()
        
    def createToDo(self, sender):
        note = self.s.note.get()

        if self.resource.type is 'font':
            glyphs = self.s.popup.getItems()
            selected_glyph = glyphs[self.s.popup.get()]
            if selected_glyph in self.resource.source:
                source = self.resource.source[selected_glyph]
            else:
                source = self.resource.source
        else:
            source = self.resource.source
        
        todo = ToDo(source, note)
        todo.save()
        self.w.todosList.append(todo.toCell())
        self.w.todosList._tableView.reloadData()
        
        self.s.close()
    
    def doubleClickCallback(self, sender):
        todo_cells = self.w.todosList.get()
        todo = todo_cells[sender.getSelection()[0]]
        
        self.s = Sheet((400, 200), self.w)
        
        self.s.note = TextEditor((0, 0, 0, 150), todo['note'])
        self.s.note._textView.setTextContainerInset_(NSMakeSize(15, 15))
        self.s.note._nsObject.setBorderType_(0)
        
        self.s.rule = HorizontalLine((0, 150, 0, 1))
        
        self.s.cancelButton = Button((-190,-35, 80,20), "Cancel",
                                     callback=self.cancelToDo)
        self.s.updateButton = Button((-95,-35, 80,20), "Update",
                                     callback=self.updateToDo)
        
        self.s.popup = TextBox((15, -35, 80, 20), todo['glyph'])
        
        self.s.setDefaultButton(self.s.updateButton)
        self.s.open()

    def updateToDo(self, sender):
        list = self.w.todosList
        todo_cells = list.get()
        todo = todo_cells[list.getSelection()[0]]
        note = self.s.note.get()
        
        todo['note'] = note
        todo['todo'].note = note
        todo['todo'].save()
        
        self.s.close()

    def cancelToDo(self, sender):
        self.s.close()
    
    def clearCompleteToDos(self, sender):
        for todo_cell in self.w.todosList.get():
            if todo_cell['todo'].completed:
                self.w.todosList.remove(todo_cell)
                todo_cell['todo'].destroy()
        
    def open(self):
        self.w.open()
        self.w.makeKey()
        
    def close(self):
        self.w.close()
        
if __name__ == "__main__":
    ToDoWindow(CurrentFont()).open()