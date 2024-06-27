import time as t
from _thread import *
from chat import Chat


class Round(object):
    def __init__(self, word, player_drawing, game):
        """
        init object
        :param word: str
        :param player_drawing: Player
        :param players: Player[]
        """
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.players_skipped = []
        self.skips = 0
        self.time = 75
        self.game = game
        self.player_scores = {player: 0 for player in self.game.players}
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())

    def skip(self, player):
        """
        Returns true if round skipped threshold met
        :return: bool
        """
        if player not in self.players_skipped:
            self.players_skipped.append(player)
            self.skips += 1
            self.chat.update_chat(f"Гравець проголосував за пропуск ({self.skips}/{len(self.game.players) -2})")
            if self.skips >= len(self.game.players) - 2:
                return True

        return False

    def get_scores(self):
        """
        :returns all the player scores
        """
        return self.player_scores

    def get_score(self, player):
        """
        gets a specific players scores
        :param player: Player
        :return: int
        """
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception("Player not in score list")

    def time_thread(self):
        """
        Runs in thread to keep track of time
        :return: None
        """
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round("Time is up")

    def guess(self, player, wrd): ################################### 2 # 
        """
        :returns bool if player got guess correct
        :param player: Player
        :param wrd: str
        :return: bool
        """
        correct = wrd.lower() == self.word.lower() # сравниваем напечатанное слово с загаданным
        if correct: # если угадали
            self.player_guessed.append(player) # в список добавили игрока который угадал
            # TODO implement scoring system here
            self.chat.update_chat(f"{player.name} вгадав слово.")# в чат на сервере написали, что игрок угадал
            return True # вернули тру

        self.chat.update_chat(f"{player.name}: {wrd}") # если не угадали, просто опубликовали сообщение пользователя
        return False

    def player_left(self, player):
        """
        removes player that left from scores and list
        :param player: Player
        :return: None
        """
        # might not be able to use player as key in dict
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove(player)

        if player == self.player_drawing:
            self.chat.update_chat("Раунд пропущено, оскільки гравець що малював покинув гру.")
            self.end_round("Гравець що малював покинув гру")

    def end_round(self, msg):
        for player in self.game.players:
            if player in self.player_scores:
                player.update_score(self.player_scores[player])
        self.game.round_ended()
