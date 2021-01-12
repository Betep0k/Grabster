from settings import settings
import argparse


class ArgsParser:

    def parse(self):
        parser = argparse.ArgumentParser(description='Smart Web Grabber - Tool that helps you to analyze big count of '
                                                     'different web services.')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--file', '-f', action='store', dest='filename',
                           help='Path to file with list of web services. '
                                'File format: IP:PORT\\n')
        group.add_argument('--stdin', '-s', action='store_true', help='If stdin flag is set, parser will be waited for '
                                                                      'input from stdin. Stdin format: IP:PORT\\n')
        # todo: --nmap-file ...
        # todo: --masscan-file ...
        parser.add_argument('--debug', action='store_true', dest='debug', help='Enabling debug mode with '
                                                                               'printing exceptions')
        # todo: --threads 10 / default 10
        # todo: --real-time / one thread, real time output, good for debug / может быть есть смысл объединить это с дебагом
        # todo: --full-output / default, каждый поток пуляет информацию хосту по факту завершения его скана в консоль
        # todo: --progress-only / только рисует прогрессбар / нужно чекать, что выставлены правила атпута в файл, иначе это бесполезно
        # todo: --silent / totally silent, without any output / нужно чекать, что выставлены правила атпута в файл, иначе это бесполезно
        # ----- parsing rules -----
        parser.add_argument('--ignore-title', action='store', dest='ignore_title',
                            help='All web-services with this title'
                                 ' will be skipped')
        parser.add_argument('--screenshots', action='store_true', dest='get_screenshots',
                            help='Script will take screenshot'
                                 ' of every page')
        parser.add_argument('--vhosts', '-vh', action='store', dest='vhosts_filename', help='File with Virtual Hosts'
                                                                                            ' for checking')
        parser.add_argument('--proxy', action='store', dest='proxy', help='Proxy Settings')
        # ----- output to files -----
        # todo: --output-txt
        # todo: --output-html
        # todo: --output-xml

        args = parser.parse_args()

        settings['DEBUG'] = args.debug

        if args.proxy is not None:
            proto = args.proxy.split('://')[0]
            settings['PROXIES'] = {
                proto: args.proxy
            }

        return args, settings
