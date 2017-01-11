from tornado.ncss import Server
from re_template_renderer import render_template
#uncomment later when DB is fixed
from db.plutonium import User,Post,Comment,database_connect

#to create street.db, double click create_db.py

###DECORATORS###
def loginRequired(fn):
    def inner(response, *args, **kwargs):
        user = response.get_secure_cookie('userCookie')
        if user is None:
            response.redirect('/login')
        else:
            return fn(response, *args, **kwargs)
    return inner

def notLoginRequired(fn):
    def inner(response, *args, **kwargs):
        user = response.get_secure_cookie('userCookie')
        if user is None:
            return fn(response, *args, **kwargs)
        else:
            response.redirect('/home')
    return inner

###REGULAR REFERENCE FUNCTIONS###

def home(response):
    user = get_current_user(response)
    html = render_template('main.html', {'user': user})
    response.write(html)



def login_handler(response):
    email = response.get_field("email")
    password = response.get_field("password")
    try:
        user = User.login(email, password)
        response.set_secure_cookie('userCookie', email)
        response.redirect('/home')
    except ValueError:
        user = get_current_user(response)
        html = render_template('login.html', {'user': user, 'invalidUser': "Invalid login." })
        response.write(html)

def submit_handler(response): 
    user = get_current_user(response)
    title = response.get_field("title")
    location = response.get_field("location")
    image = response.get_file("postImage")
    pictureName = 'static/postimages/'+title+'.'+image[1].split('/')[1]
    with open(pictureName,'wb') as pictureFile:
        pictureFile.write(image[2])
     
    description = response.get_field("description")
    if (not title) or (not location) or (not image) or (not description):
        html = render_template('new_post.html', {'user': user, 'invalidPost': "Please fill in all fields." })
    else:
        html = render_template('new_post.html', {'user': user})
    response.write(html)

def signup_handler(response):
    name = response.get_field('name')
    email = response.get_field('email')
    password = response.get_field('password')
    confpassword = response.get_field('confpassword')
    if (not name) or (not email) or (not password) or (not confpassword):
        user = get_current_user(response)
        html = render_template('signup.html', {'user': user, 'errorMessage': "You must fill in all fields. Please try again." })
        response.write(html)
    elif password != confpassword:
        user = get_current_user(response)
        html = render_template('signup.html', {'user': user, 'errorMessage': "Password did not match. Please try again." })
        response.write(html)
    else:
        try:
            user = User.register(email,password,name)
            response.set_secure_cookie('userCookie', email)
            response.redirect('/home')
        except ValueError:
            user = get_current_user(response)
            html = render_template('signup.html', {'user': user, 'errorMessage': "This user is already in the database." })
            response.write(html) 

def profile(response,name):
    user = get_current_user(response)
    html = render_template('profile.html', {'user': user})
    response.write(html)

def get_current_user(response):
    email = response.get_secure_cookie("userCookie")    #change back to User(), later when DB is fixed
    user = "hello"
    if email is not None:
        email = email.decode()
        return user
    return None
     
def view_post(response, post_id):
    user = get_current_user(response)
    html = render_template('content.html', {'user': user})
    response.write(html)

def demo(response):
    user = get_current_user(response)
    html = render_template('demo.html', {'user': user})
    response.write(html)


def notfound(response):
    user = get_current_user(response)
    html = render_template('404errorpage.html', {'user': user})
    response.write(html)
    
    
    
###NOT LOGGED IN EXCLUSIVE PAGES###
@notLoginRequired
def login(response):
    user = get_current_user(response)
    html = render_template('login.html', {'user': user})
    response.write(html)

@notLoginRequired
def signup(response):
    user = get_current_user(response)
    html = render_template('signup.html', {'user': user})
    response.write(html)

###LOGIN EXCLUSIVE PAGES###
@loginRequired
def submit(response):
    html = render_template('new_post.html', {})
    response.write(html)

@loginRequired
def logout(response):
    response.clear_cookie("userCookie")
    response.redirect('/home')

    
database_connect('db/street.db')

server = Server()
server.register(r'/?(?:home)?', home)
server.register(r'/profile(?:/([\w\.\-]+))?', profile)
server.register(r'/login', login, post=login_handler)
server.register(r'/signup',signup, post=signup_handler)
server.register(r'/post/([\w\.\-]+)',view_post)
server.register(r'/submit',submit, post=submit_handler)
server.register(r'/demo',demo)
server.register(r'/logout',logout)
server.register(r'.+',notfound)


server.run()
