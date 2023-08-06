"""
typhoon.coroutine module
"""
import sys

if sys.version < '3.3':
    from .gen_old import _run_in_executor
elif sys.version < '3.5':
    from .gen_new import _run_in_executor
else:
    from .native import _run_in_executor
