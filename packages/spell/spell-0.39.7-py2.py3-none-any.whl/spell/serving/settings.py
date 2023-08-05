from pathlib import Path

from starlette.config import Config


config = Config("/config/.env")

# Path to the config file"
CONFIG_FILE = config("CONFIG_FILE", cast=Path)
# Path to the Python module containing predictor"
MODULE_PATH = config("MODULE_PATH", cast=Path)
# Python path to the module containing the predictor"
PYTHON_PATH = config("PYTHON_PATH")
# Name of the predictor class"
CLASSNAME = config("CLASSNAME", default=None)
# Run the server in debug mode"
DEBUG = config("DEBUG", cast=bool, default=False)
