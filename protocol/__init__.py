import os
import importlib

__all__ = []

for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or not module.endswith("_pb2.py"):
        continue

    imported = importlib.import_module("." + module[:-3], __name__)

    for imp in dir(imported):
        if not imp or imp.startswith("_") or imp.endswith("_pb2") or imp == "sys":
            continue

        globals()[imp] = getattr(imported, imp)
        __all__.append(imp)

