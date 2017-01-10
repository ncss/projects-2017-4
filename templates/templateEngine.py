import re

def program(filename, context):
    """ Runs the entire program.
    Takes template file as input and returns html file """
    tree = parse(filename)
    ret = render(tree, context)
    return ret

def parse(filename):
    """ Checks the syntax of the template file 'template'
    and creates and returns a node tree """
    # Get template string
    f = open(filename)
    template = f.read()
    f.close()

    nodeTree = Lexer(template).parse()
    return nodeTree

def render(nodeTree, context):
    return nodeTree.render(context)




def getNodeType(string):
    """ Checks to see what type of node the string 'string' starts with """
    if re.match(r'\{\{.*\}\}', string) is not None:
        return "expr"
    elif re.match(r'\{\% *include.*\%\}', string) is not None:
        return "include"
    elif re.match(r'\{\% *if.*\%\}.*{% *end *if *%}', string) is not None:
        return "if"
    elif re.match(r'\{\% *for.*in.*\%\}.*{% *end *for *%}', string) is not None:
        return "for"
    else:
        return "text"

#parse("inputTest.txt")

class Lexer: # This checks the syntax and creates an expression tree of nodes
    def __init__(self, template):
        self.template = template
        self.upto = 0
        self.nodeTree = GroupNode()

    def peek(self, amt=1): # Returns None if self.upto >= len(self.template)
        if self.upto+amt-1 < len(self.template):
            return self.template[self.upto:self.upto+amt]

    def next(self):
        self.upto += 1

    def parse(self):
        while self.upto < len(self.template): # While there's still input left
            nodeType = getNodeType(self.template[self.upto:])
            if nodeType == "expr": # If its an expression
                self.parsePython()
            elif nodeType == "include":
                self.parseInclude()
            elif nodeType == "if":
                self.parseIf()
            elif nodeType == "for":
                print("Not yet implemented. For")
                return 0
            elif nodeType == "text":
                self.parseText()

        return self.nodeTree

    def parseGroup(self):
        pass

    def parseText(self):
        start = self.upto
        # Find the end of the text statement
        while self.peek() not in ["{", None]:
            self.next()
        if start == self.upto:
            raise NameError("Unknown statement.")
        # Create a text object and add it to the current children
        self.nodeTree.children.append(TextNode(self.template[start:self.upto])) # I think the errors used in these are not needed

    def parsePython(self):
        start = self.upto
        # Find the end of the expr statement
        while self.peek() not in ["}", None]:
            self.next()
        # Check that there are ending brackets
        if self.template[self.upto:self.upto+2] == "}}":
            self.next()
            self.next()
        else:
            raise SyntaxError("Closing bracket for an {{ expr }} statement was not found.")
        # Create a python object and add it to the current children
        self.nodeTree.children.append(PythonNode(self.template[start:self.upto])) # I think the errors used in these are not needed

    def parseInclude(self):
        start = self.upto
        # Find the end of the include statement
        while self.peek(2) not in ["%}", None]:
            self.next()
        # Check that there are ending brackets
        if self.template[self.upto:self.upto+2] == "%}":
            self.next()
            self.next()
        else:
            raise SyntaxError("Closing bracket for an {% include %} statement was not found.")
        # Create a python object and add it to the current children
        self.nodeTree.children.append(IncludeNode(self.template[start:self.upto])) # I think the errors used in these are not needed

    def parseIf(self):
        start = self.upto
        self.next() # Skip the inital brackets
        self.next()
        # Look for the start of the {% end if %} tag
        while self.peek(2) not in ["{%", None]:
            self.next()
        if self.peek(2) == None: # If there was no {% end if %} tag found
            raise SyntaxError("No {% end if %} tag found")
        # Look for the end of the {% end if %} tag
        while self.peek(2) not in ["%}", None]:
            self.next()
        if self.peek(2) == None: # If there was no closing bracket found of on the {% end if %} tag found
            raise SyntaxError("No closing brack on the {% end if %} tag found")
        self.next()
        self.next()
        # Create a if object and add it to the current children
        self.nodeTree.children.append(IfNode(self.template[start:self.upto]))

class GroupNode:
    def __init__(self, children=[]):
        self.children = children
        self.output = []

    def render(self, context):
        output = []
        for child in self.children:
            output.append(str(child.render(context)))
        return "".join(output)


class PythonNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        self.content = self.content[2:-2].strip()
        return eval(self.content, {}, context)

class TextNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        return self.content

class IncludeNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        string = self.content.replace("{%", "").replace("%}", "").replace("include", "")
        f = string.strip()
        return program(f, context)

class IfNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        def if_statement(match):
            predicate = match.group(1)
            if eval(predicate,{},context):
                return match.group(2)
                
        txt = re.sub(r'{% *if *([^%]+) *%}(.*){% *end if *%}',if_statement,self.content)
        if txt:
            return program(txt, context)
        else:
            return ""


