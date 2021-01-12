import subprocess
import json

class Wappalyzer:

	def __init__(self, settings, modules, coloring):
		self.settings = settings
		self.modules = modules
		self.coloring = coloring

	def check_availability(self):
		return

	def identification(self, service):

		# todo: придумать, как не переходить по редиректам
		# todo: либо чекать location и отключать wappalyzer для этого хоста
		# todo: еще нужно подумать, как заставить эту фигню работать через прокси

		proto = service['proto']
		ip = service['host']
		port = service['port']
		target = f"{proto}://{ip}:{port}"
		bin = self.settings['MODULE-SETTINGS']['WAPPALYZER']['BIN']
		try:
			module_output = ''
			result = []
			output = subprocess.check_output([bin, target])
			parsed_output = json.loads(output)
			for record in parsed_output['applications']:
				skip = False
				for categorie in record['categories']:
					categorie_id = int(list(categorie.keys())[0])
					if categorie_id in self.settings['MODULE-SETTINGS']['WAPPALYZER']['IGNORE-CATEGORIES']:
						skip = True
						break
				if skip:
					continue
				if record['version']:
					result.append(f"{record['name']} v{record['version']}")
				else:
					result.append(f"{record['name']}")

			for value in result:
				module_output += f' > %s\n' % value

			return module_output, result
		except Exception as e:
			return []