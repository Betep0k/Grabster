import ssl
from OpenSSL import crypto
import re

class SSLAnalyzer:

	def __init__(self, settings, modules, colors):
		self.settings = settings
		self.modules = modules
		self.colors = colors

	def get_domains_from_cert(self, service):
		try:
			if service['proto'] != 'https':
				return None
			output = ''
			cert = ssl.get_server_certificate((service['host'], service['port']))
			x509cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

			issued_to = x509cert.get_subject().CN
			if issued_to and (' ' in issued_to or ';' in issued_to or '.' not in issued_to):
				issued_to = []
			elif not issued_to:
				issued_to = []
			else:
				issued_to = [issued_to]

			san = ''
			ext_count = x509cert.get_extension_count()
			for i in range(0, ext_count):
				ext = x509cert.get_extension(i)
				if 'subjectAltName' in str(ext.get_short_name()):
					try:
						san = ext.__str__()
					except Exception as e:
						# logger.critical(b'Unable to decode subjectAltName: %s' % ext.get_data())
						# logger.critical(e)
						continue

			domain_strings = set(s[4:].replace('\x00', '') if s.startswith('www.') else s.replace('\x00', '') for s in (re.findall(r'DNS:(.*?)(?:\s|,|$)', san) + issued_to) if s)
			domains = set(d.rstrip('.') for d in domain_strings if (d and ' ' not in d and ';' not in d and '.' in d))
			for domain in domains:
				output += f' + {domain}\n'
			return output
		except Exception as e:
			# print(e)
			return ''