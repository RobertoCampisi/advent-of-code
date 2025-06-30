"""
optional extensions for the CLI:
 - rich: for 'rich' text for the terminal
"""
import importlib.util
import sys
from rich.console import Console 

rich_name = 'rich'
rich = None

#class ConsoleDummy:

def lazy_import_rich():
    if (spec := importlib.util.find_spec(rich_name)) is not None:
        # If you chose to perform the actual import ...
        module = importlib.util.module_from_spec(spec)
        sys.modules[rich_name] = module
        spec.loader.exec_module(module)
        importlib.import_module("console", package=rich_name)
        print(f"optinal module {rich_name!r} has been found")
    else:
        print(f"can't find the optinal {rich_name!r} module")
        raise ImportError
    return module    

def init_console():
    if rich_name in sys.modules:
        return Console()
    else:
        return None

def aoc_print(console, *msg):
    if rich_name in sys.modules:
        console.print("[bold green blink]TEST")
        console.print(msg)
    else:
        print(msg)

try:
    rich = lazy_import_rich()    
except ImportError:
    pass


