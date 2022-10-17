import threading


class A:
    def __init__(self):
        self.a = 1
        thread = threading.Thread(target=self.ba)
        thread.start()
        del self
        print("LMAO")

    def ba(self):
        while True:
            self.a = 2
            print(self.a)


ja = A()
