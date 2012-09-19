
class Scanner:
    def __init__(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        print(lines)
