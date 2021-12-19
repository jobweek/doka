from multiprocessing import Process, Pipe, freeze_support
import time

def test(conn):
    
    for i in range(20):
        
        time.sleep(5)
        print("test", i)
        conn.send(i)

class Cl():
    
    def init(self):

        self.parent_conn, self.child_conn = Pipe()
        self.p = Process(target=test, args=(self.child_conn,))
        self.p.daemon = True
        self.p.start()
        
        self.list = self.parent_conn.recv()
        print("cls init:", self.list)
        
    def get(self):
        print("cls get:", self.parent_conn.poll())
        if self.parent_conn.poll() == False:
        
            return self.list
        
        else:
        
            self.list = self.parent_conn.recv()
        
            return self.list

cl = Cl()

def main():

    cl.init()

    print('main:',cl.get())
    time.sleep(2)
    print('main:',cl.get())
    time.sleep(5)
    print('main:',cl.get())    
    
if __name__ == '__main__':

    freeze_support()
    main()