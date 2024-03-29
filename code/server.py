import _pickle
import socket
import threading
import pickle
import time


class Server:
    def __init__(self):
        self.FORMAT = "utf-8"
        self.HEADER = 16
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())  # gets host's IP
        # self.SERVER = "192.168.0.14"
        print(f"Hosting at [{self.SERVER}]")
        self.ADDR = (self.SERVER, self.PORT)
        self.DISCONNECT_MESSAGE = "!DISCONNECT"

        self.server = socket.socket(socket.AF_INET, socket.TCP_NODELAY)
        self.server.bind(self.ADDR)

        self.player_cnt = -1
        self.players = {}

        self.loaded_players = {"bill_house": {}}  # players loaded in each area, by playerId; areas remain when empty
        #     "bill_house": {        # example data
        #         2: PlayerZip(),    # PlayerZip is deprecated; now a tuple: (player.position, player.state)
        #         0: PlayerZip(),
        #         5: PlayerZip()},
        #     "celadon_city": {
        #         1: PlayerZip(),
        #         4: PlayerZip()},
        #     "celadon_mall_roof": {
        #         3: PlayerZip()}
        # }
        self.current_areas = []     # data remains loaded when player is offline, so client can retrieve last session
        self.msg_mail = {}

        print("[STARTING] server is starting...")
        self.start()

    def handle_client(self, conn, addr):  # 1 threaded handle_client method will run per client connected to server
        print(f"[NEW CONNECTION] {addr} connected.")
        pid = self.player_cnt + 1
        self.msg_mail[pid] = []

        connected = True
        while connected:
            # each message will come in the form of 2 messages,
            # the first one being a HEADER containing the length of the 2d
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)  # header
            if msg_length:  # necessary check; because when a client connects it sends an "empty" (NoneType) message
                msg_length = int(msg_length)
                try:
                    peckel = conn.recv(msg_length)
                    msg = pickle.loads(peckel)  # actual message
                except _pickle.UnpicklingError:
                    print("picklerror")
                    break
                # print(f"{time.perf_counter()}: {msg}")

                if type(msg) is tuple:  # msg is ((pos, ition), "state"); requests area frame update
                    area = self.current_areas[pid]  # gets player's data from pid in method execution memory
                    self.loaded_players[area][pid] = msg  # stores the received player's current data internally
                    self.send(conn, self.loaded_players[area])  # replies with the current area's players' data

                elif type(msg) is str:  # sending ints as string so need to check
                    try:
                        msg = int(msg)
                        if msg == -1:  # -1 => new game request, 0+ ints are playerIds
                            self.player_cnt += 1
                            print(f"[NEW GAME] created, for player {self.player_cnt}")
                            self.current_areas.append("bill_house")
                            self.loaded_players["bill_house"][self.player_cnt] = ((120, 90), "walk_down")
                            self.send(conn, pid)
                            descr = f"NEW_GAME({self.player_cnt})"
                        elif msg >= 0:  # if not new game, sets the right pid to the (current) method execution
                            pid = msg
                            self.send(conn, pid)  # can do this to use a single line to start or continue game
                            descr = "RELOG"
                        else:
                            descr = "kekw"
                    except ValueError:
                        if msg == self.DISCONNECT_MESSAGE:  # checks for abrupt disconnection
                            print("discomesg")
                            connected = False
                            descr = "DC"
                        if msg == "chat":
                            for mesg in self.msg_mail[pid]:
                                print(mesg.text)
                            self.send(conn, self.msg_mail[pid])
                            self.msg_mail[pid] = []
                            descr = "CHAT_UPDATE"
                        else:  # it's an area change
                            old_area = self.current_areas[pid]
                            # pops the player data from his old area and adds it to the new
                            if msg not in self.loaded_players:  # msg is the new area
                                self.loaded_players[msg] = {}
                            self.loaded_players[msg][pid] = self.loaded_players[old_area].pop(pid)
                            self.current_areas[pid] = msg
                            self.send(conn, True)
                            descr = "CHANGED_AREA"
                    # print(f"[{addr}] requested [{descr}]: {msg} ")
                else:   # chat message
                    if msg.channel == "l":
                        area = self.current_areas[pid]
                        for playerid in self.msg_mail:
                            if self.current_areas[playerid] == area and playerid != pid:
                                self.msg_mail[playerid].append(msg)
                    elif type(msg.channel) == int:
                        self.msg_mail[msg.channel].append(msg)
                    else:   # for now
                        for playerid, mail in self.msg_mail.items():
                            if playerid != pid:
                                mail.append(msg)

        del self.loaded_players[self.current_areas[pid]][pid]
        del self.msg_mail[pid]
        # for pidd, msgs in self.msg_mail.items():
        #     if pid in pids:
        #         self.msg_mail[mesg].pop(pid)
        conn.close()

    def send(self, conn, msg):
        message = pickle.dumps(msg)
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER - len(send_len))
        conn.send(send_len)
        conn.send(message)

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()

            # creates an individual thread that will run the target method with those arguments,
            # this is required because listening for a client's messages is asynchronous
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # print º current active connections


server = Server()
