

class GlobalState:

    # todo: добавить многопоточные блокировки

    def __init__(self):
        # todo: если указан файл со стейтом, загрузить из него
        self.state = {
            'services': []
        }

    def add_service_state(self, state):
        self.state['services'].append(state)
