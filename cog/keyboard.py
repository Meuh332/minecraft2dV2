class Keyboard:
    def __init__(self):
        self.keys = []

    def pressed(self, key):
        for pressed_key in self.keys:
            if key in pressed_key:
                return True
        return False

    def press(self, key, unicode):
        if not [key, unicode] in self.keys:
            self.keys.append([key, unicode])

    def release(self, key):
        for pressed_key in self.keys:
            if key in pressed_key:
                self.keys.remove(pressed_key)

    def reset(self):
        self.keys = []

    def set(self, keys):
        self.keys = keys
