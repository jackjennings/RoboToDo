from todo.views import ToDoWindow

glyph = CurrentGlyph()
if glyph is not None:
    ToDoWindow(glyph).open()
