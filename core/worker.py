import functools
import sys
import queue
from tqdm import tqdm
import threading
import os
import json
from importlib.machinery import SourceFileLoader
import importlib
from pydoc import locate

from core.intro_message import IntroMessage
from core.parser import Parser
from core.queue_jobs import OutputJob, ParserJob
from core.coloring import Coloring
from core.load_modules import load_modules
from core.constants import MAX_PRIORITIES
from core.global_state import GlobalState
from core.recursion import Recursion


class Worker:

    def __init__(self, args, settings):
        self.args = args
        self.settings = settings
        self.modules = {}
        self.coloring = Coloring(self.settings)
        self.vhosts = []
        self.services = []
        self.total_services = 0

    @staticmethod
    def process_output_job(q, global_variables, description, coloring, only_taskbar=False):
        current_step = 0
        with tqdm(total=global_variables['total_services']) as pbar:
            pbar.set_description_str(description)
            while True:
                output = q.get()
                pbar.update(1)
                current_step += 1
                if only_taskbar or output.text == '':
                    pass
                else:
                    n = f'{coloring.ORANGE}[{current_step}/{global_variables["total_services"]}]{coloring.RESET} '
                    pbar.write(n + output.text)
                q.task_done()

    @staticmethod
    def process_parser_job(q, output_queue):
        while True:
            current_job = q.get()
            parser = Parser(current_job.modules, current_job.settings)
            output = parser.parse(current_job.host, current_job.port, current_job.vhost, current_job.args, current_job.global_variables,
                                  current_job.vhosts, current_job.output_queue, current_job.parser_queue, current_job.global_state, current_job.recursion)
            output_queue.put(OutputJob(0, output))
            q.task_done()

    def parse_input(self):
        if self.args.vhosts_filename is not None:
            fd = open(self.args.vhosts_filename)
            data = fd.read()
            self.vhosts = data.split('\n')
            self.vhosts = list(filter(None, self.vhosts))

        data = ''
        if self.args.filename is not None:
            fd = open(self.args.filename)
            data = fd.read()
        else:
            for service in sys.stdin:
                data += service
                if service == '\n':
                    break

        self.services = list(filter(None, data.split('\n')))
        self.total_services = len(self.services)

    def start(self):

        # Parsing input files
        self.parse_input()

        # Initializing queues
        screenshot_queue = queue.PriorityQueue()
        parser_queue = queue.PriorityQueue()
        output_queue = queue.PriorityQueue()

        # Initializing global state objects
        global_state = GlobalState()

        recursion = Recursion()

        intro_message = IntroMessage(self.settings, self.modules)
        intro_message.print()

        self.modules = load_modules(self.coloring, self.args)

        print('===============================================================')
        print(f'\t\t{self.coloring.ORANGE}   Analysis of services{self.coloring.RESET}')
        print('===============================================================\n\n')

        # todo:
        # Надо сделать так, чтобы модули могут добавлять новые сервисы в очередь
        # И воркер после окончания очередного прохода цеплялся за новую очередь 
        # И начинал новый обход
        # При этом нужно контролировать уровень рекурсии
        # И вообще, чтобы в настройках можно было бы задать явно уровень рекурсии 

        # Pushing parser jobs (services) to queue
        current_service_id = 0
        global_variables = {
            'total_services': 0
        }
        for service in self.services:
            current_service_id += 1
            if service == '':
                continue
            if ':' in service:
                (host, port) = service.split(':')
                # todo: total_services похоже не используется
                # todo: глобальные стейты и локер тоже не нужны
                parser_queue.put(ParserJob(current_service_id, host, port, None, self.args, self.vhosts,
                                           global_variables, self.modules, self.settings, output_queue, parser_queue,
                                           global_state, recursion))
                global_variables['total_services'] += 1
            else:
                host = service
                global_variables['total_services'] += 2
                for port in [80, 443]:
                    parser_queue.put(ParserJob(current_service_id, host, port, None, self.args, self.vhosts,
                                               global_variables, self.modules, self.settings, output_queue, parser_queue,
                                               global_state, recursion))

        # Starting output thread
        w = threading.Thread(target=self.process_output_job, args=(output_queue, global_variables, 'Parsing services',
                                                                   self.coloring, False,))
        w.setDaemon(True)
        w.start()

        # Starting parser threads
        if self.settings['DEBUG']:
            w = threading.Thread(target=self.process_parser_job, args=(parser_queue, output_queue))
            w.setDaemon(True)
            w.start()
        else:
            for i in range(0, self.settings['THREADS']):
                w = threading.Thread(target=self.process_parser_job, args=(parser_queue, output_queue))
                w.setDaemon(True)
                w.start()

        parser_queue.join()
        output_queue.join()

        # todo: надо объединить оба цикла

        for recursion_level in range(0, recursion.recursion_max_level):

            # if empty - stop
            if len(recursion.recursive_services[recursion_level]) == 0:
                break
            recursion.increment_recursion_level()

            print('\n\n\n===============================================================')
            print(f'\t\t{self.coloring.ORANGE}    Recursion Level %d{self.coloring.RESET}' % recursion_level)
            print('===============================================================\n\n')
            parser_queue = queue.PriorityQueue()
            output_queue = queue.PriorityQueue()
            current_service_id = 0
            global_variables = {
                'total_services': 0
            }
            for service in recursion.recursive_services[recursion_level]:
                current_service_id += 1
                # todo: clean queue ???
                parser_queue.put(ParserJob(current_service_id, service['host'], service['port'], service['vhost'], self.args, self.vhosts,
                                           global_variables, self.modules, self.settings, output_queue, parser_queue,
                                           global_state, recursion))
                global_variables['total_services'] += 1

            # Starting output thread
            w = threading.Thread(target=self.process_output_job, args=(output_queue, global_variables, 'Parsing services',
                                                                       self.coloring, False,))
            w.setDaemon(True)
            w.start()

            # Starting parser threads
            if self.settings['DEBUG']:
                w = threading.Thread(target=self.process_parser_job, args=(parser_queue, output_queue))
                w.setDaemon(True)
                w.start()
            else:
                for i in range(0, self.settings['THREADS']):
                    w = threading.Thread(target=self.process_parser_job, args=(parser_queue, output_queue))
                    w.setDaemon(True)
                    w.start()

            parser_queue.join()
            output_queue.join()
            # global_state.increment_recursion_level()
            # по логике здесь надо запускать рекурсию
            # надо придумать, как получать список новых целей для следующего этапа рекурсии
            # возможно есть смысл даже хранить их отдельно для каждого этапа

        print('\n\n\n===============================================================')
        print(f'\t\t\t{self.coloring.ORANGE}Post Modules{self.coloring.RESET}')
        print('===============================================================\n\n')

        # todo: надо переименовать RINGS в Priorities
        for priority in range(0, MAX_PRIORITIES):
            for module_name, module in self.modules['post-modules'].items():
                if module['priority'] == priority:
                    try:
                        print('%s: ' % module_name)
                        module['obj'].run_post_module(global_state, self.settings, self.modules, self.coloring)
                    except Exception as e:
                        print(e)
                        pass
