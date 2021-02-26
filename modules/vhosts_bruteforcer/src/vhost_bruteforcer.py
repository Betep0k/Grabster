import requests
import difflib
import random
import string
import math

from core.queue_jobs import ParserJob


class VHostBruteforcer:

	def __init__(self, settings, modules, coloring):
		self.settings = settings
		self.modules = modules
		self.coloring = coloring
		self.min_diff_rate = 0.60  # default difference rate
		self.max_size_for_diff = 50000
		self.size_diff_rate = 0.01

	# def brute_vhosts(self, host, args, port, proto, vhosts, global_variables, output_queue, parser_queue, state, state_lock):
	def brute_vhosts(self, service, vhosts):
		output = ''
		random_vhost = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
		try:
			response = requests.get('%s://%s:%s' % (service['proto'], service['host'], service['port']), verify=False,
									timeout=self.settings['TIMEOUT'], allow_redirects=False,
									proxies=self.settings['PROXIES'], headers={'Host': random_vhost})
		except:
			return ''
		if self.settings['DEBUG'] is True:
			pass
		# print('[random-vhost: %s; response-size: %s]' % (random_vhost, len(response.text)))
		base_response_text = '%s' % response.text
		base_response_length = len(response.text)
		for vhost in vhosts:
			try:
				response = requests.get('%s://%s:%s' % (service['proto'], service['host'], service['port']), verify=False,
										timeout=self.settings['TIMEOUT'], allow_redirects=False,
										proxies=self.settings['PROXIES'], headers={'Host': vhost})
				response_length = len(response.text)
				if response_length > self.max_size_for_diff:
					diff = response_length/base_response_length
					if abs(diff - 1.0) > self.size_diff_rate:
						output += ' + %s\n' % vhost
						# global_variables['total_services'] += 1
						# # todo: выставил большой host_id, но нужно его считать динамически
						# # возможно придётся добавлять запоминание последнего id в очередь
						# # то есть наследовать свой класс
						# parser_queue.put(ParserJob(999999, host, port, vhost, args, vhosts,
						# 						   global_variables, self.modules, self.settings, output_queue, parser_queue,
						# 						   state, state_lock))
						# with state_lock:
							# state['vhosts'].append({
							# 	'host': host,
							# 	'port': port,
							# 	'vhost': vhost,
							# })
						# if args.get_screenshots is True:
						# 	self.modules['ScreenshotCollector'].add_screenshot_to_queue(proto, host, port, vhost)
				else:
					diff_rate = difflib.SequenceMatcher(None, base_response_text, response.text).ratio()
					if diff_rate < self.min_diff_rate:
						output += ' + %s\n' % vhost
						# global_variables['total_services'] += 1
						# # todo: выставил большой host_id, но нужно его считать динамически
						# # возможно придётся добавлять запоминание последнего id в очередь
						# # то есть наследовать свой класс
						# parser_queue.put(ParserJob(999999, host, port, vhost, args, vhosts,
						# 						   global_variables, self.modules, self.settings, output_queue, parser_queue,
						# 						   state, state_lock))
						# with state_lock:
						# 	state['vhosts'].append({
						# 		'host': host,
						# 		'port': port,
						# 		'vhost': vhost,
						# 	})
						# if args.get_screenshots is True:
						# 	self.modules['ScreenshotCollector'].add_screenshot_to_queue(proto, host, port, vhost)
						# if self.settings['DEBUG'] is True:
						#     pass
						# # print(' + %s [diff: %.2f%%]' % (vhost, diff_rate*100))
						# else:
						#     output += ' + %s\n' % vhost
						#     if args.get_screenshots is True:
						#         self.modules['ScreenshotCollector'].add_screenshot_to_queue(proto, host, port, vhost)
						# csp = self.modules['CSPAnalyzer'].get_csp(response)
						# if csp is not None:
						# 	pass
					elif self.settings['DEBUG'] is True:
						pass
					# print(' - %s [diff: %.2f%%]' % (vhost, diff_rate*100))
			except Exception as e:
				print(e)
				continue
		return output
