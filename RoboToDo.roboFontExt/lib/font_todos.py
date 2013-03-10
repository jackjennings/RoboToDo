from todo.views import ToDoWindow

font = CurrentFont()
if font is not None:
    ToDoWindow(font).open()
