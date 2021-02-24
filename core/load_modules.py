import os
import importlib
import sys


def load_modules(coloring, args):
    # 'module-name': {'obj': obj, 'ring': 0, 'banner': 0}
    loaded_modules = 0
    print(' Modules:')
    modules = {
        'peri-modules': {},
        'post-modules': {}
    }
    dirs = os.listdir('%s/../modules/' % os.path.dirname(os.path.realpath(__file__)))
    modules_failed_to_load = False
    for module_name in dirs:
        is_peri_module = False
        is_post_module = False
        try:
            module = importlib.import_module('modules.%s' % module_name).Main(args)
            check_status, check_message = module.check()
            if not check_status:
                print(f' {coloring.RED}[-]{coloring.RESET} %s (%s)' % (module_name, check_message))
                modules_failed_to_load = True
                continue
            if module.MODULE_SETTINGS['peri-module']['is_enabled'] is True:
                modules['peri-modules'][module_name] = {
                    'priority': module.MODULE_SETTINGS['peri-module']['priority'],
                    'banner': module.MODULE_SETTINGS['peri-module']['banner'],
                    'obj': module
                }
                is_peri_module = True
            if module.MODULE_SETTINGS['post-module']['is_enabled'] is True:
                modules['post-modules'][module_name] = {
                    'priority': module.MODULE_SETTINGS['post-module']['priority'],
                    'banner': module.MODULE_SETTINGS['post-module']['banner'],
                    'obj': module
                }
                is_post_module = True
            if is_peri_module or is_post_module:
                type = ''
                if is_peri_module and is_post_module:
                    type = f'({coloring.MAGENTA}peri-module{coloring.RESET} + {coloring.CYAN}post-module{coloring.RESET})'
                elif is_peri_module:
                    type = f'({coloring.MAGENTA}peri-module{coloring.RESET})'
                else:
                    type = f'({coloring.CYAN}post-module{coloring.RESET})'
                print(f' {coloring.GREEN}[+]{coloring.RESET} %s %s' % (module_name, type))
            else:
                print(f' {coloring.RED}[-]{coloring.RESET} %s \t\t\t(%s)' % (module_name, 'Module is disabled!'))

        except Exception as e:
            print(f' {coloring.RED}[-]{coloring.RESET} %s \t\t\t(%s)' % (module_name, 'Undefined error!'))
            modules_failed_to_load = True
            # print(e)
            pass
    print('===============================================================\n\n')
    if modules_failed_to_load:
        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}
        choice = input('At least one module failed to load. Continue anyway? [Yes/No]: ').lower()
        if choice in yes:
            print('\n')
            return modules
        elif choice in no:
            exit(1)
        else:
            sys.stdout.write("You should choose 'Yes' or 'No'")
