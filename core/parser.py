import requests
from core.coloring import Coloring
from core.constants import MAX_PRIORITIES


class Parser:

    def __init__(self, modules, settings):
        self.modules = modules
        self.settings = settings
        self.state = {}
        self.coloring = Coloring(settings)

    def strip_end(self, text, char='\n'):
        if not text.endswith(char + char):
            return text
        return self.strip_end(text[:len(text)-1])

    def parse(self, host, port, vhost, args, global_variables, vhosts, output_queue, parser_queue, global_state, recursion):
        state = {}
        output = ''
        headers = {
            'User-Agent': self.settings['USER-AGENT']
        }
        try:
            # Trying access to page using HTTP
            # If attempt is failed, then trying HTTPS
            proto = 'http'
            http_exception = False

            if vhost is not None:
                headers['Host'] = vhost

            try:
                response = requests.get('http://%s:%s/' % (host, port), verify=False, timeout=self.settings['TIMEOUT'],
                                        proxies=self.settings['PROXIES'], allow_redirects=False, headers=headers)
                response.encoding = 'utf-8'
            except:
                http_exception = True
                response = None

            if http_exception or response.status_code == 400:
                proto = 'https'
                response = requests.get('https://%s:%s/' % (host, port), verify=False, timeout=self.settings['TIMEOUT'],
                                        proxies=self.settings['PROXIES'], allow_redirects=False, headers=headers)
                response.encoding = 'utf-8'

            if vhost:
                output += f'%s://%s:%s {self.coloring.CYAN}(Host: %s){self.coloring.RESET}\n' % (proto, host, port, vhost)
            else:
                output += '%s://%s:%s\n' % (proto, host, port)

            state['service'] = {
                'proto': proto,
                'host': host,
                'port': port,
                'vhost': vhost,
            }

            state['response'] = response

            for priority in range(0, MAX_PRIORITIES):
                for module_name, module in self.modules['peri-modules'].items():
                    if module['priority'] == priority:
                        state_copy = dict(state)
                        try:
                            module_output, module_state = module['obj'].run_peri_module(state_copy, self.settings, self.modules, self.coloring, recursion)
                            state[module_name] = module_state
                            if module_output:
                                if type(module_output) is str:
                                    output += f"{self.coloring.MAGENTA}%s:{self.coloring.RESET}\n%s\n" % (module['banner'], module_output)
                                    output = self.strip_end(output)
                        except Exception as e:
                            pass
                        # state['modules'][module_name] =

            # Отправляем полученный объект в global_state
            del state['response']  # потому что он слишком здоровый
            global_state.add_service_state(state)

            output += '\n----------------------------------\n\n'
        except Exception as e:
            if args.debug is True:
                print(e)
                pass
            pass
        return output