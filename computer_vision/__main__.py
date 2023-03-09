'''
__init__.py: Initialization class for the
Computer vision control panel GUI tool.
'''
# This causes linting error because it is similar in another file
# as described in: https://www.pythonclear.com/programs/python-
#                   file-header/#Format_for_writing_Python_File_Header
# __author__ = 'Asbjørn Stokka'
# __copyright__ = 'Copyright 2023, DATBAC'
# __credits__ = ['Asbjørn Stokka']
# __license__ = 'Apache-2.0'
# __version__ = '0.1.0'
# __maintainer__ = 'Asbjørn Stokka'
# __email__ = 'asbjorn@maxit-as.com'
# __status__ = 'Testing'

import os
import sys
import argparse
import yaml
from main_window_ui import Ui
from main_headless import Headless

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='DATBAC23 Computer vision control interface.')
    parser.add_argument('--theme', dest='theme',
                        default='desktop_design',
                        help='name of theme file (default: desktop_design)')

    parser.add_argument('--full_screen', dest='full_screen',
                        default='false',
                        help='activate full_screen mode (default: false)')

    parser.add_argument('--storage', dest='storage',
                        default='tmp_db.db',
                        help='Choose SQLite storage (default: tmp_db.db)')
    parser.add_argument('--headless', dest='headless',  # in config, not used, could be override
                        default='false',
                        help='activate headless-mode (default: false)')
    parser.add_argument('--config-file', dest='config_file',
                        default='config',
                        help='name of config file (default: config)')


    args = parser.parse_args()
    if not os.path.isfile(args.theme + '.ui'):
        print('Unable to locate the theme file, \
            please check if it exists in the script folder')
        sys.exit(0)

    if not os.path.isfile(args.config_file + '.yml'):
        print('Unable to locate the config file, \
            please check if it exists in the script folder')
        sys.exit(0)

    with open(args.config_file + '.yml', encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    FULL_SCREEN = args.full_screen.lower() in ['true', 1]
    os.environ['QT_DEVICE_PIXEL_RATIO'] = '0'
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    os.environ['QT_SCREEN_SCALE_FACTORS'] = '1'
    os.environ['QT_SCALE_FACTOR'] = '1'

    if config["headless"] is True:
        main_thread = Headless(config)
    else:
        window = Ui(args.theme + '.ui', config, FULL_SCREEN)
    sys.exit(0)
