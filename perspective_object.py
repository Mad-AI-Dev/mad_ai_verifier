from collections import defaultdict

class PerspectiveObject(defaultdict):
    def __init__(self):
        super().__init__(list)
