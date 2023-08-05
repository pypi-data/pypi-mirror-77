"""
Datacube
========

Provides access to multi-dimensional data, with a focus on Earth observations data such as LANDSAT.

To use this module, see the `Developer Guide <http://datacube-core.readthedocs.io/en/stable/dev/developer.html>`_.

The main class to access the datacube is :class:`datacube.Datacube`.

To initialise this class, you will need a config pointing to a database, such as a file with the following::

    [datacube]
    db_hostname: 130.56.244.227
    db_database: democube
    db_username: cube_user

"""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = 'Unknown/Not Installed'

from .api import Datacube
import warnings
from .utils import xarray_geoextensions

# Ensure deprecation warnings from datacube modules are shown
warnings.filterwarnings('always', category=DeprecationWarning, module=r'^datacube\.')

__all__ = (
    "Datacube",
    "__version__",
    "xarray_geoextensions",
)
