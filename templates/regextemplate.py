import re

VAR_TOKEN_START = "{{"
VAR_TOKEN_END = "}}"
BLOCK_TOKEN_START = "{%"
BLOCK_TOKEN_END = "%}"
TOK_REGEX = re.compile(r'(%s.*?%s|%s.*?%s)'%(
    VAR_TOKEN_START,
    VAR_TOKEN_END,
    BLOCK_TOKEN_START,
    BLOCK_TOKEN_END))

loop = (TOK_REGEX.split((
"""<!DOCTYPE html>
<html>
<head>
{{page.title}}
{% if predicate %} X {% end if %}
{% for f in person.friends %}
{% end for %}
</head>
</hmtl>""")))

def nodeType(string):
    
    # python node {{expr}} regex
    try:
        
        if re.match(r'^(\{\{).*(\}\})$', string) is not None:

            return ("expr")

       # include tag

        if re.match(r'^(\{\%) *include .*(\%\})$',string) is not None: #Checks for beginning unary tag
            return("include")

        # if statement

        if re.match(r'^(\{\% *if) *.* *(\%\})$',string) is not None:
            
            return("if statement begin")
        if re.match(r'^(\{\% *) *end *if *(\%\})$',string) is not None:
            
            return("if statement end")

        
    except:
        print("non existent node type")

    
        
            
        



     # '{{ expr }}' {% include path %} {% if predicate 
    

#print(nodeType("{% if x %} SOMETHING {% end if %}"))

for i in loop:
    print(nodeType(i))
    
