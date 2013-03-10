import re

class ToDo(object):
    
    todo_label = u"TODO"
    done_label = u"DONE"
    boundry = "###"
    # TODO: If pattern used a backreference the bountry could be randomized
    pattern = "#{3} (%s|%s):\n(.*?)\n#{3}" % (todo_label, done_label)
    skeleton = "%s %s:\n%s\n%s\n\n"
    single_regexp = re.compile(pattern, re.U + re.S)
    
    def __init__(self, source, raw):
        self.source = source
        self.block = Block(source)
        self.raw = raw
        self.note = ToDo.parse(raw)
        self.completed = self.isComplete()
        self.newRecord = not self.block.hasToDo(self.raw)
        self.glyph = self.block.resource.getGlyph()
        self._original_state = dict(self.__dict__)
            
    def save(self):
        self.block.setup()
        
        note = self.note.strip()
        todo = self.skeleton % (self.boundry, self.done_label if self.completed else self.todo_label, note, self.boundry)
        
        if self.newRecord:
            self.block.insert(todo)
        elif self.isUpdated():
            self.block.replace(todo, self.raw)
        
        self.newRecord = False
        self._original_state = dict(self.__dict__)
        self.raw = todo
    
    def isUpdated(self):
        return self._original_state['completed'] is not self.completed or \
            self._original_state['note'] is not self.note
        
    def destroy(self):
        if not self.newRecord:
            self.block.erase(self.raw)
                        
    def isComplete(self):
        match = self.single_regexp.match(self.raw)
        return bool(match) and match.group(1).find(self.done_label) is not -1

    def toCell(self):
        return {
            "completed": self.completed, 
            "glyph": self.glyph, 
            "note": self.note,
            "todo": self
        }
        
    @staticmethod
    def parse(raw):
        if raw is None:
            return None
        match = ToDo.single_regexp.match(raw)
        if match:
            return match.group(2)
        else:
            return raw
            
class Resource(object):
    
    def __init__(self, source):
        if source is None:
            raise AttributeError
            
        self.source = source
        self.type = 'font' if hasattr(source, 'info') else 'glyph'
        self.info = self.getInfo()
        
    def getInfo(self):
        if self.type is 'font':
            return self.source.info
        else:
            return self.source
    
    def getGlyph(self):
        if self.type is 'glyph':
            return self.source.name
        else:
            return "*"
    

class Block(object):
    
    begin = "### RoboToDo ###\n\n"
    end = "#####"
    block_regexp = re.compile(r"%s(.*)%s" % (begin, end), re.S)

    def __init__(self, source):
        self.resource = Resource(source)
        self.lines = Block.parse(self.resource.info.note)
            
    def setup(self):
        if not self.resource.info.note:
            self.resource.info.note = ""
        if not self.match():
            if self.resource.info.note is not "":
                self.resource.info.note += "\n"
            self.resource.info.note += self.begin + self.end
        return self.resource.info.note
    
    def teardown(self):
        lines = Block.parse(self.resource.info.note)
        if not lines:
            self.resource.info.note = self.resource.info.note.replace(self.begin, '')
            self.resource.info.note = self.resource.info.note.replace(self.end, '')
            self.resource.info.note = self.resource.info.note.rstrip()
    
    def match(self):
        if self.resource.info.note is None:
            return None
        return self.block_regexp.search(self.resource.info.note)
        
    def insert(self, todo):
        inserted_block = r"%s\1%s%s" % (self.begin, todo, self.end)
        self.resource.info.note = re.sub(self.block_regexp, inserted_block, self.resource.info.note)
        
    def replace(self, todo, raw):
        self.resource.info.note = self.resource.info.note.replace(raw, todo)
    
    def erase(self, raw):
        self.resource.info.note = self.resource.info.note.replace(raw, '')
        self.teardown()
        
    def hasToDo(self, raw):
        match = self.match()
        if match:
            return match.group().find(raw) >= 0
        else:
            return False
    
    def contents(self):
        match = self.match()
        if match:
            return match.group(1)

    @staticmethod
    def parse(raw):
        if raw is None:
            return []
        block = Block.block_regexp.search(raw)
        if block:
            raw_note = block.group(1)
            lines = []
            matches = ToDo.single_regexp.finditer(raw_note)
            for match in matches:
                lines.append(match.group())
            return lines
        else:
            return []
