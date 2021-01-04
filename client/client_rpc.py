import xmlrpc.client
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--ip',
                    type=str,
                    help='Server IP')

parser.add_argument('--port',
                    type=int,
                    help='Server PORT')

parser.add_argument('-u',
                    '--username',
                    type=str,
                    help='Username')

parser.add_argument('-p',
                    '--password',
                    type=str,
                    help='Password')

args = parser.parse_args()

HOST = args.ip
PORT = args.port
username = args.username
password = args.password

proxy = xmlrpc.client.ServerProxy(f'http://{username}:{password}@{HOST}:{PORT}')

while True:
    command = input('rpcclient $> ')
    arg = ''
    try:
        command, arg = command.split(' ')
    except ValueError:
        command = command

    if command == 'help':
        print(proxy.help())
    elif command == 'dirList':
        print(proxy.dirList(arg))
    elif command == 'readFile':
        if arg == '':
            print('You did not provide filename')
        else:
            print(proxy.readFile(arg))
    elif command == 'downloadFile':
        if arg == '':
            print('You did not provide filename')
        else:
            content = proxy.readFile(arg)
            if content == 'File not found' or content == 'Permission denied':
                print('Can\'t download file')
                continue
            filename = os.path.basename(arg)
            with open(filename, 'w') as file:
                file.write(content)
                file.close()
    elif command == 'uploadFile':
        if arg == '':
            print('You did not provide filename')
        try:
            with open(filename, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print('File not found')
        except PermissionError:
            print('Permission denied')
        filename = os.path.basename(arg)
        if content == 'File not found' or content == 'Permission denied':
            print('Can\'t upload file')
        else:
            print(proxy.uploadFile(filename, content))
    elif command == 'createUser':
        if arg == '':
            print('You did not provide credentials')
        else:
            try:
                username, password = arg.split(':')
            except ValueError:
                print('Wrong format (username:password)')
            print(proxy.createUser(username, password))

    else:
        print('Command does not exist')
