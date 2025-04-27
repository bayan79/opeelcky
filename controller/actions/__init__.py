import importlib
import os
import pkgutil

from .base import ActionArgs, BaseAction
from .const import ActionKeyword

__all__ = ["ActionArgs", "BaseAction", "ActionKeyword"]

# Get the current package path and name
package_path = os.path.dirname(__file__)
package_name = __name__

# Iterate over all modules and sub-packages
for finder, name, is_pkg in pkgutil.iter_modules([package_path]):
    full_name = f"{package_name}.{name}"
    importlib.import_module(full_name)
