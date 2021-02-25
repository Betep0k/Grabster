from .src import Example


class Main:
    MODULE_SETTINGS = {
        'peri-module': {
            'is_enabled': False
        },
        'post-module': {
            'is_enabled': False,
            'priority': 1,
            'banner': "Template"
        }
    }

    def __init__(self, args):
        # init
        pass

    def run_peri_module(self, local_state, settings, modules, coloring):
        return None, None

    def run_post_module(self, global_state, settings, modules, coloring):
        return None

    def check(self):
        return True, None

    def args_parser(self):
        # todo: add functionality for custom args parsing
        pass