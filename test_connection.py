import socket
import json
import time as t

class Network:
    def __init__(self, name):
        """network connection client to server

        Args:
            name (str): new user name
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # задаем параметры сокета
        self.server = "192.168.1.104" # адрес подключения
        self.port = 5555 # порт подключения
        self.addr = (self.server, self.port) # кортеж адрес порт
        self.name = name # имя нового пользователя 
        self.conn_to_server() # при создании обьекта сразу делаем подключение

    def conn_to_server(self):
        """try connection to server
        """
        try:
            self.client.connect(self.addr) # выполняем подключение к серверу
            self.client.sendall(self.name.encode()) # отправляем закодированное имя нового пользователя
            return json.loads(self.client.recv(2048)) # смотрим, получаем ли мы подтверждение ("1") что сервер работает
        except Exception as e:
            self.disconnect(e) # если чтол то пошло не так, закрываем сокет

    def send(self, data):
        """send data to server in JSON format,
            return data from server requests

        Args:
            data (dict): {str: value}

        Returns:
            dict (json): {str: value}
        """

        try:
            self.client.send(json.dumps(data).encode()) # кодируем и отправляем данные на сокет

            d = "" # stage для данных, если они не пройдут за раз будут добавляться тут
            while True:
                last = self.client.recv(1024).decode() # ожидаем и декодируем полученные данные
                d += last # фрагменты полученных данных закидываем в срейдж
                try:
                    if d.count(".") == 1: # если фрегмент данных имеет точку (при отправлении данных последний симвод добавлен как точка) то завершить цикл получени данных
                        break
                except:
                    pass
            
            # убираем вручную созданный влаг
            try:
                if d[-1] == ".":
                    d = d[:-1]
            except:
                pass
 
            keys = [key for key in data.keys()] # создаем список ключей
            return json.loads(d)[str(keys[0])] # декодируем данные из джейсон и позвпращаем из строки данные по списку ключей
        except socket.error as e:
            self.disconnect(e)

    def disconnect(self, msg):
        print("[EXCEPTION] Disconnected from server:", msg)
        self.client.close()


# Example usage
n = Network('Haelgi')
print(n.send({-1: []}))
n2 = Network('2222ck')
print(n2.send({-1: []}))
