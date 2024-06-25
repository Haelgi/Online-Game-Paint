import socket
import threading
from player import Player
from game import Game
import json


class Server(object):
    PLAYERS = 3
    player_queue = [] # list of queue with obj of player

    def __init__(self):
        self.connection_queue = [] # list of queue with obj of player 
        # player_queue = [] # list of queue with obj of player
        self.game_id = 0


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

            self.authentication(conn, addr) # авторизируем каждого игрока по отдельности
            print(self.player_queue)


    def authentication(self, conn_socket, addr):
        """authentication user name, 
            add user in queue, 
            crete thread for interactions with user

        Args:
            conn (obj): socket for server and new user <socket.socket fd=452, family=2, type=1, proto=0, laddr=('192.168.1.104', 5555), raddr=('192.168.1.104', 53538)>
            addr (tuple): ip and port new user ('192.168.1.104', 53538)

        Raises:
            Exception: if there is any error, close connection
        """
        try:
            data = conn_socket.recv(1024) # получаем данные с сокета
            name = str(data.decode()) # декодируем с байтов в строку
            self.player_queue.append(name)

            if not name: # проверка если нет данных 
                raise Exception("No name received")

            conn_socket.sendall("1".encode()) # если данные есть кодирует строку "1" байты и отправляем клиенту как подтверждение

            player = Player(addr, name) # создаем на сервере игрока с адресом и  именем полученным от пользователя
            
            self.handle_queue(player) # работа с очередью и создание новой игры
            

            thread = threading.Thread(target=self.player_thread, args=(conn_socket, player)) # создаем новый поток для каздого игкрока (передаем в поток ыщслуе и обьект игрока)
            thread.start() # запуска ем новый поток
        except Exception as e:
            print("[EXCEPTION]", e)
            conn_socket.close()

    def handle_queue(self, player):
        """add obj player in queu list,
            create new game if queu reached the expected quantity

        Args:
            player (obj): new player with unique name and addr
        """
        self.connection_queue.append(player) # добавляем обьект игрока в список очереди

        if len(self.connection_queue) >= self.PLAYERS:  # проверяем, если очередь игроков достигла ожидаемое количество 
            game = Game(self.game_id, self.connection_queue[:]) # создаем обьект игры (передаем копию списка игроков)

            for p in game.players: # для каждого игрока в созданной игре передаем обьект текущей игры
                p.set_game(game)
            
            print(f"[GAME] Game {self.game_id} started...")

            self.game_id += 1  # увеличиваем счетчик игр на один
            self.connection_queue = [] # очищаем очередь игроков
            self.player_queue = [] # очищаем очередь игроков

    def player_thread(self, conn, player):
        """handling interaction between server and player   

        Args:
            conn (obj): connection socket for one player
            player (obj): one player object
        """
        while True: # цикл потока для одного игрока
            try:
                # получение и декодирования данных, если данных нет завершить цикл
                try:
                    data = conn.recv(1024)
                    data = json.loads(data.decode())
                except Exception as e:
                    break


                # переводим ключи значений в словаре из строк в число
                keys = [int(key) for key in data.keys()] # список всех ключей
                send_msg = {key:[] for key in keys} # словарь из ключей с пустім списком
                
                last_board = None

                for key in keys: # проходимся по списку ключей
                    if key == -2:  # get game, returns a list of players
                        send_msg[-2] = self.player_queue

                    if key == -1:  # get game, returns a list of players
                        if player.game:
                            send = {player.get_name():player.get_score() for player in player.game.players} # создаем словарь списка игроков с количеством очков для каждого
                            send_msg[-1] = send # закидываем словарь в словарь для ответа
                        else:
                            send_msg[-1] = [] # если у игрока не назначена игра, шлем пустой список


                    if player.game:
                        if key == 0:  # guess
                            correct = player.game.player_guess(player, data['0'][0])
                            send_msg[0] = correct
                        elif key == 1:
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
                        
                send_msg = json.dumps(send_msg) # шифруем данные для отправки
                conn.sendall(send_msg.encode() + ".".encode()) # отправляем данные по сокету игрока
            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()}:", e)
                break
        
        # если цикл прервался но у игрока есть активная игра , вызываем метод отключения
        if player.game:
            player.game.player_disconnected(player)

        # если цикл прервался но игрок есть в очереди на игру , удаляемся из списка
        if player in self.connection_queue:
            self.connection_queue.remove(player)

        print(F"[DISCONNECT] {player.name} DISCONNECTED")
        conn.close() # закрываем сокет


if __name__ == "__main__":
    s = Server()
    thread = threading.Thread(target=s.create_new_connection_thread)
    thread.start()
    thread.join()