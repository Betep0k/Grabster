

class GlobalState:

    # todo: добавить многопоточные блокировки

    def __init__(self):
        # todo: если указан файл со стейтом, загрузить из него
        self.state = {
            'services': []
        }

    def add_service_state(self, state):
        self.state['services'].append(state)

    def is_host_presented(self, ip, port):
        # or return False
        return True
