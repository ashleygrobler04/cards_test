import deck
import random
import pygame
import speech
import menu
import state
import statemachine
import sys
from sound_lib import output
from sound_lib import stream
pygame.init()
dsp = pygame.display.set_mode((500, 500))  # The display
pygame.display.set_caption("Card batler prototype")
running = True
o = output.Output()
snd = stream.FileStream(file="background.mp3")
clock = pygame.time.Clock()


def init_track():
    snd.play()
    snd.looping = True


def notify(v):
    snd.volume = v
    speech.speak(f" Music volume: {v}")


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = [deck.card.player_card()]

    def loop(self):
        global running
        for c in self.hand:
            if c.health <= 0:
                if c.type == "Player":
                    speech.speak(f" {self.name} Died.")
                    sm.to("main menu")
                else:
                    self.hand.remove(c)


class Game:
    def __init__(self, players: list):
        self.players = players
        self.turn = random.randint(0, 1)

    def evaluate(self):
        global running
        sm.run()
        if self.turn == 0:
            self.players[0].loop()
            self.turn = 1
        elif self.turn == 1:
            self.players[1].loop()
            self.turn = 0


me = Player("Ashley")
jane = Player("Jane")

g = Game([me, jane])

c = 0
for c in range(5):
    deck.deck.usable_deck.provide_card(me)
    deck.deck.usable_deck.provide_card(jane)

m = menu.Menu([menu.menu_item("attack", True, "Attack"),
              menu.menu_item("View your hand", True, "View your hand"), menu.Slider("Change music volume", 0, 10, notify), menu.menu_item("exit", True, "exit")])
jhm = menu.Menu([menu.menu_item(b.type, True, b.type)
                for b in g.players[1].hand])  # Jane hand menu
jhm.add_item(menu.menu_item("back", True, "back"))
yhm = menu.Menu([menu.menu_item(a.type, True, a.type)
                for a in g.players[0].hand])  # Your hand menu
yhm.add_item(menu.menu_item("back", True, "back"))
am = menu.Menu([menu.menu_item(card.type, True, card.type)
               for card in g.players[0].hand])
am.add_item(menu.menu_item("back", True, "back"))


class main_menu_state(state.state):
    def enter(self):
        speech.speak("Welcome!")

    def update(self):
        global running
        res = m.show("Main menu")
        if res == "Attack":
            if g.turn == 0:
                sm.to("attack")
            elif g.turn == 1:
                sm.to("jane attack")
        elif res == "View your hand":
            sm.to("your hand")
        elif res == "exit":
            sm.to("game over")

    def exit(self):
        pass


class your_hand_menu_state(state.state):
    def enter(self):
        speech.speak("Viewing your hand.")
        yhm.refresh([menu.menu_item(h.type, True, h.type)
                    for h in g.players[0].hand])

    def update(self):
        global running
        r2 = yhm.show("Your hand menu")
        if not r2 == "back":
            speech.speak(
                f"Description: {g.players[0].hand[yhm.index].description}, health: {g.players[0].hand[yhm.index].health} out of {g.players[0].hand[yhm.index].max_health}, deels {g.players[0].hand[yhm.index].attack} damage.")
        else:
            sm.to("main menu")

    def exit(self):
        pass


class attack_state_menu(state.state):
    def enter(self):
        speech.speak(f"It is {g.players[g.turn].name}'s turn")
        jhm.refresh([menu.menu_item(jcards.type, True, jcards.type)
                    for jcards in g.players[1].hand])
        am.refresh([menu.menu_item(ramcard.type, True, ramcard.type)
                   for ramcard in g.players[0].hand])

    def exit(self):
        pass

    def update(self):
        global running
        r3 = jhm.show("Attack which card?")
        if not r3 == "back":
            my_target_card = g.players[1].hand[jhm.index]
            ram = am.show("Choose a card to attack with")
            chosen_card_index = am.index
            if not ram == "back":
                my_chosen_card = g.players[0].hand[chosen_card_index]
                speech.speak(
                    f"You will use your {my_chosen_card.type} card to attack Jane's {my_target_card.type} card")
                my_chosen_card.perform_attack(my_target_card)
                g.turn = 1  # Switch to Jane's turn
                sm.to("jane attack")
            else:
                # ram = am.show("Choose a card to attack with")
                sm.to("main menu")
        else:
            sm.to("main menu")


class jane_attack_state(state.state):
    def enter(self):
        speech.speak(f"It is {g.players[g.turn].name}'s turn")

    def exit(self):
        pass

    def update(self):
        global running
        chosen_card = g.players[1].hand[random.randint(
            0, len(g.players[1].hand)-1)]
        tcard = g.players[0].hand[random.randint(
            0, len(g.players[0].hand)-1)]  # target card
        speech.speak(
            f"Jane is using {chosen_card.type} card to attack your {tcard.type} card.")
        chosen_card.perform_attack(tcard)
        g.turn = 0  # Switch back to the player's turn
        sm.to("attack")


class game_over_state(state.state):
    def enter(self):
        global running
        speech.speak("Game over!")
        global running
        snd.stop()
        pygame.quit()
        running = False
        sys.exit()

    def exit(self):
        pass

    def update(self):
        pass


sm = statemachine.state_machine()  # The state machine
mm_state = main_menu_state("main menu")  # the main menu
your_hand = your_hand_menu_state("your hand")
ja_state = jane_attack_state("jane attack")  # jane's attack state
attack_state = attack_state_menu("attack")
go_state = game_over_state("game over")  # game over state
sm.add_state(mm_state)
sm.add_state(your_hand)
sm.add_state(attack_state)
sm.add_state(ja_state)
sm.add_state(go_state)
sm.to("main menu")


def loop():
    global running
    while running:
        pygame.display.update()
        g.evaluate()
        clock.tick(60)


init_track()
loop()
