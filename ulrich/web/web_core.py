# =============================================================================
# DOCS
# =============================================================================

"""Core funcionalities for the Web views of ulrich

"""


# =============================================================================
# IMPORTS
# =============================================================================


import flask
from flask.views import View


# =============================================================================
# BASE CLASS
# =============================================================================


class TemplateView(View):
    def get_template_name(self):
        return self.template_name

    def get_context_data(self):
        return {}

    def render_template(self, context):
        template_name = self.get_template_name()
        return flask.render_template(template_name, **context)

    def dispatch_request(self):
        context = self.get_context_data()
        return self.render_template(context)
