import glob
from time import sleep
from process_task import process

if __name__ == '__main__':
    file_path = '/var/img/'
    old_list = []
    while True:
        new_list = glob.glob(file_path + '*')
        new_files = [fn for fn in new_list if fn not in old_list]
        sleep(5)
        for fn in new_files:
            print(fn)
            process.delay(fn)
        old_list = new_list
