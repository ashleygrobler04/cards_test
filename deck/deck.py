import random
from . import card

class Deck:
    def __init__(self,cards:list):
        self.cards=cards
        self.index=0

    def randomize(self):
        random.shuffle(self.cards)

    def provide_card(self,player):
        if len(self.cards)>0:
            player.hand.append(self.cards.pop(0))
        else:
            print("No more cards in the deck.")

snakes=[card.Snake() for s in range(5)]
dragons=[card.Dragon() for d in range(5)]
humans=[card.Human() for h in range(5)]
all_cards=snakes+humans+dragons
usable_deck=Deck(all_cards)
usable_deck.randomize()
