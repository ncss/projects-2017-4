from tornado.ncss import Server

def hello(response):
	response.write('hello world')

server = Server()
server.register(r'/', hello)
server.run()