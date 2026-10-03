"""Hardware-wallet provider backed by Bitcoin Core HWI."""
from __future__ import annotations
class HWIProvider:
    name="hwi"
    version="e63a0af2bf5c7c60b8cc71d99aba59068e8be0f0"
    def __init__(self):
        try:
            import hwilib
        except ImportError as e:
            raise RuntimeError("Bitcoin Core HWI dependency is required") from e
        self._hwi=hwilib
    def capabilities(self): return ("device_enumeration","get_xpub","sign_message","sign_transaction")
