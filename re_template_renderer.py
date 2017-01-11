import re
import html
import copy

def render_template(filename, context):
    """ Opens the file and calls the 'program' function """
    # Get template string
    f = open('templates/' + filename, encoding='utf-8')
    template = f.read()
    #print(template.encode("utf-8"))
    f.close()
    # Call program
    return program(template, context)

def program(string, context):
    """ Runs the entire program.
    Takes template file as input and returns html file """
    tree = parse(string) # Parse the template string and create node tree
    ret = render(tree, context) # Render the node tree and return the result
    return ret

def parse(template):
    """ Checks the syntax of the template file 'template'
    and creates and returns a node tree """
    lex = Lexer(template) # Create lexer object and pass it the template string
    nodeTree = lex.parse() # Call the parse method that will parse the string and return a node tree
    return nodeTree

def render(nodeTree, context):
    return nodeTree.render(context) # Call the render method on the head node of the tree


def getNodeType(string):
    """ Checks to see what type of node the string 'string' starts with """
    if re.match(r'{{.*}}', string) is not None: # Check if is a python expression tag
        return "expr"
    elif re.match(r'{% *include.*%}', string) is not None: # Check if its an include tag
        return "include"
    elif re.match(r'{% *safe.*%}', string) is not None: # Check if its an safe tag
        return "safe"
    elif re.match(r'{% *if.*%}.*{% *end *if *%}', string, re.DOTALL) is not None: # Check if its a pair of 'if' tags
        return "if"
    elif re.match(r'{% *comment *%}.*{% *end *comment *%}', string, re.DOTALL) is not None: # Check if its a pair of 'if' tags
        return "comment"
    elif re.match(r'{% *for.*in.*%}.*{% *end *for *%}', string, re.DOTALL) is not None: # Check if its a pair of 'for' tags
        return "for"
    else:
        return "text"


class Lexer: # This checks the syntax and creates a node tree
    def __init__(self, template):
        self.template = template
        self.upto = 0
        self.nodeTree = GroupNode() # Head node of the tree

    def peek(self, amt=1): # Returns the next 'amt' character (Returns none if thats past the end of the string)
        if self.upto+amt-1 < len(self.template):
            return self.template[self.upto:self.upto+amt]

    def next(self):
        self.upto += 1

    def parse(self):
        while self.upto < len(self.template): # While there's still input left
            #print(self.template[self.upto:].encode("utf-8"))
            nodeType = getNodeType(self.template[self.upto:])
            if nodeType == "expr":
                self.parsePython()
            elif nodeType == "include":
                self.parseInclude()
            elif nodeType == "if":
                self.parseIf()
            elif nodeType == "for":
                self.parseFor()
            elif nodeType == "text":
                self.parseText()
            elif nodeType == "safe":
                self.parseSafe()
            elif nodeType == "comment":
                self.parseComment()
        return self.nodeTree


    def parseText(self):
        start = self.upto # Log the start of the node
        while self.peek(1) not in ['{', None] or self.peek(2) not in ["{{", "{%", None]: # While its not the start of another node or the end of the string
            self.next()
        if start == self.upto: # If the node starts with a bracket and it hasnt been picked up by the earlier regex: ERROR
            #print("Unknown statement:", repr(self.template[start:self.upto][:100]))
            raise NameError("Unknown statement.")
        # Create a text object and add it to the current children
        self.nodeTree.children.append(TextNode(self.template[start:self.upto])) # I think the errors used in these are not needed

    def parsePython(self):
        start = self.upto # Log the start of the node
        while self.peek() not in ["}", None]: # While its not the end of the node or the end of the string
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
        start = self.upto # Log the start of the node
        while self.peek(2) not in ["%}", None]:  # While its not the end of the node or the end of the string
            self.next()
        # Check that there are ending brackets
        if self.template[self.upto:self.upto+2] == "%}":
            self.next()
            self.next()
        else:
            raise SyntaxError("Closing bracket for an {% include %} statement was not found.")
        # Create a include object and add it to the current children
        self.nodeTree.children.append(IncludeNode(self.template[start:self.upto])) # I think the errors used in these are not needed

    def parseSafe(self):
        start = self.upto # Log the start of the node
        while self.peek(2) not in ["%}", None]:  # While its not the end of the node or the end of the string
            self.next()
        # Check that there are ending brackets
        if self.template[self.upto:self.upto+2] == "%}":
            self.next()
            self.next()
        else:
            raise SyntaxError("Closing bracket for an {% safe %} statement was not found.")
        # Create a include object and add it to the current children
        self.nodeTree.children.append(SafeNode(self.template[start:self.upto])) # I think the errors used in these are not needed

    def parseIf(self, addToTree=True):
        start = self.upto # Log the start of the node
        self.next() # Skip the inital brackets
        self.next()
        # Look for the start of the {% end if %} tag
        while self.peek() is not None and re.match(r'{% *end *if *%}', self.template[self.upto:]) == None:
            if getNodeType(self.template[self.upto:]) == "if": # If there is another if inside this if
                self.parseIf(False) # This dosent need to be added to tree cuz it will be when the intial if is parsed
            else:
                self.next()
        if self.peek(2) == None: # If there was no {% end if %} tag found
            raise SyntaxError("No {% end if %} tag found")
        # Look for the end of the {% end if %} tag
        while self.peek(2) not in ["%}", None]:
            self.next()
        if self.peek(2) == None: # If there was no closing bracket found of on the {% end if %} tag found
            raise SyntaxError("No closing bracket on the {% end if %} tag found")
        self.next()
        self.next()
        if addToTree == True:
            # Create a if object and add it to the current children
            self.nodeTree.children.append(IfNode(self.template[start:self.upto]))

    def parseComment(self):
        start = self.upto # Log the start of the node
        self.next() # Skip the inital brackets
        self.next()
        # Look for the start of the {% end comment %} tag
        while self.peek() is not None and re.match(r'{% *end *comment *%}', self.template[self.upto:]) == None:
            self.next()
        if self.peek(2) == None: # If there was no {% end comment %} tag found
            raise SyntaxError("No {% end comment %} tag found")
        # Look for the end of the {% end comment %} tag
        while self.peek(2) not in ["%}", None]:
            self.next()
        if self.peek(2) == None: # If there was no closing bracket found of on the {% end if %} tag found
            raise SyntaxError("No closing bracket on the {% end comment %} tag found")
        self.next()
        self.next()

    def parseFor(self, addToTree=True):
        start = self.upto # Log the start of the node
        self.next()
        self.next()
        # Look for the start of the {% end for %} tag
        while self.peek() is not None and re.match(r'{% *end *for *%}', self.template[self.upto:]) == None:
            if getNodeType(self.template[self.upto:]) == "for": # If there is another for inside this for
                self.parseFor(False) # This dosent need to be added to tree cuz it will be when the intial if is parsed
            else:
                self.next()
        if self.peek(2) == None: # If there was no {% end for %} tag found
            raise SyntaxError("No {% end for %} tag found")
        # Look for the end of the {% end for %} tag
        while self.peek(2) not in ["%}", None]:
            self.next()
        if self.peek(2) == None: # If there was no closing bracket found of on the {% end for %} tag found
            raise SyntaxError("No closing brack on the {% end for %} tag found")
        self.next()
        self.next()
        if addToTree == True:
            # Create a for object and add it to the current children
            self.nodeTree.children.append(ForNode(self.template[start:self.upto]))

