import socket
import threading
from player import Player
from game import Game
import json
import struct


class Server(object):
    def __init__(self):
        self.connection_queue = [] 
        self.game_id = 0
        self.player_queue = [] 
        self.player_ready = set() 


    def create_new_connection_thread(self):
        """create new connection for listening to one incoming connection
        """
        server = "192.168.1.104"
        port = 5555

        # create socet (IPv4, TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # binding a socket to an address and port
            s.bind((server, port))
        except socket.error as e:
            str(e)

        # Listening to one incoming connection
        s.listen(1)
        print("Waiting for a connection, Server Started")

        while True:
            """handle incoming connections in an infinite loop in a new thread
            """
            conn, addr = s.accept() 
            print("[CONNECT] New connection!")

            self.authentication(conn, addr) 



    def authentication(self, conn_socket, addr):
        """authentication user name, 
            add user in queue, 
            crete thread for interactions with user

        Args:
            conn (obj): socket for server and new user 

        Raises:
            Exception: if there is any error, close connection
        """
        try:
            data = conn_socket.recv(1024)
            name = str(data.decode())
            self.player_queue.append(name)

            if not name:
                raise Exception("No name received")

            conn_socket.sendall("1".encode()) 

            player = Player(addr, name)
            self.handle_queue(player)    
            
            thread = threading.Thread(target=self.player_thread, args=(conn_socket, player))
            thread.start()
        except Exception as e:
            print("[EXCEPTION]", e)
            conn_socket.close()

    def handle_queue(self, player):
        """add obj player in queu list,
            create new game if queu reached the expected quantity

        Args:
            player (obj): new player with unique name and addr
        """
        self.connection_queue.append(player)

    def start_game(self):
            game = Game(self.game_id, self.connection_queue[:])

            for p in game.players:
                p.set_game(game)
            
            print(f"[GAME] Game {self.game_id} started...")

            self.game_id += 1
            self.connection_queue = []
            self.player_queue = []

    def player_thread(self, conn, player):
        """handling interaction between server and player   

        Args:
            conn (obj): connection socket for one player
            player (obj): one player object
        """
        while True: 
            
            try:
                try:
                    data = conn.recv(1024)
                    data = json.loads(data.decode())
                except Exception as e:
                    break

                keys = [int(key) for key in data.keys()]
                send_msg = {key:[] for key in keys} 
                
                last_board = None

                for key in keys: # start current game
                    if key == -3:
                        if 1 < len(self.player_queue) == len(self.player_ready):  
                            self.start_game()
                            self.player_ready = set()
                        self.player_ready.add(data['-3'][0])

                    if key == -2:  # get game, returns a list of players
                        send_msg[-2] = self.player_queue

                    if key == -1:  # get game, returns a list of players
                        if player.game:
                            send = {player.get_name():player.get_score() for player in player.game.players} 
                            send_msg[-1] = send 
                        else:
                            send_msg[-1] = [] 


                    if player.game:
                        if key == 0:  # guess
                            player.game.player_guess(player, data['0'][0])

                        elif key == 1: # skip
                            skip = player.game.skip(player)
                            send_msg[1] = skip
                        elif key == 2:  # get chat
                            content = player.game.round.chat.get_chat()
                            send_msg[2] = content
                        elif key == 3:  # get board
                            brd = player.game.board.get_board()
                            if last_board != brd:
                                last_board = brd
                                send_msg[3] = brd
                        elif key == 4:  # get score
                            scores = player.game.get_player_scores()
                            send_msg[4] = scores
                            
                        elif key == 5:  # get round
                            rnd = player.game.round_count
                            send_msg[5] = rnd
                        elif key == 6:  # get word
                            word = player.game.round.word
                            send_msg[6] = word
                        elif key == 7:  # get skips
                            skips = player.game.round.skips
                            send_msg[7] = skips
                        elif key == 8:  # update board
                            if player.game.round.player_drawing == player:
                                x, y, color = data['8'][:3]
                                player.game.update_board(x, y, color)
                        elif key == 9:  # get round time
                            t = player.game.round.time
                            send_msg[9] = t
                        elif key == 10:  # clear board
                            player.game.board.clear()
                        elif key == 11:
                            send_msg[11] = player.game.round.player_drawing == player
                        elif key == 12:
                            send_msg[12] = player.game.end_round()
                            
                        
                send_msg = json.dumps(send_msg).encode()
                len_msg = struct.pack('>I', len(send_msg))
                conn.sendall(len_msg + send_msg)
            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()}:", e)
                break
        
        if player.game:
            player.game.player_disconnected(player)

        if player in self.connection_queue:
            self.connection_queue.remove(player)
        try:
            self.player_queue.remove(player.name)
            self.player_ready[:-1] 
        except:
            pass
        print(F"[DISCONNECT] {player.name} DISCONNECTED")
        conn.close() 

if __name__ == "__main__":
    s = Server()
    thread = threading.Thread(target=s.create_new_connection_thread)
    thread.start()
    thread.join()