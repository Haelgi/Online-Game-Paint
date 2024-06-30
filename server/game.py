from board import Board
from round import Round
import random


class Game(object):
    def __init__(self, id, players):
        """init game and start round

        Args:
            id (int): id namber of created game 
            players (list): list of obj players [P(1), P(2), P(3)]
        """

        self.id = id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 0
        self.start_new_round()

    def start_new_round(self):
        """Starts a new round with a new word
        """
        try:

            if self.player_draw_ind > len(self.players)-1:
                self.player_draw_ind = 0

            self.round = Round(self.get_word(), self.players[self.player_draw_ind], self)

            self.round_count += 1

            if self.round_count >= len(self.players)*2+1:
                self.round_ended()
                self.end_game()

            self.player_draw_ind += 1

        except Exception as e:
            self.end_game()

    def player_guess(self, player, guess): 
        """
        Makes the player guess the word
        :param player: Player
        :param guess: str
        :return: bool
        """
        self.round.guess(player, guess)

    def end_round(self):
        new_round_guessed = len(self.round.players_skipped)+len(self.round.player_guessed) == len(self.players)-1
  
        if new_round_guessed :
            self.round_ended()

       
    def player_disconnected(self, player):
        """
        Call to clean up objects when player disconnects
        :param player: Player
        :raises: Exception()
        """

        if player in self.players:
            self.players.remove(player)
            self.round.player_left(player)
            self.round.chat.update_chat(f"Гравець {player.get_name()} покинув гру.")
        else:
            raise Exception("Player not in game")

        if len(self.players) < 2:
            print('72 game')
            self.end_game()

    def get_player_scores(self):
        """
        give a dict of player scores.
        :return: dict
        """
        scores = {player.name:player.get_score() for player in self.players}
        return scores

    def skip(self, player):
        """
        Increments the round skips, if skips are greater than
        threshold, starts new round.
        :return: None
        """
        if self.round:
            new_round_skip = self.round.skip(player)
            
            if new_round_skip :
                self.round.chat.update_chat(f"Раунд був пропущенний.")
                self.round_ended()
                return True
            return False
        else:
            raise Exception("No round started yet!")

    def round_ended(self):
        """
        If the round ends call thiss
        :return: None
        """
        self.round.chat.update_chat(f"Раунд {self.round_count} закінчився.")
        self.start_new_round()
        self.board.clear()
        

    def update_board(self, x, y, color):
        """
        calls update method on board.
        :param x: int
        :param y: int
        :param color: 0-8
        :return: None
        """
        if not self.board:
            raise Exception("No board created")
        self.board.update(x,y,color)

    def end_game(self):
        """
        ends the game
        :return:
        """
        print(f"[GAME] Game {self.id} ended")
        for player in self.players:
            player.game = None

    def get_word(self):
        """
        gives a word that has not yet been used
        :return: str
        """
        with open("server/words.txt", "r", encoding="utf-8") as f:
            words = []

            for line in f:
                wrd = line.strip()
                if wrd not in self.words_used:
                    words.append(wrd)

        wrd = random.choice(words)
        self.words_used.add(wrd)

        return wrd 
