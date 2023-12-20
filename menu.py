import speech
import pygame


class menu_item:
    def __init__(self, text: str, clickable: bool = True, name: str = ""):
        """Text param is what you want the item to speak. Clickable param is what you use if you want a user to click the menu item or not. True makes it clickable and false doesn't. Name param is what is going to be returned."""
        self.text = text
        self.clickable = clickable
        self.name = name


class Slider(menu_item):
    def __init__(self, text, min_value, max_value, callback):
        """self.value can not be larger than max_value and self.value can't be less than min_value. Callback is the function you want to execute when the arrow keys are pressed."""
        super().__init__(text, False, "")
        self.value = 0
        self.min_value = min_value
        self.max_value = max_value
        self.callback = callback

    def increase_value(self):
        if self.value < self.max_value:
            self.value += 1
            self.callback(self.value)

    def decrease_value(self):
        if self.value > self.min_value:
            self.value -= 1
            self.callback(self.value)


class Menu:
    def __init__(self, items: list):
        self.items = items
        self.index = 0

    def add_item(self, item):
        self.items.append(item)

    def cycle(self, dir: int):
        """use -1 for cycling up and 1 for cycling down"""
        if dir == 1 and self.index < len(self.items)-1:
            self.index += 1
        elif dir == -1 and self.index > 0:
            self.index -= 1
        speech.speak(self.items[self.index].text)

    def show(self, title: str):
        """The title is what you want spoken as soon as the menu shows."""
        speech.speak(title)
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        self.cycle(-1)
                    elif e.key == pygame.K_DOWN:
                        self.cycle(1)
                    elif e.key == pygame.K_ESCAPE:
                        self.close()
                    elif e.key == pygame.K_LEFT and isinstance(self.items[self.index], Slider):
                        self.items[self.index].decrease_value()
                    elif e.key == pygame.K_RIGHT and isinstance(self.items[self.index], Slider):
                        self.items[self.index].increase_value()
                    elif e.key == pygame.K_RETURN and self.items[self.index].clickable:
                        return self.items[self.index].name

    def close(self):
        return False

    def refresh(self, items):
        self.items = items
        self.add_item(menu_item("back", True, "back"))
