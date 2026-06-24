# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024, Tiny Tapeout LTD
import os
import sys
def report(dict_or_key: dict, val: str = None):
    if val is not None and not isinstance(dict_or_key, dict):
        dict_or_key = {dict_or_key: val}
    strs = list(map(lambda x: f"{x[0]}={x[1]}", dict_or_key.items()))
    print("\n".join(strs))
print()

# sys.version doesn't always contain a ';' separator. On this build it is
# "MicroPython <hash> on <date>", so split(';')[1] raised IndexError. Guard it
# and fall back to the whole string when there's no ';'.
_ver = sys.version
if ";" in _ver:
    _ver = _ver.split(";")[1].strip()
else:
    _ver = _ver.strip()
report("sys.version", _ver)

def _find_sdk_version():
    # 1) Legacy marker file at filesystem root: release_v<x.y.z>
    try:
        for f in os.listdir("/"):
            if f.startswith("release_v"):
                return f[len("release_v"):] or f
    except Exception:
        pass
    # 2) Newer SDKs expose it on the package
    try:
        import ttboard
        v = getattr(ttboard, "VERSION", None) or getattr(ttboard, "__version__", None)
        if v:
            return v
    except Exception:
        pass
    # 3) Some SDKs carry it on the DemoBoard instance
    try:
        from ttboard.demoboard import DemoBoard
        v = getattr(DemoBoard.get(), "version", None)
        if v:
            return v
    except Exception:
        pass
    return "unknown"

report("tt.sdk_version", _find_sdk_version())
