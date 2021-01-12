from .src import BasicsCollector


class Main:
    MODULE_SETTINGS = {
        'peri-module': {
            'is_enabled': True,
            'priority': 0,
            'banner': "Basics"
        },
        'post-module': {
            'is_enabled': False
        }
    }

    def __init__(self):
        # init
        pass

    def run_peri_module(self, local_state, settings, modules, coloring):
        basics_collector = BasicsCollector(settings, modules, coloring)
        module_output, module_state = basics_collector.get_basics(local_state['response'])
        return module_output, module_state

    def run_post_module(self, global_state, settings, modules, coloring):
        return None


    def check(self):
        return True, None
