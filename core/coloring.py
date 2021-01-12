

class Coloring:

    def __init__(self, settings):
        self.settings = settings

        if self.settings['COLORS']:
            # COLORS
            self.BLUE = "\033[0;34m"
            self.GREEN = "\033[0;32m"
            self.RED = "\033[0;31m"
            self.CYAN = "\033[0;36m"
            self.MAGENTA = "\033[0;35m"
            self.ORANGE = "\033[38;5;202m"
            # TEXT STYLE
            self.BOLD = "\033[1m"
            # RESET
            self.RESET = "\033[0;0m"
        else:
            # COLORS
            self.BLUE = ""
            self.GREEN = ""
            self.RED = ""
            self.CYAN = ""
            self.MAGENTA = ""
            self.ORANGE = ""
            # TEXT STYLE
            self.BOLD = ""
            # RESET
            self.RESET = ""
