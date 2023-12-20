from cytolk import tolk


def speak(text: str):
    with tolk.tolk():
        tolk.speak(text)
