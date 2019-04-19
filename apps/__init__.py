import pkgutil
import inspect
import logging

from ti700.app import TerminalApp


logger = logging.getLogger(__name__)

def all_apps():
    apps = []

    for loader, name, is_pkg in pkgutil.walk_packages(__path__):
        module = loader.find_module(name).load_module(name)

        for name, value in inspect.getmembers(module):
            if name.startswith('__'):
                continue
            if inspect.isclass(value) and issubclass(value, TerminalApp) and value != TerminalApp:
                logger.debug(name)
                apps.append(value)
    return apps
