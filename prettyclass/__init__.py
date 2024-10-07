# -*- coding: utf-8 -*-

# prettyclass
# -----------
# pretty classes - pretty easy.  (created by auxilium)
#
# Author:   sonntagsgesicht
# Version:  0.1, copyright Saturday, 05 October 2024
# Website:  https://github.com/sonntagsgesicht/prettyclass
# License:  Apache License 2.0 (see LICENSE file)


import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

__doc__ = 'pretty classes - pretty easy.  (created by auxilium)'
__license__ = 'Apache License 2.0'

__author__ = 'sonntagsgesicht'
__email__ = 'sonntagsgesicht@icloud.com'
__url__ = 'https://github.com/sonntagsgesicht/prettyclass'

__date__ = 'Monday, 07 October 2024'
__version__ = '0.1.1'
__dev_status__ = '4 - Beta'  # '5 - Production/Stable'

__dependencies__ = ()
__dependency_links__ = ()
__data__ = ()
__scripts__ = ()
__theme__ = ''

from .pp import prettyclass  # noqa F401 E402
