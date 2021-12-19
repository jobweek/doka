from multiprocessing import Process, Queue, Pool, freeze_support, Manager
import time
import random
from functools import partial



def proxy_dict_second_core(namespace):

    while True:
        string = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        random.shuffle(string)
        print(string)
        namespace.list = string
        time.sleep(5)

class Test_Class():

    def __init__(self):
        
        self.list = 0

    def get(self):
        
        return self.list
        
    def set(self, input):
        
        self.list = input

def test(i, namespace):

    time.sleep(random.randrange(3))

    k = namespace.list

    return i, k

if __name__ == '__main__':

    freeze_support()
    m = Manager()
    namespace = m.Namespace()

    p = Process(target = proxy_dict_second_core, args = (namespace,))
    p.daemon = True
    p.start()

    match_list = [1,2,3,4,5,6,7,8,9,10]

    with Pool(processes = 2) as pool:

        for i in pool.imap(partial(test, namespace = namespace), match_list):

            print(i)
