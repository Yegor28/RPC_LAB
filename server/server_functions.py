import os


users = {'yegor': 'yegor'}

def help():
    return '''
    Available commands:
    1) dirList <path>
    2) readFile <path or filename>
    3) uploadFile <path or filename>
    4) createUser <username>:<password>
    '''

def dirList(directory):
    if directory == '':
        files = os.listdir()
    else:
        try:
            files = os.listdir(directory)
        except FileNotFoundError:
            return 'Directory does not exist'
        except PermissionError:
            return 'Permission denied'
    return files

def readFile(filename):
    try:
        with open(filename) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return 'File not found'
    except PermissionError:
        return 'Permission denied'

def uploadFile(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    return 'File uploaded'

def createUser(username, password):
    if username in users.keys():
        return 'User exists'

    users[username] = password
    return 'User created'

