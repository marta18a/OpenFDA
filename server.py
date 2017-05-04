import web
import socketserver
PORT = 8000

#Handler = http.server.SimpleHTTPRequestHandler
Handler = web.testHTTPRequestHandler

#clase a partir de la cual se crean los objetor. Se crean obj de clase Handler
socketserver.TCPServer.allow_reuse_address=True
httpd = socketserver.TCPServer(("", PORT), Handler) #Utilizando la clase Handler se crea un objeto
print("serving at port", PORT)
httpd.serve_forever()
#servidor recibe peticion y la envia a Handler
#con parentesis creo obj de clase
