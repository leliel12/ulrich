"""Utilities to manage and store hiperspectral images of the CONAE
SWIR and VNIR camera.

"""

__version__ = "0.6b"

# =============================================================================
# IMPORTS
# =============================================================================

from .core import DEFAULT_CONF, create_app
from .database import Database


__all__ = [
    "DEFAULT_CONF",
    "create_app",
    "Database",
]
