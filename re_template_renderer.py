import re

def render_template(temp, context):
  def format_expr(matches):
    return str(eval(matches.group(1),{},context))
  
  with open('templates/' + temp) as f:
    txt = f.read()
    return re.sub(r'{{ *([\w\'\"\[\]\.]+) *}}',format_expr,txt)

if __name__ == '__main__':
  print(render_template('renderer_test.txt', {'name':'Mitch','f.name':'Sam','profile':{'age':17}}))
