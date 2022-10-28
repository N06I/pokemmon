import socket
import pickle


class Client:
    def __init__(self, pid=None):
        self.HEADER = 16
        self.PORT = 5050
        self.FORMAT = "utf-8"
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = socket.gethostbyname(socket.gethostname())  # replace for actual server's ip unless self-hosting
        self.SERVER = "192.168.0.13"
        self.ADDR = (self.SERVER, self.PORT)

        self.client = socket.socket(socket.AF_INET, socket.TCP_NODELAY)
        self.client.connect(self.ADDR)

        self.connection_id = pid

        # self.send(self.DISCONNECT_MESSAGE)

    def send(self, msg):
        message = pickle.dumps(msg)
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' '*(self.HEADER - len(send_len))
        self.client.send(send_len)
        self.client.send(message)

    def request(self, msg):     # requests data by msg string
        self.send(msg)      # first sends msg string

        msg_length = None   # runs until answer is obtained
        while not msg_length:
            # each message will come in the form of 2 messages,
            # the first one being a HEADER containing the length of the 2d
            msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)  # header
            if msg_length:  # necessary check; because when a client connects it sends an "empty" (NoneType) message
                msg_length = int(msg_length)
                reply = pickle.loads(self.client.recv(msg_length))  # actual message

                if type(reply) is not dict: print(f"[{self.ADDR}] {reply}")
                # conn.send("Msg received".encode(self.FORMAT))
                return reply

    def instance_update(self, player):  # could pass the 3 attributes as parameters if it's faster
        return self.request((player.position, player.state))

    def update_server_area(self, area_name):    # MUST BE RUN by game function that switches the current area
        self.request(area_name)                 # for server internal reasons

    def set_pid(self, pid=-1):  # MUST BE RUN to notify the server of a login, so it can set a pid!
        # only serves the client to store an id that connects it to a server stored session
        return int(self.request(str(pid)))
