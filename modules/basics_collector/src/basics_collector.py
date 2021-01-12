import re
from core.coloring import Coloring


class BasicsCollector:

	def __init__(self, settings, modules, coloring):
		self.settings = settings
		self.modules = modules
		self.coloring = coloring

	def get_basics(self, response):
		# output = ''
		module_state = {}
		module_output = ''

		# Getting Title
		# Checking Title in blacklist
		result = re.search(r'<title>(.+)</title>', response.text, re.IGNORECASE)
		title = '-'
		if result is not None:
			title = result.group(1)
		# todo
		# if args.ignore_title is not None and title == args.ignore_title:
		# return
		# output += f' {self.coloring.BLUE}> Title:{self.coloring.RESET} {title}\n'
		module_state['Title'] = title

		# Getting Status-Code
		# output += f' {self.coloring.BLUE}> Status Code:{self.coloring.RESET} {response.status_code}\n'
		module_state['Status-Code'] = response.status_code

		# Getting Content-Length
		if 'Content-Length' in response.headers:
			# output += f' {self.coloring.BLUE}> Content Length:{self.coloring.RESET} {response.headers["content-length"]}\n'
			module_state['Content-Length'] = response.headers["content-length"]

		if 'Content-Security-Policy' in response.headers:
			module_state['CSP'] = response.headers["Content-Security-Policy"]

		for key, value in module_state.items():
			module_output += f' > {self.coloring.BLUE}%s{self.coloring.RESET}: %s\n' % (key, value)

		return module_output, module_state
