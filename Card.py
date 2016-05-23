import random

class Card(object):

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "J", "Q", "K"]

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return Card.rank_names[self.rank] + ' ' + Card.suit_names[self.suit]


class Deck(object):

    def __init__(self):
        '''
        Create A deck of cards
        '''
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        string = ''
        for card in self.cards:
            string += str(card) + ' '
        return string

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def get_card(self, i=-1):
        return self.cards.pop(i)

    def shuffle(self):
        random.shuffle(self.cards)

    def sort(self):
        self.cards.sort()

    def move_cards(self, hand: object, num: object) -> object:
        for i in range(num):
            hand.add_card(self.get_card())


class Hand(Deck):
    def __init__(self, label=''):
        self.cards = []
        self.label = label

