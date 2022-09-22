import os
import pathlib

import ulrich



PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
CONF_PATH = PATH / "conf.yaml"

if not CONF_PATH.exists():
    import sys # noqa
    import yaml # noqa
    with open(CONF_PATH, "w") as fp:
        yaml.safe_dump(ulrich.DEFAULT_CONF, fp)
    print(f"New configuration file created at {CONF_PATH!r}")
    sys.exit(1)


app = ulrich.create_app(CONF_PATH)
