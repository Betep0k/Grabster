from .src import Wappalyzer


class Main:
    MODULE_SETTINGS = {
        'peri-module': {
            'is_enabled': True,
            'priority': 1,
            'banner': "Wappalyzer"
        },
        'post-module': {
            'is_enabled': False
        }
    }

    def __init__(self, args):
        # init
        pass

    def run_peri_module(self, local_state, settings, modules, coloring, recursion):
        wappalyzer = Wappalyzer(settings, modules, coloring)
        module_output, module_state = wappalyzer.identification(local_state['service'])
        return module_output, module_state

    def run_post_module(self, global_state, settings, modules, coloring):
        return None

    def check(self):
        return True, None
