def program(template, context):
    """ Runs the entire program.
    Takes template file as input and returns html file """
    tree = parse(template)
    ret = execute(tree, context)
    return ret

def parse(fileName):
    """ Checks the syntax of the template file 'template'
    and creates and returns a node tree """
    f = open(fileName)
    template = f.read()
    f.close()
    
    nodeTree = []


    
    return nodeTree

parse("inputTest.txt")
"""

class Lexer: # This checks the syntax and creates an expression tree of nodes
    def __init__(self, template):
        self.template = template
        self.upto = 0

    def parseGroup(self):

    def parseText(self):

    def parsePython(self):
        

class GroupNode:
    def __init__(self):


class PythonNode:
    def __init__(self):


class TextNode:
    def __init__(self):
        """
