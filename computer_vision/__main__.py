'''
__init__.py: Initialization class for the
Computer vision control panel GUI tool.
'''
# This causes linting error because it is similar in another file
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
from main_window_ui import Ui

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

    args = parser.parse_args()
    if not os.path.isfile(args.theme + '.ui'):
        print('Unable to locate the theme file, please check if it exists in the script folder')
        sys.exit(0)
    FULL_SCREEN = args.full_screen.lower() in ['true', 1]
    os.environ['QT_DEVICE_PIXEL_RATIO'] = '0'
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    os.environ['QT_SCREEN_SCALE_FACTORS'] = '1'
    os.environ['QT_SCALE_FACTOR'] = '1'

    HOST = '10.0.10.95' # socket.gethostname()  # when both code is running on same pc
    PORT = 2004  # socket server port number
    window = Ui(args.theme + '.ui', (HOST, PORT), FULL_SCREEN)
    sys.exit(0)