class GroupNode:
    def __init__(self, children=None):
        if children == None:
            self.children = []
        else:
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
        try:
            return html.escape(str(eval(self.content, {}, context)))
        except Exception: # Probably should be more specific about the error type
            return ""

class SafeNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        self.content = self.content[2:-2].replace("safe", "").strip()
        try:
            return eval(self.content, {}, context)
        except Exception: # Probably should be more specific about the error type
            return ""

class TextNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        return self.content

class IncludeNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        string = self.content[2:-2].replace("include", "").strip()
        f = string.strip()
        return render_template(f, context)

class IfNode:
    def __init__(self, content):
        self.content = content

    def render(self, context):
        def if_statement(match):
            predicate = match.group(1)
            arguments = re.match(r'{% *if.*?%}(.*){% *else *%}(.*){% *end *if *%}', self.content, re.DOTALL)
            try:
                condition = eval(predicate, {}, context)
                if condition:
                    if arguments is not None:
                        return arguments.groups()[0] # Return the if block
                    else:
                        return match.group(2) # Return the if block
                else:
                    if arguments is not None:
                        return arguments.groups()[1]
            except Exception: # Probably should be more specific about the error type
                return ""

        txt = re.sub(r'^{% *if *([^%]+) *%}(.*){% *end *if *%}$', if_statement, self.content, 0, re.DOTALL)
        if txt:
            return program(txt, context)
        else:
            return ""

class ForNode:
    def __init__(self, content):
        self.content = content
    def render(self, context):
        def for_statement(match):
            dest = match.group(1)
            src = match.group(2)
            output = []
            try:
                iterable = eval(src, {}, context)
                varCount = len(dest.split(","))
                if varCount > 1:
                    for item in iterable:
                        if len(item) != varCount:
                            #print(item)
                            raise Exception
            except Exception: # Probably should be more specific about the error type
                iterable = ""
            for item in iterable:
                codeBlock = match.group(3)
                newContext = copy.deepcopy(context)
                newContext[dest] = item
                #for index, variable in enumerate(dest.split(",")):
                #    newContext[variable.strip()] = item[index]
                output.append(program(codeBlock, newContext))
            return "".join(output)

        txt = re.sub(r'^{% *for *([^%]+) in ([^%]+) *%\}(.*)\{% *end for *%\}$', for_statement, self.content, 0, re.DOTALL)
        return txt

class f:
    def __init__(self):
        self.name = "Isaac"

