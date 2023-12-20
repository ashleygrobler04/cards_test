class BaseCard:
    def __init__(self, type: str, attack: int, max_health: int, description: str):
        """Initialize a base card with attack and health."""
        self.type = type
        self.attack = attack
        self.max_health = max_health
        self.health = self.max_health
        self.description = description

    def perform_attack(self, target_card):
        """Attacks another card."""
        target_card.health -= self.attack


class Human(BaseCard):
    def __init__(self):
        super().__init__("Human", 3, 12,
                         "A person with black eyes and antenna like shapes sticking out from the top of it's head.")


class Dragon(BaseCard):
    def __init__(self):
        super().__init__("Dragon", 4, 20, "A cute blue dragon.")


class Snake(BaseCard):
    def __init__(self):
        super().__init__("Snake", 6, 4, "A huge python like animal with 2 batteries at it's sides.")


class player_card(BaseCard):
    def __init__(self):
        super().__init__("Player", 1, 15,
                         "You, the player. Ensure your health doesn't get equal to or below 0")
