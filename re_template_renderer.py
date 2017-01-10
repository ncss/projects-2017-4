import re

def render_template(temp, context):
    def format_expr(matches):
        return str(eval(matches.group(1),{},context))
  
    def fill_include(match):
        fn = match.group(1)
        return render_template(fn,context)
  
    def if_statement(match):
        predicate = match.group(1)
        if eval(predicate,{},context):
            return match.group(2)
  
    with open('templates/' + temp) as f:
        txt = f.read()
        txt = re.sub(r'{% *if *([\w\.\'\"< \[\]]+) *%}([\w\{\} \.]+){% *end if *%}',if_statement,txt) #only < than symbol

        txt = re.sub(r'{{ *([\w\'\"\[\]\.]+) *}}',format_expr,txt)
        txt = re.sub(r'{% *include *([\w.]+) *%}',fill_include,txt)
        return txt

if __name__ == '__main__':
    class Person:
	    def __init__(self, name):
		    self.name = name
    p = Person('Bob')
    print(render_template('renderer_test.txt', {'p':p,'name':'Mitch','profile':{'age':17}}))
