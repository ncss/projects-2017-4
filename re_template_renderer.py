import re

def render_template(temp, context):
  def format_expr(matches):
    return str(eval(matches.group(1),{},context))
  
  def fill_include(match):
    fn = match.group(1)
    return render_template(fn,context)
  
  with open('templates/' + temp) as f:
    txt = f.read()
    txt = re.sub(r'{{ *([\w\'\"\[\]\.]+) *}}',format_expr,txt)
    txt = re.sub(r'{% *include *([\w.]+) *%}',fill_include,txt)
    
    return txt

if __name__ == '__main__':
  print(render_template('renderer_test.txt', {'name':'Mitch','f.name':'Sam','profile':{'age':17}}))
