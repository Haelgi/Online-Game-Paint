class Chat:
    def __init__(self, r):
        # Инициализация пустого списка для хранения сообщений чата
        self.content = []
        self.round = r

    def update_chat(self, msg):
        # Добавление нового сообщения в чат
        self.content.append(msg)

    def get_chat(self):
        # Возвращение всех сообщений чата
        return self.content

    def __len__(self):
        # Возвращение количества сообщений в чате
        return len(self.content)

    def __str__(self):
        # Объединение всех сообщений в одну строку
        return ''.join(self.content)

    def __repr__(self):
        # Представление объекта, используя метод __str__
        return str(self)
