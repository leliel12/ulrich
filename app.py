
import os
import pathlib

import ulrich

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
CONF_PATH = PATH / "conf.yaml"


app = ulrich.create_app(CONF_PATH)