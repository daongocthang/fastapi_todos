import importlib
import pkgutil
import types
from typing import Set


def _import_module(name: str) -> types.ModuleType:
    module = importlib.import_module(name)
    return module


def import_submodules(
    package: str | types.ModuleType, recursive: bool = True
) -> Set[types.ModuleType]:
    modules: Set[types.ModuleType] = set()
    if isinstance(package, str):
        package = _import_module(package)
        modules.add(package)

    if not getattr(package, "__path__", None):
        return

    for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = ".".join([package.__name__, name])
        modules.add(_import_module(full_name))
        if recursive and is_pkg:
            import_submodules(full_name)
    return modules
