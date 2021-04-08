

class Recursion:

    # todo: добавить многопоточные блокировки

    def __init__(self):
        self.current_recursion_level = 0
        self.recursion_max_level = 3 # 0 == disabled
        self.recursive_services = {
            0: []
        }

    def add_service_for_parsing(self, proto, host, port, vhost):
        self.recursive_services[self.current_recursion_level].append({
            'proto': proto,
            'host': host,
            'port': port,
            'vhost': vhost,
        })

    def increment_recursion_level(self):
        self.current_recursion_level += 1
        self.recursive_services[self.current_recursion_level] = []
