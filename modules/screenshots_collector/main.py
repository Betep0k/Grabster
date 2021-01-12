from .src import ScreenshotCollector


class Main:
    MODULE_SETTINGS = {
        'peri-module': {
            'is_enabled': False
        },
        'post-module': {
            'is_enabled': True,
            'priority': 1,
            'banner': "Screenshot Collector"
        }
    }

    def __init__(self):
        # init
        pass

    def run_peri_module(self, local_state, settings, modules, coloring):
        return None, None

    def run_post_module(self, global_state, settings, modules, coloring):
        screenshot_collector = ScreenshotCollector(settings, modules, coloring)
        screenshot_collector.collect_screenshots(global_state)
        return None

    def check(self):
        return True, None
