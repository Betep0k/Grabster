from core.coloring import Coloring


class IntroMessage:

    def __init__(self, settings, modules):
        self.settings = settings
        self.modules = modules
        self.coloring = Coloring(self.settings)
        self.VERSION = '0.0.1'
        self.GITHUB = '...'

    def _current_config(self):
        return './settings.py'

    def print(self):
        print('===============================================================')
        print(f' {self.coloring.CYAN}Grabster{self.coloring.RESET}\t\tv{self.VERSION}')
        print(f' {self.coloring.BLUE}[*] Github:\t\t{self.coloring.RESET} ...')
        print('===============================================================')
        print(f' {self.coloring.BLUE}[+] Config:{self.coloring.RESET}\t\t{self._current_config()}')
        print('===============================================================')