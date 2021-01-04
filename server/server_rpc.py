import argparse
from base64 import b64decode
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
#from server_functions import readFile, uploadFile, help, createUser, dirList
from server_functions import help, dirList, readFile, uploadFile, createUser, users



class SecureXMLRPCServer(SimpleXMLRPCServer):
    def __init__(self, host, port, username, password):
        self.username = username
        self.password = password
        class VerifyingRequestHandler(SimpleXMLRPCRequestHandler):
            def parse_request(request):
                if SimpleXMLRPCRequestHandler.parse_request(request):
                    if self.authenticate(request.headers):
                        return True
                    else:
                        request.send_error(401, 'Username or password is incorrect')
                    return False
        SimpleXMLRPCServer.__init__(self, (host, port), requestHandler=VerifyingRequestHandler)

    def authenticate(self, headers):
        headers = headers.get('Authorization').split()
        encoded = headers[1]
        username, password = str(b64decode(encoded), 'utf-8').split(':')
        if username in users.keys():
            if password == users[username]:
                return True
        return False

parser = argparse.ArgumentParser()
parser.add_argument('--ip',
                    type=str,
                    help='Server IP')

parser.add_argument('--port',
                    type=int,
                    help='Server PORT')

args = parser.parse_args()



def run_server(host, port, username, password):
    server = SecureXMLRPCServer(host, port, username, password)
    server.register_function(help)
    server.register_function(dirList)
    server.register_function(readFile)
    server.register_function(uploadFile)
    server.register_function(createUser)


    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Exiting')


run_server(args.ip, args.port, 'yegor', 'yegor')
