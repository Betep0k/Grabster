# default settings
settings = {
    'DEBUG': False,
    'COLORS': True,
    'TIMEOUT': 2,  # requests timeout
    'THREADS': 10,
    'USER-AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0',
    'PROXIES': {
        # 'http': 'socks5://localhost:3333',
        # 'https': 'socks5://localhost:3333',
    },
    'DEFAULT-PORTS': [  # If port is not specified for service
        80,
        443
    ],
    'MODULES': {
        'PATH': [
            './core/modules/',
            './modules/'
        ],
    },
    # 'MODULE-SETTINGS': {
    #     'basics_collector': {
    #         'ENABLED': True,
    #         'PRIORITY': 1,
    #         'SETTINGS': {
    #             'HEADERS': {
    #                 'Location',
    #                 'Server',
    #                 'X-Powered-By',
    #                 'Content-Security-Policy',
    #             }
    #         }
    #     },
    #     'ssl_analyzer': {
    #         'ENABLED': True,
    #         'PRIORITY': 1,
    #     },
    #     'vhost_bruteforcer': {
    #         'ENABLED': True,
    #         'PRIORITY': 1,
    #         'SETTINGS': {
    #             'ANALYZE-FOUND-VHOSTS': True
    #         }
    #     },
    #     'wappalyzer': {
    #         'ENABLED': True,
    #         'PRIORITY': 1,
    #         'SETTINGS': {
    #             'BIN': 'wappalyzer',
    #             'IGNORE-CATEGORIES': {
    #                 19,
    #                 59
    #             },
    #         },
    #     },
    #     'screenshot_collector': {
    #         'ENABLED': True,
    #         'PRIORITY': 1,
    #         'SETTINGS': {
    #             'DEFAULT-DELAY': 1,
    #             'DEFAULT-TIMEOUT': 5,
    #             'DIRECTORY-FOR-SAVE': './screenshots/',
    #         }
    #     },
    #     'csp_analyzer': {
    #         'ENABLED': True,
    #         'PRIORITY': 1,
    #     },
    # }
    'ACTIONS': {
        'basics': True,  # Basic information about web-site
        'headers': True,  # Specific headers
        'ssl': True,  # Parsing of SSL certificate
        'csp': True,
        'status_code': True,
        'redirect': True,
        'title': True,
        'identification': True,  # Identification of technology stack using Wappalyzer
        'screenshots': True,  # Collecting screenshots of main pages
    },
    'MODULE-SETTINGS': {
        'SCREENSHOT-COLLECTOR': {
            'DEFAULT-TARGETS': {
                'main_page': True,
                'vhosts': True  # doesn't work yet
            },
            'DEFAULT-DELAY': 1,
            'DEFAULT-TIMEOUT': 5,
            'DIRECTORY-FOR-SAVE': './screenshots/',
        },
        'HEADER-COLLECTOR': [
            'Location',
            'Server',
            'X-Powered-By',
            'Content-Security-Policy',
        ],
        'WAPPALYZER': {
            'BIN': 'wappalyzer',
            'IGNORE-CATEGORIES': {
                19,
                59
            },
        }
    },
}
