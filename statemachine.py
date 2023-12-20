class state_machine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def to(self, name):
        """Switch to an available state in the state machine."""
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[name]
        self.current_state.enter()

    def run(self):
        self.current_state.update()
