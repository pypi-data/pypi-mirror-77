__all__ = ['__version__', 'ROOT_DIR', 'STATIC_DIR', 'STATIC_URL', 'TEMPLATES_DIR', 'ASSETS_DIR']

import pathlib
import pkgutil

__version__ = '1.0.0'
ROOT_DIR = pathlib.Path(pkgutil.get_loader('mailtrap').get_filename()).parent
STATIC_DIR = ROOT_DIR / 'static'
TEMPLATES_DIR = ROOT_DIR / 'templates'
ASSETS_DIR = STATIC_DIR / 'assets'
STATIC_URL = '/static/'
