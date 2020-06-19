import time
from Database.scanning_interface import database_creation

if __name__ == '__main__':
    a = time.time()
    folders = database_creation()
    b = time.time()
    print('Time:', b - a)
