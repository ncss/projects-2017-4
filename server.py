from tornado.ncss import Server

def home(response):
	response.write('This is the home page')

def profile(response,name):
        response.write('Hi, ' + str(name))
		
def login(response): 
		response.write('<h1>login here.</h1>')

def signup(response):
		response.write('signup here')

def post(response,post_id):
		response.write('Look at this neato post - ' + post_id)

def submit(response):
		response.write('submit a post here jks you cant do that yet')
		
server = Server()


server.register(r'/?(?:home)?', home)
server.register(r'/profile/([\w\.\-]+)', profile)
server.register(r'/login', login)
server.register(r'/signup',signup)
server.register(r'/post/([\w\.\-]+)',post)
server.register(r'/submit',submit)


server.run()
