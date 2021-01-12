#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib3

from core.args_parser import ArgsParser
from core.worker import Worker

urllib3.disable_warnings()


def main():
    # Loading settings from file, parsing command arguments and updating settings
    args_parser = ArgsParser()
    args, settings = args_parser.parse()

    # Starting main worker
    worker = Worker(args, settings)
    worker.start()


if __name__ == '__main__':
    main()
