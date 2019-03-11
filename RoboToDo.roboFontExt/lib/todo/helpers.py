from AppKit import *
from vanilla import *

from mojo.UI import CurrentFontWindow

from todo.models import *

def doubleClickCallback(sender):
    pass
    
def editCallback(sender):
    todos = sender.get()
    
    # TODO: Make this not iterate over all todos
    for todo_cell in todos:
        todo_cell['todo'].completed = todo_cell['completed']
        todo_cell['todo'].note = todo_cell['note']
        todo_cell['todo'].save()

def ToDoList(posSize, todos, todoColumns=[], doubleClickCallback=doubleClickCallback):
    
    todo_cells = []
    for todo in todos:
        todo_cells.append(todo.toCell())

    list = List(posSize, todo_cells, columnDescriptions=todoColumns,
                drawFocusRing=False, editCallback=editCallback, 
                doubleClickCallback=doubleClickCallback,
                allowsMultipleSelection=False)
    list._tableView.setUsesAlternatingRowBackgroundColors_(False)
    list._tableView.setAllowsColumnReordering_(False)
    list._tableView.setIntercellSpacing_((2.0, 10.0))
    #list._tableView.setAllowsColumnSelection_(False)
    #list._tableView.setSelectionHighlightStyle_(NSTableViewSelectionHighlightStyleNone)
    list._nsObject.setBorderType_(0)

    return list
        
def FontToDoList(posSize, font, doubleClickCallback=doubleClickCallback):
    
    todos = []
    columns = [
               {"title": "", "key": "completed", "width": 20, "editable": True, "cell": CheckBoxListCell()}, 
               {"title": "Glyph", "key": "glyph", "width": 60}, 
               {"title": "Note", "key": "note"}
              ]
    
    if font.info.note:
        for line in Block.parse(font.info.note):
            todos.append(ToDo(font, line))
    for g in font:
        if g.note:
            for line in Block.parse(g.note):
                todos.append(ToDo(g, line))
        
    return ToDoList(posSize, todos, todoColumns=columns, doubleClickCallback=doubleClickCallback)
    
def GlyphToDoList(posSize, glyph, doubleClickCallback=doubleClickCallback):
    
    todos = []
    columns = [
               {"title": "", "key": "completed", "width": 20, "editable": True, "cell": CheckBoxListCell()},
               {"title": "Note", "key": "note", "cell": TextFieldCell()}
              ]
    
    if glyph.note:
        for line in Block.parse(glyph.note):
            todos.append(ToDo(glyph, line))
            
    return ToDoList(posSize, todos, todoColumns=columns, doubleClickCallback=doubleClickCallback)

    
def TextFieldCell():
    cell = NSTextFieldCell.alloc().init()
    cell.setWraps_(True)
    return cell