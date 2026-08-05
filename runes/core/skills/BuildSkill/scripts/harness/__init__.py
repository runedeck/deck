"""Harness adapter registry.

Resolves a harness name to its adapter module. See scripts/harness/claude.py
for the adapter contract a new harness module must implement.
"""

from importlib import import_module

_HARNESS_MODULES = {
    "claude": "scripts.harness.claude",
}


def get_harness(name: str):
    """Return the adapter module for the given harness name."""
    try:
        module_path = _HARNESS_MODULES[name]
    except KeyError:
        available = ", ".join(sorted(_HARNESS_MODULES))
        raise ValueError(
            f"Unknown harness '{name}'. Available harnesses: {available}"
        ) from None
    return import_module(module_path)
