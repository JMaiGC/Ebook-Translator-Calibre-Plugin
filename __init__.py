import os

from calibre.constants import DEBUG
from calibre.customize import InterfaceActionBase


__license__ = 'GPL v3'
__copyright__ = '2023, bookfere.com <bookfere@gmail.com>'
__docformat__ = 'restructuredtext en'

load_translations()


# To prevent update errors, avoid importing anything from plugin modules.
def _z(message): return message


class EbookTranslator(InterfaceActionBase):
    """Development environment requirements for the project:
    - Calibre version: >= 5.0.0
    - Python version: >=3.8.5
    """
    name = _z('Ebook Translator')
    title = _(name)
    supported_platforms = ['windows', 'osx', 'linux']
    identifier = 'ebook-translator'
    author = 'bookfere.com'
    version = (2, 4, 1)
    __version__ = 'v' + '.'.join(map(str, version))
    description = _(
        'A Calibre plugin to translate ebook into a specified language '
        '(optionally keeping the original content).')
    # see: https://www.mobileread.com/forums/showthread.php?t=242223
    minimum_calibre_version = (5, 0, 0)

    actual_plugin = 'calibre_plugins.ebook_translator.ui:EbookTranslatorGui'

    # The DEBUG constant cannot be shared with new worker processes.
    # To ensure that it is available, add it to the OS environment.
    DEBUG and os.environ.update(CALIBRE_DEBUG=str(DEBUG))

    def is_customizable(self):
        return False
