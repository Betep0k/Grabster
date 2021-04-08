import functools


@functools.total_ordering
class OutputJob:

    def __init__(self, priority, text):
        self.priority = priority
        self.text = text
        return

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented


@functools.total_ordering
class ScreenshotJob:

    def __init__(self, priority, proto, ip, port, vhost=''):
        self.priority = priority
        self.proto = proto
        self.ip = ip
        self.port = port
        self.vhost = vhost
        return

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented


@functools.total_ordering
class ParserJob:

    def __init__(self, priority, host, port, vhost, args, vhosts, global_variables, modules, settings, output_queue, parser_queue, global_state, recursion):
        self.priority = priority
        self.host = host
        self.port = port
        self.vhost = vhost
        self.args = args
        self.vhosts = vhosts
        self.global_variables = global_variables
        self.modules = modules
        self.settings = settings
        self.output_queue = output_queue
        self.parser_queue = parser_queue
        self.global_state = global_state
        self.recursion = recursion
        return

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            return NotImplemented
