# =============================================================================
# DOCS
# =============================================================================

"""Web views for ulrich

"""

__all__ = ["ulrich_web"]


# =============================================================================
# IMPORTS
# =============================================================================


import flask
from flask.views import View


from .. import (
    __doc__ as ULRICH_RESUME,
    __version__ as ULRICH_VERSION,
    HOMEPAGE,
    LICENSE_URL,
)

# =============================================================================
# Blueprint
# =============================================================================

#: Flask blueprint with the views implemented in arcovid19.
ulrich_web = flask.Blueprint("arcovid19", "arcovid19.web.bp")


@ulrich_web.context_processor
def inject_arcovid19():
    return {
        "ULRICH_RESUME": ULRICH_RESUME,
        "ULRICH_VERSION": ULRICH_VERSION,
        "ULRICH_URL": HOMEPAGE,
        "ULRICH_LICENSE_URL": LICENSE_URL,
    }


# register web views
ulrich_web.add_url_rule("/", view_func=IndexView.as_view("index"))
