import sys

# Always import and patch import hooks before loading anything else
from .internal.import_hooks import patch as patch_import_hooks

patch_import_hooks()  # noqa: E402

from .monkey import patch, patch_all  # noqa: E402
from .pin import Pin  # noqa: E402
from .span import Span  # noqa: E402
from .tracer import Tracer  # noqa: E402
from .settings import config  # noqa: E402
from .utils.deprecation import deprecated  # noqa: E402


__version__ = "0.2.1"


# a global tracer instance with integration settings
tracer = Tracer()

__all__ = [
    "patch",
    "patch_all",
    "Pin",
    "Span",
    "tracer",
    "Tracer",
    "config",
]


_ORIGINAL_EXCEPTHOOK = sys.excepthook


def _excepthook(tp, value, traceback):
    tracer.global_excepthook(tp, value, traceback)
    if _ORIGINAL_EXCEPTHOOK:
        return _ORIGINAL_EXCEPTHOOK(tp, value, traceback)


@deprecated("This method will be removed altogether", "1.0.0")
def install_excepthook():
    """Install a hook that intercepts unhandled exception and send metrics about them."""
    global _ORIGINAL_EXCEPTHOOK
    _ORIGINAL_EXCEPTHOOK = sys.excepthook
    sys.excepthook = _excepthook


@deprecated("This method will be removed altogether", "1.0.0")
def uninstall_excepthook():
    """Uninstall the global tracer except hook."""
    sys.excepthook = _ORIGINAL_EXCEPTHOOK
