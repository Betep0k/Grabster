from .src import SSLAnalyzer


class Main:
    MODULE_SETTINGS = {
        'peri-module': {
            'is_enabled': True,
            'priority': 1,
            'banner': "SSL"
        },
        'post-module': {
            'is_enabled': False
        }
    }

    def __init__(self, args):
        # init
        pass

    def run_peri_module(self, local_state, settings, modules, coloring):
        ssl_analyzer = SSLAnalyzer(settings, modules, coloring)
        module_output = ssl_analyzer.get_domains_from_cert(local_state['service'])
        return module_output, module_output

    def run_post_module(self, global_state, settings, modules, coloring):
        return None

    def check(self):
        return True, None
