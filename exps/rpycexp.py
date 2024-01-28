import rpyc

class MyService(rpyc.Service):
    def on_connect(self):
        # code that runs when a connection is created
        # (to init the ser
        print("on_connect")
        pass

    def on_disconnect(self):

        # code that runs when the connection has already closed
        # (to finalize the service)
        print("on_disconnect")
        pass

    def exposed_get_answer(self):  # this is an exposed method
        return 42
    

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyService, port=18861)
    t.start()
    # t.stop()
    # t.close()