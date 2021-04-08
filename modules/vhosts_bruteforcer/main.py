from .src import VHostBruteforcer


class Main:
    MODULE_SETTINGS = {
        'peri-module': {
            'is_enabled': True,
            'priority': 1,
            'banner': "VHosts Bruteforcer"
        },
        'post-module': {
            'is_enabled': False
        }
    }

    def __init__(self, args):
        try:
            vhosts_filename = args.vhosts_filename
            fd = open(vhosts_filename)
            data = fd.read()
            self.vhosts = list(filter(None, data.split('\n')))
        except Exception as e:
            print(e)
        # init

    def run_peri_module(self, local_state, settings, modules, coloring, recursion):
        # we work only with primary host
        if local_state['service']['vhost'] is not None:
            return None, None
        vhost_bruteforcer = VHostBruteforcer(settings, modules, coloring, recursion)
        module_output = vhost_bruteforcer.brute_vhosts(local_state['service'], self.vhosts)
        return module_output, module_output

    def run_post_module(self, global_state, settings, modules, coloring):
        return None

    def check(self):
        return True, None
